"""Servicios para normalizar y proyectar salarios.

Este módulo permite convertir un salario entre distintas
periodicidades y construir escenarios salariales año por año.

Las proyecciones generadas aquí todavía no representan una
pensión. Su objetivo es producir la información salarial que
posteriormente utilizarán los motores previsionales.
"""

from decimal import Decimal

from app.core.dinero import (
    a_decimal,
    redondear_moneda,
)
from app.modelos.simulacion import (
    DatosProyeccionSalario,
    DatosSalario,
    EscenarioProyeccionSalario,
    ProyeccionSalarioAnual,
    ResumenProyeccionSalario,
    ResumenSalario,
)


# ============================================================
# Normalización salarial
# ============================================================

def normalizar_salario(
    datos: DatosSalario,
) -> ResumenSalario:
    """Convierte un salario a todas las periodicidades soportadas.

    Las operaciones monetarias se realizan con ``Decimal`` y no se
    redondean durante conversiones intermedias. Cada equivalencia se
    redondea únicamente al materializar el resultado visible.
    """

    monto = a_decimal(
        datos.monto
    )

    if datos.periodicidad == "SEMANAL":
        salario_anual = (
            monto
            * Decimal("52")
        )

    elif datos.periodicidad == "QUINCENAL":
        salario_anual = (
            monto
            * Decimal("24")
        )

    elif datos.periodicidad == "MENSUAL":
        salario_anual = (
            monto
            * Decimal("12")
        )

    elif datos.periodicidad == "ANUAL":
        salario_anual = monto

    else:
        raise ValueError(
            "La periodicidad salarial indicada no es válida."
        )

    salario_mensual = (
        salario_anual
        / Decimal("12")
    )
    salario_quincenal = (
        salario_anual
        / Decimal("24")
    )
    salario_semanal = (
        salario_anual
        / Decimal("52")
    )

    return ResumenSalario(
        monto_original=redondear_moneda(
            monto
        ),
        periodicidad_original=datos.periodicidad,
        salario_semanal=redondear_moneda(
            salario_semanal
        ),
        salario_quincenal=redondear_moneda(
            salario_quincenal
        ),
        salario_mensual=redondear_moneda(
            salario_mensual
        ),
        salario_anual=redondear_moneda(
            salario_anual
        ),
    )

# ============================================================
# Funciones auxiliares de proyección
# ============================================================

def _validar_rango_anios(
    anio_inicio: int,
    anio_fin: int,
) -> None:
    """Valida que el período de proyección tenga sentido."""

    if anio_fin < anio_inicio:
        raise ValueError(
            "El año final de la proyección no puede ser "
            "anterior al año inicial."
        )


def _crear_registro_anual(
    anio: int,
    salario_mensual: Decimal,
    salario_base: Decimal,
) -> ProyeccionSalarioAnual:
    """Construye un registro anual sin redondeo intermedio.

    El salario mensual y el anual se redondean de forma independiente
    desde el valor preciso del escenario. Por ello, una cifra mensual
    visible multiplicada por doce puede diferir por un centavo del
    resultado anual cuando existan fracciones de centavo internas.
    """

    salario_anual_preciso = (
        salario_mensual
        * Decimal("12")
    )

    crecimiento_desde_base = (
        (
            salario_mensual
            / salario_base
        )
        - Decimal("1")
    ) * Decimal("100")

    return ProyeccionSalarioAnual(
        anio=anio,
        salario_mensual=redondear_moneda(
            salario_mensual
        ),
        salario_anual=redondear_moneda(
            salario_anual_preciso
        ),
        crecimiento_desde_base_pct=round(
            float(
                crecimiento_desde_base
            ),
            4,
        ),
    )

