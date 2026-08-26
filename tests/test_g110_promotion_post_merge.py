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

    def test_g110_permanece_historico_sin_fijar_version_actual(self):
        ledger = cargar_ledger()
        entry = next(e for e in ledger["entries"] if e["global_revision"] == 110)
        self.assertEqual("0.1.10.01-beta", entry["revision_aware"])
        self.assertEqual("REL.GOV.1", entry["block"])

    def test_release_g110_permanece_publicado(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("v0.1.10.01-beta", releases)
        self.assertIn("PR #86", releases)
        self.assertIn("29 tags", releases)

    def test_g111_permanece_preservado_despues_de_promociones_posteriores(self):
        ledger = cargar_ledger()
        entry = next(e for e in ledger["entries"] if e["global_revision"] == 111)
        self.assertEqual("DOC.2", entry["block"])
        self.assertEqual("0.1.11.01-beta", entry["revision_aware"])


if __name__ == "__main__":
    unittest.main()
