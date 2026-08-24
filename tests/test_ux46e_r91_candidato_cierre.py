"""UX.4.6e R9.1/R9.2 — preservación histórica del cierre 0.0.25-beta."""

from pathlib import Path
import re
import unittest

from app.core.config import APP_VERSION
from app.core.version import version_valida


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestUx46eR91CandidatoCierre(unittest.TestCase):
    """Protege el cierre histórico sin congelar la versión canónica futura."""

    def test_version_canonica_actual_es_valida_y_0_0_25_queda_historica(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, APP_VERSION)
        self.assertTrue(version_valida(version))
        self.assertIn("0.0.25-beta", (ROOT / "RELEASES.md").read_text(encoding="utf-8"))

    def test_readme_declara_cierre_historico_y_estado_ver2(self):
        texto = (ROOT / "README.md").read_text(encoding="utf-8")
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertIn(f"**Versión canónica vigente:** `{version}`", texto)
        self.assertIn("**UX.4.6e:** cerrada en `0.0.25-beta`", texto)
        self.assertIn("PR #21 integrado por squash", texto)
        self.assertNotIn("**Bloque activo:** UX.4.6e", texto)
        self.assertIn("**Bloque transversal activo:** VER.2", texto)
        self.assertIn("**Siguiente bloque funcional:** DEV.2", texto)

        indice = (DOCS / "INDICE.md").read_text(encoding="utf-8")
        self.assertIn(f"**Versión de aplicación:** `{version}`", indice)
        self.assertIn("UX.4.6e R9.2", indice)
        self.assertIn("`v0.0.25-beta`", indice)

    def test_security_distingue_candidato_y_lineas_historicas(self):
        texto = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertIn(f"| `{version}` | Versión vigente promovida en VER.2 R4", texto)
        self.assertIn("Históricas; no reciben correcciones independientes", texto)

    def test_changelog_preserva_hito_0_0_25(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [0.0.25-beta] — 2026-08-19", texto)
        self.assertIn("UX.4.6e R9.1 — candidato local de cierre", texto)
        self.assertIn("ADR-167", texto)
        self.assertIn("## [0.0.24-beta] — 2026-08-18", texto)

    def test_roadmap_preserva_r9_y_declara_cierre_ux46e(self):
        texto = (DOCS / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("R9.1 se conserva como candidato local histórico", texto)
        self.assertIn("R9.2 — cierre formal mediante PR #21/#22", texto)
        self.assertIn("[x] **UX.4.6e — Estandarización técnica", texto)
        self.assertIn("DEV.2 — Centro de desarrollo", texto)

    def test_validacion_registra_gate_local_de_660_cumplido(self):
        texto = (DOCS / "VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("Gate R9.1 — candidato `0.0.25-beta`", texto)
        self.assertIn("**652 pruebas en `OK`**", texto)
        self.assertIn("**8 regresiones específicas**", texto)
        self.assertIn("R9.1 alcanzó **660 pruebas en `OK`**", texto)
        self.assertIn("Gate R9.2 — cierre formal UX.4.6e", texto)
        self.assertIn("18e81e4ff58a1ad9622d366f7add10b7674f6e44", texto)

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

    def test_releases_registra_version_formal_y_tags_inmutables(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        self.assertIn("### `0.0.24-beta` — 2026-08-18", releases)
        self.assertIn("v0.0.24-beta", releases)
        self.assertIn("### `0.0.25-beta` — 2026-08-19", releases)
        self.assertIn("PR #21", releases)
        self.assertIn("18e81e4ff58a1ad9622d366f7add10b7674f6e44", releases)
        self.assertIn("tag firmado `v0.0.25-beta`", releases)
        self.assertIn("Los tags publicados son inmutables", versioning)
        self.assertIn("No se crean tags revision-aware retrospectivos", versioning)


if __name__ == "__main__":
    unittest.main()
