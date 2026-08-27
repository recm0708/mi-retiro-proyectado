"""Auditor permanente de documentación Markdown del repositorio.

Valida únicamente archivos Markdown rastreados y físicamente presentes.

Reglas:
- UTF-8 sin BOM;
- ausencia de whitespace final;
- H1, salvo excepciones explícitas;
- metadata documental con etiqueta en negrita;
- ausencia de metadata duplicada;
- metadata de versión vigente sincronizada con VERSION;
- ausencia de stubs documentales de compatibilidad;
- enlaces Markdown locales válidos en documentación viva/soporte/plantillas;
- etiquetas humanas en enlaces Markdown navegables de listas documentales;
- coherencia de la reserva revision-aware viva con el ledger machine-readable;
- detección conservadora de prosa inglesa no técnica;
- detección de VERSION antigua dentro de un contexto explícitamente vigente.

Los documentos históricos y auditorías conservan sus versiones, rutas y estados
originales cuando forman parte de la evidencia histórica.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote
import re
import subprocess
import sys


CURRENT_VERSION_FIELDS = {
    "version",
    "version vigente",
    "version canonica vigente",
    "version de aplicacion",
    "version de aplicacion revisada",
    "aplicacion revisada",
    "version revisada",
    "version transversal vigente",
}

METADATA_HINTS = {
    "estado",
    "version",
    "version de aplicacion",
    "version de aplicacion revisada",
    "version base",
    "version base historica",
    "version base historica preservada",
    "clasificacion",
    "fecha",
    "fecha de revision",
    "revision",
    "revision documental",
    "ultima revision",
    "ultima revision documental",
    "ultima actualizacion",
    "proyecto",
    "fase",
    "bloque",
    "alcance",
    "fuente",
    "producto",
    "seccion publica",
    "adr indexadas",
}

SPANISH = {
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "de", "del", "al", "y", "o", "pero", "que", "se", "en",
    "para", "por", "con", "sin", "como", "cuando", "donde",
    "desde", "hasta", "entre", "sobre", "este", "esta", "estos",
    "estas", "ese", "esa", "esos", "esas", "su", "sus", "si",
    "no", "más", "menos", "debe", "deben", "puede", "pueden",
    "permite", "mantiene", "conserva", "archivo", "archivos",
    "documento", "documentos", "documentación", "aplicación",
    "proyecto", "versión", "estado", "revisión", "usuario",
    "usuarios", "datos", "seguridad", "prueba", "pruebas",
    "resultado", "resultados", "cálculo", "cálculos", "actual",
    "vigente", "histórico", "histórica", "repositorio",
}

ENGLISH = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in",
    "on", "for", "with", "without", "from", "into", "this",
    "that", "these", "those", "is", "are", "was", "were",
    "be", "been", "being", "has", "have", "had", "does",
    "do", "did", "not", "only", "when", "where", "while",
    "before", "after", "between", "should", "must", "can",
    "cannot", "will", "would", "file", "files", "document",
    "documents", "documentation", "application", "project",
    "version", "status", "current", "security", "user", "users",
    "data", "test", "tests", "result", "results", "change",
    "changes", "repository", "release", "support", "policy",
}

TECHNICAL_ALLOWED = {
    "github", "python", "fastapi", "jinja2", "javascript",
    "bootstrap", "pydantic", "uvicorn", "pypdf", "dependabot",
    "workflow", "workflows", "commit", "commits", "branch",
    "branches", "pull", "request", "requests", "runtime",
    "framework", "frontend", "backend", "api", "apis",
    "markdown", "readme", "changelog", "release", "releases",
    "tag", "tags", "legacy", "upstream", "downstream",
    "pipeline", "pipelines", "snapshot", "snapshots",
    "ledger", "hook", "hooks", "precommit", "pre-commit",
    "html", "css", "json", "yaml", "powershell", "git",
    "ci", "codeowners", "sbom",
}

H1_EXCEPTIONS = {
    ".github/pull_request_template.md",
}

SUPPORT_FILES = {
    ".github/pull_request_template.md",
    ".githooks/README.md",
    "scripts/README.md",
    "tests/validation_cases/README.md",
}

BOLD_META = re.compile(
    r"^\s*(?:[-*]\s+)?"
    r"\*\*([^*:\n]{1,100}):\*\*\s*(.*)$"
)

PLAIN_META = re.compile(
    r"^\s*(?:[-*]\s+)?"
    r"([A-ZÁÉÍÓÚÑ][^:\n`]{0,90}):\s+(.+)$"
)

LINK_RX = re.compile(
    r"(?<!!)\[[^\]]*\]\(([^)]+)\)"
)

LIST_DOCUMENT_LINK_RX = re.compile(
    r"^\s*[-*]\s+"
    r"(?:\*\*)?"
    r"\[([^\]]+)\]\(([^)]+)\)"
    r"(?:\*\*)?"
)

CANDIDATE_HISTORY_FILES = {
    "CHANGELOG.md",
    "RELEASES.md",
}

VERSION_RX = re.compile(
    r"\d+\.\d+\.\d+(?:\.\d+)?(?:-[A-Za-z0-9.-]+)?"
)


@dataclass(frozen=True)
class Issue:
    path: str
    line: int
    code: str
    detail: str


def normalize(value: str) -> str:
    value = value.strip().lower()

    value = value.translate(
        str.maketrans({
            "á": "a",
            "é": "e",
            "í": "i",
            "ó": "o",
            "ú": "u",
            "ü": "u",
            "ñ": "n",
        })
    )

    return re.sub(r"\s+", " ", value)


def classify(path: str) -> str:
    if path.startswith("docs/archive/"):
        return "HISTORICO"

    if path.startswith("docs/audits/"):
        return "AUDITORIA"

    if path.startswith("docs/templates/"):
        return "PLANTILLA"

    if path in SUPPORT_FILES:
        return "SOPORTE"

    return "VIVO"


def looks_like_metadata(label: str) -> bool:
    value = normalize(label)

    if value in METADATA_HINTS:
        return True

    return value.startswith((
        "estado ",
        "version ",
        "fecha ",
        "revision ",
        "ultima ",
        "ultimo ",
        "clasificacion ",
        "base ",
    ))


def repository_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "No se pudo determinar la raíz del repositorio Git."
        )

    return Path(result.stdout.strip()).resolve()


def tracked_markdown(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "*.md"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "No se pudo obtener el inventario Markdown mediante Git."
        )

    return sorted(
        path
        for path in result.stdout.splitlines()
        if (root / path).is_file()
    )


def strip_link_label_markup(label: str) -> str:
    """Quita únicamente markup simple alrededor de una etiqueta visible."""

    value = label.strip()

    while len(value) >= 2:
        changed = False

        if value.startswith("`") and value.endswith("`"):
            value = value[1:-1].strip()
            changed = True

        if value.startswith("**") and value.endswith("**"):
            value = value[2:-2].strip()
            changed = True

        if value.startswith("__") and value.endswith("__"):
            value = value[2:-2].strip()
            changed = True

        if not changed:
            break

    return value


def looks_like_technical_markdown_label(label: str) -> bool:
    """Detecta nombres/rutas Markdown inequívocamente técnicos."""

    raw = label.strip()
    value = strip_link_label_markup(raw)

    if not value:
        return False

    if raw.startswith("`") and raw.endswith("`"):
        return True

    if value.startswith(("./", "../")):
        return True

    return value.lower().endswith((".md", ".markdown"))


def check_document_link_labels(
    root: Path,
    rel: str,
    lines: list[str],
) -> list[Issue]:
    """Exige título humano solo en listas navegables de documentación activa."""

    if classify(rel) not in {
        "VIVO",
        "SOPORTE",
        "PLANTILLA",
    }:
        return []

    issues = []
    source = root / rel
    in_code = False

    for number, line in enumerate(lines, start=1):
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code = not in_code
            continue

        if in_code:
            continue

        match = LIST_DOCUMENT_LINK_RX.match(line)

        if not match:
            continue

        label = match.group(1).strip()
        raw_target = match.group(2).strip()

        if not looks_like_technical_markdown_label(label):
            continue

        target = unquote(raw_target)
        target = target.split("#", 1)[0]
        target = target.split("?", 1)[0]

        if not target.lower().endswith((".md", ".markdown")):
            continue

        if target.startswith("/"):
            resolved = root / target.lstrip("/")
        else:
            resolved = source.parent / target

        if not resolved.is_file():
            continue

        issues.append(
            Issue(
                rel,
                number,
                "ETIQUETA_DOCUMENTAL_TECNICA",
                (
                    f"{label} -> {raw_target}; "
                    "usar un título humano visible."
                ),
            )
        )

    return issues


def check_current_candidate_state(
    rel: str,
    lines: list[str],
    *,
    next_global: int,
    next_candidate: str,
) -> list[Issue]:
    """Detecta reservas del Global vigente que contradicen el ledger actual."""

    if classify(rel) not in {
        "VIVO",
        "SOPORTE",
        "PLANTILLA",
    }:
        return []

    if rel in CANDIDATE_HISTORY_FILES:
        return []

    issues = []

    expected_match = re.fullmatch(
        r"0\.\d+\.\d+\.(\d{2})-beta",
        next_candidate,
    )

    if not expected_match:
        return []

    expected_edition = int(expected_match.group(1))

    global_pattern = re.compile(
        rf"\bG{next_global:03d}/E(\d{{2}})\b"
    )

    version_prefix = next_candidate.rsplit(".", 1)[0] + "."
    version_pattern = re.compile(
        re.escape(version_prefix) + r"(\d{2})-beta"
    )

    state_words = re.compile(
        r"\b(?:candidat|reserv|siguiente\s+checkpoint)",
        re.I,
    )

    for number, line in enumerate(lines, start=1):
        if not state_words.search(line):
            continue

        editions = {
            int(value)
            for value in global_pattern.findall(line)
        }

        editions.update(
            int(value)
            for value in version_pattern.findall(line)
        )

        wrong = sorted(
            value
            for value in editions
            if value != expected_edition
        )

        if not wrong:
            continue

        issues.append(
            Issue(
                rel,
                number,
                "CANDIDATO_REVISION_AWARE_OBSOLETO",
                (
                    f"Global G{next_global:03d} usa "
                    + ", ".join(f"E{value:02d}" for value in wrong)
                    + f"; candidato actual={next_candidate}"
                ),
            )
        )

    return issues


def load_candidate_state(root: Path) -> tuple[int, str]:
    """Carga el Global siguiente y candidato reservado desde el ledger."""

    import json

    path = root / "data" / "pre-1-0-revision-ledger.json"

    if not path.is_file():
        raise RuntimeError(
            "No existe data/pre-1-0-revision-ledger.json."
        )

    data = json.loads(path.read_text(encoding="utf-8"))

    next_global = data.get(
        "next_global",
        data.get("next_global_if_ver2_accepted"),
    )
    next_candidate = data.get("next_candidate")

    if not isinstance(next_global, int):
        raise RuntimeError(
            "El ledger no declara un siguiente Global válido."
        )

    if not isinstance(next_candidate, str):
        raise RuntimeError(
            "El ledger no declara next_candidate válido."
        )

    return next_global, next_candidate


def clean_prose(line: str) -> str:
    line = re.sub(r"`[^`]*`", " ", line)
    line = re.sub(r"https?://\S+", " ", line)
    line = re.sub(r"\[[^\]]*\]\([^)]+\)", " ", line)
    line = re.sub(r"<[^>]+>", " ", line)
    line = re.sub(r"[|]", " ", line)
    line = re.sub(r"[*_>#~-]", " ", line)
    return line


def metadata_header(
    lines: list[str],
    h1_line: int,
) -> list[tuple[str, str, str, int]]:
    metadata = []

    for number in range(
        h1_line + 1,
        min(len(lines) + 1, h1_line + 50),
    ):
        line = lines[number - 1]

        if re.match(r"^##\s+", line):
            break

        match = BOLD_META.match(line)

        if not match:
            continue

        label = match.group(1).strip()
        value = match.group(2).strip()

        if looks_like_metadata(label):
            metadata.append(
                (
                    normalize(label),
                    label,
                    value,
                    number,
                )
            )

    return metadata


def check_local_links(
    root: Path,
    rel: str,
    lines: list[str],
) -> list[Issue]:
    kind = classify(rel)

    if kind not in {
        "VIVO",
        "SOPORTE",
        "PLANTILLA",
    }:
        return []

    issues = []
    source = root / rel

    in_code = False

    for number, line in enumerate(lines, start=1):
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code = not in_code
            continue

        if in_code:
            continue

        for match in LINK_RX.finditer(line):
            raw_target = match.group(1).strip()

            if not raw_target:
                continue

            if raw_target.startswith("<") and ">" in raw_target:
                raw_target = raw_target[1:raw_target.index(">")]

            # Elimina un título opcional después de la URL/ruta.
            if " \"" in raw_target:
                raw_target = raw_target.split(" \"", 1)[0].strip()

            if " '" in raw_target:
                raw_target = raw_target.split(" '", 1)[0].strip()

            target = unquote(raw_target)

            if target.startswith((
                "#",
                "http://",
                "https://",
                "mailto:",
                "tel:",
            )):
                continue

            target = target.split("#", 1)[0]
            target = target.split("?", 1)[0]

            if not target:
                continue

            if target.startswith("/"):
                resolved = root / target.lstrip("/")
            else:
                resolved = source.parent / target

            if not resolved.exists():
                issues.append(
                    Issue(
                        rel,
                        number,
                        "ENLACE_LOCAL_ROTO",
                        raw_target,
                    )
                )

    return issues


def check_code_fences(
    rel: str,
    lines: list[str],
) -> list[Issue]:
    """Detecta bloques Markdown con triple acento grave sin cerrar."""

    opened_at = None

    for number, line in enumerate(lines, start=1):
        if not line.strip().startswith("```"):
            continue

        if opened_at is None:
            opened_at = number
        else:
            opened_at = None

    if opened_at is None:
        return []

    return [
        Issue(
            rel,
            opened_at,
            "BLOQUE_CODIGO_SIN_CERRAR",
            "Bloque Markdown iniciado con ``` sin cierre.",
        )
    ]


def check_language(
    rel: str,
    lines: list[str],
) -> list[Issue]:
    issues = []
    in_code = False

    for number, line in enumerate(lines, start=1):
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code = not in_code
            continue

        if in_code or not stripped:
            continue

        if stripped.startswith("|"):
            continue

        prose = clean_prose(stripped)

        words = [
            word.lower()
            for word in re.findall(
                r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ-]+",
                prose,
            )
        ]

        words = [
            word
            for word in words
            if word not in TECHNICAL_ALLOWED
        ]

        if len(words) < 10:
            continue

        english_score = sum(
            word in ENGLISH
            for word in words
        )

        spanish_score = sum(
            word in SPANISH
            for word in words
        )

        if (
            english_score >= 6
            and english_score >= spanish_score * 2 + 2
        ):
            issues.append(
                Issue(
                    rel,
                    number,
                    "PROSA_INGLESA_PROBABLE",
                    stripped[:240],
                )
            )

    return issues


def check_current_state_version(
    rel: str,
    lines: list[str],
    current_version: str,
) -> list[Issue]:
    """Detecta una versión antigua dentro de contexto explícitamente vigente."""

    if classify(rel) != "VIVO":
        return []

    issues = []

    pattern = re.compile(
        r"`VERSION`\s+permanece\s+en\s+"
        r"`([^`]+)`",
        re.I,
    )

    for index, line in enumerate(lines):
        match = pattern.search(line)

        if not match:
            continue

        declared = match.group(1)

        if declared == current_version:
            continue

        context = "\n".join(
            lines[max(0, index - 12):index + 1]
        )

        current_context = bool(
            re.search(
                r"(?:Estado vigente|Estado actual|"
                r"Nota de lectura vigente)",
                context,
                re.I,
            )
        )

        if current_context:
            issues.append(
                Issue(
                    rel,
                    index + 1,
                    "VERSION_ANTIGUA_EN_ESTADO_VIGENTE",
                    (
                        f"{declared}; "
                        f"VERSION actual={current_version}"
                    ),
                )
            )

    return issues


def audit_file(
    root: Path,
    rel: str,
    current_version: str,
    *,
    next_global: int | None = None,
    next_candidate: str | None = None,
) -> list[Issue]:
    path = root / rel
    issues = []

    raw = path.read_bytes()

    if raw.startswith(b"\xef\xbb\xbf"):
        issues.append(
            Issue(
                rel,
                1,
                "UTF8_BOM",
                "El archivo contiene BOM UTF-8.",
            )
        )

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [
            Issue(
                rel,
                1,
                "UTF8_INVALIDO",
                str(exc),
            )
        ]

    lines = text.splitlines()

    for number, line in enumerate(lines, start=1):
        if line.endswith((" ", "\t")):
            issues.append(
                Issue(
                    rel,
                    number,
                    "WHITESPACE_FINAL",
                    "Espacio o tabulación al final.",
                )
            )

    h1_lines = [
        number
        for number, line in enumerate(lines, start=1)
        if re.match(r"^#\s+\S", line)
    ]

    if not h1_lines:
        if rel not in H1_EXCEPTIONS:
            issues.append(
                Issue(
                    rel,
                    1,
                    "SIN_H1",
                    "El documento no tiene encabezado H1.",
                )
            )

        issues.extend(
            check_local_links(
                root,
                rel,
                lines,
            )
        )
        issues.extend(
            check_document_link_labels(
                root,
                rel,
                lines,
            )
        )
        if next_global is not None and next_candidate is not None:
            issues.extend(
                check_current_candidate_state(
                    rel,
                    lines,
                    next_global=next_global,
                    next_candidate=next_candidate,
                )
            )
        issues.extend(
            check_language(
                rel,
                lines,
            )
        )

        return issues

    h1_line = h1_lines[0]

    metadata = metadata_header(
        lines,
        h1_line,
    )

    # Metadata que parece documental pero no está en negrita.
    for number in range(
        h1_line + 1,
        min(len(lines) + 1, h1_line + 50),
    ):
        line = lines[number - 1]

        if re.match(r"^##\s+", line):
            break

        if BOLD_META.match(line):
            continue

        match = PLAIN_META.match(line)

        if not match:
            continue

        label = match.group(1).strip()
        value = match.group(2).strip()

        if looks_like_metadata(label):
            issues.append(
                Issue(
                    rel,
                    number,
                    "METADATA_SIN_NEGRITA",
                    f"{label}: {value}",
                )
            )

    grouped = defaultdict(list)

    for item in metadata:
        grouped[item[0]].append(item)

    for key, occurrences in grouped.items():
        if len(occurrences) <= 1:
            continue

        issues.append(
            Issue(
                rel,
                occurrences[0][3],
                "METADATA_REPETIDA",
                (
                    f"{occurrences[0][1]} -> "
                    + " | ".join(
                        item[2]
                        for item in occurrences
                    )
                ),
            )
        )

    if classify(rel) == "VIVO":
        for norm, label, value, number in metadata:
            if norm not in CURRENT_VERSION_FIELDS:
                continue

            versions = VERSION_RX.findall(value)

            if (
                versions
                and current_version not in versions
            ):
                issues.append(
                    Issue(
                        rel,
                        number,
                        "VERSION_VIVA_NO_ACTUAL",
                        f"{label}: {value}",
                    )
                )

    for number, line in enumerate(lines, start=1):
        low = normalize(line)

        if (
            "permanece unicamente como ruta de compatibilidad"
            in low
            or "redirect documental" in low
        ):
            if rel != (
                "docs/standards/"
                "documentation-standards.md"
            ):
                issues.append(
                    Issue(
                        rel,
                        number,
                        "STUB_COMPATIBILIDAD",
                        line.strip(),
                    )
                )

    issues.extend(
        check_code_fences(
            rel,
            lines,
        )
    )

    issues.extend(
        check_local_links(
            root,
            rel,
            lines,
        )
    )

    issues.extend(
        check_document_link_labels(
            root,
            rel,
            lines,
        )
    )

    if next_global is not None and next_candidate is not None:
        issues.extend(
            check_current_candidate_state(
                rel,
                lines,
                next_global=next_global,
                next_candidate=next_candidate,
            )
        )

    issues.extend(
        check_language(
            rel,
            lines,
        )
    )

    issues.extend(
        check_current_state_version(
            rel,
            lines,
            current_version,
        )
    )

    return issues


def audit_repository(
    root: Path,
) -> tuple[list[Issue], Counter[str], int]:
    version_path = root / "VERSION"

    if not version_path.is_file():
        raise RuntimeError(
            "No existe el archivo canónico VERSION."
        )

    current_version = version_path.read_text(
        encoding="utf-8"
    ).strip()

    files = tracked_markdown(root)
    next_global, next_candidate = load_candidate_state(root)

    counts = Counter(
        classify(path)
        for path in files
    )

    issues = []

    for rel in files:
        issues.extend(
            audit_file(
                root,
                rel,
                current_version,
                next_global=next_global,
                next_candidate=next_candidate,
            )
        )

    return issues, counts, len(files)


def main() -> int:
    try:
        root = repository_root()
        issues, counts, total = audit_repository(
            root
        )
    except RuntimeError as exc:
        print(
            f"[markdown] ERROR: {exc}",
            file=sys.stderr,
        )
        return 2

    print(
        f"[markdown] Archivos Markdown auditados: {total}"
    )

    for kind in (
        "VIVO",
        "AUDITORIA",
        "HISTORICO",
        "PLANTILLA",
        "SOPORTE",
    ):
        print(
            f"[markdown] {kind}: "
            f"{counts.get(kind, 0)}"
        )

    if issues:
        print()
        print(
            f"[markdown] ERROR: "
            f"{len(issues)} problema(s) detectado(s)."
        )

        for issue in issues:
            print(
                f"{issue.path}:{issue.line} "
                f"[{issue.code}]"
            )
            print(
                f"  {issue.detail}"
            )

        return 1

    print(
        "[markdown] OK: documentación Markdown "
        "sin problemas bloqueantes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
