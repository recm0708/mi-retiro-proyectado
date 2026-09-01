from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "git-history-attestation.json"


def run_git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="strict",
        check=False,
    )


def git_lines(*args: str) -> list[str]:
    result = run_git(*args)

    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)

    return [
        line
        for line in result.stdout.splitlines()
        if line
    ]


def history_shas(ref: str = "HEAD") -> list[str]:
    return git_lines(
        "rev-list",
        "--reverse",
        ref,
    )


def history_records(
    ref: str = "HEAD",
) -> list[tuple[str, str, str]]:
    result = run_git(
        "-c",
        "i18n.logOutputEncoding=UTF-8",
        "log",
        "--reverse",
        "--format=%H%x1f%s%x1f%G?",
        ref,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stdout + result.stderr)

    records = []

    for line in result.stdout.splitlines():
        if not line:
            continue

        parts = line.split("\x1f")

        if len(parts) != 3:
            raise RuntimeError(
                f"Registro Git inesperado: {line!r}"
            )

        records.append(
            (
                parts[0],
                parts[1],
                parts[2] or "N",
            )
        )

    return records


def commit_has_signature(
    sha: str,
) -> bool:
    """Indica si el objeto commit contiene una firma embebida."""

    result = run_git(
        "cat-file",
        "commit",
        sha,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stdout + result.stderr
        )

    return any(
        line.startswith(
            ("gpgsig ", "gpgsig-sha256 ")
        )
        for line in result.stdout.splitlines()
    )


def pr_from_subject(
    subject: str,
) -> int | None:
    match = re.search(
        r"\(#(?P<n>\d+)\)\s*$",
        subject,
    )

    if match:
        return int(match.group("n"))

    match = re.match(
        r"(?i)^Merge pull request #(?P<n>\d+)\b",
        subject,
    )

    if match:
        return int(match.group("n"))

    return None


def current_history_identity(
    ref: str = "HEAD",
) -> str:
    return f"HIST-{len(history_shas(ref)):04d}"


def load_manifest() -> dict:
    return json.loads(
        MANIFEST.read_text(
            encoding="utf-8"
        )
    )


