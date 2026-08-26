"""Regresiones de la promoción DOC.1 R3 -> G113/E03."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG113PromotionPostMerge(unittest.TestCase):
    def test_version_y_runtime_materializan_g113_e03(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.13.03-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((113, 3), descomponer_version_beta_revision(version))

    def test_ledger_acepta_doc1_r3_y_reserva_plan2(self):
        ledger = cargar_ledger()
        self.assertEqual(113, ledger["accepted_count"])
        self.assertEqual(114, ledger["next_global"])
        self.assertEqual("0.1.14.01-beta", ledger["next_candidate"])
        self.assertEqual("PLAN.2", ledger["next_candidate_block"])
        entry = ledger["entries"][-1]
        self.assertEqual(113, entry["global_revision"])
        self.assertEqual("DOC.1", entry["block"])
        self.assertEqual(3, entry["ordinal"])
        self.assertIn("PR #92", entry["evidence"])

    def test_registro_cierra_doc1_y_reserva_plan2(self):
        data = json.loads((ROOT / "data/work-block-registry.json").read_text(encoding="utf-8"))
        ids = {x["identifier"]: x for x in data["identifiers"]}
        c = data["current_candidate"]
        self.assertEqual("closed", ids["DOC.1"]["status"])
        self.assertIn("G113", ids["DOC.1"]["global_refs"])
        self.assertEqual(114, c["global_revision"])
        self.assertEqual("0.1.14.01-beta", c["revision_aware"])
        self.assertEqual("PLAN.2", c["block"])
        self.assertEqual("R1", c["revision"])
        self.assertEqual(1, c["edition"])
        self.assertEqual("DEV.2", c["next_functional_block_if_accepted"])
        self.assertIsNone(c["next_functional_global_if_accepted"])

    def test_documentacion_declara_g113_plan2_y_persist1(self):
        files = (
            "README.md", "RELEASES.md", "VERSIONING.md", "GOVERNANCE.md",
            "CONTRIBUTING.md", "SECURITY.md", "docs/README.md",
            "docs/governance/master-plan-to-1-0.md", "docs/governance/roadmap.md",
            "docs/governance/pre-1-0-revision-ledger.md", "docs/operations/validation.md",
            "docs/product/traceability-matrix.md",
        )
        for rel in files:
            text = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertIn("G113", text)
                self.assertIn("DOC.1 R3", text)
                self.assertIn("PLAN.2", text)
                self.assertIn("PERSIST.1", text)

    def test_auditoria_doc1_conserva_baseline_y_aceptacion(self):
        audit = (ROOT / "docs/audits/documentation/documentation-markdown-links-doc1-r3.md").read_text(encoding="utf-8")
        self.assertIn("**Versión de aplicación revisada:** `0.1.12.07-beta`", audit)
        self.assertIn("## 8. Resultado de aceptación", audit)
        self.assertIn("G113/E03 (`0.1.13.03-beta`)", audit)
        self.assertIn("PR #92", audit)


if __name__ == "__main__":
    unittest.main()
