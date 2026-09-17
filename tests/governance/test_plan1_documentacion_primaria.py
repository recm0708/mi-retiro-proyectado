"""Regresiones de PLAN.1 R2A para documentación primaria hacia 1.0."""

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION

ROOT = Path(__file__).resolve().parents[2]
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

    def test_plan1_historico_y_roadmap_vivo_usan_fuentes_correctas(self):
        ledger = json.loads(
            (
                ROOT
                / "data/governance/"
                "pre-1-0-revision-ledger.json"
            ).read_text(encoding="utf-8")
        )

        plan1 = [
            item
            for item in ledger["entries"]
            if item["block"] == "PLAN.1"
        ]

        self.assertGreaterEqual(
            len(plan1),
            10,
        )
        self.assertEqual(
            51,
            min(item["global_revision"] for item in plan1),
        )
        self.assertEqual(
            60,
            max(item["global_revision"] for item in plan1),
        )

        releases = (
            ROOT / "RELEASES.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "cierre formal de PLAN.1",
            releases,
        )
        self.assertIn(
            "v0.0.26-beta",
            releases,
        )

        roadmap = (
            DOCS / "governance/roadmap.md"
        ).read_text(encoding="utf-8")

        for esperado in (
            "PLAN.2 R2",
            "1.0.0.0",
            "VER.2 R6",
            "REL.1",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(
                    esperado,
                    roadmap,
                )

    def test_releases_registra_evidencia_final_0_0_25(self):
        texto = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("7affa00e2530aeede066c10ecfee8c6dbd49b10b", texto)
        self.assertIn("303d4fe58b200a2c65120758ebe9d991e85b03c5", texto)
        self.assertIn("## 6. Línea oficial futura prevista", texto)
        self.assertIn("Tag v1.0.0.0", texto)

    def test_cierre_gov1_preserva_plan_antiguo_pero_declara_sustitucion(self):
        texto = (DOCS / "archive/governance/gov1-closeout.md").read_text(encoding="utf-8")
        self.assertIn("0.1.0-beta.1", texto)
        self.assertIn("**Nota posterior — PLAN.1 / 2026-08-20:**", texto)
        self.assertIn("esa planificación fue sustituida", texto)
        self.assertIn("primera versión oficial `1.0.0.0`", texto)

    def test_version_canonica_permanece_sincronizada_tras_r2a(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, APP_VERSION)


if __name__ == "__main__":
    unittest.main()
