"""Regresión de promoción NOR.3 R8 -> G122/E01."""
from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "data/governance/pre-1-0-revision-ledger.json"
REGISTRY = ROOT / "data/governance/work-block-registry.json"
MANIFEST = ROOT / "data/governance/release-publication-manifest.json"
POLICY = ROOT / "data/governance/repository-structure-policy.json"


class TestG122NOR3Promotion(unittest.TestCase):
    def test_version_materializa_g122_e01(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.23.01-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((123, 1), descomponer_version_beta_revision(version))

    def test_ledger_cierra_g122_y_no_reserva_g123(self):
        ledger = cargar_ledger()
        self.assertEqual(123, ledger["accepted_count"])
        self.assertEqual(124, ledger["next_global"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])
        entry = next(x for x in ledger["entries"] if x["global_revision"] == 122)
        self.assertEqual(122, entry["global_revision"])
        self.assertEqual("NOR.3", entry["block"])
        self.assertEqual(1, entry["ordinal"])
        self.assertEqual("R8", entry["functional_revision"])
        self.assertEqual("0.1.22.01-beta", entry["revision_aware"])

    def test_registry_cierra_nor3_sin_preasignar_bloque(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertEqual("closed", ids["NOR.3"]["status"])
        self.assertEqual(["G122"], ids["NOR.3"]["global_refs"])
        self.assertEqual("planned_reserved", ids["PERSIST.1"]["status"])
        candidate = data["current_candidate"]
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertIsNone(candidate["block"])
        self.assertEqual("unassigned_pending_replanning", candidate["state"])
        self.assertEqual(155, candidate["planning_issue"])

    def test_manifest_publica_nor3_y_no_inventa_candidato(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual("0.1.23.01-beta", data["version"])
        self.assertEqual("MANT.2", data["block"])
        self.assertEqual("R1", data["revision"])
        self.assertEqual(124, data["next_step"]["global_revision"])
        self.assertIsNone(data["next_step"]["revision_aware"])
        self.assertIsNone(data["next_step"]["block"])
        description = data["next_step"]["description"]
        for fragment in (
            "MANT.1 R8", "#163", "#154", "#155",
            "VER.2 R6", "#164", "PERSIST.1",
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
        self.assertEqual(
            "b97cf61763479b80b8e8724b878089e8bb20fa00",
            closure["merge_commit"],
        )


if __name__ == "__main__":
    unittest.main()
