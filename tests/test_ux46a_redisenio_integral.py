"""Regresiones de UX.4.6a: rediseño visual integral y nueva portada."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "app/templates/base.html"
INDEX = ROOT / "app/templates/index.html"
DESIGN = ROOT / "app/static/css/design-system.css"
TEMA = ROOT / "app/static/js/theme.js"


class TestUX46aRedisenioIntegral(unittest.TestCase):
    """Protege el contrato visual introducido antes de la primera beta."""

    @classmethod
    def setUpClass(cls):
        cls.base = BASE.read_text(encoding="utf-8")
        cls.index = INDEX.read_text(encoding="utf-8")
        cls.design = DESIGN.read_text(encoding="utf-8")
        cls.tema = TEMA.read_text(encoding="utf-8")

    def test_capa_visual_se_carga_entre_base_y_accesibilidad(self):
        style_pos = self.base.index("path='/css/style.css'")
        design_pos = self.base.index("path='/css/design-system.css'")
        a11y_pos = self.base.index("path='/css/accessibility.css'")

        self.assertLess(style_pos, design_pos)
        self.assertLess(design_pos, a11y_pos)

    def test_navegacion_publica_usa_nombres_cortos(self):
        for etiqueta in (
            "Inicio",
            "Simular",
            "Escenarios",
            "Fuentes",
        ):
            with self.subTest(etiqueta=etiqueta):
                self.assertIn(
                    f"<span>{etiqueta}</span>",
                    self.base,
                )

        for legacy in (
            "Nueva simulación",
            "Comparar escenarios",
            "Metodología y fuentes",
        ):
            self.assertNotIn(
                legacy,
                self.base,
            )

    def test_alto_contraste_permanece_como_opcion_secundaria(self):
        posicion_claro = self.base.index(
            'data-theme-choice="light"'
        )

        posicion_oscuro = self.base.index(
            'data-theme-choice="dark"'
        )

        posicion_divisor = self.base.index(
            'class="dropdown-divider"'
        )

        posicion_contraste = self.base.index(
            'data-theme-choice="contrast"'
        )

        self.assertLess(
            posicion_claro,
            posicion_divisor,
        )

        self.assertLess(
            posicion_oscuro,
            posicion_divisor,
        )

        self.assertGreater(
            posicion_contraste,
            posicion_divisor,
        )

        self.assertIn(
            "Alto contraste",
            self.base,
        )

        self.assertIn(
            'aria-describedby="ayuda-selector-tema"',
            self.base,
        )

    def test_tema_actual_actualiza_etiqueta_y_estado_de_botones(self):
        self.assertIn("THEME_LABELS", self.tema)
        self.assertIn("theme-trigger-label", self.tema)
        self.assertIn('setAttribute("aria-pressed"', self.tema)
        self.assertIn("data-theme-choice", self.tema)
        self.assertIn("localStorage", self.tema)

    def test_footer_es_legal_compacto_y_sin_mi_caja_digital(self):
        self.assertIn("footer-modern", self.base)
        self.assertIn("Herramienta independiente de estimación previsional", self.base)
        self.assertIn("No sustituye la determinación oficial", self.base)
        self.assertIn("v{{ app_version }}", self.base)
        self.assertNotIn("Abrir Mi Caja Digital", self.base)

    def test_portada_prioriza_beneficios_y_mockup_sin_resultado_ficticio(self):
        self.assertIn("Planifica tu retiro con más claridad", self.index)
        self.assertIn("Vista ilustrativa", self.index)
        self.assertIn("B/. —", self.index)
        self.assertIn("El resultado se calcula con tus propios datos", self.index)
        self.assertNotIn("motor de cálculo específico", self.index)

    def test_paleta_clara_define_superficies_y_textos_modernos(self):
        self.assertIn("--app-background: #f7f9fc;", self.design)
        self.assertIn("--app-surface: #ffffff;", self.design)
        self.assertIn("--app-text: #0f172a;", self.design)
        self.assertIn("--app-primary: #2563eb;", self.design)

    def test_paleta_oscura_es_profunda_y_legible(self):
        self.assertIn('html[data-bs-theme="dark"] {', self.design)
        self.assertIn("--app-background: #070b12;", self.design)
        self.assertIn("--app-surface: #0d1420;", self.design)
        self.assertIn("--app-text: #f8fafc;", self.design)
        self.assertIn("--app-text-secondary: #b8c2d6;", self.design)

    def test_controles_y_tarjetas_comparten_lenguaje_visual(self):
        self.assertIn("border-radius: 0.78rem;", self.design)
        self.assertIn(".form-control,", self.design)
        self.assertIn(".simulation-card,", self.design)
        self.assertIn(".comparison-card,", self.design)
        self.assertIn(".methodology-source-card,", self.design)
        self.assertIn(".summary-card,", self.design)

    def test_componentes_nuevos_conservan_alto_contraste(self):
        # Alto contraste se resuelve en la autoridad global de tokens.
        self.assertIn(
            'html[data-app-theme="contrast"] {',
            self.design,
        )

        for expected in (
            "--app-background: #000000;",
            "--app-surface: #000000;",
            "--app-text: #ffffff;",
            "--app-border: #ffffff;",
            "--app-border-strong: #ffffff;",
            "--app-shadow-sm: none;",
            "--app-shadow-lg: none;",
        ):
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    self.design,
                )

        # Los componentes de Inicio consumen los tokens globales;
        # no necesitan una segunda paleta específica de contraste.
        self.assertIn(
            ".home-preview-shell {",
            self.design,
        )
        self.assertIn(
            ".home-feature-card {",
            self.design,
        )

        self.assertIn(
            "background: color-mix(in srgb, var(--app-surface) 94%, transparent);",
            self.design,
        )
        self.assertIn(
            "border: 1px solid var(--app-border);",
            self.design,
        )
        self.assertIn(
            "background: var(--app-surface);",
            self.design,
        )

        # Solo las diferencias que realmente necesitan tratamiento
        # especializado conservan una regla explícita.
        self.assertIn(
            'html[data-app-theme="contrast"] .home-preview-bars span',
            self.design,
        )
        self.assertIn(
            "border-width: 2px;",
            self.design,
        )

    def test_remate_portada_reduce_titulo_y_centra_pasos(self):
        self.assertIn("font-size: clamp(2.75rem, 4.7vw, 4.55rem);", self.design)
        self.assertIn("line-height: 1.055;", self.design)
        self.assertIn(".home-process-step {", self.design)
        self.assertIn("align-items: center;", self.design)
        self.assertIn("text-align: center;", self.design)

    def test_remate_disclaimer_continua_superficie_del_proceso(self):
        self.assertIn(".home-disclaimer-section {", self.design)
        self.assertIn("background: var(--app-surface);", self.design)
        self.assertIn("padding-top: 0.4rem;", self.design)

    def test_footer_final_centrado_con_version_y_fuentes(self):
        self.assertIn(
            'class="footer-identity"',
            self.base,
        )

        self.assertIn(
            'class="footer-version"',
            self.base,
        )

        self.assertIn(
            "v{{ app_version }}",
            self.base,
        )

        self.assertIn(
            'class="footer-bottom"',
            self.base,
        )

        self.assertIn(
            'href="/metodologia"',
            self.base,
        )

        self.assertIn(
            "Fuentes oficiales",
            self.base,
        )

        self.assertIn(
            "align-items: center;",
            self.design,
        )

        self.assertIn(
            "text-align: center;",
            self.design,
        )



if __name__ == "__main__":
    unittest.main()
