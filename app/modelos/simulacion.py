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
        description=(
            "Total de cuotas acreditadas por la CSS a la fecha."
        ),
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
        description=(
            "Cuotas esperadas al terminar el año actual."
        ),
    )

    cuotas_esperadas_por_anio: int = Field(
        ge=0,
        le=12,
        description=(
            "Cuotas que se espera aportar por cada año futuro."
        ),
    )


class ResumenCuotas(BaseModel):
    """Resultado preliminar del análisis de cuotas."""

    cuotas_reales: int
    cuotas_anio_actual: int

    cuotas_proyectadas_restantes_anio: int
    cuotas_proyectadas_cierre_anio: int

    faltantes_180: int
    faltantes_240: int

    anios_aprox_180: float | None
    anios_aprox_240: float | None


# ============================================================
# Historial salarial
# ============================================================

EstadoRegistroHistorial = Literal[
    "SIN_COTIZACION",
    "HISTORICO_PARCIAL",
    "HISTORICO_COMPLETO",
]


class RegistroHistorialSalarial(BaseModel):
    """Registro histórico correspondiente a un año calendario.

    ``salario_cotizado`` representa el total de salario reportado
    a la CSS durante ese año. No representa necesariamente un
    salario anualizado de doce meses.
    """

    anio: int = Field(
        ge=1900,
        le=2200,
    )

    cuotas: int = Field(
        ge=0,
        le=12,
    )

    salario_cotizado: float = Field(
        ge=0,
        description=(
            "Total de salario reportado a la CSS "
            "durante el año indicado."
        ),
    )


class RegistroHistorialNormalizado(BaseModel):
    """Registro histórico validado por el servicio."""

    anio: int
    cuotas: int
    salario_cotizado: float
    estado: EstadoRegistroHistorial


class DatosHistorialSalarial(BaseModel):
    """Historial salarial enviado para análisis."""

    anio_inicio: int = Field(
        ge=1900,
        le=2200,
    )

    anio_fin: int = Field(
        ge=1900,
        le=2200,
    )

    # Este valor proviene del Paso 2 y permite comprobar
    # si las cuotas anuales suministradas explican el total.
    cuotas_totales_referencia: int = Field(
        ge=0,
    )

    registros: list[
        RegistroHistorialSalarial
    ]


class ResumenHistorialSalarial(BaseModel):
    """Resultado de la validación del historial salarial."""

    anio_inicio: int
    anio_fin: int

    cuotas_totales_referencia: int
    cuotas_sumadas: int
    diferencia_cuotas: int
    cuotas_coinciden: bool

    historial_completo: bool
    anios_sin_registro: list[int]

    total_salarios_reportados: float

    ultimo_anio_con_cuotas: int | None
    ultimo_salario_cotizado: float | None

    registros: list[
        RegistroHistorialNormalizado
    ]


# ============================================================
# Salario actual
# ============================================================

# El salario actual se conserva separado del historial porque
# representa la remuneración vigente utilizada como base para
# proyectar períodos todavía no cotizados.
PeriodicidadSalario = Literal[
    "SEMANAL",
    "QUINCENAL",
    "MENSUAL",
    "ANUAL",
]


class DatosSalario(BaseModel):
    """Salario actual ingresado en su periodicidad original."""

    monto: float = Field(
        gt=0,
        description=(
            "Monto salarial actual indicado por el usuario."
        ),
    )

    periodicidad: PeriodicidadSalario


class ResumenSalario(BaseModel):
    """Equivalencias normalizadas del salario actual."""

    monto_original: float
    periodicidad_original: PeriodicidadSalario

    salario_semanal: float
    salario_quincenal: float
    salario_mensual: float
    salario_anual: float


# ============================================================
# Proyección salarial
# ============================================================

ModalidadProyeccionSalario = Literal[
    "CONSTANTE",
    "PORCENTAJE",
    "FUTURO_CONOCIDO",
    "ESCENARIOS",
]


class DatosProyeccionSalario(BaseModel):
    """Parámetros utilizados para proyectar el salario futuro."""

    salario_mensual_actual: float = Field(
        gt=0,
        description=(
            "Salario mensual utilizado como punto de partida."
        ),
    )

    anio_inicio: int = Field(
        ge=1900,
        le=2200,
    )

    anio_fin: int = Field(
        ge=1900,
        le=2200,
    )

    modalidad: ModalidadProyeccionSalario

    porcentaje_anual: float | None = Field(
        default=None,
        ge=-99.99,
        le=100,
    )

    salario_mensual_futuro: float | None = Field(
        default=None,
        gt=0,
    )

    anio_salario_futuro: int | None = Field(
        default=None,
        ge=1900,
        le=2200,
    )

    escenarios_porcentajes: list[float] = Field(
        default_factory=lambda: [
            0.0,
            1.0,
            2.0,
            3.0,
        ],
    )


class ProyeccionSalarioAnual(BaseModel):
    """Salario proyectado correspondiente a un año."""

    anio: int
    salario_mensual: float
    salario_anual: float
    crecimiento_desde_base_pct: float


class EscenarioProyeccionSalario(BaseModel):
    """Serie anual correspondiente a un escenario salarial."""

    nombre: str
    tasa_anual_pct: float

    registros: list[
        ProyeccionSalarioAnual
    ]


class ResumenProyeccionSalario(BaseModel):
    """Resultado completo de una proyección salarial."""

    modalidad: ModalidadProyeccionSalario
    anio_inicio: int
    anio_fin: int

    escenarios: list[
        EscenarioProyeccionSalario
    ]

# ============================================================
# Línea temporal histórica y proyectada
# ============================================================

EstadoLineaTiempo = Literal[
    "HISTORICO",
    "HISTORICO_PARCIAL",
    "MIXTO",
    "PROYECTADO",
    "PENDIENTE",
]


class RegistroLineaTiempo(BaseModel):
    """Registro anual que separa información real y proyectada."""

    anio: int

    # Información que ya consta como histórica.
    cuotas_historicas: int
    salario_historico: float

    # Información todavía estimada.
    cuotas_proyectadas: int
    salario_proyectado: float

    # Valores esperados al cierre del año.
    cuotas_cierre: int
    salario_cierre: float

    estado: EstadoLineaTiempo


class EscenarioLineaTiempo(BaseModel):
    """Línea temporal completa correspondiente a un escenario."""

    nombre: str
    tasa_anual_pct: float

    registros: list[
        RegistroLineaTiempo
    ]


class DatosLineaTiempo(BaseModel):
    """Información necesaria para unir historial y proyección."""

    historial: DatosHistorialSalarial
    cuotas: DatosCuotas
    salario_actual: DatosSalario
    proyeccion: DatosProyeccionSalario


class ResumenLineaTiempo(BaseModel):
    """Resultado completo de la unión histórica y proyectada."""

    anio_inicio_historico: int
    anio_actual: int
    anio_fin_proyeccion: int

    escenarios: list[
        EscenarioLineaTiempo
    ]