def _proyectar_por_porcentaje(
    salario_base: float,
    anio_inicio: int,
    anio_fin: int,
    porcentaje_anual: float | Decimal,
) -> list[ProyeccionSalarioAnual]:
    """Genera una serie salarial mediante crecimiento compuesto.

    La potencia se calcula con ``Decimal`` y se conserva toda la
    precisión interna hasta crear cada registro monetario.
    """

    registros: list[
        ProyeccionSalarioAnual
    ] = []

    salario_base_decimal = a_decimal(
        salario_base
    )

    factor_anual = (
        Decimal("1")
        + (
            a_decimal(
                porcentaje_anual
            )
            / Decimal("100")
        )
    )

    for anio in range(
        anio_inicio,
        anio_fin + 1,
    ):
        cantidad_anios = (
            anio - anio_inicio
        )

        salario_mensual = (
            salario_base_decimal
            * (
                factor_anual
                ** cantidad_anios
            )
        )

        registros.append(
            _crear_registro_anual(
                anio=anio,
                salario_mensual=salario_mensual,
                salario_base=salario_base_decimal,
            )
        )

    return registros

def _calcular_tasa_hasta_salario_futuro(
    salario_actual: float,
    salario_futuro: float,
    cantidad_anios: int,
) -> Decimal:
    """Calcula con ``Decimal`` la tasa anual compuesta equivalente.

    La modalidad conecta exactamente dos datos aportados por el
    Asegurado(a): el salario mensual base y un salario mensual futuro.
    La tasa equivalente se conserva con precisión decimal para que la
    trayectoria intermedia no introduzca artefactos binarios de ``float``.
    """

    if cantidad_anios <= 0:
        raise ValueError(
            "El salario futuro debe corresponder "
            "a un año posterior al año inicial."
        )

    salario_actual_decimal = a_decimal(
        salario_actual
    )
    salario_futuro_decimal = a_decimal(
        salario_futuro
    )

    factor_objetivo = (
        salario_futuro_decimal
        / salario_actual_decimal
    )
    exponente_anual = (
        Decimal("1")
        / Decimal(cantidad_anios)
    )
    factor_anual = (
        factor_objetivo
        ** exponente_anual
    )

    return (
        factor_anual - Decimal("1")
    ) * Decimal("100")


def _validar_porcentaje(
    porcentaje: float | Decimal,
) -> None:
    """Evita porcentajes que produzcan salarios nulos o negativos."""

    if porcentaje <= -100:
        raise ValueError(
            "Un porcentaje anual debe ser mayor que -100 %."
        )

    if porcentaje > 100:
        raise ValueError(
            "Un porcentaje anual no puede superar 100 % "
            "en esta versión de la simulación."
        )


# ============================================================
# Motor de proyección salarial
# ============================================================

