"""Regresiones de la promoción post-merge G110/E01."""

from __future__ import annotations

from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG110PromotionPostMerge(unittest.TestCase):
    def test_version_y_runtime_materializan_g110(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.10.01-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((110, 1), descomponer_version_beta_revision(version))

    def test_ledger_acepta_g110_y_deja_g111_para_doc2(self):
        ledger = cargar_ledger()
        self.assertEqual(110, ledger["accepted_count"])
        self.assertEqual(111, ledger["next_global_if_ver2_accepted"])
        self.assertEqual(111, ledger["next_global"])
        self.assertEqual("0.1.11.01-beta", ledger["next_candidate"])
        self.assertEqual("DOC.2", ledger["next_candidate_block"])
        self.assertEqual("5cd1cea399a6db1cf25ab0d68c789f8c0e66f302", ledger["reconciled_through_commit"])
        self.assertEqual(110, ledger["entries"][-1]["global_revision"])
        self.assertEqual("REL.GOV.1", ledger["entries"][-1]["block"])
        self.assertIn("PR #85", ledger["entries"][-1]["evidence"])

    def test_documentacion_declara_promocion_sin_consumir_g111(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs/governance/roadmap.md").read_text(encoding="utf-8")
        ledger = (ROOT / "docs/governance/pre-1-0-revision-ledger.md").read_text(encoding="utf-8")
        for text in (readme, roadmap, ledger):
            self.assertIn("G110", text)
            self.assertIn("G111", text)
            self.assertIn("DOC.2", text)
        self.assertIn("no consume G111", ledger)

    def test_release_g110_esta_publicado_y_preserva_historia(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("v0.1.10.01-beta", releases)
        self.assertIn("PR #86", releases)
        self.assertIn("29 tags", releases)
        self.assertIn("29 Releases", releases)
        self.assertIn("v0.1.09.01-beta", releases)


if __name__ == "__main__":
    unittest.main()
