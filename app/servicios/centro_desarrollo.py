"""Servicios seguros para DEV.2 — Centro de desarrollo.

El Centro de desarrollo expone metadata técnica, un visor acotado de eventos
JSONL y una exportación controlada de Developer Diagnostics. No lee documentos
personales, no inspecciona cuerpos HTTP y no devuelve rutas absolutas locales.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping

from app.core.observabilidad import (
    ENV_DEV_MODE,
    ENV_DIAGNOSTIC_DIR,
    SCHEMA_VERSION,
    directorio_diagnostico,
    exportar_diagnostico,
    modo_desarrollo_activo,
    ruta_log_actual,
)
from app.core.version import APP_VERSION


_MAX_BACKUPS_VISIBLES = 3
_MAX_EVENTOS_VISIBLES = 12
_MAX_TEXTO_EVENTO = 120
_METADATA_VISIBLE = {
    "exception_type",
    "method",
    "operation",
    "status_code",
}


@dataclass(frozen=True)
class ArchivoDiagnostico:
    """Resumen no sensible de un archivo diagnóstico conocido."""

    nombre: str
    existe: bool
    tamano_bytes: int
    actualizado_utc: str | None


@dataclass(frozen=True)
class EventoDiagnostico:
    """Evento JSONL resumido para revisión local sin datos de simulación."""

    archivo: str
    timestamp: str
    level: str
    event: str
    component: str
    outcome: str
    correlation_id: str | None
    duration_ms: float | None
    metadata: dict[str, Any]


def _timestamp_utc(ruta: Path) -> str | None:
    """Devuelve una fecha UTC legible sin exponer la ruta local."""

    if not ruta.is_file():
        return None
    return datetime.fromtimestamp(
        ruta.stat().st_mtime,
        tz=timezone.utc,
    ).isoformat(timespec="seconds")


def _resumir_archivo(ruta: Path) -> ArchivoDiagnostico:
    """Resume un archivo permitido sin abrir ni leer su contenido completo."""

    existe = ruta.is_file()
    return ArchivoDiagnostico(
        nombre=ruta.name,
        existe=existe,
        tamano_bytes=ruta.stat().st_size if existe else 0,
        actualizado_utc=_timestamp_utc(ruta) if existe else None,
    )


def _rutas_diagnostico_conocidas() -> list[Path]:
    """Devuelve el JSONL vigente y sus rotaciones esperadas."""

    actual = ruta_log_actual()
    candidatos = [actual]
    candidatos.extend(
        actual.with_suffix(actual.suffix + f".{numero}")
        for numero in range(1, _MAX_BACKUPS_VISIBLES + 1)
    )
    return candidatos


def archivos_diagnostico_conocidos() -> list[ArchivoDiagnostico]:
    """Lista únicamente el JSONL vigente y sus rotaciones esperadas."""

    return [_resumir_archivo(ruta) for ruta in _rutas_diagnostico_conocidas()]


def _etiqueta_directorio() -> str:
    """Describe el directorio sin revelar rutas absolutas del equipo."""

    directorio = directorio_diagnostico()
    if directorio == Path.cwd() / "logs" / "diagnostico":
        return "logs/diagnostico"
    return "directorio personalizado definido por MRP_DIAGNOSTIC_DIR"


def _texto_seguro(valor: Any, *, maximo: int = _MAX_TEXTO_EVENTO) -> str:
    """Convierte valores técnicos a texto corto sin expandir estructuras."""

    if valor is None:
        return ""
    if isinstance(valor, (bool, int, float)):
        return str(valor)
    texto = str(valor).replace("\r", " ").replace("\n", " ").strip()
    return texto[:maximo]


def _metadata_visible(metadata: Mapping[str, Any] | None) -> dict[str, Any]:
    """Expone solo metadata operacional permitida para el visor DEV.2."""

    if not metadata:
        return {}

    visible: dict[str, Any] = {}
    for clave in sorted(_METADATA_VISIBLE):
        if clave not in metadata:
            continue
        valor = metadata[clave]
        if clave == "status_code" and isinstance(valor, int):
            visible[clave] = valor
        else:
            visible[clave] = _texto_seguro(valor)
    return visible


def _evento_desde_json(archivo: str, datos: Mapping[str, Any]) -> EventoDiagnostico:
    """Normaliza un evento JSONL a campos seguros para la plantilla."""

    correlation_id = datos.get("correlation_id")
    if isinstance(correlation_id, str):
        correlation_id_visible = correlation_id[:32]
    else:
        correlation_id_visible = None

    duration = datos.get("duration_ms")
    duration_ms = round(float(duration), 3) if isinstance(duration, (int, float)) else None

    metadata = datos.get("metadata")
    return EventoDiagnostico(
        archivo=archivo,
        timestamp=_texto_seguro(datos.get("timestamp")),
        level=_texto_seguro(datos.get("level") or "INFO", maximo=24).upper(),
        event=_texto_seguro(datos.get("event")),
        component=_texto_seguro(datos.get("component")),
        outcome=_texto_seguro(datos.get("outcome")),
        correlation_id=correlation_id_visible,
        duration_ms=duration_ms,
        metadata=_metadata_visible(metadata if isinstance(metadata, Mapping) else None),
    )


def leer_eventos_diagnostico(
    limite: int = _MAX_EVENTOS_VISIBLES,
) -> tuple[list[EventoDiagnostico], int]:
    """Lee eventos recientes de JSONL sin exponer valores arbitrarios."""

    eventos: list[EventoDiagnostico] = []
    invalidos = 0

    for ruta in _rutas_diagnostico_conocidas():
        if not ruta.is_file():
            continue
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            if not linea.strip():
                continue
            try:
                datos = json.loads(linea)
            except json.JSONDecodeError:
                invalidos += 1
                continue
            if not isinstance(datos, Mapping):
                invalidos += 1
                continue
            eventos.append(_evento_desde_json(ruta.name, datos))

    eventos_ordenados = sorted(
        eventos,
        key=lambda evento: evento.timestamp,
        reverse=True,
    )
    return eventos_ordenados[: max(0, limite)], invalidos


def _resumen_por_nivel(eventos: list[EventoDiagnostico]) -> dict[str, int]:
    """Cuenta eventos visibles por nivel operacional."""

    resumen = {"INFO": 0, "WARNING": 0, "ERROR": 0, "OTRO": 0}
    for evento in eventos:
        if evento.level in resumen:
            resumen[evento.level] += 1
        else:
            resumen["OTRO"] += 1
    return resumen


def exportar_zip_diagnostico_sanitizado() -> Path:
    """Genera el ZIP diagnóstico permitido si hay logs locales disponibles."""

    if not modo_desarrollo_activo():
        raise PermissionError(
            "Developer Diagnostics está desactivado; active MRP_DEV_MODE=1."
        )

    if not any(ruta.is_file() for ruta in _rutas_diagnostico_conocidas()):
        raise FileNotFoundError(
            "No existen archivos diagnósticos para exportar."
        )

    return exportar_diagnostico()


def construir_estado_centro_desarrollo() -> dict[str, Any]:
    """Construye el estado seguro mostrado por la interfaz DEV.2."""

    activo = modo_desarrollo_activo()
    archivos = archivos_diagnostico_conocidos()
    archivos_existentes = [archivo for archivo in archivos if archivo.existe]
    eventos, invalidos = leer_eventos_diagnostico()

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
        "revision_actual": "DEV.2 R2",
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
        "eventos_recientes": [evento.__dict__ for evento in eventos],
        "total_eventos_visibles": len(eventos),
        "total_eventos_invalidos": invalidos,
        "resumen_eventos": _resumen_por_nivel(eventos),
        "advertencias": advertencias,
        "controles_privacidad": [
            "No lee cuerpos HTTP ni contenido de formularios.",
            "No lee ni exporta PDFs, uploads, bases de datos ni sessionStorage.",
            "No muestra rutas absolutas locales del equipo.",
            "No incluye identidad, ingresos, aportes ni importes de beneficio.",
            "El ZIP diagnóstico permitido se limita a archivos mrp-diagnostics.jsonl conocidos.",
            "El visor muestra solo metadata operacional permitida.",
        ],
    }
