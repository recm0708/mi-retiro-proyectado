"""Construcción de la trazabilidad explicable de los motores de pensión.

Este módulo no contiene fórmulas jurídicas nuevas. Recibe resultados ya
calculados y crea una representación humana de la cadena de cálculo para la
interfaz de trazabilidad. Las URLs se toman de ``normativa/*.json`` para evitar que la
interfaz mantenga enlaces legales hardcodeados.
"""

from decimal import Decimal

from app.core.normativa import (
    cargar_parametros_mixto,
    cargar_parametros_sebd,
    cargar_parametros_sucgs,
)
from app.modelos.pension import (
    ResumenResultadoMixto,
    ResumenResultadoSEBD,
    ResumenResultadoSUCGS,
)
from app.modelos.trazabilidad import (
    DatoTrazabilidad,
    FuenteTrazabilidad,
    PasoTrazabilidad,
    ResumenTrazabilidadCalculo,
)


def _moneda(valor: float | int | Decimal | None) -> str:
    """Formatea un importe para la explicación humana de trazabilidad."""

    if valor is None:
        return "No aplica"
    return f"B/.{float(valor):,.2f}"


def _numero(valor: float | int | Decimal | None, decimales: int = 2) -> str:
    """Formatea un número técnico sin ceros decimales innecesarios."""

    if valor is None:
        return "No aplica"
    numero = float(valor)
    texto = f"{numero:,.{decimales}f}"
    if decimales > 0:
        texto = texto.rstrip("0").rstrip(".")
    return texto


def _porcentaje(valor: float | int | Decimal | None) -> str:
    """Formatea un porcentaje para una sustitución explicativa."""

    if valor is None:
        return "No aplica"
    return f"{float(valor):.2f} %"


def _fuente(
    identificador: str,
    titulo: str,
    referencia: str,
    url: str,
    articulos: list[str],
    nota: str | None = None,
) -> FuenteTrazabilidad:
    """Construye una referencia normativa normalizada para la trazabilidad."""

    return FuenteTrazabilidad(
        id=identificador,
        titulo=titulo,
        referencia=referencia,
        url=url,
        articulos=articulos,
        nota=nota,
    )


def _fuentes_comunes(urls: dict) -> list[FuenteTrazabilidad]:
    """Construye las fuentes legales transversales compartidas por los motores."""

    return [
        _fuente(
            "texto_unico",
            "Texto Único de la Ley 51 de 2005",
            "Gaceta Oficial 30284-B de 22/05/2025",
            urls["texto_unico_css"],
            [],
            "Texto consolidado con las reformas incorporadas hasta la Ley 462 de 2025.",
        ),
        _fuente(
            "normativa_css",
            "Normativa de Prestaciones Económicas — CSS",
            "Portal oficial de reglamentos y resoluciones",
            urls["normativa_prestaciones_economicas_css"],
            [],
        ),
    ]


