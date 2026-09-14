"""Regresiones de promoción MANT.1 R8 -> G124/E13."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[2]


class TestG124MANT1R8Promotion(unittest.TestCase):
    def test_version_materializa_g124_e13(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.24.13-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((124, 13), descomponer_version_beta_revision(version))

    def test_ledger_materializa_mant1_r8_y_deja_g125_libre(self):
        ledger = cargar_ledger()
        self.assertEqual(124, ledger["accepted_count"])
        self.assertEqual(125, ledger["next_global"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])

        entry = ledger["entries"][-1]
        self.assertEqual(124, entry["global_revision"])
        self.assertEqual("MANT.1", entry["block"])
        self.assertEqual(13, entry["ordinal"])
        self.assertEqual("R8", entry["functional_revision"])
        self.assertEqual("0.1.24.13-beta", entry["revision_aware"])

    def test_registry_cierra_mant1_y_no_preasigna_g125(self):
        registry = json.loads(
            (ROOT / "data/governance/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        ids = {item["identifier"]: item for item in registry["identifiers"]}
        self.assertEqual("closed", ids["MANT.1"]["status"])
        self.assertIn("G074-G085", ids["MANT.1"]["global_refs"])
        self.assertIn("G124", ids["MANT.1"]["global_refs"])

        candidate = registry["current_candidate"]
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertIsNone(candidate["block"])
        self.assertEqual(125, candidate["next_global_available"])
        self.assertEqual("unassigned_pending_post_mant1_r8", candidate["state"])

    def test_manifest_materializa_g124_e13(self):
        manifest = json.loads(
            (
                ROOT / "data/governance/release-publication-manifest.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual("0.1.24.13-beta", manifest["version"])
        self.assertEqual("MANT.1", manifest["block"])
        self.assertEqual("R8", manifest["revision"])
        self.assertEqual(125, manifest["next_step"]["global_revision"])
        self.assertIsNone(manifest["next_step"]["revision_aware"])
        self.assertIsNone(manifest["next_step"]["block"])
        self.assertIn("DOC.3 R1/#154", manifest["next_step"]["description"])

    def test_evidencia_mant1_r8_conserva_resultado_de_auditoria(self):
        audit = (
            ROOT
            / "docs/audits/repository/mant1-r8-scripts-tests-consolidation.md"
        ).read_text(encoding="utf-8")
        self.assertIn("| CONSERVAR | 16 | 219 |", audit)
        self.assertIn("| CONSOLIDAR | 0 | 0 |", audit)
        self.assertIn("| RETIRAR | 0 | 0 |", audit)
        self.assertIn("220 módulos", audit)

    def test_continuidad_deja_doc3_como_siguiente_fase(self):
        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Cerrado/aceptado localmente G124/E13", matrix)
        self.assertIn("DOC.3 R1", matrix)
        self.assertIn("G125", matrix)


if __name__ == "__main__":
    unittest.main()
