"""Regresiones históricas de promoción MANT.1 R8 -> G124/E13."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[2]


class TestG124MANT1R8Promotion(unittest.TestCase):
    def test_version_actual_avanza_sin_reescribir_g124(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.128.2.0-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((128, 2), descomponer_version_beta_revision(version))
        entry = next(x for x in cargar_ledger()["entries"] if x["global_revision"] == 124)
        self.assertEqual("MANT.1", entry["block"])
        self.assertEqual(13, entry["ordinal"])
        self.assertEqual("R8", entry["functional_revision"])
        self.assertEqual("0.1.24.13-beta", entry["revision_aware"])

    def test_ledger_preserva_g124_y_materializa_g125(self):
        ledger = cargar_ledger()
        self.assertEqual(128, ledger["accepted_count"])
        self.assertEqual(129, ledger["next_global"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])
        entry = next(x for x in ledger["entries"] if x["global_revision"] == 124)
        self.assertEqual("MANT.1", entry["block"])
        self.assertEqual(13, entry["ordinal"])
        self.assertEqual("R8", entry["functional_revision"])
        self.assertEqual("0.1.24.13-beta", entry["revision_aware"])

    def test_registry_cierra_mant1_y_deja_g126_libre(self):
        registry = json.loads((ROOT / "data/governance/work-block-registry.json").read_text(encoding="utf-8"))
        ids = {item["identifier"]: item for item in registry["identifiers"]}
        self.assertEqual("closed", ids["MANT.1"]["status"])
        self.assertIn("G074-G085", ids["MANT.1"]["global_refs"])
        self.assertIn("G124", ids["MANT.1"]["global_refs"])
        candidate = registry["current_candidate"]
        self.assertEqual(128, candidate["global_revision"])
        self.assertEqual("0.128.2.0-beta", candidate["revision_aware"])
        self.assertEqual("VER.2", candidate["block"])
        self.assertEqual(129, candidate["next_global_available"])
        self.assertEqual("accepted_pending_integration", candidate["state"])

    def test_manifest_actual_materializa_mant2_r2(self):
        manifest = json.loads(
            (ROOT / "data/governance/release-publication-manifest.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("0.128.2.0-beta", manifest["version"])
        self.assertEqual("VER.2", manifest["block"])
        self.assertEqual("R6", manifest["revision"])
        self.assertEqual(129, manifest["next_step"]["global_revision"])
        self.assertIsNone(manifest["next_step"]["revision_aware"])
        self.assertIsNone(manifest["next_step"]["block"])
        self.assertIn("VER.2 R6/#164", manifest["next_step"]["description"])

    def test_evidencia_mant1_r8_conserva_resultado_de_auditoria(self):
        audit = (ROOT / "docs/audits/repository/mant1-r8-scripts-tests-consolidation.md").read_text(encoding="utf-8")
        self.assertIn("| CONSERVAR | 16 | 219 |", audit)
        self.assertIn("| CONSOLIDAR | 0 | 0 |", audit)
        self.assertIn("| RETIRAR | 0 | 0 |", audit)
        self.assertIn("220 módulos", audit)

    def test_continuidad_preserva_g124_y_frontera_viva_plan2(self):
        ledger = cargar_ledger()

        g124 = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 124
        )
        g125 = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 125
        )

        self.assertEqual("MANT.1", g124["block"])
        self.assertEqual("R8", g124["functional_revision"])
        self.assertEqual(
            "0.1.24.13-beta",
            g124["revision_aware"],
        )

        self.assertEqual("DOC.3", g125["block"])
        self.assertEqual("R1", g125["functional_revision"])
        self.assertEqual(
            "0.1.25.01-beta",
            g125["revision_aware"],
        )

        releases = (
            ROOT / "RELEASES.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "v0.1.24.13-beta",
            releases,
        )
        self.assertIn(
            "v0.1.25.01-beta",
            releases,
        )

        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "G125/E01",
            matrix,
        )
        self.assertIn(
            "PLAN.2 R2",
            matrix,
        )
        self.assertIn(
            "G126",
            matrix,
        )
        self.assertNotIn(
            "Cerrado/aceptado/publicado G124/E13",
            matrix,
        )

if __name__ == "__main__":
    unittest.main()
