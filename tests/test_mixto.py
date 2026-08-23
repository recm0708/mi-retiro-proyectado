"""Pruebas del motor preliminar del Subsistema Mixto."""

import unittest
from datetime import date

from app.models.pension import DatosCalculoMixto
from app.models.simulacion import RegistroHistorialSalarial
from app.engines.mixto import calcular_mixto


def _historial_alto() -> list[RegistroHistorialSalarial]:
    """Construye diez años completos con salarios por encima del tope Mixto."""

    return [
        RegistroHistorialSalarial(
            anio=anio,
            cuotas=12,
            salario_cotizado=12000,
        )
        for anio in range(2017, 2027)
    ]


class TestMixto(unittest.TestCase):
    """Valida transición, componente definido y ahorro personal."""

    def test_normal_mixto_suma_ambos_componentes(self):
        resultado = calcular_mixto(
            DatosCalculoMixto(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=300,
                registros=_historial_alto(),
                saldo_ahorro_personal=100000,
                bono_reconocimiento=5000,
                bono_reconocimiento_confirmado_oficialmente=True,
                valor_actuarial_expectativa_vida=200,
            )
        )

        self.assertTrue(resultado.calculo_mixto_aplicable)
        self.assertTrue(resultado.calculo_completo)
        self.assertEqual(resultado.modalidad, "NORMAL")
        self.assertEqual(
            resultado.componente_beneficio_definido.salario_base_mensual,
            500.0,
        )
        self.assertEqual(
            resultado.componente_beneficio_definido.pension_mensual_estimada,
            331.25,
        )
        self.assertEqual(
            resultado.componente_ahorro_personal.pension_programada_mensual,
            525.0,
        )
        self.assertEqual(
            resultado.pension_mensual_total_estimada,
            856.25,
        )

    def test_cap_no_se_inventa_sin_valor_actuarial(self):
        resultado = calcular_mixto(
            DatosCalculoMixto(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=300,
                registros=_historial_alto(),
                saldo_ahorro_personal=100000,
            )
        )

        self.assertFalse(resultado.calculo_completo)
        self.assertIsNone(
            resultado.componente_ahorro_personal.pension_programada_mensual
        )
        self.assertIsNone(resultado.pension_mensual_total_estimada)

    def test_proporcional_mixto_respeta_tope_500(self):
        resultado = calcular_mixto(
            DatosCalculoMixto(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=200,
                registros=_historial_alto(),
                saldo_ahorro_personal=0,
                valor_actuarial_expectativa_vida=200,
            )
        )

        self.assertEqual(resultado.modalidad, "PROPORCIONAL")
        self.assertEqual(
            resultado.componente_beneficio_definido.pension_mensual_estimada,
            250.0,
        )

    def test_desde_marzo_2032_transiciona_a_sucgs(self):
        resultado = calcular_mixto(
            DatosCalculoMixto(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2032, 3, 1),
                cuotas_totales=360,
                registros=_historial_alto(),
                saldo_ahorro_personal=100000,
                valor_actuarial_expectativa_vida=200,
            )
        )

        self.assertFalse(resultado.calculo_mixto_aplicable)
        self.assertEqual(resultado.estado_sistema, "TRANSICION_SUCGS")
        self.assertIsNone(resultado.pension_mensual_total_estimada)

    def test_opcion_sucgs_no_calcula_bajo_mixto(self):
        resultado = calcular_mixto(
            DatosCalculoMixto(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2028, 11, 16),
                cuotas_totales=324,
                registros=_historial_alto(),
                sistema_seleccionado="SUCGS",
            )
        )

        self.assertEqual(resultado.estado_sistema, "OPTO_SUCGS")
        self.assertFalse(resultado.calculo_mixto_aplicable)


if __name__ == "__main__":
    unittest.main()
