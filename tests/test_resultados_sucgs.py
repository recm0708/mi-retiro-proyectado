"""Pruebas de integración visual de los Pasos 1–5 con SUCGS."""

import unittest
from datetime import date

from app.models.pension import DatosResultadoSUCGS
from app.models.simulacion import (
    DatosHistorialSalarial,
    EscenarioLineaTiempo,
    EscenarioRetiro,
    RegistroHistorialSalarial,
    RegistroLineaTiempo,
    ResumenLineaTiempo,
    ResumenRetiro,
)
from app.services.resultados_sucgs import calcular_resultado_sucgs


class TestResultadosSUCGS(unittest.TestCase):
    """Valida que el asistente alimente SUCGS sin duplicar proyecciones."""

    def _resumen_retiro(
        self,
        *,
        cuotas_reales: int,
        cuotas_adicionales: int,
        cuotas_totales: int,
    ) -> ResumenRetiro:
        escenario = EscenarioRetiro(
            tipo="REFERENCIA",
            nombre="Edad de referencia",
            fecha_retiro=date(2026, 11, 16),
            edad_retiro_anios=57,
            meses_desde_corte_cuotas=3,
            cuotas_estimadas_adicionales=cuotas_adicionales,
            cuotas_estimadas_totales=cuotas_totales,
            fecha_ya_transcurrida=False,
        )

        return ResumenRetiro(
            fecha_corte=date(2026, 8, 11),
            fecha_corte_cuotas=date(2026, 8, 11),
            edad_actual_anios=56,
            edad_referencia=57,
            fecha_referencia=date(2026, 11, 16),
            alcanzo_edad_referencia=False,
            dias_hasta_referencia=97,
            escenarios=[escenario],
            anio_fin_proyeccion_salarial=2031,
            proyeccion_salarial_cubre_escenarios=True,
            advertencias=[],
            metodo_estimacion_cuotas=(
                f"Prueba controlada desde {cuotas_reales} cuotas reales."
            ),
        )

    def test_caso_maestro_297_mas_3_cuotas_llega_a_477(self):
        registros = [
            RegistroHistorialSalarial(
                anio=2001,
                cuotas=2,
                salario_cotizado=2000,
            )
        ]
        registros.extend(
            RegistroHistorialSalarial(
                anio=anio,
                cuotas=12,
                salario_cotizado=12000,
            )
            for anio in range(2002, 2026)
        )
        registros.append(
            RegistroHistorialSalarial(
                anio=2026,
                cuotas=7,
                salario_cotizado=7000,
            )
        )

        historial = DatosHistorialSalarial(
            anio_inicio=2001,
            anio_fin=2026,
            cuotas_totales_referencia=297,
            registros=registros,
        )

        linea = ResumenLineaTiempo(
            anio_inicio_historico=2001,
            anio_actual=2026,
            anio_fin_proyeccion=2031,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Salario constante",
                    tasa_anual_pct=0,
                    registros=[
                        RegistroLineaTiempo(
                            anio=2026,
                            cuotas_historicas=7,
                            salario_historico=7000,
                            cuotas_proyectadas=5,
                            salario_proyectado=5000,
                            cuotas_cierre=12,
                            salario_cierre=12000,
                            estado="MIXTO",
                        )
                    ],
                )
            ],
        )

        resultado = calcular_resultado_sucgs(
            DatosResultadoSUCGS(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                historial=historial,
                linea_tiempo=linea,
                resumen_retiro=self._resumen_retiro(
                    cuotas_reales=297,
                    cuotas_adicionales=3,
                    cuotas_totales=300,
                ),
                fecha_retiro_seleccionada=date(2026, 11, 16),
                escenario_salarial_nombre="Salario constante",
                saldo_capitalizacion_solidaria=100000,
                saldo_confirmado_oficialmente=True,
                valor_minimo_universal_vigente=144,
                pension_garantizada_solidaria_vigente=265,
                valores_solidarios_confirmados_oficialmente=True,
                historial_laboral_completo_confirmado=True,
                estabilidad_salarial_art197_confirmada=True,
            )
        )

        self.assertEqual(resultado.anios_proyectados_incluidos, [2026])
        self.assertEqual(resultado.calculo.historial_cuotas_sumadas, 300)
        self.assertEqual(resultado.calculo.pension_contributiva_mensual, 477.00)
        self.assertTrue(resultado.calculo.calculo_total_disponible)
        self.assertEqual(resultado.calculo.pension_mensual_total_estimada, 477.00)
        self.assertFalse(resultado.calculo.garantia_reemplazo_aplica)
        self.assertIn(2001, resultado.calculo.anios_con_1_a_4_cuotas)
        self.assertIsNotNone(resultado.resumen_unificado)
        self.assertEqual(
            resultado.resumen_unificado.pension_mensual_estimada,
            477.00,
        )

    def test_integrado_240_equilibrado_aplica_garantia_600(self):
        registros = []
        for anio in range(1997, 2017):
            registros.append(
                RegistroHistorialSalarial(
                    anio=anio,
                    cuotas=6,
                    salario_cotizado=6000,
                )
            )
        for anio in range(2017, 2027):
            registros.append(
                RegistroHistorialSalarial(
                    anio=anio,
                    cuotas=12,
                    salario_cotizado=12000,
                )
            )

        historial = DatosHistorialSalarial(
            anio_inicio=1997,
            anio_fin=2026,
            cuotas_totales_referencia=240,
            registros=registros,
        )
        linea = ResumenLineaTiempo(
            anio_inicio_historico=1997,
            anio_actual=2026,
            anio_fin_proyeccion=2026,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Escenario base",
                    tasa_anual_pct=0,
                    registros=[],
                )
            ],
        )

        resultado = calcular_resultado_sucgs(
            DatosResultadoSUCGS(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                historial=historial,
                linea_tiempo=linea,
                resumen_retiro=self._resumen_retiro(
                    cuotas_reales=240,
                    cuotas_adicionales=0,
                    cuotas_totales=240,
                ),
                fecha_retiro_seleccionada=date(2026, 11, 16),
                escenario_salarial_nombre="Escenario base",
                saldo_capitalizacion_solidaria=100000,
                saldo_confirmado_oficialmente=True,
                valor_minimo_universal_vigente=144,
                pension_garantizada_solidaria_vigente=265,
                valores_solidarios_confirmados_oficialmente=True,
                historial_laboral_completo_confirmado=True,
                estabilidad_salarial_art197_confirmada=True,
            )
        )

        self.assertEqual(resultado.anios_proyectados_incluidos, [])
        self.assertTrue(resultado.calculo.garantia_reemplazo_aplica)
        self.assertEqual(resultado.calculo.pension_mensual_total_estimada, 600.00)


if __name__ == "__main__":
    unittest.main()
