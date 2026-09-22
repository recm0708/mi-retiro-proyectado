"""Valida y presenta el contrato local de tags y GitHub Releases pre-1.0."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_PATH = ROOT / "VERSION"
LEDGER_PATH = ROOT / "data" / "governance" / "pre-1-0-revision-ledger.json"

REVISION_AWARE_V1_RE = re.compile(
    r"^0\.(?P<g_hi>0|[1-9][0-9]*)"
    r"\.(?P<g_lo>[0-9]{2})"
    r"\.(?P<ee>[0-9]{2})"
    r"-beta$"
)

REVISION_AWARE_V2_RE = re.compile(
    r"^0\.(?P<global>[1-9][0-9]*)"
    r"\.(?P<ee>[1-9][0-9]*)"
    r"\.(?P<correction>0|[1-9][0-9]*)"
    r"-beta$"
)
REQUIRED_HEADINGS = (
    "## Estado publicado",
    "## Resumen",
    "## Cambios principales",
    "## Validación",
    "## Evidencia",
    "## Siguiente paso",
)


def configure_utf8_stdio() -> None:
    """Fija UTF-8 para salida CLI también cuando Python escribe a un pipe en Windows."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="strict")


def read_version() -> str:
    """Lee VERSION y devuelve la versión canónica del repositorio."""
    return VERSION_PATH.read_text(encoding="utf-8").strip()


def read_ledger() -> dict:
    """Carga el ledger revision-aware usado por el contrato de release."""
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def parse_revision_aware_components(
    version: str,
) -> tuple[int, int, int, int, int]:
    """Descompone v1/v2 en Global, Edition, Correction, compat y schema.

    El cuarto valor se conserva por compatibilidad de API, pero el ordinal
    MANT.2 ya no se codifica en VERSION y por ello siempre vale 0 aquí.
    """

    match_v2 = REVISION_AWARE_V2_RE.fullmatch(version)
    if match_v2 is not None:
        global_revision = int(match_v2.group("global"))
        edition = int(match_v2.group("ee"))
        correction = int(match_v2.group("correction"))

        if global_revision < 128:
            raise ValueError(
                "La familia revision-aware v2 comienza en G128."
            )
        if not 1 <= edition <= 99:
            raise ValueError("Edition debe estar entre 1 y 99.")
        if not 0 <= correction <= 999:
            raise ValueError("Correction debe estar entre 0 y 999.")

        return global_revision, edition, correction, 0, 2

    match_v1 = REVISION_AWARE_V1_RE.fullmatch(version)
    if match_v1 is None:
        raise ValueError(
            "Versión beta revision-aware no válida: " + version
        )

    global_revision = (
        int(match_v1.group("g_hi")) * 100
        + int(match_v1.group("g_lo"))
    )
    edition = int(match_v1.group("ee"))

    if global_revision <= 0 or edition <= 0:
        raise ValueError("Global y Edition deben ser mayores que cero.")

    return global_revision, edition, 0, 0, 1

def parse_revision_aware(
    version: str,
) -> tuple[int, int]:
    """Conserva el contrato histórico ``(Global, Edition)``."""

    (
        global_revision,
        edition,
        _correction,
        _maintenance,
        _schema,
    ) = parse_revision_aware_components(
        version
    )

    return (
        global_revision,
        edition,
    )


def expected_title(version: str) -> str:
    """Construye el título canónico esperado para una publicación."""
    global_revision, edition = parse_revision_aware(version)
    return f"Mi Retiro Proyectado v{version} — G{global_revision:03d}/E{edition:02d}"


def validate_version_against_ledger(version: str, ledger: dict) -> list[str]:
    """Comprueba que VERSION y ledger describan el mismo estado aceptado."""
    errors: list[str] = []
    global_revision, _ = parse_revision_aware(version)
    accepted_count = int(ledger["accepted_count"])
    next_global = int(ledger["next_global"])
    next_candidate = ledger.get("next_candidate")

    if global_revision == accepted_count:
        matches = [
            entry
            for entry in ledger["entries"]
            if int(entry["global_revision"]) == global_revision
        ]
        if len(matches) != 1:
            errors.append(f"El ledger debe contener exactamente una entrada G{global_revision:03d}.")
        elif matches[0]["revision_aware"] != version:
            errors.append(
                f"La entrada G{global_revision:03d} usa {matches[0]['revision_aware']} y no {version}."
            )
    elif global_revision == next_global:
        if not isinstance(next_candidate, str) or not next_candidate.strip():
            errors.append(
                f"G{global_revision:03d} está disponible, pero no existe "
                "candidato revision-aware reservado."
            )
        elif next_candidate != version:
            errors.append(
                f"El candidato G{global_revision:03d} esperado es "
                f"{next_candidate}, no {version}."
            )
    else:
        errors.append(
            "VERSION debe corresponder al último G aceptado o al siguiente candidato reservado "
            f"(aceptado=G{accepted_count:03d}, siguiente=G{next_global:03d})."
        )
    return errors


def validate_notes(text: str) -> list[str]:
    """Valida que las notas de release contengan las secciones obligatorias."""
    return [f"Falta la sección obligatoria: {heading}" for heading in REQUIRED_HEADINGS if heading not in text]


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser de argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-tag", help="Valida que el tag sea v<VERSION>.")
    parser.add_argument("--check-title", help="Valida el título canónico del GitHub Release.")
    parser.add_argument("--check-notes", type=Path, help="Valida secciones mínimas del cuerpo del Release.")
    parser.add_argument("--print-title", action="store_true", help="Imprime el título canónico.")
    parser.add_argument("--json", action="store_true", help="Imprime el contrato calculado como JSON.")
    return parser


def main() -> int:
    """Ejecuta el flujo principal del script y devuelve el código de salida."""
    configure_utf8_stdio()
    args = build_parser().parse_args()
    version = read_version()
    ledger = read_ledger()
    (
        global_revision,
        edition,
        correction,
        maintenance,
        revision_schema,
    ) = parse_revision_aware_components(
        version
    )
    title = expected_title(version)

    errors = validate_version_against_ledger(version, ledger)
    if args.check_tag and args.check_tag != f"v{version}":
        errors.append(f"Tag inválido: se esperaba v{version} y se recibió {args.check_tag}.")
    if args.check_title and args.check_title != title:
        errors.append(f"Título inválido: se esperaba '{title}'.")
    if args.check_notes:
        errors.extend(validate_notes(args.check_notes.read_text(encoding="utf-8-sig")))

    contract = {
        "version": version,
        "tag": f"v{version}",
        "global_revision": global_revision,
        "edition": edition,
        "correction": correction,
        "maintenance": maintenance,
        "revision_schema": revision_schema,
        "title": title,
        "prerelease": version.endswith("-beta"),
        "accepted_count": int(ledger["accepted_count"]),
        "next_global": int(ledger["next_global"]),
        "next_candidate": ledger["next_candidate"],
        "next_candidate_block": ledger.get("next_candidate_block"),
    }

    if errors:
        for error in errors:
            print(f"[release-contract] ERROR: {error}")
        return 1

    if args.json:
        print(json.dumps(contract, ensure_ascii=False, indent=2))
    elif args.print_title:
        print(title)
    elif not any((args.check_tag, args.check_title, args.check_notes)):
        print(
            "[release-contract] OK: "
            f"{contract['tag']} | G{global_revision:03d}/E{edition:02d} | {title}"
        )
    else:
        print("[release-contract] OK: contrato validado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
