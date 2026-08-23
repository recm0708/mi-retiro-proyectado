"""Motor de prestaciones por vejez del Subsistema Mixto.

La subfase 6D.2 amplía el motor preliminar con tres elementos que deben
permanecer explícitamente separados:

- Pensión programada del Componente de Ahorro Personal (CAP).
- Opción de devolución total del CAP cuando procede el artículo 187.
- Garantía de continuidad del CAP mediante el Seguro Colectivo de Renta
  Vitalicia cuando se agoten los fondos después de sobrevivir la expectativa
  de vida usada en el cálculo.

El motor tampoco reconstruye el saldo CAP ni el bono de reconocimiento a
partir de salarios anuales. Esos importes deben provenir de información
oficial o de una entrada identificada como tal. Cuando el artículo 187 permite
más de una alternativa, ``AUTO`` no toma la decisión por el Asegurado(a).
"""

from calendar import monthrange
from datetime import date
from decimal import Decimal

from app.core.dinero import a_decimal, redondear_moneda
from app.core.normativa import cargar_parametros_mixto, obtener_edad_referencia
from app.models.pension import (
    AnioSeleccionadoMixtoBD,
    DatosCalculoMixto,
    DatosCalculoSEBD,
    ResumenCalculoMixto,
    ResumenComponenteAhorroPersonalMixto,
    ResumenComponenteBeneficioDefinidoMixto,
)
from app.models.simulacion import RegistroHistorialSalarial
from app.engines.sebd_modalidades import calcular_sebd


def _fuente_normativa() -> str:
    """Devuelve la referencia normativa resumida del Subsistema Mixto."""

    return (
        "Texto Único de la Ley 51 de 2005, artículos 155, 178-188, "
        "192 y 193, Gaceta Oficial 30284-B de 22/05/2025; "
        "Reglamento de Incorporación al Componente Contributivo de "
        "Capitalización Solidaria, Resolución 57,805-2025-J.D.; "
        "Reglamento de Seguros Colectivos del Componente de Ahorro "
        "Personal del Subsistema Mixto, Resolución 41,055-2009-J.D."
    )


def _sumar_anios(fecha: date, cantidad: int) -> date:
    """Suma años preservando el día cuando exista en el año destino."""

    nuevo_anio = fecha.year + cantidad
    ultimo_dia = monthrange(nuevo_anio, fecha.month)[1]
    return date(
        nuevo_anio,
        fecha.month,
        min(fecha.day, ultimo_dia),
    )


def _fecha_referencia(datos: DatosCalculoMixto) -> date:
    """Obtiene la fecha de edad de referencia del Asegurado(a)."""

    return _sumar_anios(
        datos.fecha_nacimiento,
        obtener_edad_referencia(datos.sexo),
    )


def _construir_historial_bd(
    datos: DatosCalculoMixto,
    salario_mensual_maximo: Decimal,
) -> tuple[list[RegistroHistorialSalarial], bool]:
    """Construye el historial anual utilizable por el componente definido.

    Con datos anuales no es posible reproducir con exactitud el tope mensual
    de B/.500.00 cuando dentro de un mismo año hubo salarios variables. Como
    aproximación se conserva hasta ``500 × cuotas`` por año.
    """

    registros: list[RegistroHistorialSalarial] = []
    hubo_tope_anual = False

    for registro in datos.registros:
        salario_original = a_decimal(registro.salario_cotizado)
        tope_anual = salario_mensual_maximo * Decimal(registro.cuotas)
        salario_bd = min(salario_original, tope_anual)

        if salario_bd < salario_original:
            hubo_tope_anual = True

        registros.append(
            RegistroHistorialSalarial(
                anio=registro.anio,
                cuotas=registro.cuotas,
                salario_cotizado=redondear_moneda(salario_bd),
            )
        )

    return registros, hubo_tope_anual


