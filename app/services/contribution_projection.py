"""Servicios para analizar las cuotas de una simulación previsional.

Este módulo mantiene separadas las cuotas que ya están acreditadas
de aquellas que solamente forman parte de una proyección futura.
"""

from app.models.simulation import DatosCuotas, ResumenCuotas


# ============================================================
# Umbrales preliminares
# ============================================================

# Estos valores se utilizan actualmente para mostrar al Asegurado(a)
# su distancia respecto de dos referencias de cuotas.
#
# Más adelante los parámetros normativos definitivos serán
# obtenidos desde los archivos versionados de "regulations/".
CUOTAS_PENSION_PROPORCIONAL = 180
CUOTAS_REFERENCIA = 240


# ============================================================
# Funciones auxiliares
# ============================================================

def _calcular_anios_aproximados(
    cuotas_faltantes: int,
    cuotas_por_anio: int,
) -> float | None:
    """Calcula años aproximados para alcanzar una cantidad de cuotas.

    Devuelve:
        0.0:
            Cuando el umbral ya fue alcanzado.

        None:
            Cuando todavía faltan cuotas pero la proyección indica
            que no se aportarán cuotas futuras.

        float:
            Cantidad aproximada de años necesarios.
    """

    if cuotas_faltantes <= 0:
        return 0.0

    if cuotas_por_anio <= 0:
        return None

    return round(
        cuotas_faltantes / cuotas_por_anio,
        2,
    )


# ============================================================
# Análisis principal
# ============================================================

def analizar_cuotas(datos: DatosCuotas) -> ResumenCuotas:
    """Analiza cuotas acreditadas y proyectadas.

    Las cuotas correspondientes al año actual ya forman parte
    de ``cuotas_totales``. Por esa razón únicamente se agregan
    al total las cuotas futuras que todavía no han sido acreditadas.
    """

    # Una parte de las cuotas del año actual no puede superar
    # el total histórico que ya aparece acreditado.
    if datos.cuotas_anio_actual > datos.cuotas_totales:
        raise ValueError(
            "Las cuotas del año actual no pueden superar "
            "el total de cuotas acreditadas."
        )

    if datos.continua_cotizando:
        # Si continuará cotizando, el cierre proyectado del año
        # no puede ser inferior a lo ya acreditado.
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
        # Si el Asegurado(a) indica que dejará de cotizar, no se
        # incorporan cuotas adicionales al año ni a años futuros.
        cuotas_cierre_anio = datos.cuotas_anio_actual
        cuotas_por_anio_futuras = 0

    # Calcula únicamente las cuotas del año actual que todavía
    # no existen como cuotas reales.
    proyectadas_restantes = max(
        0,
        cuotas_cierre_anio
        - datos.cuotas_anio_actual,
    )

    # El total proyectado parte siempre del total REAL acreditado.
    proyectadas_cierre = (
        datos.cuotas_totales
        + proyectadas_restantes
    )

    # Diferencia respecto del umbral de 180 cuotas.
    faltantes_180 = max(
        0,
        CUOTAS_PENSION_PROPORCIONAL
        - proyectadas_cierre,
    )

    # Diferencia respecto del umbral de 240 cuotas.
    faltantes_240 = max(
        0,
        CUOTAS_REFERENCIA
        - proyectadas_cierre,
    )

    # Estima cuánto tiempo tomaría alcanzar los umbrales
    # utilizando el ritmo anual indicado por el Asegurado(a).
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
