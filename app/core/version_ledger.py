"""Carga y valida el ledger revision-aware materializado por VER.2.

El ledger es un artefacto de auditoría local del repositorio. No consulta GitHub,
no mueve tags y no sustituye ``VERSION``. Su objetivo es garantizar que la
reconstrucción histórica permanezca contigua, no duplique estados aceptados y
codifique cada Global con la convención revision-aware vigente.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.core.version import construir_version_beta_revision


ROOT = Path(__file__).resolve().parents[2]
LEDGER_FILE = ROOT / "data" / "revision_ledger_pre_1_0.json"


class LedgerRevisionError(ValueError):
    """Indica que el ledger estructurado incumple su contrato canónico."""


def cargar_ledger(path: Path = LEDGER_FILE) -> dict[str, Any]:
    """Carga el ledger JSON y devuelve su estructura validada."""

    try:
        contenido = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise LedgerRevisionError(f"No se pudo leer el ledger: {path}") from error
    except json.JSONDecodeError as error:
        raise LedgerRevisionError("El ledger no contiene JSON válido.") from error

    validar_ledger(contenido)
    return contenido


def validar_ledger(ledger: dict[str, Any]) -> None:
    """Valida continuidad, unicidad y codificación revision-aware del ledger."""

    if ledger.get("schema_version") != 1:
        raise LedgerRevisionError("schema_version debe ser 1.")

    accepted_count = ledger.get("accepted_count")
    if not isinstance(accepted_count, int) or accepted_count <= 0:
        raise LedgerRevisionError("accepted_count debe ser un entero positivo.")

    entries = ledger.get("entries")
    if not isinstance(entries, list):
        raise LedgerRevisionError("entries debe ser una lista.")
    if len(entries) != accepted_count:
        raise LedgerRevisionError(
            "La cantidad de entries debe coincidir con accepted_count."
        )

    globales: list[int] = []
    versiones: list[str] = []

    for posicion, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise LedgerRevisionError(f"La entrada {posicion} no es un objeto.")

        global_revision = entry.get("global_revision")
        ordinal = entry.get("ordinal")
        version = entry.get("revision_aware")

        if not isinstance(global_revision, int):
            raise LedgerRevisionError(
                f"La entrada {posicion} no tiene global_revision entero."
            )
        if not isinstance(ordinal, int):
            raise LedgerRevisionError(
                f"La entrada G{global_revision:03d} no tiene ordinal entero."
            )
        if not isinstance(version, str):
            raise LedgerRevisionError(
                f"La entrada G{global_revision:03d} no tiene revision_aware."
            )

        esperada = construir_version_beta_revision(global_revision, ordinal)
        if version != esperada:
            raise LedgerRevisionError(
                f"G{global_revision:03d} declara {version!r}; se esperaba {esperada!r}."
            )

        for campo in ("block", "state", "anchor", "evidence"):
            valor = entry.get(campo)
            if not isinstance(valor, str) or not valor.strip():
                raise LedgerRevisionError(
                    f"G{global_revision:03d} requiere {campo} no vacío."
                )

        globales.append(global_revision)
        versiones.append(version)

    esperados = list(range(1, accepted_count + 1))
    if globales != esperados:
        raise LedgerRevisionError(
            "Los Global deben ser contiguos, ordenados y comenzar en G001."
        )
    if len(versiones) != len(set(versiones)):
        raise LedgerRevisionError("El ledger contiene IDs revision-aware duplicados.")

    next_global = ledger.get("next_global_if_ver2_accepted")
    if next_global != accepted_count + 1:
        raise LedgerRevisionError(
            "next_global_if_ver2_accepted debe ser accepted_count + 1."
        )

    next_candidate = ledger.get("next_candidate")
    candidato_esperado = construir_version_beta_revision(next_global, 1)
    if next_candidate != candidato_esperado:
        raise LedgerRevisionError(
            f"next_candidate debe ser {candidato_esperado!r}."
        )

    tags = ledger.get("historical_tags_immutable")
    if tags != {"from": "v0.0.1-beta", "to": "v0.0.26-beta"}:
        raise LedgerRevisionError(
            "El rango de tags históricos inmutables debe permanecer v0.0.1-beta–v0.0.26-beta."
        )

    excluded = ledger.get("excluded")
    if not isinstance(excluded, list):
        raise LedgerRevisionError("excluded debe ser una lista.")
    for posicion, item in enumerate(excluded, start=1):
        if not isinstance(item, dict):
            raise LedgerRevisionError(
                f"La exclusión {posicion} debe ser un objeto."
            )
        for campo in ("state", "reason"):
            valor = item.get(campo)
            if not isinstance(valor, str) or not valor.strip():
                raise LedgerRevisionError(
                    f"La exclusión {posicion} requiere {campo} no vacío."
                )
