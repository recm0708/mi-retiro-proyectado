"""Comparación transversal de escenarios previsionales.

Este servicio coordina los motores ya implementados y normaliza sus salidas
para una tabla común. No replica fórmulas legales; cada combinación se calcula
mediante el servicio integrado del sistema correspondiente.
"""

from __future__ import annotations

from datetime import date

from app.core.dinero import redondear_moneda
from app.models.comparacion import (
    DatosComparacionEscenarios,
    FilaComparacionEscenario,
    ResumenComparacionEscenarios,
)
from app.models.pension import (
    DatosResultadoMixto,
    DatosResultadoSEBD,
    DatosResultadoSUCGS,
)
from app.services.resultados_mixto import calcular_resultado_mixto
from app.services.resultados_sebd import calcular_resultado_sebd
from app.services.resultados_sucgs import calcular_resultado_sucgs


NOMBRES_SISTEMA = {
    "SEBD": "SEBD — Beneficio Definido",
    "MIXTO": "Subsistema Mixto",
    "SUCGS": "SUCGS — Sistema Único de Capitalización con Garantía Solidaria",
}


def _clave(fecha_retiro: date, escenario_salarial: str) -> str:
    """Genera una clave estable para una combinación comparable."""

    return f"{fecha_retiro.isoformat()}|{escenario_salarial}"


def _porcentaje_diferencia(valor: float, base: float) -> float | None:
    """Calcula la diferencia porcentual contra una base no nula."""

    if base == 0:
        return None

    return round(((valor - base) / abs(base)) * 100, 4)


def _resolver_fechas(datos: DatosComparacionEscenarios) -> list[date]:
    """Obtiene las fechas válidas a comparar, preservando orden."""

    bloque = _bloque_datos(datos)
    # Solo se comparan fechas futuras ya generadas por el resumen de retiro;
    # las fechas vencidas no se reevalúan para evitar matrices engañosas.
    disponibles = [
        escenario.fecha_retiro
        for escenario in bloque.resumen_retiro.escenarios
        if not escenario.fecha_ya_transcurrida
    ]

    solicitadas = datos.fechas_retiro or disponibles
    conjunto_disponible = set(disponibles)

    fechas: list[date] = []
    # Se preserva el orden solicitado por el usuario y se eliminan duplicados
    # sin alterar la fecha base que alimenta las diferencias.
    for fecha in solicitadas:
        if fecha in conjunto_disponible and fecha not in fechas:
            fechas.append(fecha)

    base = bloque.fecha_retiro_seleccionada
    if base in conjunto_disponible and base not in fechas:
        fechas.insert(0, base)

    return fechas


def _resolver_salarios(datos: DatosComparacionEscenarios) -> list[str]:
    """Obtiene los escenarios salariales válidos a comparar."""

    bloque = _bloque_datos(datos)
    # Los escenarios salariales disponibles provienen de la línea de tiempo ya
    # calculada; el comparador solo selecciona nombres válidos.
    disponibles = [
        escenario.nombre
        for escenario in bloque.linea_tiempo.escenarios
    ]

    solicitados = datos.escenarios_salariales or disponibles

    nombres: list[str] = []
    for nombre in solicitados:
        if nombre in disponibles and nombre not in nombres:
            nombres.append(nombre)

    base = bloque.escenario_salarial_nombre
    if base in disponibles and base not in nombres:
        nombres.insert(0, base)

    return nombres


def _bloque_datos(
    datos: DatosComparacionEscenarios,
) -> DatosResultadoSEBD | DatosResultadoMixto | DatosResultadoSUCGS:
    """Devuelve el bloque integrado correspondiente al sistema."""

    if datos.sistema == "SEBD":
        assert datos.datos_sebd is not None
        return datos.datos_sebd

    if datos.sistema == "MIXTO":
        assert datos.datos_mixto is not None
        return datos.datos_mixto

    assert datos.datos_sucgs is not None
    return datos.datos_sucgs