def construir_trazabilidad_sebd(
    resultado: ResumenResultadoSEBD,
) -> ResumenTrazabilidadCalculo:
    """Convierte un resultado SEBD en una cadena explicativa auditable."""

    calculo = resultado.calculo
    # La trazabilidad toma el resultado ya calculado y solo recupera fuentes
    # normativas para explicar el origen de cada paso visible.
    parametros = cargar_parametros_sebd()
    urls = parametros["fuentes_oficiales"]

    fuentes = _fuentes_comunes(urls)
    fuentes.append(
        _fuente(
            "reglamento_calculo",
            "Reglamento para el Cálculo de Prestaciones Económicas",
            "Resolución 39,302-2007-J.D. y modificaciones",
            urls["resolucion_39302_2007_jd"],
            ["Reglamento de cálculo"],
        )
    )

    # Datos de entrada resumidos: permiten que el usuario identifique de dónde
    # sale la cadena explicativa sin exponer todo el contrato interno.
    # Los datos iniciales contextualizan edad, cuotas y saldo sin exponer el
    # detalle completo de la simulación del usuario.
    datos = [
        DatoTrazabilidad(
            clave="fecha_retiro",
            etiqueta="Fecha de retiro evaluada",
            valor=calculo.fecha_referencia.isoformat()
            if resultado.escenario_retiro.fecha_retiro is None
            else resultado.escenario_retiro.fecha_retiro.isoformat(),
            origen="Paso 5 — escenario de retiro",
        ),
        DatoTrazabilidad(
            clave="cuotas",
            etiqueta="Cuotas estimadas al retiro",
            valor=str(calculo.cuotas_totales),
            origen="Pasos 2 y 5 — cuotas históricas y proyectadas",
        ),
        DatoTrazabilidad(
            clave="escenario_salarial",
            etiqueta="Escenario salarial",
            valor=resultado.escenario_salarial_nombre,
            origen="Paso 4 — trayectoria salarial",
        ),
    ]

    # Los pasos se agregan en el mismo orden en que una persona revisaría el
    # cálculo: elegibilidad, base salarial, tasa, límites y resultado.
    pasos: list[PasoTrazabilidad] = [
        PasoTrazabilidad(
            orden=1,
            titulo="Determinar modalidad y elegibilidad",
            regla=(
                f"Con {calculo.edad_retiro_anios} años y {calculo.cuotas_totales} "
                f"cuotas, el motor clasifica la prestación como "
                f"{calculo.modalidad_nombre}."
            ),
            resultado=calculo.modalidad_nombre,
            fuentes=["texto_unico"],
        )
    ]

    if calculo.calculo_disponible:
        # Solo se describen fórmulas cuando el motor declaró cálculo disponible;
        # en caso contrario la trazabilidad queda como explicación de no cálculo.
        pasos.append(
            PasoTrazabilidad(
                orden=len(pasos) + 1,
                titulo="Formar el salario base",
                regla=(
                    f"Se utilizan los {calculo.mejores_anios_requeridos} años "
                    "con mayor salario cotizado disponibles para la base legal."
                ),
                formula=(
                    "Total de salarios seleccionados ÷ 120 meses"
                    if calculo.mejores_anios_requeridos == 10
                    else "Promedio mensual según historial aplicable"
                ),
                sustitucion=(
                    f"{_moneda(calculo.total_salarios_seleccionados)} ÷ 120"
                    if calculo.mejores_anios_requeridos == 10
                    else None
                ),
                resultado=_moneda(calculo.salario_base_mensual),
                redondeo="Los importes monetarios finales se presentan a dos decimales.",
                fuentes=["texto_unico", "reglamento_calculo"],
            )
        )

        pasos.append(
            PasoTrazabilidad(
                orden=len(pasos) + 1,
                titulo="Construir la tasa de reemplazo",
                regla=(
                    f"Tasa base {_porcentaje(calculo.tasa_base_pct)}; "
                    f"incremento antes de referencia "
                    f"{_porcentaje(calculo.incremento_antes_referencia_pct)}; "
                    f"incremento después de referencia "
                    f"{_porcentaje(calculo.incremento_despues_referencia_pct)}."
                ),
                formula="Tasa base + incrementos aplicables por bloques completos de 12 cuotas",
                sustitucion=(
                    f"{_porcentaje(calculo.tasa_base_pct)} + "
                    f"{_porcentaje(calculo.incremento_antes_referencia_pct)} + "
                    f"{_porcentaje(calculo.incremento_despues_referencia_pct)}"
                ),
                resultado=_porcentaje(calculo.tasa_reemplazo_total_pct),
                fuentes=["texto_unico"],
            )
        )

        pasos.append(
            PasoTrazabilidad(
                orden=len(pasos) + 1,
                titulo="Calcular monto antes de factores de modalidad",
                regla="Se multiplica el salario base por la tasa de reemplazo resultante.",
                formula="Salario base × tasa de reemplazo",
                sustitucion=(
                    f"{_moneda(calculo.salario_base_mensual)} × "
                    f"{_porcentaje(calculo.tasa_reemplazo_total_pct)}"
                ),
                resultado=_moneda(calculo.monto_antes_limite_maximo),
                fuentes=["texto_unico"],
            )
        )

        if calculo.factor_proporcional_cuotas not in (None, 1.0):
            pasos.append(
                PasoTrazabilidad(
                    orden=len(pasos) + 1,
                    titulo="Aplicar proporcionalidad por cuotas",
                    regla="La modalidad proporcional ajusta el monto por la relación de cuotas acreditadas respecto de 240.",
                    formula="Monto previo × factor proporcional",
                    sustitucion=(
                        f"{_moneda(calculo.monto_despues_limite_maximo)} × "
                        f"{_numero(calculo.factor_proporcional_cuotas, 6)}"
                    ),
                    resultado=_moneda(calculo.monto_despues_factor_proporcional),
                    fuentes=["texto_unico"],
                )
            )

        if calculo.factor_reduccion_edad not in (0.0, 1.0):
            base_factor = (
                calculo.monto_despues_factor_proporcional
                if calculo.monto_despues_factor_proporcional is not None
                else calculo.monto_despues_limite_maximo
            )
            pasos.append(
                PasoTrazabilidad(
                    orden=len(pasos) + 1,
                    titulo="Aplicar factor por retiro anticipado",
                    regla=(
                        f"Se usa el factor mensual de reducción "
                        f"{_numero(calculo.factor_reduccion_edad, 6)} para la fecha anticipada."
                    ),
                    formula="Monto previo × factor de reducción por edad",
                    sustitucion=(
                        f"{_moneda(base_factor)} × "
                        f"{_numero(calculo.factor_reduccion_edad, 6)}"
                    ),
                    resultado=_moneda(calculo.pension_mensual_estimada),
                    fuentes=["texto_unico", "reglamento_calculo"],
                )
            )

        if calculo.indemnizacion_pago_unico_estimado is not None:
            pasos.append(
                PasoTrazabilidad(
                    orden=len(pasos) + 1,
                    titulo="Convertir la mensualidad hipotética en indemnización",
                    regla=(
                        "La indemnización es un pago único: se multiplica la mensualidad "
                        "hipotética por las cuotas acreditadas divididas entre seis."
                    ),
                    formula="Mensualidad hipotética × (cuotas ÷ 6)",
                    sustitucion=(
                        f"{_moneda(calculo.indemnizacion_mensualidad_hipotetica)} × "
                        f"({calculo.cuotas_totales} ÷ {calculo.indemnizacion_divisor_cuotas})"
                    ),
                    resultado=_moneda(calculo.indemnizacion_pago_unico_estimado),
                    fuentes=["texto_unico", "reglamento_calculo"],
                )
            )

    if calculo.indemnizacion_pago_unico_estimado is not None:
        etiqueta = "Indemnización por Vejez estimada"
        final = _moneda(calculo.indemnizacion_pago_unico_estimado)
        tipo = "PAGO_UNICO"
    elif calculo.pension_mensual_estimada is not None:
        etiqueta = "Pensión mensual estimada"
        final = _moneda(calculo.pension_mensual_estimada)
        tipo = "MENSUAL"
    else:
        etiqueta = "Resultado"
        final = "Pendiente / no calculable con los datos actuales"
        tipo = "PENDIENTE"

    # El resumen final queda serializable para la interfaz y mantiene fuentes,
    # datos y pasos separados para navegación y auditoría humana.
    return ResumenTrazabilidadCalculo(
        sistema="SEBD",
        tipo_prestacion=calculo.tipo_prestacion,
        datos_utilizados=datos,
        pasos=pasos,
        resultado_final_etiqueta=etiqueta,
        resultado_final=final,
        resultado_final_tipo=tipo,
        fuentes=fuentes,
        advertencias=(
            list(resultado.advertencias_integracion)
            + list(calculo.advertencias)
        ),
    )


