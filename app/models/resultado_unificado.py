"""Contrato transversal del resultado final de una simulación.

Este modelo no sustituye los desgloses jurídicos de SEBD, Mixto o SUCGS.
Su objetivo es exponer con la misma semántica los datos que sí son comunes:
estado, naturaleza de la prestación, monto mensual, pago único y escenario.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


EstadoResultadoUnificado = Literal[
    "COMPLETO",
    "INCOMPLETO",
    "DECISION_REQUERIDA",
    "NO_ELEGIBLE",
    "TRANSICION",
]

NaturalezaPrestacionUnificada = Literal[
    "PENSION_MENSUAL",
    "PAGO_UNICO",
    "PENSION_MAS_PAGO_UNICO",
    "SIN_MONTO",
    "TRANSICION",
]


class ResumenPrestacionUnificada(BaseModel):
    """Resumen común que permite interpretar los tres motores igual."""

    sistema: Literal["SEBD", "MIXTO", "SUCGS"]
    nombre_sistema: str

    escenario_retiro_nombre: str
    fecha_retiro: date
    edad_retiro_anios: int
    cuotas_estimadas_totales: int
    escenario_salarial_nombre: str

    modalidad_codigo: str | None = None
    modalidad_nombre: str | None = None

    estado_resultado: EstadoResultadoUnificado
    naturaleza_prestacion: NaturalezaPrestacionUnificada
    calculo_completo: bool
    requiere_decision_usuario: bool = False

    pension_mensual_estimada: float | None = None
    pago_unico_estimado: float | None = None

    datos_no_confirmados: list[str] = Field(default_factory=list)
    advertencias: list[str] = Field(default_factory=list)
