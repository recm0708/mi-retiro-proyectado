"""Servicios para validar y resumir el historial salarial.

Este módulo procesa los registros históricos proporcionados por
el Asegurado(a). Cada registro representa las cuotas acreditadas y el
salario reportado a la CSS durante un año calendario.

Los datos históricos se mantienen separados de cualquier
proyección salarial futura.
"""

from app.core.dinero import (
    a_decimal,
    redondear_moneda,
)
from app.modelos.simulacion import (
    DatosHistorialSalarial,
    RegistroHistorialNormalizado,
    ResumenHistorialSalarial,
)


# ============================================================
# Funciones auxiliares
# ============================================================

def _determinar_estado_registro(
    cuotas: int,
) -> str:
    """Determina el estado descriptivo de un registro anual."""

    if cuotas == 0:
        return "SIN_COTIZACION"

    if cuotas < 12:
        return "HISTORICO_PARCIAL"

    return "HISTORICO_COMPLETO"


# ============================================================
# Análisis principal
# ============================================================

def analizar_historial_salarial(
    datos: DatosHistorialSalarial,
) -> ResumenHistorialSalarial:
    """Valida y resume un historial salarial anual.

    El servicio comprueba años duplicados, límites temporales,
    coherencia básica entre cuotas y salarios y la diferencia
    entre la suma anual de cuotas y el total de referencia
    informado previamente por el Asegurado(a).
    """

    if datos.anio_fin < datos.anio_inicio:
        raise ValueError(
            "El año final del historial no puede ser "
            "anterior al año inicial."
        )

    # Impide que un mismo año aparezca más de una vez.
    anios_registrados = [
        registro.anio
        for registro in datos.registros
    ]

    if len(anios_registrados) != len(set(anios_registrados)):
        raise ValueError(
            "El historial contiene años duplicados."
        )

    registros_por_anio = {
        registro.anio: registro
        for registro in datos.registros
    }

    registros_normalizados: list[
        RegistroHistorialNormalizado
    ] = []

    anios_sin_registro: list[int] = []

    # Se recorre todo el período para poder detectar años
    # que no fueron proporcionados por el Asegurado(a).
    for anio in range(
        datos.anio_inicio,
        datos.anio_fin + 1,
    ):
        registro = registros_por_anio.get(
            anio,
        )

        if registro is None:
            anios_sin_registro.append(
                anio,
            )
            continue

        if (
            registro.cuotas > 0
            and registro.salario_cotizado <= 0
        ):
            raise ValueError(
                f"El año {anio} tiene cuotas acreditadas "
                "pero no tiene salario cotizado."
            )

        if (
            registro.cuotas == 0
            and registro.salario_cotizado > 0
        ):
            raise ValueError(
                f"El año {anio} tiene salario cotizado "
                "pero registra cero cuotas."
            )

        registros_normalizados.append(
            RegistroHistorialNormalizado(
                anio=registro.anio,
                cuotas=registro.cuotas,
                salario_cotizado=redondear_moneda(
                    registro.salario_cotizado
                ),
                estado=_determinar_estado_registro(
                    registro.cuotas,
                ),
            )
        )

    # No debe existir un registro fuera del período declarado.
    anios_fuera_rango = [
        anio
        for anio in anios_registrados
        if (
            anio < datos.anio_inicio
            or anio > datos.anio_fin
        )
    ]

    if anios_fuera_rango:
        raise ValueError(
            "Existen registros fuera del período "
            "de historial indicado."
        )

    cuotas_sumadas = sum(
        registro.cuotas
        for registro in registros_normalizados
    )

    total_salarios = sum(
        (
            a_decimal(
                registro.salario_cotizado
            )
            for registro in registros_normalizados
        ),
        start=a_decimal("0"),
    )

    # Un valor positivo significa que todavía faltan cuotas
    # por identificar dentro del historial anual.
    diferencia_cuotas = (
        datos.cuotas_totales_referencia
        - cuotas_sumadas
    )

    registros_con_cuotas = [
        registro
        for registro in registros_normalizados
        if registro.cuotas > 0
    ]

    ultimo_registro = (
        registros_con_cuotas[-1]
        if registros_con_cuotas
        else None
    )

    historial_completo = (
        len(anios_sin_registro) == 0
    )

    cuotas_coinciden = (
        historial_completo
        and diferencia_cuotas == 0
    )

    return ResumenHistorialSalarial(
        anio_inicio=datos.anio_inicio,
        anio_fin=datos.anio_fin,
        cuotas_totales_referencia=(
            datos.cuotas_totales_referencia
        ),
        cuotas_sumadas=cuotas_sumadas,
        diferencia_cuotas=diferencia_cuotas,
        cuotas_coinciden=cuotas_coinciden,
        historial_completo=historial_completo,
        anios_sin_registro=anios_sin_registro,
        total_salarios_reportados=redondear_moneda(
            total_salarios
        ),
        ultimo_anio_con_cuotas=(
            ultimo_registro.anio
            if ultimo_registro
            else None
        ),
        ultimo_salario_cotizado=(
            ultimo_registro.salario_cotizado
            if ultimo_registro
            else None
        ),
        registros=registros_normalizados,
    )
