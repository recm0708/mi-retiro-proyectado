"""Pruebas de fechas y escenarios preliminares de retiro."""

import unittest
from datetime import date

from app.models.simulacion import (
    DatosRetiro,
)
from app.services.retiro import (
    analizar_retiro,
)


class RetiroTests(unittest.TestCase):
    """Valida referencias por sexo y coherencia de cuotas."""

    def test_caso_femenino_respeta_cierre_2026(self):
        resumen = analizar_retiro(
            DatosRetiro(
                fecha_nacimiento=date(
                    1969,
                    11,
                    16,
                ),
                sexo="FEMENINO",
                fecha_corte=date(
                    2026,
                    8,
                    10,
                ),
                fecha_corte_cuotas=date(
                    2026,
                    8,
                    10,
                ),
                cuotas_reales=281,
                cuotas_anio_actual=5,
                cuotas_esperadas_cierre_anio=5,
                continua_cotizando=True,
                cuotas_esperadas_por_anio=12,
                anio_fin_proyeccion_salarial=2027,
                anios_adicionales=[
                    0,
                    1,
                    2,
                    3,
                    5,
                ],
            )
        )

        self.assertEqual(
            resumen.edad_actual_anios,
            56,
        )
        self.assertEqual(
            resumen.fecha_referencia,
            date(2026, 11, 16),
        )
        self.assertEqual(
            resumen.dias_hasta_referencia,
            98,
        )

        referencia = resumen.escenarios[0]

        self.assertEqual(
            referencia.cuotas_estimadas_adicionales,
            0,
        )
        self.assertEqual(
            referencia.cuotas_estimadas_totales,
            281,
        )

        self.assertFalse(
            resumen.proyeccion_salarial_cubre_escenarios
        )
        self.assertTrue(
            resumen.advertencias
        )

    def test_referencia_mas_un_anio_usa_meses_del_2027(self):
        resumen = analizar_retiro(
            DatosRetiro(
                fecha_nacimiento=date(
                    1969,
                    11,
                    16,
                ),
                sexo="FEMENINO",
                fecha_corte=date(
                    2026,
                    8,
                    10,
                ),
                fecha_corte_cuotas=date(
                    2026,
                    8,
                    10,
                ),
                cuotas_reales=281,
                cuotas_anio_actual=5,
                cuotas_esperadas_cierre_anio=5,
                continua_cotizando=True,
                cuotas_esperadas_por_anio=12,
                anio_fin_proyeccion_salarial=2031,
                anios_adicionales=[0, 1],
            )
        )

        escenario = resumen.escenarios[1]

        self.assertEqual(
            escenario.fecha_retiro,
            date(2027, 11, 16),
        )
        self.assertEqual(
            escenario.cuotas_estimadas_adicionales,
            10,
        )
        self.assertEqual(
            escenario.cuotas_estimadas_totales,
            291,
        )

    def test_incluye_escenarios_anticipados_estandar(self):
        resumen = analizar_retiro(
            DatosRetiro(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_corte=date(2024, 8, 10),
                fecha_corte_cuotas=date(2024, 8, 10),
                cuotas_reales=240,
                cuotas_anio_actual=8,
                cuotas_esperadas_cierre_anio=12,
                continua_cotizando=True,
                cuotas_esperadas_por_anio=12,
                anio_fin_proyeccion_salarial=2031,
                anios_adicionales=[-2, -1, 0],
            )
        )

        self.assertEqual(resumen.escenarios[0].tipo, "ANTICIPADO")
        self.assertEqual(
            resumen.escenarios[0].fecha_retiro,
            date(2024, 11, 16),
        )
        self.assertEqual(resumen.escenarios[1].tipo, "ANTICIPADO")
        self.assertEqual(resumen.escenarios[2].tipo, "REFERENCIA")


    def test_ultimo_mes_acreditado_deriva_corte_al_fin_de_mes(self):
        resumen = analizar_retiro(
            DatosRetiro(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_corte=date(2026, 8, 10),
                ultimo_mes_cuotas="2026-05",
                cuotas_reales=281,
                cuotas_anio_actual=5,
                cuotas_esperadas_cierre_anio=5,
                continua_cotizando=True,
                cuotas_esperadas_por_anio=12,
                anio_fin_proyeccion_salarial=2031,
                anios_adicionales=[0],
            )
        )

        self.assertEqual(
            resumen.fecha_corte_cuotas,
            date(2026, 5, 31),
        )
        self.assertIn(
            "último mes con cuotas acreditadas",
            resumen.metodo_estimacion_cuotas.lower(),
        )

    def test_ultimo_mes_actual_no_supera_fecha_de_evaluacion(self):
        resumen = analizar_retiro(
            DatosRetiro(
                fecha_nacimiento=date(1969, 11, 16),
                sexo="FEMENINO",
                fecha_corte=date(2026, 8, 10),
                ultimo_mes_cuotas="2026-08",
                cuotas_reales=281,
                cuotas_anio_actual=5,
                cuotas_esperadas_cierre_anio=5,
                continua_cotizando=True,
                cuotas_esperadas_por_anio=12,
                anio_fin_proyeccion_salarial=2031,
                anios_adicionales=[0],
            )
        )

        self.assertEqual(
            resumen.fecha_corte_cuotas,
            date(2026, 8, 10),
        )

    def test_ultimo_mes_futuro_se_rechaza(self):
        with self.assertRaisesRegex(
            ValueError,
            "último mes con cuotas acreditadas",
        ):
            analizar_retiro(
                DatosRetiro(
                    fecha_nacimiento=date(1969, 11, 16),
                    sexo="FEMENINO",
                    fecha_corte=date(2026, 8, 10),
                    ultimo_mes_cuotas="2026-09",
                    cuotas_reales=281,
                    cuotas_anio_actual=5,
                    cuotas_esperadas_cierre_anio=5,
                    continua_cotizando=True,
                    cuotas_esperadas_por_anio=12,
                    anio_fin_proyeccion_salarial=2031,
                    anios_adicionales=[0],
                )
            )

    def test_referencia_masculina_es_62(self):
        resumen = analizar_retiro(
            DatosRetiro(
                fecha_nacimiento=date(
                    1966,
                    12,
                    4,
                ),
                sexo="MASCULINO",
                fecha_corte=date(
                    2026,
                    8,
                    10,
                ),
                fecha_corte_cuotas=date(
                    2026,
                    8,
                    10,
                ),
                cuotas_reales=461,
                cuotas_anio_actual=0,
                cuotas_esperadas_cierre_anio=0,
                continua_cotizando=False,
                cuotas_esperadas_por_anio=0,
                anio_fin_proyeccion_salarial=2028,
                anios_adicionales=[0],
            )
        )

        self.assertEqual(
            resumen.edad_referencia,
            62,
        )
        self.assertEqual(
            resumen.fecha_referencia,
            date(2028, 12, 4),
        )


if __name__ == "__main__":
    unittest.main()