def _anios_bd_desde_calculo(
    datos: DatosCalculoMixto,
    calculo_base,
) -> list[AnioSeleccionadoMixtoBD]:
    """Convierte los años seleccionados del motor SEBD al formato Mixto."""

    seleccion_original = {
        registro.anio: registro
        for registro in datos.registros
    }

    return [
        AnioSeleccionadoMixtoBD(
            anio=registro.anio,
            cuotas=registro.cuotas,
            salario_cotizado_original=redondear_moneda(
                seleccion_original[registro.anio].salario_cotizado
            ),
            salario_considerado_bd=redondear_moneda(
                registro.salario_cotizado
            ),
        )
        for registro in calculo_base.anios_seleccionados
        if registro.anio in seleccion_original
    ]


def _calcular_componente_bd(
    datos: DatosCalculoMixto,
    parametros: dict,
) -> ResumenComponenteBeneficioDefinidoMixto:
    """Calcula pensión o indemnización del componente definido del Mixto."""

    configuracion = parametros["componente_beneficio_definido"]
    maximo_salarial = a_decimal(
        configuracion["salario_mensual_maximo_participacion"]
    )
    maximo_componente = a_decimal(
        configuracion["monto_maximo_mensual"]
    )

    historial_bd, hubo_aproximacion = _construir_historial_bd(
        datos,
        maximo_salarial,
    )

    calculo_base = calcular_sebd(
        DatosCalculoSEBD(
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
            registros=historial_bd,
        )
    )

    advertencias: list[str] = []

    if hubo_aproximacion:
        advertencias.append(
            "El tope de B/.500.00 es mensual. Como el historial disponible "
            "es anual, la aplicación aproxima el máximo del año como "
            "B/.500.00 por cada cuota registrada. El detalle mensual oficial "
            "puede modificar la base exacta."
        )

    anios = _anios_bd_desde_calculo(
        datos,
        calculo_base,
    )

    if calculo_base.tipo_prestacion == "INDEMNIZACION":
        advertencias.extend(calculo_base.advertencias)
        advertencias.append(
            "La indemnización del componente definido es un pago único y "
            "se mantiene separada de cualquier devolución del CAP."
        )

        return ResumenComponenteBeneficioDefinidoMixto(
            modalidad=calculo_base.modalidad,
            modalidad_nombre=calculo_base.modalidad_nombre,
            tipo_prestacion="INDEMNIZACION",
            elegible=calculo_base.elegible,
            calculo_disponible=calculo_base.calculo_disponible,
            salario_mensual_maximo_participacion=redondear_moneda(
                maximo_salarial
            ),
            anios_seleccionados=anios,
            total_salarios_considerados=redondear_moneda(
                calculo_base.total_salarios_seleccionados
            ),
            salario_base_mensual=redondear_moneda(
                calculo_base.salario_base_mensual
            ),
            tasa_base_pct=calculo_base.tasa_base_pct,
            incremento_antes_referencia_pct=0.0,
            incremento_despues_referencia_pct=0.0,
            tasa_reemplazo_total_pct=calculo_base.tasa_reemplazo_total_pct,
            factor_proporcional_cuotas=None,
            factor_reduccion_edad=1.0,
            monto_antes_maximo=redondear_moneda(
                calculo_base.monto_antes_limite_maximo
            ),
            monto_maximo_componente=redondear_moneda(maximo_componente),
            pension_mensual_estimada=None,
            indemnizacion_mensualidad_hipotetica=(
                calculo_base.indemnizacion_mensualidad_hipotetica
            ),
            indemnizacion_pago_unico_estimado=(
                calculo_base.indemnizacion_pago_unico_estimado
            ),
            usa_aproximacion_anual_tope_mensual=hubo_aproximacion,
            advertencias=advertencias,
        )

    if calculo_base.tipo_prestacion != "PENSION":
        advertencias.extend(calculo_base.advertencias)

        return ResumenComponenteBeneficioDefinidoMixto(
            modalidad=calculo_base.modalidad,
            modalidad_nombre=calculo_base.modalidad_nombre,
            tipo_prestacion=calculo_base.tipo_prestacion,
            elegible=calculo_base.elegible,
            calculo_disponible=False,
            salario_mensual_maximo_participacion=redondear_moneda(
                maximo_salarial
            ),
            anios_seleccionados=anios,
            total_salarios_considerados=redondear_moneda(
                calculo_base.total_salarios_seleccionados
            ),
            salario_base_mensual=redondear_moneda(
                calculo_base.salario_base_mensual
            ),
            tasa_base_pct=calculo_base.tasa_base_pct,
            incremento_antes_referencia_pct=0.0,
            incremento_despues_referencia_pct=0.0,
            tasa_reemplazo_total_pct=0.0,
            factor_proporcional_cuotas=None,
            factor_reduccion_edad=1.0,
            monto_antes_maximo=0.0,
            monto_maximo_componente=redondear_moneda(maximo_componente),
            pension_mensual_estimada=None,
            usa_aproximacion_anual_tope_mensual=hubo_aproximacion,
            advertencias=advertencias,
        )

    # El motor SEBD determina modalidad, tasa, factor proporcional y factor
    # de edad. Se recalcula el límite porque el BD del Mixto tiene máximo 500.
    monto_antes_maximo = a_decimal(
        calculo_base.monto_antes_limite_maximo
    )
    monto_limitado = min(
        monto_antes_maximo,
        maximo_componente,
    )

    factor_proporcional = (
        a_decimal(calculo_base.factor_proporcional_cuotas)
        if calculo_base.factor_proporcional_cuotas is not None
        else Decimal("1")
    )
    factor_edad = a_decimal(
        calculo_base.factor_reduccion_edad
    )

    pension = monto_limitado * factor_proporcional * factor_edad

    if (
        calculo_base.modalidad == "NORMAL"
        and pension
        < a_decimal(configuracion["monto_minimo_base_no_indexado"])
    ):
        advertencias.append(
            "El componente definido calculado queda por debajo del mínimo "
            "base de B/.265.00. El valor mínimo indexado vigente por fecha "
            "todavía no está versionado y no se eleva automáticamente."
        )

    return ResumenComponenteBeneficioDefinidoMixto(
        modalidad=calculo_base.modalidad,
        modalidad_nombre=calculo_base.modalidad_nombre,
        tipo_prestacion="PENSION",
        elegible=calculo_base.elegible,
        calculo_disponible=calculo_base.calculo_disponible,
        salario_mensual_maximo_participacion=redondear_moneda(maximo_salarial),
        anios_seleccionados=anios,
        total_salarios_considerados=redondear_moneda(
            calculo_base.total_salarios_seleccionados
        ),
        salario_base_mensual=redondear_moneda(
            calculo_base.salario_base_mensual
        ),
        tasa_base_pct=calculo_base.tasa_base_pct,
        incremento_antes_referencia_pct=(
            calculo_base.incremento_antes_referencia_pct
        ),
        incremento_despues_referencia_pct=(
            calculo_base.incremento_despues_referencia_pct
        ),
        tasa_reemplazo_total_pct=calculo_base.tasa_reemplazo_total_pct,
        factor_proporcional_cuotas=calculo_base.factor_proporcional_cuotas,
        factor_reduccion_edad=calculo_base.factor_reduccion_edad,
        monto_antes_maximo=redondear_moneda(monto_antes_maximo),
        monto_maximo_componente=redondear_moneda(maximo_componente),
        pension_mensual_estimada=redondear_moneda(pension),
        indemnizacion_mensualidad_hipotetica=None,
        indemnizacion_pago_unico_estimado=None,
        usa_aproximacion_anual_tope_mensual=hubo_aproximacion,
        advertencias=advertencias,
    )


