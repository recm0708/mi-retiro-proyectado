"""Pruebas de cálculo e integración de la Indemnización por Vejez SEBD."""

import unittest
from datetime import date

from app.modelos.pension import (
    DatosCalculoSEBD,
    DatosResultadoSEBD,
)
from app.modelos.simulacion import (
    DatosHistorialSalarial,
    EscenarioLineaTiempo,
    EscenarioRetiro,
    RegistroHistorialSalarial,
    RegistroLineaTiempo,
    ResumenLineaTiempo,
    ResumenRetiro,
)
from app.motores.elegibilidad import clasificar_modalidad_sebd
from app.motores.sebd_modalidades import calcular_sebd
from app.servicios.resultados_sebd import calcular_resultado_sebd


class TestIndemnizacionVejezSEBD(unittest.TestCase):
    """Valida la prestación de pago único prevista para menos de 180 cuotas."""

    def _registros_base(self) -> list[RegistroHistorialSalarial]:
        """Genera diez años con salario anual uniforme para cálculos exactos."""

        return [
            RegistroHistorialSalarial(
                anio=2017 + indice,
                cuotas=12,
                salario_cotizado=12000.0,
            )
            for indice in range(10)
        ]

    def test_120_cuotas_generan_pago_unico_12000(self):
        resultado = calcular_sebd(
            DatosCalculoSEBD(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=120,
                registros=self._registros_base(),
            )
        )

        self.assertEqual(resultado.modalidad, "INDEMNIZACION")
        self.assertEqual(resultado.tipo_prestacion, "INDEMNIZACION")
        self.assertTrue(resultado.elegible)
        self.assertTrue(resultado.calculo_disponible)
        self.assertIsNone(resultado.pension_mensual_estimada)
        self.assertEqual(resultado.salario_base_mensual, 1000.0)
        self.assertIsNone(resultado.factor_proporcional_cuotas)
        self.assertIsNone(resultado.monto_despues_factor_proporcional)
        self.assertEqual(
            resultado.indemnizacion_mensualidad_hipotetica,
            600.0,
        )
        self.assertEqual(resultado.indemnizacion_factor_cuotas, 20.0)
        self.assertEqual(resultado.indemnizacion_divisor_cuotas, 6)
        self.assertEqual(
            resultado.indemnizacion_pago_unico_estimado,
            12000.0,
        )

    def test_179_cuotas_no_truncan_el_cociente_entre_seis(self):
        resultado = calcular_sebd(
            DatosCalculoSEBD(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_retiro=date(2026, 11, 16),
                cuotas_totales=179,
                registros=self._registros_base(),
            )
        )

        self.assertAlmostEqual(
            resultado.indemnizacion_factor_cuotas,
            179 / 6,
            places=10,
        )
        self.assertEqual(
            resultado.indemnizacion_pago_unico_estimado,
            17900.0,
        )

    def test_desde_2036_03_01_clasifica_transicion_sucgs(self):
        resultado = clasificar_modalidad_sebd(
            date(1979, 3, 1),
            "FEMENINO",
            date(2036, 3, 1),
            120,
        )

        self.assertEqual(resultado["modalidad"], "NO_ELEGIBLE")
        self.assertEqual(
            resultado["tipo_prestacion"],
            "TRANSICION_SUCGS",
        )
        self.assertFalse(resultado["elegible"])

    def test_integracion_del_paso_6_devuelve_indemnizacion(self):
        registros = self._registros_base()

        historial = DatosHistorialSalarial(
            anio_inicio=2017,
            anio_fin=2026,
            cuotas_totales_referencia=120,
            registros=registros,
        )

        registros_linea = [
            RegistroLineaTiempo(
                anio=registro.anio,
                cuotas_historicas=registro.cuotas,
                salario_historico=registro.salario_cotizado,
                cuotas_proyectadas=0,
                salario_proyectado=0.0,
                cuotas_cierre=registro.cuotas,
                salario_cierre=registro.salario_cotizado,
                estado="HISTORICO",
            )
            for registro in registros
        ]

        linea = ResumenLineaTiempo(
            anio_inicio_historico=2017,
            anio_actual=2026,
            anio_fin_proyeccion=2026,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Salario constante",
                    tasa_anual_pct=0.0,
                    registros=registros_linea,
                )
            ],
        )

        referencia = EscenarioRetiro(
            tipo="REFERENCIA",
            nombre="Edad de referencia",
            fecha_retiro=date(2026, 11, 16),
            edad_retiro_anios=57,
            meses_desde_corte_cuotas=0,
            cuotas_estimadas_adicionales=0,
            cuotas_estimadas_totales=120,
            fecha_ya_transcurrida=False,
        )

        retiro = ResumenRetiro(
            fecha_corte=date(2026, 11, 16),
            fecha_corte_cuotas=date(2026, 11, 16),
            edad_actual_anios=57,
            edad_referencia=57,
            fecha_referencia=date(2026, 11, 16),
            alcanzo_edad_referencia=True,
            dias_hasta_referencia=0,
            escenarios=[referencia],
            anio_fin_proyeccion_salarial=2026,
            proyeccion_salarial_cubre_escenarios=True,
            advertencias=[],
            metodo_estimacion_cuotas="Prueba sin cuotas futuras.",
        )

        resultado = calcular_resultado_sebd(
            DatosResultadoSEBD(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                historial=historial,
                linea_tiempo=linea,
                resumen_retiro=retiro,
                fecha_retiro_seleccionada=date(2026, 11, 16),
                escenario_salarial_nombre="Salario constante",
            )
        )

        self.assertEqual(resultado.calculo.modalidad, "INDEMNIZACION")
        self.assertIsNone(
            resultado.calculo.factor_proporcional_cuotas
        )
        self.assertIsNone(
            resultado.calculo.monto_despues_factor_proporcional
        )
        self.assertEqual(
            resultado.calculo.indemnizacion_pago_unico_estimado,
            12000.0,
        )
        self.assertEqual(resultado.anios_proyectados_incluidos, [])


if __name__ == "__main__":
    unittest.main()
