"""Modelos transversales para comparar escenarios previsionales.

La comparación se construye sobre las solicitudes integradas ya utilizadas
por los motores SEBD, Mixto y SUCGS. No introduce fórmulas jurídicas nuevas:
solo normaliza resultados ya calculados por los servicios existentes.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.modelos.pension import (
    DatosResultadoMixto,
    DatosResultadoSEBD,
    DatosResultadoSUCGS,
)


SistemaComparacion = Literal[
    "SEBD",
    "MIXTO",
    "SUCGS",
]


class DatosComparacionEscenarios(BaseModel):
    """Solicitud para comparar combinaciones de retiro y salario.

    Debe incluir únicamente la estructura integrada que corresponda al
    sistema seleccionado. Las fechas y escenarios se toman de los Pasos 4 y
    5; si no se indican filtros, se comparan todas las alternativas vigentes.
    """

    sistema: SistemaComparacion

    datos_sebd: DatosResultadoSEBD | None = None
    datos_mixto: DatosResultadoMixto | None = None
    datos_sucgs: DatosResultadoSUCGS | None = None

    fechas_retiro: list[date] = Field(default_factory=list)
    escenarios_salariales: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validar_datos_del_sistema(self):
        """Exige exactamente el bloque de entrada del sistema elegido."""

        presentes = {
            "SEBD": self.datos_sebd is not None,
            "MIXTO": self.datos_mixto is not None,
            "SUCGS": self.datos_sucgs is not None,
        }

        if not presentes[self.sistema]:
            raise ValueError(
                "Faltan los datos integrados correspondientes al sistema "
                f"{self.sistema}."
            )

        if sum(1 for valor in presentes.values() if valor) != 1:
            raise ValueError(
                "La comparación debe recibir un único bloque de datos "
                "integrados, correspondiente al sistema seleccionado."
            )

        return self


class FilaComparacionEscenario(BaseModel):
    """Resultado normalizado de una combinación retiro/salario."""

    clave: str
    es_base: bool

    sistema: SistemaComparacion
    escenario_retiro_nombre: str
    tipo_retiro: str
    fecha_retiro: date
    edad_retiro_anios: int
    cuotas_estimadas_totales: int
    escenario_salarial_nombre: str

    modalidad: str | None
    modalidad_nombre: str | None
    tipo_prestacion: str | None
    calculo_completo: bool

    pension_mensual_estimada: float | None
    pago_unico_estimado: float | None

    diferencia_mensual_absoluta: float | None = None
    diferencia_mensual_pct: float | None = None
    diferencia_pago_unico_absoluta: float | None = None
    diferencia_pago_unico_pct: float | None = None

    advertencias: list[str] = Field(default_factory=list)


class ResumenComparacionEscenarios(BaseModel):
    """Matriz comparable y diferencias contra el escenario base."""

    sistema: SistemaComparacion
    nombre_sistema: str

    clave_escenario_base: str
    filas: list[FilaComparacionEscenario]

    total_combinaciones: int
    resultados_completos: int
    resultados_incompletos: int

    clave_mejor_pension_mensual: str | None = None
    clave_mayor_pago_unico: str | None = None

    advertencias: list[str] = Field(default_factory=list)
