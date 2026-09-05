"""Regresiones históricas de promoción DEV.2 R6 -> G119/E05."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger


ROOT = Path(__file__).resolve().parents[1]


class TestG119PromotionPostMerge(unittest.TestCase):
    def test_g119_permanece_preservado_en_ledger(self):
        ledger = cargar_ledger()

        entry = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 119
        )

        self.assertEqual("DEV.2", entry["block"])
        self.assertEqual(5, entry["ordinal"])
        self.assertEqual("R6", entry["functional_revision"])
        self.assertEqual(
            "0.1.19.05-beta",
            entry["revision_aware"],
        )
        self.assertIn("PR #111", entry["evidence"])
        self.assertIn("bd2accb", entry["evidence"])

    def test_dev2_conserva_referencia_g119(self):
        data = json.loads(
            (
                ROOT / "data/work-block-registry.json"
            ).read_text(encoding="utf-8")
        )

        dev2 = next(
            item
            for item in data["identifiers"]
            if item["identifier"] == "DEV.2"
        )

        self.assertEqual("closed", dev2["status"])
        self.assertIn("G119", dev2["global_refs"])

    def test_publicacion_g119_permanece_en_historial(self):
        corpus = "\n".join(
            (
                (ROOT / "RELEASES.md").read_text(
                    encoding="utf-8"
                ),
                (ROOT / "SECURITY.md").read_text(
                    encoding="utf-8"
                ),
            )
        )

        self.assertIn("v0.1.19.05-beta", corpus)
        self.assertIn("G119/E05", corpus)


if __name__ == "__main__":
    unittest.main()
