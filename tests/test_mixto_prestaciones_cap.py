"""Pruebas de devolución, garantía y pagos únicos del CAP Mixto."""

import unittest
from datetime import date

from app.models.pension import DatosCalculoMixto
from app.models.simulacion import RegistroHistorialSalarial
from app.engines.mixto import calcular_mixto


def _historial_alto(cantidad_anios: int = 10) -> list[RegistroHistorialSalarial]:
    """Construye años completos con salario por encima del tope Mixto."""

    inicio = 2027 - cantidad_anios
    return [
        RegistroHistorialSalarial(
            anio=anio,
            cuotas=12,
            salario_cotizado=12000,
        )
        for anio in range(inicio, 2027)
    ]


class TestPrestacionesCAPMixto(unittest.TestCase):
    """Valida las reglas añadidas en 6D.2."""

    def test_pension_programada_informa_garantia_vitalicia(self):
        resultado = calcular_mixto(
            DatosCalculoMixto(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=300,
                registros=_historial_alto(),
                saldo_ahorro_personal=100000,
                valor_actuarial_expectativa_vida=200,
            )
        )

        cap = resultado.componente_ahorro_personal
        self.assertTrue(cap.calculo_disponible)
        self.assertEqual(cap.opcion_solicitada, "PENSION_PROGRAMADA")
        self.assertTrue(cap.garantia_renta_vitalicia_aplica)
        self.assertEqual(cap.garantia_monto_mensual, 500.0)
        self.assertEqual(cap.prima_renta_vitalicia_pct_referencia, 0.93)
        self.assertTrue(cap.prima_renta_vitalicia_es_referencia_historica)
        self.assertEqual(resultado.pension_mensual_total_estimada, 831.25)

    def test_proporcional_en_referencia_auto_exige_decision_cap(self):
        resultado = calcular_mixto(
            DatosCalculoMixto(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=200,
                registros=_historial_alto(),
                saldo_ahorro_personal=20000,
                valor_actuarial_expectativa_vida=200,
            )
        )

        cap = resultado.componente_ahorro_personal
        self.assertTrue(cap.devolucion_total_disponible)
        self.assertTrue(cap.decision_requerida)
        self.assertFalse(cap.calculo_disponible)
        self.assertEqual(resultado.tipo_prestacion, "DECISION_CAP_PENDIENTE")
        self.assertIsNone(resultado.pension_mensual_total_estimada)
        self.assertFalse(resultado.calculo_completo)

    def test_proporcional_puede_elegir_devolucion_total_cap(self):
        resultado = calcular_mixto(
            DatosCalculoMixto(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=200,
                registros=_historial_alto(),
                saldo_ahorro_personal=20000,
                opcion_prestacion_cap="DEVOLUCION_TOTAL",
            )
        )

        cap = resultado.componente_ahorro_personal
        self.assertTrue(cap.calculo_disponible)
        self.assertEqual(cap.devolucion_pago_unico_estimado, 20000.0)
        self.assertIsNone(cap.pension_programada_mensual)
        self.assertEqual(resultado.tipo_prestacion, "PENSION_MAS_DEVOLUCION_CAP")
        self.assertEqual(resultado.pension_mensual_total_estimada, 250.0)
        self.assertEqual(resultado.pago_unico_cap_estimado, 20000.0)
        self.assertEqual(resultado.pago_unico_total_estimado, 20000.0)
        self.assertTrue(resultado.calculo_completo)

    def test_indemnizacion_bd_mas_devolucion_cap_suma_pagos_unicos(self):
        resultado = calcular_mixto(
            DatosCalculoMixto(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=120,
                registros=_historial_alto(),
                saldo_ahorro_personal=10000,
                opcion_prestacion_cap="DEVOLUCION_TOTAL",
            )
        )

        bd = resultado.componente_beneficio_definido
        cap = resultado.componente_ahorro_personal

        # El historial BD queda limitado a B/.500 mensuales. La mensualidad
        # hipotética es B/.300 y 120/6 = 20, por lo que el BD paga B/.6,000.
        self.assertEqual(bd.indemnizacion_mensualidad_hipotetica, 300.0)
        self.assertEqual(bd.indemnizacion_pago_unico_estimado, 6000.0)
        self.assertEqual(cap.devolucion_pago_unico_estimado, 10000.0)
        self.assertEqual(resultado.tipo_prestacion, "INDEMNIZACION_MIXTA")
        self.assertIsNone(resultado.pension_mensual_total_estimada)
        self.assertEqual(resultado.pago_unico_bd_estimado, 6000.0)
        self.assertEqual(resultado.pago_unico_cap_estimado, 10000.0)
        self.assertEqual(resultado.pago_unico_total_estimado, 16000.0)
        self.assertTrue(resultado.calculo_completo)

    def test_devolucion_cap_no_procede_antes_de_edad_referencia(self):
        resultado = calcular_mixto(
            DatosCalculoMixto(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 10, 16),
                cuotas_totales=200,
                registros=_historial_alto(),
                saldo_ahorro_personal=20000,
                opcion_prestacion_cap="DEVOLUCION_TOTAL",
            )
        )

        cap = resultado.componente_ahorro_personal
        self.assertFalse(cap.devolucion_total_disponible)
        self.assertFalse(cap.calculo_disponible)
        self.assertIsNone(cap.devolucion_pago_unico_estimado)
        self.assertFalse(resultado.calculo_completo)

    def test_bono_no_confirmado_mantiene_total_provisional(self):
        resultado = calcular_mixto(
            DatosCalculoMixto(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=300,
                registros=_historial_alto(),
                saldo_ahorro_personal=100000,
                bono_reconocimiento=5000,
                valor_actuarial_expectativa_vida=200,
            )
        )

        self.assertEqual(resultado.pension_mensual_total_estimada, 856.25)
        self.assertFalse(resultado.calculo_completo)
        self.assertTrue(
            any(
                "bono de reconocimiento" in advertencia.lower()
                for advertencia in resultado.advertencias
            )
        )


if __name__ == "__main__":
    unittest.main()
