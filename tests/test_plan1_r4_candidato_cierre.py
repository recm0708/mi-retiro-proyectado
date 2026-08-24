"""PLAN.1 R4.2 — preservación histórica del cierre formal de PLAN.1."""

from pathlib import Path
import unittest
import warnings

from app.core.config import APP_VERSION
from app.core.version import version_valida

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestPlan1R4CandidatoCierre(unittest.TestCase):
    """Protege el cierre histórico sin congelar la versión canónica futura."""

    def setUp(self):
        self.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    def test_version_actual_valida_y_preserva_cierre_plan1(self):
        self.assertEqual(self.version, APP_VERSION)
        self.assertTrue(version_valida(self.version))
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("0.0.26-beta", releases)
        self.assertIn("cierre formal de PLAN.1", releases)

    def test_readme_muestra_candidato_y_preserva_0_0_25_0_0_26(self):
        texto = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"**Versión canónica vigente:** `{self.version}`", texto)
        self.assertIn("PLAN.1:** cerrado en `0.0.26-beta`", texto)
        self.assertIn("**720 pruebas en `OK`**", texto)
        self.assertIn("tag firmado `v0.0.26-beta` publicado", texto)
        self.assertIn("**UX.4.6e:** cerrada en `0.0.25-beta`", texto)
        self.assertIn("v0.0.25-beta", texto)

    def test_security_soporta_candidato_y_archiva_legacy(self):
        texto = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn(f"| `{self.version}` | Versión vigente promovida en VER.2 R4", texto)
        self.assertIn("`0.0.26-beta`", texto)
        self.assertIn("Históricas", texto)

    def test_changelog_preserva_r4_2_y_tag_historico(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [0.0.26-beta] — 2026-08-20", texto)
        self.assertIn("R3B2", texto)
        self.assertIn("**710 pruebas en `OK`**", texto)
        self.assertIn("R4.1 promovió `VERSION` a `0.0.26-beta`", texto)
        self.assertIn("**720 pruebas en `OK`**", texto)
        self.assertIn("PR #23", texto)
        self.assertIn("497097f720c98f6e5a7ed689cf91368011a96be1", texto)
        self.assertIn("`SyntaxWarning`", texto)
        self.assertIn("tag formal asociado: `v0.0.26-beta`", texto)
        self.assertIn("bfbb746b177ebcc577f7241fef4d6914f713739a", texto)
        self.assertIn("b572796d68ff6fd91ce9944a0c6d1cf7d45753a0", texto)

    def test_releases_preserva_plan1_y_tags_legacy(self):
        texto = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("### `0.0.26-beta` — 2026-08-20 — cierre formal de PLAN.1", texto)
        self.assertIn("**720 pruebas en `OK`**", texto)
        self.assertIn("Pull Request #23", texto)
        self.assertIn("Pull Request #24", texto)
        self.assertIn("tag formal: `v0.0.26-beta`", texto)
        self.assertIn("bfbb746b177ebcc577f7241fef4d6914f713739a", texto)
        self.assertIn("b572796d68ff6fd91ce9944a0c6d1cf7d45753a0", texto)
        self.assertIn("v0.0.25-beta", texto)
        self.assertIn("7affa00e2530aeede066c10ecfee8c6dbd49b10b", texto)

    def test_roadmap_y_plan_maestro_preservan_r4_1_r4_2(self):
        roadmap = (DOCS / "ROADMAP.md").read_text(encoding="utf-8")
        plan = (DOCS / "PLAN_MAESTRO_HACIA_1_0.md").read_text(encoding="utf-8")
        self.assertIn("R4.1 — candidato local `0.0.26-beta`", roadmap)
        self.assertIn("**720 pruebas en `OK`**", roadmap)
        self.assertIn("R4.2 — PR #23/#24", roadmap)
        self.assertIn("**Cierre histórico de PLAN.1:** `0.0.26-beta`", plan)
        self.assertIn("**Estado de PLAN.1:** cerrado", plan)
        self.assertIn("PR #23 y PR #24", plan)
        self.assertIn("`v0.0.26-beta`", plan)

    def test_validacion_preserva_cierre_posttag(self):
        texto = (DOCS / "VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("cerró con **710 pruebas en `OK`**", texto)
        self.assertIn("cerró localmente con **720 pruebas en `OK`**", texto)
        self.assertIn("PR #24", texto)
        self.assertIn("b572796d68ff6fd91ce9944a0c6d1cf7d45753a0", texto)
        self.assertIn("**720 pruebas en `OK`** sin `SyntaxWarning`", texto)
        self.assertIn("`v0.0.26-beta`", texto)
        self.assertIn("bfbb746b177ebcc577f7241fef4d6914f713739a", texto)

    def test_auditoria_r4_documenta_frontera_local_y_remota(self):
        texto = (DOCS / "AUDITORIA_PLAN1_R4_2026-08-20.md").read_text(encoding="utf-8")
        self.assertIn("**Estado:** Cerrada — PLAN.1 completado en `0.0.26-beta`", texto)
        self.assertIn("R3B2 | 710 pruebas en `OK`", texto)
        self.assertIn("Ran 720 tests", texto)
        self.assertIn("**720 pruebas en `OK`** sin `SyntaxWarning`", texto)
        self.assertIn("`v0.0.26-beta`", texto)
        self.assertIn("bfbb746b177ebcc577f7241fef4d6914f713739a", texto)
        self.assertIn("b572796d68ff6fd91ce9944a0c6d1cf7d45753a0", texto)
        self.assertIn("## 6. Gate remoto R4.2", texto)

    def test_metadata_de_revision_documental_no_congela_version_actual(self):
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        self.assertIn("Los documentos de dominio pueden conservar la versión en la que fueron revisados", versioning)
        self.assertIn("versión en la que un documento fue revisado", versioning)

        transversal_path = ROOT / "tests/test_plan1_documentacion_transversal.py"
        transversal = transversal_path.read_text(encoding="utf-8")
        with warnings.catch_warnings():
            warnings.simplefilter("error", SyntaxWarning)
            compile(transversal, str(transversal_path), "exec")

    def test_indice_preserva_auditoria_y_declara_version_actual(self):
        texto = (DOCS / "INDICE.md").read_text(encoding="utf-8")
        self.assertIn("AUDITORIA_PLAN1_R4_2026-08-20.md", texto)
        self.assertIn("UX.4.6e R9.2", texto)
        self.assertIn("`v0.0.25-beta`", texto)
        self.assertIn(f"**Versión de aplicación:** `{self.version}`", texto)
        self.assertIn("AUDITORIA_VERSIONADO_PRE_1_0.md", texto)
        self.assertIn("LEDGER_REVISIONES_PRE_1_0.md", texto)


if __name__ == "__main__":
    unittest.main()
