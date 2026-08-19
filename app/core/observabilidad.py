"""Observabilidad local y Developer Diagnostics de Mi Retiro Proyectado.

El diagnóstico está desactivado por defecto y solo se habilita cuando
``MRP_DEV_MODE=1``. Los eventos usan un esquema JSONL deliberadamente
restrictivo: no deben incluir cuerpos HTTP, PDF, identificadores personales,
valores financieros ni mensajes de excepción potencialmente sensibles.
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar, Token
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
from threading import Lock
from time import monotonic
from typing import Any, Iterator, Mapping
from uuid import uuid4
from zipfile import ZIP_DEFLATED, ZipFile

from app.core.version import APP_VERSION


SCHEMA_VERSION = "1"
ENV_DEV_MODE = "MRP_DEV_MODE"
ENV_DIAGNOSTIC_DIR = "MRP_DIAGNOSTIC_DIR"

_LOG_FILENAME = "mrp-diagnostics.jsonl"
_MAX_BYTES = 1_048_576
_MAX_BACKUPS = 3
_MAX_STRING = 240

_CORRELATION_ID: ContextVar[str | None] = ContextVar(
    "mrp_correlation_id",
    default=None,
)
_WRITE_LOCK = Lock()

_SENSITIVE_KEY_PARTS = {
    "apellido",
    "archivo",
    "balance",
    "birth",
    "cedula",
    "cédula",
    "document",
    "documento",
    "email",
    "file",
    "filename",
    "identificador",
    "ingreso",
    "monto",
    "name",
    "nombre",
    "nss",
    "pension",
    "pensión",
    "pdf",
    "salary",
    "salario",
    "seguro_social",
    "ssn",
    "telefono",
    "teléfono",
    "token",
}

_SENSITIVE_TEXT_PATTERNS = (
    re.compile(r"\b\d{1,2}-\d{2,4}-\d{2,6}\b"),
    re.compile(r"\b\d{6,12}\b"),
    re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    re.compile(r"(?i)\b(?:B\/\.|\$|USD)\s*\d"),
)




_OPERACIONES_HTTP = {
    "/": "ui.inicio",
    "/simulacion": "ui.simulacion",
    "/comparar": "ui.comparar",
    "/metodologia": "ui.metodologia",
    "/salud": "system.health",
    "/api/sistema/fecha-referencia": "system.date_reference",
    "/api/simulacion/cuotas": "simulation.cuotas",
    "/api/simulacion/historial-salarial": "simulation.historial",
    "/api/simulacion/detalle-anio-actual": "simulation.detalle_actual",
    "/api/simulacion/referencia-mi-retiro-seguro": "import.mi_retiro_seguro",
    "/api/simulacion/ficha-digital": "import.ficha_digital",
    "/api/simulacion/salario": "simulation.salario",
    "/api/simulacion/proyeccion-salario": "simulation.proyeccion_salario",
    "/api/simulacion/linea-tiempo": "simulation.linea_tiempo",
    "/api/simulacion/retiro": "simulation.retiro",
    "/api/simulacion/sebd/normal": "motor.sebd.normal",
    "/api/simulacion/resultados/sebd-normal": "result.sebd.normal",
    "/api/simulacion/sebd": "motor.sebd",
    "/api/simulacion/resultados/sebd": "result.sebd",
    "/api/simulacion/mixto": "motor.mixto",
    "/api/simulacion/resultados/mixto": "result.mixto",
    "/api/simulacion/sucgs": "motor.sucgs",
    "/api/simulacion/resultados/sucgs": "result.sucgs",
    "/api/simulacion/comparar-escenarios": "result.compare",
}


def clasificar_operacion_http(path: str) -> str | None:
    """Clasifica una ruta sin registrar el path arbitrario solicitado.

    Recursos estáticos y favicon se omiten para reducir ruido. Una ruta no
    reconocida se agrupa como ``http.other`` y nunca se escribe literalmente.
    """

    if path == "/favicon.ico" or path.startswith("/static/"):
        return None
    return _OPERACIONES_HTTP.get(path, "http.other")


def modo_desarrollo_activo() -> bool:
    """Devuelve ``True`` únicamente con activación explícita ``MRP_DEV_MODE=1``."""

    return os.getenv(ENV_DEV_MODE, "").strip() == "1"


def directorio_diagnostico() -> Path:
    """Resuelve el directorio local de diagnóstico sin crear nada todavía."""

    personalizado = os.getenv(ENV_DIAGNOSTIC_DIR, "").strip()
    if personalizado:
        return Path(personalizado).expanduser()
    return Path.cwd() / "logs" / "diagnostico"


def ruta_log_actual() -> Path:
    """Ruta del archivo JSONL vigente."""

    return directorio_diagnostico() / _LOG_FILENAME


def nueva_correlacion() -> str:
    """Genera un identificador aleatorio no derivado del usuario."""

    return uuid4().hex


def correlacion_actual() -> str | None:
    """Obtiene el ID de correlación del contexto actual."""

    return _CORRELATION_ID.get()


def establecer_correlacion(correlation_id: str | None = None) -> Token:
    """Establece una correlación y devuelve el token para restaurarla."""

    return _CORRELATION_ID.set(correlation_id or nueva_correlacion())


def restablecer_correlacion(token: Token) -> None:
    """Restaura el contexto anterior."""

    _CORRELATION_ID.reset(token)


@contextmanager
def contexto_correlacion(
    correlation_id: str | None = None,
) -> Iterator[str]:
    """Context manager útil para operaciones internas y pruebas."""

    token = establecer_correlacion(correlation_id)
    try:
        actual = correlacion_actual()
        assert actual is not None
        yield actual
    finally:
        restablecer_correlacion(token)


def _clave_sensible(clave: str) -> bool:
    """Indica si el nombre de una clave puede identificar metadata sensible."""

    normalizada = clave.casefold().replace("-", "_")
    return any(fragmento in normalizada for fragmento in _SENSITIVE_KEY_PARTS)


def _texto_potencialmente_sensible(texto: str) -> bool:
    """Detecta patrones textuales que no deben persistirse en diagnóstico."""

    return any(patron.search(texto) for patron in _SENSITIVE_TEXT_PATTERNS)


def _sanitizar_valor(clave: str, valor: Any) -> Any:
    """Redacta y limita recursivamente un valor antes de escribirlo en JSONL."""

    if _clave_sensible(clave):
        return "[REDACTED]"

    if valor is None or isinstance(valor, (bool, int)):
        return valor

    if isinstance(valor, float):
        return round(valor, 3)

    if isinstance(valor, str):
        limpio = valor.replace("\r", " ").replace("\n", " ").strip()
        if _texto_potencialmente_sensible(limpio):
            return "[REDACTED]"
        return limpio[:_MAX_STRING]

    if isinstance(valor, Mapping):
        return {
            str(subclave): _sanitizar_valor(str(subclave), subvalor)
            for subclave, subvalor in valor.items()
        }

    if isinstance(valor, (list, tuple, set)):
        return [
            _sanitizar_valor(clave, elemento)
            for elemento in list(valor)[:20]
        ]

    return type(valor).__name__


def sanitizar_metadata(
    metadata: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Redacta metadata antes de escribirla en disco."""

    if not metadata:
        return {}
    return {
        str(clave): _sanitizar_valor(str(clave), valor)
        for clave, valor in metadata.items()
    }


