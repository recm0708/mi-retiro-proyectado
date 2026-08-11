from app.modelos.simulacion import DatosCuotas, ResumenCuotas


CUOTAS_PENSION_PROPORCIONAL = 180
CUOTAS_REFERENCIA = 240


def _calcular_anios_aproximados(
    cuotas_faltantes: int,
    cuotas_por_anio: int,
) -> float | None:
    if cuotas_faltantes <= 0:
        return 0.0

    if cuotas_por_anio <= 0:
        return None

    return round(
        cuotas_faltantes / cuotas_por_anio,
        2,
    )


def analizar_cuotas(datos: DatosCuotas) -> ResumenCuotas:
    if datos.cuotas_anio_actual > datos.cuotas_totales:
        raise ValueError(
            "Las cuotas del año actual no pueden superar "
            "el total de cuotas acreditadas."
        )

    if datos.continua_cotizando:
        if (
            datos.cuotas_esperadas_cierre_anio
            < datos.cuotas_anio_actual
        ):
            raise ValueError(
                "Las cuotas esperadas al cierre del año "
                "no pueden ser menores que las ya acreditadas."
            )

        cuotas_cierre_anio = (
            datos.cuotas_esperadas_cierre_anio
        )

        cuotas_por_anio_futuras = (
            datos.cuotas_esperadas_por_anio
        )

    else:
        cuotas_cierre_anio = datos.cuotas_anio_actual
        cuotas_por_anio_futuras = 0

    proyectadas_restantes = max(
        0,
        cuotas_cierre_anio
        - datos.cuotas_anio_actual,
    )

    proyectadas_cierre = (
        datos.cuotas_totales
        + proyectadas_restantes
    )

    faltantes_180 = max(
        0,
        CUOTAS_PENSION_PROPORCIONAL
        - proyectadas_cierre,
    )

    faltantes_240 = max(
        0,
        CUOTAS_REFERENCIA
        - proyectadas_cierre,
    )

    anios_180 = _calcular_anios_aproximados(
        faltantes_180,
        cuotas_por_anio_futuras,
    )

    anios_240 = _calcular_anios_aproximados(
        faltantes_240,
        cuotas_por_anio_futuras,
    )

    return ResumenCuotas(
        cuotas_reales=datos.cuotas_totales,
        cuotas_anio_actual=datos.cuotas_anio_actual,
        cuotas_proyectadas_restantes_anio=proyectadas_restantes,
        cuotas_proyectadas_cierre_anio=proyectadas_cierre,
        faltantes_180=faltantes_180,
        faltantes_240=faltantes_240,
        anios_aprox_180=anios_180,
        anios_aprox_240=anios_240,
    )