"""Regresiones de UX.4.5: origen acreditado/proyectado y cierre accesible."""

import unittest
from datetime import date
from pathlib import Path

from app.models.pension import DatosResultadoSEBD
from app.models.simulation import (
    DatosHistorialSalarial,
    EscenarioLineaTiempo,
    EscenarioRetiro,
    RegistroHistorialSalarial,
    RegistroLineaTiempo,
    ResumenLineaTiempo,
    ResumenRetiro,
)
from app.services.sebd_results import calcular_resultado_sebd


ROOT = Path(__file__).resolve().parents[1]


class TestUX45CierreResultadosAccesibilidad(unittest.TestCase):
    """Valida que el resultado distinga datos acreditados y proyección."""

    @classmethod
    def setUpClass(cls):
        cls.resultados_js = (ROOT / "app/static/js/results.js").read_text(
            encoding="utf-8"
        )
        cls.simulacion_js = (ROOT / "app/static/js/simulation.js").read_text(
            encoding="utf-8"
        )
        cls.referencia_js = (
            ROOT / "app/static/js/mi_retiro_seguro_reference.js"
        ).read_text(encoding="utf-8")
        cls.resultados_html = (
            ROOT / "app/templates/partials/results.html"
        ).read_text(encoding="utf-8")
        cls.importacion_html = "\n".join([
            (ROOT / "app/templates/partials/official_data_import.html").read_text(encoding="utf-8"),
            (ROOT / "app/templates/partials/ficha_digital_import.html").read_text(encoding="utf-8"),
        ])
        cls.css = (ROOT / "app/static/css/style.css").read_text(encoding="utf-8")

    def _datos_femeninos(self, modo: str) -> DatosResultadoSEBD:
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
            anio_fin_proyeccion=2031,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Salario constante",
                    tasa_anual_pct=0.0,
                    registros=[
                        RegistroLineaTiempo(
                            anio=2026,
                            cuotas_historicas=5,
                            salario_historico=6659.50,
                            cuotas_proyectadas=7,
                            salario_proyectado=10500.00,
                            cuotas_cierre=12,
                            salario_cierre=17159.50,
                            estado="MIXTO",
                        ),
                        *[
                            RegistroLineaTiempo(
                                anio=anio,
                                cuotas_historicas=0,
                                salario_historico=0.0,
                                cuotas_proyectadas=12,
                                salario_proyectado=18000.00,
                                cuotas_cierre=12,
                                salario_cierre=18000.00,
                                estado="PROYECTADO",
                            )
                            for anio in range(2027, 2032)
                        ],
                    ],
                )
            ],
        )

        referencia = EscenarioRetiro(
            tipo="REFERENCIA",
            nombre="Edad de referencia",
            fecha_retiro=date(2026, 11, 16),
            edad_retiro_anios=57,
            meses_desde_corte_cuotas=5,
            cuotas_estimadas_adicionales=5,
            cuotas_estimadas_totales=286,
            fecha_ya_transcurrida=False,
        )

        retiro = ResumenRetiro(
            fecha_corte=date(2026, 8, 10),
            fecha_corte_cuotas=date(2026, 5, 31),
            edad_actual_anios=56,
            edad_referencia=57,
            fecha_referencia=date(2026, 11, 16),
            alcanzo_edad_referencia=False,
            dias_hasta_referencia=98,
            escenarios=[referencia],
            anio_fin_proyeccion_salarial=2031,
            proyeccion_salarial_cubre_escenarios=True,
            advertencias=[],
            metodo_estimacion_cuotas="Prueba UX.4.5",
        )

        return DatosResultadoSEBD(
            modo_integracion=modo,
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            historial=historial,
            linea_tiempo=linea,
            resumen_retiro=retiro,
            fecha_retiro_seleccionada=date(2026, 11, 16),
            escenario_salarial_nombre="Salario constante",
        )

    def test_fotografia_acreditada_reproduce_741_59_sin_periodos_futuros(self):
        resultado = calcular_resultado_sebd(
            self._datos_femeninos("SOLO_ACREDITADO")
        )

        self.assertEqual(resultado.modo_integracion, "SOLO_ACREDITADO")
        self.assertEqual(resultado.calculo.cuotas_totales, 281)
        self.assertEqual(resultado.calculo.salario_base_mensual, 1163.28)
        self.assertEqual(resultado.calculo.pension_mensual_estimada, 741.59)
        self.assertEqual(resultado.anios_proyectados_incluidos, [])

    def test_proyeccion_con_1500_mensuales_conserva_769_42(self):
        resultado = calcular_resultado_sebd(self._datos_femeninos("PROYECTADO"))

        self.assertEqual(resultado.modo_integracion, "PROYECTADO")
        self.assertEqual(resultado.calculo.cuotas_totales, 286)
        self.assertEqual(resultado.calculo.salario_base_mensual, 1206.94)
        self.assertEqual(resultado.calculo.pension_mensual_estimada, 769.42)
        self.assertEqual(resultado.anios_proyectados_incluidos, [2026])

    def test_frontend_solicita_segunda_evaluacion_solo_acreditada(self):
        self.assertIn('modo_integracion: "SOLO_ACREDITADO"', self.resultados_js)
        self.assertIn('"/api/simulacion/resultados/sebd"', self.resultados_js)
        self.assertIn('"/api/simulacion/resultados/mixto"', self.resultados_js)
        self.assertIn('"/api/simulacion/resultados/sucgs"', self.resultados_js)
        self.assertIn("mostrarComparacionOrigenDatos", self.resultados_js)

    def test_estado_temporal_separa_e_invalida_resultados_acreditados(self):
        self.assertIn("resultado_sebd_acreditado: null", self.simulacion_js)
        self.assertIn("resultado_mixto_acreditado: null", self.simulacion_js)
        self.assertIn("resultado_sucgs_acreditado: null", self.simulacion_js)
        self.assertIn("simulacion.resultado_sebd_acreditado = null", self.simulacion_js)

    def test_comparacion_visible_es_independiente_del_pdf(self):
        self.assertIn('id="resultado-comparacion-origen-datos"', self.resultados_html)
        self.assertIn("Información acreditada y proyección al retiro", self.resultados_html)
        self.assertIn("Solo información acreditada", self.resultados_html)
        self.assertIn("Proyección al retiro", self.resultados_html)
        self.assertIn('id="resultado-origen-estado"', self.resultados_html)

    def test_tabla_comparativa_tiene_semantica_accesible(self):
        self.assertIn("Comparación entre información acreditada", self.resultados_html)
        self.assertGreaterEqual(self.resultados_html.count('scope="col"'), 4)
        self.assertGreaterEqual(self.resultados_html.count('scope="row"'), 4)
        self.assertIn('role="status"', self.resultados_html)

    def test_referencia_pdf_prefiere_fotografia_acreditada_propia(self):
        self.assertIn("obtenerResumenAcreditadoReferenciaGuardado", self.referencia_js)
        self.assertIn("const resumenComparado = resumenAcreditado || resumenActual", self.referencia_js)
        self.assertIn("referencia.sistema_elegido === resumenComparado.sistema", self.referencia_js)

    def test_modales_importacion_conservan_titulo_y_cierre_accesibles(self):
        self.assertIn('aria-labelledby="modal-import-comprobante-titulo"', self.importacion_html)
        self.assertIn('aria-labelledby="modal-import-ficha-digital-titulo"', self.importacion_html)
        self.assertGreaterEqual(self.importacion_html.count('aria-label="Cerrar"'), 2)
        self.assertIn("<caption", self.importacion_html)

    def test_contraste_refuerza_comparacion_de_origen(self):
        self.assertIn(".result-data-origin-comparison", self.css)
        self.assertIn('html[data-app-theme="contrast"] .result-data-origin-comparison', self.css)
        self.assertIn("font-variant-numeric: tabular-nums", self.css)


if __name__ == "__main__":
    unittest.main()
