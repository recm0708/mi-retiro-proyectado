"""Regresiones de UX.4.6d R10 para el contrato visual transversal de tablas."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision10TablasTransversales(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.design = (ROOT / "app/static/css/design-system.css").read_text(encoding="utf-8")
        cls.accesibilidad = (ROOT / "app/static/js/accesibilidad.js").read_text(encoding="utf-8")
        cls.simulacion_js = (ROOT / "app/static/js/simulacion.js").read_text(encoding="utf-8")
        cls.linea_tiempo_js = (ROOT / "app/static/js/linea_tiempo.js").read_text(encoding="utf-8")

    def test_tablas_estaticas_principales_usan_superficie_comun(self):
        rutas = (
            "app/templates/partials/historial_salarial.html",
            "app/templates/partials/detalle_anio_actual.html",
            "app/templates/partials/importacion_datos_oficiales.html",
            "app/templates/partials/importacion_ficha_digital.html",
            "app/templates/partials/retiro.html",
            "app/templates/partials/resultados.html",
            "app/templates/comparar.html",
        )
        for ruta in rutas:
            contenido = (ROOT / ruta).read_text(encoding="utf-8")
            self.assertIn("app-table-shell", contenido, ruta)

    def test_tablas_dinamicas_reutilizan_el_mismo_contrato(self):
        self.assertIn('"table-responsive app-table-shell"', self.simulacion_js)
        self.assertIn('"timeline-history-wrapper app-table-shell"', self.linea_tiempo_js)
        self.assertIn('"table-responsive app-table-shell"', self.linea_tiempo_js)

    def test_superficie_comun_define_radio_borde_y_encabezado(self):
        self.assertIn(".app-table-shell {", self.design)
        self.assertIn("--app-table-radius: var(--app-radius-lg)", self.design)
        self.assertIn("border-radius: var(--app-table-radius) !important", self.design)
        self.assertIn("--app-table-shell-border:", self.design)
        self.assertIn("--app-table-header-bg:", self.design)
        self.assertIn("border-collapse: separate", self.design)
        self.assertIn("border-top-left-radius", self.design)
        self.assertIn("border-bottom-right-radius", self.design)

    def test_paleta_tabular_tiene_adaptacion_oscura_y_alto_contraste(self):
        self.assertIn('html[data-bs-theme="dark"] .app-table-shell', self.design)
        self.assertIn('html[data-app-theme="contrast"] .app-table-shell', self.design)
        self.assertIn("border-width: 2px !important", self.design)
        self.assertIn("--app-table-header-bg: #000000", self.design)

    def test_accesibilidad_reconoce_superficie_tabular_comun(self):
        self.assertIn('querySelectorAll(".app-table-shell,', self.accesibilidad)
        self.assertIn('contenedor.setAttribute("aria-label", "Tabla desplazable horizontalmente")', self.accesibilidad)

    def test_contrato_visual_no_reemplaza_semanticas_especificas(self):
        historial_js = (ROOT / "app/static/js/historial_salarios.js").read_text(encoding="utf-8")
        detalle = (ROOT / "app/static/js/detalle_anio_actual.js").read_text(encoding="utf-8")
        self.assertIn("function evaluarEstadoFilaHistorial", historial_js)
        self.assertIn("cuota_acreditada", detalle)
        self.assertIn("data-row-imported", self.design)


if __name__ == "__main__":
    unittest.main()
