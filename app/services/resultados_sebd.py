"""Integración general del asistente con las modalidades SEBD.

Reutiliza la construcción cronológica ya validada en ``resultados.py`` y
entrega la entrada consolidada al clasificador/motor general SEBD.
"""

from app.models.pension import (
    DatosCalculoSEBD,
    DatosResultadoSEBD,
    ResumenResultadoSEBD,
)
from app.engines.sebd_modalidades import calcular_sebd
from app.services.trazabilidad import construir_trazabilidad_sebd
from app.services.resultado_unificado import construir_resumen_unificado_sebd
from app.services.resultados import (
    _buscar_escenario_referencia,
    _buscar_escenario_retiro,
    _buscar_escenario_salarial,
    _ajustar_escenario_solo_acreditado,
    _construir_registros_hasta_retiro,
    _resolver_exceso_por_momento,
)


def calcular_resultado_sebd(
    datos: DatosResultadoSEBD,
) -> ResumenResultadoSEBD:
    """Clasifica y calcula la prestación SEBD del escenario elegido."""

    if not datos.linea_tiempo.escenarios:
        raise ValueError(
            "No existe una línea temporal salarial disponible. "
            "Vuelve al Paso 4 y genera la proyección."
        )

    escenario_retiro = _buscar_escenario_retiro(datos)
    escenario_retiro = _ajustar_escenario_solo_acreditado(
        datos, escenario_retiro
    )

    if escenario_retiro.fecha_ya_transcurrida:
        raise ValueError(
            "El escenario seleccionado ya transcurrió. Con el historial "
            "anual actual no se reconstruye automáticamente el total exacto "
            "de cuotas de una fecha pasada. Usa una fecha futura o aporta "
            "posteriormente detalle mensual."
        )

    escenario_referencia = _buscar_escenario_referencia(datos)
    escenario_referencia = _ajustar_escenario_solo_acreditado(
        datos, escenario_referencia
    )
    escenario_salarial = _buscar_escenario_salarial(datos)

    (
        registros,
        anios_proyectados,
        hubo_prorrateo,
    ) = _construir_registros_hasta_retiro(
        datos,
        escenario_retiro,
        escenario_salarial,
    )

    exceso_antes, exceso_despues = _resolver_exceso_por_momento(
        escenario_retiro=escenario_retiro,
        escenario_referencia=escenario_referencia,
    )

    calculo = calcular_sebd(
        DatosCalculoSEBD(
            fecha_nacimiento=datos.fecha_nacimiento,
            sexo=datos.sexo,
            fecha_retiro=escenario_retiro.fecha_retiro,
            cuotas_totales=(
                escenario_retiro.cuotas_estimadas_totales
            ),
            cuotas_exceso_antes_referencia=exceso_antes,
            cuotas_exceso_despues_referencia=exceso_despues,
            registros=registros,
        )
    )

    advertencias: list[str] = []

    if datos.modo_integracion == "SOLO_ACREDITADO":
        advertencias.append(
            "Este cálculo conserva la fecha de retiro seleccionada, pero usa "
            "solo cuotas y salarios ya acreditados en el historial actual; "
            "no incorpora nuevas cotizaciones futuras."
        )

    if anios_proyectados:
        advertencias.append(
            "El cálculo incorpora salarios proyectados de los años: "
            + ", ".join(str(anio) for anio in anios_proyectados)
            + "."
        )

    if hubo_prorrateo:
        advertencias.append(
            "El último año proyectado fue prorrateado porque el retiro "
            "ocurre antes de consumir todas las cuotas previstas de ese año."
        )

    resumen = ResumenResultadoSEBD(
        modo_integracion=datos.modo_integracion,
        escenario_retiro=escenario_retiro,
        escenario_salarial_nombre=datos.escenario_salarial_nombre,
        anios_proyectados_incluidos=anios_proyectados,
        advertencias_integracion=advertencias,
        calculo=calculo,
    )
    resumen.trazabilidad = construir_trazabilidad_sebd(resumen)
    resumen.resumen_unificado = construir_resumen_unificado_sebd(resumen)
    return resumen
