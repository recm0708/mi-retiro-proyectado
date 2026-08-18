"""GOV.1.8 — auditoría final y cierre del programa GOV.1."""

from pathlib import Path
import unittest

from app.core.config import APP_VERSION


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestGov18CierreGobierno(unittest.TestCase):
    def test_version_formal_cierre_es_0_0_24_beta(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.0.24-beta", version)
        self.assertEqual(version, APP_VERSION)

    def test_readme_declara_gov1_cerrado_y_ux46e_activo(self):
        texto = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("**Versión formal vigente:** `0.0.24-beta`", texto)
        self.assertIn("**Programa GOV.1:** cerrado", texto)
        self.assertIn(
            "**Bloque activo:** UX.4.6e — Paso 4 · Proyección salarial/laboral",
            texto,
        )
        self.assertIn("**GOV.1.8:**", texto)
        self.assertIn("0.1.0-beta.1", texto)

    def test_roadmap_cierra_gov18_y_descongela_ux46e(self):
        texto = (DOCS / "ROADMAP.md").read_text(encoding="utf-8")
        for bloque in range(1, 9):
            self.assertIn(f"**GOV.1.{bloque}", texto)
        self.assertIn(
            "- [x] **GOV.1.8 — Auditoría final y cierre pre-beta de gobierno**",
            texto,
        )
        self.assertIn("UX.4.6e queda descongelada", texto)
        self.assertIn("**Bloque activo:** UX.4.6e", texto)

    def test_releases_documenta_0_0_24_y_tag_firmado(self):
        texto = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("### `0.0.24-beta` — 2026-08-18", texto)
        self.assertIn("v0.0.24-beta", texto)
        self.assertIn("anotado y firmado", texto)
        self.assertIn("540 pruebas", texto)
        self.assertIn("no es una beta pública", texto)

    def test_changelog_mueve_cierre_a_release_0_0_24(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [0.0.24-beta] — 2026-08-18", texto)
        self.assertIn("GOV.1.8 — Auditoría final", texto)
        self.assertIn("saltos de línea reales", texto)
        self.assertIn("v0.0.24-beta", texto)

    def test_cierre_gov1_declara_evidencia_y_gates_restantes(self):
        texto = (DOCS / "CIERRE_GOV1.md").read_text(encoding="utf-8")
        for esperado in (
            "530 pruebas",
            "540 pruebas",
            "Python 3.13",
            "Python 3.14",
            "Auditoría de gobernanza",
            "v0.0.24-beta",
            "revisión jurídica externa",
            "UX.4.6e",
            "0.1.0-beta.1",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_auditoria_github_declara_tres_checks_y_evidencia(self):
        texto = (DOCS / "AUDITORIA_GITHUB.md").read_text(encoding="utf-8")
        for esperado in (
            "`Python 3.13`",
            "`Python 3.14`",
            "`Auditoría de gobernanza`",
            "PR #15",
            "PR #16",
            "cero Pull Requests abiertos",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_security_soporta_version_actual(self):
        texto = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn(
            "| `0.0.24-beta` | Soportada durante el desarrollo interno vigente |",
            texto,
        )
        self.assertIn("`0.0.23-beta` y anteriores", texto)

    def test_regresiones_historicas_declaran_version_base(self):
        casos = (
            ("test_gov13_documentacion_r2.py", 'BASE_VERSION = "0.0.23-beta"'),
            ("test_gov13_documentacion_r3.py", 'self.version_base = "0.0.23-beta"'),
            ("test_gov13_documentacion_r4.py", 'self.version_base = "0.0.23-beta"'),
            ("test_gov15_modelo_amenazas.py", 'self.version_base = "0.0.23-beta"'),
            (
                "test_gov15_procedimientos_privacidad.py",
                'self.version_base = "0.0.23-beta"',
            ),
            (
                "test_gov15_cierre_seguridad_privacidad.py",
                'self.version_base = "0.0.23-beta"',
            ),
        )
        for nombre, esperado in casos:
            with self.subTest(nombre=nombre):
                texto = (ROOT / "tests" / nombre).read_text(encoding="utf-8")
                self.assertIn(esperado, texto)

    def test_documentos_cierre_limpios_y_licencia_sin_escapes(self):
        archivos = (
            ROOT / "README.md",
            ROOT / "CHANGELOG.md",
            ROOT / "RELEASES.md",
            ROOT / "SECURITY.md",
            DOCS / "ROADMAP.md",
            DOCS / "VALIDACION.md",
            DOCS / "INDICE.md",
            DOCS / "AUDITORIA_GITHUB.md",
            DOCS / "CIERRE_GOV1.md",
            ROOT / "LICENSE",
            ROOT / "THIRD_PARTY_NOTICES.md",
            DOCS / "LICENCIA_Y_DISTRIBUCION.md",
        )
        for path in archivos:
            texto = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertFalse(
                    any(ord(c) < 32 and c not in "\n\r\t" for c in texto)
                )
                self.assertFalse(
                    any(line.endswith((" ", "\t")) for line in texto.splitlines())
                )
        for path in (
            ROOT / "LICENSE",
            ROOT / "THIRD_PARTY_NOTICES.md",
            DOCS / "LICENCIA_Y_DISTRIBUCION.md",
        ):
            self.assertNotIn(r"\n", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
