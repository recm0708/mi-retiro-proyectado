"""Modelos de datos para los motores legales de pensión.

Este módulo contiene estructuras separadas del asistente general para
mantener explícitos los datos que consumen los motores jurídicos y los
desgloses que estos producen.
"""

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

from app.modelos.trazabilidad import ResumenTrazabilidadCalculo
from app.modelos.resultado_unificado import ResumenPrestacionUnificada

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

    trazabilidad: ResumenTrazabilidadCalculo | None = None
    resumen_unificado: ResumenPrestacionUnificada | None = None
    calculo: ResumenCalculoSEBD


# ============================================================
# Subsistema Mixto
# ============================================================

SistemaMixtoSeleccionado = Literal[
    "MIXTO",
    "SUCGS",
]

OpcionPrestacionCAP = Literal[
    "AUTO",
    "PENSION_PROGRAMADA",
    "DEVOLUCION_TOTAL",
]


class DatosCalculoMixto(BaseModel):
    """Datos necesarios para evaluar una prestación de vejez del Mixto.

    El Componente de Ahorro Personal requiere el saldo ahorrado y
    capitalizado a la fecha de solicitud. El valor actuarial se mantiene
    como entrada explícita mientras no exista un parámetro público vigente
    versionado por la aplicación.

    ``opcion_prestacion_cap`` permite separar la pensión programada de la
    devolución total prevista por el artículo 187 cuando esta última puede
    solicitarse. ``AUTO`` nunca elige silenciosamente una devolución: si la
    persona tiene ambas alternativas, la salida exige una decisión expresa.
    """

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

    sistema_seleccionado: SistemaMixtoSeleccionado = "MIXTO"

    saldo_ahorro_personal: float | None = Field(
        default=None,
        ge=0,
        description=(
            "Saldo ahorrado y capitalizado del Componente de Ahorro "
            "Personal a la fecha de solicitud."
        ),
    )
    bono_reconocimiento: float = Field(
        default=0.0,
        ge=0,
        description=(
            "Monto del bono de reconocimiento ya determinado. La aplicación "
            "todavía no calcula automáticamente este bono."
        ),
    )
    bono_reconocimiento_confirmado_oficialmente: bool = Field(
        default=False,
        description=(
            "Indica si el monto del bono proviene de un dato oficial o ya "
            "validado para el Asegurado(a)."
        ),
    )
    valor_actuarial_expectativa_vida: float | None = Field(
        default=None,
        gt=0,
        description=(
            "Divisor actuarial oficial aplicable al Componente de "
            "Ahorro Personal según expectativa de vida y tasa de descuento."
        ),
    )
    opcion_prestacion_cap: OpcionPrestacionCAP = Field(
        default="AUTO",
        description=(
            "AUTO calcula la pensión programada cuando no existe una opción "
            "de devolución. Cuando el artículo 187 permite devolución, AUTO "
            "deja la decisión pendiente en vez de escoger por el Asegurado(a)."
        ),
    )


class AnioSeleccionadoMixtoBD(BaseModel):
    """Año utilizado en la base del Componente de Beneficio Definido."""

    anio: int
    cuotas: int
    salario_cotizado_original: float
    salario_considerado_bd: float


class ResumenComponenteBeneficioDefinidoMixto(BaseModel):
    """Desglose del Componente de Beneficio Definido del Mixto."""

    modalidad: str
    modalidad_nombre: str
    tipo_prestacion: str
    elegible: bool
    calculo_disponible: bool

    salario_mensual_maximo_participacion: float
    anios_seleccionados: list[AnioSeleccionadoMixtoBD]
    total_salarios_considerados: float
    salario_base_mensual: float

    tasa_base_pct: float
    incremento_antes_referencia_pct: float
    incremento_despues_referencia_pct: float
    tasa_reemplazo_total_pct: float

    factor_proporcional_cuotas: float | None
    factor_reduccion_edad: float

    monto_antes_maximo: float
    monto_maximo_componente: float
    pension_mensual_estimada: float | None

    indemnizacion_mensualidad_hipotetica: float | None = None
    indemnizacion_pago_unico_estimado: float | None = None

    usa_aproximacion_anual_tope_mensual: bool
    advertencias: list[str]


class ResumenComponenteAhorroPersonalMixto(BaseModel):
    """Desglose del Componente de Ahorro Personal del Mixto."""

    calculo_disponible: bool
    saldo_ahorro_personal: float | None
    bono_reconocimiento: float
    bono_reconocimiento_confirmado_oficialmente: bool
    capital_total_considerado: float | None
    valor_actuarial_expectativa_vida: float | None

    opcion_solicitada: OpcionPrestacionCAP
    decision_requerida: bool

    pension_programada_mensual: float | None
    devolucion_total_disponible: bool
    devolucion_pago_unico_estimado: float | None

    garantia_renta_vitalicia_aplica: bool
    garantia_monto_mensual: float | None
    garantia_condicion_activacion: str | None
    prima_renta_vitalicia_pct_referencia: float | None
    prima_renta_vitalicia_es_referencia_historica: bool

    monto_maximo_aplicable: float | None
    advertencias: list[str]