def audit_history() -> dict:
    data = load_manifest()
    errors: list[str] = []
    entries = data.get(
        "commits",
        [],
    )
    baseline_count = data.get(
        "attested_commit_count"
    )

    if (
        not isinstance(
            baseline_count,
            int,
        )
        or baseline_count <= 0
    ):
        errors.append(
            "attested_commit_count inválido."
        )
        baseline_count = 0

    if len(entries) != baseline_count:
        errors.append(
            "Entradas del manifiesto: "
            f"{len(entries)}; "
            f"esperado: {baseline_count}."
        )

    current = history_records(
        "HEAD"
    )

    baseline_head = str(
        data.get(
            "attested_head",
            "",
        )
    ).strip()

    if not baseline_head:
        errors.append(
            "attested_head ausente."
        )
        baseline_records = []
    else:
        baseline_records = history_records(
            baseline_head
        )

        if len(baseline_records) != baseline_count:
            errors.append(
                "El historial del snapshot contiene "
                f"{len(baseline_records)} commits; "
                f"esperado: {baseline_count}."
            )

        merge_commits = git_lines(
            "rev-list",
            "--merges",
            baseline_head,
        )

        if merge_commits:
            errors.append(
                "El snapshot atestado dejó de ser lineal: "
                f"{len(merge_commits)} merge commits."
            )

    for index, entry in enumerate(
        entries,
        start=1,
    ):
        expected_id = (
            f"HIST-{index:04d}"
        )

        if (
            entry.get("hist_id")
            != expected_id
        ):
            errors.append(
                "ID histórico no continuo en "
                f"posición {index}: "
                f"{entry.get('hist_id')!r}."
            )

        if entry.get("ordinal") != index:
            errors.append(
                f"Ordinal incorrecto en {expected_id}."
            )

        if index > len(baseline_records):
            continue

        sha, subject, _sig_status = (
            baseline_records[
                index - 1
            ]
        )

        if entry.get("sha") != sha:
            errors.append(
                f"SHA divergente en {expected_id}."
            )

        if (
            entry.get("subject_original")
            != subject
        ):
            errors.append(
                "Asunto original divergente en "
                f"{expected_id}."
            )

        signature_present = (
            commit_has_signature(
                sha
            )
        )

        if (
            bool(
                entry.get(
                    "signature_present"
                )
            )
            != signature_present
        ):
            errors.append(
                "Estado de firma divergente en "
                f"{expected_id}."
            )

        if (
            entry.get(
                "pr_number_explicit_in_subject"
            )
            != pr_from_subject(subject)
        ):
            errors.append(
                "PR explícito divergente en "
                f"{expected_id}."
            )

        canonical = str(
            entry.get(
                "subject_canonical_es",
                "",
            )
        ).strip()

        if not canonical:
            errors.append(
                "Descripción canónica vacía en "
                f"{expected_id}."
            )

    if entries:
        if (
            entries[0].get("sha")
            != data.get("root_sha")
        ):
            errors.append(
                "root_sha no coincide con HIST-0001."
            )

        if (
            entries[-1].get("sha")
            != data.get("attested_head")
        ):
            errors.append(
                "attested_head no coincide "
                "con la última entrada."
            )

    sig = data.get(
        "signature_attestation",
        {},
    )

    unsigned = [
        entry
        for entry in entries
        if not bool(
            entry.get(
                "signature_present"
            )
        )
    ]
    signed = [
        entry
        for entry in entries
        if bool(
            entry.get(
                "signature_present"
            )
        )
    ]

    if (
        len(unsigned)
        != sig.get("unsigned_count")
    ):
        errors.append(
            "Conteo de commits sin firma divergente."
        )

    if (
        len(signed)
        != sig.get("signed_object_count")
    ):
        errors.append(
            "Conteo de commits firmados divergente."
        )

    if (
        unsigned
        and unsigned[-1].get("hist_id")
        != sig.get("last_unsigned_hist_id")
    ):
        errors.append(
            "Frontera final sin firma divergente."
        )

    if (
        signed
        and signed[0].get("hist_id")
        != sig.get("first_signed_hist_id")
    ):
        errors.append(
            "Frontera inicial firmada divergente."
        )

    if any(
        bool(
            entry.get(
                "signature_present"
            )
        )
        for entry in entries[:89]
    ):
        errors.append(
            "Apareció una firma dentro de "
            "HIST-0001..HIST-0089."
        )

    if any(
        not bool(
            entry.get(
                "signature_present"
            )
        )
        for entry in entries[89:]
    ):
        errors.append(
            "Apareció un commit sin firma "
            "desde HIST-0090."
        )

    baseline_head = str(
        data.get(
            "attested_head",
            "",
        )
    )

    if baseline_head:
        ancestor = run_git(
            "merge-base",
            "--is-ancestor",
            baseline_head,
            "HEAD",
        )

        if ancestor.returncode != 0:
            errors.append(
                "El snapshot atestado dejó de "
                "ser ancestro de HEAD."
            )

    translated_ids = {
        entry["hist_id"]
        for entry in entries
        if entry.get(
            "canonicalization_category"
        )
        != "preservado_es_o_tecnico"
    }
    expected_translated = set(
        data.get(
            "language_attestation",
            {},
        ).get(
            "canonicalized_hist_ids",
            [],
        )
    )

    if (
        translated_ids
        != expected_translated
    ):
        errors.append(
            "La lista de descripciones "
            "normalizadas no coincide."
        )

    return {
        "result": (
            "pass"
            if not errors
            else "fail"
        ),
        "errors": errors,
        "baseline_commit_count": (
            baseline_count
        ),
        "current_commit_count": len(
            current
        ),
        "current_hist_id": (
            current_history_identity(
                "HEAD"
            )
        ),
        "unsigned_count": len(
            unsigned
        ),
        "signed_object_count": len(
            signed
        ),
        "first_signed_hist_id": (
            signed[0]["hist_id"]
            if signed
            else None
        ),
        "last_unsigned_hist_id": (
            unsigned[-1]["hist_id"]
            if unsigned
            else None
        ),
    }


def main() -> int:
    report = audit_history()

    print(
        "[git-history-attestation] "
        f"Snapshot: "
        f"{report['baseline_commit_count']} "
        "commits"
    )
    print(
        "[git-history-attestation] "
        f"Historial actual: "
        f"{report['current_commit_count']} "
        "commits "
        f"({report['current_hist_id']})"
    )
    print(
        "[git-history-attestation] "
        f"Sin firma: "
        f"{report['unsigned_count']} | "
        f"Con firma: "
        f"{report['signed_object_count']}"
    )
    print(
        "[git-history-attestation] "
        f"Frontera: "
        f"{report['last_unsigned_hist_id']} "
        "-> "
        f"{report['first_signed_hist_id']}"
    )

    if report["errors"]:
        for error in report["errors"]:
            print(
                "[git-history-attestation] "
                f"ERROR: {error}"
            )
        return 1

    print(
        "[git-history-attestation] OK: "
        "identidad HIST, snapshot y frontera "
        "criptográfica preservados sin "
        "reescritura."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
