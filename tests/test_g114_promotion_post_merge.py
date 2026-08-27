"""Regresiones históricas de la promoción PLAN.2 R1 -> G114/E01."""
from __future__ import annotations
import json
from pathlib import Path
import unittest
from app.core.version_ledger import cargar_ledger
ROOT=Path(__file__).resolve().parents[1]
class TestG114PromotionPostMerge(unittest.TestCase):
    def test_g114_permanece_preservado_en_ledger(self):
        ledger=cargar_ledger(); entry=next(x for x in ledger["entries"] if x["global_revision"]==114)
        self.assertEqual("PLAN.2",entry["block"]); self.assertEqual(1,entry["ordinal"]); self.assertEqual("0.1.14.01-beta",entry["revision_aware"]); self.assertIn("PR #94",entry["evidence"]); self.assertIn("7ded70c",entry["evidence"])
    def test_registro_preserva_plan2_cerrado(self):
        data=json.loads((ROOT/"data/work-block-registry.json").read_text(encoding="utf-8")); ids={x["identifier"]:x for x in data["identifiers"]}
        self.assertEqual("closed",ids["PLAN.2"]["status"]); self.assertIn("G114",ids["PLAN.2"]["global_refs"])
    def test_documentacion_preserva_g114_plan2(self):
        for rel in ("README.md","RELEASES.md","VERSIONING.md","GOVERNANCE.md","SECURITY.md","docs/README.md","docs/governance/master-plan-to-1-0.md","docs/governance/roadmap.md","docs/governance/pre-1-0-revision-ledger.md","docs/governance/pre-1-0-pending-matrix.md"):
            text=(ROOT/rel).read_text(encoding="utf-8"); self.assertIn("G114",text); self.assertIn("PLAN.2 R1",text)
    def test_publicacion_g114_permanece_preservada(self):
        for rel in ("README.md","SECURITY.md","VERSIONING.md","RELEASES.md"): self.assertIn("v0.1.14.01-beta",(ROOT/rel).read_text(encoding="utf-8"))
if __name__ == "__main__": unittest.main()