def _fila_sebd(
    datos: DatosResultadoSEBD,
    fecha: date,
    salario: str,
    es_base: bool,
) -> FilaComparacionEscenario:
    """Calcula y normaliza una combinación SEBD."""

    # Cada fila se calcula con una copia del contrato original para no mutar
    # el resultado base que ya fue mostrado en el Paso 6.
    # La fecha/salario alternativo viaja como copia; los saldos aportados por
    # el usuario se conservan para advertir cuando no hay proyección actuarial.
    # SUCGS reutiliza el saldo solidario informado; por eso una fecha distinta
    # agrega advertencia en vez de simular un saldo no calculado.
    solicitud = datos.model_copy(
        update={
            "fecha_retiro_seleccionada": fecha,
            "escenario_salarial_nombre": salario,
        }
    )
    resultado = calcular_resultado_sebd(solicitud)
    calculo = resultado.calculo
    normalizado = resultado.resumen_unificado
    assert normalizado is not None

    advertencias = normalizado.advertencias

    return FilaComparacionEscenario(
        clave=_clave(fecha, salario),
        es_base=es_base,
        sistema="SEBD",
        escenario_retiro_nombre=resultado.escenario_retiro.nombre,
        tipo_retiro=resultado.escenario_retiro.tipo,
        fecha_retiro=resultado.escenario_retiro.fecha_retiro,
        edad_retiro_anios=resultado.escenario_retiro.edad_retiro_anios,
        cuotas_estimadas_totales=(
            resultado.escenario_retiro.cuotas_estimadas_totales
        ),
        escenario_salarial_nombre=resultado.escenario_salarial_nombre,
        modalidad=normalizado.modalidad_codigo,
        modalidad_nombre=normalizado.modalidad_nombre,
        tipo_prestacion=normalizado.naturaleza_prestacion,
        calculo_completo=normalizado.calculo_completo,
        pension_mensual_estimada=normalizado.pension_mensual_estimada,
        pago_unico_estimado=normalizado.pago_unico_estimado,
        advertencias=advertencias,
    )


def _fila_mixto(
    datos: DatosResultadoMixto,
    fecha: date,
    salario: str,
    es_base: bool,
) -> FilaComparacionEscenario:
    """Calcula y normaliza una combinación del Subsistema Mixto."""

    solicitud = datos.model_copy(
        update={
            "fecha_retiro_seleccionada": fecha,
            "escenario_salarial_nombre": salario,
        }
    )
    resultado = calcular_resultado_mixto(solicitud)
    calculo = resultado.calculo
    normalizado = resultado.resumen_unificado
    assert normalizado is not None

    advertencias = list(normalizado.advertencias)

    if fecha != datos.fecha_retiro_seleccionada:
        advertencias.append(
            "El saldo CAP, el bono y el valor actuarial se reutilizaron sin "
            "proyectarlos para esta fecha alternativa. Interpreta la fila "
            "como un escenario hipotético con esos datos constantes."
        )

    return FilaComparacionEscenario(
        clave=_clave(fecha, salario),
        es_base=es_base,
        sistema="MIXTO",
        escenario_retiro_nombre=resultado.escenario_retiro.nombre,
        tipo_retiro=resultado.escenario_retiro.tipo,
        fecha_retiro=resultado.escenario_retiro.fecha_retiro,
        edad_retiro_anios=resultado.escenario_retiro.edad_retiro_anios,
        cuotas_estimadas_totales=(
            resultado.escenario_retiro.cuotas_estimadas_totales
        ),
        escenario_salarial_nombre=resultado.escenario_salarial_nombre,
        modalidad=normalizado.modalidad_codigo,
        modalidad_nombre=normalizado.modalidad_nombre,
        tipo_prestacion=normalizado.naturaleza_prestacion,
        calculo_completo=normalizado.calculo_completo,
        pension_mensual_estimada=normalizado.pension_mensual_estimada,
        pago_unico_estimado=normalizado.pago_unico_estimado,
        advertencias=advertencias,
    )


