"""UX.4.6e R9.1 — candidato local de cierre 0.0.25-beta."""

from pathlib import Path
import re
import unittest

from app.core.config import APP_VERSION


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestUx46eR91CandidatoCierre(unittest.TestCase):
    """Protege el candidato antes del PR, CI y tag formal."""

    def test_version_canonica_es_0_0_25_y_app_version_coincide(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.0.25-beta", version)
        self.assertEqual(version, APP_VERSION)

    def test_readme_declara_candidato_validado_y_proximo_bloque_sin_beta_publica(self):
        texto = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("**Versión candidata de cierre:** `0.0.25-beta`", texto)
        self.assertIn(
            "R9.1 validada localmente con 660 pruebas en `OK`",
            texto,
        )
        self.assertIn(
            "R9.2 queda pendiente de commits firmados, PR, CI, squash",
            texto,
        )
        self.assertIn("UX.4.6f — Paso 4 · Proyección salarial/laboral", texto)
        self.assertIn("0.1.0-beta.1", texto)
        indice = (DOCS / "INDICE.md").read_text(encoding="utf-8")
        self.assertIn(
            "**Versión de aplicación revisada:** `0.0.25-beta`",
            indice,
        )
        self.assertIn("UX.4.6e R9.1", indice)

    def test_security_soporta_nueva_linea_y_archiva_anterior(self):
        texto = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("| `0.0.25-beta` | Soportada", texto)
        self.assertIn("| `0.0.24-beta` y anteriores | Históricas", texto)

    def test_changelog_promueve_acumulado_a_0_0_25(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [0.0.25-beta] — 2026-08-19", texto)
        self.assertIn("UX.4.6e R9.1 — candidato local de cierre", texto)
        self.assertIn("ADR-167", texto)
        self.assertIn("## [0.0.24-beta] — 2026-08-18", texto)

    def test_roadmap_mantiene_r9_2_pendiente_y_paso4_sin_iniciar(self):
        texto = (DOCS / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("R9.1 — candidato local `0.0.25-beta`", texto)
        self.assertIn("[ ] R9.2 — commits firmados, PR, CI, squash", texto)
        self.assertIn("- [ ] **UX.4.6f — Paso 4", texto)

    def test_validacion_registra_gate_local_de_660_cumplido(self):
        texto = (DOCS / "VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("Gate R9.1 — candidato `0.0.25-beta`", texto)
        self.assertIn("**652 pruebas en `OK`**", texto)
        self.assertIn("**8 regresiones específicas**", texto)
        self.assertIn("R9.1 alcanzó **660 pruebas en `OK`**", texto)

    def test_regresiones_historicas_no_congelan_version_0_0_24(self):
        rutas = (
            ROOT / "tests/test_gov18_cierre_gobierno.py",
            ROOT / "tests/test_identidad_publica_github_pre_r8.py",
            ROOT / "tests/test_ux46e_estandar_runtime.py",
            ROOT / "tests/test_ux46e_r81_procedencia_editable.py",
            ROOT / "tests/test_ux46e_r8_cierre_funcional.py",
        )
        patron = re.compile(
            r"assertEqual\(\s*[\"']0\.0\.24-beta[\"']\s*,\s*"
            r"\(ROOT / [\"']VERSION[\"']\)",
            re.S,
        )
        for ruta in rutas:
            with self.subTest(ruta=ruta.name):
                self.assertIsNone(patron.search(ruta.read_text(encoding="utf-8")))

    def test_releases_registra_candidato_y_preserva_tag_0_0_24(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        self.assertIn("### `0.0.24-beta` — 2026-08-18", releases)
        self.assertIn("v0.0.24-beta", releases)
        self.assertIn(
            "### `0.0.25-beta` — candidato local 2026-08-19",
            releases,
        )
        self.assertIn(
            "todavía no existe un tag formal `v0.0.25-beta`",
            releases,
        )
        self.assertIn("los tags publicados vuelven a ser inmutables", versioning)


if __name__ == "__main__":
    unittest.main()
