"""Auditoría estructural y documental del repositorio.

Responsabilidad:
- derivar la estructura versionable desde Git;
- contrastar el árbol canónico documentado en README;
- detectar divergencias estructurales y documentales.

Límites:
- no modifica archivos del proyecto;
- no inspecciona contenido ignorado por Git;
- no valida URLs externas;
- no sustituye revisión semántica humana.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

EXCLUDED_ORPHAN_PREFIXES = (
    "docs/archive/",
    "docs/audits/",
    "docs/templates/",
)

EXCLUDED_LINK_SOURCE_PREFIXES = (
    "docs/archive/",
)


def link_source_is_enforced(
    source: str,
) -> bool:
    """Indica si los enlaces locales de una fuente son bloqueantes.

    La documentación histórica puede conservar referencias válidas en el
    contexto de su época. Reescribirlas alteraría evidencia archivada.
    """

    return not source.startswith(
        EXCLUDED_LINK_SOURCE_PREFIXES
    )


def run_git(*args: str) -> str:
    """Ejecuta Git y devuelve stdout UTF-8."""

    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Falló git "
            + " ".join(args)
            + ":\n"
            + result.stdout
            + result.stderr
        )

    return result.stdout


def repository_files() -> list[str]:
    """Devuelve archivos rastreados y no ignorados del workspace."""

    output = run_git(
        "ls-files",
        "--cached",
        "--others",
        "--exclude-standard",
    )

    return sorted(
        {
            line.strip().replace("\\", "/")
            for line in output.splitlines()
            if line.strip()
        }
    )


def canonical_directories(
    files: list[str],
) -> set[str]:
    """Deriva todos los directorios versionables."""

    directories: set[str] = set()

    for rel in files:
        parts = rel.split("/")

        for index in range(1, len(parts)):
            directories.add(
                "/".join(parts[:index])
            )

    return directories


def root_files(
    files: list[str],
) -> set[str]:
    """Devuelve archivos ubicados en la raíz."""

    return {
        rel
        for rel in files
        if "/" not in rel
    }


def readme_tree_block() -> str:
    """Obtiene el bloque de arquitectura canónica del README."""

    text = README.read_text(
        encoding="utf-8"
    )

    match = re.search(
        r"## Arquitectura canónica del repositorio"
        r".*?```text\s*\n"
        r"(?P<tree>.*?)"
        r"\n```",
        text,
        flags=re.DOTALL,
    )

    if match is None:
        raise ValueError(
            "README no contiene el árbol canónico esperado."
        )

    return match.group("tree")


def parse_readme_tree() -> tuple[set[str], set[str]]:
    """Reconstruye directorios y archivos raíz del árbol README."""

    tree = readme_tree_block()

    directories: set[str] = set()
    files_at_root: set[str] = set()
    stack: dict[int, str] = {}

    pattern = re.compile(
        r"^(?P<prefix>(?:(?:│   |    ))*)"
        r"(?:├── |└── )"
        r"(?P<name>.+?)\s*$"
    )

    for line in tree.splitlines():
        match = pattern.match(line)

        if match is None:
            continue

        prefix = match.group("prefix")
        name = match.group("name").strip()
        depth = (len(prefix) // 4) + 1

        for old_depth in list(stack):
            if old_depth >= depth:
                del stack[old_depth]

        if name.endswith("/"):
            component = name[:-1]

            if depth == 1:
                full = component
            else:
                parent = stack.get(depth - 1)

                if parent is None:
                    raise ValueError(
                        "Árbol README mal formado cerca de: "
                        + line
                    )

                full = parent + "/" + component

            directories.add(full)
            stack[depth] = full
            continue

        if depth == 1:
            files_at_root.add(name)

    return directories, files_at_root


def without_fenced_code(
    text: str,
) -> str:
    """Retira bloques de código para no interpretar ejemplos como enlaces."""

    return re.sub(
        r"```.*?```",
        "",
        text,
        flags=re.DOTALL,
    )


def markdown_targets(
    text: str,
) -> list[str]:
    """Extrae destinos Markdown inline y por referencia."""

    clean = without_fenced_code(text)

    inline = re.findall(
        r"!?\[[^\]]*\]\(([^)]+)\)",
        clean,
    )

    references = re.findall(
        r"^\s*\[[^\]]+\]:\s*(\S+)",
        clean,
        flags=re.MULTILINE,
    )

    return inline + references


def clean_target(
    raw: str,
) -> str | None:
    """Normaliza un destino Markdown local."""

    target = raw.strip()

    if not target:
        return None

    if target.startswith("<"):
        closing = target.find(">")

        if closing > 0:
            target = target[1:closing]
    else:
        target = target.split(None, 1)[0]

    target = unquote(target.strip())
    lower = target.lower()

    if (
        target.startswith("#")
        or lower.startswith("http://")
        or lower.startswith("https://")
        or lower.startswith("mailto:")
        or lower.startswith("tel:")
    ):
        return None

    if any(
        token in target
        for token in ("{", "}", "*")
    ):
        return None

    target = target.split("#", 1)[0]
    target = target.split("?", 1)[0]
    target = target.strip()

    return target or None


def resolve_local_target(
    source: str,
    target: str,
) -> str:
    """Resuelve un enlace relativo a una ruta Git POSIX."""

    if target.startswith("/"):
        return target.lstrip("/")

    return posixpath.normpath(
        posixpath.join(
            posixpath.dirname(source),
            target,
        )
    )


def local_link_analysis(
    files: list[str],
    directories: set[str],
) -> tuple[
    list[dict[str, str]],
    dict[str, int],
]:
    """Detecta referencias locales rotas y referencias entrantes."""

    file_set = set(files)

    markdown = {
        rel
        for rel in files
        if rel.lower().endswith(".md")
    }

    inbound = {
        rel: 0
        for rel in markdown
    }

    broken: list[dict[str, str]] = []

    for source in sorted(markdown):
        if not link_source_is_enforced(source):
            continue

        path = ROOT / source

        try:
            text = path.read_text(
                encoding="utf-8-sig"
            )
        except OSError:
            broken.append(
                {
                    "source": source,
                    "target": "<unreadable>",
                    "resolved": source,
                }
            )
            continue

        for raw_target in markdown_targets(text):
            target = clean_target(raw_target)

            if target is None:
                continue

            resolved = resolve_local_target(
                source,
                target,
            )

            if (
                resolved == "."
                or resolved in directories
                or resolved in file_set
            ):
                if (
                    resolved in inbound
                    and resolved != source
                ):
                    inbound[resolved] += 1

                continue

            broken.append(
                {
                    "source": source,
                    "target": target,
                    "resolved": resolved,
                }
            )

    return broken, inbound


def live_document_candidates(
    files: list[str],
) -> list[str]:
    """Selecciona documentación viva sujeta a descubribilidad."""

    result = []

    for rel in files:
        if not (
            rel.startswith("docs/")
            and rel.lower().endswith(".md")
        ):
            continue

        if rel.startswith(
            EXCLUDED_ORPHAN_PREFIXES
        ):
            continue

        result.append(rel)

    return sorted(result)


def orphan_documents(
    files: list[str],
    inbound: dict[str, int],
) -> list[str]:
    """Detecta documentación viva sin referencias entrantes."""

    return [
        rel
        for rel in live_document_candidates(files)
        if inbound.get(rel, 0) == 0
    ]


def trivial_stubs(
    files: list[str],
) -> list[str]:
    """Detecta documentos vivos trivialmente pequeños."""

    stubs = []

    for rel in live_document_candidates(files):
        if rel.endswith("/README.md"):
            continue

        path = ROOT / rel

        try:
            text = path.read_text(
                encoding="utf-8-sig"
            )
        except OSError:
            continue

        nonempty = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if (
            len(text.strip()) < 240
            and len(nonempty) <= 8
        ):
            stubs.append(rel)

    return sorted(stubs)


def normalized_markdown(
    text: str,
) -> str:
    """Normaliza Markdown conservadoramente para detectar duplicados."""

    lines = [
        line.rstrip()
        for line in text.replace(
            "\r\n",
            "\n",
        ).replace(
            "\r",
            "\n",
        ).splitlines()
    ]

    normalized = "\n".join(lines).strip()

    return re.sub(
        r"\n{3,}",
        "\n\n",
        normalized,
    )


def duplicate_groups(
    files: list[str],
) -> tuple[
    list[list[str]],
    list[list[str]],
]:
    """Detecta duplicados exactos y normalizados de Markdown."""

    exact: dict[str, list[str]] = defaultdict(list)
    normalized: dict[str, list[str]] = defaultdict(list)

    for rel in files:
        if not rel.lower().endswith(".md"):
            continue

        path = ROOT / rel

        try:
            raw = path.read_bytes()
        except OSError:
            continue

        exact_digest = hashlib.sha256(
            raw
        ).hexdigest()

        exact[exact_digest].append(rel)

        text = raw.decode(
            "utf-8-sig",
            errors="replace",
        )

        normalized_digest = hashlib.sha256(
            normalized_markdown(text).encode(
                "utf-8"
            )
        ).hexdigest()

        normalized[
            normalized_digest
        ].append(rel)

    exact_groups = sorted(
        sorted(group)
        for group in exact.values()
        if len(group) > 1
    )

    normalized_groups = sorted(
        sorted(group)
        for group in normalized.values()
        if len(group) > 1
    )

    return exact_groups, normalized_groups


def audit_repository() -> dict:
    """Ejecuta la auditoría integral del repositorio."""

    files = repository_files()

    directories = canonical_directories(files)
    roots = root_files(files)

    (
        readme_directories,
        readme_roots,
    ) = parse_readme_tree()

    broken, inbound = local_link_analysis(
        files,
        directories,
    )

    orphans = orphan_documents(
        files,
        inbound,
    )

    stubs = trivial_stubs(files)

    (
        exact_duplicates,
        normalized_duplicates,
    ) = duplicate_groups(files)

    blockers = {
        "missing_directories": sorted(
            directories - readme_directories
        ),
        "extra_directories": sorted(
            readme_directories - directories
        ),
        "missing_root_files": sorted(
            roots - readme_roots
        ),
        "extra_root_files": sorted(
            readme_roots - roots
        ),
        "broken_local_links": broken,
        "orphan_live_documents": orphans,
        "trivial_stubs": stubs,
        "exact_duplicate_groups": exact_duplicates,
        "normalized_duplicate_groups": normalized_duplicates,
    }

    failed = any(
        bool(value)
        for value in blockers.values()
    )

    return {
        "schema_version": 1,
        "result": (
            "fail"
            if failed
            else "pass"
        ),
        "inventory": {
            "repository_files": len(files),
            "canonical_directories": len(
                directories
            ),
            "readme_directories": len(
                readme_directories
            ),
            "root_files": len(roots),
            "readme_root_files": len(
                readme_roots
            ),
            "markdown_files": len(
                [
                    rel
                    for rel in files
                    if rel.lower().endswith(".md")
                ]
            ),
            "live_document_candidates": len(
                live_document_candidates(files)
            ),
        },
        "blockers": blockers,
    }


def print_report(
    report: dict,
) -> None:
    """Muestra resumen y divergencias detectadas."""

    inventory = report["inventory"]
    blockers = report["blockers"]

    print(
        "[repository-integrity] "
        f"Archivos Git/versionables: "
        f"{inventory['repository_files']}"
    )

    print(
        "[repository-integrity] "
        f"Directorios canónicos: "
        f"{inventory['canonical_directories']}"
    )

    print(
        "[repository-integrity] "
        f"Directorios README: "
        f"{inventory['readme_directories']}"
    )

    print(
        "[repository-integrity] "
        f"Archivos raíz: "
        f"{inventory['root_files']}"
    )

    print(
        "[repository-integrity] "
        f"Markdown: "
        f"{inventory['markdown_files']}"
    )

    labels = (
        (
            "Directorios faltantes en README",
            "missing_directories",
        ),
        (
            "Directorios extra en README",
            "extra_directories",
        ),
        (
            "Archivos raíz faltantes en README",
            "missing_root_files",
        ),
        (
            "Archivos raíz extra en README",
            "extra_root_files",
        ),
        (
            "Enlaces locales rotos",
            "broken_local_links",
        ),
        (
            "Documentos vivos huérfanos",
            "orphan_live_documents",
        ),
        (
            "Stubs triviales",
            "trivial_stubs",
        ),
        (
            "Grupos duplicados exactos",
            "exact_duplicate_groups",
        ),
        (
            "Grupos duplicados normalizados",
            "normalized_duplicate_groups",
        ),
    )

    for label, key in labels:
        values = blockers[key]

        print(
            "[repository-integrity] "
            f"{label}: {len(values)}"
        )

        for value in values[:10]:
            if isinstance(value, dict):
                print(
                    "  - "
                    + value["source"]
                    + " -> "
                    + value["target"]
                    + " => "
                    + value["resolved"]
                )
            elif isinstance(value, list):
                print(
                    "  - "
                    + " | ".join(value)
                )
            else:
                print(
                    "  - "
                    + str(value)
                )

    if report["result"] == "pass":
        print(
            "[repository-integrity] "
            "OK: estructura, referencias y documentación "
            "sin divergencias bloqueantes."
        )
    else:
        print(
            "[repository-integrity] "
            "ERROR: se detectaron divergencias bloqueantes.",
            file=sys.stderr,
        )


def parser() -> argparse.ArgumentParser:
    """Construye la CLI."""

    p = argparse.ArgumentParser(
        description=__doc__,
    )

    p.add_argument(
        "--json",
        action="store_true",
        help="Imprime además el reporte JSON.",
    )

    return p


def main() -> int:
    """Punto de entrada CLI."""

    args = parser().parse_args()

    try:
        report = audit_repository()
    except (
        OSError,
        RuntimeError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
        print(
            "[repository-integrity] ERROR: "
            + str(exc),
            file=sys.stderr,
        )
        return 1

    print_report(report)

    if args.json:
        print(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            )
        )

    return (
        0
        if report["result"] == "pass"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
