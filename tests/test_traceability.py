"""Pruebas de la explicación transversal 6F.2 sin recalcular los motores."""

import unittest
from datetime import date
from types import SimpleNamespace

from app.services.trazabilidad import (
    construir_trazabilidad_mixto,
    construir_trazabilidad_sebd,
    construir_trazabilidad_sucgs,
)


class TestTrazabilidadCalculo(unittest.TestCase):
    """Valida fórmulas visibles, resultados finales y fuentes oficiales."""

    def test_sebd_normal_explica_base_tasa_y_resultado(self):
        calculo = SimpleNamespace(
            modalidad="NORMAL",
            modalidad_nombre="Pensión de Retiro por Vejez Normal",
            tipo_prestacion="PENSION",
            calculo_disponible=True,
            edad_retiro_anios=57,
            cuotas_totales=300,
            mejores_anios_requeridos=10,
            total_salarios_seleccionados=120000,
            salario_base_mensual=1000,
            tasa_base_pct=60,
            incremento_antes_referencia_pct=6.25,
            incremento_despues_referencia_pct=0,
            tasa_reemplazo_total_pct=66.25,
            monto_antes_limite_maximo=662.50,
            monto_despues_limite_maximo=662.50,
            factor_proporcional_cuotas=1.0,
            factor_reduccion_edad=1.0,
            monto_despues_factor_proporcional=662.50,
            pension_mensual_estimada=662.50,
            indemnizacion_pago_unico_estimado=None,
            indemnizacion_mensualidad_hipotetica=None,
            indemnizacion_divisor_cuotas=None,
            fecha_referencia=date(2026, 11, 16),
            advertencias=[],
        )
        resultado = SimpleNamespace(
            calculo=calculo,
            escenario_retiro=SimpleNamespace(
                fecha_retiro=date(2026, 11, 16),
                cuotas_estimadas_totales=300,
            ),
            escenario_salarial_nombre="Salario constante",
            advertencias_integracion=[],
        )

        traza = construir_trazabilidad_sebd(resultado)

        self.assertEqual(traza.resultado_final, "B/.662.50")
        self.assertEqual(traza.resultado_final_tipo, "MENSUAL")
        self.assertTrue(any("120" in (paso.formula or "") for paso in traza.pasos))
        self.assertTrue(any(fuente.url.startswith("https://") for fuente in traza.fuentes))

    def test_mixto_separa_bd_cap_y_suma_mensual(self):
        bd = SimpleNamespace(
            salario_mensual_maximo_participacion=500,
            salario_base_mensual=500,
            tasa_reemplazo_total_pct=66.25,
            pension_mensual_estimada=331.25,
            indemnizacion_pago_unico_estimado=None,
            advertencias=[],
        )
        cap = SimpleNamespace(
            saldo_ahorro_personal=100000,
            bono_reconocimiento=5000,
            bono_reconocimiento_confirmado_oficialmente=True,
            valor_actuarial_expectativa_vida=200,
            capital_total_considerado=105000,
            pension_programada_mensual=525,
            devolucion_pago_unico_estimado=None,
            decision_requerida=False,
            advertencias=[],
        )
        calculo = SimpleNamespace(
            componente_beneficio_definido=bd,
            componente_ahorro_personal=cap,
            pension_mensual_total_estimada=856.25,
            pago_unico_total_estimado=None,
            tipo_prestacion="PENSION",
            estado_sistema="MIXTO_CALCULABLE",
            advertencias=[],
        )
        resultado = SimpleNamespace(
            calculo=calculo,
            escenario_retiro=SimpleNamespace(cuotas_estimadas_totales=300),
            escenario_salarial_nombre="Salario constante",
            advertencias_integracion=[],
        )

        traza = construir_trazabilidad_mixto(resultado)

        self.assertEqual(traza.resultado_final, "B/.856.25")
        self.assertTrue(any("Componente BD + Componente CAP" == paso.formula for paso in traza.pasos))
        self.assertTrue(any("Seguros Colectivos" in fuente.titulo for fuente in traza.fuentes))

    def test_sucgs_explica_saldo_factor_y_articulo_197(self):
        calculo = SimpleNamespace(
            cuotas_totales=240,
            saldo_capitalizacion_solidaria=100000,
            saldo_confirmado_oficialmente=True,
            factor_pensionamiento_actuarial=4.77,
            divisor_formula=1000,
            pension_contributiva_mensual=477,
            garantia_solidaria_evaluada=True,
            complemento_solidario_mensual=0,
            pension_despues_componente_solidario=477,
            garantia_reemplazo_evaluada=True,
            garantia_reemplazo_aplica=True,
            condicion_minimo_cuotas_anuales_cumple=True,
            condicion_distribucion_cuotas_cumple=True,
            condicion_estabilidad_salarial_cumple=True,
            salario_promedio_base_mensual=1000,
            tasa_reemplazo_minima_pct_aplicable=60,
            garantia_reemplazo_monto_objetivo=600,
            garantia_reemplazo_complemento_mensual=123,
            pension_mensual_total_estimada=600,
            tipo_prestacion_solidaria="PENSION_CONTRIBUTIVA_SIN_COMPLEMENTO",
            tipo_calculo="SUCGS_COMPLETO_HASTA_ART197_6E3",
            advertencias=[],
        )
        resultado = SimpleNamespace(
            calculo=calculo,
            escenario_salarial_nombre="Salario constante",
            advertencias_integracion=[],
        )

        traza = construir_trazabilidad_sucgs(resultado)

        self.assertEqual(traza.resultado_final, "B/.600.00")
        self.assertTrue(any("Saldo ÷ 1,000 × factor actuarial" == paso.formula for paso in traza.pasos))
        self.assertTrue(any("artículo 197" in paso.regla.lower() for paso in traza.pasos))
        self.assertTrue(any("Ley 462" in fuente.titulo for fuente in traza.fuentes))


if __name__ == "__main__":
    unittest.main()
