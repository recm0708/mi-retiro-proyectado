"""Regresión histórica de promoción NOR.3 R8 -> G122/E01."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "data/governance/work-block-registry.json"
MANIFEST = ROOT / "data/governance/release-publication-manifest.json"
POLICY = ROOT / "data/governance/repository-structure-policy.json"


class TestG122NOR3Promotion(unittest.TestCase):
    def test_version_actual_avanza_sin_reescribir_g122(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.27.02-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((127, 2), descomponer_version_beta_revision(version))
        entry = next(x for x in cargar_ledger()["entries"] if x["global_revision"] == 122)
        self.assertEqual("NOR.3", entry["block"])
        self.assertEqual("0.1.22.01-beta", entry["revision_aware"])

    def test_ledger_preserva_g122_y_estado_actual_g125(self):
        ledger = cargar_ledger()
        self.assertEqual(127, ledger["accepted_count"])
        self.assertEqual(128, ledger["next_global"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])
        entry = next(x for x in ledger["entries"] if x["global_revision"] == 122)
        self.assertEqual(1, entry["ordinal"])
        self.assertEqual("R8", entry["functional_revision"])
        self.assertEqual("0.1.22.01-beta", entry["revision_aware"])

    def test_registry_preserva_nor3_cerrado_y_estado_actual(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertEqual("closed", ids["NOR.3"]["status"])
        self.assertEqual(["G122"], ids["NOR.3"]["global_refs"])
        self.assertEqual("planned_reserved", ids["PERSIST.1"]["status"])
        candidate = data["current_candidate"]
        self.assertEqual("unassigned", candidate["state"])
        self.assertIsNone(candidate["global_revision"])
        self.assertEqual(128, candidate["next_global_available"])
        self.assertEqual(164, candidate["planning_issue"])

    def test_manifest_actual_materializa_mant2_r2(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))

        self.assertEqual("0.1.27.02-beta", data["version"])
        self.assertEqual("MANT.2", data["block"])
        self.assertEqual("R2", data["revision"])

        next_step = data["next_step"]
        self.assertEqual(128, next_step["global_revision"])
        self.assertIsNone(next_step["revision_aware"])
        self.assertIsNone(next_step["block"])

        description = next_step["description"]
        for fragment in (
            "MANT.2 R2/G127-E02",
            "G128",
            "VER.2 R6/#164",
            "#166",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, description)

    def test_policy_conserva_procedencia_r2_y_registra_promocion(self):
        data = json.loads(POLICY.read_text(encoding="utf-8"))
        self.assertEqual("NOR.3 R2", data["phase"])
        closure = data["nor3_closure_contract"]
        self.assertEqual("integrated_accepted_post_merge", closure["candidate_state"])
        self.assertFalse(closure["next_candidate_assigned"])
        self.assertFalse(closure["post_merge_acceptance_required"])
        self.assertEqual("b97cf61763479b80b8e8724b878089e8bb20fa00", closure["merge_commit"])


if __name__ == "__main__":
    unittest.main()
