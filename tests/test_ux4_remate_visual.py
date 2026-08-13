"""Regresiones del remate visual e interactivo de UX.4.1."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestRemateUX41(unittest.TestCase):
    """Protege los ajustes pequeños validados manualmente en PC/laptop."""

    @classmethod
    def setUpClass(cls):
        cls.simulacion = (ROOT / "app/templates/simulacion.html").read_text(
            encoding="utf-8",
        )
        cls.historial = (
            ROOT / "app/templates/partials/historial_salarial.html"
        ).read_text(encoding="utf-8")
        cls.resultados = (
            ROOT / "app/templates/partials/resultados.html"
        ).read_text(encoding="utf-8")
        cls.retiro_js = (ROOT / "app/static/js/retiro.js").read_text(
            encoding="utf-8",
        )
        cls.estilos = (ROOT / "app/static/css/style.css").read_text(
            encoding="utf-8",
        )

    def test_sucgs_usa_nombre_breve_en_selector_del_paso_1(self):
        self.assertIn(
            "SUCGS — Capitalización con Garantía Solidaria",
            self.simulacion,
        )
        self.assertNotIn(
            "SUCGS — Sistema Único de Capitalización con Garantía Solidaria",
            self.simulacion,
        )

    def test_accion_completar_cuotas_tiene_estilo_semantico_propio(self):
        self.assertIn("history-fill-action", self.historial)
        self.assertIn(".history-fill-action", self.estilos)
        self.assertIn("--app-warning-bg", self.estilos)
        self.assertIn("--app-warning-border", self.estilos)

    def test_fila_completa_puede_seleccionar_escenario_futuro(self):
        self.assertIn("retirement-row-selectable", self.retiro_js)
        self.assertIn('fila.addEventListener(\n      "click"', self.retiro_js)
        self.assertIn("selector.checked = true", self.retiro_js)
        self.assertIn(".retirement-row-selectable", self.estilos)

    def test_boton_sebd_se_alinea_con_selector_salarial(self):
        self.assertIn("align-items-start", self.resultados)
        self.assertIn("results-sebd-action-col", self.resultados)
        self.assertIn(".results-sebd-action-col", self.estilos)
        self.assertIn("padding-top: 2rem", self.estilos)

    def test_ayuda_contextual_es_hover_focus_y_no_solo_click(self):
        js = (ROOT / "app/static/js/accesibilidad.js").read_text(
            encoding="utf-8",
        )
        css = (ROOT / "app/static/css/accesibilidad.css").read_text(
            encoding="utf-8",
        )

        self.assertIn('"mouseenter"', js)
        self.assertIn('"mouseleave"', js)
        self.assertIn('"focus"', js)
        self.assertIn('role", "tooltip"', js)
        self.assertIn("min-height: 1.8rem", css)
        self.assertIn("border-radius: 999px", css)
        self.assertIn(".context-help-icon", css)
        self.assertIn("position: absolute", css)


if __name__ == "__main__":
    unittest.main()
