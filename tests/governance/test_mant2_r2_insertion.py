"""Regresiones de inserción MANT.2 R2 post-G126 antes de VER.2."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "data/governance/work-block-registry.json"
LEDGER = ROOT / "data/governance/pre-1-0-revision-ledger.json"
MANIFEST = ROOT / "data/governance/release-publication-manifest.json"
ROADMAP = ROOT / "docs/governance/roadmap.md"
MASTER = ROOT / "docs/governance/master-plan-to-1-0.md"
MATRIX = ROOT / "docs/governance/pre-1-0-pending-matrix.md"


class TestMANT2R2Insertion(unittest.TestCase):
    def test_g127_permanece_libre_y_version_no_avanza(self):
        self.assertEqual("0.1.26.01-beta", (ROOT / "VERSION").read_text(encoding="utf-8").strip())
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(126, ledger["accepted_count"])
        self.assertEqual(127, ledger["next_global"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])

    def test_registry_declara_mant2_r2_sin_candidato(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        candidate = data["current_candidate"]
        self.assertEqual("unassigned", candidate["state"])
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertIsNone(candidate["block"])
        self.assertEqual(206, candidate["planning_issue"])
        self.assertEqual(127, candidate["next_global_available"])
        active = data["active_phase"]
        self.assertEqual("MANT.2", active["block"])
        self.assertEqual("R2", active["revision"])
        self.assertEqual(206, active["issue"])
        self.assertEqual("in_progress", active["state"])
        self.assertIsNone(active["global_revision"])
        self.assertIsNone(active["revision_aware"])
        self.assertEqual(126, active["base_global_revision"])
        self.assertEqual("0.1.26.01-beta", active["base_revision_aware"])
        self.assertEqual(164, active["next_phase_issue"])
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertEqual("in_progress", ids["MANT.2"]["status"])
        self.assertEqual(["G123"], ids["MANT.2"]["global_refs"])
        self.assertEqual("closed", ids["PLAN.2"]["status"])
        self.assertEqual(["G114", "G126"], ids["PLAN.2"]["global_refs"])

    def test_ledger_apunta_a_issue_206_sin_consumir_g127(self):
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        assignment = data["next_candidate_assignment"]
        self.assertEqual("unassigned", assignment["state"])
        self.assertEqual(127, assignment["next_global_available"])
        self.assertEqual(206, assignment["issue"])
        self.assertEqual(206, assignment["planning_issue"])
        active = data["active_phase"]
        self.assertEqual("MANT.2", active["block"])
        self.assertEqual(206, active["issue"])
        self.assertIsNone(active["global_revision"])

    def test_manifest_sigue_siendo_g126_y_solo_reconcilia_next_step(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual("0.1.26.01-beta", data["version"])
        self.assertEqual("PLAN.2", data["block"])
        self.assertEqual("R2", data["revision"])
        next_step = data["next_step"]
        self.assertEqual(127, next_step["global_revision"])
        self.assertIsNone(next_step["revision_aware"])
        self.assertIsNone(next_step["block"])
        self.assertIn("MANT.2 R2/#206", next_step["description"])
        self.assertIn("VER.2 R6/#164", next_step["description"])

    def test_arbol_vivo_inserta_mant2_antes_de_ver2(self):
        for path in (ROADMAP, MASTER, MATRIX):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("MANT.2 R2", text)
                self.assertIn("#206", text)
                self.assertLess(text.index("MANT.2 R2"), text.index("VER.2 R6"))


if __name__ == "__main__":
    unittest.main()
