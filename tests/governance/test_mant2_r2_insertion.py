"""Regresiones de inserción y materialización MANT.2 R2 -> G127/E02."""

from __future__ import annotations
import json
from pathlib import Path
import unittest
from app.core.version import descomponer_version_beta_revision

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "data/governance/work-block-registry.json"
LEDGER = ROOT / "data/governance/pre-1-0-revision-ledger.json"
MANIFEST = ROOT / "data/governance/release-publication-manifest.json"
ROADMAP = ROOT / "docs/governance/roadmap.md"
MASTER = ROOT / "docs/governance/master-plan-to-1-0.md"
MATRIX = ROOT / "docs/governance/pre-1-0-pending-matrix.md"

class TestMANT2R2Insertion(unittest.TestCase):
    def test_g127_e02_materializado_y_g128_libre(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.27.02-beta", version)
        self.assertEqual((127, 2), descomponer_version_beta_revision(version))
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(127, ledger["accepted_count"])
        self.assertEqual(128, ledger["next_global"])
        self.assertEqual(128, ledger["next_global_if_ver2_accepted"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])
        entry = ledger["entries"][-1]
        self.assertEqual((127, "MANT.2", 2, "R2", "0.1.27.02-beta"),
            (entry["global_revision"], entry["block"], entry["ordinal"],
             entry["functional_revision"], entry["revision_aware"]))

    def test_registry_declara_mant2_r2_aceptado_pendiente_publicacion(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        candidate = data["current_candidate"]
        self.assertEqual("unassigned", candidate["state"])
        self.assertIsNone(candidate["global_revision"])
        self.assertEqual(164, candidate["planning_issue"])
        self.assertEqual(128, candidate["next_global_available"])
        active = data["active_phase"]
        self.assertEqual(("MANT.2", "R2", 206, "accepted_pending_publication", 127, "0.1.27.02-beta", 164),
            (active["block"], active["revision"], active["issue"], active["state"],
             active["global_revision"], active["revision_aware"], active["next_phase_issue"]))
        ids = {x["identifier"]: x for x in data["identifiers"]}
        self.assertEqual("accepted_pending_publication_r2", ids["MANT.2"]["status"])
        self.assertEqual(["G123", "G127"], ids["MANT.2"]["global_refs"])

    def test_ledger_deja_g128_libre_y_ver2_como_siguiente_owner(self):
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        a = data["next_candidate_assignment"]
        self.assertEqual(("unassigned", 128, 164, 164),
            (a["state"], a["next_global_available"], a["issue"], a["planning_issue"]))

    def test_manifest_materializa_g127_e02_y_no_preasigna_g128(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(("0.1.27.02-beta", "MANT.2", "R2"),
            (data["version"], data["block"], data["revision"]))
        nxt = data["next_step"]
        self.assertEqual(128, nxt["global_revision"])
        self.assertIsNone(nxt["revision_aware"])
        self.assertIsNone(nxt["block"])
        self.assertIn("G127-E02", nxt["description"])
        self.assertIn("VER.2 R6/#164", nxt["description"])

    def test_arbol_vivo_conserva_mant2_antes_de_ver2(self):
        for path in (ROADMAP, MASTER, MATRIX):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("MANT.2 R2", text)
                self.assertIn("G127/E02", text)
                self.assertLess(text.index("MANT.2 R2"), text.index("VER.2 R6"))

if __name__ == "__main__":
    unittest.main()
