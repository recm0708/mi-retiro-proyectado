"""Configuración general y de identidad de la aplicación.

Los parámetros jurídicos y actuariales no se almacenan aquí. Se mantienen
versionados en ``regulations/`` para conservar la separación entre identidad,
configuración técnica y reglas previsionales.
"""

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