def _fila_sucgs(
    datos: DatosResultadoSUCGS,
    fecha: date,
    salario: str,
    es_base: bool,
) -> FilaComparacionEscenario:
    """Calcula y normaliza una combinación SUCGS."""

    solicitud = datos.model_copy(
        update={
            "fecha_retiro_seleccionada": fecha,
            "escenario_salarial_nombre": salario,
        }
    )
    resultado = calcular_resultado_sucgs(solicitud)
    calculo = resultado.calculo
    normalizado = resultado.resumen_unificado
    assert normalizado is not None

    advertencias = list(normalizado.advertencias)

    if fecha != datos.fecha_retiro_seleccionada:
        advertencias.append(
            "El saldo de Capitalización Solidaria se reutilizó sin "
            "proyectarlo para esta fecha alternativa. Interpreta la fila "
            "como un escenario hipotético con saldo constante."
        )

    return FilaComparacionEscenario(
        clave=_clave(fecha, salario),
        es_base=es_base,
        sistema="SUCGS",
        escenario_retiro_nombre=resultado.escenario_retiro.nombre,
        tipo_retiro=resultado.escenario_retiro.tipo,
        fecha_retiro=resultado.escenario_retiro.fecha_retiro,
        edad_retiro_anios=resultado.escenario_retiro.edad_retiro_anios,
        cuotas_estimadas_totales=(
            resultado.escenario_retiro.cuotas_estimadas_totales
        ),
        escenario_salarial_nombre=resultado.escenario_salarial_nombre,
        modalidad=normalizado.modalidad_codigo,
        modalidad_nombre=normalizado.modalidad_nombre,
        tipo_prestacion=normalizado.naturaleza_prestacion,
        calculo_completo=normalizado.calculo_completo,
        pension_mensual_estimada=normalizado.pension_mensual_estimada,
        pago_unico_estimado=normalizado.pago_unico_estimado,
        advertencias=advertencias,
    )


def _calcular_fila(
    datos: DatosComparacionEscenarios,
    fecha: date,
    salario: str,
    es_base: bool,
) -> FilaComparacionEscenario:
    """Delega el cálculo al servicio integrado del sistema."""

    if datos.sistema == "SEBD":
        assert datos.datos_sebd is not None
        return _fila_sebd(datos.datos_sebd, fecha, salario, es_base)

    if datos.sistema == "MIXTO":
        assert datos.datos_mixto is not None
        return _fila_mixto(datos.datos_mixto, fecha, salario, es_base)

    assert datos.datos_sucgs is not None
    return _fila_sucgs(datos.datos_sucgs, fecha, salario, es_base)


def _aplicar_diferencias(
    filas: list[FilaComparacionEscenario],
    clave_base: str,
) -> None:
    """Completa diferencias absolutas y porcentuales contra la base."""

    base = next((fila for fila in filas if fila.clave == clave_base), None)

    # Sin fila base no existe denominador confiable; en ese caso se devuelven
    # las filas sin diferencias para que la interfaz muestre la advertencia.
    if base is None:
        return

    for fila in filas:
        if (
            base.pension_mensual_estimada is not None
            and fila.pension_mensual_estimada is not None
        ):
            diferencia = redondear_moneda(
                fila.pension_mensual_estimada
                - base.pension_mensual_estimada
            )
            fila.diferencia_mensual_absoluta = diferencia
            fila.diferencia_mensual_pct = _porcentaje_diferencia(
                fila.pension_mensual_estimada,
                base.pension_mensual_estimada,
            )

        if (
            base.pago_unico_estimado is not None
            and fila.pago_unico_estimado is not None
        ):
            diferencia_pago = redondear_moneda(
                fila.pago_unico_estimado
                - base.pago_unico_estimado
            )
            fila.diferencia_pago_unico_absoluta = diferencia_pago
            fila.diferencia_pago_unico_pct = _porcentaje_diferencia(
                fila.pago_unico_estimado,
                base.pago_unico_estimado,
            )


