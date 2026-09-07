"""Regresiones del cierre de términos públicos de la aplicación principal."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def texto_visible_normalizado(contenido: str) -> str:
    """Normaliza HTML/Markdown y espacios sin alterar el contrato semántico."""
    texto = re.sub(r"<[^>]+>", " ", contenido)
    texto = texto.replace("**", "")
    return " ".join(texto.split())


class TestPublicTermsFinal(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.modal = (
            ROOT / "app/templates/partials/privacy_consent.html"
        ).read_text(encoding="utf-8")
        cls.policy = (
            ROOT / "docs/security/privacy-policy.md"
        ).read_text(encoding="utf-8")
        cls.terms = (
            ROOT / "docs/security/terms-and-privacy.md"
        ).read_text(encoding="utf-8")
        cls.privacy_js = (
            ROOT / "app/static/js/privacy.js"
        ).read_text(encoding="utf-8")

    def test_modal_explica_manual_asistida_y_fuentes_documentales(self):
        visible = texto_visible_normalizado(self.modal)
        for esperado in (
            "modalidad Manual",
            "modalidad Asistida",
            "Mi Retiro Seguro",
            "Ficha Digital",
            "confirmes expresamente la importación",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, visible)

    def test_modo_asistido_no_toma_decisiones_personales(self):
        self.assertIn(
            "no selecciona decisiones personales por ti",
            texto_visible_normalizado(self.modal),
        )
        self.assertIn(
            "no toma decisiones personales por el Asegurado(a)",
            texto_visible_normalizado(self.policy),
        )
        self.assertIn(
            "no decide por el Asegurado(a)",
            texto_visible_normalizado(self.terms),
        )

    def test_cambio_a_manual_documenta_retiro_de_datos_documentales(self):
        for contenido in (
            self.modal,
            self.policy,
            self.terms,
        ):
            visible = texto_visible_normalizado(contenido)
            with self.subTest():
                self.assertIn(
                    "datos que proceden de documentos",
                    visible,
                )
                self.assertIn(
                    "datos personales introducidos manualmente",
                    visible,
                )

    def test_documentos_originales_no_se_guardan(self):
        for contenido in (
            self.modal,
            self.policy,
            self.terms,
        ):
            visible = texto_visible_normalizado(contenido)
            with self.subTest():
                self.assertIn(
                    "archivo original no se guarda",
                    visible,
                )

    def test_terminos_publicos_siguen_sin_contratos_developer(self):
        for contenido in (
            self.modal,
            self.policy,
            self.terms,
        ):
            with self.subTest():
                for prohibido in (
                    "mrp_admin_session",
                    "Portal Developer",
                    "Developer Diagnostics",
                ):
                    self.assertNotIn(
                        prohibido,
                        contenido,
                    )

    def test_version_material_permanece_estable(self):
        self.assertIn(
            'VERSION_PRIVACIDAD = "2026-08-16.1"',
            self.privacy_js,
        )
        self.assertIn(
            "`2026-08-16.1`",
            self.policy,
        )
        self.assertIn(
            "`2026-08-16.1`",
            self.terms,
        )


if __name__ == "__main__":
    unittest.main()
