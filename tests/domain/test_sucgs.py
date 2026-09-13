"""Pruebas del componente contributivo base del SUCGS."""

import unittest
from datetime import date

from app.models.pension import DatosCalculoSUCGS
from app.engines.sucgs import calcular_sucgs


class TestSUCGS(unittest.TestCase):
    """Valida la fórmula y la tabla actuarial del artículo 196."""

    def test_mujer_57_factor_4_77(self):
        resultado = calcular_sucgs(
            DatosCalculoSUCGS(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=300,
                saldo_capitalizacion_solidaria=100000,
                saldo_confirmado_oficialmente=True,
            )
        )

        self.assertTrue(resultado.calculo_contributivo_disponible)
        self.assertEqual(resultado.factor_pensionamiento_actuarial, 4.77)
        self.assertEqual(resultado.pension_contributiva_mensual, 477.00)
        self.assertTrue(resultado.garantia_solidaria_evaluada)
        self.assertEqual(
            resultado.tipo_prestacion_solidaria,
            "PENSION_CONTRIBUTIVA_SIN_COMPLEMENTO",
        )
        self.assertEqual(
            resultado.pension_despues_componente_solidario,
            477.00,
        )
        self.assertFalse(resultado.calculo_total_disponible)
        self.assertIsNone(resultado.pension_mensual_total_estimada)

    def test_hombre_62_factor_5_15(self):
        resultado = calcular_sucgs(
            DatosCalculoSUCGS(
                fecha_nacimiento=date(1964, 8, 11),
                sexo="MASCULINO",
                fecha_retiro=date(2026, 8, 11),
                cuotas_totales=300,
                saldo_capitalizacion_solidaria=100000,
                saldo_confirmado_oficialmente=True,
            )
        )

        self.assertEqual(resultado.edad_retiro_anios, 62)
        self.assertEqual(resultado.factor_pensionamiento_actuarial, 5.15)
        self.assertEqual(resultado.pension_contributiva_mensual, 515.00)

    def test_edad_80_o_mas_usa_factor_7_94(self):
        resultado = calcular_sucgs(
            DatosCalculoSUCGS(
                fecha_nacimiento=date(1940, 1, 1),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 1, 1),
                cuotas_totales=300,
                saldo_capitalizacion_solidaria=100000,
                saldo_confirmado_oficialmente=True,
            )
        )

        self.assertEqual(resultado.factor_pensionamiento_actuarial, 7.94)
        self.assertEqual(resultado.pension_contributiva_mensual, 794.00)

    def test_retiro_antes_edad_referencia_no_calcula_vejez_estandar(self):
        resultado = calcular_sucgs(
            DatosCalculoSUCGS(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 10, 16),
                cuotas_totales=300,
                saldo_capitalizacion_solidaria=100000,
            )
        )

        self.assertFalse(resultado.cumple_edad_referencia)
        self.assertFalse(resultado.calculo_contributivo_disponible)
        self.assertIsNone(resultado.pension_contributiva_mensual)


if __name__ == "__main__":
    unittest.main()
