"""Pruebas del clasificador y las modalidades generales del SEBD."""

import unittest
from datetime import date

from app.models.pension import DatosCalculoSEBD
from app.models.simulacion import RegistroHistorialSalarial
from app.engines.elegibilidad import clasificar_modalidad_sebd
from app.engines.sebd_modalidades import calcular_sebd


class TestModalidadesSEBD(unittest.TestCase):
    """Valida clasificación y factores de las modalidades del artículo 181."""

    def _registros(self) -> list[RegistroHistorialSalarial]:
        return [
            RegistroHistorialSalarial(
                anio=2016 + indice,
                cuotas=12,
                salario_cotizado=12000.0,
            )
            for indice in range(10)
        ]

    def test_clasifica_las_cuatro_modalidades(self):
        nacimiento = date(1969, 11, 16)

        casos = [
            (date(2026, 11, 16), 240, "NORMAL"),
            (date(2025, 11, 16), 240, "ANTICIPADA"),
            (date(2026, 11, 16), 200, "PROPORCIONAL"),
            (
                date(2025, 11, 16),
                200,
                "PROPORCIONAL_ANTICIPADA",
            ),
        ]

        for fecha, cuotas, modalidad in casos:
            with self.subTest(modalidad=modalidad):
                resultado = clasificar_modalidad_sebd(
                    nacimiento,
                    "FEMENINO",
                    fecha,
                    cuotas,
                )
                self.assertEqual(resultado["modalidad"], modalidad)

    def test_motor_general_conserva_regresion_normal(self):
        salarios = [
            8920.45, 10013.23, 10431.36, 10910.82, 11064.62,
            17474.59, 17538.10, 17719.86, 17760.01, 17760.67,
        ]
        registros = [
            RegistroHistorialSalarial(
                anio=2016 + indice,
                cuotas=12,
                salario_cotizado=salario,
            )
            for indice, salario in enumerate(salarios)
        ]

        resultado = calcular_sebd(
            DatosCalculoSEBD(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=281,
                registros=registros,
            )
        )

        self.assertEqual(resultado.modalidad, "NORMAL")
        self.assertEqual(resultado.pension_mensual_estimada, 741.59)
        self.assertEqual(resultado.factor_proporcional_cuotas, 1.0)
        self.assertEqual(resultado.factor_reduccion_edad, 1.0)

    def test_anticipada_usa_factor_mensual_23(self):
        resultado = calcular_sebd(
            DatosCalculoSEBD(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 10, 16),
                cuotas_totales=281,
                registros=self._registros(),
            )
        )

        self.assertEqual(resultado.modalidad, "ANTICIPADA")
        self.assertEqual(resultado.meses_desde_limite_anticipado, 23)
        self.assertEqual(resultado.factor_reduccion_edad, 0.9927)
        self.assertEqual(resultado.tasa_reemplazo_total_pct, 63.75)
        self.assertEqual(resultado.pension_mensual_estimada, 632.85)

    def test_proporcional_200_cuotas(self):
        resultado = calcular_sebd(
            DatosCalculoSEBD(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=200,
                registros=self._registros(),
            )
        )

        self.assertEqual(resultado.modalidad, "PROPORCIONAL")
        self.assertAlmostEqual(
            resultado.factor_proporcional_cuotas,
            200 / 240,
        )
        self.assertEqual(resultado.pension_mensual_estimada, 500.0)

    def test_proporcional_anticipada_combina_factores(self):
        resultado = calcular_sebd(
            DatosCalculoSEBD(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2025, 11, 16),
                cuotas_totales=200,
                registros=self._registros(),
            )
        )

        self.assertEqual(
            resultado.modalidad,
            "PROPORCIONAL_ANTICIPADA",
        )
        self.assertEqual(resultado.factor_reduccion_edad, 0.9128)
        self.assertEqual(resultado.pension_mensual_estimada, 456.4)

    def test_menos_de_180_en_referencia_identifica_indemnizacion(self):
        resultado = clasificar_modalidad_sebd(
            date(1969, 11, 16),
            "FEMENINO",
            date(2026, 11, 16),
            150,
        )

        self.assertEqual(resultado["modalidad"], "INDEMNIZACION")
        self.assertEqual(resultado["tipo_prestacion"], "INDEMNIZACION")

    def test_antes_de_banda_no_elegible(self):
        resultado = clasificar_modalidad_sebd(
            date(1969, 11, 16),
            "FEMENINO",
            date(2024, 10, 16),
            281,
        )

        self.assertEqual(resultado["modalidad"], "NO_ELEGIBLE")
        self.assertFalse(resultado["elegible"])


if __name__ == "__main__":
    unittest.main()
