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
        self.assertEqual("0.129.3.0-beta", version)
        self.assertEqual((129, 3), descomponer_version_beta_revision(version))

        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertEqual(129, ledger["accepted_count"])
        self.assertEqual(130, ledger["next_global"])
        self.assertEqual(2, ledger["schema_version"])
        self.assertNotIn("next_global_if_ver2_accepted", ledger)
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])

        g127 = next(
            item for item in ledger["entries"]
            if item["global_revision"] == 127
        )
        self.assertEqual(
            (127, "MANT.2", 2, "R2", "0.1.27.02-beta"),
            (
                g127["global_revision"],
                g127["block"],
                g127["ordinal"],
                g127["functional_revision"],
                g127["revision_aware"],
            ),
        )

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

    def test_registry_declara_mant2_r2_aceptado_pendiente_publicacion(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        candidate = data["current_candidate"]
        self.assertEqual(
            (
                "accepted_pending_integration",
                129,
                "0.129.3.0-beta",
                "MANT.2",
                "R3",
                211,
                130,
            ),
            (
                candidate["state"],
                candidate["global_revision"],
                candidate["revision_aware"],
                candidate["block"],
                candidate["revision"],
                candidate["planning_issue"],
                candidate["next_global_available"],
            ),
        )

        active = data["active_phase"]
        self.assertEqual(
            (
                "MANT.2",
                "R3",
                211,
                "accepted_pending_integration",
                129,
                "0.129.3.0-beta",
                171,
                128,
                "0.128.2.0-beta",
            ),
            (
                active["block"],
                active["revision"],
                active["issue"],
                active["state"],
                active["global_revision"],
                active["revision_aware"],
                active["next_phase_issue"],
                active["base_global_revision"],
                active["base_revision_aware"],
            ),
        )

        ids = {x["identifier"]: x for x in data["identifiers"]}
        self.assertEqual(
            "accepted_r3_pending_integration",
            ids["MANT.2"]["status"],
        )
        self.assertEqual(
            ["G123", "G127", "G129"],
            ids["MANT.2"]["global_refs"],
        )

    def test_ledger_deja_g128_libre_y_ver2_como_siguiente_owner(self):
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertNotIn("next_candidate_assignment", data)
        self.assertNotIn("active_phase", data)
        self.assertEqual(130, data["next_global"])
        self.assertIsNone(data["next_candidate"])
        self.assertIsNone(data["next_candidate_block"])

    def test_manifest_materializa_g127_e02_y_no_preasigna_g128(self):
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(
            ("0.129.3.0-beta", "MANT.2", "R3"),
            (data["version"], data["block"], data["revision"]),
        )

        nxt = data["next_step"]
        self.assertEqual(130, nxt["global_revision"])
        self.assertIsNone(nxt["revision_aware"])
        self.assertIsNone(nxt["block"])
        for fragment in (
            "G129/E03/C0",
            "MANT.2 R3/#211",
            "G130",
            "DOC.4 R1/#171",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, nxt["description"])

    def test_arbol_vivo_conserva_mant2_antes_de_ver2(self):
        for path in (ROADMAP, MASTER, MATRIX):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("MANT.2 R2", text)
                self.assertIn("G127/E02", text)
                self.assertLess(text.index("MANT.2 R2"), text.index("VER.2 R6"))

if __name__ == "__main__":
    unittest.main()
