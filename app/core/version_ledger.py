"""Carga y valida el ledger revision-aware previo a 1.0.

El ledger es un artefacto de auditoría local del repositorio. No consulta
servicios externos, no mueve tags y no sustituye ``VERSION``.

El schema vivo distingue la Edition canónica del alias histórico ``ordinal``
y permite preservar identificadores revision-aware v1 mientras prepara
entradas futuras con identificadores revision-aware v2.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.core.version import (
    construir_version_beta_revision,
    construir_version_beta_revision_v2,
    descomponer_version_beta_revision_v2,
)


ROOT = Path(__file__).resolve().parents[2]

LEDGER_FILE = (
    ROOT
    / "data"
    / "governance"
    / "pre-1-0-revision-ledger.json"
)


class LedgerRevisionError(ValueError):
    """Indica que el ledger estructurado incumple su contrato canónico."""


def cargar_ledger(
    path: Path = LEDGER_FILE,
) -> dict[str, Any]:
    """Carga el ledger JSON y devuelve su estructura validada."""

    try:
        contenido = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except OSError as error:
        raise LedgerRevisionError(
            f"No se pudo leer el ledger: {path}"
        ) from error
    except json.JSONDecodeError as error:
        raise LedgerRevisionError(
            "El ledger no contiene JSON válido."
        ) from error

    validar_ledger(
        contenido
    )

    return contenido


def _validar_entero_en_rango(
    *,
    value: object,
    minimum: int,
    maximum: int,
    field: str,
    global_revision: int,
) -> int:
    """Valida un entero acotado perteneciente a una entrada."""

    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or not minimum <= value <= maximum
    ):
        raise LedgerRevisionError(
            f"G{global_revision:03d} requiere "
            f"{field} entre {minimum} y {maximum}."
        )

    return value


def _validar_entry(
    entry: dict[str, Any],
    posicion: int,
) -> tuple[int, str]:
    """Valida una entrada individual y devuelve Global e identificador."""

    global_revision = entry.get(
        "global_revision"
    )

    if (
        not isinstance(global_revision, int)
        or isinstance(global_revision, bool)
        or global_revision <= 0
    ):
        raise LedgerRevisionError(
            f"La entrada {posicion} no tiene "
            "global_revision entero positivo."
        )

    edition = _validar_entero_en_rango(
        value=entry.get(
            "edition"
        ),
        minimum=1,
        maximum=99,
        field="edition",
        global_revision=global_revision,
    )

    ordinal = _validar_entero_en_rango(
        value=entry.get(
            "ordinal"
        ),
        minimum=1,
        maximum=99,
        field="ordinal",
        global_revision=global_revision,
    )

    if ordinal != edition:
        raise LedgerRevisionError(
            f"G{global_revision:03d} declara "
            "ordinal y edition divergentes."
        )

    identifier_schema = entry.get(
        "identifier_schema"
    )

    if identifier_schema not in (
        1,
        2,
    ):
        raise LedgerRevisionError(
            f"G{global_revision:03d} requiere "
            "identifier_schema 1 o 2."
        )

    expected_format = (
        "revision-aware-v1"
        if identifier_schema == 1
        else "revision-aware-v2"
    )

    if entry.get(
        "version_format"
    ) != expected_format:
        raise LedgerRevisionError(
            f"G{global_revision:03d} requiere "
            f"version_format {expected_format!r}."
        )

    correction = entry.get(
        "correction_ordinal"
    )

    maintenance = _validar_entero_en_rango(
        value=entry.get(
            "maintenance_ordinal"
        ),
        minimum=0,
        maximum=999,
        field="maintenance_ordinal",
        global_revision=global_revision,
    )

    if identifier_schema == 1:
        if correction is not None:
            raise LedgerRevisionError(
                f"G{global_revision:03d} es histórica v1; "
                "correction_ordinal debe ser null."
            )

        expected_version = (
            construir_version_beta_revision(
                global_revision,
                edition,
            )
        )
    else:
        correction_value = _validar_entero_en_rango(
            value=correction,
            minimum=0,
            maximum=999,
            field="correction_ordinal",
            global_revision=global_revision,
        )

        expected_version = (
            construir_version_beta_revision_v2(
                global_revision,
                edition,
                correction_value,
                maintenance,
            )
        )

    version = entry.get(
        "revision_aware"
    )

    if not isinstance(
        version,
        str,
    ):
        raise LedgerRevisionError(
            f"G{global_revision:03d} no tiene "
            "revision_aware."
        )

    if version != expected_version:
        raise LedgerRevisionError(
            f"G{global_revision:03d} declara "
            f"{version!r}; se esperaba "
            f"{expected_version!r}."
        )

    for field in (
        "block",
        "state",
        "anchor",
        "evidence",
    ):
        value = entry.get(
            field
        )

        if (
            not isinstance(
                value,
                str,
            )
            or not value.strip()
        ):
            raise LedgerRevisionError(
                f"G{global_revision:03d} requiere "
                f"{field} no vacío."
            )

    if "functional_revision" not in entry:
        raise LedgerRevisionError(
            f"G{global_revision:03d} debe declarar "
            "functional_revision explícitamente."
        )

    functional_revision = entry[
        "functional_revision"
    ]

    if (
        functional_revision is not None
        and (
            not isinstance(
                functional_revision,
                str,
            )
            or not functional_revision.strip()
        )
    ):
        raise LedgerRevisionError(
            f"G{global_revision:03d} declara "
            "functional_revision inválida."
        )

    return (
        global_revision,
        version,
    )


def validar_ledger(
    ledger: dict[str, Any],
) -> None:
    """Valida continuidad, schema y codificación revision-aware."""

    if ledger.get(
        "schema_version"
    ) != 2:
        raise LedgerRevisionError(
            "schema_version debe ser 2."
        )

    if (
        "next_global_if_ver2_accepted"
        in ledger
    ):
        raise LedgerRevisionError(
            "El ledger v2 no admite la clave "
            "next_global_if_ver2_accepted."
        )

    for field in (
        "next_candidate_assignment",
        "active_phase",
    ):
        if field in ledger:
            raise LedgerRevisionError(
                "El ledger v2 no admite estado de workflow: "
                + field
            )

    accepted_count = ledger.get(
        "accepted_count"
    )

    if (
        not isinstance(
            accepted_count,
            int,
        )
        or isinstance(
            accepted_count,
            bool,
        )
        or accepted_count <= 0
    ):
        raise LedgerRevisionError(
            "accepted_count debe ser "
            "un entero positivo."
        )

    entries = ledger.get(
        "entries"
    )

    if not isinstance(
        entries,
        list,
    ):
        raise LedgerRevisionError(
            "entries debe ser una lista."
        )

    if len(
        entries
    ) != accepted_count:
        raise LedgerRevisionError(
            "La cantidad de entries debe "
            "coincidir con accepted_count."
        )

    globales: list[int] = []
    versiones: list[str] = []

    for posicion, entry in enumerate(
        entries,
        start=1,
    ):
        if not isinstance(
            entry,
            dict,
        ):
            raise LedgerRevisionError(
                f"La entrada {posicion} "
                "no es un objeto."
            )

        (
            global_revision,
            version,
        ) = _validar_entry(
            entry,
            posicion,
        )

        globales.append(
            global_revision
        )

        versiones.append(
            version
        )

    esperados = list(
        range(
            1,
            accepted_count + 1,
        )
    )

    if globales != esperados:
        raise LedgerRevisionError(
            "Los Global deben ser contiguos, "
            "ordenados y comenzar en G001."
        )

    if len(
        versiones
    ) != len(
        set(
            versiones
        )
    ):
        raise LedgerRevisionError(
            "El ledger contiene IDs "
            "revision-aware duplicados."
        )

    next_global = ledger.get(
        "next_global"
    )

    if next_global != accepted_count + 1:
        raise LedgerRevisionError(
            "next_global debe ser "
            "accepted_count + 1."
        )

    next_candidate_block = ledger.get(
        "next_candidate_block"
    )

    next_candidate = ledger.get(
        "next_candidate"
    )

    if (
        next_candidate_block is None
        or next_candidate is None
    ):
        if not (
            next_candidate_block is None
            and next_candidate is None
        ):
            raise LedgerRevisionError(
                "next_candidate y "
                "next_candidate_block deben "
                "ser ambos nulos o ambos "
                "estar definidos."
            )
    else:
        if (
            not isinstance(
                next_candidate_block,
                str,
            )
            or not next_candidate_block.strip()
        ):
            raise LedgerRevisionError(
                "next_candidate_block debe "
                "ser texto no vacío o null."
            )

        if (
            not isinstance(
                next_candidate,
                str,
            )
            or not next_candidate.strip()
        ):
            raise LedgerRevisionError(
                "next_candidate debe ser "
                "texto no vacío o null."
            )

        details = (
            descomponer_version_beta_revision_v2(
                next_candidate
            )
        )

        if details is None:
            raise LedgerRevisionError(
                "Un candidato nuevo bajo el "
                "ledger v2 debe usar un "
                "identificador revision-aware v2."
            )

        (
            candidate_global,
            candidate_edition,
            _candidate_correction,
            _candidate_maintenance,
        ) = details

        if candidate_global != next_global:
            raise LedgerRevisionError(
                "El Global del candidato no "
                "coincide con next_global."
            )

        editions = [
            entry[
                "edition"
            ]
            for entry in entries
            if entry[
                "block"
            ]
            == next_candidate_block
        ]

        expected_edition = (
            max(
                editions,
                default=0,
            )
            + 1
        )

        if (
            candidate_edition
            != expected_edition
        ):
            raise LedgerRevisionError(
                "La Edition del candidato "
                "no coincide con el siguiente "
                "ordinal aceptable del bloque."
            )

    tags = ledger.get(
        "historical_tags_immutable"
    )

    if tags != {
        "from": "v0.0.1-beta",
        "to": "v0.0.26-beta",
    }:
        raise LedgerRevisionError(
            "El rango de tags históricos "
            "inmutables debe permanecer "
            "v0.0.1-beta–v0.0.26-beta."
        )

    excluded = ledger.get(
        "excluded"
    )

    if not isinstance(
        excluded,
        list,
    ):
        raise LedgerRevisionError(
            "excluded debe ser una lista."
        )

    for posicion, item in enumerate(
        excluded,
        start=1,
    ):
        if not isinstance(
            item,
            dict,
        ):
            raise LedgerRevisionError(
                f"La exclusión {posicion} "
                "debe ser un objeto."
            )

        for field in (
            "state",
            "reason",
        ):
            value = item.get(
                field
            )

            if (
                not isinstance(
                    value,
                    str,
                )
                or not value.strip()
            ):
                raise LedgerRevisionError(
                    f"La exclusión {posicion} "
                    f"requiere {field} no vacío."
                )
