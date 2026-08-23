"""Construcción de la línea temporal histórica y proyectada.

Este servicio integra los datos ya acreditados por la CSS con
los escenarios salariales futuros, manteniendo una separación
explícita entre valores históricos y estimaciones.

La línea temporal se utiliza para presentación y planificación.
Todavía no constituye un cálculo de pensión.
"""

from decimal import Decimal

from app.core.dinero import (
    a_decimal,
    redondear_moneda,
)
from app.models.simulacion import (
    DatosLineaTiempo,
    EscenarioLineaTiempo,
    RegistroLineaTiempo,
    ResumenLineaTiempo,
)
from app.services.historial_salarios import (
    analizar_historial_salarial,
)
from app.services.proyeccion_cuotas import (
    analizar_cuotas,
)
from app.services.proyeccion_salarios import (
    normalizar_salario,
    proyectar_salario,
)


# ============================================================
# Construcción principal
# ============================================================

def construir_linea_tiempo(
    datos: DatosLineaTiempo,
) -> ResumenLineaTiempo:
    """Une historial, año actual parcial y proyección futura.

    El año actual puede contener simultáneamente una porción
    histórica y otra proyectada. Los años posteriores son
    completamente proyectados.
    """

    resumen_historial = (
        analizar_historial_salarial(
            datos.historial,
        )
    )

    resumen_cuotas = analizar_cuotas(
        datos.cuotas,
    )

    resumen_salario = normalizar_salario(
        datos.salario_actual,
    )

    resumen_proyeccion = proyectar_salario(
        datos.proyeccion,
    )

    anio_actual = (
        datos.historial.anio_fin
    )


    # --------------------------------------------------------
    # Validaciones de coherencia entre etapas
    # --------------------------------------------------------

    if (
        datos.proyeccion.anio_inicio
        != anio_actual
    ):
        raise ValueError(
            "El año inicial de la proyección debe coincidir "
            "con el año final del historial."
        )

    if (
        datos.proyeccion.salario_mensual_actual
        != resumen_salario.salario_mensual
    ):
        raise ValueError(
            "El salario base de la proyección no coincide "
            "con el salario actual normalizado."
        )


    # --------------------------------------------------------
    # Indexar registros históricos
    # --------------------------------------------------------

    historial_por_anio = {
        registro.anio: registro
        for registro
        in resumen_historial.registros
    }

    if not resumen_historial.historial_completo:
        raise ValueError(
            "El historial debe cubrir todos los años declarados "
            "antes de construir la línea temporal."
        )

    if (
        resumen_historial.cuotas_totales_referencia
        != datos.cuotas.cuotas_totales
    ):
        raise ValueError(
            "El total de cuotas de referencia del historial no coincide "
            "con el total acreditado del Paso 2."
        )

    if not resumen_historial.cuotas_coinciden:
        raise ValueError(
            "La suma de cuotas del historial debe coincidir con "
            "el total acreditado del Paso 2."
        )

    registro_actual_validacion = historial_por_anio.get(
        anio_actual
    )
    if registro_actual_validacion is None:
        raise ValueError(
            "El historial debe incluir el año actual antes de "
            "construir la línea temporal."
        )

    if (
        registro_actual_validacion.cuotas
        != datos.cuotas.cuotas_anio_actual
    ):
        raise ValueError(
            "Las cuotas del año actual del historial no coinciden "
            "con las cuotas acreditadas del año actual del Paso 2."
        )


    # --------------------------------------------------------
    # Cuotas pendientes del año actual
    # --------------------------------------------------------

    cuotas_restantes_actual = (
        resumen_cuotas
        .cuotas_proyectadas_restantes_anio
    )

    # Una cuota futura se aproxima a un mes adicional cotizado
    # al salario mensual actual. Esta aproximación se mantendrá
    # identificada como proyección en la interfaz.
    salario_restante_actual = redondear_moneda(
        a_decimal(
            resumen_salario.salario_mensual
        )
        * cuotas_restantes_actual
    )


    # --------------------------------------------------------
    # Crear una línea temporal por escenario
    # --------------------------------------------------------

    escenarios_resultado: list[
        EscenarioLineaTiempo
    ] = []

    for escenario in (
        resumen_proyeccion.escenarios
    ):
        registros_linea: list[
            RegistroLineaTiempo
        ] = []

        proyeccion_por_anio = {
            registro.anio: registro
            for registro
            in escenario.registros
        }


        # ----------------------------------------------------
        # Años históricos anteriores al actual
        # ----------------------------------------------------

        for anio in range(
            datos.historial.anio_inicio,
            anio_actual,
        ):
            registro_historico = (
                historial_por_anio.get(
                    anio,
                )
            )

            if registro_historico is None:
                registros_linea.append(
                    RegistroLineaTiempo(
                        anio=anio,
                        cuotas_historicas=0,
                        salario_historico=0.0,
                        cuotas_proyectadas=0,
                        salario_proyectado=0.0,
                        cuotas_cierre=0,
                        salario_cierre=0.0,
                        estado="PENDIENTE",
                    )
                )

                continue

            if registro_historico.cuotas == 0:
                estado = "SIN_COTIZACION"

            elif registro_historico.cuotas == 12:
                estado = "HISTORICO"

            else:
                estado = "HISTORICO_PARCIAL"

            registros_linea.append(
                RegistroLineaTiempo(
                    anio=anio,
                    cuotas_historicas=(
                        registro_historico.cuotas
                    ),
                    salario_historico=(
                        registro_historico
                        .salario_cotizado
                    ),
                    cuotas_proyectadas=0,
                    salario_proyectado=0.0,
                    cuotas_cierre=(
                        registro_historico.cuotas
                    ),
                    salario_cierre=(
                        registro_historico
                        .salario_cotizado
                    ),
                    estado=estado,
                )
            )


        # ----------------------------------------------------
        # Año actual: real + proyectado
        # ----------------------------------------------------

        registro_actual = (
            historial_por_anio.get(
                anio_actual,
            )
        )

        cuotas_historicas_actual = (
            registro_actual.cuotas
            if registro_actual
            else datos.cuotas.cuotas_anio_actual
        )

        salario_historico_actual = (
            registro_actual.salario_cotizado
            if registro_actual
            else 0.0
        )

        salario_cierre_actual = redondear_moneda(
            a_decimal(
                salario_historico_actual
            )
            + a_decimal(
                salario_restante_actual
            )
        )

        if cuotas_restantes_actual > 0:
            estado_actual = "MIXTO"

        elif cuotas_historicas_actual == 0:
            estado_actual = "SIN_COTIZACION"

        elif cuotas_historicas_actual >= 12:
            estado_actual = "HISTORICO"

        else:
            estado_actual = (
                "HISTORICO_PARCIAL"
            )

        registros_linea.append(
            RegistroLineaTiempo(
                anio=anio_actual,
                cuotas_historicas=(
                    cuotas_historicas_actual
                ),
                salario_historico=(
                    salario_historico_actual
                ),
                cuotas_proyectadas=(
                    cuotas_restantes_actual
                ),
                salario_proyectado=(
                    salario_restante_actual
                ),
                salario_mensual_proyectado=(
                    resumen_salario.salario_mensual
                    if cuotas_restantes_actual > 0
                    else None
                ),
                cuotas_cierre=(
                    cuotas_historicas_actual
                    + cuotas_restantes_actual
                ),
                salario_cierre=(
                    salario_cierre_actual
                ),
                estado=estado_actual,
            )
        )


        # ----------------------------------------------------
        # Años completamente proyectados
        # ----------------------------------------------------

        for anio in range(
            anio_actual + 1,
            datos.proyeccion.anio_fin + 1,
        ):
            registro_proyectado = (
                proyeccion_por_anio.get(
                    anio,
                )
            )

            if registro_proyectado is None:
                continue

            cuotas_proyectadas = (
                datos.cuotas
                .cuotas_esperadas_por_anio
                if datos.cuotas
                .continua_cotizando
                else 0
            )

            # El salario cotizado proyectado debe respetar la
            # cantidad de cuotas esperada. Si se proyectan menos
            # de doce cuotas, no se utiliza el salario anual completo.
            salario_proyectado = (
                redondear_moneda(
                    a_decimal(
                        registro_proyectado.salario_anual
                    )
                    * Decimal(
                        cuotas_proyectadas
                    )
                    / Decimal("12")
                )
                if cuotas_proyectadas > 0
                else 0.0
            )

            registros_linea.append(
                RegistroLineaTiempo(
                    anio=anio,
                    cuotas_historicas=0,
                    salario_historico=0.0,
                    cuotas_proyectadas=(
                        cuotas_proyectadas
                    ),
                    salario_proyectado=(
                        salario_proyectado
                    ),
                    salario_mensual_proyectado=(
                        registro_proyectado.salario_mensual
                    ),
                    cuotas_cierre=(
                        cuotas_proyectadas
                    ),
                    salario_cierre=(
                        salario_proyectado
                    ),
                    estado=(
                        "PROYECTADO"
                        if cuotas_proyectadas > 0
                        else "PROYECTADO_SIN_COTIZACION"
                    ),
                )
            )


        escenarios_resultado.append(
            EscenarioLineaTiempo(
                nombre=escenario.nombre,
                tasa_anual_pct=(
                    escenario.tasa_anual_pct
                ),
                registros=registros_linea,
            )
        )


    return ResumenLineaTiempo(
        anio_inicio_historico=(
            datos.historial.anio_inicio
        ),
        anio_actual=anio_actual,
        anio_fin_proyeccion=(
            datos.proyeccion.anio_fin
        ),
        escenarios=escenarios_resultado,
    )
