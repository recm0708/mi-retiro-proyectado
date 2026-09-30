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


    def test_registry_preserva_mant2_historico_y_doc4_activo(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))

        candidate = data["current_candidate"]
        self.assertEqual("unassigned", candidate["state"])
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertIsNone(candidate["block"])
        self.assertIsNone(candidate["revision"])
        self.assertIsNone(candidate["planning_issue"])
        self.assertEqual(130, candidate["next_global_available"])

        active = data["active_phase"]
        self.assertEqual("DOC.4", active["block"])
        self.assertEqual("R1", active["revision"])
        self.assertEqual(171, active["issue"])
        self.assertEqual("in_progress", active["state"])
        self.assertIsNone(active["global_revision"])
        self.assertIsNone(active["revision_aware"])
        self.assertEqual(129, active["base_global_revision"])
        self.assertEqual("0.129.3.0-beta", active["base_revision_aware"])

        ids = {x["identifier"]: x for x in data["identifiers"]}
        self.assertEqual("closed_r3_published", ids["MANT.2"]["status"])
        self.assertEqual(
            ["G123", "G127", "G129"],
            ids["MANT.2"]["global_refs"],
        )
        self.assertEqual("in_progress", ids["DOC.4"]["status"])

    def test_ledger_deja_g128_libre_y_ver2_como_siguiente_owner(self):
        data = json.loads(LEDGER.read_text(encoding="utf-8"))
        self.assertNotIn("next_candidate_assignment", data)
        self.assertNotIn("active_phase", data)
        self.assertEqual(130, data["next_global"])
        self.assertIsNone(data["next_candidate"])
        self.assertIsNone(data["next_candidate_block"])


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


    def test_arbol_vivo_refleja_doc4_sobre_g129_publicado(self):
        for path in (ROADMAP, MASTER, MATRIX):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn("G129/E03/C0", text)
                self.assertIn("DOC.4 R1", text)
                self.assertNotIn("MANT.2 R2", text)
                self.assertNotIn("G127/E02", text)
                self.assertNotIn("VER.2 R6", text)

if __name__ == "__main__":
    unittest.main()
