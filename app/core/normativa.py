"""Carga y acceso a los parámetros normativos de la aplicación.

Los valores legales susceptibles de modificarse no deben quedar
dispersos directamente dentro de los motores de cálculo. Este
módulo centraliza la lectura de los archivos JSON almacenados
en el directorio ``normativa``.
"""

import json
from functools import lru_cache
from pathlib import Path


# ============================================================
# Rutas
# ============================================================

# Raíz del proyecto:
# calculadora-pension-css/
RAIZ_PROYECTO = (
    Path(__file__)
    .resolve()
    .parents[2]
)

DIRECTORIO_NORMATIVA = (
    RAIZ_PROYECTO
    / "normativa"
)


# ============================================================
# Carga de parámetros
# ============================================================

@lru_cache(maxsize=1)
def cargar_parametros_generales() -> dict:
    """Carga los parámetros legales generales versionados.

    El resultado se mantiene temporalmente en memoria para evitar
    leer el archivo desde disco en cada solicitud.
    """

    ruta = (
        DIRECTORIO_NORMATIVA
        / "parametros_generales.json"
    )

    if not ruta.exists():
        raise FileNotFoundError(
            "No se encontró el archivo "
            "normativa/parametros_generales.json."
        )

    with ruta.open(
        "r",
        encoding="utf-8",
    ) as archivo:
        return json.load(
            archivo,
        )


def obtener_edad_referencia(
    sexo: str,
) -> int:
    """Obtiene la edad de referencia correspondiente al sexo.

    Se aceptan varias representaciones comunes para mantener
    compatibilidad con la interfaz y futuras importaciones.
    """

    valor = (
        sexo
        .strip()
        .upper()
    )

    equivalencias = {
        "F": "FEMENINO",
        "FEMENINO": "FEMENINO",
        "MUJER": "FEMENINO",

        "M": "MASCULINO",
        "MASCULINO": "MASCULINO",
        "HOMBRE": "MASCULINO",
    }

    sexo_normalizado = (
        equivalencias.get(
            valor,
        )
    )

    if sexo_normalizado is None:
        raise ValueError(
            "El sexo indicado no es válido "
            "para determinar la edad de referencia."
        )

    parametros = (
        cargar_parametros_generales()
    )

    return int(
        parametros[
            "edades_referencia"
        ][sexo_normalizado]
    )

@lru_cache(maxsize=1)
def cargar_parametros_sebd() -> dict:
    """Carga los parámetros normativos versionados del SEBD."""

    ruta = (
        DIRECTORIO_NORMATIVA
        / "sebd.json"
    )

    if not ruta.exists():
        raise FileNotFoundError(
            "No se encontró el archivo normativa/sebd.json."
        )

    with ruta.open(
        "r",
        encoding="utf-8",
    ) as archivo:
        return json.load(
            archivo,
        )


@lru_cache(maxsize=1)
def cargar_parametros_mixto() -> dict:
    """Carga los parámetros normativos versionados del Subsistema Mixto."""

    ruta = (
        DIRECTORIO_NORMATIVA
        / "mixto.json"
    )

    if not ruta.exists():
        raise FileNotFoundError(
            "No se encontró el archivo normativa/mixto.json."
        )

    with ruta.open(
        "r",
        encoding="utf-8",
    ) as archivo:
        return json.load(archivo)


@lru_cache(maxsize=1)
def cargar_parametros_sucgs() -> dict:
    """Carga los parámetros normativos versionados del SUCGS."""

    ruta = (
        DIRECTORIO_NORMATIVA
        / "sucgs.json"
    )

    if not ruta.exists():
        raise FileNotFoundError(
            "No se encontró el archivo normativa/sucgs.json."
        )

    with ruta.open(
        "r",
        encoding="utf-8",
    ) as archivo:
        return json.load(archivo)
