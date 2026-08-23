"""Motor del Subsistema Exclusivamente de Beneficio Definido (SEBD).

La primera versión implementa la Pensión de Retiro por Vejez Normal
de acuerdo con los artículos 178 a 181 y 193 del Texto Único de la
Ley 51 de 2005 con las reformas incluidas en la Gaceta Oficial
30284-B de 22 de mayo de 2025.

El monto mínimo indexado del artículo 192 se mantiene pendiente de
versionar para cada fecha de cálculo. El motor sí aplica los límites
máximos del artículo 193 cuando corresponden.
"""

from decimal import Decimal

from app.core.dinero import (
    a_decimal,
    redondear_moneda,
)
from app.core.normativa import (
    cargar_parametros_sebd,
    obtener_edad_referencia,
)
from app.models.pension import (
    AnioSeleccionadoSEBD,
    DatosCalculoSEBDNormal,
    ResumenCalculoSEBDNormal,
)
from app.engines.elegibilidad import (
    calcular_edad_cumplida,
    evaluar_elegibilidad_sebd_normal,
    fecha_edad_referencia,
)


def _seleccionar_mejores_anios(
    datos: DatosCalculoSEBDNormal,
    cantidad: int,
) -> list:
    """Selecciona los años con mayor salario cotizado hasta el retiro."""

    registros_validos = [
        registro
        for registro in datos.registros
        if (
            registro.anio
            <= datos.fecha_retiro.year
            and registro.salario_cotizado > 0
        )
    ]

    if len(registros_validos) < cantidad:
        raise ValueError(
            "No existen suficientes años con salario cotizado para "
            f"formar una base de {cantidad} años."
        )

    seleccion = sorted(
        registros_validos,
        key=lambda registro: (
            registro.salario_cotizado,
            registro.anio,
        ),
        reverse=True,
    )[:cantidad]

    return sorted(
        seleccion,
        key=lambda registro: registro.anio,
    )


def _calcular_promedio_mensual(
    registros: list,
) -> Decimal:
    """Calcula el promedio mensual sin redondeos intermedios."""

    total = sum(
        (
            a_decimal(
                registro.salario_cotizado
            )
            for registro in registros
        ),
        Decimal("0"),
    )

    meses = Decimal(
        len(registros) * 12
    )

    return total / meses


def _determinar_base_y_maximo(
    datos: DatosCalculoSEBDNormal,
    parametros: dict,
) -> tuple[list, Decimal, Decimal]:
    """Determina la base salarial y el límite máximo aplicable."""

    limites = parametros[
        "montos_maximos_sebd"
    ]

    # Primero se evalúa el nivel más alto porque sus condiciones
    # son más exigentes.
    candidatos = [
        limites["ampliado_2500"],
        limites["ampliado_2000"],
    ]

    for candidato in candidatos:
        cuotas_minimas = int(
            candidato[
                "cuotas_minimas"
            ]
        )

        if datos.cuotas_totales < cuotas_minimas:
            continue

        cantidad = int(
            candidato[
                "mejores_anios_base"
            ]
        )

        try:
            seleccion = _seleccionar_mejores_anios(
                datos,
                cantidad,
            )
        except ValueError:
            continue

        promedio = _calcular_promedio_mensual(
            seleccion,
        )

        minimo_promedio = a_decimal(
            candidato[
                "promedio_mensual_minimo"
            ]
        )

        if promedio >= minimo_promedio:
            return (
                seleccion,
                promedio,
                a_decimal(
                    candidato[
                        "monto_maximo"
                    ]
                ),
            )

    ordinario = limites[
        "ordinario"
    ]

    cantidad = int(
        ordinario[
            "mejores_anios_base"
        ]
    )

    seleccion = _seleccionar_mejores_anios(
        datos,
        cantidad,
    )

    promedio = _calcular_promedio_mensual(
        seleccion,
    )

    return (
        seleccion,
        promedio,
        a_decimal(
            ordinario[
                "monto_maximo"
            ]
        ),
    )


def _resolver_cuotas_exceso(
    datos: DatosCalculoSEBDNormal,
    cuotas_referencia: int,
) -> tuple[int, int, int]:
    """Resuelve la distribución de cuotas excedentes por momento."""

    exceso_total = max(
        datos.cuotas_totales
        - cuotas_referencia,
        0,
    )

    fecha_referencia = fecha_edad_referencia(
        datos.fecha_nacimiento,
        datos.sexo,
    )

    antes = datos.cuotas_exceso_antes_referencia
    despues = datos.cuotas_exceso_despues_referencia

    if antes is None and despues is None:
        # Si el retiro ocurre en la fecha de referencia o antes,
        # todas las cuotas excedentes existentes son necesariamente
        # anteriores a esa fecha.
        if datos.fecha_retiro <= fecha_referencia:
            return (
                exceso_total,
                0,
                exceso_total,
            )

        raise ValueError(
            "Para retiros posteriores a la edad de referencia se debe "
            "indicar cuántas cuotas excedentes fueron aportadas antes "
            "y después de alcanzarla."
        )

    antes = int(antes or 0)
    despues = int(despues or 0)

    if antes + despues != exceso_total:
        raise ValueError(
            "La suma de cuotas excedentes antes y después de la edad "
            "de referencia debe coincidir con el exceso total de cuotas."
        )

    return (
        antes,
        despues,
        exceso_total,
    )


