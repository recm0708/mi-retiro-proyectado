"""Validación del detalle salarial disponible para el año actual.

El servicio separa tres ideas que pueden evolucionar a ritmos distintos:

- salario visible/reportado en la Ficha Digital;
- cuota ya acreditada por la CSS;
- dato parcial o completo del mes.

Esto permite representar, por ejemplo, una primera quincena visible cuando la
segunda todavía no había sido incorporada al momento de una consulta previa.
"""

from decimal import Decimal

from app.core.dinero import a_decimal, redondear_moneda
from app.models.simulacion import (
    DatosDetalleAnioActual,
    RegistroDetalleAnioActualNormalizado,
    ResumenDetalleAnioActual,
)


MESES = {
    1: "01",
    2: "02",
    3: "03",
    4: "04",
    5: "05",
    6: "06",
    7: "07",
    8: "08",
    9: "09",
    10: "10",
    11: "11",
    12: "12",
}


def _mes_iso(anio: int, mes: int) -> str:
    """Devuelve YYYY-MM para un mes ya validado."""

    return f"{anio}-{MESES[mes]}"


def _normalizar_mensual(registro):
    """Normaliza un registro capturado como total mensual."""

    salario = a_decimal(registro.salario_mensual or 0)

    # Un mes sin información debe quedar realmente en cero para no mezclar
    # salarios visibles con cuotas todavía no confirmadas.
    if registro.estado == "SIN_INFORMACION":
        if salario != Decimal("0"):
            raise ValueError(
                f"El mes {registro.mes} tiene salario pero está marcado "
                "como sin información."
            )
        return "SIN_INFORMACION", Decimal("0"), None, None

    if salario <= Decimal("0"):
        raise ValueError(
            f"El mes {registro.mes} debe tener un salario mayor que cero "
            "cuando su estado es parcial o completo."
        )

    return registro.estado, salario, None, None


def _normalizar_quincenal(registro):
    """Deriva total y estado a partir de las quincenas disponibles."""

    primera = a_decimal(registro.primera_quincena or 0)
    segunda = a_decimal(registro.segunda_quincena or 0)
    # La captura quincenal permite registrar meses parciales sin completar la
    # cuota por inferencia; cada quincena se valida por separado.

    if primera < 0 or segunda < 0:
        raise ValueError(
            f"Las quincenas del mes {registro.mes} no pueden ser negativas."
        )

    tiene_primera = primera > 0
    tiene_segunda = segunda > 0

    if not tiene_primera and not tiene_segunda:
        return "SIN_INFORMACION", Decimal("0"), None, None

    total = primera + segunda
    estado = (
        "COMPLETO"
        if tiene_primera and tiene_segunda
        else "PARCIAL"
    )

    return (
        estado,
        total,
        redondear_moneda(primera) if tiene_primera else None,
        redondear_moneda(segunda) if tiene_segunda else None,
    )


def analizar_detalle_anio_actual(
    datos: DatosDetalleAnioActual,
) -> ResumenDetalleAnioActual:
    """Valida el detalle mensual/quincenal y calcula bases sugeridas.

    El total salarial acreditado suma únicamente meses cuya cuota fue marcada
    como ya acreditada. El total salarial disponible puede ser mayor porque
    la Ficha Digital puede reflejar un salario antes de que la cuota asociada
    aparezca acreditada.
    """

    meses = [registro.mes for registro in datos.registros]

    if len(meses) != len(set(meses)):
        raise ValueError(
            "El detalle del año actual contiene meses duplicados."
        )

    # El orden mensual se normaliza antes de acumular totales para que los
    # últimos meses completos y promedios sean cronológicos, no de captura.
    registros_ordenados = sorted(
        datos.registros,
        key=lambda registro: registro.mes,
    )

    normalizados: list[RegistroDetalleAnioActualNormalizado] = []

    total_disponible = Decimal("0")
    total_acreditado = Decimal("0")
    cuotas_identificadas = 0

    completos: list[tuple[int, Decimal]] = []
    ultimo_mes_acreditado: int | None = None

    for registro in registros_ordenados:
        # La normalización convierte ambas modalidades de entrada al mismo
        # contrato de salida: estado, salario total y quincenas opcionales.
        if datos.modo_captura == "MENSUAL":
            estado, salario, primera, segunda = _normalizar_mensual(
                registro
            )
        else:
            estado, salario, primera, segunda = _normalizar_quincenal(
                registro
            )

        if registro.cuota_acreditada:
            # Solo una cuota marcada como acreditada alimenta el total usado
            # para promedio por cuota; el salario visible sigue en otro total.
            cuotas_identificadas += 1
            ultimo_mes_acreditado = registro.mes

            if salario <= Decimal("0"):
                raise ValueError(
                    f"El mes {registro.mes} está marcado con cuota acreditada "
                    "pero no tiene salario disponible."
                )

            total_acreditado += salario

        total_disponible += salario

        if estado == "COMPLETO":
            completos.append((registro.mes, salario))

        normalizados.append(
            RegistroDetalleAnioActualNormalizado(
                mes=registro.mes,
                cuota_acreditada=registro.cuota_acreditada,
                estado=estado,
                salario_total=redondear_moneda(salario),
                primera_quincena=primera,
                segunda_quincena=segunda,
            )
        )

    # Las bases sugeridas se calculan con meses completos para no proyectar
    # ingresos desde un mes parcial o sin segunda quincena.
    salario_ultimo = (
        completos[-1][1]
        if completos
        else None
    )

    promedio_completos = (
        sum((valor for _, valor in completos), start=Decimal("0"))
        / Decimal(len(completos))
        if completos
        else None
    )

    ultimos_tres = completos[-3:]
    promedio_tres = (
        sum((valor for _, valor in ultimos_tres), start=Decimal("0"))
        / Decimal(len(ultimos_tres))
        if ultimos_tres
        else None
    )

    promedio_por_cuota = (
        total_acreditado / Decimal(cuotas_identificadas)
        if cuotas_identificadas > 0
        else None
    )

    ultimo_mes_completo = (
        completos[-1][0]
        if completos
        else None
    )

    return ResumenDetalleAnioActual(
        anio=datos.anio,
        modo_captura=datos.modo_captura,
        cuotas_acreditadas_identificadas=cuotas_identificadas,
        cuotas_coinciden=(
            cuotas_identificadas
            == datos.cuotas_anio_actual_referencia
        ),
        ultimo_mes_cuota_acreditada=(
            _mes_iso(datos.anio, ultimo_mes_acreditado)
            if ultimo_mes_acreditado
            else None
        ),
        ultimo_mes_con_salario_completo=(
            _mes_iso(datos.anio, ultimo_mes_completo)
            if ultimo_mes_completo
            else None
        ),
        total_salario_disponible=redondear_moneda(total_disponible),
        total_salario_acreditado=redondear_moneda(total_acreditado),
        meses_con_informacion=sum(
            1
            for registro in normalizados
            if registro.estado != "SIN_INFORMACION"
        ),
        meses_completos=len(completos),
        salario_ultimo_mes_completo=(
            redondear_moneda(salario_ultimo)
            if salario_ultimo is not None
            else None
        ),
        promedio_meses_completos=(
            redondear_moneda(promedio_completos)
            if promedio_completos is not None
            else None
        ),
        promedio_ultimos_3_meses_completos=(
            redondear_moneda(promedio_tres)
            if promedio_tres is not None
            else None
        ),
        promedio_por_cuota_acreditada=(
            redondear_moneda(promedio_por_cuota)
            if promedio_por_cuota is not None
            else None
        ),
        registros=normalizados,
    )
