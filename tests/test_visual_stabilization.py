"""Regresiones de estabilización visual y evolución UX.4.6a."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "app/static/css/style.css"
DESIGN = ROOT / "app/static/css/design-system.css"
TEMA = ROOT / "app/static/js/tema.js"
INDEX = ROOT / "app/templates/index.html"
BASE = ROOT / "app/templates/base.html"
TEMPLATES = ROOT / "app/templates"


class TestEstabilizacionVisual(unittest.TestCase):
    """Protege temas, portada y separación entre interfaz y detalles técnicos."""

    def test_oscuro_conserva_base_estable_y_capa_moderna_profunda(self):
        historico = CSS.read_text(encoding="utf-8")
        moderno = DESIGN.read_text(encoding="utf-8")

        self.assertIn("--app-background: #05070b;", historico)
        self.assertIn("--app-surface: #0d1117;", historico)
        self.assertIn("--app-background: #070b12;", moderno)
        self.assertIn("--app-surface: #0d1420;", moderno)
        self.assertIn("--app-text-secondary: #b8c2d6;", moderno)

    def test_alto_contraste_es_negro_y_se_resuelve_como_tema_oscuro(self):
        css = CSS.read_text(encoding="utf-8")
        tema = TEMA.read_text(encoding="utf-8")
        self.assertIn("--app-background: #000000;", css)
        self.assertIn("--app-text: #ffffff;", css)
        self.assertIn("--app-focus: #ffdf00;", css)
        self.assertIn('if (preference === "contrast")', tema)
        self.assertIn('return "dark";', tema)

    def test_wizard_y_barra_rapida_consumen_superficies_del_tema(self):
        contenido = CSS.read_text(encoding="utf-8")
        moderno = DESIGN.read_text(encoding="utf-8")
        self.assertIn("background: var(--app-sticky-bg);", contenido)
        self.assertIn(".wizard-step.active span", contenido)
        self.assertIn(".wizard-sticky-nav .form-select", contenido)
        self.assertIn("backdrop-filter: blur(16px);", moderno)

    def test_inicio_es_portada_orientada_a_beneficios_y_no_al_motor(self):
        contenido = INDEX.read_text(encoding="utf-8")
        self.assertIn("Planifica tu retiro con más claridad", contenido)
        self.assertIn("Proyecta tu jubilación con información clara, útil y comparable", contenido)
        self.assertIn("Vista ilustrativa", contenido)
        self.assertIn("Entiende mejor cada decisión de retiro", contenido)
        self.assertIn("De tus datos a un resultado explicado", contenido)
        self.assertIn("Comenzar simulación", contenido)
        self.assertNotIn("motor de cálculo específico", contenido)

    def test_botones_identificados_conservan_centrado(self):
        css = CSS.read_text(encoding="utf-8")
        index = INDEX.read_text(encoding="utf-8")
        simulacion = (TEMPLATES / "simulation.html").read_text(encoding="utf-8")
        metodologia = (TEMPLATES / "metodologia.html").read_text(encoding="utf-8")
        resultados_js = (ROOT / "app/static/js/results.js").read_text(encoding="utf-8")

        self.assertIn(".btn-center-content {", css)
        self.assertIn("align-items: center;", css)
        self.assertIn("justify-content: center;", css)
        self.assertIn('btn-primary btn-center-content px-4', index)
        self.assertIn('btn-outline-primary btn-center-content', index)
        self.assertIn('id="wizard-sticky-back"', simulacion)
        self.assertIn('class="btn btn-outline-secondary"', simulacion)
        self.assertGreaterEqual(metodologia.count("btn-center-content"), 2)
        self.assertIn("align-self-start btn-center-content", resultados_js)

    def test_footer_moderno_no_repite_acceso_a_mi_caja_digital(self):
        base = BASE.read_text(encoding="utf-8")
        moderno = DESIGN.read_text(encoding="utf-8")

        self.assertIn("footer-modern", base)
        self.assertIn("No sustituye la determinación oficial", base)
        self.assertIn("Fuentes oficiales", base)
        self.assertNotIn("Abrir Mi Caja Digital", base)
        self.assertIn(".footer-modern {", moderno)
        self.assertIn(".footer-identity {", moderno)
        self.assertIn(".footer-version {", moderno)
        self.assertIn(".footer-bottom {", moderno)

    def test_plantillas_no_exponen_detalles_de_implementacion(self):
        contenido = "\n".join(
            path.read_text(encoding="utf-8")
            for path in TEMPLATES.rglob("*.html")
        )
        prohibidos = [
            "regulations/*.json",
            "metadatos versionados",
            "Documentación técnica del proyecto",
            "Paso 6F.",
            "Metodología 6F.",
        ]
        for texto in prohibidos:
            with self.subTest(texto=texto):
                self.assertNotIn(texto, contenido)


if __name__ == "__main__":
    unittest.main()
