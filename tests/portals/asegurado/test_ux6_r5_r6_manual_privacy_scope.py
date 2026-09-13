"""Regresiones del acceso Manual y la frontera pública de privacidad."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]


class TestManualPrivacyScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.assisted = (
            ROOT / "app/templates/asegurado/partials/assisted_preparation.html"
        ).read_text(encoding="utf-8")
        cls.mode_js = (
            ROOT / "app/static/asegurado/js/simulation_mode.js"
        ).read_text(encoding="utf-8")
        cls.privacy_html = (
            ROOT / "app/templates/asegurado/partials/privacy_consent.html"
        ).read_text(encoding="utf-8")
        cls.methodology = (
            ROOT / "app/templates/asegurado/methodology.html"
        ).read_text(encoding="utf-8")
        cls.privacy_policy = (
            ROOT / "docs/security/privacy-policy.md"
        ).read_text(encoding="utf-8")
        cls.terms = (
            ROOT / "docs/security/terms-and-privacy.md"
        ).read_text(encoding="utf-8")

    def test_manual_es_acceso_directo_desde_preparacion_asistida(self):
        self.assertIn(
            'href="#simulation-wizard-shell"',
            self.assisted,
        )
        self.assertIn(
            'data-simulation-mode-choice="MANUAL"',
            self.assisted,
        )
        self.assertIn(
            "Cambiar a modalidad Manual y comenzar la captura de datos",
            self.assisted,
        )
        self.assertIn(
            '"[data-simulation-mode-choice]"',
            self.mode_js,
        )
        self.assertIn(
            "seleccionarModalidad(",
            self.mode_js,
        )
        self.assertIn(
            "enfocarPasoActual(",
            self.mode_js,
        )

    def test_modal_publico_cubre_importaciones_y_no_persistencia_pdf(self):
        self.assertIn(
            "PDF de Mi Retiro Seguro o Ficha Digital",
            self.privacy_html,
        )
        self.assertIn(
            "archivo original no se guarda",
            self.privacy_html,
        )
        self.assertIn(
            "Ningún dato detectado se aplica hasta que confirmes",
            self.privacy_html,
        )
        self.assertIn(
            "ruta local del archivo",
            self.privacy_html,
        )

    def test_privacidad_publica_no_mezcla_portal_developer(self):
        for contenido in (
            self.privacy_html,
            self.privacy_policy,
            self.terms,
        ):
            with self.subTest():
                self.assertNotIn(
                    "mrp_admin_session",
                    contenido,
                )
                self.assertNotIn(
                    "Portal Developer",
                    contenido,
                )
                self.assertNotIn(
                    "Developer Diagnostics",
                    contenido,
                )

    def test_ausencia_de_cookies_se_acota_a_aplicacion_principal(self):
        self.assertIn(
            "aplicación principal no utiliza cookies",
            self.privacy_html.lower(),
        )
        self.assertIn(
            "aplicación principal no utiliza cookies",
            self.methodology.lower(),
        )
        self.assertIn(
            "aplicación principal de simulación no implementa cookies",
            self.privacy_policy.lower(),
        )

    def test_version_material_no_cambia_por_clarificacion_no_material(self):
        self.assertIn(
            'VERSION_PRIVACIDAD = "2026-08-16.1"',
            (
                ROOT / "app/static/asegurado/js/privacy.js"
            ).read_text(encoding="utf-8"),
        )
        self.assertIn(
            "`2026-08-16.1`",
            self.privacy_policy,
        )


if __name__ == "__main__":
    unittest.main()
