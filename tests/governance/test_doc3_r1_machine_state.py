"""Regresiones del estado machine-readable de DOC.3 R1 materializado."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "data/governance/work-block-registry.json"
LEDGER = ROOT / "data/governance/pre-1-0-revision-ledger.json"
MANIFEST = ROOT / "data/governance/release-publication-manifest.json"


class TestDOC3R1MachineState(unittest.TestCase):
    def test_registry_materializa_doc3_y_deja_g126_libre(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        ids = {item["identifier"]: item for item in data["identifiers"]}

        candidate = data["current_candidate"]
        self.assertEqual("unassigned", candidate["state"])
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertIsNone(candidate["block"])
        self.assertEqual(126, candidate["next_global_available"])
        self.assertEqual(155, candidate["planning_issue"])

        active = data["active_phase"]
        self.assertEqual("DOC.3", active["block"])
        self.assertEqual("R1", active["revision"])
        self.assertEqual(154, active["issue"])
        self.assertEqual("accepted_pending_publication", active["state"])
        self.assertEqual(125, active["global_revision"])
        self.assertEqual("0.1.25.01-beta", active["revision_aware"])
        self.assertEqual(124, active["base_global_revision"])
        self.assertEqual("0.1.24.13-beta", active["base_revision_aware"])
        self.assertEqual(155, active["next_phase_issue"])

        doc3 = ids["DOC.3"]
        self.assertEqual("accepted_pending_publication", doc3["status"])
        self.assertEqual(["G125"], doc3["global_refs"])
        self.assertEqual("R1", doc3["active_scope"])

        doc4 = ids["DOC.4"]
        self.assertEqual("planned_reserved", doc4["status"])
        self.assertEqual([], doc4["global_refs"])

    def test_ledger_materializa_g125_e01(self):
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(125, data["accepted_count"])
        self.assertEqual(126, data["next_global"])
        self.assertEqual(126, data["next_global_if_ver2_accepted"])
        self.assertIsNone(data["next_candidate"])
        self.assertIsNone(data["next_candidate_block"])

        entry = data["entries"][-1]
        self.assertEqual(125, entry["global_revision"])
        self.assertEqual("DOC.3", entry["block"])
        self.assertEqual(1, entry["ordinal"])
        self.assertEqual("R1", entry["functional_revision"])
        self.assertEqual("0.1.25.01-beta", entry["revision_aware"])

        assignment = data["next_candidate_assignment"]
        self.assertEqual("unassigned", assignment["state"])
        self.assertEqual(126, assignment["next_global_available"])

        active = data["active_phase"]
        self.assertEqual("accepted_pending_publication", active["state"])
        self.assertEqual(125, active["global_revision"])
        self.assertEqual("0.1.25.01-beta", active["revision_aware"])

    def test_manifest_materializa_g125_e01(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual("0.1.25.01-beta", data["version"])
        self.assertEqual("DOC.3", data["block"])
        self.assertEqual("R1", data["revision"])

        next_step = data["next_step"]
        self.assertEqual(126, next_step["global_revision"])
        self.assertIsNone(next_step["revision_aware"])
        self.assertIsNone(next_step["block"])
        self.assertIn("PLAN.2 R2/#155", next_step["description"])


if __name__ == "__main__":
    unittest.main()
