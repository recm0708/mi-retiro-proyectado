"""PLAN.1 R4.2 — cierre remoto, evidencia post-merge e higiene pre-tag."""

from pathlib import Path
import re
import unittest
import warnings

from app.core.config import APP_VERSION
from app.core.version import version_valida

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestPlan1R4CandidatoCierre(unittest.TestCase):
    """Protege la evidencia remota real y mantiene bloqueado el tag hasta un gate limpio."""

    def setUp(self):
        self.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    def test_version_promovida_a_0_0_26_y_runtime_coincide(self):
        self.assertEqual("0.0.26-beta", self.version)
        self.assertEqual(self.version, APP_VERSION)
        self.assertTrue(version_valida(self.version))

    def test_readme_muestra_candidato_validado_y_preserva_0_0_25(self):
        texto = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("**Versión formal vigente:** `0.0.26-beta`", texto)
        self.assertIn("R4.2 integró el PR #23 por squash", texto)
        self.assertIn("**720 pruebas en `OK`**", texto)
        self.assertIn("`SyntaxWarning`", texto)
        self.assertIn("**UX.4.6e:** cerrada en `0.0.25-beta`", texto)
        self.assertIn("v0.0.25-beta", texto)

    def test_security_soporta_candidato_y_archiva_previa(self):
        texto = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("| `0.0.26-beta` | Soportada durante la etapa beta vigente |", texto)
        self.assertIn("| `0.0.25-beta` y anteriores | Históricas", texto)

    def test_changelog_registra_r4_2_real_sin_fingir_tag(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("## [0.0.26-beta] — 2026-08-20", texto)
        self.assertIn("R3B2", texto)
        self.assertIn("**710 pruebas en `OK`**", texto)
        self.assertIn("R4.1 promovió `VERSION` a `0.0.26-beta`", texto)
        self.assertIn("**720 pruebas en `OK`**", texto)
        self.assertIn("PR #23", texto)
        self.assertIn("497097f720c98f6e5a7ed689cf91368011a96be1", texto)
        self.assertIn("`SyntaxWarning`", texto)
        self.assertIn("`v0.0.26-beta` continúa sin crearse", texto)

    def test_releases_registra_candidato_sin_tag_anticipado(self):
        texto = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("### `0.0.26-beta` — 2026-08-20 — candidato R4.2 en higiene pre-tag", texto)
        self.assertIn("**720 pruebas en `OK`**", texto)
        self.assertIn("tag `v0.0.26-beta`: **no creado todavía**", texto)
        self.assertIn("Pull Request #23", texto)
        self.assertIn("`success`", texto)
        self.assertIn("v0.0.25-beta", texto)
        self.assertIn("7affa00e2530aeede066c10ecfee8c6dbd49b10b", texto)

    def test_roadmap_y_plan_maestro_separan_r4_1_de_r4_2(self):
        roadmap = (DOCS / "ROADMAP.md").read_text(encoding="utf-8")
        plan = (DOCS / "PLAN_MAESTRO_HACIA_1_0.md").read_text(encoding="utf-8")
        self.assertIn("[x] R4.1 — candidato local `0.0.26-beta` validado", roadmap)
        self.assertIn("**720 pruebas en `OK`**", roadmap)
        self.assertIn("[ ] R4.2 — cierre remoto y tag firmado", roadmap)
        self.assertIn("[x] PR #23 integrado por squash", roadmap)
        self.assertIn("[ ] corregir y revalidar sin `SyntaxWarning`", roadmap)
        self.assertIn("**Versión candidata de cierre de PLAN.1:** `0.0.26-beta`", plan)
        self.assertIn("R4.2 integró el PR #23", plan)
        self.assertIn("tag permanece bloqueado", plan)

    def test_validacion_registra_postmerge_y_higiene_pretag(self):
        texto = (DOCS / "VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("cerró con **710 pruebas en `OK`**", texto)
        self.assertIn("cerró localmente con **720 pruebas en `OK`**", texto)
        self.assertIn("PR #23", texto)
        self.assertIn("497097f720c98f6e5a7ed689cf91368011a96be1", texto)
        self.assertIn("`SyntaxWarning`", texto)
        self.assertIn("repetir el mismo gate de **720 pruebas en `OK`** sin la advertencia", texto)

    def test_auditoria_r4_documenta_frontera_local_y_remota(self):
        texto = (DOCS / "AUDITORIA_PLAN1_R4_2026-08-20.md").read_text(encoding="utf-8")
        self.assertIn("**Estado:** R4.2 — PR #23 integrado; higiene pre-tag pendiente", texto)
        self.assertIn("R3B2 | 710 pruebas en `OK`", texto)
        self.assertIn("Ran 720 tests", texto)
        self.assertIn("gate post-merge: **720 pruebas en `OK`**", texto)
        self.assertIn("`SyntaxWarning`", texto)
        self.assertIn("tag firmado `v0.0.26-beta`", texto)
        self.assertIn("## 6. Gate remoto R4.2", texto)

    def test_documentacion_viva_revisada_con_version_candidata(self):
        excepciones = {
            "AUDITORIA_UX46E_R7_2026-08-18.md",
            "AUDITORIA_REPOSITORIO_2026-08-18.md",
            "CIERRE_GOV1.md",
            "MIGRACION_FIRMAS_GIT_2026-08-17.md",
            "PLAN_MAESTRO_HACIA_1_0.md",
            "REGISTRO_CAMBIOS_HISTORICO.md",
        }
        errores = []
        for path in DOCS.glob("*.md"):
            if path.name in excepciones or path.name.startswith("UX_4_6"):
                continue
            texto = path.read_text(encoding="utf-8")
            match = re.search(
                r"\*\*(?:Versión de aplicación revisada|Versión candidata revisada|Versión de aplicación):\*\* `([^`]+)`",
                texto[:1500],
            )
            if match and match.group(1) != self.version:
                errores.append(f"{path.name}:{match.group(1)}")
        self.assertEqual([], errores)

        transversal_path = ROOT / "tests/test_plan1_documentacion_transversal.py"
        transversal = transversal_path.read_text(encoding="utf-8")
        with warnings.catch_warnings():
            warnings.simplefilter("error", SyntaxWarning)
            compile(transversal, str(transversal_path), "exec")

    def test_indice_enlaza_auditoria_y_preserva_cierre_ux(self):
        texto = (DOCS / "INDICE.md").read_text(encoding="utf-8")
        self.assertIn("AUDITORIA_PLAN1_R4_2026-08-20.md", texto)
        self.assertIn("UX.4.6e R9.2", texto)
        self.assertIn("cierre formal `0.0.25-beta`", texto)
        self.assertIn("**Versión de aplicación revisada:** `0.0.26-beta`", texto)


if __name__ == "__main__":
    unittest.main()