def _rotar_si_corresponde(ruta: Path, bytes_entrantes: int) -> None:
    """Rota el log cuando la siguiente escritura superaría el límite local."""

    if not ruta.exists():
        return
    if ruta.stat().st_size + bytes_entrantes <= _MAX_BYTES:
        return

    ultimo = ruta.with_suffix(ruta.suffix + f".{_MAX_BACKUPS}")
    if ultimo.exists():
        ultimo.unlink()

    for numero in range(_MAX_BACKUPS - 1, 0, -1):
        origen = ruta.with_suffix(ruta.suffix + f".{numero}")
        destino = ruta.with_suffix(ruta.suffix + f".{numero + 1}")
        if origen.exists():
            origen.replace(destino)

    ruta.replace(ruta.with_suffix(ruta.suffix + ".1"))


def registrar_evento(
    *,
    level: str,
    event: str,
    component: str,
    outcome: str,
    duration_ms: float | None = None,
    metadata: Mapping[str, Any] | None = None,
    correlation_id: str | None = None,
) -> bool:
    """Escribe un evento seguro si Developer Diagnostics está habilitado.

    Retorna ``True`` cuando se escribió y ``False`` cuando el modo está apagado.
    """

    if not modo_desarrollo_activo():
        return False

    correlation = correlation_id or correlacion_actual() or nueva_correlacion()

    evento = {
        "schema_version": SCHEMA_VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "level": str(level).upper(),
        "event": str(event)[:120],
        "component": str(component)[:120],
        "app_version": APP_VERSION,
        "correlation_id": correlation,
        "duration_ms": (
            None
            if duration_ms is None
            else round(max(0.0, float(duration_ms)), 3)
        ),
        "outcome": str(outcome)[:80],
        "metadata": sanitizar_metadata(metadata),
    }

    linea = json.dumps(
        evento,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ) + "\n"
    encoded = linea.encode("utf-8")
    ruta = ruta_log_actual()

    with _WRITE_LOCK:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        _rotar_si_corresponde(ruta, len(encoded))
        with ruta.open("a", encoding="utf-8", newline="\n") as archivo:
            archivo.write(linea)

    return True


