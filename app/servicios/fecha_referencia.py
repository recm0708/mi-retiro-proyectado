"""Fecha de referencia verificable para controles de vigencia documental.

La aplicación no utiliza el reloj del navegador para decidir si una Ficha Digital
está actualizada. Cuando necesita una fecha de referencia intenta obtener el
encabezado HTTP ``Date`` de infraestructura oficial de la Caja de Seguro Social
por HTTPS. No se envían datos de la simulación en estas solicitudes.

Si la verificación externa falla, el resultado queda expresamente marcado como
no confiable. Los consumidores deben adoptar una conducta conservadora y pedir
revisión al usuario en vez de asumir que la fecha local del equipo es correcta.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from threading import Lock
from time import monotonic
from urllib.request import Request, urlopen

from app.core.observabilidad import registrar_evento


PANAMA_TZ = timezone(timedelta(hours=-5))
FUENTES_OFICIALES_FECHA = (
    ("CSS", "https://www.css.gob.pa/"),
    ("CSS_TRAMITES", "https://tramites.css.gob.pa/"),
)
_TIMEOUT_SEGUNDOS = 1.75
_CACHE_SEGUNDOS = 300.0


@dataclass(frozen=True)
class FechaReferencia:
    """Fecha externa y evidencia mínima de confianza para controles de vigencia."""

    fecha: date | None
    confiable: bool
    fuente: str


_cache_lock = Lock()
_cache_resultado: FechaReferencia | None = None
_cache_instante: float = 0.0


def _consultar_fecha_http(url: str) -> date | None:
    """Obtiene la fecha del servidor HTTPS sin enviar datos de simulación."""

    encabezado = None
    ultimo_error: Exception | None = None
    for metodo, extras in (
        ("HEAD", {}),
        ("GET", {"Range": "bytes=0-0"}),
    ):
        solicitud = Request(
            url,
            method=metodo,
            headers={
                "User-Agent": "MiRetiroProyectado/1.0",
                "Connection": "close",
                **extras,
            },
        )
        try:
            with urlopen(solicitud, timeout=_TIMEOUT_SEGUNDOS) as respuesta:  # nosec B310
                encabezado = respuesta.headers.get("Date")
            if encabezado:
                break
        except Exception as error:
            ultimo_error = error

    if not encabezado:
        if ultimo_error is not None:
            raise ultimo_error
        return None

    instante = parsedate_to_datetime(encabezado)
    if instante.tzinfo is None:
        instante = instante.replace(tzinfo=timezone.utc)
    return instante.astimezone(PANAMA_TZ).date()


def _consultar_fuentes() -> FechaReferencia:
    """Consulta en paralelo las fuentes oficiales y reconcilia sus fechas."""

    inicio = monotonic()
    fechas: list[tuple[str, date]] = []

    with ThreadPoolExecutor(max_workers=len(FUENTES_OFICIALES_FECHA)) as ejecutor:
        pendientes = {
            ejecutor.submit(_consultar_fecha_http, url): nombre
            for nombre, url in FUENTES_OFICIALES_FECHA
        }
        for tarea in as_completed(pendientes):
            nombre = pendientes[tarea]
            try:
                fecha = tarea.result()
            except Exception:
                continue
            if fecha is not None:
                fechas.append((nombre, fecha))

    metadata = {
        "source_count": len(FUENTES_OFICIALES_FECHA),
        "success_count": len(fechas),
    }

    if not fechas:
        registrar_evento(
            level="WARNING",
            event="external.date_reference.query",
            component="fecha_referencia",
            outcome="unavailable",
            duration_ms=(monotonic() - inicio) * 1000,
            metadata=metadata,
        )
        return FechaReferencia(
            fecha=None,
            confiable=False,
            fuente="NO_DISPONIBLE",
        )

    fechas_distintas = {fecha for _, fecha in fechas}
    if len(fechas_distintas) > 1:
        mas_antigua = min(fechas_distintas)
        mas_reciente = max(fechas_distintas)
        if (mas_reciente - mas_antigua).days > 1:
            registrar_evento(
                level="WARNING",
                event="external.date_reference.query",
                component="fecha_referencia",
                outcome="inconsistent",
                duration_ms=(monotonic() - inicio) * 1000,
                metadata=metadata,
            )
            return FechaReferencia(
                fecha=None,
                confiable=False,
                fuente="FUENTES_INCONSISTENTES",
            )

    # Una diferencia de un día puede ocurrir alrededor de medianoche UTC/Panamá.
    # Elegimos la fecha más reciente y registramos las fuentes que respondieron.
    fecha_elegida = max(fecha for _, fecha in fechas)
    fuentes = "+".join(nombre for nombre, _ in fechas)
    registrar_evento(
        level="INFO",
        event="external.date_reference.query",
        component="fecha_referencia",
        outcome="success",
        duration_ms=(monotonic() - inicio) * 1000,
        metadata=metadata,
    )
    return FechaReferencia(
        fecha=fecha_elegida,
        confiable=True,
        fuente=fuentes,
    )


def obtener_fecha_referencia_confiable(*, forzar: bool = False) -> FechaReferencia:
    """Devuelve una fecha externa verificada o un estado explícito no confiable.

    El resultado se cachea brevemente para evitar repetir solicitudes de red al
    analizar varios documentos en una misma sesión. Nunca se usa ``date.today``
    como sustituto silencioso cuando la verificación externa falla.
    """

    global _cache_resultado, _cache_instante

    ahora_monotono = monotonic()
    with _cache_lock:
        if (
            not forzar
            and _cache_resultado is not None
            and (ahora_monotono - _cache_instante) < _CACHE_SEGUNDOS
        ):
            registrar_evento(
                level="DEBUG",
                event="external.date_reference.cache",
                component="fecha_referencia",
                outcome="hit",
                metadata={"cache": "hit"},
            )
            return _cache_resultado

    registrar_evento(
        level="DEBUG",
        event="external.date_reference.cache",
        component="fecha_referencia",
        outcome="miss",
        metadata={"cache": "miss"},
    )
    resultado = _consultar_fuentes()

    with _cache_lock:
        _cache_resultado = resultado
        _cache_instante = monotonic()

    return resultado
