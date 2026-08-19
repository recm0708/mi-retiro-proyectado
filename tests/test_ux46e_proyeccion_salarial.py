"""Regresiones de UX.4.6e R2 para proyección salarial/laboral."""

import unittest

from app.modelos.simulacion import (
    DatosCuotas,
    DatosHistorialSalarial,
    DatosLineaTiempo,
    DatosProyeccionSalario,
    DatosSalario,
    RegistroHistorialSalarial,
)
from app.servicios.linea_tiempo import construir_linea_tiempo
from app.servicios.proyeccion_salarios import proyectar_salario


class TestUX46eProyeccionSalarial(unittest.TestCase):
    """Protege los contratos matemáticos previos al rediseño del Paso 4."""

    def test_constante_conserva_salario_y_anualiza_sin_deriva(self):
        resumen = proyectar_salario(
            DatosProyeccionSalario(
                salario_mensual_actual=1500,
                anio_inicio=2026,
                anio_fin=2028,
                modalidad="CONSTANTE",
            )
        )

        escenario = resumen.escenarios[0]
        self.assertEqual(0.0, escenario.tasa_anual_pct)
        self.assertEqual(
            [1500.0, 1500.0, 1500.0],
            [registro.salario_mensual for registro in escenario.registros],
        )
        self.assertEqual(
            [18000.0, 18000.0, 18000.0],
            [registro.salario_anual for registro in escenario.registros],
        )

    def test_porcentaje_compone_sobre_valor_preciso(self):
        resumen = proyectar_salario(
            DatosProyeccionSalario(
                salario_mensual_actual=1500,
                anio_inicio=2026,
                anio_fin=2028,
                modalidad="PORCENTAJE",
                porcentaje_anual=2.5,
            )
        )

        registros = resumen.escenarios[0].registros
        self.assertEqual(1537.50, registros[1].salario_mensual)
        self.assertEqual(1575.94, registros[2].salario_mensual)
        self.assertEqual(18911.25, registros[2].salario_anual)
        self.assertEqual(5.0625, registros[2].crecimiento_desde_base_pct)

    def test_porcentaje_negativo_disminuye_sin_convertirse_en_salario_nulo(self):
        resumen = proyectar_salario(
            DatosProyeccionSalario(
                salario_mensual_actual=1500,
                anio_inicio=2026,
                anio_fin=2027,
                modalidad="PORCENTAJE",
                porcentaje_anual=-2,
            )
        )

        registro = resumen.escenarios[0].registros[1]
        self.assertEqual(1470.0, registro.salario_mensual)
        self.assertEqual(17640.0, registro.salario_anual)

    def test_futuro_conocido_deriva_diez_por_ciento_y_alcanza_objetivo(self):
        resumen = proyectar_salario(
            DatosProyeccionSalario(
                salario_mensual_actual=1000,
                anio_inicio=2026,
                anio_fin=2028,
                modalidad="FUTURO_CONOCIDO",
                salario_mensual_futuro=1210,
                anio_salario_futuro=2028,
            )
        )

        escenario = resumen.escenarios[0]
        self.assertAlmostEqual(10.0, escenario.tasa_anual_pct, places=6)
        self.assertEqual(
            [1000.0, 1100.0, 1210.0],
            [registro.salario_mensual for registro in escenario.registros],
        )

    def test_futuro_conocido_irregular_llega_al_monto_indicado_a_centavos(self):
        resumen = proyectar_salario(
            DatosProyeccionSalario(
                salario_mensual_actual=1331.90,
                anio_inicio=2026,
                anio_fin=2029,
                modalidad="FUTURO_CONOCIDO",
                salario_mensual_futuro=1500,
                anio_salario_futuro=2029,
            )
        )

        registro_objetivo = resumen.escenarios[0].registros[-1]
        self.assertEqual(1500.0, registro_objetivo.salario_mensual)
        self.assertEqual(18000.0, registro_objetivo.salario_anual)

    def test_futuro_conocido_rechaza_anio_no_posterior(self):
        with self.assertRaisesRegex(ValueError, "posterior al año inicial"):
            proyectar_salario(
                DatosProyeccionSalario(
                    salario_mensual_actual=1500,
                    anio_inicio=2026,
                    anio_fin=2030,
                    modalidad="FUTURO_CONOCIDO",
                    salario_mensual_futuro=1700,
                    anio_salario_futuro=2026,
                )
            )

    def test_futuro_conocido_rechaza_anio_fuera_del_horizonte(self):
        with self.assertRaisesRegex(ValueError, "dentro del período de proyección"):
            proyectar_salario(
                DatosProyeccionSalario(
                    salario_mensual_actual=1500,
                    anio_inicio=2026,
                    anio_fin=2030,
                    modalidad="FUTURO_CONOCIDO",
                    salario_mensual_futuro=1700,
                    anio_salario_futuro=2031,
                )
            )

    def test_escenarios_elimina_duplicados_y_ordena_por_tasa(self):
        resumen = proyectar_salario(
            DatosProyeccionSalario(
                salario_mensual_actual=1500,
                anio_inicio=2026,
                anio_fin=2027,
                modalidad="ESCENARIOS",
                escenarios_porcentajes=[2, 0, 2, -1],
            )
        )

        self.assertEqual(
            [-1.0, 0.0, 2.0],
            [escenario.tasa_anual_pct for escenario in resumen.escenarios],
        )

    def test_rechaza_horizonte_con_fin_anterior_al_inicio(self):
        with self.assertRaisesRegex(ValueError, "año final"):
            proyectar_salario(
                DatosProyeccionSalario(
                    salario_mensual_actual=1500,
                    anio_inicio=2028,
                    anio_fin=2027,
                    modalidad="CONSTANTE",
                )
            )

    def test_linea_tiempo_separa_anio_actual_y_escala_futuro_por_cuotas(self):
        datos = DatosLineaTiempo(
            historial=DatosHistorialSalarial(
                anio_inicio=2026,
                anio_fin=2026,
                cuotas_totales_referencia=5,
                registros=[
                    RegistroHistorialSalarial(
                        anio=2026,
                        cuotas=5,
                        salario_cotizado=7500,
                    )
                ],
            ),
            cuotas=DatosCuotas(
                cuotas_totales=5,
                cuotas_anio_actual=5,
                continua_cotizando=True,
                cuotas_esperadas_cierre_anio=12,
                cuotas_esperadas_por_anio=6,
            ),
            salario_actual=DatosSalario(
                monto=1500,
                periodicidad="MENSUAL",
            ),
            proyeccion=DatosProyeccionSalario(
                salario_mensual_actual=1500,
                anio_inicio=2026,
                anio_fin=2027,
                modalidad="PORCENTAJE",
                porcentaje_anual=10,
            ),
        )

        resumen = construir_linea_tiempo(datos)
        actual, futuro = resumen.escenarios[0].registros

        self.assertEqual("MIXTO", actual.estado)
        self.assertEqual(5, actual.cuotas_historicas)
        self.assertEqual(7, actual.cuotas_proyectadas)
        self.assertEqual(7500.0, actual.salario_historico)
        self.assertEqual(10500.0, actual.salario_proyectado)
        self.assertEqual(18000.0, actual.salario_cierre)

        self.assertEqual("PROYECTADO", futuro.estado)
        self.assertEqual(6, futuro.cuotas_proyectadas)
        self.assertEqual(9900.0, futuro.salario_proyectado)
        self.assertEqual(9900.0, futuro.salario_cierre)


if __name__ == "__main__":
    unittest.main()
