"""Normalización transversal de resultados previsionales.

Las funciones de este módulo no recalculan ninguna prestación. Reciben el
resultado ya producido por el motor integrado y construyen un contrato común
para la interfaz, el comparador y futuras exportaciones.
"""

from app.modelos.pension import (
    ResumenResultadoMixto,
    ResumenResultadoSEBD,
    ResumenResultadoSUCGS,
)
from app.modelos.resultado_unificado import ResumenPrestacionUnificada


NOMBRES_SISTEMA = {
    "SEBD": "SEBD — Beneficio Definido",
    "MIXTO": "Subsistema Mixto",
    "SUCGS": "SUCGS — Sistema Único de Capitalización con Garantía Solidaria",
}

NOMBRES_PRESTACION_SUCGS = {
    "PENSION_CONTRIBUTIVA_SIN_COMPLEMENTO": (
        "Pensión contributiva sin complemento"
    ),
    "PENSION_BENEFICIO_SOLIDARIO": "Pensión Garantizada Solidaria",
    "PENSION_BENEFICIO_MINIMO": "Pensión de Beneficio Mínimo",
    "PENSION_CONTRIBUTIVA_MENOR_MINIMO": (
        "Pensión contributiva inferior al mínimo universal"
    ),
}

NOMBRES_ESTADO_MIXTO = {
    "TRANSICION_SUCGS": "Transición del Subsistema Mixto al SUCGS",
    "MIXTO_CALCULABLE": "Subsistema Mixto calculable",
}


def _naturaleza(
    pension_mensual: float | None,
    pago_unico: float | None,
    transicion: bool = False,
) -> str:
    """Clasifica la naturaleza económica sin mezclar mensualidad y pago único."""

    if transicion:
        return "TRANSICION"
    if pension_mensual is not None and pago_unico is not None:
        return "PENSION_MAS_PAGO_UNICO"
    if pension_mensual is not None:
        return "PENSION_MENSUAL"
    if pago_unico is not None:
        return "PAGO_UNICO"
    return "SIN_MONTO"


def construir_resumen_unificado_sebd(
    resultado: ResumenResultadoSEBD,
) -> ResumenPrestacionUnificada:
    """Normaliza un resultado SEBD ya calculado."""

    calculo = resultado.calculo
    transicion = calculo.modalidad == "TRANSICION_SUCGS"

    if transicion:
        estado = "TRANSICION"
    elif not calculo.elegible:
        estado = "NO_ELEGIBLE"
    elif calculo.calculo_disponible:
        estado = "COMPLETO"
    else:
        estado = "INCOMPLETO"

    pago_unico = calculo.indemnizacion_pago_unico_estimado
    advertencias = [
        *resultado.advertencias_integracion,
        *calculo.advertencias,
    ]

    return ResumenPrestacionUnificada(
        sistema="SEBD",
        nombre_sistema=NOMBRES_SISTEMA["SEBD"],
        escenario_retiro_nombre=resultado.escenario_retiro.nombre,
        fecha_retiro=resultado.escenario_retiro.fecha_retiro,
        edad_retiro_anios=resultado.escenario_retiro.edad_retiro_anios,
        cuotas_estimadas_totales=(
            resultado.escenario_retiro.cuotas_estimadas_totales
        ),
        escenario_salarial_nombre=resultado.escenario_salarial_nombre,
        modalidad_codigo=calculo.modalidad,
        modalidad_nombre=calculo.modalidad_nombre,
        estado_resultado=estado,
        naturaleza_prestacion=_naturaleza(
            calculo.pension_mensual_estimada,
            pago_unico,
            transicion,
        ),
        calculo_completo=(estado == "COMPLETO"),
        pension_mensual_estimada=calculo.pension_mensual_estimada,
        pago_unico_estimado=pago_unico,
        advertencias=advertencias,
    )


