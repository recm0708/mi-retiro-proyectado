"""Modelos de trazabilidad para explicar un cálculo previsional paso a paso.

La capa 6F.2 no vuelve a calcular la prestación. Solo transforma resultados
ya producidos por los motores legales en una secuencia auditable de datos,
reglas, fórmulas, sustituciones numéricas, resultados intermedios y fuentes.
"""

from typing import Literal

from pydantic import BaseModel, Field


class DatoTrazabilidad(BaseModel):
    """Dato de entrada o derivado que participa en la explicación."""

    clave: str
    etiqueta: str
    valor: str
    origen: str
    confirmado: bool | None = None


class FuenteTrazabilidad(BaseModel):
    """Fuente oficial enlazable utilizada por uno o más pasos."""

    id: str
    titulo: str
    referencia: str
    url: str
    articulos: list[str] = Field(default_factory=list)
    nota: str | None = None


class PasoTrazabilidad(BaseModel):
    """Paso explicativo de la cadena de cálculo."""

    orden: int = Field(ge=1)
    titulo: str
    regla: str
    formula: str | None = None
    sustitucion: str | None = None
    resultado: str | None = None
    redondeo: str | None = None
    fuentes: list[str] = Field(default_factory=list)


TipoResultadoTrazabilidad = Literal[
    "MENSUAL",
    "PAGO_UNICO",
    "MENSUAL_Y_PAGO_UNICO",
    "PENDIENTE",
]


class ResumenTrazabilidadCalculo(BaseModel):
    """Explicación transversal de un resultado SEBD, Mixto o SUCGS."""

    version_metodologia: str = "6F.2"
    sistema: str
    tipo_prestacion: str
    datos_utilizados: list[DatoTrazabilidad]
    pasos: list[PasoTrazabilidad]
    resultado_final_etiqueta: str
    resultado_final: str
    resultado_final_tipo: TipoResultadoTrazabilidad
    fuentes: list[FuenteTrazabilidad]
    advertencias: list[str] = Field(default_factory=list)