def _resumen_cap_vacio(
    datos: DatosCalculoMixto,
    *,
    saldo: Decimal | None,
    bono: Decimal,
    capital: Decimal | None,
    valor_actuarial: Decimal | None,
    devolucion_disponible: bool,
    decision_requerida: bool,
    advertencias: list[str],
) -> ResumenComponenteAhorroPersonalMixto:
    """Construye una salida CAP sin prestación calculada."""

    parametros = cargar_parametros_mixto()
    prima = parametros["seguros_colectivos"]["prima_renta_vitalicia_pct_historica"]

    return ResumenComponenteAhorroPersonalMixto(
        calculo_disponible=False,
        saldo_ahorro_personal=(
            redondear_moneda(saldo)
            if saldo is not None
            else None
        ),
        bono_reconocimiento=redondear_moneda(bono),
        bono_reconocimiento_confirmado_oficialmente=(
            datos.bono_reconocimiento_confirmado_oficialmente
        ),
        capital_total_considerado=(
            redondear_moneda(capital)
            if capital is not None
            else None
        ),
        valor_actuarial_expectativa_vida=(
            float(valor_actuarial)
            if valor_actuarial is not None
            else None
        ),
        opcion_solicitada=datos.opcion_prestacion_cap,
        decision_requerida=decision_requerida,
        pension_programada_mensual=None,
        devolucion_total_disponible=devolucion_disponible,
        devolucion_pago_unico_estimado=None,
        garantia_renta_vitalicia_aplica=False,
        garantia_monto_mensual=None,
        garantia_condicion_activacion=None,
        prima_renta_vitalicia_pct_referencia=float(prima),
        prima_renta_vitalicia_es_referencia_historica=True,
        monto_maximo_aplicable=None,
        advertencias=advertencias,
    )


