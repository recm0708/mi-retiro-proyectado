"""Pruebas de la garantía de reemplazo mínimo del artículo 197."""

import unittest
from datetime import date

from app.models.pension import DatosCalculoSUCGS
from app.models.simulacion import RegistroHistorialSalarial
from app.engines.sucgs import calcular_sucgs


def _registro(anio: int, cuotas: int, salario_mensual: float = 1000.0):
    return RegistroHistorialSalarial(
        anio=anio,
        cuotas=cuotas,
        salario_cotizado=cuotas * salario_mensual,
    )


def _historial_240_equilibrado():
    registros = []
    for anio in range(1997, 2017):
        registros.append(_registro(anio, 6))
    for anio in range(2017, 2027):
        registros.append(_registro(anio, 12))
    return registros


def _historial_240_desbalanceado():
    registros = []
    for anio in range(1997, 2017):
        registros.append(_registro(anio, 9))
    for anio in range(2017, 2027):
        registros.append(_registro(anio, 6))
    return registros


def _historial_180_equilibrado():
    registros = []
    ceros = {2005, 2010}
    for anio in range(1997, 2017):
        cuotas = 0 if anio in ceros else 5
        registros.append(_registro(anio, cuotas))
    for anio in range(2017, 2027):
        registros.append(_registro(anio, 9))
    return registros


