"""Regresiones históricas de la promoción DOC.1 R4 -> G115/E04."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[2]


class TestG115PromotionPostMerge(unittest.TestCase):
    def test_ledger_preserva_g115_doc1_r4(self):
        ledger = cargar_ledger()
        entry = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 115
        )
        self.assertEqual("DOC.1", entry["block"])
        self.assertEqual(4, entry["ordinal"])
        self.assertEqual("0.1.15.04-beta", entry["revision_aware"])
        self.assertIn("PR #96", entry["evidence"])
        self.assertIn("9f51229", entry["evidence"])

    def test_registro_preserva_g115_en_doc1(self):
        data = json.loads(
            (ROOT / "data/governance/work-block-registry.json").read_text(encoding="utf-8")
        )
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertIn("G115", ids["DOC.1"]["global_refs"])

    def test_historia_g115_no_depende_de_matriz_viva(self):
        ledger = cargar_ledger()

        entry = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 115
        )

        self.assertEqual("DOC.1", entry["block"])
        self.assertEqual(4, entry["ordinal"])
        self.assertEqual(
            "0.1.15.04-beta",
            entry["revision_aware"],
        )

        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")

        self.assertIn("PLAN.2 R2", matrix)
        self.assertNotIn(
            "Cerrado/aceptado G115/E04",
            matrix,
        )

        releases = (
            ROOT / "RELEASES.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "v0.1.15.04-beta",
            releases,
        )

    def test_publicacion_g115_permanece_preservada(self):
        ledger = cargar_ledger()
        entry = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 115
        )
        self.assertEqual("0.1.15.04-beta", entry["revision_aware"])
        self.assertEqual("DOC.1", entry["block"])
        self.assertEqual(4, entry["ordinal"])

        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("Promoción G115/E04", releases)
        self.assertIn("v0.1.15.04-beta", releases)

if __name__ == "__main__":
    unittest.main()