def construir_resumen_unificado_mixto(
    resultado: ResumenResultadoMixto,
) -> ResumenPrestacionUnificada:
    """Normaliza un resultado del Subsistema Mixto ya calculado."""

    calculo = resultado.calculo
    cap = calculo.componente_ahorro_personal
    decision = bool(cap and cap.decision_requerida)
    transicion = calculo.estado_sistema == "TRANSICION_SUCGS"

    if transicion:
        estado = "TRANSICION"
    elif decision:
        estado = "DECISION_REQUERIDA"
    elif not calculo.elegible:
        estado = "NO_ELEGIBLE"
    elif calculo.calculo_completo:
        estado = "COMPLETO"
    else:
        estado = "INCOMPLETO"

    no_confirmados: list[str] = []
    if cap is not None:
        if (
            cap.bono_reconocimiento > 0
            and not cap.bono_reconocimiento_confirmado_oficialmente
        ):
            no_confirmados.append("Bono de reconocimiento")
        if cap.saldo_ahorro_personal is None:
            no_confirmados.append("Saldo CAP")

    advertencias = [
        *resultado.advertencias_integracion,
        *calculo.advertencias,
    ]

    return ResumenPrestacionUnificada(
        sistema="MIXTO",
        nombre_sistema=NOMBRES_SISTEMA["MIXTO"],
        escenario_retiro_nombre=resultado.escenario_retiro.nombre,
        fecha_retiro=resultado.escenario_retiro.fecha_retiro,
        edad_retiro_anios=resultado.escenario_retiro.edad_retiro_anios,
        cuotas_estimadas_totales=(
            resultado.escenario_retiro.cuotas_estimadas_totales
        ),
        escenario_salarial_nombre=resultado.escenario_salarial_nombre,
        modalidad_codigo=calculo.modalidad or calculo.estado_sistema,
        modalidad_nombre=(
            calculo.modalidad_nombre
            or NOMBRES_ESTADO_MIXTO.get(
                calculo.estado_sistema,
                calculo.estado_sistema,
            )
        ),
        estado_resultado=estado,
        naturaleza_prestacion=_naturaleza(
            calculo.pension_mensual_total_estimada,
            calculo.pago_unico_total_estimado,
            transicion,
        ),
        calculo_completo=(estado == "COMPLETO"),
        requiere_decision_usuario=decision,
        pension_mensual_estimada=calculo.pension_mensual_total_estimada,
        pago_unico_estimado=calculo.pago_unico_total_estimado,
        datos_no_confirmados=no_confirmados,
        advertencias=advertencias,
    )


def construir_resumen_unificado_sucgs(
    resultado: ResumenResultadoSUCGS,
) -> ResumenPrestacionUnificada:
    """Normaliza un resultado SUCGS ya calculado."""

    calculo = resultado.calculo

    if not calculo.cumple_edad_referencia:
        estado = "NO_ELEGIBLE"
    elif calculo.calculo_total_disponible:
        estado = "COMPLETO"
    else:
        estado = "INCOMPLETO"

    no_confirmados: list[str] = []
    if not calculo.saldo_confirmado_oficialmente:
        no_confirmados.append("Saldo de Capitalización Solidaria")
    if not calculo.valores_solidarios_confirmados_oficialmente:
        no_confirmados.append("Valores solidarios vigentes")

    advertencias = [
        *resultado.advertencias_integracion,
        *calculo.advertencias,
    ]

    return ResumenPrestacionUnificada(
        sistema="SUCGS",
        nombre_sistema=NOMBRES_SISTEMA["SUCGS"],
        escenario_retiro_nombre=resultado.escenario_retiro.nombre,
        fecha_retiro=resultado.escenario_retiro.fecha_retiro,
        edad_retiro_anios=resultado.escenario_retiro.edad_retiro_anios,
        cuotas_estimadas_totales=(
            resultado.escenario_retiro.cuotas_estimadas_totales
        ),
        escenario_salarial_nombre=resultado.escenario_salarial_nombre,
        modalidad_codigo="SUCGS",
        modalidad_nombre=(
            NOMBRES_PRESTACION_SUCGS.get(
                calculo.tipo_prestacion_solidaria,
                calculo.tipo_prestacion_solidaria,
            )
            if calculo.tipo_prestacion_solidaria
            else "Sistema Único de Capitalización con Garantía Solidaria"
        ),
        estado_resultado=estado,
        naturaleza_prestacion=_naturaleza(
            calculo.pension_mensual_total_estimada,
            None,
        ),
        calculo_completo=(estado == "COMPLETO"),
        pension_mensual_estimada=calculo.pension_mensual_total_estimada,
        pago_unico_estimado=None,
        datos_no_confirmados=no_confirmados,
        advertencias=advertencias,
    )
