"""Regresiones históricas de la promoción post-merge G110/E01."""

from __future__ import annotations

from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG110PromotionPostMerge(unittest.TestCase):
    def test_g110_permanece_preservado_en_ledger(self):
        ledger = cargar_ledger()
        entry = next(e for e in ledger["entries"] if e["global_revision"] == 110)
        self.assertEqual("REL.GOV.1", entry["block"])
        self.assertEqual("0.1.10.01-beta", entry["revision_aware"])
        self.assertIn("PR #85", entry["evidence"])

    def test_version_actual_avanza_a_g111_sin_reescribir_g110(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.11.01-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((111, 1), descomponer_version_beta_revision(version))

    def test_release_g110_permanece_publicado(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("v0.1.10.01-beta", releases)
        self.assertIn("PR #86", releases)
        self.assertIn("29 tags", releases)

    def test_g111_es_doc2_y_g112_queda_para_persist1(self):
        ledger = cargar_ledger()
        self.assertEqual(111, ledger["accepted_count"])
        self.assertEqual(112, ledger["next_global"])
        self.assertEqual("PERSIST.1", ledger["next_candidate_block"])


if __name__ == "__main__":
    unittest.main()
