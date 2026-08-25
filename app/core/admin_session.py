"""SEC.2 R6 - Sesiones administrativas web endurecidas."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import secrets

from app.core.config import (
    ADMIN_MAX_SESSIONS,
    ADMIN_SESSION_MAX_HOURS,
    ADMIN_SESSION_MINUTES,
)


@dataclass
class SesionAdministrativa:
    """Representa una sesión administrativa temporal."""

    identificador: str
    creada: datetime
    ultima_actividad: datetime


_sesiones: dict[str, SesionAdministrativa] = {}


def crear_sesion_admin() -> str:
    """Crea una sesión administrativa temporal."""
    limpiar_sesiones_expiradas()

    identificador = secrets.token_urlsafe(32)
    ahora = datetime.now(timezone.utc)

    _sesiones[identificador] = SesionAdministrativa(
        identificador=identificador,
        creada=ahora,
        ultima_actividad=ahora,
    )

    limitar_sesiones_activas()

    return identificador


def validar_sesion_admin(identificador: str) -> bool:
    """Valida una sesión administrativa existente."""
    limpiar_sesiones_expiradas()

    sesion = _sesiones.get(identificador)

    if sesion is None:
        return False

    ahora = datetime.now(timezone.utc)

    if ahora - sesion.ultima_actividad > timedelta(
        minutes=ADMIN_SESSION_MINUTES,
    ):
        eliminar_sesion_admin(identificador)
        return False

    if ahora - sesion.creada > timedelta(
        hours=ADMIN_SESSION_MAX_HOURS,
    ):
        eliminar_sesion_admin(identificador)
        return False

    sesion.ultima_actividad = ahora

    return True


def eliminar_sesion_admin(identificador: str) -> None:
    """Elimina una sesión administrativa."""
    _sesiones.pop(
        identificador,
        None,
    )


def obtener_sesiones_activas() -> list[str]:
    """Devuelve identificadores de sesiones activas."""
    limpiar_sesiones_expiradas()
    return list(_sesiones.keys())


def revocar_todas_las_sesiones_admin() -> None:
    """Revoca todas las sesiones administrativas."""
    _sesiones.clear()


def limpiar_sesiones_expiradas() -> None:
    """Elimina sesiones vencidas."""
    ahora = datetime.now(timezone.utc)

    for identificador, sesion in list(_sesiones.items()):
        if (
            ahora - sesion.ultima_actividad
            > timedelta(minutes=ADMIN_SESSION_MINUTES)
            or ahora - sesion.creada
            > timedelta(hours=ADMIN_SESSION_MAX_HOURS)
        ):
            eliminar_sesion_admin(identificador)


def limitar_sesiones_activas() -> None:
    """Mantiene el límite máximo de sesiones activas."""
    while len(_sesiones) > ADMIN_MAX_SESSIONS:
        primera = next(iter(_sesiones))
        eliminar_sesion_admin(primera)
