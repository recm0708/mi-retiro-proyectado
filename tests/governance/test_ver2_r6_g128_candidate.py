"""Regresiones de materialización VER.2 R6 / G128-E02-C0."""

# Regresiones de materialización final VER.2 R6 / G128-E02-C0.

import json
from pathlib import Path
import unittest

from app.core.version import descomponer_version_beta_revision, descomponer_version_beta_revision_v2
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[2]

class TestVer2R6G128Candidate(unittest.TestCase):
    def test_machine_state(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.128.2.0-beta", version)
        self.assertEqual((128, 2), descomponer_version_beta_revision(version))
        self.assertEqual((128, 2, 0), descomponer_version_beta_revision_v2(version))
        ledger = cargar_ledger()
        self.assertEqual(128, ledger["accepted_count"])
        self.assertEqual(129, ledger["next_global"])
        e = ledger["entries"][-1]
        self.assertEqual((128, "VER.2", 2, "R6", 2, 0, "0.128.2.0-beta"), (e["global_revision"], e["block"], e["edition"], e["functional_revision"], e["identifier_schema"], e["correction_ordinal"], e["revision_aware"]))

    def test_registry_and_manifest(self):
        reg = json.loads((ROOT / "data/governance/work-block-registry.json").read_text(encoding="utf-8"))
        self.assertEqual(128, reg["accepted_baseline"]["global_revision"])
        self.assertEqual("accepted_pending_integration", reg["current_candidate"]["state"])
        self.assertEqual(129, reg["current_candidate"]["next_global_available"])
        man = json.loads((ROOT / "data/governance/release-publication-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual((128, 2, 2, 0, "0.128.2.0-beta", "VER.2", "R6"), (man["global_revision"], man["edition"], man["identifier_schema"], man["correction_ordinal"], man["version"], man["block"], man["revision"]))
        self.assertEqual(129, man["next_step"]["global_revision"])
