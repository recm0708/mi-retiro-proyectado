"""Integración de los pasos del asistente con los motores de pensión.

Este módulo no contiene fórmulas legales nuevas. Su responsabilidad es
convertir el historial, la línea temporal salarial y el escenario de retiro
seleccionado en una entrada coherente para los motores jurídicos.

Las proyecciones futuras se mantienen identificadas como estimaciones y se
prorratean únicamente cuando la fecha de retiro corta un año proyectado antes
de consumir todas las cuotas previstas para ese año.
"""

from decimal import Decimal

from app.core.dinero import (
    a_decimal,
    redondear_moneda,
)
from app.models.pension import (
    DatosCalculoSEBDNormal,
    DatosResultadoSEBDNormal,
    ResumenResultadoSEBDNormal,
)
from app.models.simulacion import (
    EscenarioLineaTiempo,
    EscenarioRetiro,
    RegistroHistorialSalarial,
)
from app.engines.sebd import calcular_sebd_normal


def _buscar_escenario_retiro(
    datos: DatosResultadoSEBDNormal,
) -> EscenarioRetiro:
    """Localiza el escenario de retiro seleccionado por fecha exacta."""

    for escenario in datos.resumen_retiro.escenarios:
        if escenario.fecha_retiro == datos.fecha_retiro_seleccionada:
            return escenario

    raise ValueError(
        "El escenario de retiro seleccionado ya no existe en el análisis "
        "del Paso 5. Vuelve a analizar los escenarios de retiro."
    )


def _buscar_escenario_referencia(
    datos: DatosResultadoSEBDNormal,
) -> EscenarioRetiro:
    """Obtiene el escenario correspondiente a la edad de referencia."""

    for escenario in datos.resumen_retiro.escenarios:
        if escenario.tipo == "REFERENCIA":
            return escenario

    raise ValueError(
        "No se encontró el escenario base de edad de referencia del Paso 5."
    )


def _buscar_escenario_salarial(
    datos: DatosResultadoSEBDNormal,
) -> EscenarioLineaTiempo:
    """Obtiene la línea temporal salarial elegida por el Asegurado(a)."""

    for escenario in datos.linea_tiempo.escenarios:
        if escenario.nombre == datos.escenario_salarial_nombre:
            return escenario

    raise ValueError(
        "El escenario salarial seleccionado ya no existe en el Paso 4. "
        "Vuelve a generar la proyección salarial."
    )


def _ajustar_escenario_solo_acreditado(
    datos: DatosResultadoSEBDNormal,
    escenario: EscenarioRetiro,
) -> EscenarioRetiro:
    """Devuelve el mismo momento de retiro usando solo cuotas ya acreditadas.

    La fecha y la edad del escenario no cambian. Únicamente se elimina la
    incorporación de cuotas futuras para que los motores puedan responder a
    la pregunta: qué prestación resultaría en esa fecha si no se añadieran
    nuevos salarios ni nuevas cuotas después del corte actual.
    """

    if getattr(datos, "modo_integracion", "PROYECTADO") != "SOLO_ACREDITADO":
        return escenario

    cuotas_acreditadas = int(datos.historial.cuotas_totales_referencia)

    return escenario.model_copy(
        update={
            "cuotas_estimadas_adicionales": 0,
            "cuotas_estimadas_totales": cuotas_acreditadas,
        }
    )


def _prorratear_salario_proyectado(
    salario_proyectado: float,
    cuotas_disponibles: int,
    cuotas_utilizadas: int,
) -> Decimal:
    """Prorratea un salario anual proyectado por las cuotas consumidas."""

    if (
        cuotas_disponibles <= 0
        or cuotas_utilizadas <= 0
    ):
        return Decimal("0")

    salario = a_decimal(
        salario_proyectado
    )

    return (
        salario
        * Decimal(cuotas_utilizadas)
        / Decimal(cuotas_disponibles)
    )


