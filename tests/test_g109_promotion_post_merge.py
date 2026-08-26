"""Regresiones de la promoción post-merge G109/E01."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG109PromotionPostMerge(unittest.TestCase):
    def test_version_y_runtime_materializan_g109(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.09.01-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((109, 1), descomponer_version_beta_revision(version))

    def test_ledger_acepta_g109_y_deja_g110_disponible(self):
        ledger = cargar_ledger()
        self.assertEqual(109, ledger["accepted_count"])
        self.assertEqual(110, ledger["next_global_if_ver2_accepted"])
        self.assertEqual(110, ledger["next_global"])
        self.assertEqual("0.1.10.01-beta", ledger["next_candidate"])
        self.assertEqual("DOC.2", ledger["next_candidate_block"])
        self.assertEqual(
            "ec1842dac10a5395fb594223d31092fdee3cdfc1",
            ledger["reconciled_through_commit"],
        )
        self.assertEqual(109, ledger["entries"][-1]["global_revision"])
        self.assertEqual("AUD.SEC2", ledger["entries"][-1]["block"])

    def test_documentacion_viva_declara_promocion_sin_consumir_g110(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs/governance/roadmap.md").read_text(encoding="utf-8")
        ledger = (ROOT / "docs/governance/pre-1-0-revision-ledger.md").read_text(
            encoding="utf-8"
        )
        for texto in (readme, roadmap, ledger):
            self.assertIn("0.1.09.01-beta", texto)
            self.assertIn("G109", texto)
            self.assertIn("G110", texto)
        self.assertIn("DOC.2", roadmap)
        self.assertIn("no consume G110", ledger)

    def test_tag_historico_permanece_inmutable_y_nuevo_tag_no_se_declara_publicado(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("v0.0.71.01-beta", releases)
        self.assertIn("Tag formal `v0.1.09.01-beta`: pendiente", releases)


if __name__ == "__main__":
    unittest.main()
