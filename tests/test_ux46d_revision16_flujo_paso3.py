"""Regresiones UX.4.6d R16: dependencias y jerarquía del Paso 3."""

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


ROOT = Path(__file__).resolve().parents[1]


class TestUX46dRevision16FlujoPaso3(unittest.TestCase):
    """Protege que Paso 3 no obligue a retroceder por una validación recuperable."""

    @classmethod
    def setUpClass(cls):
        cls.simulacion = (ROOT / "app/templates/simulacion.html").read_text(encoding="utf-8")
        cls.detalle = (
            ROOT / "app/templates/partials/detalle_anio_actual.html"
        ).read_text(encoding="utf-8")
        cls.ficha = (
            ROOT / "app/templates/partials/importacion_ficha_digital.html"
        ).read_text(encoding="utf-8")
        cls.simulacion_js = (
            ROOT / "app/static/js/simulacion.js"
        ).read_text(encoding="utf-8")
        cls.historial_js = (
            ROOT / "app/static/js/historial_salarios.js"
        ).read_text(encoding="utf-8")

    def test_paso3_agrupa_ficha_digital_dentro_del_detalle_actual(self):
        paso3 = self.simulacion.split('data-panel="3"', 1)[1].split('data-panel="4"', 1)[0]
        self.assertLess(
            paso3.index('partials/historial_salarial.html'),
            paso3.index('partials/detalle_anio_actual.html'),
        )
        self.assertNotIn('partials/importacion_ficha_digital.html', paso3)
        self.assertIn('partials/importacion_ficha_digital.html', self.detalle)
        self.assertLess(
            self.detalle.index('partials/importacion_ficha_digital.html'),
            self.detalle.index('id="detalle-anio-actual-contenido"'),
        )

    def test_render_final_mantiene_fuente_antes_de_tabla_mensual(self):
        respuesta = TestClient(app).get("/simulacion")
        self.assertEqual(respuesta.status_code, 200)
        html = respuesta.text
        self.assertLess(
            html.index("Importar salarios recientes desde Ficha Digital"),
            html.index('id="detalle-anio-actual-contenido"'),
        )
        self.assertLess(
            html.index("Historial salarial anual"),
            html.index("Detalle salarial del año actual"),
        )
        self.assertLess(
            html.index("Detalle salarial del año actual"),
            html.index("Base salarial para proyección"),
        )

    def test_ficha_digital_es_componente_interno_y_no_nuevo_subpaso(self):
        self.assertIn('id="seccion-importacion-ficha"', self.ficha)
        self.assertNotIn('step3-subsection mt-5', self.ficha)
        self.assertIn('official-import-section mt-4 mb-4', self.ficha)

    def test_paso3_revalida_cuotas_sin_navegar_hacia_atras(self):
        self.assertIn('async function asegurarCuotasAnalizadasParaPaso3()', self.simulacion_js)
        self.assertIn('await analizarCuotas(', self.simulacion_js)
        self.assertIn('{ mostrarMensajes: false, reportarValidez: false }', self.simulacion_js)
        self.assertIn('const cuotasListas = await asegurarCuotasAnalizadasParaPaso3();', self.simulacion_js)
        self.assertNotIn('mostrarPaso(2);', self.historial_js)

    def test_historial_reutiliza_la_revalidacion_automatica(self):
        self.assertIn('await asegurarCuotasAnalizadasParaPaso3()', self.historial_js)
        self.assertNotIn('Primero debes analizar las cuotas en el Paso 2.', self.historial_js)

    def test_restauracion_no_reabre_un_paso_con_dependencias_invalidas(self):
        self.assertIn('let pasoRestaurado', self.simulacion_js)
        self.assertIn('!puedeAccederDirectamenteAPaso(', self.simulacion_js)
        self.assertIn('pasoRestaurado -= 1;', self.simulacion_js)
        self.assertIn('mostrarPaso(pasoRestaurado);', self.simulacion_js)


if __name__ == "__main__":
    unittest.main()
