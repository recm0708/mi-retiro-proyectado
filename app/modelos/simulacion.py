from typing import Literal
from pydantic import BaseModel, Field

class DatosCuotas(BaseModel):
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
    cuotas_reales: int
    cuotas_anio_actual: int
    cuotas_proyectadas_restantes_anio: int
    cuotas_proyectadas_cierre_anio: int

    faltantes_180: int
    faltantes_240: int

    anios_aprox_180: float | None
    anios_aprox_240: float | None

PeriodicidadSalario = Literal[
    "SEMANAL",
    "QUINCENAL",
    "MENSUAL",
    "ANUAL",
]

class DatosSalario(BaseModel):
    monto: float = Field(
        gt=0,
        description="Monto salarial indicado por el usuario.",
    )

    periodicidad: PeriodicidadSalario

class ResumenSalario(BaseModel):
    monto_original: float
    periodicidad_original: PeriodicidadSalario

    salario_semanal: float
    salario_quincenal: float
    salario_mensual: float
    salario_anual: float