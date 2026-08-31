"""Audita referencias externas usadas por GitHub Actions.

Bloquea referencias evidentemente mutables como main, master o latest.
Acepta tags versionados vN/vN.N/vN.N.N y SHA completos de 40 caracteres.
No modifica workflows ni consulta servicios externos.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"

MUTABLE_REFS = {
    "main",
    "master",
    "latest",
    "head",
    "develop",
    "development",
    "dev",
}

VERSION_RE = re.compile(
    r"^v\d+(?:\.\d+){0,2}$"
)

SHA_RE = re.compile(
    r"^[0-9a-fA-F]{40}$"
)

USES_RE = re.compile(
    r"^\s*(?:-\s*)?uses:\s*([^\s#]+)",
    flags=re.MULTILINE,
)


def workflow_files() -> list[Path]:
    """Devuelve YAML versionables de GitHub Actions."""

    return sorted(
        [
            *WORKFLOWS.glob("*.yml"),
            *WORKFLOWS.glob("*.yaml"),
        ]
    )


def extract_uses(
    text: str,
) -> list[str]:
    """Extrae referencias declaradas mediante uses."""

    return USES_RE.findall(text)


def validate_reference(
    reference: str,
) -> str | None:
    """Devuelve error si una referencia no cumple política mínima."""

    if reference.startswith("./"):
        return None

    if reference.startswith("docker://"):
        image = reference.removeprefix(
            "docker://"
        )

        if image.endswith(":latest"):
            return (
                "imagen Docker usa tag mutable latest"
            )

        return None

    if "@" not in reference:
        return (
            "acción externa sin referencia versionada"
        )

    action, ref = reference.rsplit(
        "@",
        1,
    )

    if not action or not ref:
        return (
            "referencia de acción incompleta"
        )

    if ref.lower() in MUTABLE_REFS:
        return (
            "referencia mutable no permitida: "
            + ref
        )

    if SHA_RE.fullmatch(ref):
        return None

    if VERSION_RE.fullmatch(ref):
        return None

    return (
        "referencia no reconocida como versión "
        "estable o SHA completo: "
        + ref
    )


def audit_workflows() -> dict:
    """Audita todos los workflows y produce reporte."""

    files = workflow_files()
    references = []
    errors = []

    for path in files:
        text = path.read_text(
            encoding="utf-8"
        )

        for reference in extract_uses(
            text
        ):
            references.append(
                {
                    "workflow": str(
                        path.relative_to(ROOT)
                    ).replace("\\", "/"),
                    "reference": reference,
                }
            )

            error = validate_reference(
                reference
            )

            if error:
                errors.append(
                    {
                        "workflow": str(
                            path.relative_to(ROOT)
                        ).replace("\\", "/"),
                        "reference": reference,
                        "error": error,
                    }
                )

    return {
        "result": (
            "pass"
            if not errors
            else "fail"
        ),
        "workflow_count": len(files),
        "reference_count": len(references),
        "references": references,
        "errors": errors,
    }


def main() -> int:
    report = audit_workflows()

    print(
        "[action-references] Workflows: "
        + str(report["workflow_count"])
    )

    print(
        "[action-references] Referencias uses: "
        + str(report["reference_count"])
    )

    if report["errors"]:
        for item in report["errors"]:
            print(
                "[action-references] ERROR: "
                + item["workflow"]
                + " -> "
                + item["reference"]
                + " — "
                + item["error"],
                file=sys.stderr,
            )

        return 1

    print(
        "[action-references] "
        "OK: referencias externas versionadas."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
