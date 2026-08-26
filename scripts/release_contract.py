"""Valida y presenta el contrato local de tags y GitHub Releases pre-1.0."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_PATH = ROOT / "VERSION"
LEDGER_PATH = ROOT / "data" / "pre-1-0-revision-ledger.json"

REVISION_AWARE_RE = re.compile(r"^0\.(?P<gg>\d+)\.(?P<rr>\d{2})\.(?P<ee>\d{2})-beta$")
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
    return VERSION_PATH.read_text(encoding="utf-8").strip()


def read_ledger() -> dict:
    return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))


def parse_revision_aware(version: str) -> tuple[int, int]:
    match = REVISION_AWARE_RE.fullmatch(version)
    if not match:
        raise ValueError(f"Versión beta revision-aware no válida: {version}")
    global_revision = int(match.group("gg")) * 100 + int(match.group("rr"))
    edition = int(match.group("ee"))
    return global_revision, edition


def expected_title(version: str) -> str:
    global_revision, edition = parse_revision_aware(version)
    return f"Mi Retiro Proyectado v{version} — G{global_revision:03d}/E{edition:02d}"


def validate_version_against_ledger(version: str, ledger: dict) -> list[str]:
    errors: list[str] = []
    global_revision, _ = parse_revision_aware(version)
    accepted_count = int(ledger["accepted_count"])
    next_global = int(ledger["next_global"])
    next_candidate = str(ledger["next_candidate"])

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
        if next_candidate != version:
            errors.append(
                f"El candidato G{global_revision:03d} esperado es {next_candidate}, no {version}."
            )
    else:
        errors.append(
            "VERSION debe corresponder al último G aceptado o al siguiente candidato reservado "
            f"(aceptado=G{accepted_count:03d}, siguiente=G{next_global:03d})."
        )
    return errors


def validate_notes(text: str) -> list[str]:
    return [f"Falta la sección obligatoria: {heading}" for heading in REQUIRED_HEADINGS if heading not in text]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-tag", help="Valida que el tag sea v<VERSION>.")
    parser.add_argument("--check-title", help="Valida el título canónico del GitHub Release.")
    parser.add_argument("--check-notes", type=Path, help="Valida secciones mínimas del cuerpo del Release.")
    parser.add_argument("--print-title", action="store_true", help="Imprime el título canónico.")
    parser.add_argument("--json", action="store_true", help="Imprime el contrato calculado como JSON.")
    return parser


def main() -> int:
    configure_utf8_stdio()
    args = build_parser().parse_args()
    version = read_version()
    ledger = read_ledger()
    global_revision, edition = parse_revision_aware(version)
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