def calcular_sebd_normal(
    datos: DatosCalculoSEBDNormal,
) -> ResumenCalculoSEBDNormal:
    """Calcula la Pensión de Retiro por Vejez Normal del SEBD."""

    parametros_raiz = cargar_parametros_sebd()
    parametros = parametros_raiz[
        "pension_vejez"
    ]

    cuotas_referencia = int(
        parametros[
            "cuotas_referencia"
        ]
    )

    elegible, motivos = evaluar_elegibilidad_sebd_normal(
        fecha_nacimiento=datos.fecha_nacimiento,
        sexo=datos.sexo,
        fecha_retiro=datos.fecha_retiro,
        cuotas_totales=datos.cuotas_totales,
    )

    edad_referencia = obtener_edad_referencia(
        datos.sexo,
    )

    fecha_referencia = fecha_edad_referencia(
        datos.fecha_nacimiento,
        datos.sexo,
    )

    edad_retiro = calcular_edad_cumplida(
        datos.fecha_nacimiento,
        datos.fecha_retiro,
    )

    antes, despues, exceso_total = _resolver_cuotas_exceso(
        datos,
        cuotas_referencia,
    )

    seleccion, salario_base, monto_maximo = _determinar_base_y_maximo(
        datos,
        parametros,
    )

    tasa_base = a_decimal(
        parametros[
            "tasa_reemplazo_base_pct"
        ]
    )

    incremento_antes_por_bloque = a_decimal(
        parametros[
            "incremento_12_cuotas_antes_referencia_pct"
        ]
    )

    incremento_despues_por_bloque = a_decimal(
        parametros[
            "incremento_12_cuotas_despues_referencia_pct"
        ]
    )

    bloques_antes = antes // 12
    bloques_despues = despues // 12

    incremento_antes = (
        Decimal(bloques_antes)
        * incremento_antes_por_bloque
    )

    incremento_despues = (
        Decimal(bloques_despues)
        * incremento_despues_por_bloque
    )

    tasa_total = (
        tasa_base
        + incremento_antes
        + incremento_despues
    )

    monto_antes_maximo = (
        salario_base
        * tasa_total
        / Decimal("100")
    )

    monto_final = min(
        monto_antes_maximo,
        monto_maximo,
    )

    total_salarios = sum(
        (
            a_decimal(
                registro.salario_cotizado
            )
            for registro in seleccion
        ),
        Decimal("0"),
    )

    advertencias: list[str] = []

    minimo_base = a_decimal(
        parametros[
            "monto_minimo_base"
        ]["valor"]
    )

    if monto_final < minimo_base:
        advertencias.append(
            "El resultado está por debajo del monto mínimo base del "
            "artículo 192. El mínimo indexado aplicable a la fecha de "
            "retiro aún no se ha versionado, por lo que no se eleva "
            "automáticamente este resultado."
        )

    if not elegible:
        advertencias.append(
            "El desglose matemático se muestra con fines de validación, "
            "pero la persona no cumple todavía los requisitos de la "
            "modalidad normal del SEBD."
        )

    return ResumenCalculoSEBDNormal(
        modalidad="PENSION_VEJEZ_NORMAL_SEBD",
        elegible=elegible,
        motivos_no_elegible=motivos,
        edad_retiro_anios=edad_retiro,
        edad_referencia=edad_referencia,
        fecha_referencia=fecha_referencia,
        cuotas_referencia=cuotas_referencia,
        cuotas_totales=datos.cuotas_totales,
        cuotas_exceso_total=exceso_total,
        cuotas_exceso_antes_referencia=antes,
        cuotas_exceso_despues_referencia=despues,
        mejores_anios_requeridos=len(seleccion),
        anios_seleccionados=[
            AnioSeleccionadoSEBD(
                anio=registro.anio,
                cuotas=registro.cuotas,
                salario_cotizado=redondear_moneda(
                    registro.salario_cotizado
                ),
            )
            for registro in seleccion
        ],
        total_salarios_seleccionados=redondear_moneda(
            total_salarios
        ),
        salario_base_mensual=redondear_moneda(
            salario_base
        ),
        tasa_base_pct=float(tasa_base),
        bloques_12_antes_referencia=bloques_antes,
        incremento_antes_referencia_pct=float(
            incremento_antes
        ),
        bloques_12_despues_referencia=bloques_despues,
        incremento_despues_referencia_pct=float(
            incremento_despues
        ),
        tasa_reemplazo_total_pct=float(
            tasa_total
        ),
        monto_antes_limite_maximo=redondear_moneda(
            monto_antes_maximo
        ),
        monto_maximo_aplicable=redondear_moneda(
            monto_maximo
        ),
        pension_mensual_estimada=redondear_moneda(
            monto_final
        ),
        minimo_indexado_aplicado=False,
        advertencias=advertencias,
        fuente_normativa=(
            "Texto Único de la Ley 51 de 2005, artículos 178-181 "
            "y 193, Gaceta Oficial 30284-B de 22/05/2025."
        ),
    )
