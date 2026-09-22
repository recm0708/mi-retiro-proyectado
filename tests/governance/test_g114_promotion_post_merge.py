"""Regresiones históricas de la promoción PLAN.2 R1 -> G114/E01."""
from __future__ import annotations
import json
from pathlib import Path
import unittest
from app.core.version_ledger import cargar_ledger
ROOT=Path(__file__).resolve().parents[2]
class TestG114PromotionPostMerge(unittest.TestCase):
    def test_g114_permanece_preservado_en_ledger(self):
        ledger=cargar_ledger(); entry=next(x for x in ledger["entries"] if x["global_revision"]==114)
        self.assertEqual("PLAN.2",entry["block"]); self.assertEqual(1,entry["ordinal"]); self.assertEqual("0.1.14.01-beta",entry["revision_aware"]); self.assertIn("PR #94",entry["evidence"]); self.assertIn("7ded70c",entry["evidence"])
    def test_registro_preserva_g114_y_reconoce_mant2_r2_actual(self):
        data = json.loads(
            (
                ROOT
                / "data/governance/work-block-registry.json"
            ).read_text(
                encoding="utf-8"
            )
        )

        ids = {
            item["identifier"]: item
            for item in data["identifiers"]
        }

        self.assertEqual(
            "closed",
            ids["PLAN.2"]["status"],
        )
        self.assertEqual(
            ["G114", "G126"],
            ids["PLAN.2"]["global_refs"],
        )
        self.assertEqual(
            "closed_r2",
            ids["MANT.2"]["status"],
        )

        active = data["active_phase"]

        self.assertEqual("VER.2", active["block"])
        self.assertEqual("R6", active["revision"])
        self.assertEqual(164, active["issue"])
        self.assertEqual("accepted_pending_integration", active["state"])
        self.assertEqual(128, active["global_revision"])
        self.assertEqual("0.128.2.0-beta", active["revision_aware"])
        self.assertEqual(
            127,
            active["base_global_revision"],
        )
        self.assertEqual(
            "0.1.27.02-beta",
            active["base_revision_aware"],
        )

    def test_documentacion_preserva_g114_plan2(self):
        ledger = cargar_ledger()
        entry = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 114
        )
        self.assertEqual("PLAN.2", entry["block"])
        self.assertEqual(1, entry["ordinal"])
        self.assertEqual("0.1.14.01-beta", entry["revision_aware"])

        historical_audit = (
            ROOT
            / "docs/audits/documentation/"
            "post-g113-live-documentation-audit-plan2-r1.md"
        )
        self.assertTrue(historical_audit.is_file())

        audit_text = historical_audit.read_text(encoding="utf-8")
        self.assertIn("PLAN.2 R1", audit_text)

        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("v0.1.14.01-beta", releases)

    def test_publicacion_g114_permanece_preservada(self):
        ledger = cargar_ledger()
        entry = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 114
        )
        self.assertEqual("PLAN.2", entry["block"])
        self.assertEqual(1, entry["ordinal"])
        self.assertEqual("0.1.14.01-beta", entry["revision_aware"])

        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("v0.1.14.01-beta", releases)
if __name__ == "__main__": unittest.main()
