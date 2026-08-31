"""Audita firmas y pertenencia histórica de todos los tags v*.

No crea, modifica ni elimina tags.
La confianza SSH proviene exclusivamente de .github/allowed_signers.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SIGNERS = (
    ROOT
    / ".github"
    / "allowed_signers"
)


def run_git(
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


def version_tags() -> list[str]:
    result = run_git(
        "tag",
        "--list",
        "v*",
        "--sort=version:refname",
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stdout
            + result.stderr
        )

    return [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def verify_tag(
    tag: str,
) -> list[str]:
    errors = []

    signature = subprocess.run(
        [
            "git",
            "-c",
            "gpg.format=ssh",
            "-c",
            (
                "gpg.ssh.allowedSignersFile="
                + str(ALLOWED_SIGNERS)
            ),
            "tag",
            "-v",
            tag,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    if signature.returncode != 0:
        errors.append(
            "firma inválida o no autorizada"
        )

    target = run_git(
        "rev-parse",
        f"{tag}^{{}}",
    )

    if target.returncode != 0:
        errors.append(
            "target no resoluble"
        )
        return errors

    ancestor = run_git(
        "merge-base",
        "--is-ancestor",
        target.stdout.strip(),
        "HEAD",
    )

    if ancestor.returncode != 0:
        errors.append(
            "target fuera del historial de HEAD"
        )

    return errors


def main() -> int:
    if not ALLOWED_SIGNERS.is_file():
        print(
            "[tag-audit] ERROR: allowed_signers no existe.",
            file=sys.stderr,
        )
        return 1

    try:
        tags = version_tags()
    except RuntimeError as exc:
        print(
            "[tag-audit] ERROR: "
            + str(exc),
            file=sys.stderr,
        )
        return 1

    if not tags:
        print(
            "[tag-audit] ERROR: no existen tags v*.",
            file=sys.stderr,
        )
        return 1

    failed = []

    for tag in tags:
        errors = verify_tag(
            tag
        )

        if errors:
            failed.append(
                (
                    tag,
                    errors,
                )
            )

            print(
                "[tag-audit] FAIL: "
                + tag
                + " — "
                + "; ".join(errors),
                file=sys.stderr,
            )
        else:
            print(
                "[tag-audit] PASS: "
                + tag
            )

    print()
    print(
        "[tag-audit] Tags auditados: "
        + str(len(tags))
    )

    print(
        "[tag-audit] Fallos: "
        + str(len(failed))
    )

    return (
        0
        if not failed
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
