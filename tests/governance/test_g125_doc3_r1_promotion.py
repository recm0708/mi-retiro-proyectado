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
        self.assertEqual("0.129.3.0-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((129, 3), descomponer_version_beta_revision(version))

    def test_ledger_preserva_g125_y_materializa_g127_e02(self):
        ledger = cargar_ledger()
        self.assertEqual(129, ledger["accepted_count"])
        self.assertEqual(130, ledger["next_global"])
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
        self.assertEqual(
            (129, "MANT.2", 3, "R3", "0.129.3.0-beta"),
            (
                current["global_revision"],
                current["block"],
                current["ordinal"],
                current["functional_revision"],
                current["revision_aware"],
            ),
        )


    def test_registry_materializa_doc3_y_expone_doc4_activo(self):
        registry = json.loads(
            (ROOT / "data/governance/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        ids = {item["identifier"]: item for item in registry["identifiers"]}

        self.assertEqual("closed", ids["DOC.3"]["status"])
        self.assertIn("G125", ids["DOC.3"]["global_refs"])
        self.assertEqual("in_progress", ids["DOC.4"]["status"])
        self.assertEqual([], ids["DOC.4"]["global_refs"])

        plan2 = ids["PLAN.2"]
        self.assertEqual("closed", plan2["status"])
        self.assertIn("G114", plan2["global_refs"])
        self.assertIn("G126", plan2["global_refs"])

        candidate = registry["current_candidate"]
        self.assertEqual("unassigned", candidate["state"])
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertIsNone(candidate["block"])
        self.assertEqual(130, candidate["next_global_available"])

        active = registry["active_phase"]
        self.assertEqual("DOC.4", active["block"])
        self.assertEqual("R1", active["revision"])
        self.assertEqual(171, active["issue"])
        self.assertEqual(129, active["base_global_revision"])


    def test_manifest_actual_materializa_g129_y_deja_g130_libre(self):
        data = json.loads(
            (ROOT / "data/governance/release-publication-manifest.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual("0.129.3.0-beta", data["version"])
        self.assertEqual("MANT.2", data["block"])
        self.assertEqual("R3", data["revision"])

        next_step = data["next_step"]
        self.assertEqual(130, next_step["global_revision"])
        self.assertIsNone(next_step["revision_aware"])
        self.assertIsNone(next_step["block"])

        for fragment in (
            "G130",
            "G129/E03/C0",
            "DOC.4 R1/#171",
            "sin candidato",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, next_step["description"])

        self.assertNotIn("pendiente de integración", next_step["description"])
        self.assertNotIn("pendiente de publicación", next_step["description"])

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
