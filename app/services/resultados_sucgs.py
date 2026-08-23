"""Integración visual del asistente con el motor SUCGS hasta el art. 197.

El servicio reutiliza la construcción cronológica ya validada por SEBD y
Mixto. De este modo el historial real, las cuotas proyectadas y el escenario
salarial seleccionado llegan al motor SUCGS sin duplicar reglas de proyección.
"""

from app.models.pension import (
    DatosCalculoSUCGS,
    DatosResultadoSUCGS,
    ResumenResultadoSUCGS,
)
from app.engines.sucgs import calcular_sucgs
from app.services.trazabilidad import construir_trazabilidad_sucgs
from app.services.resultado_unificado import construir_resumen_unificado_sucgs
from app.services.resultados import (
    _buscar_escenario_retiro,
    _buscar_escenario_salarial,
    _ajustar_escenario_solo_acreditado,
    _construir_registros_hasta_retiro,
)


def calcular_resultado_sucgs(
    datos: DatosResultadoSUCGS,
) -> ResumenResultadoSUCGS:
    """Calcula SUCGS usando los Pasos 1–5 y los datos específicos del Paso 6."""

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
            "anual actual no se reconstruye automáticamente el saldo ni la "
            "distribución mensual exacta de una fecha pasada."
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

    anio_inicio_vida_laboral = datos.historial.anio_inicio

    calculo = calcular_sucgs(
        DatosCalculoSUCGS(
            fecha_nacimiento=datos.fecha_nacimiento,
            sexo=datos.sexo,
            fecha_retiro=escenario_retiro.fecha_retiro,
            cuotas_totales=escenario_retiro.cuotas_estimadas_totales,
            saldo_capitalizacion_solidaria=(
                datos.saldo_capitalizacion_solidaria
            ),
            saldo_confirmado_oficialmente=(
                datos.saldo_confirmado_oficialmente
            ),
            valor_minimo_universal_vigente=(
                datos.valor_minimo_universal_vigente
            ),
            pension_garantizada_solidaria_vigente=(
                datos.pension_garantizada_solidaria_vigente
            ),
            valores_solidarios_confirmados_oficialmente=(
                datos.valores_solidarios_confirmados_oficialmente
            ),
            anio_inicio_vida_laboral=anio_inicio_vida_laboral,
            registros_historial_laboral=registros,
            historial_laboral_completo=(
                datos.historial_laboral_completo_confirmado
            ),
            estabilidad_salarial_art197_confirmada=(
                datos.estabilidad_salarial_art197_confirmada
            ),
        )
    )

    advertencias: list[str] = []

    if datos.modo_integracion == "SOLO_ACREDITADO":
        advertencias.append(
            "La comparación acreditada conserva el saldo solidario y valores "
            "específicos introducidos en el Paso 6, pero no añade salarios ni "
            "cuotas futuras al historial."
        )

    if anios_proyectados:
        advertencias.append(
            "La evaluación SUCGS incorpora salarios proyectados de los años: "
            + ", ".join(str(anio) for anio in anios_proyectados)
            + "."
        )

    if hubo_prorrateo:
        advertencias.append(
            "El último año proyectado fue prorrateado porque la fecha de "
            "retiro ocurre antes de consumir todas las cuotas previstas."
        )

    if not datos.historial_laboral_completo_confirmado:
        advertencias.append(
            "La garantía de reemplazo del artículo 197 no puede cerrarse "
            "mientras no se confirme que el historial ingresado cubre toda "
            "la vida laboral relevante."
        )

    resumen = ResumenResultadoSUCGS(
        modo_integracion=datos.modo_integracion,
        escenario_retiro=escenario_retiro,
        escenario_salarial_nombre=escenario_salarial.nombre,
        anios_proyectados_incluidos=anios_proyectados,
        advertencias_integracion=advertencias,
        calculo=calculo,
    )
    resumen.trazabilidad = construir_trazabilidad_sucgs(resumen)
    resumen.resumen_unificado = construir_resumen_unificado_sucgs(resumen)
    return resumen
