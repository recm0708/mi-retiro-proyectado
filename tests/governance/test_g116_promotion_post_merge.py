"""Regresiones históricas de la promoción DOC.1 R5 -> G116/E05."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[2]


class TestG116PromotionPostMerge(unittest.TestCase):
    def test_ledger_preserva_g116_doc1_r5(self):
        ledger = cargar_ledger()
        entry = next(
            item for item in ledger["entries"]
            if item["global_revision"] == 116
        )
        self.assertEqual("DOC.1", entry["block"])
        self.assertEqual(5, entry["ordinal"])
        self.assertEqual("0.1.16.05-beta", entry["revision_aware"])
        self.assertIn("PR #101", entry["evidence"])
        self.assertIn("6f4266d", entry["evidence"])

    def test_registro_preserva_g116_en_doc1(self):
        data = json.loads(
            (ROOT / "data/governance/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertIn("G116", ids["DOC.1"]["global_refs"])

    def test_historia_g116_no_depende_de_matriz_viva(self):
        ledger = cargar_ledger()

        entry = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 116
        )

        self.assertEqual("DOC.1", entry["block"])
        self.assertEqual(5, entry["ordinal"])
        self.assertEqual(
            "0.1.16.05-beta",
            entry["revision_aware"],
        )

        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")

        self.assertIn("PLAN.2 R2", matrix)
        self.assertNotIn(
            "Cerrado/aceptado G116/E05",
            matrix,
        )

        releases = (
            ROOT / "RELEASES.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "v0.1.16.05-beta",
            releases,
        )

    def test_publicacion_g116_permanece_en_fuentes_canonicas(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")

        self.assertIn("v0.1.16.05-beta", releases)
        self.assertIn("0.1.16.05-beta", changelog)
        self.assertIn(
            "| `0.1.16.05-beta` | Beta previa G116/E05 publicada;",
            security,
        )


if __name__ == "__main__":
    unittest.main()
