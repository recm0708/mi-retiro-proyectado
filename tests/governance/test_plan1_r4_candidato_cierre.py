"""PLAN.1 R4.2 — preservación histórica del cierre formal de PLAN.1."""

import json
from pathlib import Path
import unittest
import warnings

from app.core.config import APP_VERSION
from app.core.version import version_valida

ROOT = Path(__file__).resolve().parents[2]
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

    def test_readme_muestra_estado_vigente_y_release_preserva_plan1(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")

        self.assertIn(f"**Versión de desarrollo:** `{self.version}`", readme)
        self.assertIn("**Objetivo de primera versión oficial:** `1.0.0.0`.", readme)

        for marcador in (
            "PLAN.1:** cerrado",
            "**720 pruebas en `OK`**",
            "tag firmado `v0.0.26-beta` publicado",
            "**UX.4.6e:** cerrada",
            "v0.0.25-beta",
        ):
            self.assertNotIn(marcador, readme)

        self.assertIn("cierre formal de PLAN.1", releases)
        self.assertIn("**720 pruebas en `OK`**", releases)
        self.assertIn("v0.0.25-beta", releases)
        self.assertIn("v0.0.26-beta", releases)


    def test_security_expone_version_actual_y_delega_historia_legacy(self):
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")

        self.assertIn(
            f"**Versión de desarrollo actual:** `{self.version}`",
            security,
        )
        self.assertIn("**Etapa soportada:** desarrollo beta", security)
        self.assertIn(
            "Las versiones beta anteriores, tags y Releases se conservan como historia",
            security,
        )
        self.assertNotIn("0.0.26-beta", security)

        self.assertIn("0.0.26-beta", releases)
        self.assertIn("cierre formal de PLAN.1", releases)

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


    def test_plan1_r4_1_r4_2_se_preservan_en_ledger_y_release(self):
        ledger = json.loads(
            (
                ROOT
                / "data/governance/"
                "pre-1-0-revision-ledger.json"
            ).read_text(encoding="utf-8")
        )
        entries = {
            item["global_revision"]: item
            for item in ledger["entries"]
        }

        g59 = entries[59]
        g60 = entries[60]
        self.assertEqual("PLAN.1", g59["block"])
        self.assertEqual("R4.1 — candidato local cerrado", g59["state"])
        self.assertIn("PR #23", g59["evidence"])
        self.assertIn("720 pruebas", g59["evidence"])

        self.assertEqual("PLAN.1", g60["block"])
        self.assertEqual("R4.2 — higiene y cierre formal", g60["state"])
        self.assertEqual("v0.0.26-beta", g60["anchor"])
        self.assertIn("PR #24", g60["evidence"])

        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("cierre formal de PLAN.1", releases)
        self.assertIn("v0.0.26-beta", releases)

        for path in (
            DOCS / "governance/roadmap.md",
            DOCS / "governance/master-plan-to-1-0.md",
        ):
            documento = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("G129/E03/C0", documento)
                self.assertIn("DOC.4 R1", documento)
                self.assertNotIn("PLAN.2 R2", documento)
                self.assertNotIn("G125/E01", documento)

    def test_validacion_preserva_cierre_posttag(self):
        texto = (DOCS / "operations/validation.md").read_text(encoding="utf-8")
        self.assertIn("cerró con **710 pruebas en `OK`**", texto)
        self.assertIn("cerró localmente con **720 pruebas en `OK`**", texto)
        self.assertIn("PR #24", texto)
        self.assertIn("b572796d68ff6fd91ce9944a0c6d1cf7d45753a0", texto)
        self.assertIn("**720 pruebas en `OK`** sin `SyntaxWarning`", texto)
        self.assertIn("`v0.0.26-beta`", texto)
        self.assertIn("bfbb746b177ebcc577f7241fef4d6914f713739a", texto)

    def test_auditoria_r4_documenta_frontera_local_y_remota(self):
        texto = (DOCS / "archive/governance/plan1-r4-audit-2026-08-20.md").read_text(encoding="utf-8")
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
        self.assertIn("## Metadata documental", versioning)
        self.assertIn(
            "**versión de aplicación revisada por un documento:** puede conservar la base",
            versioning,
        )
        self.assertIn(
            "Un documento histórico, ADR o auditoría no se moderniza únicamente",
            versioning,
        )

        transversal_path = (
            ROOT / "tests/governance/test_plan1_documentacion_transversal.py"
        )
        transversal = transversal_path.read_text(encoding="utf-8")
        with warnings.catch_warnings():
            warnings.simplefilter("error", SyntaxWarning)
            compile(transversal, str(transversal_path), "exec")


    def test_indice_delega_auditorias_y_versionado_a_sus_autoridades(self):
        indice = (DOCS / "README.md").read_text(encoding="utf-8")
        audits = (DOCS / "audits/README.md").read_text(encoding="utf-8")

        self.assertIn(
            "| Versionado | [Política de versionado](../VERSIONING.md)",
            indice,
        )
        self.assertIn("governance/pre-1-0-revision-ledger.md", indice)
        self.assertIn("| Auditorías | [Índice de auditorías](audits/README.md)", indice)
        self.assertIn("governance/", audits)
        self.assertNotIn("UX.4.6e R9.2", indice)
        self.assertNotIn("v0.0.25-beta", indice)

if __name__ == "__main__":
    unittest.main()