def _calcular_componente_cap(
    datos: DatosCalculoMixto,
    componente_bd: ResumenComponenteBeneficioDefinidoMixto,
    parametros: dict,
) -> ResumenComponenteAhorroPersonalMixto:
    """Calcula pensión programada o devolución total del CAP."""

    advertencias: list[str] = []

    saldo = (
        a_decimal(datos.saldo_ahorro_personal)
        if datos.saldo_ahorro_personal is not None
        else None
    )
    bono = a_decimal(datos.bono_reconocimiento)
    valor_actuarial = (
        a_decimal(datos.valor_actuarial_expectativa_vida)
        if datos.valor_actuarial_expectativa_vida is not None
        else None
    )
    capital = (
        saldo + bono
        if saldo is not None
        else None
    )

    fecha_referencia = _fecha_referencia(datos)
    devolucion_disponible = (
        datos.fecha_retiro >= fecha_referencia
        and datos.cuotas_totales < int(
            parametros["componente_beneficio_definido"]["cuotas_referencia"]
        )
    )

    if bono > 0 and not datos.bono_reconocimiento_confirmado_oficialmente:
        advertencias.append(
            "Se ingresó un bono de reconocimiento no marcado como monto "
            "oficialmente confirmado. La aplicación no calcula por sí sola "
            "el bono del artículo 183; el resultado debe validarse con CSS."
        )

    if saldo is None:
        advertencias.append(
            "Para calcular o devolver el Componente de Ahorro Personal se "
            "necesita el saldo ahorrado y capitalizado a la fecha de "
            "solicitud. Debe provenir de la cuenta individual oficial o de "
            "una importación validada."
        )
        return _resumen_cap_vacio(
            datos,
            saldo=saldo,
            bono=bono,
            capital=capital,
            valor_actuarial=valor_actuarial,
            devolucion_disponible=devolucion_disponible,
            decision_requerida=False,
            advertencias=advertencias,
        )

    if devolucion_disponible and datos.opcion_prestacion_cap == "AUTO":
        advertencias.append(
            "El artículo 187 permite solicitar la devolución total del CAP "
            "al alcanzar la edad de referencia sin cumplir los requisitos "
            "de la pensión normal. La aplicación no elige entre devolución "
            "y prestación programada sin una decisión expresa del Asegurado(a)."
        )
        return _resumen_cap_vacio(
            datos,
            saldo=saldo,
            bono=bono,
            capital=capital,
            valor_actuarial=valor_actuarial,
            devolucion_disponible=True,
            decision_requerida=True,
            advertencias=advertencias,
        )

    if datos.opcion_prestacion_cap == "DEVOLUCION_TOTAL":
        if not devolucion_disponible:
            advertencias.append(
                "La devolución total del artículo 187 no está disponible en "
                "este escenario: exige haber alcanzado la edad de referencia "
                "sin cumplir los requisitos de la pensión normal."
            )
            return _resumen_cap_vacio(
                datos,
                saldo=saldo,
                bono=bono,
                capital=capital,
                valor_actuarial=valor_actuarial,
                devolucion_disponible=False,
                decision_requerida=False,
                advertencias=advertencias,
            )

        advertencias.extend(
            [
                "La devolución del CAP es un pago único. No se presenta como "
                "pensión mensual.",
                "Con la devolución total del artículo 187 el Asegurado(a) queda "
                "desligado del Subsistema Mixto respecto de este componente.",
                "Las primas del Seguro Colectivo de Renta Vitalicia no son "
                "objeto de devolución porque forman parte del aporte de "
                "solidaridad conforme al reglamento de seguros colectivos.",
            ]
        )

        prima = parametros["seguros_colectivos"][
            "prima_renta_vitalicia_pct_historica"
        ]

        return ResumenComponenteAhorroPersonalMixto(
            calculo_disponible=True,
            saldo_ahorro_personal=redondear_moneda(saldo),
            bono_reconocimiento=redondear_moneda(bono),
            bono_reconocimiento_confirmado_oficialmente=(
                datos.bono_reconocimiento_confirmado_oficialmente
            ),
            capital_total_considerado=redondear_moneda(capital),
            valor_actuarial_expectativa_vida=(
                float(valor_actuarial)
                if valor_actuarial is not None
                else None
            ),
            opcion_solicitada="DEVOLUCION_TOTAL",
            decision_requerida=False,
            pension_programada_mensual=None,
            devolucion_total_disponible=True,
            devolucion_pago_unico_estimado=redondear_moneda(capital),
            garantia_renta_vitalicia_aplica=False,
            garantia_monto_mensual=None,
            garantia_condicion_activacion=None,
            prima_renta_vitalicia_pct_referencia=float(prima),
            prima_renta_vitalicia_es_referencia_historica=True,
            monto_maximo_aplicable=None,
            advertencias=advertencias,
        )

    # Si el componente definido solo genera indemnización, no se presume una
    # pensión mensual CAP sin una confirmación normativa individual. La ruta
    # expresamente implementada en esta fase es la devolución del artículo 187.
    if componente_bd.tipo_prestacion == "INDEMNIZACION":
        advertencias.append(
            "Con menos de 180 cuotas el componente definido genera una "
            "indemnización. Esta versión no presume una pensión programada "
            "CAP en ese caso; para completar el cálculo seleccione la "
            "devolución total del artículo 187 o valide el caso con la CSS."
        )
        return _resumen_cap_vacio(
            datos,
            saldo=saldo,
            bono=bono,
            capital=capital,
            valor_actuarial=valor_actuarial,
            devolucion_disponible=devolucion_disponible,
            decision_requerida=devolucion_disponible,
            advertencias=advertencias,
        )

    if valor_actuarial is None:
        advertencias.append(
            "El artículo 182 exige dividir el capital entre el valor "
            "actuarial de la expectativa de vida considerando la tasa de "
            "descuento vigente. La aplicación no dispone todavía de una "
            "tabla actuarial pública versionada y no reutiliza factores del "
            "SUCGS."
        )
        return _resumen_cap_vacio(
            datos,
            saldo=saldo,
            bono=bono,
            capital=capital,
            valor_actuarial=None,
            devolucion_disponible=devolucion_disponible,
            decision_requerida=False,
            advertencias=advertencias,
        )

    pension = capital / valor_actuarial
    prima = parametros["seguros_colectivos"][
        "prima_renta_vitalicia_pct_historica"
    ]

    advertencias.append(
        "La garantía de renta vitalicia no aumenta el monto inicial: se "
        "activa si el pensionado sobrevive la expectativa de vida usada en "
        "el cálculo y se agotan los fondos del CAP."
    )

    return ResumenComponenteAhorroPersonalMixto(
        calculo_disponible=True,
        saldo_ahorro_personal=redondear_moneda(saldo),
        bono_reconocimiento=redondear_moneda(bono),
        bono_reconocimiento_confirmado_oficialmente=(
            datos.bono_reconocimiento_confirmado_oficialmente
        ),
        capital_total_considerado=redondear_moneda(capital),
        valor_actuarial_expectativa_vida=float(valor_actuarial),
        opcion_solicitada=(
            "PENSION_PROGRAMADA"
            if datos.opcion_prestacion_cap == "AUTO"
            else datos.opcion_prestacion_cap
        ),
        decision_requerida=False,
        pension_programada_mensual=redondear_moneda(pension),
        devolucion_total_disponible=devolucion_disponible,
        devolucion_pago_unico_estimado=None,
        garantia_renta_vitalicia_aplica=True,
        garantia_monto_mensual=redondear_moneda(pension),
        garantia_condicion_activacion=(
            "Sobrevivir la expectativa de vida utilizada para determinar "
            "la pensión CAP y que se extingan los fondos ahorrados."
        ),
        prima_renta_vitalicia_pct_referencia=float(prima),
        prima_renta_vitalicia_es_referencia_historica=True,
        monto_maximo_aplicable=None,
        advertencias=advertencias,
    )


