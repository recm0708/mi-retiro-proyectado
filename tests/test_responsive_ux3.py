"""Regresiones de UX.3: responsive, navegación móvil y Paso 5."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "app/static/css/style.css"
DESIGN = ROOT / "app/static/css/design-system.css"
SIMULACION = ROOT / "app/templates/simulacion.html"
RETIRO = ROOT / "app/templates/partials/retiro.html"
METODOLOGIA = ROOT / "app/templates/metodologia.html"
RETIRO_JS = ROOT / "app/static/js/retiro.js"


class TestResponsiveUX3(unittest.TestCase):
    """Protege las decisiones responsive y la semántica del Paso 5."""

    def test_barra_wizard_conserva_responsive_sin_cubrir_contenido(self):
        css = CSS.read_text(encoding="utf-8")
        moderno = DESIGN.read_text(encoding="utf-8")

        self.assertIn("Responsive y navegación móvil", css)
        self.assertIn("Paso 1 y navegación común del asistente", moderno)
        self.assertIn(".wizard-navigation-bar-top", moderno)
        self.assertIn("position: sticky;", moderno)
        self.assertIn(".wizard-navigation-bar-bottom", moderno)
        self.assertIn("padding-bottom: 2rem !important;", moderno)

    def test_progreso_y_tablas_no_comprimen_contenido_en_movil(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertIn("scroll-snap-type: x proximity;", css)
        self.assertIn(".retirement-table {\n  min-width: 940px;", css)
        self.assertIn(".comparison-table {\n  min-width: 1080px;", css)
        self.assertIn("-webkit-overflow-scrolling: touch;", css)

    def test_acciones_del_wizard_se_adaptan_a_ancho_completo(self):
        css = CSS.read_text(encoding="utf-8")
        simulacion = SIMULACION.read_text(encoding="utf-8")

        self.assertIn(".wizard-actions {", css)
        self.assertIn("flex-direction: column-reverse;", css)
        self.assertIn('data-wizard-nav="top"', simulacion)
        self.assertIn('data-wizard-nav="bottom"', simulacion)
        self.assertIn('id="wizard-sticky-primary"', simulacion)
        self.assertIn(".wizard-actions .btn", css)
        self.assertIn("width: 100%;", css)

    def test_paso5_separa_evaluacion_de_ultimo_mes_acreditado(self):
        retiro = RETIRO.read_text(encoding="utf-8")
        retiro_js = RETIRO_JS.read_text(encoding="utf-8")

        self.assertIn('type="month"', retiro)
        self.assertIn('id="ultimo_mes_cuotas"', retiro)
        self.assertIn("Último mes con cuotas acreditadas", retiro)
        self.assertIn("No es la fecha en la que", retiro)
        self.assertIn("convertirMesCuotasAFechaCorte", retiro_js)
        self.assertIn("ultimo_mes_cuotas: ultimoMesCuotas", retiro_js)
        self.assertNotIn('id="fecha_corte_cuotas"', retiro)

    def test_recursos_oficiales_conservan_nombre_y_centran_accion(self):
        metodologia = METODOLOGIA.read_text(encoding="utf-8")

        self.assertIn("Recursos oficiales para verificar información individual", metodologia)
        self.assertIn("Abrir fuente oficial", metodologia)
        self.assertNotIn("Abrir recurso oficial", metodologia)
        self.assertIn("recurso.url", metodologia)
        self.assertIn(
            "btn btn-sm btn-outline-primary btn-center-content",
            metodologia,
        )

    def test_navegacion_movil_mantiene_selector_de_tema_y_menu_tactil(self):
        css = CSS.read_text(encoding="utf-8")

        self.assertIn(".app-navbar .navbar-collapse", css)
        self.assertIn(".app-navbar .nav-link", css)
        self.assertIn(".theme-select", css)
        self.assertIn("min-height: 48px;", css)


if __name__ == "__main__":
    unittest.main()
