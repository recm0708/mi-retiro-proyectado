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
BOOT_JS = ROOT / "app/static/js/shell_state_boot.js"
SHELL_UI_JS = ROOT / "app/static/js/shell_ui.js"

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

    def test_estado_sidebar_se_aplica_antes_del_primer_pintado(self):
        boot = BOOT_JS.read_text(
            encoding="utf-8"
        )

        base = BASE.read_text(
            encoding="utf-8"
        )

        developer = DEV_BASE.read_text(
            encoding="utf-8"
        )

        developer_css = DEV_CSS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "miRetiroProyectado.shell.sidebar",
            boot,
        )

        self.assertIn(
            "document.documentElement.classList.add",
            boot,
        )

        self.assertLess(
            base.index("shell_state_boot.js"),
            base.index("bootstrap@5.3.8/dist/css/bootstrap.min.css"),
        )

        self.assertLess(
            developer.index("shell_state_boot.js"),
            developer.index("bootstrap@5.3.8/dist/css/bootstrap.min.css"),
        )

        self.assertNotIn(
            "body.dev-sidebar-collapsed",
            developer_css,
        )


    def test_shell_app_y_developer_comparten_interaccion_visual(self):
        base = BASE.read_text(
            encoding="utf-8"
        )

        developer = DEV_BASE.read_text(
            encoding="utf-8"
        )

        design = DESIGN.read_text(
            encoding="utf-8"
        )

        style = STYLE.read_text(
            encoding="utf-8"
        )

        developer_css = DEV_CSS.read_text(
            encoding="utf-8"
        )

        shell_ui = SHELL_UI_JS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "shell-menu-icon",
            base,
        )

        self.assertIn(
            "shell-menu-icon",
            developer,
        )

        self.assertIn(
            "shell_ui.js",
            base,
        )

        self.assertIn(
            "shell_ui.js",
            developer,
        )

        self.assertIn(
            "shell-nav-icon-selected",
            design,
        )

        self.assertIn(
            "shell-sidebar-tooltip",
            design,
        )

        self.assertIn(
            "data-sidebar-label",
            shell_ui,
        )

        self.assertIn(
            "prefers-reduced-motion",
            design,
        )

        self.assertNotIn(
            "inset 3px 0 0",
            style,
        )

        self.assertNotIn(
            ".dev-sidebar-nav a.active::before",
            developer_css,
        )

        self.assertNotIn(
            "dev-nav-icon-selected",
            developer_css,
        )


    def test_sidebar_colapsado_publica_etiquetas_contextuales(self):
        base = BASE.read_text(
            encoding="utf-8"
        )

        developer = DEV_BASE.read_text(
            encoding="utf-8"
        )

        for etiqueta in (
            "Inicio",
            "Simular",
            "Escenarios",
            "Cómo se calcula",
            "Fuentes",
        ):
            with self.subTest(
                app=etiqueta
            ):
                self.assertIn(
                    f'data-sidebar-label="{etiqueta}"',
                    base,
                )

        for etiqueta in (
            "Resumen",
            "Diagnóstico",
            "Eventos",
            "Archivos",
            "Mantenimiento",
            "Privacidad",
        ):
            with self.subTest(
                developer=etiqueta
            ):
                self.assertIn(
                    f'data-sidebar-label="{etiqueta}"',
                    developer,
                )


    def test_developer_reutiliza_identidad_visual_de_la_app(self):
        developer = DEV_BASE.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'class="dev-brand app-brand"',
            developer,
        )

        self.assertIn(
            'class="dev-brand-mark app-brand-mark"',
            developer,
        )

        self.assertIn(
            'class="app-brand-mark-image"',
            developer,
        )

        self.assertIn(
            'class="dev-brand-copy app-brand-copy"',
            developer,
        )


    def test_rail_developer_no_conserva_offset_colapsado_exclusivo(self):
        developer_css = DEV_CSS.read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            "min-height: 58px;",
            developer_css,
        )

        self.assertNotIn(
            "padding: .3rem .6rem;",
            developer_css,
        )

        self.assertIn(
            "padding-inline: var(--app-space-2);",
            developer_css,
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
            "Planificación previsional",
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
