"""Pruebas de integración del asistente con el clasificador SEBD general."""

import unittest
from datetime import date

from app.modelos.pension import DatosResultadoSEBD
from app.modelos.simulacion import (
    DatosHistorialSalarial,
    EscenarioLineaTiempo,
    EscenarioRetiro,
    RegistroHistorialSalarial,
    RegistroLineaTiempo,
    ResumenLineaTiempo,
    ResumenRetiro,
)
from app.servicios.resultados_sebd import calcular_resultado_sebd


class TestResultadosModalidadesSEBD(unittest.TestCase):
    """Valida que la modalidad detectada llegue correctamente al Paso 6."""

    def test_fecha_personalizada_anticipada_femenina(self):
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

        historial = DatosHistorialSalarial(
            anio_inicio=2016,
            anio_fin=2026,
            cuotas_totales_referencia=281,
            registros=registros,
        )

        linea = ResumenLineaTiempo(
            anio_inicio_historico=2016,
            anio_actual=2026,
            anio_fin_proyeccion=2026,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Crecimiento anual de 1 %",
                    tasa_anual_pct=1.0,
                    registros=[
                        RegistroLineaTiempo(
                            anio=2026,
                            cuotas_historicas=5,
                            salario_historico=6659.50,
                            cuotas_proyectadas=0,
                            salario_proyectado=0.0,
                            cuotas_cierre=5,
                            salario_cierre=6659.50,
                            estado="HISTORICO_PARCIAL",
                        )
                    ],
                )
            ],
        )

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
        personalizada = EscenarioRetiro(
            tipo="PERSONALIZADO",
            nombre="Fecha personalizada",
            fecha_retiro=date(2026, 10, 16),
            edad_retiro_anios=56,
            meses_desde_corte_cuotas=2,
            cuotas_estimadas_adicionales=0,
            cuotas_estimadas_totales=281,
            fecha_ya_transcurrida=False,
        )

        retiro = ResumenRetiro(
            fecha_corte=date(2026, 8, 10),
            fecha_corte_cuotas=date(2026, 8, 10),
            edad_actual_anios=56,
            edad_referencia=57,
            fecha_referencia=date(2026, 11, 16),
            alcanzo_edad_referencia=False,
            dias_hasta_referencia=98,
            escenarios=[referencia, personalizada],
            anio_fin_proyeccion_salarial=2026,
            proyeccion_salarial_cubre_escenarios=True,
            advertencias=[],
            metodo_estimacion_cuotas="Prueba.",
        )

        resultado = calcular_resultado_sebd(
            DatosResultadoSEBD(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                historial=historial,
                linea_tiempo=linea,
                resumen_retiro=retiro,
                fecha_retiro_seleccionada=date(2026, 10, 16),
                escenario_salarial_nombre="Crecimiento anual de 1 %",
            )
        )

        self.assertEqual(resultado.calculo.modalidad, "ANTICIPADA")
        self.assertEqual(resultado.calculo.factor_reduccion_edad, 0.9927)
        self.assertEqual(resultado.calculo.pension_mensual_estimada, 736.18)


if __name__ == "__main__":
    unittest.main()
