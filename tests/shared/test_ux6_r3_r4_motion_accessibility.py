"""Regresiones del contrato transversal de movimiento y accesibilidad."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class TestMotionAccessibilityContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.motion = (
            ROOT / "app/static/shared/css/motion.css"
        ).read_text(encoding="utf-8")

        cls.interaction = (
            ROOT / "app/static/shared/js/interaction_ui.js"
        ).read_text(encoding="utf-8")

        cls.base = (
            ROOT / "app/templates/asegurado/base.html"
        ).read_text(encoding="utf-8")

        cls.dev_base = (
            ROOT / "app/templates/developer/dev_base.html"
        ).read_text(encoding="utf-8")

    def test_ambos_shells_cargan_movimiento_e_interaccion(self):
        for contenido in (
            self.base,
            self.dev_base,
        ):
            with self.subTest():
                self.assertIn(
                    "/shared/css/motion.css",
                    contenido,
                )
                self.assertIn(
                    "/shared/js/interaction_ui.js",
                    contenido,
                )

    def test_motion_consume_tokens_sin_crear_tokens_app(self):
        self.assertIn(
            "var(--app-duration-fast)",
            self.motion,
        )
        self.assertIn(
            "var(--app-duration-base)",
            self.motion,
        )
        self.assertIn(
            "var(--app-duration-slow)",
            self.motion,
        )
        self.assertIn(
            "var(--app-ease-standard)",
            self.motion,
        )
        self.assertNotRegex(
            self.motion,
            r"(?m)^\s*--app-[\w-]+\s*:",
        )

    def test_movimiento_reducido_es_transversal(self):
        self.assertIn(
            "@media (prefers-reduced-motion: reduce)",
            self.motion,
        )
        self.assertIn(
            "animation-duration: 0.01ms !important",
            self.motion,
        )
        self.assertIn(
            "transition-duration: 0.01ms !important",
            self.motion,
        )

    def test_app_y_developer_comparten_entrada(self):
        self.assertIn(
            ".app-main > section",
            self.motion,
        )
        self.assertIn(
            ".dev-main > section",
            self.motion,
        )
        self.assertIn(
            "@keyframes app-surface-enter",
            self.motion,
        )

    def test_fallback_no_depende_exclusivamente_de_has(self):
        self.assertIn(
            "is-invalid-group",
            self.motion,
        )
        self.assertIn(
            "is-invalid-group",
            self.interaction,
        )
        self.assertIn(
            "is-disabled",
            self.interaction,
        )
        self.assertIn(
            "MutationObserver",
            self.interaction,
        )

    def test_archivos_operativos_tienen_encabezado_canonico(self):
        self.assertTrue(
            self.interaction.startswith(
                '"use strict";\n\n/*',
            )
        )
        primeras = "\n".join(
            self.interaction.splitlines()[:12]
        )
        self.assertIn(
            "Mi Retiro Proyectado —",
            primeras,
        )
        self.assertIn(
            "Propósito:",
            primeras,
        )
        self.assertIn(
            "Alcance:",
            primeras,
        )


if __name__ == "__main__":
    unittest.main()
