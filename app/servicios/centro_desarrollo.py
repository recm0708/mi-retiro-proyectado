"""Servicios seguros para DEV.2 — Centro de desarrollo.

El Centro de desarrollo expone únicamente metadata técnica de la
aplicación y de Developer Diagnostics. No lee documentos personales,
no inspecciona cuerpos HTTP y no devuelve rutas absolutas locales.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.core.observabilidad import (
    ENV_DEV_MODE,
    ENV_DIAGNOSTIC_DIR,
    SCHEMA_VERSION,
    directorio_diagnostico,
    modo_desarrollo_activo,
    ruta_log_actual,
)
from app.core.version import APP_VERSION


_MAX_BACKUPS_VISIBLES = 3


@dataclass(frozen=True)
class ArchivoDiagnostico:
    """Resumen no sensible de un archivo diagnóstico conocido."""

    nombre: str
    existe: bool
    tamano_bytes: int
    actualizado_utc: str | None


def _timestamp_utc(ruta: Path) -> str | None:
    """Devuelve una fecha UTC legible sin exponer la ruta local."""

    if not ruta.is_file():
        return None
    return datetime.fromtimestamp(
        ruta.stat().st_mtime,
        tz=timezone.utc,
    ).isoformat(timespec="seconds")


def _resumir_archivo(ruta: Path) -> ArchivoDiagnostico:
    """Resume un archivo permitido sin abrir ni leer su contenido."""

    existe = ruta.is_file()
    return ArchivoDiagnostico(
        nombre=ruta.name,
        existe=existe,
        tamano_bytes=ruta.stat().st_size if existe else 0,
        actualizado_utc=_timestamp_utc(ruta) if existe else None,
    )


def archivos_diagnostico_conocidos() -> list[ArchivoDiagnostico]:
    """Lista únicamente el JSONL vigente y sus rotaciones esperadas."""

    actual = ruta_log_actual()
    candidatos = [actual]
    candidatos.extend(
        actual.with_suffix(actual.suffix + f".{numero}")
        for numero in range(1, _MAX_BACKUPS_VISIBLES + 1)
    )
    return [_resumir_archivo(ruta) for ruta in candidatos]


def _etiqueta_directorio() -> str:
    """Describe el directorio sin revelar rutas absolutas del equipo."""

    directorio = directorio_diagnostico()
    if directorio == Path.cwd() / "logs" / "diagnostico":
        return "logs/diagnostico"
    return "directorio personalizado definido por MRP_DIAGNOSTIC_DIR"


def construir_estado_centro_desarrollo() -> dict[str, Any]:
    """Construye el estado seguro mostrado por la interfaz DEV.2."""

    activo = modo_desarrollo_activo()
    archivos = archivos_diagnostico_conocidos()
    archivos_existentes = [archivo for archivo in archivos if archivo.existe]

    advertencias = [
        "No usar con datos personales reales, PDFs reales ni información financiera real.",
        "Los logs son locales y permanecen excluidos de Git.",
    ]
    if not activo:
        advertencias.insert(
            0,
            "Developer Diagnostics está desactivado; active MRP_DEV_MODE=1 solo durante desarrollo.",
        )

    return {
        "bloque": "DEV.2 R1",
        "titulo": "Centro de desarrollo",
        "descripcion": (
            "Superficie interna para revisar el estado técnico de Developer Diagnostics "
            "sin exponer datos personales, datos financieros, PDFs ni secretos."
        ),
        "app_version": APP_VERSION,
        "dev_mode_env": ENV_DEV_MODE,
        "diagnostic_dir_env": ENV_DIAGNOSTIC_DIR,
        "dev_mode_activo": activo,
        "schema_version": SCHEMA_VERSION,
        "directorio_diagnostico": _etiqueta_directorio(),
        "archivo_log_actual": ruta_log_actual().name,
        "archivos_diagnostico": [archivo.__dict__ for archivo in archivos],
        "total_archivos_existentes": len(archivos_existentes),
        "total_bytes": sum(archivo.tamano_bytes for archivo in archivos_existentes),
        "exportacion_zip_disponible": activo and bool(archivos_existentes),
        "advertencias": advertencias,
        "controles_privacidad": [
            "No lee cuerpos HTTP ni contenido de formularios.",
            "No lee ni exporta PDFs, uploads, bases de datos ni sessionStorage.",
            "No muestra rutas absolutas locales del equipo.",
            "No incluye identidad, ingresos, aportes ni importes de beneficio.",
            "El ZIP diagnóstico permitido se limita a archivos mrp-diagnostics.jsonl conocidos.",
        ],
    }
