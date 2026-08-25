"""Regresiones de PLAN.1 R2A para documentación primaria hacia 1.0."""

from pathlib import Path
import unittest

from app.core.config import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestPlan1DocumentacionPrimaria(unittest.TestCase):
    """Protege la planificación vigente sin reescribir evidencia histórica."""

    def test_readme_declara_beta_actual_y_objetivo_oficial(self):
        texto = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("**Etapa:** desarrollo beta", texto)
        self.assertIn("PLAN.1", texto)
        self.assertIn("**Primera versión oficial objetivo:** `1.0.0.0`", texto)
        self.assertIn("`Build 000001`", texto)
        self.assertNotIn("Primera beta pública objetivo de la aplicación", texto)

    def test_roadmap_registra_plan_de_catorce_bloques(self):
        texto = (DOCS / "governance/roadmap.md").read_text(encoding="utf-8")
        self.assertIn("## 4. PLAN.1 y secuencia hacia 1.0", texto)
        self.assertIn("14. REL.1 — preparación de la primera versión oficial", texto)
        self.assertIn("## 8. Criterio para primera versión oficial", texto)
        self.assertIn("Versión 1.0.0.0", texto)
        self.assertIn("Build 000001", texto)

    def test_releases_registra_evidencia_final_0_0_25(self):
        texto = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("7affa00e2530aeede066c10ecfee8c6dbd49b10b", texto)
        self.assertIn("303d4fe58b200a2c65120758ebe9d991e85b03c5", texto)
        self.assertIn("## 6. Línea oficial futura prevista", texto)
        self.assertIn("Tag v1.0.0.0", texto)

    def test_cierre_gov1_preserva_plan_antiguo_pero_declara_sustitucion(self):
        texto = (DOCS / "archive/governance/CIERRE_GOV1.md").read_text(encoding="utf-8")
        self.assertIn("0.1.0-beta.1", texto)
        self.assertIn("**Nota posterior — PLAN.1 / 2026-08-20:**", texto)
        self.assertIn("esa planificación fue sustituida", texto)
        self.assertIn("primera versión oficial `1.0.0.0`", texto)

    def test_version_canonica_permanece_sincronizada_tras_r2a(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, APP_VERSION)


if __name__ == "__main__":
    unittest.main()
