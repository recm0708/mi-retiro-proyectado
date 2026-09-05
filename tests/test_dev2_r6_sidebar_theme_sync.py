"""DEV.2 R6 — Sidebar y sincronización temática del Portal Developer."""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestDev2R6SidebarThemeSync(unittest.TestCase):
    """Protege la separación de layout y la unidad temática."""

    def test_sidebar_contiene_todas_las_rutas_principales(self):
        base = (
            ROOT / "app/templates/dev_base.html"
        ).read_text(encoding="utf-8")

        self.assertIn(
            'id="dev-sidebar"',
            base,
        )

        self.assertIn(
            "data-dev-sidebar-toggle",
            base,
        )

        for ruta in (
            "/dev",
            "/dev/diagnostico",
            "/dev/eventos",
            "/dev/archivos",
            "/dev/mantenimiento",
            "/dev/privacidad",
        ):
            self.assertIn(
                f'href="{ruta}"',
                base,
            )

    def test_header_ya_no_contiene_navegacion_horizontal(self):
        base = (
            ROOT / "app/templates/dev_base.html"
        ).read_text(encoding="utf-8")

        self.assertNotIn(
            'class="dev-nav"',
            base,
        )

    def test_header_usa_identidad_compacta(self):
        base = (
            ROOT / "app/templates/dev_base.html"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "@{{ dev_usuario.usuario }}",
            base,
        )
        self.assertIn(
            "{{ dev_nombre_presentacion }}",
            base,
        )

    def test_developer_deriva_colores_del_sistema_global(self):
        css = (
            ROOT
            / "app/static/css/developer-portal.css"
        ).read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            "--dev-",
            css,
        )

        for token in (
            "var(--app-primary)",
            "var(--app-surface)",
            "var(--app-text)",
            "var(--app-border)",
            "var(--app-shell-sidebar-width)",
        ):
            with self.subTest(token=token):
                self.assertIn(
                    token,
                    css,
                )

    def test_developer_no_define_temas_paralelos(self):
        css = (
            ROOT
            / "app/static/css/developer-portal.css"
        ).read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            '[data-app-theme="contrast"]',
            css,
        )
        self.assertNotIn(
            'data-bs-theme="dark"',
            css,
        )
        self.assertNotIn(
            "#3b82f6",
            css.casefold(),
        )

    def test_sistema_global_contiene_estados_semanticos(self):
        css = (
            ROOT
            / "app/static/css/design-system.css"
        ).read_text(
            encoding="utf-8"
        )

        for token in (
            "--app-primary:",
            "--app-background:",
            "--app-surface:",
            "--app-text:",
            "--app-success-bg:",
            "--app-warning-bg:",
            "--app-danger-bg:",
        ):
            self.assertIn(
                token,
                css,
            )

    def test_theme_js_es_compartido(self):
        js = (
            ROOT / "app/static/js/theme.js"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'miRetiroProyectado.tema',
            js,
        )

        self.assertIn(
            '"system", "light", "dark", "contrast"',
            js,
        )

    def test_sidebar_persiste_solo_preferencia_visual(self):
        js = (
            ROOT
            / "app/static/js/developer_portal.js"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "miRetiroProyectado.shell.sidebar",
            js,
        )

        self.assertIn(
            "localStorage",
            js,
        )

        self.assertNotIn(
            "sessionStorage",
            js,
        )

        self.assertNotIn(
            "sidebar=compact",
            js,
        )

    def test_toggle_password_apunta_al_formulario_r6(self):
        js = (
            ROOT
            / "app/static/js/developer_portal.js"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'getElementById("dev-password")',
            js,
        )


if __name__ == "__main__":
    unittest.main()
