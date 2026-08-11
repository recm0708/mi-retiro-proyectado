"""Modelos de datos utilizados durante una simulación previsional.

Los modelos Pydantic de este módulo definen la estructura y las
validaciones básicas de los datos intercambiados entre la interfaz,
los endpoints de FastAPI y los servicios de cálculo.
"""

from typing import Literal

from pydantic import BaseModel, Field


# ============================================================
# Cuotas
# ============================================================

class DatosCuotas(BaseModel):
    """Datos de cuotas proporcionados por el usuario."""

    cuotas_totales: int = Field(
        ge=0,
        description="Total de cuotas acreditadas por la CSS a la fecha.",
    )

    cuotas_anio_actual: int = Field(
        ge=0,
        le=12,
        description=(
            "Cuotas del año actual ya incluidas dentro "
            "del total de cuotas acreditadas."
        ),
    )

    continua_cotizando: bool

    cuotas_esperadas_cierre_anio: int = Field(
        ge=0,
        le=12,
        description="Cuotas esperadas al terminar el año actual.",
    )

    cuotas_esperadas_por_anio: int = Field(
        ge=0,
        le=12,
        description="Cuotas que se espera aportar por cada año futuro.",
    )


class ResumenCuotas(BaseModel):
    """Resultado preliminar del análisis de cuotas."""

    # Cuotas que ya constan como acreditadas.
    cuotas_reales: int

    # Cuotas reales correspondientes al año calendario actual.
    cuotas_anio_actual: int

    # Cuotas todavía no acreditadas que se proyectan para
    # completar el año en curso.
    cuotas_proyectadas_restantes_anio: int

    # Total esperado al cierre del año actual.
    cuotas_proyectadas_cierre_anio: int

    # Diferencias respecto de los umbrales preliminares.
    faltantes_180: int
    faltantes_240: int

    # Tiempo aproximado necesario para alcanzar cada umbral.
    # None indica que no puede alcanzarse con la proyección actual.
    anios_aprox_180: float | None
    anios_aprox_240: float | None


# ============================================================
# Salarios
# ============================================================

# Periodicidades aceptadas actualmente por la aplicación.
PeriodicidadSalario = Literal[
    "SEMANAL",
    "QUINCENAL",
    "MENSUAL",
    "ANUAL",
]


class DatosSalario(BaseModel):
    """Salario ingresado por el usuario en su periodicidad original."""

    monto: float = Field(
        gt=0,
        description="Monto salarial indicado por el usuario.",
    )

    periodicidad: PeriodicidadSalario


class ResumenSalario(BaseModel):
    """Equivalencias normalizadas de un salario."""

    # Se conserva el dato tal como fue proporcionado.
    monto_original: float
    periodicidad_original: PeriodicidadSalario

    # Equivalencias utilizadas por los cálculos posteriores.
    salario_semanal: float
    salario_quincenal: float
    salario_mensual: float
    salario_anual: float