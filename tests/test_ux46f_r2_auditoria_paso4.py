"""Regresiones UX.4.6f R2 para lógica, matemática y trazabilidad del Paso 4."""

from pathlib import Path
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


ROOT = Path(__file__).resolve().parents[1]


class TestUX46fR2AuditoriaPaso4(unittest.TestCase):
    """Protege contratos auditados de proyección y línea temporal."""

    @staticmethod
    def _linea_actual(
        *,
        salario_historico: float = 7321.13,
        cuotas_actuales: int = 5,
        continua: bool = True,
        cuotas_cierre: int = 12,
        cuotas_futuras: int = 12,
        anio_fin: int = 2031,
        modalidad: str = "CONSTANTE",
        porcentaje: float | None = None,
    ):
        return construir_linea_tiempo(
            DatosLineaTiempo(
                historial=DatosHistorialSalarial(
                    anio_inicio=2026,
                    anio_fin=2026,
                    cuotas_totales_referencia=cuotas_actuales,
                    registros=[
                        RegistroHistorialSalarial(
                            anio=2026,
                            cuotas=cuotas_actuales,
                            salario_cotizado=salario_historico,
                        )
                    ],
                ),
                cuotas=DatosCuotas(
                    cuotas_totales=cuotas_actuales,
                    cuotas_anio_actual=cuotas_actuales,
                    continua_cotizando=continua,
                    cuotas_esperadas_cierre_anio=cuotas_cierre,
                    cuotas_esperadas_por_anio=cuotas_futuras,
                ),
                salario_actual=DatosSalario(
                    monto=1500,
                    periodicidad="MENSUAL",
                ),
                proyeccion=DatosProyeccionSalario(
                    salario_mensual_actual=1500,
                    anio_inicio=2026,
                    anio_fin=anio_fin,
                    modalidad=modalidad,
                    porcentaje_anual=porcentaje,
                ),
            )
        )

    def test_01_caso_femenino_visible_cierra_2026_sin_deriva(self):
        resumen = self._linea_actual()
        actual = resumen.escenarios[0].registros[0]

        self.assertEqual(5, actual.cuotas_historicas)
        self.assertEqual(7, actual.cuotas_proyectadas)
        self.assertEqual(12, actual.cuotas_cierre)
        self.assertEqual(7321.13, actual.salario_historico)
        self.assertEqual(10500.0, actual.salario_proyectado)
        self.assertEqual(17821.13, actual.salario_cierre)
        self.assertEqual(1500.0, actual.salario_mensual_proyectado)

    def test_02_caso_femenino_constante_proyecta_18000_por_anio(self):
        resumen = self._linea_actual()
        futuros = resumen.escenarios[0].registros[1:]

        self.assertEqual([2027, 2028, 2029, 2030, 2031], [r.anio for r in futuros])
        self.assertTrue(all(r.cuotas_proyectadas == 12 for r in futuros))
        self.assertTrue(all(r.salario_mensual_proyectado == 1500.0 for r in futuros))
        self.assertTrue(all(r.salario_proyectado == 18000.0 for r in futuros))

    def test_03_rechaza_total_historial_distinto_del_paso2(self):
        datos = DatosLineaTiempo(
            historial=DatosHistorialSalarial(
                anio_inicio=2025,
                anio_fin=2026,
                cuotas_totales_referencia=6,
                registros=[
                    RegistroHistorialSalarial(anio=2025, cuotas=1, salario_cotizado=100),
                    RegistroHistorialSalarial(anio=2026, cuotas=5, salario_cotizado=7500),
                ],
            ),
            cuotas=DatosCuotas(
                cuotas_totales=5,
                cuotas_anio_actual=5,
                continua_cotizando=True,
                cuotas_esperadas_cierre_anio=12,
                cuotas_esperadas_por_anio=12,
            ),
            salario_actual=DatosSalario(monto=1500, periodicidad="MENSUAL"),
            proyeccion=DatosProyeccionSalario(
                salario_mensual_actual=1500,
                anio_inicio=2026,
                anio_fin=2027,
                modalidad="CONSTANTE",
            ),
        )

        with self.assertRaisesRegex(ValueError, "total acreditado del Paso 2"):
            construir_linea_tiempo(datos)

    def test_04_rechaza_cuotas_del_anio_actual_desincronizadas(self):
        datos = DatosLineaTiempo(
            historial=DatosHistorialSalarial(
                anio_inicio=2025,
                anio_fin=2026,
                cuotas_totales_referencia=5,
                registros=[
                    RegistroHistorialSalarial(anio=2025, cuotas=1, salario_cotizado=100),
                    RegistroHistorialSalarial(anio=2026, cuotas=4, salario_cotizado=6000),
                ],
            ),
            cuotas=DatosCuotas(
                cuotas_totales=5,
                cuotas_anio_actual=5,
                continua_cotizando=True,
                cuotas_esperadas_cierre_anio=12,
                cuotas_esperadas_por_anio=12,
            ),
            salario_actual=DatosSalario(monto=1500, periodicidad="MENSUAL"),
            proyeccion=DatosProyeccionSalario(
                salario_mensual_actual=1500,
                anio_inicio=2026,
                anio_fin=2027,
                modalidad="CONSTANTE",
            ),
        )

        with self.assertRaisesRegex(ValueError, "año actual del historial"):
            construir_linea_tiempo(datos)

    def test_05_rechaza_linea_temporal_con_historial_incompleto(self):
        datos = DatosLineaTiempo(
            historial=DatosHistorialSalarial(
                anio_inicio=2025,
                anio_fin=2026,
                cuotas_totales_referencia=5,
                registros=[
                    RegistroHistorialSalarial(anio=2026, cuotas=5, salario_cotizado=7500),
                ],
            ),
            cuotas=DatosCuotas(
                cuotas_totales=5,
                cuotas_anio_actual=5,
                continua_cotizando=True,
                cuotas_esperadas_cierre_anio=12,
                cuotas_esperadas_por_anio=12,
            ),
            salario_actual=DatosSalario(monto=1500, periodicidad="MENSUAL"),
            proyeccion=DatosProyeccionSalario(
                salario_mensual_actual=1500,
                anio_inicio=2026,
                anio_fin=2027,
                modalidad="CONSTANTE",
            ),
        )

        with self.assertRaisesRegex(ValueError, "cubrir todos los años"):
            construir_linea_tiempo(datos)

    def test_06_salario_mensual_futuro_se_transporta_sin_reconstruir(self):
        resumen = self._linea_actual(
            cuotas_futuras=6,
            anio_fin=2027,
            modalidad="PORCENTAJE",
            porcentaje=10,
        )
        futuro = resumen.escenarios[0].registros[-1]

        self.assertEqual(6, futuro.cuotas_proyectadas)
        self.assertEqual(1650.0, futuro.salario_mensual_proyectado)
        self.assertEqual(9900.0, futuro.salario_proyectado)

        js = (ROOT / "app/static/js/linea_tiempo.js").read_text(encoding="utf-8")
        self.assertIn("registro.salario_mensual_proyectado", js)

    def test_07_sin_cotizacion_futura_tiene_estado_explicito(self):
        resumen = self._linea_actual(
            continua=False,
            cuotas_cierre=5,
            cuotas_futuras=12,
            anio_fin=2027,
        )
        futuro = resumen.escenarios[0].registros[-1]

        self.assertEqual(0, futuro.cuotas_proyectadas)
        self.assertEqual(0.0, futuro.salario_proyectado)
        self.assertEqual("PROYECTADO_SIN_COTIZACION", futuro.estado)

    def test_08_futuro_conocido_no_inventa_crecimiento_despues_del_objetivo(self):
        resumen = proyectar_salario(
            DatosProyeccionSalario(
                salario_mensual_actual=1000,
                anio_inicio=2026,
                anio_fin=2030,
                modalidad="FUTURO_CONOCIDO",
                salario_mensual_futuro=1210,
                anio_salario_futuro=2028,
            )
        )
        escenario = resumen.escenarios[0]

        self.assertAlmostEqual(10.0, escenario.tasa_anual_pct, places=6)
        self.assertIn("constante después", escenario.nombre)
        self.assertEqual(
            [1000.0, 1100.0, 1210.0, 1210.0, 1210.0],
            [registro.salario_mensual for registro in escenario.registros],
        )

    def test_09_interfaz_explica_compuesto_y_futuro_conocido(self):
        plantilla = (ROOT / "app/templates/simulacion.html").read_text(encoding="utf-8")
        self.assertIn("Se aplica de forma compuesta", plantilla)
        self.assertIn("tasa anual compuesta necesaria", plantilla)
        self.assertIn("se mantendrá constante", plantilla)
        self.assertIn("Cada escenario se calcula de forma compuesta", plantilla)
        simulacion_js = (ROOT / "app/static/js/simulacion.js").read_text(encoding="utf-8")
        self.assertIn("Tasa equivalente al objetivo", simulacion_js)

    def test_10_ajuste_desde_retiro_actualiza_procedencia_y_borrador(self):
        retiro = (ROOT / "app/static/js/retiro.js").read_text(encoding="utf-8")
        simulacion = (ROOT / "app/static/js/simulacion.js").read_text(encoding="utf-8")

        self.assertIn('simulacion.origen_proyeccion_anio_fin = "AJUSTADO_DESDE_RETIRO"', retiro)
        self.assertIn("anio_fin: anioMaximo", retiro)
        self.assertIn('origen === "AJUSTADO_DESDE_RETIRO"', simulacion)
        self.assertIn("cubrir el escenario de retiro más lejano", simulacion)

    def test_11_documentacion_traza_r2(self):
        decisiones = (ROOT / "docs/DECISIONES.md").read_text(encoding="utf-8")
        especificacion = (ROOT / "docs/ESPECIFICACION_FUNCIONAL.md").read_text(encoding="utf-8")
        matriz = (ROOT / "docs/MATRIZ_TRAZABILIDAD.md").read_text(encoding="utf-8")
        validacion = (ROOT / "docs/VALIDACION.md").read_text(encoding="utf-8")

        self.assertIn("## ADR-172 —", decisiones)
        self.assertIn("## ADR-173 —", decisiones)
        for rf in range(358, 366):
            self.assertIn(f"**RF-{rf}.**", especificacion)
        self.assertIn("| TR-020 |", matriz)
        self.assertIn("| TR-021 |", matriz)
        self.assertIn("UX.4.6f R2", validacion)


    def test_12_escenarios_inicia_sin_porcentajes_predeterminados(self):
        plantilla = (ROOT / "app/templates/simulacion.html").read_text(encoding="utf-8")
        javascript = (ROOT / "app/static/js/simulacion.js").read_text(encoding="utf-8")

        self.assertNotIn('value="0, 1, 2, 3"', plantilla)
        self.assertIn('placeholder="Escribe los porcentajes a comparar"', plantilla)
        self.assertIn("let escenariosPorcentajes = [];", javascript)

        datos = DatosProyeccionSalario(
            salario_mensual_actual=1500,
            anio_inicio=2026,
            anio_fin=2031,
            modalidad="ESCENARIOS",
        )
        self.assertEqual([], datos.escenarios_porcentajes)

    def test_13_escenarios_exige_porcentajes_explicitamente(self):
        with self.assertRaisesRegex(
            ValueError,
            "al menos un escenario",
        ):
            proyectar_salario(
                DatosProyeccionSalario(
                    salario_mensual_actual=1500,
                    anio_inicio=2026,
                    anio_fin=2031,
                    modalidad="ESCENARIOS",
                )
            )


if __name__ == "__main__":
    unittest.main()