def construir_trazabilidad_mixto(
    resultado: ResumenResultadoMixto,
) -> ResumenTrazabilidadCalculo:
    """Construye la explicación separada de los componentes BD y CAP."""

    calculo = resultado.calculo
    # En Mixto se explican dos componentes: beneficio definido y ahorro
    # personal, sin recalcularlos ni mezclar sus advertencias.
    parametros = cargar_parametros_mixto()
    urls = parametros["fuentes_oficiales"]
    fuentes = _fuentes_comunes(urls)
    fuentes.extend(
        [
            _fuente(
                "reglamento_mixto",
                "Reglamento de Incorporación al Subsistema Mixto",
                "Reglamento y resoluciones de incorporación",
                urls["reglamento_incorporacion_mixto"],
                ["Subsistema Mixto"],
            ),
            _fuente(
                "seguros_cap",
                "Reglamento de Seguros Colectivos del CAP",
                "Subsistema Mixto",
                urls["reglamento_seguros_colectivos_cap"],
                ["Seguro Colectivo de Renta Vitalicia"],
            ),
        ]
    )

    bd = calculo.componente_beneficio_definido
    cap = calculo.componente_ahorro_personal
    datos = [
        DatoTrazabilidad(
            clave="cuotas",
            etiqueta="Cuotas estimadas al retiro",
            valor=str(resultado.escenario_retiro.cuotas_estimadas_totales),
            origen="Pasos 2 y 5",
        ),
        DatoTrazabilidad(
            clave="escenario_salarial",
            etiqueta="Escenario salarial",
            valor=resultado.escenario_salarial_nombre,
            origen="Paso 4",
        ),
    ]
    if cap is not None:
        datos.extend(
            [
                DatoTrazabilidad(
                    clave="saldo_cap",
                    etiqueta="Saldo CAP",
                    valor=_moneda(cap.saldo_ahorro_personal),
                    origen="Paso 6 — dato específico Mixto",
                ),
                DatoTrazabilidad(
                    clave="bono",
                    etiqueta="Bono de reconocimiento",
                    valor=_moneda(cap.bono_reconocimiento),
                    origen="Paso 6 — dato específico Mixto",
                    confirmado=cap.bono_reconocimiento_confirmado_oficialmente,
                ),
                DatoTrazabilidad(
                    clave="valor_actuarial",
                    etiqueta="Valor actuarial de expectativa de vida",
                    valor=_numero(cap.valor_actuarial_expectativa_vida, 6),
                    origen="Paso 6 — divisor actuarial informado",
                ),
            ]
        )

    pasos: list[PasoTrazabilidad] = []
    if bd is not None:
        pasos.append(
            PasoTrazabilidad(
                orden=len(pasos) + 1,
                titulo="Calcular el Componente de Beneficio Definido",
                regla=(
                    "El tramo salarial que participa en el componente definido se "
                    f"limita a {_moneda(bd.salario_mensual_maximo_participacion)} mensuales."
                ),
                formula="Salario base BD × tasa resultante del componente definido",
                sustitucion=(
                    f"{_moneda(bd.salario_base_mensual)} × "
                    f"{_porcentaje(bd.tasa_reemplazo_total_pct)}"
                ),
                resultado=(
                    _moneda(bd.pension_mensual_estimada)
                    if bd.pension_mensual_estimada is not None
                    else _moneda(bd.indemnizacion_pago_unico_estimado)
                ),
                fuentes=["texto_unico", "reglamento_mixto"],
            )
        )

    if cap is not None:
        if cap.pension_programada_mensual is not None:
            pasos.append(
                PasoTrazabilidad(
                    orden=len(pasos) + 1,
                    titulo="Calcular la pensión programada del CAP",
                    regla="El capital disponible del CAP se divide entre el valor actuarial aplicable.",
                    formula="(Saldo CAP + bono aplicable) ÷ valor actuarial",
                    sustitucion=(
                        f"{_moneda(cap.capital_total_considerado)} ÷ "
                        f"{_numero(cap.valor_actuarial_expectativa_vida, 6)}"
                    ),
                    resultado=_moneda(cap.pension_programada_mensual),
                    fuentes=["texto_unico"],
                )
            )
        elif cap.devolucion_pago_unico_estimado is not None:
            pasos.append(
                PasoTrazabilidad(
                    orden=len(pasos) + 1,
                    titulo="Determinar devolución total del CAP",
                    regla="Cuando corresponde y se selecciona expresamente, el CAP se devuelve como pago único.",
                    formula="Saldo CAP + bono aplicable",
                    sustitucion=_moneda(cap.capital_total_considerado),
                    resultado=_moneda(cap.devolucion_pago_unico_estimado),
                    fuentes=["texto_unico"],
                )
            )
        elif cap.decision_requerida:
            pasos.append(
                PasoTrazabilidad(
                    orden=len(pasos) + 1,
                    titulo="Resolver decisión del CAP",
                    regla="La aplicación no elige por el Asegurado(a) cuando la devolución total requiere una decisión expresa.",
                    resultado="Decisión pendiente",
                    fuentes=["texto_unico"],
                )
            )

    if (
        calculo.pension_mensual_total_estimada is not None
        and bd is not None
        and cap is not None
        and cap.pension_programada_mensual is not None
    ):
        pasos.append(
            PasoTrazabilidad(
                orden=len(pasos) + 1,
                titulo="Sumar componentes mensuales",
                regla="La prestación mensual Mixto suma el componente definido y la pensión programada del CAP.",
                formula="Componente BD + Componente CAP",
                sustitucion=(
                    f"{_moneda(bd.pension_mensual_estimada)} + "
                    f"{_moneda(cap.pension_programada_mensual)}"
                ),
                resultado=_moneda(calculo.pension_mensual_total_estimada),
                fuentes=["texto_unico"],
            )
        )

    mensual = calculo.pension_mensual_total_estimada
    unico = calculo.pago_unico_total_estimado
    if mensual is not None and unico is not None:
        etiqueta = "Pensión mensual y pago único estimados"
        final = f"{_moneda(mensual)} mensuales + {_moneda(unico)} de pago único"
        tipo = "MENSUAL_Y_PAGO_UNICO"
    elif mensual is not None:
        etiqueta = "Pensión mensual Mixto estimada"
        final = _moneda(mensual)
        tipo = "MENSUAL"
    elif unico is not None:
        etiqueta = "Pago único Mixto estimado"
        final = _moneda(unico)
        tipo = "PAGO_UNICO"
    else:
        etiqueta = "Resultado Mixto"
        final = "Pendiente / no calculable con los datos actuales"
        tipo = "PENDIENTE"

    # Mixto devuelve una narrativa compuesta; la interfaz decide cómo agrupar
    # visualmente los pasos, no este servicio.
    return ResumenTrazabilidadCalculo(
        sistema="MIXTO",
        tipo_prestacion=calculo.tipo_prestacion or calculo.estado_sistema,
        datos_utilizados=datos,
        pasos=pasos,
        resultado_final_etiqueta=etiqueta,
        resultado_final=final,
        resultado_final_tipo=tipo,
        fuentes=fuentes,
        advertencias=(
            list(resultado.advertencias_integracion)
            + list(calculo.advertencias)
            + (list(bd.advertencias) if bd else [])
            + (list(cap.advertencias) if cap else [])
        ),
    )