class ResumenCalculoMixto(BaseModel):
    """Resultado del motor de vejez del Subsistema Mixto."""

    sistema_solicitado: str
    estado_sistema: str
    calculo_mixto_aplicable: bool
    fecha_fin_calculo_mixto: date
    fecha_inicio_calculo_sucgs: date

    modalidad: str | None
    modalidad_nombre: str | None
    tipo_prestacion: str | None
    elegible: bool
    calculo_completo: bool

    componente_beneficio_definido: (
        ResumenComponenteBeneficioDefinidoMixto | None
    )
    componente_ahorro_personal: (
        ResumenComponenteAhorroPersonalMixto | None
    )

    pension_mensual_total_estimada: float | None
    pago_unico_bd_estimado: float | None = None
    pago_unico_cap_estimado: float | None = None
    pago_unico_total_estimado: float | None = None

    advertencias: list[str]
    fuente_normativa: str

class DatosResultadoMixto(BaseModel):
    """Datos consolidados de los Pasos 1–5 para el Subsistema Mixto.

    El asistente aporta el historial, la trayectoria salarial y el escenario
    de retiro. Los datos específicos del CAP se mantienen explícitos porque
    no pueden reconstruirse de forma fiable a partir del historial anual.
    """

    fecha_nacimiento: date
    sexo: str = Field(min_length=1)

    historial: DatosHistorialSalarial
    linea_tiempo: ResumenLineaTiempo
    resumen_retiro: ResumenRetiro

    fecha_retiro_seleccionada: date
    escenario_salarial_nombre: str = Field(min_length=1)

    saldo_ahorro_personal: float | None = Field(
        default=None,
        ge=0,
    )
    bono_reconocimiento: float = Field(
        default=0.0,
        ge=0,
    )
    bono_reconocimiento_confirmado_oficialmente: bool = False
    valor_actuarial_expectativa_vida: float | None = Field(
        default=None,
        gt=0,
    )
    opcion_prestacion_cap: OpcionPrestacionCAP = "AUTO"


class ResumenResultadoMixto(BaseModel):
    """Resultado Mixto integrado con el escenario elegido en el asistente."""

    escenario_retiro: EscenarioRetiro
    escenario_salarial_nombre: str

    anios_proyectados_incluidos: list[int]
    advertencias_integracion: list[str]

    trazabilidad: ResumenTrazabilidadCalculo | None = None
    resumen_unificado: ResumenPrestacionUnificada | None = None
    calculo: ResumenCalculoMixto



# ============================================================
# Sistema Único de Capitalización con Garantía Solidaria
# ============================================================


class DatosCalculoSUCGS(BaseModel):
    """Datos para calcular la pensión de vejez del SUCGS hasta el art. 197.

    El saldo de Capitalización Solidaria continúa recibiéndose explícitamente
    porque su reconstrucción exige información mensual, aportes pre y
    posreforma y rendimientos efectivos del Fondo Único Solidario.

    Para evaluar la garantía de reemplazo mínimo del artículo 197 se requiere
    un historial laboral anual completo. Las condiciones de cuotas y su
    distribución se preevalúan con ese historial. La estabilidad salarial se
    mantiene como confirmación explícita porque el numeral 3 del artículo 197
    contiene una redacción que requiere validación operativa de la CSS y la
    propia Ley asigna a la Institución los mecanismos de control.
    """

    fecha_nacimiento: date
    sexo: str = Field(min_length=1)
    fecha_retiro: date
    cuotas_totales: int = Field(ge=0)

    saldo_capitalizacion_solidaria: float = Field(
        ge=0,
        description=(
            "Saldo acumulado y capitalizado del Componente Contributivo de "
            "Capitalización Solidaria a la fecha de retiro evaluada."
        ),
    )
    saldo_confirmado_oficialmente: bool = Field(
        default=False,
        description=(
            "Indica si el saldo proviene de una fuente oficial o validada "
            "para el Asegurado(a)."
        ),
    )

    valor_minimo_universal_vigente: float | None = Field(
        default=None,
        gt=0,
        description=(
            "Valor mínimo universal vigente. Si se omite, se usa la "
            "referencia legal B/.144.00 versionada en normativa/sucgs.json."
        ),
    )
    pension_garantizada_solidaria_vigente: float | None = Field(
        default=None,
        gt=0,
        description=(
            "Monto vigente de la Pensión Garantizada Solidaria. Si se omite, "
            "se usa la referencia legal mínima B/.265.00 versionada."
        ),
    )
    valores_solidarios_confirmados_oficialmente: bool = Field(
        default=False,
        description=(
            "Indica si los valores vigentes del mínimo universal y de la "
            "Pensión Garantizada Solidaria fueron confirmados oficialmente."
        ),
    )

    anio_inicio_vida_laboral: int | None = Field(
        default=None,
        ge=1900,
        le=2200,
        description=(
            "Primer año de la vida laboral usado para distribuir las cuotas "
            "del artículo 197."
        ),
    )
    registros_historial_laboral: list[RegistroHistorialSalarial] = Field(
        default_factory=list,
        description=(
            "Historial anual completo hasta el retiro para preevaluar las "
            "condiciones 1 y 2 del artículo 197 y obtener el salario base."
        ),
    )
    historial_laboral_completo: bool = Field(
        default=False,
        description=(
            "Confirma que el rango anual suministrado representa toda la "
            "vida laboral relevante hasta la fecha de retiro."
        ),
    )
    estabilidad_salarial_art197_confirmada: bool | None = Field(
        default=None,
        description=(
            "Confirmación de cumplimiento de la condición de estabilidad "
            "salarial del numeral 3 del artículo 197. None significa que la "
            "condición todavía no fue confirmada."
        ),
    )


