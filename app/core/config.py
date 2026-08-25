"""Configuración general y de identidad de la aplicación.

Los parámetros jurídicos y actuariales no se almacenan aquí. Se mantienen
versionados en ``regulations/`` para conservar la separación entre identidad,
configuración técnica y reglas previsionales.
"""

from os import getenv

from app.core.version import APP_VERSION


APP_NAME = "Mi Retiro Proyectado"
APP_DESCRIPTION = (
    "Herramienta web independiente para estimar, explicar y comparar "
    "escenarios de retiro de Asegurados(as) de la Caja de Seguro Social "
    "de Panamá."
)
APP_SUBTITLE = (
    "Estimación previsional independiente para Asegurados(as) de la CSS."
)
APP_AUDIENCE_SINGULAR = "Asegurado(a)"
APP_AUDIENCE_PLURAL = "Asegurados(as)"
APP_AUTHOR = "Rubén Enrique Cañizares Miranda"
MI_CAJA_DIGITAL_URL = "https://micajadigital.css.gob.pa/Auth/SignIn"


# ============================================================
# Configuración de seguridad administrativa web
# ============================================================

def _booleano_entorno(nombre: str, defecto: bool) -> bool:
    """Convierte una variable de entorno booleana."""
    valor = getenv(nombre)

    if valor is None:
        return defecto

    return valor.strip().lower() in {"1", "true", "yes", "on"}


def _entero_entorno(nombre: str, defecto: int) -> int:
    """Obtiene enteros configurables desde entorno."""
    valor = getenv(nombre)

    if valor is None:
        return defecto

    try:
        return int(valor)
    except ValueError:
        return defecto


ADMIN_SESSION_MINUTES = _entero_entorno(
    "MRP_ADMIN_SESSION_MINUTES",
    30,
)

ADMIN_SESSION_MAX_HOURS = _entero_entorno(
    "MRP_ADMIN_SESSION_MAX_HOURS",
    8,
)

ADMIN_COOKIE_SECURE = _booleano_entorno(
    "MRP_ADMIN_COOKIE_SECURE",
    False,
)

ADMIN_COOKIE_SAMESITE = getenv(
    "MRP_ADMIN_COOKIE_SAMESITE",
    "lax",
).strip().lower()

ADMIN_MAX_SESSIONS = _entero_entorno(
    "MRP_ADMIN_MAX_SESSIONS",
    5,
)
