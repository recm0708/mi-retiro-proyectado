"""Integración del asistente con el motor del Subsistema Mixto.

Este servicio reutiliza la construcción cronológica validada para SEBD y
agrega únicamente los datos específicos del Componente de Ahorro Personal.
No contiene fórmulas legales nuevas: prepara una entrada coherente para el
motor ``mixto.py`` y conserva la trazabilidad de años proyectados.
"""

from app.modelos.pension import (
    DatosCalculoMixto,
    DatosResultadoMixto,
    ResumenResultadoMixto,
)
from app.motores.mixto import calcular_mixto
from app.servicios.trazabilidad import construir_trazabilidad_mixto
from app.servicios.resultado_unificado import construir_resumen_unificado_mixto
from app.servicios.resultados import (
    _buscar_escenario_referencia,
    _buscar_escenario_retiro,
    _buscar_escenario_salarial,
    _construir_registros_hasta_retiro,
    _resolver_exceso_por_momento,
)


def calcular_resultado_mixto(
    datos: DatosResultadoMixto,
) -> ResumenResultadoMixto:
    """Calcula el Mixto usando el escenario seleccionado en los Pasos 1–5."""

    if not datos.linea_tiempo.escenarios:
        raise ValueError(
            "No existe una línea temporal salarial disponible. "
            "Vuelve al Paso 4 y genera la proyección."
        )

    escenario_retiro = _buscar_escenario_retiro(datos)

    if escenario_retiro.fecha_ya_transcurrida:
        raise ValueError(
            "El escenario seleccionado ya transcurrió. Con el historial "
            "anual actual no se reconstruye automáticamente el total exacto "
            "de cuotas de una fecha pasada. Usa una fecha futura o aporta "
            "posteriormente detalle mensual."
        )

    escenario_referencia = _buscar_escenario_referencia(datos)
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

    calculo = calcular_mixto(
        DatosCalculoMixto(
            fecha_nacimiento=datos.fecha_nacimiento,
            sexo=datos.sexo,
            fecha_retiro=escenario_retiro.fecha_retiro,
            cuotas_totales=escenario_retiro.cuotas_estimadas_totales,
            cuotas_exceso_antes_referencia=exceso_antes,
            cuotas_exceso_despues_referencia=exceso_despues,
            registros=registros,
            sistema_seleccionado="MIXTO",
            saldo_ahorro_personal=datos.saldo_ahorro_personal,
            bono_reconocimiento=datos.bono_reconocimiento,
            bono_reconocimiento_confirmado_oficialmente=(
                datos.bono_reconocimiento_confirmado_oficialmente
            ),
            valor_actuarial_expectativa_vida=(
                datos.valor_actuarial_expectativa_vida
            ),
            opcion_prestacion_cap=datos.opcion_prestacion_cap,
        )
    )

    advertencias: list[str] = []

    if anios_proyectados:
        advertencias.append(
            "El cálculo Mixto incorpora salarios proyectados de los años: "
            + ", ".join(str(anio) for anio in anios_proyectados)
            + "."
        )

    if hubo_prorrateo:
        advertencias.append(
            "El último año proyectado fue prorrateado porque el retiro "
            "ocurre antes de consumir todas las cuotas previstas de ese año."
        )

    resumen = ResumenResultadoMixto(
        escenario_retiro=escenario_retiro,
        escenario_salarial_nombre=escenario_salarial.nombre,
        anios_proyectados_incluidos=anios_proyectados,
        advertencias_integracion=advertencias,
        calculo=calculo,
    )
    resumen.trazabilidad = construir_trazabilidad_mixto(resumen)
    resumen.resumen_unificado = construir_resumen_unificado_mixto(resumen)
    return resumen
