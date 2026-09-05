"""Regresiones de UX.5 R1 para la autoridad del sistema visual."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CSS_DIR = ROOT / "app" / "static" / "css"

DESIGN_SYSTEM = CSS_DIR / "design-system.css"
STYLE = CSS_DIR / "style.css"

TOKEN_DECL_RE = re.compile(
    r"(?m)^[ \t]*(--app-[A-Za-z0-9_-]+)\s*:"
)


def rule_body(
    css: str,
    selector: str,
) -> str:
    """Devuelve el cuerpo de una regla CSS de primer nivel."""

    pattern = re.compile(
        rf"(?ms)^{re.escape(selector)}\s*\{{"
        rf"(?P<body>.*?)"
        rf"^\}}"
    )

    match = pattern.search(css)

    if match is None:
        raise AssertionError(
            f"No se encontró la regla CSS: {selector}"
        )

    return match.group("body")


def declaration_count(
    css: str,
    token: str,
) -> int:
    """Cuenta declaraciones exactas de un token."""

    pattern = re.compile(
        rf"(?m)^[ \t]*{re.escape(token)}\s*:"
    )

    return len(
        pattern.findall(css)
    )


class TestUX5R1DesignSystem(unittest.TestCase):
    """Protege la fuente visual canónica introducida en UX.5 R1."""

    @classmethod
    def setUpClass(cls):
        cls.css_files = sorted(
            CSS_DIR.glob("*.css")
        )

        cls.contents = {
            path.name: path.read_text(
                encoding="utf-8"
            )
            for path in cls.css_files
        }

        cls.design = cls.contents[
            DESIGN_SYSTEM.name
        ]

        cls.style = cls.contents[
            STYLE.name
        ]

        cls.all_css = "\n".join(
            cls.contents.values()
        )

    def test_design_system_es_unica_fuente_de_tokens_app(self):
        owners = {}

        for name, text in self.contents.items():
            tokens = TOKEN_DECL_RE.findall(
                text
            )

            if tokens:
                owners[name] = tokens

        self.assertEqual(
            {DESIGN_SYSTEM.name},
            set(owners),
            owners,
        )

        self.assertGreaterEqual(
            len(owners[DESIGN_SYSTEM.name]),
            60,
        )

    def test_tipografia_global_tiene_un_solo_propietario(self):
        self.assertEqual(
            1,
            declaration_count(
                self.design,
                "--app-font-family",
            ),
        )

        design_body = rule_body(
            self.design,
            "body",
        )

        style_body = rule_body(
            self.style,
            "body",
        )

        self.assertIn(
            "font-family: var(--app-font-family);",
            design_body,
        )

        self.assertNotIn(
            "font-family:",
            style_body,
        )

    def test_tokens_generales_migrados_siguen_activos(self):
        tokens = (
            "--app-font-base",
            "--app-font-important",
            "--app-radius",
        )

        for token in tokens:
            with self.subTest(token=token):
                self.assertEqual(
                    1,
                    declaration_count(
                        self.design,
                        token,
                    ),
                )

                self.assertIn(
                    f"var({token})",
                    self.all_css,
                )

    def test_seleccion_retiro_tiene_tokens_por_tema(self):
        tokens = (
            "--app-retirement-selected-bg",
            "--app-retirement-selected-border",
            "--app-retirement-selected-text",
            "--app-retirement-selected-badge-bg",
            "--app-retirement-selected-badge-text",
            "--app-retirement-selected-radio-ring",
        )

        for token in tokens:
            with self.subTest(token=token):
                self.assertEqual(
                    3,
                    declaration_count(
                        self.design,
                        token,
                    ),
                )

                self.assertIn(
                    f"var({token})",
                    self.all_css,
                )

    def test_tres_mapeos_de_tema_permanecen_canonicos(self):
        selectors = (
            ":root",
            'html[data-bs-theme="dark"]',
            'html[data-app-theme="contrast"]',
        )

        required = (
            "--app-primary",
            "--app-background",
            "--app-surface",
            "--app-text",
            "--app-border",
            "--app-focus",
        )

        for selector in selectors:
            body = rule_body(
                self.design,
                selector,
            )

            for token in required:
                with self.subTest(
                    selector=selector,
                    token=token,
                ):
                    self.assertRegex(
                        body,
                        rf"(?m)^[ \t]*"
                        rf"{re.escape(token)}\s*:",
                    )

    def test_selector_archivo_no_se_duplica_en_style(self):
        selector = (
            'input[type="file"].form-control'
            '::file-selector-button'
        )

        self.assertNotIn(
            selector,
            self.style,
        )

        self.assertIn(
            selector,
            self.design,
        )

        for token in (
            "--app-file-button-color",
            "--app-file-button-bg",
            "--app-file-button-hover-bg",
            "--app-file-button-border",
        ):
            with self.subTest(token=token):
                self.assertIn(
                    token,
                    self.design,
                )


    def test_style_no_reintroduce_colores_literales_en_temas(self):
        rule_re = re.compile(
            r"(?ms)^"
            r"(?P<selectors>[^@{}][^{}]*?)"
            r"\{"
            r"(?P<body>.*?)"
            r"^\}"
        )

        raw_color_re = re.compile(
            r"#[0-9A-Fa-f]{3,8}\b"
            r"|rgba?\("
            r"|hsla?\("
        )

        violations = []

        for match in rule_re.finditer(
            self.style
        ):
            selectors = match.group(
                "selectors"
            ).strip()

            if (
                'html[data-bs-theme="dark"]'
                not in selectors
                and
                'html[data-app-theme="contrast"]'
                not in selectors
            ):
                continue

            if raw_color_re.search(
                match.group("body")
            ):
                violations.append(
                    selectors
                )

        self.assertEqual(
            [],
            violations,
            msg=(
                "style.css no puede contener colores "
                "literales dentro de overrides de tema."
            ),
        )

    def test_footer_comun_consumido_por_tokens_tematicos(self):
        for token in (
            "--app-footer-link",
            "--app-footer-link-hover",
        ):
            with self.subTest(token=token):
                self.assertEqual(
                    3,
                    declaration_count(
                        self.design,
                        token,
                    ),
                )

        self.assertIn(
            "color: var(--app-footer-link);",
            self.design,
        )

        self.assertIn(
            "color: var(--app-footer-link-hover);",
            self.design,
        )

        self.assertNotIn(
            'html[data-app-theme="contrast"] .footer-link',
            self.style,
        )

    def test_estados_compactos_contraste_pertenecen_al_sistema(self):
        self.assertIn(
            'html[data-app-theme="contrast"] .history-status,',
            self.design,
        )

        self.assertIn(
            "border: 2px solid var(--app-border);",
            self.design,
        )

        self.assertNotIn(
            "border: 2px solid #000000;",
            self.style,
        )

    def test_puente_bootstrap_usa_colores_accesibles_del_sistema(self):
        for token in (
            "--app-accent-text",
            "--app-accent-text-rgb",
            "--app-accent-hover-rgb",
            "--app-button-primary-bg",
            "--app-button-primary-border",
            "--app-button-primary-text",
        ):
            with self.subTest(token=token):
                self.assertEqual(
                    3,
                    declaration_count(
                        self.design,
                        token,
                    ),
                )

        for bridge in (
            "--bs-primary-rgb: var(--app-accent-text-rgb);",
            "--bs-link-color-rgb: var(--app-accent-text-rgb);",
            "--bs-link-hover-color-rgb: var(--app-accent-hover-rgb);",
        ):
            with self.subTest(bridge=bridge):
                self.assertEqual(
                    3,
                    self.design.count(
                        bridge
                    ),
                )

        self.assertIn(
            "--bs-btn-bg: var(--app-button-primary-bg);",
            self.design,
        )
        self.assertIn(
            "--bs-btn-color: var(--app-button-primary-text);",
            self.design,
        )

        self.assertIn(
            ".btn-outline-danger {",
            self.design,
        )
        self.assertIn(
            "--bs-btn-color: var(--app-danger-text);",
            self.design,
        )
        self.assertIn(
            "--bs-btn-border-color: var(--app-danger-border);",
            self.design,
        )

if __name__ == "__main__":
    unittest.main()
