"""Pruebas de integración de los Pasos 1–5 con el motor Mixto."""

import unittest
from datetime import date

from app.models.pension import DatosResultadoMixto
from app.models.simulation import (
    DatosHistorialSalarial,
    EscenarioLineaTiempo,
    EscenarioRetiro,
    RegistroHistorialSalarial,
    ResumenLineaTiempo,
    ResumenRetiro,
)
from app.services.mixto_results import calcular_resultado_mixto


class TestResultadosMixto(unittest.TestCase):
    """Valida que el asistente alimente el motor Mixto sin duplicar lógica."""

    def _linea_tiempo(self, anio_inicio: int) -> ResumenLineaTiempo:
        return ResumenLineaTiempo(
            anio_inicio_historico=anio_inicio,
            anio_actual=2026,
            anio_fin_proyeccion=2026,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Escenario base",
                    tasa_anual_pct=0.0,
                    registros=[],
                )
            ],
        )

    def _resumen_retiro(self, cuotas: int) -> ResumenRetiro:
        referencia = EscenarioRetiro(
            tipo="REFERENCIA",
            nombre="Edad de referencia",
            fecha_retiro=date(2026, 11, 16),
            edad_retiro_anios=57,
            meses_desde_corte_cuotas=3,
            cuotas_estimadas_adicionales=0,
            cuotas_estimadas_totales=cuotas,
            fecha_ya_transcurrida=False,
        )

        return ResumenRetiro(
            fecha_corte=date(2026, 8, 10),
            fecha_corte_cuotas=date(2026, 8, 10),
            edad_actual_anios=56,
            edad_referencia=57,
            fecha_referencia=date(2026, 11, 16),
            alcanzo_edad_referencia=False,
            dias_hasta_referencia=98,
            escenarios=[referencia],
            anio_fin_proyeccion_salarial=2026,
            proyeccion_salarial_cubre_escenarios=True,
            advertencias=[],
            metodo_estimacion_cuotas="Prueba controlada.",
        )

    def _historial_300(self) -> DatosHistorialSalarial:
        registros = [
            RegistroHistorialSalarial(
                anio=anio,
                cuotas=12,
                salario_cotizado=12000,
            )
            for anio in range(2002, 2027)
        ]

        return DatosHistorialSalarial(
            anio_inicio=2002,
            anio_fin=2026,
            cuotas_totales_referencia=300,
            registros=registros,
        )

    def _historial_200(self) -> DatosHistorialSalarial:
        registros = [
            RegistroHistorialSalarial(
                anio=anio,
                cuotas=12,
                salario_cotizado=12000,
            )
            for anio in range(2010, 2026)
        ]
        registros.append(
            RegistroHistorialSalarial(
                anio=2026,
                cuotas=8,
                salario_cotizado=8000,
            )
        )

        return DatosHistorialSalarial(
            anio_inicio=2010,
            anio_fin=2026,
            cuotas_totales_referencia=200,
            registros=registros,
        )

    def test_normal_mixto_integrado_conserva_856_25(self):
        datos = DatosResultadoMixto(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            historial=self._historial_300(),
            linea_tiempo=self._linea_tiempo(2002),
            resumen_retiro=self._resumen_retiro(300),
            fecha_retiro_seleccionada=date(2026, 11, 16),
            escenario_salarial_nombre="Escenario base",
            saldo_ahorro_personal=100000,
            bono_reconocimiento=5000,
            bono_reconocimiento_confirmado_oficialmente=True,
            valor_actuarial_expectativa_vida=200,
            opcion_prestacion_cap="PENSION_PROGRAMADA",
        )

        resultado = calcular_resultado_mixto(datos)

        self.assertTrue(resultado.calculo.calculo_completo)
        self.assertEqual(resultado.calculo.modalidad, "NORMAL")
        self.assertEqual(
            resultado.calculo.pension_mensual_total_estimada,
            856.25,
        )
        self.assertEqual(resultado.anios_proyectados_incluidos, [])
        self.assertIsNotNone(resultado.resumen_unificado)
        self.assertEqual(
            resultado.resumen_unificado.pension_mensual_estimada,
            856.25,
        )

    def test_auto_integrado_con_200_cuotas_exige_decision(self):
        datos = DatosResultadoMixto(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            historial=self._historial_200(),
            linea_tiempo=self._linea_tiempo(2010),
            resumen_retiro=self._resumen_retiro(200),
            fecha_retiro_seleccionada=date(2026, 11, 16),
            escenario_salarial_nombre="Escenario base",
            saldo_ahorro_personal=20000,
            valor_actuarial_expectativa_vida=200,
            opcion_prestacion_cap="AUTO",
        )

        resultado = calcular_resultado_mixto(datos)

        self.assertEqual(resultado.calculo.modalidad, "PROPORCIONAL")
        self.assertEqual(
            resultado.calculo.tipo_prestacion,
            "DECISION_CAP_PENDIENTE",
        )
        self.assertTrue(
            resultado.calculo.componente_ahorro_personal.decision_requerida
        )
        self.assertIsNone(resultado.calculo.pension_mensual_total_estimada)


if __name__ == "__main__":
    unittest.main()
