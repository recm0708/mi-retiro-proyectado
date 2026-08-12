"""Motor del Sistema Único de Capitalización con Garantía Solidaria.

La subfase 6E.3 aplica las tres capas necesarias para la pensión de vejez:

1. Componente Contributivo de Capitalización Solidaria, artículo 196.
2. Componente Solidario No Contributivo y Pensión Garantizada Solidaria,
   artículos 194 y 195.
3. Garantía de reemplazo mínimo del artículo 197.

Las condiciones 1 y 2 del artículo 197 se preevalúan con el historial anual.
La condición 3 de estabilidad salarial se mantiene como confirmación
explícita: su redacción legal requiere validación operativa de la CSS y la
propia norma asigna a la Institución los mecanismos de control.
"""

from calendar import monthrange
from datetime import date
from decimal import Decimal
from math import ceil

from app.core.dinero import a_decimal, redondear_moneda
from app.core.normativa import (
    cargar_parametros_sucgs,
    obtener_edad_referencia,
)
from app.modelos.pension import (
    DatosCalculoSUCGS,
    ResumenCalculoSUCGS,
)


def _fuente_normativa() -> str:
    """Devuelve las fuentes principales usadas por la subfase 6E.3."""

    return (
        "Texto Único de la Ley 51 de 2005, artículo 1 numeral 41 y "
        "artículos 152, 153 y 194-198, Gaceta Oficial 30284-B de "
        "22/05/2025. En 6E.3 se aplican la fórmula y tabla actuarial del "
        "artículo 196, la capa solidaria de los artículos 194 y 195 y la "
        "garantía de reemplazo mínimo del artículo 197. La estabilidad "
        "salarial del numeral 3 se exige como confirmación expresa debido a "
        "su redacción y a los mecanismos de control reservados a la CSS."
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


def _edad_en_fecha(fecha_nacimiento: date, fecha: date) -> int:
    """Calcula la edad cumplida en años en una fecha determinada."""

    edad = fecha.year - fecha_nacimiento.year
    if (fecha.month, fecha.day) < (
        fecha_nacimiento.month,
        fecha_nacimiento.day,
    ):
        edad -= 1
    return edad


def _factor_actuarial(edad: int) -> Decimal | None:
    """Obtiene el factor actuarial legal versionado por edad."""

    parametros = cargar_parametros_sucgs()
    tabla = parametros[
        "componente_contributivo"
    ]["factores_pensionamiento_actuarial"]

    if edad >= 80:
        return a_decimal(tabla["80_mas"])

    valor = tabla.get(str(edad))
    if valor is None:
        return None

    return a_decimal(valor)


def _resolver_valores_solidarios(
    datos: DatosCalculoSUCGS,
    advertencias: list[str],
) -> tuple[Decimal, Decimal, int]:
    """Resuelve los valores monetarios usados por los artículos 194 y 195.

    La Ley versionada fija B/.144.00 como referencia del valor mínimo
    universal y establece una Pensión Garantizada Solidaria de al menos
    B/.265.00. El usuario puede aportar valores vigentes confirmados; de lo
    contrario se conservan las referencias legales de la versión cargada.
    """

    parametros = cargar_parametros_sucgs()
    garantias = parametros["garantias"]

    minimo_referencia = a_decimal(
        garantias["valor_minimo_universal_referencia"]
    )
    pgs_referencia = a_decimal(
        garantias["pension_garantizada_solidaria_base"]
    )
    edad_solidaria = int(
        garantias["edad_referencia_componente_solidario"]
    )

    minimo = (
        a_decimal(datos.valor_minimo_universal_vigente)
        if datos.valor_minimo_universal_vigente is not None
        else minimo_referencia
    )
    pgs = (
        a_decimal(datos.pension_garantizada_solidaria_vigente)
        if datos.pension_garantizada_solidaria_vigente is not None
        else pgs_referencia
    )

    if pgs < pgs_referencia:
        advertencias.append(
            "El monto ingresado para la Pensión Garantizada Solidaria es "
            "inferior al mínimo legal de referencia B/.265.00 del artículo "
            "195. Para evitar reducir una garantía legal, se utilizará "
            "B/.265.00."
        )
        pgs = pgs_referencia

    if not datos.valores_solidarios_confirmados_oficialmente:
        advertencias.append(
            "Los valores monetarios de la capa solidaria no fueron marcados "
            "como vigentes y confirmados oficialmente. La aplicación usa, "
            "cuando no se suministran otros valores, las referencias legales "
            "B/.144.00 y B/.265.00 versionadas al 22/05/2025. Las "
            "prestaciones del artículo 194 están sujetas a indexación."
        )

    return minimo, pgs, edad_solidaria


def _aplicar_capa_solidaria(
    *,
    pension_contributiva: Decimal,
    edad_retiro: int,
    edad_referencia: int,
    cuotas_totales: int,
    valor_minimo_universal: Decimal,
    pension_garantizada: Decimal,
    edad_solidaria: int,
    advertencias: list[str],
) -> tuple[str, Decimal, Decimal]:
    """Aplica los artículos 194 y 195 sobre la pensión contributiva.

    Devuelve ``(tipo_prestacion, complemento, pension_resultante)``.
    """

    cero = Decimal("0")

    # Artículo 195: con edad de referencia y 240 o más cuotas, la PGS es la
    # pensión mínima del componente contributivo. Se evalúa primero porque el
    # numeral 2 del artículo 194 incluye literalmente el límite de 240 cuotas,
    # produciendo una superposición normativa en ese punto exacto.
    if edad_retiro >= edad_referencia and cuotas_totales >= 240:
        if pension_contributiva >= pension_garantizada:
            return (
                "PENSION_CONTRIBUTIVA_SIN_COMPLEMENTO",
                cero,
                pension_contributiva,
            )

        complemento = pension_garantizada - pension_contributiva

        if pension_contributiva >= valor_minimo_universal:
            tipo = "PENSION_BENEFICIO_SOLIDARIO"
        else:
            tipo = "PENSION_GARANTIZADA_SOLIDARIA_ART195"
            advertencias.append(
                "El artículo 194 numeral 4 describe expresamente la Pensión "
                "de Beneficio Solidario cuando la pensión contributiva es "
                "igual o superior al valor mínimo universal. Cuando la "
                "pensión contributiva queda por debajo de ese umbral pero "
                "existen 240 o más cuotas, esta subfase conserva el mínimo "
                "general del artículo 195 y lo identifica separadamente."
            )

        return tipo, complemento, pension_garantizada

    # Artículo 194: los casos con menos de 240 cuotas se incorporan al
    # Componente Solidario No Contributivo al alcanzar 65 años.
    if edad_retiro < edad_solidaria:
        return (
            "COMPONENTE_SOLIDARIO_AUN_NO_ACCESIBLE",
            cero,
            pension_contributiva,
        )

    if cuotas_totales < 120:
        # Numeral 1: si queda por debajo del mínimo universal, se paga el
        # propio resultado contributivo; no se completa hasta B/.144.00.
        if pension_contributiva < valor_minimo_universal:
            return (
                "PENSION_CONTRIBUTIVA_BAJO_MINIMO_UNIVERSAL",
                cero,
                pension_contributiva,
            )

        return (
            "PENSION_CONTRIBUTIVA_ART194_3",
            cero,
            pension_contributiva,
        )

    # Para evitar la superposición literal de 240 cuotas entre los artículos
    # 194 y 195, este bloque usa 120 <= cuotas < 240.
    if cuotas_totales < 240:
        if pension_contributiva <= valor_minimo_universal:
            complemento = valor_minimo_universal - pension_contributiva
            return (
                "PENSION_BENEFICIO_MINIMO",
                complemento,
                valor_minimo_universal,
            )

        return (
            "PENSION_CONTRIBUTIVA_ART194_3",
            cero,
            pension_contributiva,
        )

    # Defensa adicional: el flujo de 240 o más cuotas debió resolverse antes.
    return (
        "PENSION_CONTRIBUTIVA_SIN_COMPLEMENTO",
        cero,
        pension_contributiva,
    )


def _max_consecutivos(valores: list[int]) -> int:
    """Devuelve la mayor racha consecutiva de años de una lista ordenada."""

    if not valores:
        return 0

    maximo = 1
    actual = 1

    for anterior, actual_anio in zip(valores, valores[1:]):
        if actual_anio == anterior + 1:
            actual += 1
            maximo = max(maximo, actual)
        else:
            actual = 1

    return maximo


def _evaluar_garantia_reemplazo(
    *,
    datos: DatosCalculoSUCGS,
    pension_despues_solidaria: Decimal,
    advertencias: list[str],
) -> dict[str, object]:
    """Preevalúa y aplica, cuando procede, la garantía del artículo 197.

    La definición general de salario base mensual del artículo 1 numeral 41
    permite obtener un promedio mensual dividiendo salarios cotizados entre
    meses cotizados. El historial anual conserva ambos totales y permite esa
    operación sin inventar meses salariales.

    La condición de estabilidad salarial no se infiere automáticamente. El
    texto legal usa una formulación susceptible de interpretación y ordena a
    la CSS implementar mecanismos de control; por ello esta subfase exige una
    confirmación expresa para otorgar la garantía.
    """

    parametros = cargar_parametros_sucgs()
    garantia = parametros["garantias"]["reemplazo_minimo_art197"]

    cuotas_referencia = int(garantia["cuotas_referencia"])
    cuotas_minimas_proporcional = int(
        garantia["cuotas_minimas_garantia_proporcional"]
    )
    tasa_base = a_decimal(garantia["tasa_reemplazo_minima_pct"])
    max_anios_cero = int(garantia["max_anios_sin_cotizacion"])
    max_consecutivos_cero = int(
        garantia["max_anios_sin_cotizacion_consecutivos"]
    )
    cuotas_minimas_anio = int(garantia["cuotas_minimas_por_anio_activo"])
    primeros_anios = int(garantia["primeros_anios_distribucion"])
    proporcion_tramo = a_decimal(garantia["proporcion_minima_por_tramo"])

    registros = sorted(
        datos.registros_historial_laboral,
        key=lambda registro: registro.anio,
    )

    anio_inicio = datos.anio_inicio_vida_laboral
    if anio_inicio is None and registros:
        anio_inicio = registros[0].anio
        advertencias.append(
            "El año inicial de vida laboral no fue suministrado; para la "
            "preevaluación del artículo 197 se tomó el primer año presente "
            "en el historial."
        )

    historial_cuotas_sumadas: int | None = None
    historial_cuotas_coinciden: bool | None = None
    rango_completo = False
    salario_base: Decimal | None = None

    condicion_anual_evaluada = False
    condicion_anual_cumple: bool | None = None
    anios_sin_cotizacion_total: int | None = None
    max_anios_sin_cotizacion_consecutivos: int | None = None
    anios_con_1_a_4: list[int] = []

    condicion_distribucion_evaluada = False
    condicion_distribucion_cumple: bool | None = None
    cuotas_objetivo: int | None = None
    cuotas_minimas_tramo: int | None = None
    cuotas_primeros_20: int | None = None
    cuotas_restantes: int | None = None

    condicion_estabilidad_evaluada = (
        datos.estabilidad_salarial_art197_confirmada is not None
    )
    condicion_estabilidad_cumple = (
        datos.estabilidad_salarial_art197_confirmada
        if condicion_estabilidad_evaluada
        else None
    )

    if registros:
        historial_cuotas_sumadas = sum(registro.cuotas for registro in registros)
        historial_cuotas_coinciden = (
            historial_cuotas_sumadas == datos.cuotas_totales
        )

    if anio_inicio is not None and registros:
        anios_esperados = list(
            range(anio_inicio, datos.fecha_retiro.year + 1)
        )
        por_anio = {registro.anio: registro for registro in registros}
        sin_duplicados = len(por_anio) == len(registros)
        rango_completo = sin_duplicados and all(
            anio in por_anio for anio in anios_esperados
        )

        if not sin_duplicados:
            advertencias.append(
                "El historial laboral contiene años duplicados; no puede "
                "usarse para verificar automáticamente el artículo 197."
            )

        if datos.historial_laboral_completo and not rango_completo:
            advertencias.append(
                "El historial fue marcado como completo, pero faltan años "
                "entre el inicio de la vida laboral y el retiro."
            )

        if rango_completo:
            anios_cero = [
                anio
                for anio in anios_esperados
                if por_anio[anio].cuotas == 0
            ]
            anios_con_1_a_4 = [
                anio
                for anio in anios_esperados
                if 0 < por_anio[anio].cuotas < cuotas_minimas_anio
            ]
            anios_sin_cotizacion_total = len(anios_cero)
            max_anios_sin_cotizacion_consecutivos = _max_consecutivos(
                anios_cero
            )

            condicion_anual_evaluada = True
            condicion_anual_cumple = (
                not anios_con_1_a_4
                and anios_sin_cotizacion_total <= max_anios_cero
                and max_anios_sin_cotizacion_consecutivos
                <= max_consecutivos_cero
            )

            if datos.cuotas_totales >= cuotas_minimas_proporcional:
                cuotas_objetivo = min(
                    datos.cuotas_totales,
                    cuotas_referencia,
                )
                cuotas_minimas_tramo = ceil(
                    Decimal(cuotas_objetivo) * proporcion_tramo
                )
                fin_primer_tramo = anio_inicio + primeros_anios - 1
                cuotas_primeros_20 = sum(
                    por_anio[anio].cuotas
                    for anio in anios_esperados
                    if anio <= fin_primer_tramo
                )
                cuotas_restantes = sum(
                    por_anio[anio].cuotas
                    for anio in anios_esperados
                    if anio > fin_primer_tramo
                )
                condicion_distribucion_evaluada = True
                condicion_distribucion_cumple = (
                    cuotas_primeros_20 >= cuotas_minimas_tramo
                    and cuotas_restantes >= cuotas_minimas_tramo
                )
            else:
                condicion_distribucion_evaluada = True
                condicion_distribucion_cumple = False

            total_salarios = sum(
                a_decimal(por_anio[anio].salario_cotizado)
                for anio in anios_esperados
            )
            total_meses = sum(
                por_anio[anio].cuotas
                for anio in anios_esperados
            )
            if total_meses > 0:
                salario_base = total_salarios / Decimal(total_meses)

    historial_valido = (
        datos.historial_laboral_completo
        and rango_completo
        and historial_cuotas_coinciden is True
    )

    if datos.historial_laboral_completo and historial_cuotas_coinciden is False:
        advertencias.append(
            "Las cuotas del historial laboral no coinciden con las cuotas "
            "totales evaluadas al retiro; la garantía del artículo 197 no "
            "puede cerrarse con esos datos."
        )

    # Menos de 120 cuotas: esta implementación no extiende la garantía
    # proporcional del segundo párrafo del artículo 197 a ese grupo.
    if datos.cuotas_totales < cuotas_minimas_proporcional:
        advertencias.append(
            "La garantía proporcional del artículo 197 se modela desde 120 "
            "cuotas, umbral explícito del Componente Solidario del artículo "
            "194. Con menos cuotas se conserva la prestación resultante de "
            "las capas anteriores."
        )
        return {
            "garantia_reemplazo_evaluada": True,
            "garantia_reemplazo_aplica": False,
            "historial_laboral_completo": datos.historial_laboral_completo,
            "historial_rango_anual_completo": rango_completo,
            "historial_cuotas_sumadas": historial_cuotas_sumadas,
            "historial_cuotas_coinciden": historial_cuotas_coinciden,
            "condicion_minimo_cuotas_anuales_evaluada": condicion_anual_evaluada,
            "condicion_minimo_cuotas_anuales_cumple": condicion_anual_cumple,
            "anios_sin_cotizacion_total": anios_sin_cotizacion_total,
            "max_anios_sin_cotizacion_consecutivos": max_anios_sin_cotizacion_consecutivos,
            "anios_con_1_a_4_cuotas": anios_con_1_a_4,
            "condicion_distribucion_cuotas_evaluada": condicion_distribucion_evaluada,
            "condicion_distribucion_cuotas_cumple": condicion_distribucion_cumple,
            "cuotas_objetivo_distribucion": cuotas_objetivo,
            "cuotas_minimas_por_tramo": cuotas_minimas_tramo,
            "cuotas_primeros_20_anios": cuotas_primeros_20,
            "cuotas_anios_restantes": cuotas_restantes,
            "condicion_estabilidad_salarial_evaluada": condicion_estabilidad_evaluada,
            "condicion_estabilidad_salarial_cumple": condicion_estabilidad_cumple,
            "salario_promedio_base_mensual": salario_base,
            "tasa_reemplazo_minima_pct_aplicable": None,
            "garantia_reemplazo_monto_objetivo": None,
            "garantia_reemplazo_complemento_mensual": Decimal("0"),
            "calculo_total_disponible": True,
            "pension_mensual_total_estimada": pension_despues_solidaria,
        }

    condiciones_falsas = (
        condicion_anual_cumple is False
        or condicion_distribucion_cumple is False
        or condicion_estabilidad_cumple is False
    )

    if condiciones_falsas:
        razones: list[str] = []
        if condicion_anual_cumple is False:
            razones.append("mínimo anual / años sin cotización")
        if condicion_distribucion_cumple is False:
            razones.append("distribución 50 % / 50 %")
        if condicion_estabilidad_cumple is False:
            razones.append("estabilidad salarial")
        advertencias.append(
            "La garantía de reemplazo mínimo del artículo 197 no se aplica "
            "porque no se cumple: " + ", ".join(razones) + "."
        )
        return {
            "garantia_reemplazo_evaluada": True,
            "garantia_reemplazo_aplica": False,
            "historial_laboral_completo": datos.historial_laboral_completo,
            "historial_rango_anual_completo": rango_completo,
            "historial_cuotas_sumadas": historial_cuotas_sumadas,
            "historial_cuotas_coinciden": historial_cuotas_coinciden,
            "condicion_minimo_cuotas_anuales_evaluada": condicion_anual_evaluada,
            "condicion_minimo_cuotas_anuales_cumple": condicion_anual_cumple,
            "anios_sin_cotizacion_total": anios_sin_cotizacion_total,
            "max_anios_sin_cotizacion_consecutivos": max_anios_sin_cotizacion_consecutivos,
            "anios_con_1_a_4_cuotas": anios_con_1_a_4,
            "condicion_distribucion_cuotas_evaluada": condicion_distribucion_evaluada,
            "condicion_distribucion_cuotas_cumple": condicion_distribucion_cumple,
            "cuotas_objetivo_distribucion": cuotas_objetivo,
            "cuotas_minimas_por_tramo": cuotas_minimas_tramo,
            "cuotas_primeros_20_anios": cuotas_primeros_20,
            "cuotas_anios_restantes": cuotas_restantes,
            "condicion_estabilidad_salarial_evaluada": condicion_estabilidad_evaluada,
            "condicion_estabilidad_salarial_cumple": condicion_estabilidad_cumple,
            "salario_promedio_base_mensual": salario_base,
            "tasa_reemplazo_minima_pct_aplicable": None,
            "garantia_reemplazo_monto_objetivo": None,
            "garantia_reemplazo_complemento_mensual": Decimal("0"),
            "calculo_total_disponible": True,
            "pension_mensual_total_estimada": pension_despues_solidaria,
        }

    condiciones_completas = (
        historial_valido
        and condicion_anual_cumple is True
        and condicion_distribucion_cumple is True
        and condicion_estabilidad_cumple is True
        and salario_base is not None
    )

    if not condiciones_completas:
        advertencias.append(
            "La garantía de reemplazo mínimo del artículo 197 todavía no "
            "puede determinarse. Se requiere historial laboral anual completo "
            "y coincidente con las cuotas del retiro, además de confirmación "
            "de la condición de estabilidad salarial."
        )
        return {
            "garantia_reemplazo_evaluada": False,
            "garantia_reemplazo_aplica": None,
            "historial_laboral_completo": datos.historial_laboral_completo,
            "historial_rango_anual_completo": rango_completo,
            "historial_cuotas_sumadas": historial_cuotas_sumadas,
            "historial_cuotas_coinciden": historial_cuotas_coinciden,
            "condicion_minimo_cuotas_anuales_evaluada": condicion_anual_evaluada,
            "condicion_minimo_cuotas_anuales_cumple": condicion_anual_cumple,
            "anios_sin_cotizacion_total": anios_sin_cotizacion_total,
            "max_anios_sin_cotizacion_consecutivos": max_anios_sin_cotizacion_consecutivos,
            "anios_con_1_a_4_cuotas": anios_con_1_a_4,
            "condicion_distribucion_cuotas_evaluada": condicion_distribucion_evaluada,
            "condicion_distribucion_cuotas_cumple": condicion_distribucion_cumple,
            "cuotas_objetivo_distribucion": cuotas_objetivo,
            "cuotas_minimas_por_tramo": cuotas_minimas_tramo,
            "cuotas_primeros_20_anios": cuotas_primeros_20,
            "cuotas_anios_restantes": cuotas_restantes,
            "condicion_estabilidad_salarial_evaluada": condicion_estabilidad_evaluada,
            "condicion_estabilidad_salarial_cumple": condicion_estabilidad_cumple,
            "salario_promedio_base_mensual": salario_base,
            "tasa_reemplazo_minima_pct_aplicable": None,
            "garantia_reemplazo_monto_objetivo": None,
            "garantia_reemplazo_complemento_mensual": None,
            "calculo_total_disponible": False,
            "pension_mensual_total_estimada": None,
        }

    if datos.cuotas_totales >= cuotas_referencia:
        tasa_aplicable = tasa_base
    else:
        tasa_aplicable = (
            tasa_base
            * Decimal(datos.cuotas_totales)
            / Decimal(cuotas_referencia)
        )

    objetivo = salario_base * tasa_aplicable / Decimal("100")
    complemento = max(
        Decimal("0"),
        objetivo - pension_despues_solidaria,
    )
    pension_final = max(pension_despues_solidaria, objetivo)
    aplica = complemento > 0

    if aplica:
        advertencias.append(
            "Se aplicó la garantía de reemplazo mínimo del artículo 197. "
            "El resultado se elevó hasta la tasa mínima que corresponde al "
            "salario promedio base y al número de cuotas."
        )
    else:
        advertencias.append(
            "Las condiciones del artículo 197 se cumplen, pero la prestación "
            "obtenida por las capas anteriores ya es igual o superior al "
            "mínimo garantizado de reemplazo."
        )

    return {
        "garantia_reemplazo_evaluada": True,
        "garantia_reemplazo_aplica": aplica,
        "historial_laboral_completo": datos.historial_laboral_completo,
        "historial_rango_anual_completo": rango_completo,
        "historial_cuotas_sumadas": historial_cuotas_sumadas,
        "historial_cuotas_coinciden": historial_cuotas_coinciden,
        "condicion_minimo_cuotas_anuales_evaluada": condicion_anual_evaluada,
        "condicion_minimo_cuotas_anuales_cumple": condicion_anual_cumple,
        "anios_sin_cotizacion_total": anios_sin_cotizacion_total,
        "max_anios_sin_cotizacion_consecutivos": max_anios_sin_cotizacion_consecutivos,
        "anios_con_1_a_4_cuotas": anios_con_1_a_4,
        "condicion_distribucion_cuotas_evaluada": condicion_distribucion_evaluada,
        "condicion_distribucion_cuotas_cumple": condicion_distribucion_cumple,
        "cuotas_objetivo_distribucion": cuotas_objetivo,
        "cuotas_minimas_por_tramo": cuotas_minimas_tramo,
        "cuotas_primeros_20_anios": cuotas_primeros_20,
        "cuotas_anios_restantes": cuotas_restantes,
        "condicion_estabilidad_salarial_evaluada": condicion_estabilidad_evaluada,
        "condicion_estabilidad_salarial_cumple": condicion_estabilidad_cumple,
        "salario_promedio_base_mensual": salario_base,
        "tasa_reemplazo_minima_pct_aplicable": tasa_aplicable,
        "garantia_reemplazo_monto_objetivo": objetivo,
        "garantia_reemplazo_complemento_mensual": complemento,
        "calculo_total_disponible": True,
        "pension_mensual_total_estimada": pension_final,
    }


def calcular_sucgs(
    datos: DatosCalculoSUCGS,
) -> ResumenCalculoSUCGS:
    """Calcula las capas de vejez del SUCGS hasta el artículo 197."""

    parametros = cargar_parametros_sucgs()
    divisor = int(
        parametros[
            "componente_contributivo"
        ]["divisor_formula"]
    )

    edad_referencia = obtener_edad_referencia(datos.sexo)
    fecha_referencia = _sumar_anios(
        datos.fecha_nacimiento,
        edad_referencia,
    )
    edad_retiro = _edad_en_fecha(
        datos.fecha_nacimiento,
        datos.fecha_retiro,
    )
    cumple_edad = datos.fecha_retiro >= fecha_referencia
    factor = _factor_actuarial(edad_retiro)

    advertencias: list[str] = []
    calculo_contributivo_disponible = True

    if not cumple_edad:
        calculo_contributivo_disponible = False
        advertencias.append(
            "La subfase 6E.3 evalúa retiro por vejez desde la edad de "
            "referencia. La fecha seleccionada es anterior; regímenes "
            "especiales o excepciones deben evaluarse por separado."
        )

    if factor is None:
        calculo_contributivo_disponible = False
        advertencias.append(
            "No existe un factor de pensionamiento actuarial versionado para "
            "la edad seleccionada en la tabla aplicada por esta subfase."
        )

    saldo = a_decimal(datos.saldo_capitalizacion_solidaria)
    pension_contributiva: Decimal | None = None

    if calculo_contributivo_disponible and factor is not None:
        pension_contributiva = (
            saldo
            / Decimal(divisor)
            * factor
        )

    if not datos.saldo_confirmado_oficialmente:
        advertencias.append(
            "El saldo de Capitalización Solidaria fue ingresado manualmente y "
            "no está marcado como dato oficial o validado. El cálculo sirve "
            "como simulación matemática del artículo 196."
        )

    minimo, pgs, edad_solidaria = _resolver_valores_solidarios(
        datos,
        advertencias,
    )

    garantia_solidaria_evaluada = False
    tipo_prestacion_solidaria: str | None = None
    complemento_solidario: Decimal | None = None
    pension_despues_solidaria: Decimal | None = None

    if pension_contributiva is not None:
        (
            tipo_prestacion_solidaria,
            complemento_solidario,
            pension_despues_solidaria,
        ) = _aplicar_capa_solidaria(
            pension_contributiva=pension_contributiva,
            edad_retiro=edad_retiro,
            edad_referencia=edad_referencia,
            cuotas_totales=datos.cuotas_totales,
            valor_minimo_universal=minimo,
            pension_garantizada=pgs,
            edad_solidaria=edad_solidaria,
            advertencias=advertencias,
        )
        garantia_solidaria_evaluada = True

    garantia = {
        "garantia_reemplazo_evaluada": False,
        "garantia_reemplazo_aplica": None,
        "historial_laboral_completo": datos.historial_laboral_completo,
        "historial_rango_anual_completo": False,
        "historial_cuotas_sumadas": None,
        "historial_cuotas_coinciden": None,
        "condicion_minimo_cuotas_anuales_evaluada": False,
        "condicion_minimo_cuotas_anuales_cumple": None,
        "anios_sin_cotizacion_total": None,
        "max_anios_sin_cotizacion_consecutivos": None,
        "anios_con_1_a_4_cuotas": [],
        "condicion_distribucion_cuotas_evaluada": False,
        "condicion_distribucion_cuotas_cumple": None,
        "cuotas_objetivo_distribucion": None,
        "cuotas_minimas_por_tramo": None,
        "cuotas_primeros_20_anios": None,
        "cuotas_anios_restantes": None,
        "condicion_estabilidad_salarial_evaluada": False,
        "condicion_estabilidad_salarial_cumple": None,
        "salario_promedio_base_mensual": None,
        "tasa_reemplazo_minima_pct_aplicable": None,
        "garantia_reemplazo_monto_objetivo": None,
        "garantia_reemplazo_complemento_mensual": None,
        "calculo_total_disponible": False,
        "pension_mensual_total_estimada": None,
    }

    if pension_despues_solidaria is not None:
        garantia = _evaluar_garantia_reemplazo(
            datos=datos,
            pension_despues_solidaria=pension_despues_solidaria,
            advertencias=advertencias,
        )

    return ResumenCalculoSUCGS(
        sistema="SUCGS",
        nombre_sistema=(
            "Sistema Único de Capitalización con Garantía Solidaria"
        ),
        tipo_calculo="SUCGS_COMPLETO_HASTA_ART197_6E3",
        edad_retiro_anios=edad_retiro,
        edad_referencia=edad_referencia,
        fecha_referencia=fecha_referencia,
        cumple_edad_referencia=cumple_edad,
        cuotas_totales=datos.cuotas_totales,
        saldo_capitalizacion_solidaria=redondear_moneda(saldo),
        saldo_confirmado_oficialmente=(
            datos.saldo_confirmado_oficialmente
        ),
        divisor_formula=divisor,
        factor_pensionamiento_actuarial=(
            float(factor)
            if factor is not None
            else None
        ),
        calculo_contributivo_disponible=(
            calculo_contributivo_disponible
        ),
        pension_contributiva_mensual=(
            redondear_moneda(pension_contributiva)
            if pension_contributiva is not None
            else None
        ),
        garantia_solidaria_evaluada=garantia_solidaria_evaluada,
        edad_referencia_componente_solidario=edad_solidaria,
        valor_minimo_universal_utilizado=redondear_moneda(minimo),
        pension_garantizada_solidaria_utilizada=redondear_moneda(pgs),
        valores_solidarios_confirmados_oficialmente=(
            datos.valores_solidarios_confirmados_oficialmente
        ),
        tipo_prestacion_solidaria=tipo_prestacion_solidaria,
        complemento_solidario_mensual=(
            redondear_moneda(complemento_solidario)
            if complemento_solidario is not None
            else None
        ),
        pension_despues_componente_solidario=(
            redondear_moneda(pension_despues_solidaria)
            if pension_despues_solidaria is not None
            else None
        ),
        garantia_reemplazo_evaluada=bool(
            garantia["garantia_reemplazo_evaluada"]
        ),
        garantia_reemplazo_aplica=garantia["garantia_reemplazo_aplica"],
        historial_laboral_completo=bool(
            garantia["historial_laboral_completo"]
        ),
        historial_rango_anual_completo=bool(
            garantia["historial_rango_anual_completo"]
        ),
        historial_cuotas_sumadas=garantia["historial_cuotas_sumadas"],
        historial_cuotas_coinciden=garantia["historial_cuotas_coinciden"],
        condicion_minimo_cuotas_anuales_evaluada=bool(
            garantia["condicion_minimo_cuotas_anuales_evaluada"]
        ),
        condicion_minimo_cuotas_anuales_cumple=(
            garantia["condicion_minimo_cuotas_anuales_cumple"]
        ),
        anios_sin_cotizacion_total=garantia["anios_sin_cotizacion_total"],
        max_anios_sin_cotizacion_consecutivos=(
            garantia["max_anios_sin_cotizacion_consecutivos"]
        ),
        anios_con_1_a_4_cuotas=list(
            garantia["anios_con_1_a_4_cuotas"]
        ),
        condicion_distribucion_cuotas_evaluada=bool(
            garantia["condicion_distribucion_cuotas_evaluada"]
        ),
        condicion_distribucion_cuotas_cumple=(
            garantia["condicion_distribucion_cuotas_cumple"]
        ),
        cuotas_objetivo_distribucion=garantia["cuotas_objetivo_distribucion"],
        cuotas_minimas_por_tramo=garantia["cuotas_minimas_por_tramo"],
        cuotas_primeros_20_anios=garantia["cuotas_primeros_20_anios"],
        cuotas_anios_restantes=garantia["cuotas_anios_restantes"],
        condicion_estabilidad_salarial_evaluada=bool(
            garantia["condicion_estabilidad_salarial_evaluada"]
        ),
        condicion_estabilidad_salarial_cumple=(
            garantia["condicion_estabilidad_salarial_cumple"]
        ),
        salario_promedio_base_mensual=(
            redondear_moneda(garantia["salario_promedio_base_mensual"])
            if garantia["salario_promedio_base_mensual"] is not None
            else None
        ),
        tasa_reemplazo_minima_pct_aplicable=(
            float(garantia["tasa_reemplazo_minima_pct_aplicable"])
            if garantia["tasa_reemplazo_minima_pct_aplicable"] is not None
            else None
        ),
        garantia_reemplazo_monto_objetivo=(
            redondear_moneda(garantia["garantia_reemplazo_monto_objetivo"])
            if garantia["garantia_reemplazo_monto_objetivo"] is not None
            else None
        ),
        garantia_reemplazo_complemento_mensual=(
            redondear_moneda(
                garantia["garantia_reemplazo_complemento_mensual"]
            )
            if garantia["garantia_reemplazo_complemento_mensual"] is not None
            else None
        ),
        calculo_total_disponible=bool(
            garantia["calculo_total_disponible"]
        ),
        pension_mensual_total_estimada=(
            redondear_moneda(garantia["pension_mensual_total_estimada"])
            if garantia["pension_mensual_total_estimada"] is not None
            else None
        ),
        advertencias=advertencias,
        fuente_normativa=_fuente_normativa(),
    )
