"""Pruebas del contrato transversal de salida de la Fase 6F.4."""

import unittest
from datetime import date
from types import SimpleNamespace

from app.services.resultado_unificado import (
    construir_resumen_unificado_mixto,
    construir_resumen_unificado_sebd,
    construir_resumen_unificado_sucgs,
)


class TestResultadoUnificado(unittest.TestCase):
    """Comprueba que mensualidades, pagos únicos y estados no se mezclen."""

    @staticmethod
    def _escenario(cuotas: int = 300):
        return SimpleNamespace(
            nombre="Edad de referencia",
            fecha_retiro=date(2026, 11, 16),
            edad_retiro_anios=57,
            cuotas_estimadas_totales=cuotas,
        )

    def test_sebd_indemnizacion_se_normaliza_como_pago_unico(self):
        calculo = SimpleNamespace(
            modalidad="INDEMNIZACION",
            modalidad_nombre="Indemnización por Vejez",
            elegible=True,
            calculo_disponible=True,
            pension_mensual_estimada=None,
            indemnizacion_pago_unico_estimado=12000.0,
            advertencias=[],
        )
        resultado = SimpleNamespace(
            escenario_retiro=self._escenario(120),
            escenario_salarial_nombre="Salario constante",
            advertencias_integracion=[],
            calculo=calculo,
        )

        resumen = construir_resumen_unificado_sebd(resultado)

        self.assertEqual(resumen.estado_resultado, "COMPLETO")
        self.assertEqual(resumen.naturaleza_prestacion, "PAGO_UNICO")
        self.assertIsNone(resumen.pension_mensual_estimada)
        self.assertEqual(resumen.pago_unico_estimado, 12000.0)

    def test_mixto_con_decision_pendiente_no_finge_resultado_completo(self):
        cap = SimpleNamespace(
            decision_requerida=True,
            bono_reconocimiento=0.0,
            bono_reconocimiento_confirmado_oficialmente=False,
            saldo_ahorro_personal=20000.0,
        )
        calculo = SimpleNamespace(
            componente_ahorro_personal=cap,
            estado_sistema="MIXTO_CALCULABLE",
            elegible=True,
            calculo_completo=False,
            modalidad="PROPORCIONAL",
            modalidad_nombre="Pensión de Retiro por Vejez Proporcional",
            pension_mensual_total_estimada=None,
            pago_unico_total_estimado=None,
            advertencias=[],
        )
        resultado = SimpleNamespace(
            escenario_retiro=self._escenario(200),
            escenario_salarial_nombre="Salario constante",
            advertencias_integracion=[],
            calculo=calculo,
        )

        resumen = construir_resumen_unificado_mixto(resultado)

        self.assertEqual(resumen.estado_resultado, "DECISION_REQUERIDA")
        self.assertTrue(resumen.requiere_decision_usuario)
        self.assertFalse(resumen.calculo_completo)
        self.assertEqual(resumen.naturaleza_prestacion, "SIN_MONTO")

    def test_sucgs_completo_conserva_477_como_pension_mensual(self):
        calculo = SimpleNamespace(
            cumple_edad_referencia=True,
            calculo_total_disponible=True,
            saldo_confirmado_oficialmente=True,
            valores_solidarios_confirmados_oficialmente=True,
            tipo_prestacion_solidaria="PENSION_CONTRIBUTIVA_SIN_COMPLEMENTO",
            pension_mensual_total_estimada=477.0,
            advertencias=[],
        )
        resultado = SimpleNamespace(
            escenario_retiro=self._escenario(300),
            escenario_salarial_nombre="Salario constante",
            advertencias_integracion=[],
            calculo=calculo,
        )

        resumen = construir_resumen_unificado_sucgs(resultado)

        self.assertEqual(resumen.estado_resultado, "COMPLETO")
        self.assertEqual(resumen.naturaleza_prestacion, "PENSION_MENSUAL")
        self.assertEqual(resumen.pension_mensual_estimada, 477.0)
        self.assertIsNone(resumen.pago_unico_estimado)


if __name__ == "__main__":
    unittest.main()