def _construir_registros_hasta_retiro(
    datos: DatosResultadoSEBDNormal,
    escenario_retiro: EscenarioRetiro,
    escenario_salarial: EscenarioLineaTiempo,
) -> tuple[list[RegistroHistorialSalarial], list[int], bool]:
    """Combina historia real y proyección necesaria hasta el retiro.

    Las cuotas nuevas estimadas por el Paso 5 se consumen cronológicamente
    sobre la capacidad anual de la línea temporal del Paso 4. Si el retiro
    ocurre antes de completar el año, solo se incorpora la fracción salarial
    asociada a las cuotas que efectivamente caben antes de esa fecha.
    """

    anio_actual = datos.linea_tiempo.anio_actual
    anio_retiro = escenario_retiro.fecha_retiro.year

    registros_por_anio: dict[int, RegistroHistorialSalarial] = {}

    for registro in datos.historial.registros:
        if registro.anio > anio_retiro:
            continue

        registros_por_anio[registro.anio] = (
            RegistroHistorialSalarial(
                anio=registro.anio,
                cuotas=registro.cuotas,
                salario_cotizado=registro.salario_cotizado,
            )
        )

    cuotas_nuevas_pendientes = int(
        escenario_retiro.cuotas_estimadas_adicionales
    )

    anios_proyectados: list[int] = []
    hubo_prorrateo = False

    for registro in sorted(
        escenario_salarial.registros,
        key=lambda item: item.anio,
    ):
        if (
            registro.anio < anio_actual
            or registro.anio > anio_retiro
            or cuotas_nuevas_pendientes <= 0
        ):
            continue

        capacidad = int(
            registro.cuotas_proyectadas
        )

        if capacidad <= 0:
            continue

        cuotas_utilizadas = min(
            capacidad,
            cuotas_nuevas_pendientes,
        )

        salario_adicional = (
            _prorratear_salario_proyectado(
                registro.salario_proyectado,
                capacidad,
                cuotas_utilizadas,
            )
        )

        existente = registros_por_anio.get(
            registro.anio
        )

        if existente is None:
            existente = RegistroHistorialSalarial(
                anio=registro.anio,
                cuotas=0,
                salario_cotizado=0.0,
            )

        salario_total = (
            a_decimal(
                existente.salario_cotizado
            )
            + salario_adicional
        )

        registros_por_anio[registro.anio] = (
            RegistroHistorialSalarial(
                anio=registro.anio,
                cuotas=(
                    existente.cuotas
                    + cuotas_utilizadas
                ),
                salario_cotizado=float(
                    redondear_moneda(
                        salario_total
                    )
                ),
            )
        )

        anios_proyectados.append(
            registro.anio
        )

        if cuotas_utilizadas < capacidad:
            hubo_prorrateo = True

        cuotas_nuevas_pendientes -= (
            cuotas_utilizadas
        )

    if cuotas_nuevas_pendientes > 0:
        raise ValueError(
            "La línea temporal salarial no cubre todas las cuotas "
            "estimadas hasta la fecha de retiro seleccionada. Amplía "
            "el horizonte del Paso 4 y vuelve a generar la proyección."
        )

    return (
        sorted(
            registros_por_anio.values(),
            key=lambda item: item.anio,
        ),
        sorted(set(anios_proyectados)),
        hubo_prorrateo,
    )


