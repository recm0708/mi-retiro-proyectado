"""Regresiones de UX.4.2 para estados activos y selección perceptible."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestEstadosVisualesUX42(unittest.TestCase):
    """Protege los dos ajustes visuales detectados al cerrar UX.4.1."""

    @classmethod
    def setUpClass(cls):
        cls.estilos = (ROOT / "app/static/css/style.css").read_text(
            encoding="utf-8",
        )

    def test_paso_activo_usa_numero_blanco_en_tema_claro(self):
        self.assertIn(
            'html[data-bs-theme="light"] .wizard-step.active span',
            self.estilos,
        )
        self.assertIn("color: #ffffff;", self.estilos)

    def test_fila_retiro_seleccionada_usa_tokens_especificos_por_tema(self):
        for token in (
            "--app-retirement-selected-bg",
            "--app-retirement-selected-border",
            "--app-retirement-selected-text",
            "--app-retirement-selected-badge-bg",
            "--app-retirement-selected-radio-ring",
        ):
            self.assertIn(token, self.estilos)

        self.assertIn('html[data-bs-theme="dark"]', self.estilos)
        self.assertIn('html[data-app-theme="contrast"]', self.estilos)

    def test_fila_seleccionada_refuerza_fondo_contorno_radio_y_badge(self):
        self.assertIn(".retirement-row-selected > td", self.estilos)
        self.assertIn("inset 4px 0 0", self.estilos)
        self.assertIn(
            ".retirement-row-selected .retirement-scenario-radio",
            self.estilos,
        )
        self.assertIn(
            ".retirement-row-selected .retirement-status-future",
            self.estilos,
        )

    def test_fila_retiro_muestra_foco_y_soporta_colores_forzados(self):
        self.assertIn(
            ".retirement-row-selectable:focus-within > td",
            self.estilos,
        )
        self.assertIn("@media (forced-colors: active)", self.estilos)
        self.assertIn("background-color: Highlight !important;", self.estilos)


if __name__ == "__main__":
    unittest.main()
