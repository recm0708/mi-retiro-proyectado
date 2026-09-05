"""Regresiones de UX.4.1 para semántica y ayudas contextuales."""

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


ROOT = Path(__file__).resolve().parents[1]


class TestAccesibilidadUX4(unittest.TestCase):
    """Protege la primera capa de accesibilidad avanzada de UX.4."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(app)
        cls.js = (ROOT / "app/static/js/accessibility.js").read_text(encoding="utf-8")
        cls.css = (ROOT / "app/static/css/accessibility.css").read_text(encoding="utf-8")

    def test_base_carga_recursos_globales_de_accesibilidad(self):
        respuesta = self.cliente.get("/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("/static/css/accessibility.css", respuesta.text)
        self.assertIn("/static/js/accessibility.js", respuesta.text)

    def test_base_define_landmark_estado_y_ayuda_de_tema(self):
        respuesta = self.cliente.get("/metodologia")

        self.assertIn('aria-label="Navegación principal"', respuesta.text)
        self.assertIn('id="a11y-global-status"', respuesta.text)
        self.assertIn('aria-live="polite"', respuesta.text)
        self.assertIn('aria-describedby="ayuda-selector-tema"', respuesta.text)

    def test_ayudas_contextuales_cubren_campos_ambiguos(self):
        for identificador in (
            "sistema",
            "cuotas_totales",
            "cuotas_esperadas_cierre_anio",
            "modo_historial",
            "monto_salario",
            "modalidad_proyeccion",
            "fecha_corte_retiro",
            "ultimo_mes_cuotas",
        ):
            self.assertIn(f"{identificador}:", self.js)

        self.assertIn("context-help-trigger", self.js)
        self.assertIn('aria-expanded', self.js)
        self.assertIn('aria-controls', self.js)
        self.assertIn('role", "tooltip"', self.js)
        self.assertIn('"mouseenter"', self.js)
        self.assertIn('"focus"', self.js)

    def test_validacion_marca_campos_invalidos_y_mueve_foco(self):
        self.assertIn('addEventListener("invalid"', self.js)
        self.assertIn('aria-invalid', self.js)
        self.assertIn('control.focus', self.js)
        self.assertIn('Revisa el campo', self.js)

    def test_wizard_recibe_regiones_y_relacion_de_controles(self):
        self.assertIn('role", "navigation"', self.js)
        self.assertIn('aria-label", "Progreso de la simulación"', self.js)
        self.assertIn('role", "region"', self.js)
        self.assertIn('aria-labelledby', self.js)
        self.assertIn('aria-controls', self.js)
        self.assertIn('aria-hidden', self.js)

    def test_tablas_dinamicas_reciben_caption_y_foco_si_desbordan(self):
        self.assertIn("CAPTIONS_TABLAS", self.js)
        self.assertIn('caption.className = "visually-hidden"', self.js)
        self.assertIn("scrollWidth > contenedor.clientWidth", self.js)
        self.assertIn('table-scroll-focus', self.js)

    def test_css_protege_ayudas_contraste_y_estado_invalido(self):
        self.assertIn(
            ".context-help-trigger",
            self.css,
        )
        self.assertIn(
            ".context-help-panel",
            self.css,
        )
        self.assertIn(
            "min-height: 1.8rem",
            self.css,
        )
        self.assertIn(
            "border-radius: var(--app-radius-pill);",
            self.css,
        )
        self.assertIn(
            ".context-help-icon",
            self.css,
        )
        self.assertIn(
            "cursor: help",
            self.css,
        )
        self.assertIn(
            '[aria-invalid="true"]',
            self.css,
        )
        self.assertIn(
            "prefers-contrast: more",
            self.css,
        )
        self.assertIn(
            'data-app-theme="contrast"',
            self.css,
        )



if __name__ == "__main__":
    unittest.main()
