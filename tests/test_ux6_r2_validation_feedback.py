"""Regresiones UX.6 R2 para feedback visual final de validacion."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestUX6R2ValidationFeedback(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.design = (
            ROOT / "app/static/css/design-system.css"
        ).read_text(encoding="utf-8")
        cls.a11y = (
            ROOT / "app/static/css/accessibility.css"
        ).read_text(encoding="utf-8")
        cls.dev_css = (
            ROOT / "app/static/css/developer-portal.css"
        ).read_text(encoding="utf-8")
        cls.forms_js = (
            ROOT / "app/static/js/developer_forms.js"
        ).read_text(encoding="utf-8")
        cls.users = (
            ROOT / "app/templates/developer/dev_users.html"
        ).read_text(encoding="utf-8")

    def test_tokens_de_validacion_pertenecen_al_design_system(self):
        for token in (
            "--app-validation-border",
            "--app-validation-text",
            "--app-validation-ring",
        ):
            with self.subTest(token=token):
                self.assertIn(token, self.design)

    def test_feedback_global_usa_tokens_semanticos(self):
        self.assertIn(
            '.form-control[aria-invalid="true"]',
            self.a11y,
        )
        self.assertIn(
            "var(--app-validation-border)",
            self.a11y,
        )
        self.assertIn(
            "var(--app-validation-text)",
            self.a11y,
        )

    def test_password_invalido_marca_input_y_ojo_completos(self):
        self.assertIn(
            '.dev-secret-group:has(> .form-control[aria-invalid="true"])',
            self.dev_css,
        )
        self.assertIn(
            "> .dev-password-toggle",
            self.dev_css,
        )
        self.assertIn(
            "outline: 2px solid var(--app-validation-border)",
            self.dev_css,
        )

    def test_foco_final_busca_primer_control_invalido(self):
        self.assertIn(
            "function enfocarPrimerInvalido()",
            self.forms_js,
        )
        self.assertIn(
            "control.scrollIntoView({",
            self.forms_js,
        )
        self.assertIn(
            "control.focus({",
            self.forms_js,
        )
        self.assertIn(
            "MutationObserver",
            self.forms_js,
        )

    def test_usuarios_no_duplica_asterisco_obligatorio(self):
        self.assertNotIn(
            '<span aria-hidden="true">*</span>',
            self.users,
        )
        self.assertIn(
            'class="required-marker"',
            self.users,
        )


if __name__ == "__main__":
    unittest.main()
