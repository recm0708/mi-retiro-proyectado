"""Cálculo general de las modalidades de retiro por vejez del SEBD.

Este módulo extiende el motor normal ya validado y aplica las modalidades
Anticipada, Proporcional y Proporcional Anticipada del artículo 181.
La indemnización por vejez se clasifica, pero su monto queda pendiente de una
subfase propia para evitar mezclar una prestación de pago único con una pensión
mensual.
"""

from decimal import Decimal

from app.core.dinero import a_decimal, redondear_moneda
from app.core.normativa import cargar_parametros_sebd
from app.modelos.pension import (
    AnioSeleccionadoSEBD,
    DatosCalculoSEBD,
    DatosCalculoSEBDNormal,
    ResumenCalculoSEBD,
)
from app.motores.elegibilidad import (
    clasificar_modalidad_sebd,
    meses_desde_limite_anticipado,
)
from app.motores.sebd import (
    _calcular_promedio_mensual,
    _seleccionar_mejores_anios,
    calcular_sebd_normal,
)


def _fuente_normativa() -> str:
    """Devuelve la referencia resumida utilizada por este motor."""

    return (
        "Texto Único de la Ley 51 de 2005, artículos 178-181, 186, "
        "192 y 193, Gaceta Oficial 30284-B de 22/05/2025; "
        "Reglamento para el Cálculo de Prestaciones Económicas, "
        "Resolución 39,302-2007-J.D. y sus modificaciones listadas "
        "por la CSS."
    )


def _convertir_normal(
    datos: DatosCalculoSEBD,
) -> ResumenCalculoSEBD:
    """Convierte la salida del motor normal al modelo general."""

    normal = calcular_sebd_normal(
        DatosCalculoSEBDNormal(
            fecha_nacimiento=datos.fecha_nacimiento,
            sexo=datos.sexo,
            fecha_retiro=datos.fecha_retiro,
            cuotas_totales=datos.cuotas_totales,
            cuotas_exceso_antes_referencia=(
                datos.cuotas_exceso_antes_referencia
            ),
            cuotas_exceso_despues_referencia=(
                datos.cuotas_exceso_despues_referencia
            ),
            registros=datos.registros,
        )
    )

    clasificacion = clasificar_modalidad_sebd(
        datos.fecha_nacimiento,
        datos.sexo,
        datos.fecha_retiro,
        datos.cuotas_totales,
    )

    return ResumenCalculoSEBD(
        modalidad="NORMAL",
        modalidad_nombre="Pensión de Retiro por Vejez Normal",
        tipo_prestacion="PENSION",
        elegible=normal.elegible,
        calculo_disponible=True,
        motivos_no_elegible=normal.motivos_no_elegible,
        edad_retiro_anios=normal.edad_retiro_anios,
        edad_referencia=normal.edad_referencia,
        fecha_referencia=normal.fecha_referencia,
        fecha_minima_anticipada=clasificacion["fecha_minima_anticipada"],
        cuotas_referencia=normal.cuotas_referencia,
        cuotas_minimas_proporcional=int(
            cargar_parametros_sebd()["pension_vejez"]
            ["cuotas_minimas_proporcional"]
        ),
        cuotas_totales=normal.cuotas_totales,
        cuotas_exceso_total=normal.cuotas_exceso_total,
        cuotas_exceso_antes_referencia=(
            normal.cuotas_exceso_antes_referencia
        ),
        cuotas_exceso_despues_referencia=(
            normal.cuotas_exceso_despues_referencia
        ),
        mejores_anios_requeridos=normal.mejores_anios_requeridos,
        anios_seleccionados=normal.anios_seleccionados,
        total_salarios_seleccionados=(
            normal.total_salarios_seleccionados
        ),
        salario_base_mensual=normal.salario_base_mensual,
        tasa_base_pct=normal.tasa_base_pct,
        bloques_12_antes_referencia=(
            normal.bloques_12_antes_referencia
        ),
        incremento_antes_referencia_pct=(
            normal.incremento_antes_referencia_pct
        ),
        bloques_12_despues_referencia=(
            normal.bloques_12_despues_referencia
        ),
        incremento_despues_referencia_pct=(
            normal.incremento_despues_referencia_pct
        ),
        tasa_reemplazo_total_pct=(
            normal.tasa_reemplazo_total_pct
        ),
        monto_antes_limite_maximo=(
            normal.monto_antes_limite_maximo
        ),
        monto_maximo_aplicable=normal.monto_maximo_aplicable,
        monto_despues_limite_maximo=(
            normal.pension_mensual_estimada
        ),
        factor_proporcional_cuotas=1.0,
        factor_reduccion_edad=1.0,
        meses_desde_limite_anticipado=None,
        meses_anticipacion_referencia=0,
        monto_despues_factor_proporcional=(
            normal.pension_mensual_estimada
        ),
        pension_mensual_estimada=(
            normal.pension_mensual_estimada
        ),
        minimo_indexado_aplicado=(
            normal.minimo_indexado_aplicado
        ),
        advertencias=normal.advertencias,
        fuente_normativa=_fuente_normativa(),
    )


