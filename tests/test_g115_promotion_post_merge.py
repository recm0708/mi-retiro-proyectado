"Regresiones históricas de la promoción DOC.1 R4 -> G115/E04."
from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG115PromotionPostMerge(unittest.TestCase):
    def test_version_y_runtime_preservan_g115_e04(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.15.04-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((115, 4), descomponer_version_beta_revision(version))

    def test_ledger_preserva_g115_doc1_r4_como_ultimo_aceptado(self):
        ledger = cargar_ledger()
        self.assertEqual(115, ledger["accepted_count"])
        self.assertEqual(116, ledger["next_global"])
        entry = ledger["entries"][-1]
        self.assertEqual(115, entry["global_revision"])
        self.assertEqual("DOC.1", entry["block"])
        self.assertEqual(4, entry["ordinal"])
        self.assertIn("PR #96", entry["evidence"])
        self.assertIn("9f51229", entry["evidence"])

    def test_registro_preserva_g115_en_doc1(self):
        data = json.loads((ROOT / "data/work-block-registry.json").read_text(encoding="utf-8"))
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertIn("G115", ids["DOC.1"]["global_refs"])

    def test_matriz_preserva_g115_como_estado_aceptado(self):
        matrix = (ROOT / "docs/governance/pre-1-0-pending-matrix.md").read_text(encoding="utf-8")
        self.assertIn("Cerrado/aceptado G115/E04", matrix)
        self.assertIn("DOC.1 R4", matrix)


if __name__ == "__main__":
    unittest.main()
