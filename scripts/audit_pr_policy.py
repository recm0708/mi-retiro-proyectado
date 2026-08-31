"""Audita política, integridad y firmas de un Pull Request.

Comprueba:
- nombre de rama de trabajo;
- título mínimo del PR;
- ausencia de merge commits dentro de la rama;
- coherencia de archivos revision-aware sensibles;
- firma criptográfica de commits humanos contra allowed_signers de la base.

Dependabot queda exento únicamente de la comprobación local contra
allowed_signers. La protección de firmas de GitHub continúa siendo
responsabilidad adicional del ruleset de la rama.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

TRUSTED_BOTS = {
    "dependabot[bot]",
}

REVISION_STATE_FILES = {
    "VERSION",
    "data/pre-1-0-revision-ledger.json",
    "data/release-publication-manifest.json",
}

BRANCH_RE = re.compile(
    r"^[a-z][a-z0-9-]*/"
    r"[a-z0-9][a-z0-9._/-]*$"
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


def git_lines(
    *args: str,
) -> list[str]:
    result = run_git(*args)

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


def branch_errors(
    branch: str,
) -> list[str]:
    errors = []

    if not branch:
        return [
            "No se recibió nombre de rama."
        ]

    if branch == "main":
        return [
            "Un Pull Request no puede originarse directamente desde main."
        ]

    if not BRANCH_RE.fullmatch(branch):
        errors.append(
            "La rama debe usar el patrón "
            "<tipo>/<descripcion> en minúsculas."
        )

    if ".." in branch:
        errors.append(
            "La rama no puede contener '..'."
        )

    return errors


def title_errors(
    title: str,
) -> list[str]:
    errors = []

    if not title.strip():
        return [
            "El Pull Request requiere título."
        ]

    if title != title.strip():
        errors.append(
            "El título no debe comenzar ni terminar con espacios."
        )

    if len(title) > 140:
        errors.append(
            "El título supera 140 caracteres."
        )

    if re.match(
        r"(?i)^(wip|draft)\b",
        title,
    ):
        errors.append(
            "Un PR listo para gate no debe usar WIP/DRAFT en el título."
        )

    return errors


def changed_files(
    base: str,
    head: str,
) -> list[str]:
    return git_lines(
        "diff",
        "--name-only",
        f"{base}...{head}",
    )


def commits_in_range(
    base: str,
    head: str,
) -> list[str]:
    return git_lines(
        "rev-list",
        "--reverse",
        f"{base}..{head}",
    )


def merge_commits(
    base: str,
    head: str,
) -> list[str]:
    return git_lines(
        "rev-list",
        "--merges",
        f"{base}..{head}",
    )


def revision_state_errors(
    files: list[str],
) -> list[str]:
    changed = (
        REVISION_STATE_FILES
        & set(files)
    )

    if (
        changed
        and changed != REVISION_STATE_FILES
    ):
        missing = sorted(
            REVISION_STATE_FILES
            - changed
        )

        return [
            "Los archivos de estado revision-aware deben "
            "cambiar de forma coordinada. Faltan: "
            + ", ".join(missing)
        ]

    return []


def base_allowed_signers(
    base: str,
) -> str:
    result = run_git(
        "show",
        f"{base}:.github/allowed_signers",
    )

    if result.returncode != 0:
        raise RuntimeError(
            "No se pudo obtener allowed_signers "
            "desde la rama base:\n"
            + result.stdout
            + result.stderr
        )

    if not result.stdout.strip():
        raise RuntimeError(
            "allowed_signers de la base está vacío."
        )

    return result.stdout


def verify_human_commits(
    commits: list[str],
    *,
    base: str,
) -> list[str]:
    errors = []

    allowed = base_allowed_signers(
        base
    )

    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="\n",
        delete=False,
    ) as handle:
        handle.write(allowed)
        allowed_path = Path(
            handle.name
        )

    try:
        for sha in commits:
            result = subprocess.run(
                [
                    "git",
                    "-c",
                    "gpg.format=ssh",
                    "-c",
                    (
                        "gpg.ssh.allowedSignersFile="
                        + str(allowed_path)
                    ),
                    "verify-commit",
                    sha,
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )

            if result.returncode != 0:
                errors.append(
                    "Firma no válida o no autorizada: "
                    + sha
                )
    finally:
        allowed_path.unlink(
            missing_ok=True
        )

    return errors


def audit_pr(
    *,
    base: str,
    head: str,
    branch: str,
    title: str,
    actor: str,
) -> dict:
    files = changed_files(
        base,
        head,
    )

    commits = commits_in_range(
        base,
        head,
    )

    merges = merge_commits(
        base,
        head,
    )

    errors = []

    errors.extend(
        branch_errors(branch)
    )

    errors.extend(
        title_errors(title)
    )

    errors.extend(
        revision_state_errors(files)
    )

    if merges:
        errors.append(
            "La rama del PR contiene merge commits: "
            + ", ".join(merges)
        )

    signature_mode = "trusted-bot"

    if actor not in TRUSTED_BOTS:
        signature_mode = "allowed-signers-base"

        errors.extend(
            verify_human_commits(
                commits,
                base=base,
            )
        )

    return {
        "result": (
            "pass"
            if not errors
            else "fail"
        ),
        "base": base,
        "head": head,
        "branch": branch,
        "title": title,
        "actor": actor,
        "commits": commits,
        "changed_files": files,
        "merge_commits": merges,
        "signature_mode": signature_mode,
        "errors": errors,
    }


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description=__doc__,
    )

    p.add_argument(
        "--base",
        required=True,
    )

    p.add_argument(
        "--head",
        default="HEAD",
    )

    p.add_argument(
        "--branch",
        required=True,
    )

    p.add_argument(
        "--title",
        required=True,
    )

    p.add_argument(
        "--actor",
        required=True,
    )

    return p


def main() -> int:
    args = parser().parse_args()

    try:
        report = audit_pr(
            base=args.base,
            head=args.head,
            branch=args.branch,
            title=args.title,
            actor=args.actor,
        )
    except RuntimeError as exc:
        print(
            "[pr-policy] ERROR: "
            + str(exc),
            file=sys.stderr,
        )
        return 1

    print(
        "[pr-policy] Rama: "
        + report["branch"]
    )

    print(
        "[pr-policy] Actor: "
        + report["actor"]
    )

    print(
        "[pr-policy] Commits del PR: "
        + str(
            len(
                report["commits"]
            )
        )
    )

    print(
        "[pr-policy] Archivos cambiados: "
        + str(
            len(
                report["changed_files"]
            )
        )
    )

    print(
        "[pr-policy] Verificación de firma: "
        + report["signature_mode"]
    )

    if report["errors"]:
        for error in report["errors"]:
            print(
                "[pr-policy] ERROR: "
                + error,
                file=sys.stderr,
            )

        return 1

    print(
        "[pr-policy] OK: política del Pull Request validada."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
