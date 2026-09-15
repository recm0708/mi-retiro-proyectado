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
        self.assertEqual("0.1.25.01-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((125, 1), descomponer_version_beta_revision(version))

    def test_ledger_materializa_doc3_r1_y_deja_g126_libre(self):
        ledger = cargar_ledger()
        self.assertEqual(125, ledger["accepted_count"])
        self.assertEqual(126, ledger["next_global"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])

        entry = ledger["entries"][-1]
        self.assertEqual(125, entry["global_revision"])
        self.assertEqual("DOC.3", entry["block"])
        self.assertEqual(1, entry["ordinal"])
        self.assertEqual("R1", entry["functional_revision"])
        self.assertEqual("0.1.25.01-beta", entry["revision_aware"])

    def test_registry_materializa_doc3_y_preserva_doc4_reservado(self):
        registry = json.loads(
            (ROOT / "data/governance/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        ids = {item["identifier"]: item for item in registry["identifiers"]}
        self.assertEqual("accepted_pending_publication", ids["DOC.3"]["status"])
        self.assertIn("G125", ids["DOC.3"]["global_refs"])
        self.assertEqual("planned_reserved", ids["DOC.4"]["status"])

        candidate = registry["current_candidate"]
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertIsNone(candidate["block"])
        self.assertEqual(126, candidate["next_global_available"])
        self.assertEqual("unassigned", candidate["state"])

    def test_manifest_materializa_g125_e01(self):
        manifest = json.loads(
            (
                ROOT / "data/governance/release-publication-manifest.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual("0.1.25.01-beta", manifest["version"])
        self.assertEqual("DOC.3", manifest["block"])
        self.assertEqual("R1", manifest["revision"])
        self.assertEqual(126, manifest["next_step"]["global_revision"])
        self.assertIsNone(manifest["next_step"]["revision_aware"])
        self.assertIsNone(manifest["next_step"]["block"])
        self.assertIn("PLAN.2 R2/#155", manifest["next_step"]["description"])

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
