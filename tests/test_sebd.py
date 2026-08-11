"""Pruebas del motor normal del Subsistema Exclusivamente de Beneficio Definido."""

import unittest
from datetime import date

from app.modelos.pension import DatosCalculoSEBDNormal
from app.modelos.simulacion import RegistroHistorialSalarial
from app.motores.sebd import calcular_sebd_normal


class TestSEBDNormal(unittest.TestCase):
    """Valida fórmula, selección salarial y cuotas adicionales."""

    def _registros_anonimizados(self):
        """Crea una serie sintética cuyo top 10 suma B/.139,593.71."""

        salarios_top = [
            13959.37,
            13959.37,
            13959.37,
            13959.37,
            13959.37,
            13959.37,
            13959.37,
            13959.37,
            13959.37,
            13959.38,
        ]

        registros = [
            RegistroHistorialSalarial(
                anio=2010 + indice,
                cuotas=12,
                salario_cotizado=salario,
            )
            for indice, salario in enumerate(salarios_top)
        ]

        # Dos años inferiores verifican que el motor seleccione
        # realmente los diez salarios anuales más altos.
        registros.extend(
            [
                RegistroHistorialSalarial(
                    anio=2008,
                    cuotas=12,
                    salario_cotizado=6000.00,
                ),
                RegistroHistorialSalarial(
                    anio=2009,
                    cuotas=12,
                    salario_cotizado=8000.00,
                ),
            ]
        )

        return registros

    def test_caso_regresion_femenino_741_59(self):
        datos = DatosCalculoSEBDNormal(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            fecha_retiro=date(2026, 11, 16),
            cuotas_totales=281,
            registros=self._registros_anonimizados(),
        )

        resultado = calcular_sebd_normal(datos)

        self.assertTrue(resultado.elegible)
        self.assertEqual(resultado.cuotas_exceso_total, 41)
        self.assertEqual(resultado.bloques_12_antes_referencia, 3)
        self.assertEqual(resultado.bloques_12_despues_referencia, 0)
        self.assertEqual(resultado.tasa_reemplazo_total_pct, 63.75)
        self.assertEqual(resultado.total_salarios_seleccionados, 139593.71)
        self.assertEqual(resultado.salario_base_mensual, 1163.28)
        self.assertEqual(resultado.pension_mensual_estimada, 741.59)

    def test_incremento_despues_referencia_usa_dos_por_ciento(self):
        datos = DatosCalculoSEBDNormal(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            fecha_retiro=date(2027, 11, 16),
            cuotas_totales=264,
            cuotas_exceso_antes_referencia=12,
            cuotas_exceso_despues_referencia=12,
            registros=self._registros_anonimizados(),
        )

        resultado = calcular_sebd_normal(datos)

        self.assertEqual(resultado.bloques_12_antes_referencia, 1)
        self.assertEqual(resultado.incremento_antes_referencia_pct, 1.25)
        self.assertEqual(resultado.bloques_12_despues_referencia, 1)
        self.assertEqual(resultado.incremento_despues_referencia_pct, 2.0)
        self.assertEqual(resultado.tasa_reemplazo_total_pct, 63.25)

    def test_no_elegible_normal_con_menos_de_240_cuotas(self):
        datos = DatosCalculoSEBDNormal(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            fecha_retiro=date(2026, 11, 16),
            cuotas_totales=239,
            registros=self._registros_anonimizados(),
        )

        resultado = calcular_sebd_normal(datos)

        self.assertFalse(resultado.elegible)
        self.assertTrue(resultado.motivos_no_elegible)

    def test_tope_ordinario_sebd_1500(self):
        registros = [
            RegistroHistorialSalarial(
                anio=2000 + indice,
                cuotas=12,
                salario_cotizado=36000.00,
            )
            for indice in range(10)
        ]

        datos = DatosCalculoSEBDNormal(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            fecha_retiro=date(2026, 11, 16),
            cuotas_totales=240,
            registros=registros,
        )

        resultado = calcular_sebd_normal(datos)

        self.assertEqual(resultado.monto_antes_limite_maximo, 1800.00)
        self.assertEqual(resultado.monto_maximo_aplicable, 1500.00)
        self.assertEqual(resultado.pension_mensual_estimada, 1500.00)

    def test_monto_bajo_advierte_minimo_indexado_pendiente(self):
        registros = [
            RegistroHistorialSalarial(
                anio=2000 + indice,
                cuotas=12,
                salario_cotizado=3600.00,
            )
            for indice in range(10)
        ]

        datos = DatosCalculoSEBDNormal(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            fecha_retiro=date(2026, 11, 16),
            cuotas_totales=240,
            registros=registros,
        )

        resultado = calcular_sebd_normal(datos)

        self.assertEqual(resultado.pension_mensual_estimada, 180.00)
        self.assertFalse(resultado.minimo_indexado_aplicado)
        self.assertTrue(resultado.advertencias)


if __name__ == "__main__":
    unittest.main()
