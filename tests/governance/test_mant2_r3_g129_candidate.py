"""Regresiones de materialización MANT.2 R3 / G129-E03-C0."""

import json
from pathlib import Path
import unittest

from app.core.version import descomponer_version_beta_revision, descomponer_version_beta_revision_v2
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[2]


class TestMANT2R3G129Candidate(unittest.TestCase):
    def test_machine_state_g129(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.129.3.0-beta", version)
        self.assertEqual((129, 3), descomponer_version_beta_revision(version))
        self.assertEqual((129, 3, 0), descomponer_version_beta_revision_v2(version))
        ledger = cargar_ledger()
        self.assertEqual(129, ledger["accepted_count"])
        self.assertEqual(130, ledger["next_global"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])
        entry = ledger["entries"][-1]
        self.assertEqual(
            (129, "MANT.2", 3, "R3", 2, 0, 3, "0.129.3.0-beta"),
            (entry["global_revision"], entry["block"], entry["edition"], entry["functional_revision"], entry["identifier_schema"], entry["correction_ordinal"], entry["maintenance_ordinal"], entry["revision_aware"]),
        )

    def test_registry_y_manifest_g129(self):
        reg = json.loads((ROOT / "data/governance/work-block-registry.json").read_text(encoding="utf-8"))
        self.assertEqual(129, reg["accepted_baseline"]["global_revision"])
        self.assertEqual("MANT.2", reg["accepted_baseline"]["block"])
        self.assertEqual("accepted_pending_integration", reg["current_candidate"]["state"])
        self.assertEqual(129, reg["current_candidate"]["global_revision"])
        self.assertEqual(130, reg["current_candidate"]["next_global_available"])
        ids = {item["identifier"]: item for item in reg["identifiers"]}
        self.assertEqual("accepted_r3_pending_integration", ids["MANT.2"]["status"])
        self.assertEqual(["G123", "G127", "G129"], ids["MANT.2"]["global_refs"])
        man = json.loads((ROOT / "data/governance/release-publication-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual((129, 3, 2, 0, 3, "0.129.3.0-beta", "MANT.2", "R3"), (man["global_revision"], man["edition"], man["identifier_schema"], man["correction_ordinal"], man["maintenance_ordinal"], man["version"], man["block"], man["revision"]))
        self.assertEqual(130, man["next_step"]["global_revision"])
        self.assertIsNone(man["next_step"]["revision_aware"])
        self.assertIsNone(man["next_step"]["block"])


if __name__ == "__main__":
    unittest.main()
