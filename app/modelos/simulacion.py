"""Modelos de datos utilizados durante una simulación previsional.

Los modelos Pydantic de este módulo definen la estructura y las
validaciones básicas de los datos intercambiados entre la interfaz,
los endpoints de FastAPI y los servicios de cálculo.
"""

from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, field_validator

from app.core.dinero import (
    tiene_maximo_dos_decimales,
)


def _validar_precision_dos_decimales(
    valor: float | None,
) -> float | None:
    """Valida que un dato editable no exceda dos decimales."""

    if valor is None:
        return valor

    if not tiene_maximo_dos_decimales(valor):
        raise ValueError(
            "El valor admite como máximo dos decimales."
        )

    return valor


# ============================================================
# Cuotas
# ============================================================

class DatosCuotas(BaseModel):
    """Datos de cuotas proporcionados por el Asegurado(a)."""

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

    _validar_salario_cotizado = field_validator(
        "salario_cotizado",
    )(
        _validar_precision_dos_decimales
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
# Detalle salarial del año actual
# ============================================================

ModoDetalleAnioActual = Literal[
    "MENSUAL",
    "QUINCENAL",
]

EstadoPeriodoSalarial = Literal[
    "SIN_INFORMACION",
    "PARCIAL",
    "COMPLETO",
]


class RegistroDetalleAnioActual(BaseModel):
    """Información salarial disponible para un mes del año actual.

    Un mes puede disponer de salario aun cuando su cuota todavía no
    aparezca acreditada. En modo quincenal, el total se deriva de las
    dos quincenas y permite representar un mes parcialmente reportado.
    """

    mes: int = Field(ge=1, le=12)
    cuota_acreditada: bool = False

    estado: EstadoPeriodoSalarial = "SIN_INFORMACION"

    salario_mensual: float | None = Field(default=None, ge=0)
    primera_quincena: float | None = Field(default=None, ge=0)
    segunda_quincena: float | None = Field(default=None, ge=0)

    _validar_salario_mensual = field_validator(
        "salario_mensual",
    )(
        _validar_precision_dos_decimales
    )

    _validar_primera_quincena = field_validator(
        "primera_quincena",
    )(
        _validar_precision_dos_decimales
    )

    _validar_segunda_quincena = field_validator(
        "segunda_quincena",
    )(
        _validar_precision_dos_decimales
    )


class RegistroDetalleAnioActualNormalizado(BaseModel):
    """Mes normalizado después de aplicar las reglas de captura."""

    mes: int
    cuota_acreditada: bool
    estado: EstadoPeriodoSalarial
    salario_total: float
    primera_quincena: float | None = None
    segunda_quincena: float | None = None


class DatosDetalleAnioActual(BaseModel):
    """Detalle mensual o quincenal disponible para el año actual."""

    anio: int = Field(ge=1900, le=2200)
    modo_captura: ModoDetalleAnioActual
    cuotas_anio_actual_referencia: int = Field(ge=0, le=12)
    registros: list[RegistroDetalleAnioActual]


class ResumenDetalleAnioActual(BaseModel):
    """Resumen del detalle salarial real disponible en el año actual."""

    anio: int
    modo_captura: ModoDetalleAnioActual

    cuotas_acreditadas_identificadas: int
    cuotas_coinciden: bool

    ultimo_mes_cuota_acreditada: str | None
    ultimo_mes_con_salario_completo: str | None

    total_salario_disponible: float
    total_salario_acreditado: float

    meses_con_informacion: int
    meses_completos: int

    salario_ultimo_mes_completo: float | None
    promedio_meses_completos: float | None
    promedio_ultimos_3_meses_completos: float | None
    promedio_por_cuota_acreditada: float | None

    registros: list[RegistroDetalleAnioActualNormalizado]


# ============================================================
# Referencia importada de Mi Retiro Seguro
# ============================================================

SistemaReferenciaMiRetiroSeguro = Literal[
    "SEBD",
    "MIXTO",
    "SUCGS",
    "NO_IDENTIFICADO",
]

NaturalezaReferenciaMiRetiroSeguro = Literal[
    "PENSION_MENSUAL",
    "PAGO_UNICO",
    "NO_IDENTIFICADA",
]

TipoRegistroReferenciaMiRetiroSeguro = Literal[
    "HISTORICO",
    "HISTORICO_PROYECTADO",
    "PROYECTADO",
]


class RegistroReferenciaMiRetiroSeguro(BaseModel):
    """Fila anual extraída del comprobante sin datos identificativos."""

    anio: int = Field(ge=1900, le=2200)
    edad: int = Field(ge=0, le=150)
    tipo: TipoRegistroReferenciaMiRetiroSeguro
    salario_anual: float = Field(ge=0)
    cuotas: int = Field(ge=0, le=12)


class ResumenReferenciaMiRetiroSeguro(BaseModel):
    """Datos operativos extraídos de un comprobante personal en PDF.

    El contrato excluye deliberadamente nombre, cédula y número de seguro
    social. La referencia se usa para comparar fotografías personales, no
    para sustituir los motores legales de la aplicación.
    """

    fecha_comprobante: date | None = None
    fecha_decision_texto: str | None = None
    fecha_nacimiento: date | None = None
    sexo: str | None = None
    fecha_ingreso_css: date | None = None

    sistema_elegido: SistemaReferenciaMiRetiroSeguro
    sistema_elegido_nombre: str

    edad_retiro_elegida: int | None = Field(default=None, ge=0, le=150)
    cuotas_historicas: int | None = Field(default=None, ge=0)

    prestacion_esperada: str | None = None
    naturaleza_prestacion: NaturalezaReferenciaMiRetiroSeguro
    monto_estimado_prestacion: float = Field(gt=0)

    total_cuotas_acumuladas: int | None = Field(default=None, ge=0)
    registros: list[RegistroReferenciaMiRetiroSeguro] = Field(default_factory=list)
    advertencias: list[str] = Field(default_factory=list)



# ============================================================
# Ficha Digital — salarios del último año
# ============================================================

EstadoRegistroFichaDigital = Literal[
    "COMPLETO",
    "PARCIAL",
    "SIN_INFORMACION",
]


class RegistroFichaDigital(BaseModel):
    """Salario mensual detectado en la Ficha Digital.

    El importador no presume si la cuota del mes ya está acreditada.
    Esa decisión se confirma en la vista previa antes de aplicar datos.
    """

    anio: int = Field(ge=1900, le=2200)
    mes: int = Field(ge=1, le=12)
    salario: float = Field(ge=0)
    estado: EstadoRegistroFichaDigital = "COMPLETO"

    _validar_salario = field_validator("salario")(
        _validar_precision_dos_decimales
    )


class ResumenFichaDigital(BaseModel):
    """Datos salariales no identificativos extraídos de la Ficha Digital."""

    registros: list[RegistroFichaDigital]
    anio_mas_reciente: int | None = None
    mes_mas_reciente: int | None = Field(default=None, ge=1, le=12)
    advertencias: list[str] = Field(default_factory=list)


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
            "Monto salarial actual indicado por el Asegurado(a)."
        ),
    )

    _validar_monto = field_validator(
        "monto",
    )(
        _validar_precision_dos_decimales
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

    _validar_salario_mensual_actual = field_validator(
        "salario_mensual_actual",
    )(
        _validar_precision_dos_decimales
    )

    _validar_porcentaje_anual = field_validator(
        "porcentaje_anual",
    )(
        _validar_precision_dos_decimales
    )

    _validar_salario_mensual_futuro = field_validator(
        "salario_mensual_futuro",
    )(
        _validar_precision_dos_decimales
    )

    @field_validator("escenarios_porcentajes")
    @classmethod
    def validar_precision_escenarios(
        cls,
        valores: list[float],
    ) -> list[float]:
        """Limita cada porcentaje editable a dos decimales."""

        for valor in valores:
            _validar_precision_dos_decimales(
                valor
            )

        return valores


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
    "SIN_COTIZACION",
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

# ============================================================
# Retiro
# ============================================================

TipoEscenarioRetiro = Literal[
    "ANTICIPADO",
    "REFERENCIA",
    "ADICIONAL",
    "PERSONALIZADO",
]


class DatosRetiro(BaseModel):
    """Datos utilizados para construir escenarios de retiro.

    Las fechas se calculan con precisión de día. Las cuotas futuras
    de esta primera versión siguen siendo estimaciones basadas en
    una densidad anual, porque todavía no disponemos necesariamente
    del detalle mensual de cotizaciones.
    """

    fecha_nacimiento: date

    sexo: str = Field(
        min_length=1,
    )

    fecha_corte: date | None = Field(
        default=None,
        description=(
            "Fecha en la que se evalúa la situación previsional. "
            "Si se omite, se utiliza la fecha actual del servidor."
        ),
    )

    # Las cuotas reales pueden provenir de un reporte cuyo último mes
    # acreditado sea anterior al momento en que se realiza la simulación.
    # UX.3 permite expresar ese dato como YYYY-MM y conserva la fecha
    # exacta de corte para compatibilidad y trazabilidad interna.
    ultimo_mes_cuotas: str | None = Field(
        default=None,
        pattern=r"^\d{4}-(0[1-9]|1[0-2])$",
        description=(
            "Último mes con cuotas reales acreditadas, en formato YYYY-MM. "
            "Cuando se proporciona, el servicio deriva la fecha de corte "
            "al último día de ese mes, limitada por la fecha de evaluación."
        ),
    )

    fecha_corte_cuotas: date | None = Field(
        default=None,
        description=(
            "Fecha exacta hasta la cual se consideran acreditadas "
            "las cuotas reales. Se conserva para compatibilidad; cuando "
            "se informa ultimo_mes_cuotas ambos valores deben ser coherentes."
        ),
    )

    cuotas_reales: int = Field(
        ge=0,
    )

    cuotas_anio_actual: int = Field(
        ge=0,
        le=12,
        description=(
            "Cuotas del año de evaluación ya incluidas "
            "dentro del total real."
        ),
    )

    cuotas_esperadas_cierre_anio: int = Field(
        ge=0,
        le=12,
        description=(
            "Total de cuotas esperado al cierre del año "
            "de evaluación."
        ),
    )

    continua_cotizando: bool

    cuotas_esperadas_por_anio: int = Field(
        ge=0,
        le=12,
    )

    anio_fin_proyeccion_salarial: int | None = Field(
        default=None,
        ge=1900,
        le=2200,
        description=(
            "Último año cubierto por la proyección salarial "
            "del Paso 4."
        ),
    )

    anios_adicionales: list[int] = Field(
        default_factory=lambda: [
            -2,
            -1,
            0,
            1,
            2,
            3,
            5,
        ],
    )

    fecha_retiro_personalizada: date | None = None


class EscenarioRetiro(BaseModel):
    """Posible momento de retiro utilizado para comparación."""

    tipo: TipoEscenarioRetiro
    nombre: str

    fecha_retiro: date
    edad_retiro_anios: int

    meses_desde_corte_cuotas: int

    cuotas_estimadas_adicionales: int
    cuotas_estimadas_totales: int

    fecha_ya_transcurrida: bool


class ResumenRetiro(BaseModel):
    """Resultado preliminar del análisis de fechas de retiro."""

    fecha_corte: date
    fecha_corte_cuotas: date

    edad_actual_anios: int
    edad_referencia: int
    fecha_referencia: date

    alcanzo_edad_referencia: bool
    dias_hasta_referencia: int

    escenarios: list[
        EscenarioRetiro
    ]

    anio_fin_proyeccion_salarial: int | None
    proyeccion_salarial_cubre_escenarios: bool
    advertencias: list[str]

    metodo_estimacion_cuotas: str