def _resultado_transicion(
    *,
    sistema: str,
    estado: str,
    fecha_fin_mixto: date,
    fecha_inicio_sucgs: date,
    advertencia: str,
) -> ResumenCalculoMixto:
    """Construye una salida Mixto que debe resolverse bajo SUCGS."""

    return ResumenCalculoMixto(
        sistema_solicitado=sistema,
        estado_sistema=estado,
        calculo_mixto_aplicable=False,
        fecha_fin_calculo_mixto=fecha_fin_mixto,
        fecha_inicio_calculo_sucgs=fecha_inicio_sucgs,
        modalidad=None,
        modalidad_nombre=None,
        tipo_prestacion="TRANSICION_SUCGS",
        elegible=False,
        calculo_completo=False,
        componente_beneficio_definido=None,
        componente_ahorro_personal=None,
        pension_mensual_total_estimada=None,
        pago_unico_bd_estimado=None,
        pago_unico_cap_estimado=None,
        pago_unico_total_estimado=None,
        advertencias=[advertencia],
        fuente_normativa=_fuente_normativa(),
    )


def calcular_mixto(datos: DatosCalculoMixto) -> ResumenCalculoMixto:
    """Evalúa pensión, devolución o indemnización del Subsistema Mixto."""

    parametros = cargar_parametros_mixto()
    transicion = parametros["transicion"]

    fecha_fin_mixto = date.fromisoformat(
        transicion["fecha_fin_calculo_bajo_mixto"]
    )
    fecha_inicio_sucgs = date.fromisoformat(
        transicion["fecha_inicio_calculo_bajo_sucgs"]
    )

    if datos.sistema_seleccionado == "SUCGS":
        return _resultado_transicion(
            sistema="SUCGS",
            estado="OPTO_SUCGS",
            fecha_fin_mixto=fecha_fin_mixto,
            fecha_inicio_sucgs=fecha_inicio_sucgs,
            advertencia=(
                "El escenario indica que el Asegurado(a) optó por el SUCGS. "
                "La prestación debe calcularse bajo el artículo 196 y no "
                "con las reglas del Subsistema Mixto."
            ),
        )

    if datos.fecha_retiro >= fecha_inicio_sucgs:
        return _resultado_transicion(
            sistema="MIXTO",
            estado="TRANSICION_SUCGS",
            fecha_fin_mixto=fecha_fin_mixto,
            fecha_inicio_sucgs=fecha_inicio_sucgs,
            advertencia=(
                "Para solicitudes desde el 1 de marzo de 2032, el "
                "Reglamento de Incorporación al Componente Contributivo de "
                "Capitalización Solidaria dispone calcular la prestación "
                "conforme al artículo 196 del SUCGS."
            ),
        )

    componente_bd = _calcular_componente_bd(
        datos,
        parametros,
    )
    componente_cap = _calcular_componente_cap(
        datos,
        componente_bd,
        parametros,
    )

    advertencias: list[str] = []

    pension_total = None
    pago_unico_bd = componente_bd.indemnizacion_pago_unico_estimado
    pago_unico_cap = componente_cap.devolucion_pago_unico_estimado
    pago_unico_total = None

    if (
        componente_bd.pension_mensual_estimada is not None
        and componente_cap.calculo_disponible
    ):
        # En la ruta de pensión programada se suman ambos componentes. Si el
        # Asegurado(a) eligió devolución total, el CAP deja de aportar una renta
        # mensual y el total mensual queda compuesto únicamente por el BD.
        pension_total_decimal = a_decimal(
            componente_bd.pension_mensual_estimada
        )

        if componente_cap.pension_programada_mensual is not None:
            pension_total_decimal += a_decimal(
                componente_cap.pension_programada_mensual
            )

        pension_total = redondear_moneda(pension_total_decimal)

    if pago_unico_bd is not None and pago_unico_cap is not None:
        pago_unico_total = redondear_moneda(
            a_decimal(pago_unico_bd)
            + a_decimal(pago_unico_cap)
        )
    elif pago_unico_bd is None and pago_unico_cap is not None:
        pago_unico_total = redondear_moneda(pago_unico_cap)

    bono_validado = (
        datos.bono_reconocimiento == 0
        or datos.bono_reconocimiento_confirmado_oficialmente
    )

    if not componente_cap.calculo_disponible:
        if componente_cap.decision_requerida:
            advertencias.append(
                "El resultado Mixto está pendiente porque debe escogerse "
                "expresamente el tratamiento del Componente de Ahorro "
                "Personal."
            )
        else:
            advertencias.append(
                "El resultado Mixto está incompleto porque el Componente de "
                "Ahorro Personal no puede calcularse con los datos actuales."
            )

    if not bono_validado:
        advertencias.append(
            "El bono de reconocimiento ingresado no fue marcado como monto "
            "oficialmente confirmado; el total se considera provisional."
        )

    advertencias.append(
        "La fecha operativa comunicada por la CSS para ejercer determinadas "
        "opciones de cambio de sistema en 2026 es el 18/08/2026. La "
        "elegibilidad individual para esa opción debe verificarse con la CSS."
    )

    if componente_bd.tipo_prestacion == "INDEMNIZACION":
        tipo_prestacion = (
            "INDEMNIZACION_MIXTA"
            if pago_unico_total is not None
            else "INDEMNIZACION"
        )
    elif componente_cap.devolucion_pago_unico_estimado is not None:
        tipo_prestacion = "PENSION_MAS_DEVOLUCION_CAP"
    elif componente_cap.decision_requerida:
        tipo_prestacion = "DECISION_CAP_PENDIENTE"
    else:
        tipo_prestacion = componente_bd.tipo_prestacion

    calculo_completo = (
        componente_bd.calculo_disponible
        and componente_cap.calculo_disponible
        and bono_validado
        and (
            pension_total is not None
            or pago_unico_total is not None
        )
    )

    return ResumenCalculoMixto(
        sistema_solicitado="MIXTO",
        estado_sistema="MIXTO_CALCULABLE",
        calculo_mixto_aplicable=True,
        fecha_fin_calculo_mixto=fecha_fin_mixto,
        fecha_inicio_calculo_sucgs=fecha_inicio_sucgs,
        modalidad=componente_bd.modalidad,
        modalidad_nombre=componente_bd.modalidad_nombre,
        tipo_prestacion=tipo_prestacion,
        elegible=componente_bd.elegible,
        calculo_completo=calculo_completo,
        componente_beneficio_definido=componente_bd,
        componente_ahorro_personal=componente_cap,
        pension_mensual_total_estimada=pension_total,
        pago_unico_bd_estimado=pago_unico_bd,
        pago_unico_cap_estimado=pago_unico_cap,
        pago_unico_total_estimado=pago_unico_total,
        advertencias=advertencias,
        fuente_normativa=_fuente_normativa(),
    )