class TestSUCGSReemplazoMinimo(unittest.TestCase):
    """Valida la preevaluación auditable del artículo 197."""

    def test_240_cuotas_equilibradas_elevan_a_60_por_ciento(self):
        resultado = calcular_sucgs(
            DatosCalculoSUCGS(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=240,
                saldo_capitalizacion_solidaria=100000,
                saldo_confirmado_oficialmente=True,
                valor_minimo_universal_vigente=144,
                pension_garantizada_solidaria_vigente=265,
                valores_solidarios_confirmados_oficialmente=True,
                anio_inicio_vida_laboral=1997,
                registros_historial_laboral=_historial_240_equilibrado(),
                historial_laboral_completo=True,
                estabilidad_salarial_art197_confirmada=True,
            )
        )

        self.assertTrue(resultado.garantia_reemplazo_evaluada)
        self.assertTrue(resultado.garantia_reemplazo_aplica)
        self.assertTrue(resultado.condicion_minimo_cuotas_anuales_cumple)
        self.assertTrue(resultado.condicion_distribucion_cuotas_cumple)
        self.assertTrue(resultado.condicion_estabilidad_salarial_cumple)
        self.assertEqual(resultado.cuotas_primeros_20_anios, 120)
        self.assertEqual(resultado.cuotas_anios_restantes, 120)
        self.assertEqual(resultado.salario_promedio_base_mensual, 1000.00)
        self.assertEqual(resultado.tasa_reemplazo_minima_pct_aplicable, 60.0)
        self.assertEqual(resultado.garantia_reemplazo_monto_objetivo, 600.00)
        self.assertEqual(resultado.garantia_reemplazo_complemento_mensual, 123.00)
        self.assertEqual(resultado.pension_mensual_total_estimada, 600.00)

    def test_180_cuotas_aplican_garantia_proporcional_45_por_ciento(self):
        resultado = calcular_sucgs(
            DatosCalculoSUCGS(
                fecha_nacimiento=date(1961, 1, 1),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 1, 1),
                cuotas_totales=180,
                saldo_capitalizacion_solidaria=20000,
                saldo_confirmado_oficialmente=True,
                valor_minimo_universal_vigente=144,
                pension_garantizada_solidaria_vigente=265,
                valores_solidarios_confirmados_oficialmente=True,
                anio_inicio_vida_laboral=1997,
                registros_historial_laboral=_historial_180_equilibrado(),
                historial_laboral_completo=True,
                estabilidad_salarial_art197_confirmada=True,
            )
        )

        self.assertEqual(resultado.pension_despues_componente_solidario, 144.00)
        self.assertTrue(resultado.garantia_reemplazo_aplica)
        self.assertEqual(resultado.cuotas_minimas_por_tramo, 90)
        self.assertEqual(resultado.cuotas_primeros_20_anios, 90)
        self.assertEqual(resultado.cuotas_anios_restantes, 90)
        self.assertEqual(resultado.tasa_reemplazo_minima_pct_aplicable, 45.0)
        self.assertEqual(resultado.garantia_reemplazo_monto_objetivo, 450.00)
        self.assertEqual(resultado.garantia_reemplazo_complemento_mensual, 306.00)
        self.assertEqual(resultado.pension_mensual_total_estimada, 450.00)

    def test_distribucion_incorrecta_impide_garantia(self):
        resultado = calcular_sucgs(
            DatosCalculoSUCGS(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=240,
                saldo_capitalizacion_solidaria=100000,
                saldo_confirmado_oficialmente=True,
                anio_inicio_vida_laboral=1997,
                registros_historial_laboral=_historial_240_desbalanceado(),
                historial_laboral_completo=True,
                estabilidad_salarial_art197_confirmada=True,
            )
        )

        self.assertTrue(resultado.condicion_minimo_cuotas_anuales_cumple)
        self.assertFalse(resultado.condicion_distribucion_cuotas_cumple)
        self.assertEqual(resultado.cuotas_primeros_20_anios, 180)
        self.assertEqual(resultado.cuotas_anios_restantes, 60)
        self.assertTrue(resultado.garantia_reemplazo_evaluada)
        self.assertFalse(resultado.garantia_reemplazo_aplica)
        self.assertTrue(resultado.calculo_total_disponible)
        self.assertEqual(resultado.pension_mensual_total_estimada, 477.00)

    def test_estabilidad_no_confirmada_deja_total_pendiente(self):
        resultado = calcular_sucgs(
            DatosCalculoSUCGS(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=240,
                saldo_capitalizacion_solidaria=100000,
                saldo_confirmado_oficialmente=True,
                anio_inicio_vida_laboral=1997,
                registros_historial_laboral=_historial_240_equilibrado(),
                historial_laboral_completo=True,
                estabilidad_salarial_art197_confirmada=None,
            )
        )

        self.assertTrue(resultado.condicion_minimo_cuotas_anuales_cumple)
        self.assertTrue(resultado.condicion_distribucion_cuotas_cumple)
        self.assertFalse(resultado.condicion_estabilidad_salarial_evaluada)
        self.assertFalse(resultado.garantia_reemplazo_evaluada)
        self.assertFalse(resultado.calculo_total_disponible)
        self.assertIsNone(resultado.pension_mensual_total_estimada)

    def test_historial_con_1_a_4_cuotas_falla_condicion_anual(self):
        historial = _historial_240_equilibrado()
        # Mantener 240 cuotas trasladando dos cuotas a otro año sin superar 12.
        historial[0] = _registro(1997, 4)
        historial[20] = _registro(2017, 12)
        historial[21] = _registro(2018, 12)
        # El total ahora es 238; se usa ese total para aislar la condición anual.
        resultado = calcular_sucgs(
            DatosCalculoSUCGS(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=238,
                saldo_capitalizacion_solidaria=100000,
                saldo_confirmado_oficialmente=True,
                anio_inicio_vida_laboral=1997,
                registros_historial_laboral=historial,
                historial_laboral_completo=True,
                estabilidad_salarial_art197_confirmada=True,
            )
        )

        self.assertFalse(resultado.condicion_minimo_cuotas_anuales_cumple)
        self.assertIn(1997, resultado.anios_con_1_a_4_cuotas)
        self.assertTrue(resultado.garantia_reemplazo_evaluada)
        self.assertFalse(resultado.garantia_reemplazo_aplica)
        self.assertEqual(resultado.pension_mensual_total_estimada, 477.00)


if __name__ == "__main__":
    unittest.main()
