"""Regresiones de saneamiento semántico DOC.1 R4 y su aceptación G115/E04."""
from __future__ import annotations
import json
from pathlib import Path
import unittest
from app.core.version_ledger import cargar_ledger
ROOT = Path(__file__).resolve().parents[1]
class TestDOC1R4LiveStateSanitization(unittest.TestCase):
    def test_g115_acepta_doc1_r4(self):
        ledger=cargar_ledger(); self.assertGreaterEqual(ledger["accepted_count"],115)
        entry=next(e for e in ledger["entries"] if e["global_revision"]==115)
        self.assertEqual("DOC.1",entry["block"]); self.assertEqual(4,entry["ordinal"]); self.assertEqual("0.1.15.04-beta",entry["revision_aware"]); self.assertIn("PR #96",entry["evidence"]); self.assertIn("9f51229",entry["evidence"])
    def test_registro_preserva_g115_en_doc1(self):
        data=json.loads((ROOT/"data/work-block-registry.json").read_text(encoding="utf-8")); ids={x["identifier"]:x for x in data["identifiers"]}
        self.assertIn("G115",ids["DOC.1"]["global_refs"]); self.assertFalse(ids["DOC.1"]["reusable_for_different_scope"])
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
    def test_historia_g115_y_transicion_actual_usan_fuentes_canonicas(self):
        ledger = cargar_ledger()
        g115 = next(
            entry
            for entry in ledger["entries"]
            if entry["global_revision"] == 115
        )
        g117 = next(
            entry
            for entry in ledger["entries"]
            if entry["global_revision"] == 117
        )

        self.assertEqual("DOC.1", g115["block"])
        self.assertEqual(4, g115["ordinal"])
        self.assertEqual("0.1.15.04-beta", g115["revision_aware"])
        self.assertEqual("REL.GOV.1", g117["block"])
        self.assertEqual(2, g117["ordinal"])

        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Cerrado/aceptado G115/E04", matrix)
        self.assertIn("DOC.1 R4", matrix)
        self.assertIn("Cerrado/aceptado G117/E02", matrix)
        self.assertIn("Candidato G118/E04", matrix)

        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("v0.1.15.04-beta", releases)

        registry = json.loads(
            (ROOT / "data/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        candidate = registry["current_candidate"]
        self.assertEqual(118, candidate["global_revision"])
        self.assertEqual("DEV.2", candidate["block"])
        self.assertEqual("R5", candidate["revision"])

    def test_ledger_markdown_registra_g115(self):
        text=(ROOT/"docs/governance/pre-1-0-revision-ledger.md").read_text(encoding="utf-8"); self.assertIn("| G115 | `0.1.15.04-beta` | DOC.1 R4",text)
    def test_historia_y_evidencia_quedan_preservadas(self):
        self.assertIn("`VERSION` permanece en `0.0.26-beta`",(ROOT/"CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertIn("`VERSION=0.1.13.03-beta`",(ROOT/"docs/operations/validation.md").read_text(encoding="utf-8"))
        self.assertIn("Promoción G113/E03",(ROOT/"RELEASES.md").read_text(encoding="utf-8"))
        self.assertIn("documentation-live-state-doc1-r4.md",(ROOT/"docs/README.md").read_text(encoding="utf-8"))
if __name__ == "__main__": unittest.main()