def _resolver_exceso_por_momento(
    *,
    escenario_retiro: EscenarioRetiro,
    escenario_referencia: EscenarioRetiro,
    cuotas_referencia: int = 240,
) -> tuple[int | None, int | None]:
    """Distribuye el exceso entre antes y después de la referencia.

    Para fechas posteriores a la referencia se usa como frontera el total
    estimado exactamente en la fecha de referencia del Paso 5. Si esa fecha
    ya transcurrió, el análisis actual no permite reconstruir con precisión
    el total histórico a ese día sin información mensual, por lo que no se
    inventa una distribución.
    """

    if (
        escenario_retiro.fecha_retiro
        <= escenario_referencia.fecha_retiro
    ):
        return (
            None,
            None,
        )

    if escenario_referencia.fecha_ya_transcurrida:
        raise ValueError(
            "La edad de referencia ya transcurrió. Para separar con "
            "precisión las cuotas excedentes aportadas antes y después "
            "de esa fecha se necesita detalle histórico mensual. Esta "
            "distribución no se inferirá automáticamente."
        )

    exceso_total = max(
        escenario_retiro.cuotas_estimadas_totales
        - cuotas_referencia,
        0,
    )

    exceso_antes = min(
        max(
            escenario_referencia.cuotas_estimadas_totales
            - cuotas_referencia,
            0,
        ),
        exceso_total,
    )

    exceso_despues = (
        exceso_total
        - exceso_antes
    )

    return (
        exceso_antes,
        exceso_despues,
    )


def calcular_resultado_sebd_normal(
    datos: DatosResultadoSEBDNormal,
) -> ResumenResultadoSEBDNormal:
    """Calcula SEBD normal usando el escenario elegido en el asistente."""

    if not datos.linea_tiempo.escenarios:
        raise ValueError(
            "No existe una línea temporal salarial disponible. "
            "Vuelve al Paso 4 y genera la proyección."
        )

    escenario_retiro = (
        _buscar_escenario_retiro(
            datos
        )
    )

    escenario_retiro = _ajustar_escenario_solo_acreditado(
        datos,
        escenario_retiro,
    )

    if escenario_retiro.fecha_ya_transcurrida:
        raise ValueError(
            "El escenario de retiro seleccionado ya transcurrió. "
            "Con el historial anual actual no se puede reconstruir "
            "con precisión cuántas cuotas estaban acreditadas en esa "
            "fecha. Selecciona una fecha futura o agrega posteriormente "
            "detalle mensual."
        )

    escenario_referencia = (
        _buscar_escenario_referencia(
            datos
        )
    )

    escenario_referencia = _ajustar_escenario_solo_acreditado(
        datos,
        escenario_referencia,
    )

    escenario_salarial = (
        _buscar_escenario_salarial(
            datos
        )
    )

    (
        registros,
        anios_proyectados,
        hubo_prorrateo,
    ) = _construir_registros_hasta_retiro(
        datos,
        escenario_retiro,
        escenario_salarial,
    )

    (
        exceso_antes,
        exceso_despues,
    ) = _resolver_exceso_por_momento(
        escenario_retiro=escenario_retiro,
        escenario_referencia=escenario_referencia,
    )

    calculo = calcular_sebd_normal(
        DatosCalculoSEBDNormal(
            fecha_nacimiento=(
                datos.fecha_nacimiento
            ),
            sexo=datos.sexo,
            fecha_retiro=(
                escenario_retiro.fecha_retiro
            ),
            cuotas_totales=(
                escenario_retiro
                .cuotas_estimadas_totales
            ),
            cuotas_exceso_antes_referencia=(
                exceso_antes
            ),
            cuotas_exceso_despues_referencia=(
                exceso_despues
            ),
            registros=registros,
        )
    )

    advertencias: list[str] = []

    if anios_proyectados:
        advertencias.append(
            "El cálculo incorpora salarios proyectados para los años "
            + ", ".join(
                str(anio)
                for anio in anios_proyectados
            )
            + ". Estos importes son estimaciones, no salarios oficiales "
            "ya acreditados por la CSS."
        )

    if hubo_prorrateo:
        advertencias.append(
            "El salario del último año proyectado se prorrateó según "
            "las cuotas estimadas hasta la fecha de retiro. El detalle "
            "mensual oficial puede producir diferencias."
        )

    return ResumenResultadoSEBDNormal(
        modo_integracion=datos.modo_integracion,
        escenario_retiro=(
            escenario_retiro
        ),
        escenario_salarial_nombre=(
            escenario_salarial.nombre
        ),
        anios_proyectados_incluidos=(
            anios_proyectados
        ),
        advertencias_integracion=(
            advertencias
        ),
        calculo=calculo,
    )