def _factor_reduccion_anticipado(
    datos: DatosCalculoSEBD,
) -> tuple[Decimal, int, int]:
    """Obtiene el factor de reducción mensual dentro de la banda anticipada."""

    parametros = cargar_parametros_sebd()["pension_vejez"]
    configuracion = parametros["retiro_anticipado"]
    tabla = configuracion[
        "tabla_factor_reduccion_meses_desde_limite_inferior"
    ]

    meses_desde_limite = meses_desde_limite_anticipado(
        datos.fecha_nacimiento,
        datos.sexo,
        datos.fecha_retiro,
    )

    if str(meses_desde_limite) not in tabla:
        raise ValueError(
            "La fecha anticipada no corresponde a un mes completo de la "
            "tabla de reducción vigente o está fuera de la banda permitida."
        )

    maximo_meses = int(
        configuracion["maximo_meses_anticipacion"]
    )

    meses_anticipacion = max(
        maximo_meses - meses_desde_limite,
        1,
    )

    return (
        a_decimal(tabla[str(meses_desde_limite)]),
        meses_desde_limite,
        meses_anticipacion,
    )


def _resultado_sin_calculo(
    datos: DatosCalculoSEBD,
    clasificacion: dict,
) -> ResumenCalculoSEBD:
    """Construye una salida explicable para indemnización o no elegibilidad."""

    parametros = cargar_parametros_sebd()["pension_vejez"]
    exceso = max(
        datos.cuotas_totales - int(parametros["cuotas_referencia"]),
        0,
    )

    advertencias = list(
        clasificacion.get("advertencias", [])
    )

    if clasificacion["modalidad"] == "INDEMNIZACION":
        advertencias.append(
            "La indemnización por vejez es una prestación de pago único. "
            "Su cálculo monetario se implementará en una subfase específica."
        )

    return ResumenCalculoSEBD(
        modalidad=clasificacion["modalidad"],
        modalidad_nombre=clasificacion["modalidad_nombre"],
        tipo_prestacion=clasificacion["tipo_prestacion"],
        elegible=clasificacion["elegible"],
        calculo_disponible=False,
        motivos_no_elegible=list(
            clasificacion.get("motivos", [])
        ),
        edad_retiro_anios=clasificacion["edad_retiro_anios"],
        edad_referencia=clasificacion["edad_referencia"],
        fecha_referencia=clasificacion["fecha_referencia"],
        fecha_minima_anticipada=clasificacion["fecha_minima_anticipada"],
        cuotas_referencia=clasificacion["cuotas_referencia"],
        cuotas_minimas_proporcional=(
            clasificacion["cuotas_minimas_proporcional"]
        ),
        cuotas_totales=datos.cuotas_totales,
        cuotas_exceso_total=exceso,
        cuotas_exceso_antes_referencia=0,
        cuotas_exceso_despues_referencia=0,
        mejores_anios_requeridos=0,
        anios_seleccionados=[],
        total_salarios_seleccionados=0.0,
        salario_base_mensual=0.0,
        tasa_base_pct=float(parametros["tasa_reemplazo_base_pct"]),
        bloques_12_antes_referencia=0,
        incremento_antes_referencia_pct=0.0,
        bloques_12_despues_referencia=0,
        incremento_despues_referencia_pct=0.0,
        tasa_reemplazo_total_pct=0.0,
        monto_antes_limite_maximo=0.0,
        monto_maximo_aplicable=float(
            parametros["montos_maximos_sebd"]["ordinario"]["monto_maximo"]
        ),
        monto_despues_limite_maximo=0.0,
        factor_proporcional_cuotas=0.0,
        factor_reduccion_edad=0.0,
        meses_desde_limite_anticipado=None,
        meses_anticipacion_referencia=0,
        monto_despues_factor_proporcional=0.0,
        pension_mensual_estimada=None,
        minimo_indexado_aplicado=False,
        advertencias=advertencias,
        fuente_normativa=_fuente_normativa(),
    )


