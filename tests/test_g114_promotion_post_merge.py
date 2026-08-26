"""Regresiones de la promoción PLAN.2 R1 -> G114/E01."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG114PromotionPostMerge(unittest.TestCase):
    def test_version_y_runtime_materializan_g114_e01(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.14.01-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual(
            (114, 1),
            descomponer_version_beta_revision(version),
        )

    def test_ledger_acepta_plan2_y_reserva_doc1_r4(self):
        ledger = cargar_ledger()
        self.assertEqual(114, ledger["accepted_count"])
        self.assertEqual(115, ledger["next_global"])
        self.assertEqual("0.1.15.04-beta", ledger["next_candidate"])
        self.assertEqual("DOC.1", ledger["next_candidate_block"])
        entry = ledger["entries"][-1]
        self.assertEqual(114, entry["global_revision"])
        self.assertEqual("PLAN.2", entry["block"])
        self.assertEqual(1, entry["ordinal"])
        self.assertIn("PR #94", entry["evidence"])
        self.assertIn("7ded70c", entry["evidence"])

    def test_registro_cierra_plan2_y_reabre_doc1_r4(self):
        data = json.loads(
            (ROOT / "data/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        ids = {x["identifier"]: x for x in data["identifiers"]}
        self.assertEqual("closed", ids["PLAN.2"]["status"])
        self.assertIn("G114", ids["PLAN.2"]["global_refs"])
        self.assertEqual("reopened_candidate_r4", ids["DOC.1"]["status"])
        c = data["current_candidate"]
        self.assertEqual(115, c["global_revision"])
        self.assertEqual("0.1.15.04-beta", c["revision_aware"])
        self.assertEqual("DOC.1", c["block"])
        self.assertEqual("R4", c["revision"])
        self.assertEqual(4, c["edition"])

    def test_documentacion_declara_g114_y_doc1_r4(self):
        files = (
            "README.md",
            "RELEASES.md",
            "VERSIONING.md",
            "GOVERNANCE.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "docs/README.md",
            "docs/governance/master-plan-to-1-0.md",
            "docs/governance/roadmap.md",
            "docs/governance/pre-1-0-revision-ledger.md",
            "docs/governance/pre-1-0-pending-matrix.md",
            "docs/operations/validation.md",
            "docs/product/traceability-matrix.md",
        )
        for rel in files:
            text = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertIn("G114", text)
                self.assertIn("PLAN.2 R1", text)
                self.assertIn("DOC.1 R4", text)
                self.assertIn("G115", text)

    def test_g113_publicado_permanece_como_ultimo_tag_pre_promocion(self):
        for rel in ("README.md", "SECURITY.md", "VERSIONING.md", "RELEASES.md"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertIn("v0.1.13.03-beta", text)


if __name__ == "__main__":
    unittest.main()
