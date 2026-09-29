"""Regresiones históricas de materialización VER.2 R6 / G128-E02-C0."""

import json
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[2]


class TestVer2R6G128Candidate(unittest.TestCase):
    def test_g128_permanece_inmutable_en_ledger(self):
        ledger = cargar_ledger()
        entry = next(item for item in ledger["entries"] if item["global_revision"] == 128)
        self.assertEqual(
            ("VER.2", 2, "R6", 2, 0, 0, "0.128.2.0-beta"),
            (entry["block"], entry["edition"], entry["functional_revision"], entry["identifier_schema"], entry["correction_ordinal"], entry["maintenance_ordinal"], entry["revision_aware"]),
        )

    def test_registry_conserva_g128_como_ver2_historico(self):
        reg = json.loads((ROOT / "data/governance/work-block-registry.json").read_text(encoding="utf-8"))
        ids = {item["identifier"]: item for item in reg["identifiers"]}
        self.assertIn("G128", ids["VER.2"]["global_refs"])
        self.assertEqual("closed_r6", ids["VER.2"]["status"])


if __name__ == "__main__":
    unittest.main()
