"""Regresiones UX.4.6d R15: campos bloqueados, copia documental y limpieza Paso 2."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision15CamposImportacionYLimpieza(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.design = (ROOT / "app/static/css/design-system.css").read_text(encoding="utf-8")
        cls.simulacion = (ROOT / "app/templates/simulation.html").read_text(encoding="utf-8")
        cls.importador = (ROOT / "app/templates/partials/official_data_import.html").read_text(encoding="utf-8")
        cls.ficha = (ROOT / "app/templates/partials/ficha_digital_import.html").read_text(encoding="utf-8")
        cls.simulacion_js = (ROOT / "app/static/js/simulation.js").read_text(encoding="utf-8")
        cls.importacion_js = (ROOT / "app/static/js/official_data_import.js").read_text(encoding="utf-8")

    def test_campos_no_editables_tienen_contrato_visual_transversal(self):
        for token in (
            "--app-field-locked-bg",
            "--app-field-locked-border",
            "--app-field-locked-text",
        ):
            self.assertGreaterEqual(self.design.count(token), 4)
        self.assertIn(':is(.form-control, .form-select):disabled', self.design)
        self.assertIn('.form-control[readonly]', self.design)
        self.assertIn('box-shadow: inset 3px 0 0 var(--app-primary) !important', self.design)
        self.assertIn('html[data-app-theme="contrast"] :is(.form-control, .form-select):disabled', self.design)

    def test_paso1_no_presenta_importacion_como_pdf_en_encabezados_principales(self):
        simulacion = (
            ROOT
            / "app/templates/simulation.html"
        ).read_text(
            encoding="utf-8"
        )

        paso1 = simulacion.split(
            'data-panel="1"',
            1,
        )[1].split(
            'data-panel="2"',
            1,
        )[0]

        assisted = (
            ROOT
            / "app/templates/partials/assisted_preparation.html"
        ).read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            "Mi Retiro Seguro",
            paso1,
        )

        self.assertNotIn(
            "Ficha Digital",
            paso1,
        )

        self.assertIn(
            "Mi Retiro Seguro",
            assisted,
        )

        self.assertIn(
            "Ficha Digital",
            assisted,
        )

    def test_ficha_digital_usa_copia_de_documento_no_de_pdf(self):
        self.assertIn("1. Selecciona el documento", self.ficha)
        self.assertNotIn("1. Selecciona el PDF", self.ficha)
        self.assertIn("Selecciona primero el documento de Ficha Digital", self.importacion_js)

    def test_cotizacion_futura_inicia_vacia_y_sin_presunciones(self):
        bloque = self.simulacion.split('id="cotizacion-futura-titulo"', 1)[1].split('id="error-cuotas"', 1)[0]
        self.assertIn('<option value="" selected disabled>Selecciona una opción</option>', bloque)
        self.assertNotIn('value="12"', bloque)
        self.assertIn('} else if (continua === "true") {', self.simulacion_js)
        self.assertIn('Estado limpio/nuevo: ninguna decisión de cotización futura se presume.', self.simulacion_js)
        self.assertIn('cierre.value = "";', self.simulacion_js)
        self.assertIn('futuras.value = "";', self.simulacion_js)
        self.assertIn('simulacion.cuotas?.cuotas_totales != null', self.simulacion_js)
        self.assertIn('simulacion.cuotas?.cuotas_anio_actual != null', self.simulacion_js)


if __name__ == "__main__":
    unittest.main()
