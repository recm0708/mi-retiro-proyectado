"""Modelos de datos para los motores legales de pensión.

Este módulo contiene estructuras separadas del asistente general para
mantener explícitos los datos que consumen los motores jurídicos y los
desgloses que estos producen.
"""

from datetime import date

from pydantic import BaseModel, Field

from app.modelos.simulacion import (
    DatosHistorialSalarial,
    EscenarioRetiro,
    RegistroHistorialSalarial,
    ResumenLineaTiempo,
    ResumenRetiro,
)


class DatosCalculoSEBDNormal(BaseModel):
    """Datos necesarios para calcular una pensión normal del SEBD.

    La separación de cuotas adicionales antes y después de la edad de
    referencia es explícita porque la ley aplica porcentajes diferentes
    a cada grupo.
    """

    fecha_nacimiento: date
    sexo: str = Field(min_length=1)
    fecha_retiro: date

    cuotas_totales: int = Field(ge=0)

    cuotas_exceso_antes_referencia: int | None = Field(
        default=None,
        ge=0,
        description=(
            "Cuotas completas aportadas en exceso de las cuotas de "
            "referencia antes de alcanzar la edad de referencia."
        ),
    )

    cuotas_exceso_despues_referencia: int | None = Field(
        default=None,
        ge=0,
        description=(
            "Cuotas completas aportadas en exceso de las cuotas de "
            "referencia después de alcanzar la edad de referencia."
        ),
    )

    registros: list[RegistroHistorialSalarial]


class AnioSeleccionadoSEBD(BaseModel):
    """Año utilizado para formar el salario base del SEBD."""

    anio: int
    cuotas: int
    salario_cotizado: float


class ResumenCalculoSEBDNormal(BaseModel):
    """Desglose explicable del cálculo normal del SEBD."""

    modalidad: str
    elegible: bool
    motivos_no_elegible: list[str]

    edad_retiro_anios: int
    edad_referencia: int
    fecha_referencia: date

    cuotas_referencia: int
    cuotas_totales: int
    cuotas_exceso_total: int
    cuotas_exceso_antes_referencia: int
    cuotas_exceso_despues_referencia: int

    mejores_anios_requeridos: int
    anios_seleccionados: list[AnioSeleccionadoSEBD]
    total_salarios_seleccionados: float
    salario_base_mensual: float

    tasa_base_pct: float
    bloques_12_antes_referencia: int
    incremento_antes_referencia_pct: float
    bloques_12_despues_referencia: int
    incremento_despues_referencia_pct: float
    tasa_reemplazo_total_pct: float

    monto_antes_limite_maximo: float
    monto_maximo_aplicable: float
    pension_mensual_estimada: float

    minimo_indexado_aplicado: bool
    advertencias: list[str]
    fuente_normativa: str

# ============================================================
# Integración del asistente con el motor SEBD
# ============================================================

class DatosResultadoSEBDNormal(BaseModel):
    """Datos consolidados de los Pasos 1–5 para calcular SEBD normal."""

    fecha_nacimiento: date
    sexo: str = Field(min_length=1)

    historial: DatosHistorialSalarial
    linea_tiempo: ResumenLineaTiempo
    resumen_retiro: ResumenRetiro

    fecha_retiro_seleccionada: date
    escenario_salarial_nombre: str = Field(min_length=1)


class ResumenResultadoSEBDNormal(BaseModel):
    """Resultado SEBD normal unido al escenario elegido en el asistente."""

    escenario_retiro: EscenarioRetiro
    escenario_salarial_nombre: str

    anios_proyectados_incluidos: list[int]
    advertencias_integracion: list[str]

    calculo: ResumenCalculoSEBDNormal



# ============================================================
# Modalidades generales SEBD
# ============================================================

class DatosCalculoSEBD(BaseModel):
    """Datos para clasificar y calcular una prestación general del SEBD."""

    fecha_nacimiento: date
    sexo: str = Field(min_length=1)
    fecha_retiro: date
    cuotas_totales: int = Field(ge=0)

    cuotas_exceso_antes_referencia: int | None = Field(
        default=None,
        ge=0,
    )
    cuotas_exceso_despues_referencia: int | None = Field(
        default=None,
        ge=0,
    )

    registros: list[RegistroHistorialSalarial]


class ResumenCalculoSEBD(BaseModel):
    """Desglose común para las modalidades de retiro por vejez del SEBD."""

    modalidad: str
    modalidad_nombre: str
    tipo_prestacion: str
    elegible: bool
    calculo_disponible: bool
    motivos_no_elegible: list[str]

    edad_retiro_anios: int
    edad_referencia: int
    fecha_referencia: date
    fecha_minima_anticipada: date

    cuotas_referencia: int
    cuotas_minimas_proporcional: int
    cuotas_totales: int
    cuotas_exceso_total: int
    cuotas_exceso_antes_referencia: int
    cuotas_exceso_despues_referencia: int

    mejores_anios_requeridos: int
    anios_seleccionados: list[AnioSeleccionadoSEBD]
    total_salarios_seleccionados: float
    salario_base_mensual: float

    tasa_base_pct: float
    bloques_12_antes_referencia: int
    incremento_antes_referencia_pct: float
    bloques_12_despues_referencia: int
    incremento_despues_referencia_pct: float
    tasa_reemplazo_total_pct: float

    monto_antes_limite_maximo: float
    monto_maximo_aplicable: float
    monto_despues_limite_maximo: float

    factor_proporcional_cuotas: float | None
    factor_reduccion_edad: float
    meses_desde_limite_anticipado: int | None
    meses_anticipacion_referencia: int

    monto_despues_factor_proporcional: float | None
    pension_mensual_estimada: float | None

    # Campos exclusivos de la Indemnización por Vejez.
    # Para las modalidades de pensión permanecen en ``None``.
    indemnizacion_mensualidad_hipotetica: float | None = None
    indemnizacion_factor_cuotas: float | None = None
    indemnizacion_divisor_cuotas: int | None = None
    indemnizacion_pago_unico_estimado: float | None = None

    minimo_indexado_aplicado: bool
    advertencias: list[str]
    fuente_normativa: str


class DatosResultadoSEBD(BaseModel):
    """Datos consolidados de los Pasos 1–5 para cualquier modalidad SEBD."""

    fecha_nacimiento: date
    sexo: str = Field(min_length=1)

    historial: DatosHistorialSalarial
    linea_tiempo: ResumenLineaTiempo
    resumen_retiro: ResumenRetiro

    fecha_retiro_seleccionada: date
    escenario_salarial_nombre: str = Field(min_length=1)


class ResumenResultadoSEBD(BaseModel):
    """Resultado integrado del asistente para la modalidad SEBD detectada."""

    escenario_retiro: EscenarioRetiro
    escenario_salarial_nombre: str

    anios_proyectados_incluidos: list[int]
    advertencias_integracion: list[str]

    calculo: ResumenCalculoSEBD
