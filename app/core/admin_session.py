"""SEC.2 - Sesiones administrativas web temporales."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import secrets


DURACION_SESION = timedelta(minutes=30)

_sesiones: dict[str, datetime] = {}


def crear_sesion_admin() -> str:
    """Crea una sesión administrativa temporal."""
    limpiar_sesiones_expiradas()
    identificador = secrets.token_urlsafe(32)
    _sesiones[identificador] = datetime.now(timezone.utc)
    return identificador


def validar_sesion_admin(identificador: str) -> bool:
    """Valida una sesión administrativa existente."""
    limpiar_sesiones_expiradas()
    creada = _sesiones.get(identificador)

    if creada is None:
        return False

    if datetime.now(timezone.utc) - creada > DURACION_SESION:
        eliminar_sesion_admin(identificador)
        return False

    _sesiones[identificador] = datetime.now(timezone.utc)
    return True


def eliminar_sesion_admin(identificador: str) -> None:
    """Elimina una sesión administrativa."""
    _sesiones.pop(identificador, None)


def limpiar_sesiones_expiradas() -> None:
    """Elimina sesiones vencidas."""
    ahora = datetime.now(timezone.utc)

    for sesion, fecha in list(_sesiones.items()):
        if ahora - fecha > DURACION_SESION:
            eliminar_sesion_admin(sesion)
