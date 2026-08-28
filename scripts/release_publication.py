"""Gobierna manifiesto, notas e idempotencia de GitHub Releases."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from release_contract import (
    expected_title,
    parse_revision_aware,
    read_ledger,
    read_version,
    validate_notes,
    validate_version_against_ledger,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "release-publication-manifest.json"


def configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="strict")


def load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} debe contener un objeto JSON.")
    return data


def _validate_text_list(data: dict, field: str, errors: list[str]) -> None:
    value = data.get(field)
    if not isinstance(value, list) or not value:
        errors.append(f"{field} debe ser una lista no vacía.")
        return
    if any(not isinstance(item, str) or not item.strip() for item in value):
        errors.append(f"{field} solo puede contener texto no vacío.")


def validate_manifest(manifest: dict, version: str, ledger: dict) -> list[str]:
    errors = validate_version_against_ledger(version, ledger)

    if manifest.get("schema_version") != 1:
        errors.append("schema_version debe ser 1.")

    if manifest.get("version") != version:
        errors.append(
            "El manifiesto no corresponde a VERSION: "
            f"{manifest.get('version')!r} != {version!r}."
        )

    global_revision, edition = parse_revision_aware(version)
    entries = [
        entry
        for entry in ledger["entries"]
        if int(entry["global_revision"]) == global_revision
    ]

    if len(entries) != 1:
        errors.append(
            f"Debe existir una única entrada G{global_revision:03d}."
        )
    else:
        entry = entries[0]
        if manifest.get("block") != entry.get("block"):
            errors.append(
                "El bloque del manifiesto no coincide con el ledger."
            )
        expected_revision = f"R{int(entry['ordinal'])}"
        if manifest.get("revision") != expected_revision:
            errors.append(
                f"La revisión esperada es {expected_revision}."
            )
        if int(entry["ordinal"]) != edition:
            errors.append(
                f"E{edition:02d} no coincide con el ordinal "
                f"{entry['ordinal']} del bloque."
            )

    for field in ("summary", "changes", "validation", "evidence"):
        _validate_text_list(manifest, field, errors)

    next_step = manifest.get("next_step")
    if not isinstance(next_step, dict):
        errors.append("next_step debe ser un objeto.")
    else:
        expected = {
            "global_revision": int(ledger["next_global"]),
            "revision_aware": str(ledger["next_candidate"]),
            "block": ledger.get("next_candidate_block"),
        }
        for field, expected_value in expected.items():
            if next_step.get(field) != expected_value:
                errors.append(
                    f"next_step.{field}={next_step.get(field)!r}; "
                    f"se esperaba {expected_value!r}."
                )
        description = next_step.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append("next_step.description debe contener texto.")

    return errors


def _run_git(*args: str) -> str:
    cp = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if cp.returncode != 0:
        raise RuntimeError(
            f"Falló git {' '.join(args)}:\n{cp.stdout}{cp.stderr}"
        )
    return cp.stdout.strip()


def resolve_tag(tag: str) -> tuple[str, str]:
    object_type = _run_git("cat-file", "-t", tag)
    if object_type != "tag":
        raise ValueError(f"{tag} no es un tag anotado.")
    return (
        _run_git("rev-parse", f"{tag}^{{}}"),
        _run_git("rev-parse", tag),
    )


def render_notes(
    manifest: dict,
    published_commit: str,
    tag_object: str,
) -> str:
    version = str(manifest["version"])
    global_revision, edition = parse_revision_aware(version)
    tag = f"v{version}"
    publication_type = (
        "prerelease beta"
        if version.endswith("-beta")
        else "release estable"
    )

    lines = [
        "## Estado publicado",
        "",
        f"- **Versión:** `{version}`",
        f"- **Tag:** `{tag}`",
        f"- **Estado revision-aware:** G{global_revision:03d}/E{edition:02d}",
        f"- **Bloque aceptado:** {manifest['block']} {manifest['revision']}",
        f"- **Commit publicado:** `{published_commit}`",
        f"- **Objeto de tag firmado:** `{tag_object}`",
        f"- **Tipo:** {publication_type}",
        "",
        "## Resumen",
        "",
    ]

    for index, paragraph in enumerate(manifest["summary"]):
        if index:
            lines.append("")
        lines.append(paragraph)

    for heading, field in (
        ("## Cambios principales", "changes"),
        ("## Validación", "validation"),
        ("## Evidencia", "evidence"),
    ):
        lines.extend(["", heading, ""])
        lines.extend(f"- {item}" for item in manifest[field])

    next_step = manifest["next_step"]
    candidate_global, candidate_edition = parse_revision_aware(
        str(next_step["revision_aware"])
    )
    if candidate_global != int(next_step["global_revision"]):
        raise ValueError(
            "next_step.global_revision no coincide con "
            "next_step.revision_aware."
        )

    lines.extend(
        [
            "",
            "## Siguiente paso",
            "",
            (
                "El siguiente Global disponible es "
                f"**G{candidate_global:03d}/E{candidate_edition:02d}**, "
                f"candidato `{next_step['revision_aware']}`."
            ),
            "",
            next_step["description"],
        ]
    )

    text = "\n".join(lines).rstrip() + "\n"
    errors = validate_notes(text)
    if errors:
        raise ValueError("; ".join(errors))
    return text


def normalize_body(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n").rstrip()


def validate_release_snapshot(
    snapshot: dict,
    *,
    version: str,
    expected_notes: str,
) -> list[str]:
    expected = {
        "tagName": f"v{version}",
        "name": expected_title(version),
        "isDraft": False,
        "isPrerelease": version.endswith("-beta"),
    }
    errors: list[str] = []

    for field, expected_value in expected.items():
        if snapshot.get(field) != expected_value:
            errors.append(
                "Release existente incompatible: "
                f"{field}={snapshot.get(field)!r}; "
                f"se esperaba {expected_value!r}."
            )

    body = snapshot.get("body")
    if not isinstance(body, str):
        errors.append("Release existente incompatible: body ausente.")
    elif normalize_body(body) != normalize_body(expected_notes):
        errors.append(
            "Release existente incompatible: el body no coincide "
            "con las notas canónicas."
        )

    return errors


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    p.add_argument("--check-manifest", action="store_true")
    p.add_argument("--render-notes", type=Path)
    p.add_argument("--check-release-json", type=Path)
    p.add_argument("--notes", type=Path)
    p.add_argument("--tag")
    p.add_argument("--published-commit")
    p.add_argument("--tag-object")
    return p


def main() -> int:
    configure_utf8_stdio()
    args = parser().parse_args()

    try:
        manifest = load_json(args.manifest)
        version = read_version()
        ledger = read_ledger()
        errors = validate_manifest(manifest, version, ledger)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"[release-publication] ERROR: {exc}")
        return 1

    if errors:
        for error in errors:
            print(f"[release-publication] ERROR: {error}")
        return 1

    if args.check_manifest:
        global_revision, edition = parse_revision_aware(version)
        print(
            "[release-publication] OK: manifiesto "
            f"G{global_revision:03d}/E{edition:02d} validado."
        )

    if args.render_notes:
        if bool(args.published_commit) != bool(args.tag_object):
            print(
                "[release-publication] ERROR: --published-commit y "
                "--tag-object deben usarse juntos."
            )
            return 2

        expected_tag = f"v{version}"
        if args.tag and args.tag != expected_tag:
            print(
                f"[release-publication] ERROR: se esperaba {expected_tag}."
            )
            return 1

        try:
            if args.published_commit:
                published_commit = args.published_commit
                tag_object = args.tag_object
            else:
                published_commit, tag_object = resolve_tag(
                    args.tag or expected_tag
                )
            notes = render_notes(
                manifest,
                published_commit,
                tag_object,
            )
            args.render_notes.parent.mkdir(parents=True, exist_ok=True)
            args.render_notes.write_text(
                notes,
                encoding="utf-8",
                newline="\n",
            )
        except (OSError, RuntimeError, ValueError) as exc:
            print(f"[release-publication] ERROR: {exc}")
            return 1

        print(
            f"[release-publication] OK: notas en {args.render_notes}."
        )

    if args.check_release_json:
        if args.notes is None:
            print(
                "[release-publication] ERROR: "
                "--check-release-json requiere --notes."
            )
            return 2
        try:
            snapshot = load_json(args.check_release_json)
            notes = args.notes.read_text(encoding="utf-8-sig")
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print(f"[release-publication] ERROR: {exc}")
            return 1

        release_errors = validate_release_snapshot(
            snapshot,
            version=version,
            expected_notes=notes,
        )
        if release_errors:
            for error in release_errors:
                print(f"[release-publication] ERROR: {error}")
            return 1
        print(
            "[release-publication] OK: Release existente coincide "
            "con el contrato; operación idempotente."
        )

    if not any(
        (
            args.check_manifest,
            args.render_notes,
            args.check_release_json,
        )
    ):
        print("[release-publication] OK: manifiesto validado.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
