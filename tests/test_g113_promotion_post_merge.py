"""Regresiones históricas de la promoción DOC.1 R3 -> G113/E03."""
from __future__ import annotations
import json
from pathlib import Path
import unittest
from app.core.version_ledger import cargar_ledger
ROOT=Path(__file__).resolve().parents[1]
class TestG113PromotionPostMerge(unittest.TestCase):
    def test_g113_permanece_preservado_en_ledger(self):
        ledger=cargar_ledger(); entry=next(x for x in ledger["entries"] if x["global_revision"]==113)
        self.assertEqual("DOC.1",entry["block"]); self.assertEqual(3,entry["ordinal"]); self.assertEqual("0.1.13.03-beta",entry["revision_aware"]); self.assertIn("PR #92",entry["evidence"])
    def test_registro_preserva_g113_en_doc1(self):
        data=json.loads((ROOT/"data/work-block-registry.json").read_text(encoding="utf-8")); ids={x["identifier"]:x for x in data["identifiers"]}
        self.assertIn("G113",ids["DOC.1"]["global_refs"]); self.assertFalse(ids["DOC.1"]["reusable_for_different_scope"])
    def test_documentacion_preserva_g113_y_doc1_r3(self):
        ledger = cargar_ledger()
        entry = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 113
        )
        self.assertEqual("DOC.1", entry["block"])
        self.assertEqual(3, entry["ordinal"])
        self.assertEqual("0.1.13.03-beta", entry["revision_aware"])

        ledger_md = (
            ROOT / "docs/governance/pre-1-0-revision-ledger.md"
        ).read_text(encoding="utf-8")
        self.assertIn("G113", ledger_md)
        self.assertIn("DOC.1 R3", ledger_md)

        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("v0.1.13.03-beta", releases)

    def test_auditoria_doc1_conserva_baseline_y_aceptacion(self):
        text=(ROOT/"docs/audits/documentation/documentation-markdown-links-doc1-r3.md").read_text(encoding="utf-8")
        self.assertIn("**Versión de aplicación revisada:** `0.1.12.07-beta`",text); self.assertIn("## 8. Resultado de aceptación",text); self.assertIn("G113/E03 (`0.1.13.03-beta`)",text); self.assertIn("PR #92",text)
if __name__ == "__main__": unittest.main()
