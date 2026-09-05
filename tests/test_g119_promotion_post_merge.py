"""Regresiones de promoción DEV.2 R6 -> G119/E05."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG119PromotionPostMerge(unittest.TestCase):
    def test_version_y_runtime_materializan_g119_e05(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.19.05-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual(
            (119, 5),
            descomponer_version_beta_revision(version),
        )

    def test_ledger_acepta_g119_y_reserva_g120_e01(self):
        ledger = cargar_ledger()
        self.assertEqual(119, ledger["accepted_count"])
        self.assertEqual(120, ledger["next_global"])
        self.assertEqual("0.1.20.01-beta", ledger["next_candidate"])
        self.assertEqual("UX.5", ledger["next_candidate_block"])

        entry = ledger["entries"][-1]
        self.assertEqual(119, entry["global_revision"])
        self.assertEqual("DEV.2", entry["block"])
        self.assertEqual(5, entry["ordinal"])
        self.assertEqual("R6", entry["functional_revision"])
        self.assertEqual("0.1.19.05-beta", entry["revision_aware"])
        self.assertIn("PR #111", entry["evidence"])
        self.assertIn("bd2accb", entry["evidence"])

    def test_registro_cierra_dev2_y_mantiene_candidato_ux5(self):
        data = json.loads(
            (ROOT / "data/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        ids = {
            item["identifier"]: item
            for item in data["identifiers"]
        }

        self.assertEqual("closed", ids["DEV.2"]["status"])
        self.assertIn("G119", ids["DEV.2"]["global_refs"])

        candidate = data["current_candidate"]
        self.assertEqual(120, candidate["global_revision"])
        self.assertEqual("0.1.20.01-beta", candidate["revision_aware"])
        self.assertEqual("UX.5", candidate["block"])
        self.assertEqual("R6", candidate["revision"])
        self.assertEqual(1, candidate["edition"])
        self.assertEqual(
            "reserved_not_accepted",
            candidate["state"],
        )

    def test_manifiesto_materializa_r6_y_apunta_a_ux5(self):
        data = json.loads(
            (ROOT / "data/release-publication-manifest.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("0.1.19.05-beta", data["version"])
        self.assertEqual("DEV.2", data["block"])
        self.assertEqual("R6", data["revision"])
        self.assertEqual(
            120,
            data["next_step"]["global_revision"],
        )
        self.assertEqual(
            "0.1.20.01-beta",
            data["next_step"]["revision_aware"],
        )
        self.assertEqual("UX.5", data["next_step"]["block"])

    def test_documentacion_viva_declara_g119_y_g120(self):
        for rel in (
            "README.md",
            "GOVERNANCE.md",
            "VERSIONING.md",
            "SECURITY.md",
            "docs/README.md",
            "docs/governance/roadmap.md",
            "docs/governance/master-plan-to-1-0.md",
            "docs/governance/pre-1-0-pending-matrix.md",
            "docs/governance/pre-1-0-revision-ledger.md",
            "docs/operations/release-process.md",
            "docs/architecture/development-center.md",
        ):
            with self.subTest(rel=rel):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn("G119", text)
                self.assertIn("G120", text)
                self.assertIn("UX.5", text)

    def test_trazabilidad_acepta_dev2_r6(self):
        text = (
            ROOT / "docs/product/traceability-matrix.md"
        ).read_text(encoding="utf-8")
        self.assertIn("TR-030", text)
        self.assertIn("G119/E05", text)
        self.assertIn("PR #111", text)


if __name__ == "__main__":
    unittest.main()
