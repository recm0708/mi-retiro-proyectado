"""Genera el estado post-merge y de preparación de release.

Este auditor no crea commits, tags ni GitHub Releases.

Distingue entre:
- versión ya etiquetada y preservada;
- versión integrada que todavía requiere tag firmado;
- divergencia de un tag existente respecto de main.

La existencia del tag se evalúa localmente contra el historial Git.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LEDGER_PATH = (
    ROOT
    / "data"
    / "pre-1-0-revision-ledger.json"
)

MANIFEST_PATH = (
    ROOT
    / "data"
    / "release-publication-manifest.json"
)

VERSION_PATH = ROOT / "VERSION"


def read_json(
    path: Path,
) -> dict:
    data = json.loads(
        path.read_text(
            encoding="utf-8-sig"
        )
    )

    if not isinstance(data, dict):
        raise ValueError(
            f"{path} debe contener un objeto JSON."
        )

    return data


def git(
    *args: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def tag_state(
    version: str,
) -> dict:
    tag = "v" + version

    exists = git(
        "rev-parse",
        "--verify",
        "--quiet",
        f"refs/tags/{tag}",
    )

    if exists.returncode != 0:
        return {
            "tag": tag,
            "exists": False,
            "target": None,
            "points_to_head": False,
            "ancestor_of_head": False,
        }

    target_result = git(
        "rev-list",
        "-n",
        "1",
        tag,
    )

    if target_result.returncode != 0:
        raise RuntimeError(
            "No se pudo resolver el target de "
            + tag
        )

    target = target_result.stdout.strip()

    head_result = git(
        "rev-parse",
        "HEAD",
    )

    if head_result.returncode != 0:
        raise RuntimeError(
            "No se pudo resolver HEAD."
        )

    head = head_result.stdout.strip()

    ancestor = git(
        "merge-base",
        "--is-ancestor",
        target,
        "HEAD",
    )

    return {
        "tag": tag,
        "exists": True,
        "target": target,
        "points_to_head": target == head,
        "ancestor_of_head": (
            ancestor.returncode == 0
        ),
    }


def derive_release_action(
    *,
    tag_exists: bool,
    tag_is_ancestor: bool,
) -> str:
    """Determina la acción de publicación sin ejecutarla."""

    if not tag_exists:
        return "signed-tag-required"

    if tag_is_ancestor:
        return "none"

    return "investigate-tag-divergence"


def build_report() -> dict:
    version = VERSION_PATH.read_text(
        encoding="utf-8"
    ).strip()

    ledger = read_json(
        LEDGER_PATH
    )

    manifest = read_json(
        MANIFEST_PATH
    )

    entries = ledger.get(
        "entries"
    )

    if not isinstance(entries, list):
        raise ValueError(
            "El ledger requiere entries."
        )

    accepted = ledger.get(
        "accepted_count"
    )

    next_global = ledger.get(
        "next_global_if_ver2_accepted"
    )

    next_candidate = ledger.get(
        "next_candidate"
    )

    next_block = ledger.get(
        "next_candidate_block"
    )

    errors: list[str] = []

    if not isinstance(
        accepted,
        int,
    ):
        errors.append(
            "accepted_count no es entero."
        )

    if (
        isinstance(accepted, int)
        and len(entries) != accepted
    ):
        errors.append(
            "accepted_count no coincide "
            "con la cantidad de entries."
        )

    current_entry = (
        entries[-1]
        if entries
        else {}
    )

    if current_entry.get(
        "global_revision"
    ) != accepted:
        errors.append(
            "La última entrada del ledger "
            "no coincide con accepted_count."
        )

    if current_entry.get(
        "revision_aware"
    ) != version:
        errors.append(
            "VERSION no coincide con la "
            "última revisión aceptada."
        )

    if manifest.get(
        "version"
    ) != version:
        errors.append(
            "VERSION no coincide con el "
            "manifiesto de publicación."
        )

    next_step = manifest.get(
        "next_step"
    )

    if not isinstance(
        next_step,
        dict,
    ):
        errors.append(
            "El manifiesto requiere next_step."
        )
        next_step = {}

    if next_step.get(
        "global_revision"
    ) != next_global:
        errors.append(
            "next_step.global_revision no "
            "coincide con el ledger."
        )

    if next_step.get(
        "revision_aware"
    ) != next_candidate:
        errors.append(
            "next_step.revision_aware no "
            "coincide con el ledger."
        )

    if next_step.get(
        "block"
    ) != next_block:
        errors.append(
            "next_step.block no coincide "
            "con el ledger."
        )

    tag = tag_state(
        version
    )

    action = derive_release_action(
        tag_exists=tag["exists"],
        tag_is_ancestor=tag[
            "ancestor_of_head"
        ],
    )

    if action == "investigate-tag-divergence":
        errors.append(
            "El tag de VERSION existe pero "
            "no pertenece a la historia de HEAD."
        )

    return {
        "schema_version": 1,
        "result": (
            "pass"
            if not errors
            else "fail"
        ),
        "version": version,
        "accepted_count": accepted,
        "accepted_block": current_entry.get(
            "block"
        ),
        "accepted_revision": current_entry.get(
            "functional_revision"
        ),
        "manifest_block": manifest.get(
            "block"
        ),
        "manifest_revision": manifest.get(
            "revision"
        ),
        "next_global": next_global,
        "next_candidate": next_candidate,
        "next_candidate_block": next_block,
        "tag": tag,
        "release_action": action,
        "errors": errors,
    }


def render_markdown(
    report: dict,
) -> str:
    tag = report["tag"]

    tag_status = (
        "presente"
        if tag["exists"]
        else "pendiente"
    )

    lines = [
        "# Post-Merge / Release Readiness",
        "",
        f"- **Resultado:** `{report['result'].upper()}`",
        f"- **Versión:** `{report['version']}`",
        (
            "- **Global aceptado:** "
            f"`G{report['accepted_count']:03d}`"
        ),
        (
            "- **Estado publicado documentado:** "
            f"`{report['manifest_block']} "
            f"{report['manifest_revision']}`"
        ),
        (
            "- **Siguiente candidato:** "
            f"`G{report['next_global']:03d}` — "
            f"`{report['next_candidate']}` — "
            f"`{report['next_candidate_block']}`"
        ),
        (
            "- **Tag esperado:** "
            f"`{tag['tag']}` — {tag_status}"
        ),
        (
            "- **Acción de release:** "
            f"`{report['release_action']}`"
        ),
    ]

    if tag["exists"]:
        lines.append(
            "- **Tag dentro de la historia de HEAD:** "
            + (
                "`sí`"
                if tag["ancestor_of_head"]
                else "`no`"
            )
        )

        lines.append(
            "- **Tag apunta exactamente a HEAD:** "
            + (
                "`sí`"
                if tag["points_to_head"]
                else "`no`"
            )
        )

    if report["errors"]:
        lines.extend(
            [
                "",
                "## Bloqueadores",
                "",
            ]
        )

        for error in report["errors"]:
            lines.append(
                "- " + error
            )

    return "\n".join(lines) + "\n"


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=__doc__,
    )

    p.add_argument(
        "--json-out",
        type=Path,
    )

    p.add_argument(
        "--markdown-out",
        type=Path,
    )

    return p


def main() -> int:
    args = parser().parse_args()

    try:
        report = build_report()
    except (
        OSError,
        ValueError,
        RuntimeError,
        json.JSONDecodeError,
    ) as exc:
        print(
            "[release-readiness] ERROR: "
            + str(exc),
            file=sys.stderr,
        )
        return 1

    print(
        "[release-readiness] "
        f"VERSION: {report['version']}"
    )

    print(
        "[release-readiness] "
        f"G{report['accepted_count']:03d} aceptado"
    )

    print(
        "[release-readiness] "
        f"Siguiente: "
        f"G{report['next_global']:03d} / "
        f"{report['next_candidate_block']} / "
        f"{report['next_candidate']}"
    )

    print(
        "[release-readiness] "
        "Acción: "
        + report["release_action"]
    )

    if report["errors"]:
        for error in report["errors"]:
            print(
                "[release-readiness] ERROR: "
                + error,
                file=sys.stderr,
            )

    if args.json_out:
        args.json_out.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        args.json_out.write_text(
            json.dumps(
                report,
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

    if args.markdown_out:
        args.markdown_out.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        args.markdown_out.write_text(
            render_markdown(report),
            encoding="utf-8",
            newline="\n",
        )

    if report["result"] == "pass":
        print(
            "[release-readiness] "
            "OK: estado post-merge coherente."
        )
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