class ResumenCalculoSUCGS(BaseModel):
    """Resultado explicable de la pensión de vejez del SUCGS."""

    sistema: str
    nombre_sistema: str
    tipo_calculo: str

    edad_retiro_anios: int
    edad_referencia: int
    fecha_referencia: date
    cumple_edad_referencia: bool
    cuotas_totales: int

    saldo_capitalizacion_solidaria: float
    saldo_confirmado_oficialmente: bool
    divisor_formula: int
    factor_pensionamiento_actuarial: float | None

    calculo_contributivo_disponible: bool
    pension_contributiva_mensual: float | None

    garantia_solidaria_evaluada: bool
    edad_referencia_componente_solidario: int
    valor_minimo_universal_utilizado: float
    pension_garantizada_solidaria_utilizada: float
    valores_solidarios_confirmados_oficialmente: bool
    tipo_prestacion_solidaria: str | None
    complemento_solidario_mensual: float | None
    pension_despues_componente_solidario: float | None

    # Artículo 197: trazabilidad de la garantía de reemplazo mínimo.
    garantia_reemplazo_evaluada: bool
    garantia_reemplazo_aplica: bool | None
    historial_laboral_completo: bool
    historial_rango_anual_completo: bool
    historial_cuotas_sumadas: int | None
    historial_cuotas_coinciden: bool | None

    condicion_minimo_cuotas_anuales_evaluada: bool
    condicion_minimo_cuotas_anuales_cumple: bool | None
    anios_sin_cotizacion_total: int | None
    max_anios_sin_cotizacion_consecutivos: int | None
    anios_con_1_a_4_cuotas: list[int]

    condicion_distribucion_cuotas_evaluada: bool
    condicion_distribucion_cuotas_cumple: bool | None
    cuotas_objetivo_distribucion: int | None
    cuotas_minimas_por_tramo: int | None
    cuotas_primeros_20_anios: int | None
    cuotas_anios_restantes: int | None

    condicion_estabilidad_salarial_evaluada: bool
    condicion_estabilidad_salarial_cumple: bool | None

    salario_promedio_base_mensual: float | None
    tasa_reemplazo_minima_pct_aplicable: float | None
    garantia_reemplazo_monto_objetivo: float | None
    garantia_reemplazo_complemento_mensual: float | None

    calculo_total_disponible: bool
    pension_mensual_total_estimada: float | None

    advertencias: list[str]
    fuente_normativa: str


class DatosResultadoSUCGS(BaseModel):
    """Datos consolidados del asistente para el cálculo SUCGS.

    El historial y la trayectoria salarial provienen de los Pasos 3 y 4.
    El saldo solidario y las confirmaciones que no pueden deducirse de esos
    pasos se mantienen como datos explícitos del Paso 6.
    """

    fecha_nacimiento: date
    sexo: str = Field(min_length=1)

    historial: DatosHistorialSalarial
    linea_tiempo: ResumenLineaTiempo
    resumen_retiro: ResumenRetiro

    fecha_retiro_seleccionada: date
    escenario_salarial_nombre: str = Field(min_length=1)

    saldo_capitalizacion_solidaria: float = Field(ge=0)
    saldo_confirmado_oficialmente: bool = False

    valor_minimo_universal_vigente: float | None = Field(
        default=None,
        gt=0,
    )
    pension_garantizada_solidaria_vigente: float | None = Field(
        default=None,
        gt=0,
    )
    valores_solidarios_confirmados_oficialmente: bool = False

    historial_laboral_completo_confirmado: bool = False
    estabilidad_salarial_art197_confirmada: bool | None = None


class ResumenResultadoSUCGS(BaseModel):
    """Resultado SUCGS asociado al escenario de retiro seleccionado."""

    escenario_retiro: EscenarioRetiro
    escenario_salarial_nombre: str
    anios_proyectados_incluidos: list[int]
    advertencias_integracion: list[str]
    trazabilidad: ResumenTrazabilidadCalculo | None = None
    resumen_unificado: ResumenPrestacionUnificada | None = None
    calculo: ResumenCalculoSUCGS