def registrar_excepcion(
    *,
    event: str,
    component: str,
    error: BaseException,
    duration_ms: float | None = None,
    metadata: Mapping[str, Any] | None = None,
    correlation_id: str | None = None,
) -> bool:
    """Registra solo la clase de excepción; nunca el mensaje original."""

    segura = {
        "exception_type": type(error).__name__,
        **sanitizar_metadata(metadata),
    }
    return registrar_evento(
        level="ERROR",
        event=event,
        component=component,
        outcome="error",
        duration_ms=duration_ms,
        metadata=segura,
        correlation_id=correlation_id,
    )


@contextmanager
def medir_evento(
    *,
    level: str,
    event: str,
    component: str,
    metadata: Mapping[str, Any] | None = None,
) -> Iterator[None]:
    """Mide una operación sin ejecutarla más de una vez."""

    inicio = monotonic()
    try:
        yield
    except Exception as error:
        registrar_excepcion(
            event=event,
            component=component,
            error=error,
            duration_ms=(monotonic() - inicio) * 1000,
            metadata=metadata,
        )
        raise
    else:
        registrar_evento(
            level=level,
            event=event,
            component=component,
            outcome="success",
            duration_ms=(monotonic() - inicio) * 1000,
            metadata=metadata,
        )


def exportar_diagnostico(
    destino: str | Path | None = None,
) -> Path:
    """Empaqueta exclusivamente los JSONL diagnósticos conocidos.

    La función solo opera con Developer Diagnostics activo. No recorre el
    repositorio ni incluye bases de datos, documentos, PDFs, uploads o archivos
    de sesión.
    """

    if not modo_desarrollo_activo():
        raise RuntimeError(
            "Developer Diagnostics está desactivado; use MRP_DEV_MODE=1."
        )

    directorio = directorio_diagnostico()
    directorio.mkdir(parents=True, exist_ok=True)

    if destino is None:
        destino_path = directorio / "mrp-diagnostics-export.zip"
    else:
        destino_path = Path(destino).expanduser()

    destino_path.parent.mkdir(parents=True, exist_ok=True)

    candidatos = [ruta_log_actual()] + [
        ruta_log_actual().with_suffix(
            ruta_log_actual().suffix + f".{numero}"
        )
        for numero in range(1, _MAX_BACKUPS + 1)
    ]

    temporal = destino_path.with_suffix(destino_path.suffix + ".tmp")
    if temporal.exists():
        temporal.unlink()

    with ZipFile(temporal, "w", compression=ZIP_DEFLATED) as paquete:
        for candidato in candidatos:
            if candidato.is_file():
                paquete.write(
                    candidato,
                    arcname=candidato.name,
                )

    shutil.move(str(temporal), str(destino_path))
    return destino_path
