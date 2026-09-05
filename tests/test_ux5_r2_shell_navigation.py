"""Regresiones UX.5 R2 del shell y navegación."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]

BASE = ROOT / "app/templates/base.html"
DEV_BASE = ROOT / "app/templates/dev_base.html"

STYLE = ROOT / "app/static/css/style.css"
DESIGN = ROOT / "app/static/css/design-system.css"
DEV_CSS = ROOT / "app/static/css/developer-portal.css"

APP_SHELL_JS = ROOT / "app/static/js/app_shell.js"
DEV_JS = ROOT / "app/static/js/developer_portal.js"

HOME = ROOT / "app/templates/index.html"
DEV_HOME = ROOT / "app/templates/dev_dashboard.html"


class TestUX5R2ShellNavigation(unittest.TestCase):

    def test_app_usa_sidebar_y_no_navbar_legacy(self):
        base = BASE.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'id="app-sidebar"',
            base,
        )
        self.assertIn(
            "data-app-sidebar-toggle",
            base,
        )
        self.assertIn(
            "data-app-sidebar-overlay",
            base,
        )

        for legacy in (
            "navbarPrincipal",
            "app-navbar",
            "app-nav-links",
            "navbar-toggler",
        ):
            with self.subTest(
                legacy=legacy
            ):
                self.assertNotIn(
                    legacy,
                    base,
                )


    def test_sidebar_app_persiste_preferencia_y_es_responsive(self):
        script = APP_SHELL_JS.read_text(
            encoding="utf-8"
        )

        style = STYLE.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "miRetiroProyectado.shell.sidebar",
            script,
        )

        self.assertIn(
            "window.localStorage.getItem",
            script,
        )

        self.assertIn(
            "window.localStorage.setItem",
            script,
        )

        self.assertIn(
            "(max-width: 991.98px)",
            script,
        )

        self.assertIn(
            "preferencia === \"collapsed\"",
            script,
        )

        self.assertIn(
            "transform: translateX(-105%);",
            style,
        )

        self.assertIn(
            ".app-sidebar-open .app-sidebar",
            style,
        )

    def test_developer_comparte_persistencia_visual_del_sidebar(self):
        base = DEV_BASE.read_text(
            encoding="utf-8"
        )

        script = DEV_JS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "miRetiroProyectado.shell.sidebar",
            script,
        )

        self.assertIn(
            "window.localStorage.getItem",
            script,
        )

        self.assertIn(
            "window.localStorage.setItem",
            script,
        )

        self.assertNotIn(
            "sidebar') == 'compact",
            base,
        )

        self.assertNotIn(
            'const PARAMETRO = "sidebar";',
            script,
        )

    def test_sidebars_no_repiten_version(self):
        base = BASE.read_text(
            encoding="utf-8"
        )

        developer = DEV_BASE.read_text(
            encoding="utf-8"
        )

        style = STYLE.read_text(
            encoding="utf-8"
        )

        developer_css = DEV_CSS.read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            "app-sidebar-meta",
            base,
        )
        self.assertNotIn(
            "dev-sidebar-meta",
            developer,
        )
        self.assertNotIn(
            ".app-sidebar-meta",
            style,
        )
        self.assertNotIn(
            ".dev-sidebar-meta",
            developer_css,
        )


    def test_developer_consume_tokens_app_directos(self):
        css = DEV_CSS.read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            "--dev-",
            css,
        )

        for token in (
            "var(--app-primary)",
            "var(--app-surface)",
            "var(--app-border)",
            "var(--app-text)",
            "var(--app-shell-topbar-height)",
            "var(--app-shell-sidebar-width)",
        ):
            with self.subTest(
                token=token
            ):
                self.assertIn(
                    token,
                    css,
                )


    def test_metricas_del_shell_son_universales(self):
        design = DESIGN.read_text(
            encoding="utf-8"
        )

        for token in (
            "--app-shell-topbar-height",
            "--app-shell-sidebar-width",
            "--app-shell-sidebar-collapsed-width",
            "--app-control-height",
            "--app-duration-base",
            "--app-ease-standard",
        ):
            with self.subTest(
                token=token
            ):
                self.assertEqual(
                    1,
                    design.count(
                        token + ":"
                    ),
                )


    def test_tema_conserva_cuatro_preferencias(self):
        for template in (
            BASE,
            DEV_BASE,
        ):
            text = template.read_text(
                encoding="utf-8"
            )

            for preference in (
                "system",
                "light",
                "dark",
                "contrast",
            ):
                with self.subTest(
                    template=template.name,
                    preference=preference,
                ):
                    self.assertIn(
                        f'data-theme-choice="{preference}"',
                        text,
                    )


    def test_inicio_app_y_developer_son_portadas_profesionales(self):
        home = HOME.read_text(
            encoding="utf-8"
        )

        developer = DEV_HOME.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "home-hero-modern",
            home,
        )

        self.assertIn(
            "Planifica tu retiro con más claridad",
            home,
        )

        self.assertIn(
            "dev-home-hero",
            developer,
        )

        self.assertIn(
            "Centro de control del entorno local",
            developer,
        )


if __name__ == "__main__":
    unittest.main()
