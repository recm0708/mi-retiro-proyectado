"""Regresiones de la estabilización visual UX.2.1."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "app/static/css/style.css"
TEMA = ROOT / "app/static/js/tema.js"
INDEX = ROOT / "app/templates/index.html"
TEMPLATES = ROOT / "app/templates"


class TestEstabilizacionVisual(unittest.TestCase):
    """Protege temas, portada y separación entre interfaz y detalles técnicos."""

    def test_oscuro_usa_superficies_casi_negras_y_texto_legible(self):
        contenido = CSS.read_text(encoding="utf-8")
        self.assertIn("--app-background: #05070b;", contenido)
        self.assertIn("--app-surface: #0d1117;", contenido)
        self.assertIn("--app-text-secondary: #c5cfdb;", contenido)
        self.assertIn("--bs-secondary-color: var(--app-muted);", contenido)

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
        self.assertIn("background: var(--app-sticky-bg);", contenido)
        self.assertIn(".wizard-step.active span", contenido)
        self.assertIn(".wizard-sticky-nav .form-select", contenido)

    def test_inicio_funciona_como_portada_orientada_al_asegurado(self):
        contenido = INDEX.read_text(encoding="utf-8")
        self.assertIn("Proyecta tu retiro con información clara y comparable", contenido)
        self.assertIn("Sistemas contemplados", contenido)
        self.assertIn("Analiza tu retiro desde varios ángulos", contenido)
        self.assertIn("De tus datos a un resultado explicado", contenido)
        self.assertIn("Comenzar simulación", contenido)

    def test_remate_ux21_centra_solo_los_botones_identificados(self):
        css = CSS.read_text(encoding="utf-8")
        index = INDEX.read_text(encoding="utf-8")
        simulacion = (TEMPLATES / "simulacion.html").read_text(encoding="utf-8")
        metodologia = (TEMPLATES / "metodologia.html").read_text(encoding="utf-8")
        resultados_js = (ROOT / "app/static/js/resultados.js").read_text(encoding="utf-8")

        self.assertIn(".btn-center-content {", css)
        self.assertIn("align-items: center;", css)
        self.assertIn("justify-content: center;", css)
        self.assertIn('btn-primary btn-center-content">Iniciar ahora', index)
        self.assertIn('btn-outline-primary btn-center-content', index)
        self.assertIn('btn-outline-secondary btn-center-content', simulacion)
        self.assertGreaterEqual(metodologia.count("btn-center-content"), 2)
        self.assertIn("align-self-start btn-center-content", resultados_js)

    def test_footer_mantiene_acceso_oficial_en_segunda_linea_en_escritorio_amplio(self):
        contenido = CSS.read_text(encoding="utf-8")
        self.assertIn("@media (min-width: 1400px)", contenido)
        self.assertIn("max-width: 1760px;", contenido)
        self.assertIn("white-space: nowrap;", contenido)

    def test_plantillas_no_exponen_detalles_de_implementacion(self):
        contenido = "\n".join(
            path.read_text(encoding="utf-8")
            for path in TEMPLATES.rglob("*.html")
        )
        prohibidos = [
            "normativa/*.json",
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
