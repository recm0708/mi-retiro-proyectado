"""Regresiones de G125 publicado y de la frontera activa PLAN.2 R2."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "data/governance/work-block-registry.json"
LEDGER = ROOT / "data/governance/pre-1-0-revision-ledger.json"
MANIFEST = ROOT / "data/governance/release-publication-manifest.json"


class TestDOC3R1PublishedMachineState(unittest.TestCase):
    def test_registry_preserva_g125_publicado_y_g126_libre(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        ids = {
            item["identifier"]: item
            for item in data["identifiers"]
        }

        self.assertEqual(2, data["schema_version"])

        candidate = data["current_candidate"]
        self.assertEqual("unassigned", candidate["state"])
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertIsNone(candidate["block"])
        self.assertEqual(128, candidate["next_global_available"])
        self.assertEqual(164, candidate["planning_issue"])

        baseline = data["accepted_baseline"]
        self.assertEqual(127, baseline["global_revision"])
        self.assertEqual(2, baseline["edition"])
        self.assertEqual(
            "0.1.27.02-beta",
            baseline["revision_aware"],
        )
        self.assertEqual("MANT.2", baseline["block"])
        self.assertEqual("R2", baseline["functional_revision"])

        active = data["active_phase"]
        self.assertEqual("VER.2", active["block"])
        self.assertEqual("R6", active["revision"])
        self.assertEqual(164, active["issue"])
        self.assertEqual("in_progress", active["state"])
        self.assertIsNone(active["global_revision"])
        self.assertIsNone(active["revision_aware"])
        self.assertEqual(127, active["base_global_revision"])
        self.assertEqual(
            "0.1.27.02-beta",
            active["base_revision_aware"],
        )
        self.assertEqual(171, active["next_phase_issue"])

        doc3 = ids["DOC.3"]
        self.assertEqual("closed", doc3["status"])
        self.assertEqual(["G125"], doc3["global_refs"])
        self.assertEqual("R1", doc3["active_scope"])

        plan2 = ids["PLAN.2"]
        self.assertEqual("closed", plan2["status"])
        self.assertIn("G114", plan2["global_refs"])
        self.assertIn("G126", plan2["global_refs"])

        doc4 = ids["DOC.4"]
        self.assertEqual("planned_reserved", doc4["status"])
        self.assertEqual([], doc4["global_refs"])

    def test_ledger_preserva_g125_y_estado_actual_g127_e02(self):
        data = json.loads(LEDGER.read_text(encoding="utf-8"))

        self.assertEqual(127, data["accepted_count"])
        self.assertEqual(128, data["next_global"])
        self.assertEqual(2, data["schema_version"])
        self.assertNotIn("next_global_if_ver2_accepted", data)
        self.assertNotIn("next_candidate_assignment", data)
        self.assertNotIn("active_phase", data)

        self.assertIsNone(data["next_candidate"])
        self.assertIsNone(data["next_candidate_block"])

        g125 = next(
            item
            for item in data["entries"]
            if item["global_revision"] == 125
        )

        self.assertEqual("DOC.3", g125["block"])
        self.assertEqual("R1", g125["functional_revision"])
        self.assertEqual(
            "0.1.25.01-beta",
            g125["revision_aware"],
        )

        current = data["entries"][-1]

        self.assertEqual(127, current["global_revision"])
        self.assertEqual("MANT.2", current["block"])
        self.assertEqual(2, current["ordinal"])
        self.assertEqual(2, current["edition"])
        self.assertEqual("R2", current["functional_revision"])
        self.assertEqual(
            "0.1.27.02-beta",
            current["revision_aware"],
        )

    def test_manifest_actual_materializa_mant2_r2_y_deja_g128_libre(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual("0.1.27.02-beta", data["version"])
        self.assertEqual("MANT.2", data["block"])
        self.assertEqual("R2", data["revision"])

        next_step = data["next_step"]
        self.assertEqual(128, next_step["global_revision"])
        self.assertIsNone(next_step["revision_aware"])
        self.assertIsNone(next_step["block"])
        self.assertIn("G127-E02", next_step["description"])
        self.assertIn("G128", next_step["description"])
        self.assertIn("VER.2 R6/#164", next_step["description"])



if __name__ == "__main__":
    unittest.main()