def construir_trazabilidad_sucgs(
    resultado: ResumenResultadoSUCGS,
) -> ResumenTrazabilidadCalculo:
    """Construye la cadena contributiva, solidaria y de garantía SUCGS."""

    calculo = resultado.calculo
    # SUCGS combina saldo contributivo, garantías y advertencias solidarias;
    # la trazabilidad conserva esas capas en pasos separados.
    parametros = cargar_parametros_sucgs()
    urls = parametros["fuentes_oficiales"]
    fuentes = _fuentes_comunes(urls)
    fuentes.extend(
        [
            _fuente(
                "ley_462",
                "Ley 462 de 2025",
                "Reforma de la Ley Orgánica de la CSS",
                urls["ley_462_2025"],
                ["194", "195", "196", "197", "198"],
            ),
            _fuente(
                "reglamento_cccs",
                "Reglamento de Incorporación al Componente Contributivo de Capitalización Solidaria",
                "Resolución 57,805-2025-J.D.",
                urls["reglamento_incorporacion_cccs"],
                ["Transición / incorporación"],
            ),
        ]
    )

    datos = [
        DatoTrazabilidad(
            clave="cuotas",
            etiqueta="Cuotas estimadas al retiro",
            valor=str(calculo.cuotas_totales),
            origen="Pasos 2 y 5",
        ),
        DatoTrazabilidad(
            clave="saldo_solidario",
            etiqueta="Saldo de Capitalización Solidaria",
            valor=_moneda(calculo.saldo_capitalizacion_solidaria),
            origen="Paso 6 — saldo informado",
            confirmado=calculo.saldo_confirmado_oficialmente,
        ),
        DatoTrazabilidad(
            clave="factor",
            etiqueta="Factor actuarial por edad",
            valor=_numero(calculo.factor_pensionamiento_actuarial, 4),
            origen="Artículo 196 — tabla versionada",
        ),
        DatoTrazabilidad(
            clave="escenario_salarial",
            etiqueta="Escenario salarial",
            valor=resultado.escenario_salarial_nombre,
            origen="Paso 4",
        ),
    ]

    pasos: list[PasoTrazabilidad] = []
    if calculo.pension_contributiva_mensual is not None:
        pasos.append(
            PasoTrazabilidad(
                orden=1,
                titulo="Calcular el componente contributivo",
                regla="El artículo 196 convierte el saldo acumulado usando el divisor 1,000 y el factor actuarial correspondiente a la edad.",
                formula="Saldo ÷ 1,000 × factor actuarial",
                sustitucion=(
                    f"{_moneda(calculo.saldo_capitalizacion_solidaria)} ÷ "
                    f"{calculo.divisor_formula:,} × "
                    f"{_numero(calculo.factor_pensionamiento_actuarial, 4)}"
                ),
                resultado=_moneda(calculo.pension_contributiva_mensual),
                fuentes=["texto_unico", "ley_462"],
            )
        )

    if calculo.garantia_solidaria_evaluada:
        pasos.append(
            PasoTrazabilidad(
                orden=len(pasos) + 1,
                titulo="Evaluar la capa solidaria",
                regla=(
                    "Se revisan el Componente Solidario No Contributivo y la "
                    "Pensión Garantizada Solidaria según edad, cuotas y montos vigentes."
                ),
                formula="Prestación contributiva + complemento solidario aplicable",
                sustitucion=(
                    f"{_moneda(calculo.pension_contributiva_mensual)} + "
                    f"{_moneda(calculo.complemento_solidario_mensual)}"
                ),
                resultado=_moneda(calculo.pension_despues_componente_solidario),
                fuentes=["texto_unico", "ley_462"],
            )
        )

    if calculo.garantia_reemplazo_evaluada:
        if calculo.garantia_reemplazo_aplica:
            pasos.append(
                PasoTrazabilidad(
                    orden=len(pasos) + 1,
                    titulo="Aplicar garantía de reemplazo mínimo",
                    regla=(
                        "Cumplidas las condiciones evaluables del artículo 197 y la "
                        "confirmación de estabilidad salarial, se compara la prestación "
                        "previa con el mínimo de reemplazo aplicable."
                    ),
                    formula="Salario promedio base × tasa mínima aplicable",
                    sustitucion=(
                        f"{_moneda(calculo.salario_promedio_base_mensual)} × "
                        f"{_porcentaje(calculo.tasa_reemplazo_minima_pct_aplicable)}"
                    ),
                    resultado=(
                        f"Objetivo {_moneda(calculo.garantia_reemplazo_monto_objetivo)}; "
                        f"complemento {_moneda(calculo.garantia_reemplazo_complemento_mensual)}"
                    ),
                    fuentes=["texto_unico", "ley_462"],
                )
            )
        else:
            razones: list[str] = []
            if calculo.condicion_minimo_cuotas_anuales_cumple is False:
                razones.append("mínimo anual / años sin cotización")
            if calculo.condicion_distribucion_cuotas_cumple is False:
                razones.append("distribución 50 % / 50 %")
            if calculo.condicion_estabilidad_salarial_cumple is False:
                razones.append("estabilidad salarial")
            pasos.append(
                PasoTrazabilidad(
                    orden=len(pasos) + 1,
                    titulo="Evaluar garantía de reemplazo mínimo",
                    regla="La garantía del artículo 197 solo se aplica si se cumplen sus condiciones.",
                    resultado=(
                        "No aplica"
                        + (f": {', '.join(razones)}" if razones else "")
                    ),
                    fuentes=["texto_unico", "ley_462"],
                )
            )
    else:
        pasos.append(
            PasoTrazabilidad(
                orden=len(pasos) + 1,
                titulo="Garantía de reemplazo pendiente",
                regla="Faltan datos o confirmaciones para cerrar la evaluación del artículo 197.",
                resultado="Pendiente",
                fuentes=["texto_unico", "ley_462"],
            )
        )

    if calculo.pension_mensual_total_estimada is not None:
        etiqueta = "Pensión mensual SUCGS estimada"
        final = _moneda(calculo.pension_mensual_total_estimada)
        tipo = "MENSUAL"
    else:
        etiqueta = "Resultado SUCGS"
        final = "Pendiente / cálculo total no disponible"
        tipo = "PENDIENTE"

    # La salida conserva las advertencias del motor para que la interfaz no
    # convierta una estimación limitada en dictamen oficial.
    return ResumenTrazabilidadCalculo(
        sistema="SUCGS",
        tipo_prestacion=calculo.tipo_prestacion_solidaria or calculo.tipo_calculo,
        datos_utilizados=datos,
        pasos=pasos,
        resultado_final_etiqueta=etiqueta,
        resultado_final=final,
        resultado_final_tipo=tipo,
        fuentes=fuentes,
        advertencias=(
            list(resultado.advertencias_integracion)
            + list(calculo.advertencias)
        ),
    )
