"""Regresiones históricas de la promoción NOR.1 R8 -> G112/E07."""
from __future__ import annotations
import json
from pathlib import Path
import re
import unittest
from app.core.version_ledger import cargar_ledger
ROOT = Path(__file__).resolve().parents[1]
class TestG112PromotionPostMerge(unittest.TestCase):
    def test_g112_permanece_preservado_en_ledger(self):
        ledger = cargar_ledger(); entry = next(x for x in ledger["entries"] if x["global_revision"] == 112)
        self.assertEqual("NOR.1", entry["block"]); self.assertEqual(7, entry["ordinal"]); self.assertEqual("0.1.12.07-beta", entry["revision_aware"])
        self.assertIn("PR #89", entry["evidence"]); self.assertIn("PR #90", entry["evidence"])
    def test_registro_preserva_nor1(self):
        data=json.loads((ROOT/"data/work-block-registry.json").read_text(encoding="utf-8")); ids={x["identifier"]:x for x in data["identifiers"]}
        self.assertEqual("closed",ids["NOR.1"]["status"]); self.assertIn("G112",ids["NOR.1"]["global_refs"]); self.assertFalse(ids["NOR.1"]["reusable_for_different_scope"])
    def test_documentacion_viva_no_asocia_nor1_r8_con_e01(self):
        files=("README.md","RELEASES.md","VERSIONING.md","GOVERNANCE.md","CONTRIBUTING.md","SECURITY.md","docs/README.md","docs/governance/master-plan-to-1-0.md","docs/governance/roadmap.md","docs/governance/pre-1-0-revision-ledger.md","docs/operations/validation.md","docs/standards/work-block-identifiers.md")
        bad=re.compile(r"NOR\.1 R8.*(?:G112/E01|0\.1\.12\.01-beta)|(?:G112/E01|0\.1\.12\.01-beta).*NOR\.1 R8"); findings=[]
        for rel in files:
            for n,line in enumerate((ROOT/rel).read_text(encoding="utf-8").splitlines(),1):
                if bad.search(line): findings.append(f"{rel}:{n}")
        self.assertEqual([],findings)
    def test_historia_doc2_puede_conservar_e01_para_persist1(self):
        text=(ROOT/"docs/operations/validation.md").read_text(encoding="utf-8"); self.assertIn("0.1.12.01-beta",text); self.assertIn("next_candidate_block = PERSIST.1",text)
if __name__ == "__main__": unittest.main()
