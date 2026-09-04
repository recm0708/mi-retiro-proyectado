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
        cls.simulacion = (ROOT / "app/templates/simulation.html").read_text(encoding="utf-8")
        cls.detalle = (
            ROOT / "app/templates/partials/current_year_detail.html"
        ).read_text(encoding="utf-8")
        cls.ficha = (
            ROOT / "app/templates/partials/ficha_digital_import.html"
        ).read_text(encoding="utf-8")
        cls.simulacion_js = (
            ROOT / "app/static/js/simulation.js"
        ).read_text(encoding="utf-8")
        cls.historial_js = (
            ROOT / "app/static/js/salary_history.js"
        ).read_text(encoding="utf-8")

    def test_paso3_agrupa_ficha_digital_dentro_del_detalle_actual(self):
        paso3 = self.simulacion.split(
            'data-panel="3"',
            1,
        )[1].split(
            'data-panel="4"',
            1,
        )[0]

        assisted = (
            ROOT
            / "app/templates/partials/assisted_preparation.html"
        ).read_text(
            encoding="utf-8"
        )

        self.assertLess(
            paso3.index(
                "partials/salary_history.html"
            ),
            paso3.index(
                "partials/current_year_detail.html"
            ),
        )

        self.assertNotIn(
            "partials/ficha_digital_import.html",
            paso3,
        )

        self.assertNotIn(
            "partials/ficha_digital_import.html",
            self.detalle,
        )

        self.assertIn(
            "partials/ficha_digital_import.html",
            assisted,
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
        assisted = (
            ROOT
            / "app/templates/partials/assisted_preparation.html"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "partials/ficha_digital_import.html",
            assisted,
        )

        self.assertNotIn(
            "partials/ficha_digital_import.html",
            self.detalle,
        )

        self.assertIn(
            'id="seccion-detalle-anio-actual"',
            self.detalle,
        )

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
