"""Regresiones históricas de la promoción REL.GOV.1 R2 -> G117/E02."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG117PromotionPostMerge(unittest.TestCase):
    def test_g117_permanece_preservado_en_ledger(self):
        ledger = cargar_ledger()
        self.assertGreaterEqual(ledger["accepted_count"], 117)
        entry = next(item for item in ledger["entries"] if item["global_revision"] == 117)
        self.assertEqual("REL.GOV.1", entry["block"])
        self.assertEqual(2, entry["ordinal"])
        self.assertEqual("0.1.17.02-beta", entry["revision_aware"])
        self.assertIn("PR #103", entry["evidence"])
        self.assertIn("46c464e", entry["evidence"])

    def test_registro_preserva_rel_gov1(self):
        data = json.loads((ROOT / "data/work-block-registry.json").read_text(encoding="utf-8"))
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertIn("G117", ids["REL.GOV.1"]["global_refs"])
        self.assertEqual("closed", ids["REL.GOV.1"]["status"])

    def test_publicacion_g117_permanece_documentada(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("0.1.17.02-beta", releases)
        self.assertIn("G117/E02", releases)
        self.assertIn("v0.1.17.02-beta", releases)

    def test_estado_vivo_puede_avanzar_sin_reescribir_g117(self):
        ledger = cargar_ledger()
        self.assertGreaterEqual(ledger["accepted_count"], 117)
        self.assertGreaterEqual(ledger["next_global"], 118)
        self.assertTrue((ROOT / "VERSION").read_text(encoding="utf-8").strip().endswith("-beta"))


if __name__ == "__main__":
    unittest.main()
