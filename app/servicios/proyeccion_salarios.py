"""Servicios para normalizar y proyectar salarios.

Este módulo permite convertir un salario entre distintas
periodicidades y construir escenarios salariales año por año.

Las proyecciones generadas aquí todavía no representan una
pensión. Su objetivo es producir la información salarial que
posteriormente utilizarán los motores previsionales.
"""

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

    Primero se obtiene un salario anual equivalente. A partir de
    ese valor común se calculan las demás periodicidades para evitar
    conversiones encadenadas y diferencias innecesarias de redondeo.
    """

    monto = datos.monto

    # Normaliza el dato original a un equivalente anual.
    if datos.periodicidad == "SEMANAL":
        salario_anual = monto * 52

    elif datos.periodicidad == "QUINCENAL":
        salario_anual = monto * 24

    elif datos.periodicidad == "MENSUAL":
        salario_anual = monto * 12

    elif datos.periodicidad == "ANUAL":
        salario_anual = monto

    else:
        # Esta validación normalmente será interceptada primero
        # por Pydantic, pero se conserva como protección del servicio.
        raise ValueError(
            "La periodicidad salarial indicada no es válida."
        )

    # Todas las demás equivalencias se derivan del valor anual.
    salario_mensual = salario_anual / 12
    salario_quincenal = salario_anual / 24
    salario_semanal = salario_anual / 52

    # Los valores mostrados y enviados a la interfaz se expresan
    # con dos decimales monetarios.
    return ResumenSalario(
        monto_original=round(monto, 2),
        periodicidad_original=datos.periodicidad,
        salario_semanal=round(salario_semanal, 2),
        salario_quincenal=round(salario_quincenal, 2),
        salario_mensual=round(salario_mensual, 2),
        salario_anual=round(salario_anual, 2),
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
    salario_mensual: float,
    salario_base: float,
) -> ProyeccionSalarioAnual:
    """Construye un registro salarial anual normalizado.

    El salario mensual se redondea primero a centavos. El salario
    anual se calcula a partir de ese valor visible para garantizar
    que ambas cifras sean consistentes entre sí en la interfaz.
    """

    # Los salarios proyectados se expresan monetariamente
    # con una precisión máxima de dos decimales.
    salario_mensual_redondeado = round(
        salario_mensual,
        2,
    )

    # El salario anual debe coincidir exactamente con el
    # salario mensual mostrado multiplicado por doce meses.
    salario_anual = (
        salario_mensual_redondeado
        * 12
    )

    # El crecimiento acumulado también utiliza el salario
    # mensual ya redondeado que verá el usuario.
    crecimiento_desde_base = (
        (
            salario_mensual_redondeado
            / salario_base
        )
        - 1
    ) * 100

    return ProyeccionSalarioAnual(
        anio=anio,
        salario_mensual=salario_mensual_redondeado,
        salario_anual=round(
            salario_anual,
            2,
        ),
        crecimiento_desde_base_pct=round(
            crecimiento_desde_base,
            4,
        ),
    )


def _proyectar_por_porcentaje(
    salario_base: float,
    anio_inicio: int,
    anio_fin: int,
    porcentaje_anual: float,
) -> list[ProyeccionSalarioAnual]:
    """Genera una serie salarial utilizando crecimiento compuesto."""

    registros: list[ProyeccionSalarioAnual] = []

    # Convierte el porcentaje a un factor multiplicativo.
    factor_anual = 1 + (
        porcentaje_anual / 100
    )

    for anio in range(
        anio_inicio,
        anio_fin + 1,
    ):
        # El año inicial conserva el salario base.
        cantidad_anios = (
            anio - anio_inicio
        )

        salario_mensual = (
            salario_base
            * (factor_anual ** cantidad_anios)
        )

        registros.append(
            _crear_registro_anual(
                anio=anio,
                salario_mensual=salario_mensual,
                salario_base=salario_base,
            )
        )

    return registros


def _calcular_tasa_hasta_salario_futuro(
    salario_actual: float,
    salario_futuro: float,
    cantidad_anios: int,
) -> float:
    """Calcula la tasa anual compuesta necesaria para llegar a un salario.

    Esta modalidad evita inventar aumentos intermedios arbitrarios.
    Se calcula una tasa anual equivalente que conecta el salario
    actual con el salario futuro indicado por el usuario.
    """

    if cantidad_anios <= 0:
        raise ValueError(
            "El salario futuro debe corresponder "
            "a un año posterior al año inicial."
        )

    tasa_decimal = (
        (salario_futuro / salario_actual)
        ** (1 / cantidad_anios)
    ) - 1

    return tasa_decimal * 100


def _validar_porcentaje(
    porcentaje: float,
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