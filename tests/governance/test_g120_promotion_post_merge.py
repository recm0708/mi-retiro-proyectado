"""Regresiones históricas de promoción UX.5 R6 -> G120/E01."""

from __future__ import annotations
import json
from pathlib import Path
import unittest
from app.core.version_ledger import cargar_ledger
ROOT = Path(__file__).resolve().parents[2]

class TestG120PromotionPostMerge(unittest.TestCase):
    def test_g120_permanece_preservado_en_ledger(self):
        entry = next(x for x in cargar_ledger()["entries"] if x["global_revision"] == 120)
        self.assertEqual("UX.5", entry["block"])
        self.assertEqual(1, entry["ordinal"])
        self.assertEqual("R6", entry["functional_revision"])
        self.assertEqual("0.1.20.01-beta", entry["revision_aware"])
        self.assertIn("PR #122", entry["evidence"])
        self.assertIn("4c43a816", entry["evidence"])

    def test_ux5_conserva_referencia_g120(self):
        data = json.loads((ROOT / "data/governance/work-block-registry.json").read_text(encoding="utf-8"))
        ux5 = next(x for x in data["identifiers"] if x["identifier"] == "UX.5")
        self.assertEqual("closed", ux5["status"])
        self.assertIn("G120", ux5["global_refs"])

    def test_publicacion_g120_permanece_en_historial(self):
        corpus = "\n".join(((ROOT / "README.md").read_text(encoding="utf-8"), (ROOT / "RELEASES.md").read_text(encoding="utf-8"), (ROOT / "SECURITY.md").read_text(encoding="utf-8")))
        self.assertIn("v0.1.20.01-beta", corpus)
        self.assertIn("G120/E01", corpus)
        self.assertIn("383133233", corpus)

if __name__ == "__main__": unittest.main()
