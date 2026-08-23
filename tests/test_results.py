"""Pruebas de integración entre Pasos 1–5 y el motor SEBD normal."""

import unittest
from datetime import date

from app.models.pension import DatosResultadoSEBDNormal
from app.models.simulation import (
    DatosHistorialSalarial,
    EscenarioLineaTiempo,
    EscenarioRetiro,
    RegistroHistorialSalarial,
    RegistroLineaTiempo,
    ResumenLineaTiempo,
    ResumenRetiro,
)
from app.services.results import calcular_resultado_sebd_normal


class TestResultadosSEBDNormal(unittest.TestCase):
    """Valida la consolidación del asistente antes del motor jurídico."""

    def _historial_base(self) -> DatosHistorialSalarial:
        salarios = [
            8920.45,
            10013.23,
            10431.36,
            10910.82,
            11064.62,
            17474.59,
            17538.10,
            17719.86,
            17760.01,
            17760.67,
        ]

        registros = [
            RegistroHistorialSalarial(
                anio=2016 + indice,
                cuotas=12,
                salario_cotizado=salario,
            )
            for indice, salario in enumerate(salarios)
        ]

        registros.append(
            RegistroHistorialSalarial(
                anio=2026,
                cuotas=5,
                salario_cotizado=6659.50,
            )
        )

        return DatosHistorialSalarial(
            anio_inicio=2016,
            anio_fin=2026,
            cuotas_totales_referencia=281,
            registros=registros,
        )

    def _linea_tiempo(self) -> ResumenLineaTiempo:
        registros = [
            RegistroLineaTiempo(
                anio=2026,
                cuotas_historicas=5,
                salario_historico=6659.50,
                cuotas_proyectadas=0,
                salario_proyectado=0.0,
                cuotas_cierre=5,
                salario_cierre=6659.50,
                estado="HISTORICO_PARCIAL",
            ),
            RegistroLineaTiempo(
                anio=2027,
                cuotas_historicas=0,
                salario_historico=0.0,
                cuotas_proyectadas=12,
                salario_proyectado=16142.63,
                cuotas_cierre=12,
                salario_cierre=16142.63,
                estado="PROYECTADO",
            ),
        ]

        return ResumenLineaTiempo(
            anio_inicio_historico=2016,
            anio_actual=2026,
            anio_fin_proyeccion=2027,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Crecimiento anual de 1 %",
                    tasa_anual_pct=1.0,
                    registros=registros,
                )
            ],
        )

    def _resumen_retiro(self) -> ResumenRetiro:
        referencia = EscenarioRetiro(
            tipo="REFERENCIA",
            nombre="Edad de referencia",
            fecha_retiro=date(2026, 11, 16),
            edad_retiro_anios=57,
            meses_desde_corte_cuotas=3,
            cuotas_estimadas_adicionales=0,
            cuotas_estimadas_totales=281,
            fecha_ya_transcurrida=False,
        )

        adicional = EscenarioRetiro(
            tipo="ADICIONAL",
            nombre="Edad de referencia + 1 año",
            fecha_retiro=date(2027, 11, 16),
            edad_retiro_anios=58,
            meses_desde_corte_cuotas=15,
            cuotas_estimadas_adicionales=10,
            cuotas_estimadas_totales=291,
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
            escenarios=[referencia, adicional],
            anio_fin_proyeccion_salarial=2027,
            proyeccion_salarial_cubre_escenarios=True,
            advertencias=[],
            metodo_estimacion_cuotas="Prueba.",
        )

    def test_referencia_reproduce_741_59(self):
        datos = DatosResultadoSEBDNormal(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            historial=self._historial_base(),
            linea_tiempo=self._linea_tiempo(),
            resumen_retiro=self._resumen_retiro(),
            fecha_retiro_seleccionada=date(2026, 11, 16),
            escenario_salarial_nombre="Crecimiento anual de 1 %",
        )

        resultado = calcular_resultado_sebd_normal(datos)

        self.assertTrue(resultado.calculo.elegible)
        self.assertEqual(resultado.calculo.pension_mensual_estimada, 741.59)
        self.assertEqual(resultado.anios_proyectados_incluidos, [])

    def test_mas_un_anio_separa_exceso_y_prorratea_2027(self):
        datos = DatosResultadoSEBDNormal(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            historial=self._historial_base(),
            linea_tiempo=self._linea_tiempo(),
            resumen_retiro=self._resumen_retiro(),
            fecha_retiro_seleccionada=date(2027, 11, 16),
            escenario_salarial_nombre="Crecimiento anual de 1 %",
        )

        resultado = calcular_resultado_sebd_normal(datos)

        self.assertEqual(
            resultado.calculo.cuotas_exceso_antes_referencia,
            41,
        )
        self.assertEqual(
            resultado.calculo.cuotas_exceso_despues_referencia,
            10,
        )
        self.assertEqual(resultado.anios_proyectados_incluidos, [2027])
        self.assertEqual(resultado.calculo.salario_base_mensual, 1201.05)
        self.assertEqual(resultado.calculo.pension_mensual_estimada, 765.67)
        self.assertTrue(resultado.advertencias_integracion)


if __name__ == "__main__":
    unittest.main()
