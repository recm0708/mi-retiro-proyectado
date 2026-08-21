"""Prepara parámetros versionados para la explicación pública del cálculo.

La guía no ejecuta prestaciones ni replica motores previsionales. Expone de
forma legible los parámetros que ya viven en ``normativa/`` para que la
plantilla pueda documentar el orden de operaciones implementado.
"""

from datetime import date

from app.core.normativa import (
    cargar_parametros_generales,
    cargar_parametros_mixto,
    cargar_parametros_sebd,
    cargar_parametros_sucgs,
)


def _formatear_fecha_iso(valor: str) -> str:
    """Convierte una fecha ISO versionada a formato visible DD/MM/YYYY."""

    return date.fromisoformat(valor).strftime("%d/%m/%Y")


def _formatear_moneda(valor: float | int) -> str:
    """Presenta un importe con símbolo balboa, miles y dos decimales."""

    return f"B/.{float(valor):,.2f}"


def construir_guia_calculo() -> dict:
    """Devuelve parámetros normativos necesarios para la guía explicativa."""

    generales = cargar_parametros_generales()
    sebd = cargar_parametros_sebd()
    mixto = cargar_parametros_mixto()
    sucgs = cargar_parametros_sucgs()

    sebd_vejez = sebd["pension_vejez"]
    mixto_bd = mixto["componente_beneficio_definido"]
    mixto_cap = mixto["componente_ahorro_personal"]
    sucgs_contributivo = sucgs["componente_contributivo"]
    sucgs_garantias = sucgs["garantias"]
    reemplazo = sucgs_garantias["reemplazo_minimo_art197"]

    factores_anticipacion = [
        {
            "mes_desde_limite": int(mes),
            "factor": float(factor),
        }
        for mes, factor in sorted(
            sebd_vejez["retiro_anticipado"]
            ["tabla_factor_reduccion_meses_desde_limite_inferior"].items(),
            key=lambda item: int(item[0]),
        )
    ]

    factores_sucgs = [
        {
            "edad": edad.replace("_mas", "+"),
            "factor": float(factor),
        }
        for edad, factor in sucgs_contributivo[
            "factores_pensionamiento_actuarial"
        ].items()
    ]

    maximos = sebd_vejez["montos_maximos_sebd"]

    return {
        "version_normativa": generales["version"],
        "fuente_general": generales["fuente"],
        "gaceta_oficial": generales["gaceta_oficial"],
        "fecha_gaceta": generales["fecha_gaceta"],
        "fecha_gaceta_visible": _formatear_fecha_iso(generales["fecha_gaceta"]),
        "edades_referencia": generales["edades_referencia"],
        "sebd": {
            "cuotas_referencia": int(sebd_vejez["cuotas_referencia"]),
            "cuotas_minimas_proporcional": int(
                sebd_vejez["cuotas_minimas_proporcional"]
            ),
            "mejores_anios_base": int(sebd_vejez["mejores_anios_base"]),
            "tasa_base_pct": float(sebd_vejez["tasa_reemplazo_base_pct"]),
            "incremento_antes_pct": float(
                sebd_vejez["incremento_12_cuotas_antes_referencia_pct"]
            ),
            "incremento_despues_pct": float(
                sebd_vejez["incremento_12_cuotas_despues_referencia_pct"]
            ),
            "maximo_meses_anticipacion": int(
                sebd_vejez["retiro_anticipado"]["maximo_meses_anticipacion"]
            ),
            "factores_anticipacion": factores_anticipacion,
            "maximos": [
                {
                    "nivel": "Ordinario",
                    "cuotas_minimas": None,
                    "promedio_minimo": None,
                    "promedio_minimo_visible": None,
                    "mejores_anios": int(maximos["ordinario"]["mejores_anios_base"]),
                    "monto_maximo": float(maximos["ordinario"]["monto_maximo"]),
                    "monto_maximo_visible": _formatear_moneda(
                        maximos["ordinario"]["monto_maximo"]
                    ),
                },
                {
                    "nivel": "Ampliado",
                    "cuotas_minimas": int(maximos["ampliado_2000"]["cuotas_minimas"]),
                    "promedio_minimo": float(
                        maximos["ampliado_2000"]["promedio_mensual_minimo"]
                    ),
                    "promedio_minimo_visible": _formatear_moneda(
                        maximos["ampliado_2000"]["promedio_mensual_minimo"]
                    ),
                    "mejores_anios": int(
                        maximos["ampliado_2000"]["mejores_anios_base"]
                    ),
                    "monto_maximo": float(maximos["ampliado_2000"]["monto_maximo"]),
                    "monto_maximo_visible": _formatear_moneda(
                        maximos["ampliado_2000"]["monto_maximo"]
                    ),
                },
                {
                    "nivel": "Ampliado superior",
                    "cuotas_minimas": int(maximos["ampliado_2500"]["cuotas_minimas"]),
                    "promedio_minimo": float(
                        maximos["ampliado_2500"]["promedio_mensual_minimo"]
                    ),
                    "promedio_minimo_visible": _formatear_moneda(
                        maximos["ampliado_2500"]["promedio_mensual_minimo"]
                    ),
                    "mejores_anios": int(
                        maximos["ampliado_2500"]["mejores_anios_base"]
                    ),
                    "monto_maximo": float(maximos["ampliado_2500"]["monto_maximo"]),
                    "monto_maximo_visible": _formatear_moneda(
                        maximos["ampliado_2500"]["monto_maximo"]
                    ),
                },
            ],
            "indemnizacion_divisor": int(
                sebd_vejez["indemnizacion_vejez"]["divisor_meses_cotizados"]
            ),
            "indemnizacion_fin": sebd_vejez["indemnizacion_vejez"][
                "fecha_fin_regimen"
            ],
            "indemnizacion_fin_visible": _formatear_fecha_iso(
                sebd_vejez["indemnizacion_vejez"]["fecha_fin_regimen"]
            ),
        },
        "mixto": {
            "tope_salarial_bd": float(
                mixto_bd["salario_mensual_maximo_participacion"]
            ),
            "tope_salarial_bd_visible": _formatear_moneda(
                mixto_bd["salario_mensual_maximo_participacion"]
            ),
            "mejores_anios_bd": int(mixto_bd["mejores_anios_base"]),
            "cuotas_referencia": int(mixto_bd["cuotas_referencia"]),
            "cuotas_minimas_proporcional": int(
                mixto_bd["cuotas_minimas_proporcional"]
            ),
            "tasa_base_pct": float(mixto_bd["tasa_reemplazo_base_pct"]),
            "incremento_antes_pct": float(
                mixto_bd["incremento_12_cuotas_antes_referencia_pct"]
            ),
            "incremento_despues_pct": float(
                mixto_bd["incremento_12_cuotas_despues_referencia_pct"]
            ),
            "monto_maximo_bd": float(mixto_bd["monto_maximo_mensual"]),
            "monto_maximo_bd_visible": _formatear_moneda(
                mixto_bd["monto_maximo_mensual"]
            ),
            "formula_cap": mixto_cap["formula_pension_programada"],
            "requiere_actuarial": bool(
                mixto_cap["requiere_parametros_actuariales_vigentes"]
            ),
            "fecha_fin_mixto": mixto["transicion"][
                "fecha_fin_calculo_bajo_mixto"
            ],
            "fecha_fin_mixto_visible": _formatear_fecha_iso(
                mixto["transicion"]["fecha_fin_calculo_bajo_mixto"]
            ),
            "fecha_inicio_sucgs": mixto["transicion"][
                "fecha_inicio_calculo_bajo_sucgs"
            ],
            "fecha_inicio_sucgs_visible": _formatear_fecha_iso(
                mixto["transicion"]["fecha_inicio_calculo_bajo_sucgs"]
            ),
            "nota_transicion": mixto["transicion"]["nota_discrepancia"],
        },
        "sucgs": {
            "divisor": int(sucgs_contributivo["divisor_formula"]),
            "factores": factores_sucgs,
            "actualizacion_factores_anios": int(
                sucgs_contributivo["actualizacion_factores"]
                ["periodicidad_maxima_anios"]
            ),
            "cuotas_referencia": int(sucgs_garantias["cuotas_referencia"]),
            "pgs_referencia": float(
                sucgs_garantias["pension_garantizada_solidaria_base"]
            ),
            "pgs_referencia_visible": _formatear_moneda(
                sucgs_garantias["pension_garantizada_solidaria_base"]
            ),
            "minimo_universal_referencia": float(
                sucgs_garantias["valor_minimo_universal_referencia"]
            ),
            "minimo_universal_referencia_visible": _formatear_moneda(
                sucgs_garantias["valor_minimo_universal_referencia"]
            ),
            "edad_solidaria": int(
                sucgs_garantias["edad_referencia_componente_solidario"]
            ),
            "tasa_reemplazo_minima_pct": float(
                reemplazo["tasa_reemplazo_minima_pct"]
            ),
            "cuotas_minimas_garantia_proporcional": int(
                reemplazo["cuotas_minimas_garantia_proporcional"]
            ),
            "cuotas_minimas_por_anio_activo": int(
                reemplazo["cuotas_minimas_por_anio_activo"]
            ),
            "max_anios_sin_cotizacion": int(
                reemplazo["max_anios_sin_cotizacion"]
            ),
            "max_anios_sin_cotizacion_consecutivos": int(
                reemplazo["max_anios_sin_cotizacion_consecutivos"]
            ),
            "primeros_anios_distribucion": int(
                reemplazo["primeros_anios_distribucion"]
            ),
            "proporcion_minima_por_tramo": float(
                reemplazo["proporcion_minima_por_tramo"]
            ),
            "estabilidad_modo": reemplazo["estabilidad_salarial"][
                "modo_aplicacion"
            ],
        },
    }
