"""Regresiones de promoción DOC.3 R1 -> G125/E01."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger


ROOT = Path(__file__).resolve().parents[2]


class TestG125DOC3R1Promotion(unittest.TestCase):
    def test_version_materializa_g125_e01(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.128.2.0-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((128, 2), descomponer_version_beta_revision(version))

    def test_ledger_preserva_g125_y_materializa_g127_e02(self):
        ledger = cargar_ledger()
        self.assertEqual(128, ledger["accepted_count"])
        self.assertEqual(129, ledger["next_global"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])

        g125 = next(
            item for item in ledger["entries"]
            if item["global_revision"] == 125
        )
        self.assertEqual("DOC.3", g125["block"])
        self.assertEqual(1, g125["ordinal"])
        self.assertEqual("R1", g125["functional_revision"])
        self.assertEqual("0.1.25.01-beta", g125["revision_aware"])

        current = ledger["entries"][-1]
        self.assertEqual(128, current["global_revision"])
        self.assertEqual("VER.2", current["block"])
        self.assertEqual(2, current["ordinal"])
        self.assertEqual("R6", current["functional_revision"])
        self.assertEqual("0.128.2.0-beta", current["revision_aware"])

    def test_registry_materializa_doc3_y_preserva_doc4_reservado(self):
        registry = json.loads(
            (ROOT / "data/governance/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        ids = {item["identifier"]: item for item in registry["identifiers"]}
        self.assertEqual("closed", ids["DOC.3"]["status"])
        self.assertIn("G125", ids["DOC.3"]["global_refs"])
        self.assertEqual("planned_reserved", ids["DOC.4"]["status"])

        plan2 = ids["PLAN.2"]
        self.assertEqual("closed", plan2["status"])
        self.assertIn("G114", plan2["global_refs"])
        self.assertIn("G126", plan2["global_refs"])

        candidate = registry["current_candidate"]
        self.assertEqual(128, candidate["global_revision"])
        self.assertEqual("0.128.2.0-beta", candidate["revision_aware"])
        self.assertEqual("VER.2", candidate["block"])
        self.assertEqual(129, candidate["next_global_available"])
        self.assertEqual("accepted_pending_integration", candidate["state"])

    def test_manifest_actual_materializa_mant2_r2(self):
        manifest = json.loads(
            (
                ROOT / "data/governance/release-publication-manifest.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual("0.128.2.0-beta", manifest["version"])
        self.assertEqual("VER.2", manifest["block"])
        self.assertEqual("R6", manifest["revision"])
        self.assertEqual(129, manifest["next_step"]["global_revision"])
        self.assertIsNone(manifest["next_step"]["revision_aware"])
        self.assertIsNone(manifest["next_step"]["block"])
        self.assertIn("VER.2 R6/#164", manifest["next_step"]["description"])

    def test_evidencia_doc3_declara_materializacion(self):
        audit = (
            ROOT / "docs/audits/documentation/documentation-audit-doc3-r1.md"
        ).read_text(encoding="utf-8")
        self.assertIn("G125/E01", audit)
        self.assertIn("0.1.25.01-beta", audit)
        self.assertIn("11 PASS / 0 FAIL", audit)
        self.assertIn("DOC.4", audit)


if __name__ == "__main__":
    unittest.main()
