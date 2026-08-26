"""Regresiones históricas de la promoción post-merge G109/E01."""

from __future__ import annotations

from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG109PromotionPostMerge(unittest.TestCase):
    def test_g109_permanece_preservado_en_ledger(self):
        ledger = cargar_ledger()
        entry = next(e for e in ledger["entries"] if e["global_revision"] == 109)
        self.assertEqual("AUD.SEC2", entry["block"])
        self.assertEqual("0.1.09.01-beta", entry["revision_aware"])
        self.assertIn("PR #83", entry["evidence"])

    def test_version_actual_puede_avanzar_sin_reescribir_g109(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.10.01-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((110, 1), descomponer_version_beta_revision(version))

    def test_documentacion_conserva_publicacion_g109(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("G109/E01", releases)
        self.assertIn("v0.1.09.01-beta", releases)
        self.assertIn("## [0.1.09.01-beta]", changelog)

    def test_reconciliacion_historica_g087_permanece_documentada(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("v0.0.71.01-beta", releases)
        self.assertIn("G087/E01", releases)


if __name__ == "__main__":
    unittest.main()