def proyectar_salario(
    datos: DatosProyeccionSalario,
) -> ResumenProyeccionSalario:
    """Construye uno o varios escenarios salariales año por año."""

    _validar_rango_anios(
        datos.anio_inicio,
        datos.anio_fin,
    )

    escenarios: list[EscenarioProyeccionSalario] = []


    # --------------------------------------------------------
    # Modalidad: salario constante
    # --------------------------------------------------------

    if datos.modalidad == "CONSTANTE":
        registros = _proyectar_por_porcentaje(
            salario_base=datos.salario_mensual_actual,
            anio_inicio=datos.anio_inicio,
            anio_fin=datos.anio_fin,
            porcentaje_anual=0.0,
        )

        escenarios.append(
            EscenarioProyeccionSalario(
                nombre="Salario constante",
                tasa_anual_pct=0.0,
                registros=registros,
            )
        )


    # --------------------------------------------------------
    # Modalidad: porcentaje anual indicado
    # --------------------------------------------------------

    elif datos.modalidad == "PORCENTAJE":
        if datos.porcentaje_anual is None:
            raise ValueError(
                "Debes indicar el porcentaje anual "
                "para esta modalidad."
            )

        _validar_porcentaje(
            datos.porcentaje_anual,
        )

        registros = _proyectar_por_porcentaje(
            salario_base=datos.salario_mensual_actual,
            anio_inicio=datos.anio_inicio,
            anio_fin=datos.anio_fin,
            porcentaje_anual=datos.porcentaje_anual,
        )

        escenarios.append(
            EscenarioProyeccionSalario(
                nombre=(
                    f"Crecimiento anual de "
                    f"{datos.porcentaje_anual:g} %"
                ),
                tasa_anual_pct=round(
                    datos.porcentaje_anual,
                    6,
                ),
                registros=registros,
            )
        )


    # --------------------------------------------------------
    # Modalidad: salario futuro conocido
    # --------------------------------------------------------

    elif datos.modalidad == "FUTURO_CONOCIDO":
        if datos.salario_mensual_futuro is None:
            raise ValueError(
                "Debes indicar el salario mensual futuro."
            )

        if datos.anio_salario_futuro is None:
            raise ValueError(
                "Debes indicar el año del salario futuro."
            )

        if (
            datos.anio_salario_futuro
            <= datos.anio_inicio
        ):
            raise ValueError(
                "El año del salario futuro debe ser "
                "posterior al año inicial."
            )

        if (
            datos.anio_salario_futuro
            > datos.anio_fin
        ):
            raise ValueError(
                "El año del salario futuro debe estar "
                "dentro del período de proyección."
            )

        cantidad_anios = (
            datos.anio_salario_futuro
            - datos.anio_inicio
        )

        tasa_equivalente = (
            _calcular_tasa_hasta_salario_futuro(
                salario_actual=(
                    datos.salario_mensual_actual
                ),
                salario_futuro=(
                    datos.salario_mensual_futuro
                ),
                cantidad_anios=cantidad_anios,
            )
        )

        _validar_porcentaje(
            tasa_equivalente,
        )

        registros = _proyectar_por_porcentaje(
            salario_base=datos.salario_mensual_actual,
            anio_inicio=datos.anio_inicio,
            anio_fin=datos.anio_fin,
            porcentaje_anual=tasa_equivalente,
        )

        escenarios.append(
            EscenarioProyeccionSalario(
                nombre=(
                    "Proyección hasta salario conocido "
                    f"en {datos.anio_salario_futuro}"
                ),
                tasa_anual_pct=round(
                    tasa_equivalente,
                    6,
                ),
                registros=registros,
            )
        )


    # --------------------------------------------------------
    # Modalidad: comparación de varios escenarios
    # --------------------------------------------------------

    elif datos.modalidad == "ESCENARIOS":
        if not datos.escenarios_porcentajes:
            raise ValueError(
                "Debes indicar al menos un escenario "
                "de crecimiento salarial."
            )

        # Elimina valores repetidos y ordena los escenarios
        # para que la salida sea consistente.
        porcentajes = sorted(
            set(
                datos.escenarios_porcentajes
            )
        )

        for porcentaje in porcentajes:
            _validar_porcentaje(
                porcentaje,
            )

            registros = _proyectar_por_porcentaje(
                salario_base=(
                    datos.salario_mensual_actual
                ),
                anio_inicio=datos.anio_inicio,
                anio_fin=datos.anio_fin,
                porcentaje_anual=porcentaje,
            )

            escenarios.append(
                EscenarioProyeccionSalario(
                    nombre=(
                        f"Escenario {porcentaje:g} % anual"
                    ),
                    tasa_anual_pct=round(
                        porcentaje,
                        6,
                    ),
                    registros=registros,
                )
            )


    # --------------------------------------------------------
    # Protección adicional
    # --------------------------------------------------------

    else:
        raise ValueError(
            "La modalidad de proyección salarial "
            "indicada no es válida."
        )


    return ResumenProyeccionSalario(
        modalidad=datos.modalidad,
        anio_inicio=datos.anio_inicio,
        anio_fin=datos.anio_fin,
        escenarios=escenarios,
    )
