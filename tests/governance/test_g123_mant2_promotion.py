"""Regresiones históricas de promoción MANT.2 R1 -> G123/E01."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[2]


class TestG123MANT2Promotion(unittest.TestCase):
    def test_version_actual_avanza_sin_reescribir_g123(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.129.3.0-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((129, 3), descomponer_version_beta_revision(version))

    def test_ledger_preserva_g123_y_avanza_a_g125(self):
        ledger = cargar_ledger()
        self.assertEqual(129, ledger["accepted_count"])
        self.assertEqual(130, ledger["next_global"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])

        entry = next(
            x for x in ledger["entries"]
            if x["global_revision"] == 123
        )
        self.assertEqual("MANT.2", entry["block"])
        self.assertEqual("R1", entry["functional_revision"])
        self.assertEqual("0.1.23.01-beta", entry["revision_aware"])


    def test_registry_y_manifest_preservan_g123_y_estado_actual_g129(self):
        registry = json.loads(
            (ROOT / "data/governance/work-block-registry.json")
            .read_text(encoding="utf-8")
        )
        ids = {x["identifier"]: x for x in registry["identifiers"]}

        self.assertEqual("closed_r3_published", ids["MANT.2"]["status"])
        self.assertEqual(
            ["G123", "G127", "G129"],
            ids["MANT.2"]["global_refs"],
        )
        self.assertIn("G123/E01", ids["MANT.2"]["evidence"])
        self.assertIn("Issue #206", ids["MANT.2"]["evidence"])
        self.assertIn("Issue #211", ids["MANT.2"]["evidence"])

        candidate = registry["current_candidate"]
        self.assertEqual("unassigned", candidate["state"])
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["block"])
        self.assertEqual(130, candidate["next_global_available"])

        active = registry["active_phase"]
        self.assertEqual("DOC.4", active["block"])
        self.assertEqual("R1", active["revision"])
        self.assertEqual(129, active["base_global_revision"])

        manifest = json.loads(
            (ROOT / "data/governance/release-publication-manifest.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual("0.129.3.0-beta", manifest["version"])
        self.assertEqual("MANT.2", manifest["block"])
        self.assertEqual("R3", manifest["revision"])
        self.assertEqual(130, manifest["next_step"]["global_revision"])
        self.assertIsNone(manifest["next_step"]["revision_aware"])
        self.assertIsNone(manifest["next_step"]["block"])

    def test_dependencias_historicas_g123_preservadas(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("## Promoción G123/E01 — MANT.2 R1", releases)
        self.assertIn(
            "`httpx2`/`httpcore2`: 2.12.0; `pypdf`: 6.18.1; Playwright: 1.63.0.",
            releases,
        )


if __name__ == "__main__":
    unittest.main()