def comparar_escenarios(
    datos: DatosComparacionEscenarios,
) -> ResumenComparacionEscenarios:
    """Construye la matriz retiro × salario y sus diferencias."""

    bloque = _bloque_datos(datos)
    fechas = _resolver_fechas(datos)
    salarios = _resolver_salarios(datos)

    if not fechas:
        raise ValueError(
            "No existen escenarios de retiro futuros disponibles para comparar."
        )

    if not salarios:
        raise ValueError(
            "No existen escenarios salariales disponibles para comparar."
        )

    clave_base = _clave(
        bloque.fecha_retiro_seleccionada,
        bloque.escenario_salarial_nombre,
    )

    filas: list[FilaComparacionEscenario] = []

    # La matriz retiro × salario se construye de forma exhaustiva y cada
    # combinación se mantiene independiente para poder comparar o advertir.
    for fecha in fechas:
        for salario in salarios:
            es_base = _clave(fecha, salario) == clave_base

            try:
                fila = _calcular_fila(
                    datos=datos,
                    fecha=fecha,
                    salario=salario,
                    es_base=es_base,
                )
            except ValueError as error:
                # Un fallo de cálculo en una combinación no invalida toda la
                # matriz; se conserva la fila incompleta con la causa visible.
                escenario = next(
                    escenario
                    for escenario in bloque.resumen_retiro.escenarios
                    if escenario.fecha_retiro == fecha
                )

                fila = FilaComparacionEscenario(
                    clave=_clave(fecha, salario),
                    es_base=es_base,
                    sistema=datos.sistema,
                    escenario_retiro_nombre=escenario.nombre,
                    tipo_retiro=escenario.tipo,
                    fecha_retiro=escenario.fecha_retiro,
                    edad_retiro_anios=escenario.edad_retiro_anios,
                    cuotas_estimadas_totales=(
                        escenario.cuotas_estimadas_totales
                    ),
                    escenario_salarial_nombre=salario,
                    modalidad=None,
                    modalidad_nombre=None,
                    tipo_prestacion=None,
                    calculo_completo=False,
                    pension_mensual_estimada=None,
                    pago_unico_estimado=None,
                    advertencias=[str(error)],
                )

            filas.append(fila)

    _aplicar_diferencias(filas, clave_base)

    # Los destacados se calculan únicamente con filas completas para no
    # convertir advertencias o pagos no disponibles en recomendaciones.
    completas = [fila for fila in filas if fila.calculo_completo]
    con_mensual = [
        fila
        for fila in completas
        if fila.pension_mensual_estimada is not None
    ]
    con_pago = [
        fila
        for fila in completas
        if fila.pago_unico_estimado is not None
    ]

    mejor_mensual = (
        max(con_mensual, key=lambda fila: fila.pension_mensual_estimada).clave
        if con_mensual
        else None
    )
    mayor_pago = (
        max(con_pago, key=lambda fila: fila.pago_unico_estimado).clave
        if con_pago
        else None
    )

    advertencias: list[str] = [
        "Las diferencias se calculan contra la combinación seleccionada en "
        "el Paso 6 como escenario base.",
        "Una cifra mayor no implica por sí sola una decisión óptima: la "
        "comparación no incorpora valor presente, inflación, impuestos, "
        "preferencias personales ni riesgo actuarial individual.",
    ]

    if datos.sistema == "MIXTO":
        advertencias.append(
            "Para fechas alternativas se reutilizan el saldo CAP, el bono y "
            "el valor actuarial ingresados en el Paso 6. La aplicación aún no "
            "proyecta automáticamente esos valores por fecha."
        )

    if datos.sistema == "SUCGS":
        advertencias.append(
            "Para fechas alternativas se reutiliza el saldo de Capitalización "
            "Solidaria ingresado en el Paso 6. La aplicación aún no proyecta "
            "automáticamente ese saldo por fecha."
        )

    if not any(fila.es_base for fila in filas):
        advertencias.append(
            "El escenario base actual no pudo incluirse en la matriz; las "
            "diferencias porcentuales pueden quedar sin calcular."
        )

    return ResumenComparacionEscenarios(
        sistema=datos.sistema,
        nombre_sistema=NOMBRES_SISTEMA[datos.sistema],
        clave_escenario_base=clave_base,
        filas=filas,
        total_combinaciones=len(filas),
        resultados_completos=len(completas),
        resultados_incompletos=len(filas) - len(completas),
        clave_mejor_pension_mensual=mejor_mensual,
        clave_mayor_pago_unico=mayor_pago,
        advertencias=advertencias,
    )
