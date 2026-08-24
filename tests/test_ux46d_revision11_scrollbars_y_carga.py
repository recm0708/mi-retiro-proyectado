"""Regresiones UX.4.6d R11 para scrollbars internos y carga PDF simétrica."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision11ScrollbarsYCarga(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.design = (ROOT / "app/static/css/design-system.css").read_text(encoding="utf-8")
        cls.ficha = (ROOT / "app/templates/partials/ficha_digital_import.html").read_text(encoding="utf-8")
        cls.oficial = (ROOT / "app/templates/partials/official_data_import.html").read_text(encoding="utf-8")

    def test_scrollbar_tabular_elimina_flechas_nativas(self):
        self.assertIn(".app-table-shell::-webkit-scrollbar-button", self.design)
        self.assertIn("display: none", self.design)
        self.assertIn("width: 0", self.design)
        self.assertIn("height: 0", self.design)

    def test_scrollbar_tabular_reserva_margen_en_esquinas_redondeadas(self):
        self.assertIn(".app-table-shell::-webkit-scrollbar-track:vertical", self.design)
        self.assertIn("margin-block: 0.55rem", self.design)
        self.assertIn(".app-table-shell::-webkit-scrollbar-track:horizontal", self.design)
        self.assertIn("margin-inline: 0.55rem", self.design)
        self.assertIn(".app-table-shell::-webkit-scrollbar-corner", self.design)

    def test_scrollbar_tabular_adapta_colores_por_tema(self):
        self.assertIn('html[data-bs-theme="dark"] .app-table-shell', self.design)
        self.assertIn('html[data-app-theme="contrast"] .app-table-shell', self.design)
        self.assertIn("scrollbar-color: #ffffff #000000", self.design)

    def test_selector_y_accion_pdf_comparten_altura_exterior(self):
        self.assertIn(".official-import-upload-file .official-import-file-input,", self.design)
        self.assertIn(".official-import-upload-action .btn", self.design)
        self.assertIn("min-height: 3rem !important", self.design)
        self.assertIn("height: 3rem !important", self.design)
        self.assertIn("max-height: 3rem", self.design)

    def test_ambos_importadores_reutilizan_contrato_de_carga(self):
        for contenido in (self.ficha, self.oficial):
            self.assertIn("official-import-upload-grid", contenido)
            self.assertIn("official-import-file-input", contenido)
            self.assertIn("official-import-upload-action", contenido)
            self.assertIn("Analizar documento", contenido)


if __name__ == "__main__":
    unittest.main()
