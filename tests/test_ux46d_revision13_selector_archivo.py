"""Regresiones UX.4.6d R13 para selector de archivo estable."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision13SelectorArchivo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.design = (ROOT / "app/static/css/design-system.css").read_text(encoding="utf-8")

    def test_hover_del_input_no_puede_restaurar_paleta_bootstrap(self):
        selector = (
            'input[type="file"].form-control:not(:disabled):not([readonly]):hover::file-selector-button'
        )
        self.assertIn(selector, self.design)
        self.assertIn("background: var(--app-file-button-bg) !important", self.design)
        self.assertIn("color: var(--app-file-button-color) !important", self.design)
        self.assertIn("border-color: var(--app-file-button-border) !important", self.design)

    def test_focus_conserva_el_mismo_contrato_visual(self):
        self.assertIn(
            'input[type="file"].form-control:not(:disabled):not([readonly]):focus::file-selector-button',
            self.design,
        )
        self.assertIn(
            'input[type="file"].form-control:not(:disabled):not([readonly]):focus-visible::file-selector-button',
            self.design,
        )

    def test_prefijo_webkit_tambien_esta_protegido(self):
        self.assertIn("::-webkit-file-upload-button", self.design)
        self.assertIn(":hover::-webkit-file-upload-button", self.design)


if __name__ == "__main__":
    unittest.main()
