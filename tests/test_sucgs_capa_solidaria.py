"""Pruebas de los artículos 194 y 195 del SUCGS."""

import unittest
from datetime import date

from app.models.pension import DatosCalculoSUCGS
from app.engines.sucgs import calcular_sucgs


class TestSUCGSCapaSolidaria(unittest.TestCase):
    """Valida las reglas solidarias sin aplicar aún el artículo 197."""

    def _calcular(
        self,
        *,
        nacimiento: date,
        retiro: date,
        cuotas: int,
        saldo: float,
        sexo: str = "FEMENINO",
    ):
        return calcular_sucgs(
            DatosCalculoSUCGS(
                fecha_nacimiento=nacimiento,
                sexo=sexo,
                fecha_retiro=retiro,
                cuotas_totales=cuotas,
                saldo_capitalizacion_solidaria=saldo,
                saldo_confirmado_oficialmente=True,
                valor_minimo_universal_vigente=144,
                pension_garantizada_solidaria_vigente=265,
                valores_solidarios_confirmados_oficialmente=True,
            )
        )

    def test_art195_300_cuotas_completa_hasta_265(self):
        resultado = self._calcular(
            nacimiento=date(1969, 11, 16),
            retiro=date(2026, 11, 16),
            cuotas=300,
            saldo=40000,
        )

        self.assertEqual(resultado.pension_contributiva_mensual, 190.80)
        self.assertEqual(
            resultado.tipo_prestacion_solidaria,
            "PENSION_BENEFICIO_SOLIDARIO",
        )
        self.assertEqual(resultado.complemento_solidario_mensual, 74.20)
        self.assertEqual(
            resultado.pension_despues_componente_solidario,
            265.00,
        )
        self.assertFalse(resultado.garantia_reemplazo_evaluada)
        self.assertIsNone(resultado.pension_mensual_total_estimada)

    def test_art194_120_a_239_y_pension_menor_144_da_beneficio_minimo(self):
        resultado = self._calcular(
            nacimiento=date(1961, 1, 1),
            retiro=date(2026, 1, 1),
            cuotas=180,
            saldo=20000,
        )

        self.assertEqual(resultado.edad_retiro_anios, 65)
        self.assertEqual(resultado.pension_contributiva_mensual, 108.80)
        self.assertEqual(
            resultado.tipo_prestacion_solidaria,
            "PENSION_BENEFICIO_MINIMO",
        )
        self.assertEqual(resultado.complemento_solidario_mensual, 35.20)
        self.assertEqual(
            resultado.pension_despues_componente_solidario,
            144.00,
        )

    def test_art194_menos_120_no_completa_hasta_144(self):
        resultado = self._calcular(
            nacimiento=date(1961, 1, 1),
            retiro=date(2026, 1, 1),
            cuotas=100,
            saldo=20000,
        )

        self.assertEqual(resultado.pension_contributiva_mensual, 108.80)
        self.assertEqual(
            resultado.tipo_prestacion_solidaria,
            "PENSION_CONTRIBUTIVA_BAJO_MINIMO_UNIVERSAL",
        )
        self.assertEqual(resultado.complemento_solidario_mensual, 0.00)
        self.assertEqual(
            resultado.pension_despues_componente_solidario,
            108.80,
        )

    def test_art194_180_cuotas_entre_144_y_265_conserva_resultado(self):
        resultado = self._calcular(
            nacimiento=date(1961, 1, 1),
            retiro=date(2026, 1, 1),
            cuotas=180,
            saldo=30000,
        )

        self.assertEqual(resultado.pension_contributiva_mensual, 163.20)
        self.assertEqual(
            resultado.tipo_prestacion_solidaria,
            "PENSION_CONTRIBUTIVA_ART194_3",
        )
        self.assertEqual(resultado.complemento_solidario_mensual, 0.00)
        self.assertEqual(
            resultado.pension_despues_componente_solidario,
            163.20,
        )

    def test_240_cuotas_prioriza_pgs_art195_en_superposicion(self):
        resultado = self._calcular(
            nacimiento=date(1961, 1, 1),
            retiro=date(2026, 1, 1),
            cuotas=240,
            saldo=20000,
        )

        self.assertEqual(resultado.pension_contributiva_mensual, 108.80)
        self.assertEqual(
            resultado.tipo_prestacion_solidaria,
            "PENSION_GARANTIZADA_SOLIDARIA_ART195",
        )
        self.assertEqual(resultado.complemento_solidario_mensual, 156.20)
        self.assertEqual(
            resultado.pension_despues_componente_solidario,
            265.00,
        )


if __name__ == "__main__":
    unittest.main()
