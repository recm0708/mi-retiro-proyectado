"""Regresiones de pulido visual, responsive y accesibilidad transversal."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestInterfacePolishResponsive(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.design = (
            ROOT / "app/static/css/design-system.css"
        ).read_text(encoding="utf-8")
        cls.a11y = (
            ROOT / "app/static/css/accessibility.css"
        ).read_text(encoding="utf-8")
        cls.motion = (
            ROOT / "app/static/css/motion.css"
        ).read_text(encoding="utf-8")

    def test_design_system_es_propietario_del_pulido_compartido(self):
        self.assertIn(
            "Componentes compartidos de interfaz",
            self.design,
        )
        for selector in (
            ".card,",
            ".dropdown-menu",
            ".form-control,",
            ".form-select",
            ".table",
        ):
            with self.subTest(selector=selector):
                self.assertIn(selector, self.design)

    def test_controles_respetan_altura_tactil(self):
        self.assertIn(
            "min-block-size: 44px",
            self.a11y,
        )
        self.assertIn(
            ".app-menu-button",
            self.a11y,
        )
        self.assertIn(
            ".dev-menu-button",
            self.a11y,
        )

    def test_responsive_cubre_app_y_developer(self):
        self.assertIn(
            "@media (max-width: 991.98px)",
            self.a11y,
        )
        self.assertIn(
            "@media (max-width: 575.98px)",
            self.a11y,
        )
        self.assertIn(
            ".app-topbar-inner",
            self.a11y,
        )
        self.assertIn(
            ".dev-topbar-inner",
            self.a11y,
        )

    def test_forced_colors_tiene_foco_y_bordes(self):
        self.assertIn(
            "@media (forced-colors: active)",
            self.a11y,
        )
        self.assertIn(
            "outline: 3px solid Highlight",
            self.a11y,
        )
        self.assertIn(
            "border: 1px solid CanvasText",
            self.a11y,
        )

    def test_tablas_desplazables_conservan_foco_visible(self):
        self.assertIn(
            ".table-responsive:focus-visible",
            self.a11y,
        )
        self.assertIn(
            ".history-table-wrapper:focus-visible",
            self.a11y,
        )
        self.assertIn(
            "overscroll-behavior-inline: contain",
            self.a11y,
        )

    def test_movimiento_reducido_sigue_siendo_global(self):
        self.assertIn(
            "@media (prefers-reduced-motion: reduce)",
            self.motion,
        )
        self.assertIn(
            "body *::before",
            self.motion,
        )
        self.assertIn(
            "transition-duration: 0.01ms !important",
            self.motion,
        )


if __name__ == "__main__":
    unittest.main()
