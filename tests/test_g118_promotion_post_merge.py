"""Regresiones históricas de promoción DEV.2 R5 -> G118/E04."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG118PromotionPostMerge(unittest.TestCase):
    def test_g118_permanece_preservado_en_ledger(self):
        ledger = cargar_ledger()
        entry = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 118
        )
        self.assertEqual("DEV.2", entry["block"])
        self.assertEqual(4, entry["ordinal"])
        self.assertEqual("R5", entry["functional_revision"])
        self.assertEqual("0.1.18.04-beta", entry["revision_aware"])
        self.assertIn("PR #107", entry["evidence"])
        self.assertIn("bc97db0", entry["evidence"])

    def test_g118_permanece_publicado_como_estado_anterior(self):
        corpus = "\n".join(
            (
                (ROOT / "README.md").read_text(encoding="utf-8"),
                (ROOT / "RELEASES.md").read_text(encoding="utf-8"),
                (ROOT / "SECURITY.md").read_text(encoding="utf-8"),
            )
        )
        self.assertIn("v0.1.18.04-beta", corpus)
        self.assertIn(
            "290e84aab70a257e8b718d172e37365af49ef048",
            corpus,
        )

    def test_registro_dev2_preserva_g118_y_g119(self):
        data = json.loads(
            (ROOT / "data/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        dev2 = next(
            item
            for item in data["identifiers"]
            if item["identifier"] == "DEV.2"
        )
        self.assertIn("G118", dev2["global_refs"])
        self.assertIn("G119", dev2["global_refs"])
        self.assertEqual("closed", dev2["status"])


if __name__ == "__main__":
    unittest.main()