def calcular_sebd(
    datos: DatosCalculoSEBD,
) -> ResumenCalculoSEBD:
    """Clasifica y calcula la modalidad general de retiro por vejez SEBD."""

    clasificacion = clasificar_modalidad_sebd(
        datos.fecha_nacimiento,
        datos.sexo,
        datos.fecha_retiro,
        datos.cuotas_totales,
    )

    if clasificacion["modalidad"] == "NORMAL":
        return _convertir_normal(datos)

    if clasificacion["modalidad"] in {
        "INDEMNIZACION",
        "NO_ELEGIBLE",
    }:
        return _resultado_sin_calculo(
            datos,
            clasificacion,
        )

    parametros = cargar_parametros_sebd()["pension_vejez"]
    cuotas_referencia = int(parametros["cuotas_referencia"])

    datos_base = DatosCalculoSEBDNormal(
        fecha_nacimiento=datos.fecha_nacimiento,
        sexo=datos.sexo,
        fecha_retiro=datos.fecha_retiro,
        cuotas_totales=datos.cuotas_totales,
        registros=datos.registros,
    )

    cantidad = int(parametros["mejores_anios_base"])
    seleccion = _seleccionar_mejores_anios(
        datos_base,
        cantidad,
    )
    salario_base = _calcular_promedio_mensual(
        seleccion,
    )

    total_salarios = sum(
        (
            a_decimal(registro.salario_cotizado)
            for registro in seleccion
        ),
        Decimal("0"),
    )

    tasa_base = a_decimal(
        parametros["tasa_reemplazo_base_pct"]
    )
    tasa_total = tasa_base

    exceso_total = max(
        datos.cuotas_totales - cuotas_referencia,
        0,
    )
    exceso_antes = 0
    bloques_antes = 0
    incremento_antes = Decimal("0")

    if clasificacion["modalidad"] == "ANTICIPADA":
        exceso_antes = exceso_total
        bloques_antes = exceso_antes // 12
        incremento_antes = (
            Decimal(bloques_antes)
            * a_decimal(
                parametros[
                    "incremento_12_cuotas_antes_referencia_pct"
                ]
            )
        )
        tasa_total += incremento_antes

    monto_antes_maximo = (
        salario_base
        * tasa_total
        / Decimal("100")
    )

    monto_maximo = a_decimal(
        parametros["montos_maximos_sebd"]["ordinario"]["monto_maximo"]
    )
    monto_limitado = min(
        monto_antes_maximo,
        monto_maximo,
    )

    factor_proporcional = Decimal("1")

    if clasificacion["modalidad"] in {
        "PROPORCIONAL",
        "PROPORCIONAL_ANTICIPADA",
    }:
        factor_proporcional = (
            Decimal(datos.cuotas_totales)
            / Decimal(cuotas_referencia)
        )

    monto_proporcional = (
        monto_limitado
        * factor_proporcional
    )

    factor_edad = Decimal("1")
    meses_desde_limite = None
    meses_anticipacion = 0

    if clasificacion["modalidad"] in {
        "ANTICIPADA",
        "PROPORCIONAL_ANTICIPADA",
    }:
        (
            factor_edad,
            meses_desde_limite,
            meses_anticipacion,
        ) = _factor_reduccion_anticipado(datos)

    monto_final = (
        monto_proporcional
        * factor_edad
    )

    advertencias = list(
        clasificacion.get("advertencias", [])
    )

    if clasificacion["modalidad"] in {
        "ANTICIPADA",
        "PROPORCIONAL",
        "PROPORCIONAL_ANTICIPADA",
    }:
        advertencias.append(
            "La Ley permite que esta modalidad quede por debajo del mínimo general de pensión; no se eleva automáticamente al mínimo indexado."
        )

    if clasificacion["modalidad"] in {
        "ANTICIPADA",
        "PROPORCIONAL_ANTICIPADA",
    }:
        advertencias.append(
            "El factor de reducción se determina por mes completo dentro de la banda anticipada según la tabla reglamentaria versionada."
        )

    return ResumenCalculoSEBD(
        modalidad=clasificacion["modalidad"],
        modalidad_nombre=clasificacion["modalidad_nombre"],
        tipo_prestacion=clasificacion["tipo_prestacion"],
        elegible=True,
        calculo_disponible=True,
        motivos_no_elegible=[],
        edad_retiro_anios=clasificacion["edad_retiro_anios"],
        edad_referencia=clasificacion["edad_referencia"],
        fecha_referencia=clasificacion["fecha_referencia"],
        fecha_minima_anticipada=clasificacion["fecha_minima_anticipada"],
        cuotas_referencia=cuotas_referencia,
        cuotas_minimas_proporcional=(
            clasificacion["cuotas_minimas_proporcional"]
        ),
        cuotas_totales=datos.cuotas_totales,
        cuotas_exceso_total=exceso_total,
        cuotas_exceso_antes_referencia=exceso_antes,
        cuotas_exceso_despues_referencia=0,
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
        total_salarios_seleccionados=redondear_moneda(total_salarios),
        salario_base_mensual=redondear_moneda(salario_base),
        tasa_base_pct=float(tasa_base),
        bloques_12_antes_referencia=bloques_antes,
        incremento_antes_referencia_pct=float(incremento_antes),
        bloques_12_despues_referencia=0,
        incremento_despues_referencia_pct=0.0,
        tasa_reemplazo_total_pct=float(tasa_total),
        monto_antes_limite_maximo=redondear_moneda(monto_antes_maximo),
        monto_maximo_aplicable=redondear_moneda(monto_maximo),
        monto_despues_limite_maximo=redondear_moneda(monto_limitado),
        factor_proporcional_cuotas=float(factor_proporcional),
        factor_reduccion_edad=float(factor_edad),
        meses_desde_limite_anticipado=meses_desde_limite,
        meses_anticipacion_referencia=meses_anticipacion,
        monto_despues_factor_proporcional=redondear_moneda(
            monto_proporcional
        ),
        pension_mensual_estimada=redondear_moneda(monto_final),
        minimo_indexado_aplicado=False,
        advertencias=advertencias,
        fuente_normativa=_fuente_normativa(),
    )
