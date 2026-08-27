"""Regresiones de la promoción DOC.1 R4 -> G115/E04."""
from __future__ import annotations
import json
from pathlib import Path
import unittest
from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger
ROOT=Path(__file__).resolve().parents[1]
class TestG115PromotionPostMerge(unittest.TestCase):
    def test_version_y_runtime_materializan_g115_e04(self):
        version=(ROOT/"VERSION").read_text(encoding="utf-8").strip(); self.assertEqual("0.1.15.04-beta",version); self.assertEqual(version,APP_VERSION); self.assertEqual((115,4),descomponer_version_beta_revision(version))
    def test_ledger_acepta_doc1_r4_y_reserva_rel_gov_r2(self):
        ledger=cargar_ledger(); self.assertEqual(115,ledger["accepted_count"]); self.assertEqual(116,ledger["next_global"]); self.assertEqual("0.1.16.02-beta",ledger["next_candidate"]); self.assertEqual("REL.GOV.1",ledger["next_candidate_block"])
        entry=ledger["entries"][-1]; self.assertEqual(115,entry["global_revision"]); self.assertEqual("DOC.1",entry["block"]); self.assertEqual(4,entry["ordinal"]); self.assertIn("PR #96",entry["evidence"]); self.assertIn("9f51229",entry["evidence"])
    def test_registro_cierra_doc1_r4_y_reabre_rel_gov_r2(self):
        data=json.loads((ROOT/"data/work-block-registry.json").read_text(encoding="utf-8")); ids={x["identifier"]:x for x in data["identifiers"]}; self.assertIn("G115",ids["DOC.1"]["global_refs"]); self.assertEqual("closed_r4_reopen_planned_r5",ids["DOC.1"]["status"]); self.assertEqual("reopened_candidate_r2",ids["REL.GOV.1"]["status"])
        c=data["current_candidate"]; self.assertEqual(116,c["global_revision"]); self.assertEqual("0.1.16.02-beta",c["revision_aware"]); self.assertEqual("REL.GOV.1",c["block"]); self.assertEqual("R2",c["revision"]); self.assertEqual(2,c["edition"])
    def test_matriz_declara_g115_aceptado_y_g116_candidato(self):
        matrix=(ROOT/"docs/governance/pre-1-0-pending-matrix.md").read_text(encoding="utf-8"); self.assertIn("Cerrado/aceptado G115/E04",matrix); self.assertIn("Candidato G116/E02",matrix); self.assertIn("REL.GOV.1 R2",matrix)
if __name__ == "__main__": unittest.main()
