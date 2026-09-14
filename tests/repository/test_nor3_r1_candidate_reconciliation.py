'Regresiones NOR.3 R1 y continuidad post-promoción G122/E01.'

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger


ROOT = Path(__file__).resolve().parents[2]


class TestNOR3R1CandidateReconciliation(unittest.TestCase):
    def test_version_material_promueve_g122(self):
        version = (ROOT / "VERSION").read_text(
            encoding="utf-8"
        ).strip()
        self.assertEqual("0.1.23.01-beta", version)

        ledger = cargar_ledger()
        self.assertEqual(123, ledger["accepted_count"])
        self.assertEqual(
            "0.1.22.01-beta",
            next(x for x in ledger["entries"] if x["global_revision"] == 122)["revision_aware"],
        )

    def test_g123_disponible_sin_candidato_preasignado(self):
        ledger = cargar_ledger()
        self.assertEqual(124, ledger["next_global"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])

    def test_registry_separa_nor3_cerrado_de_persist1(self):
        registry = json.loads(
            (
                ROOT / "data/governance/work-block-registry.json"
            ).read_text(encoding="utf-8")
        )
        ids = {
            item["identifier"]: item
            for item in registry["identifiers"]
        }

        self.assertEqual("closed", ids["NOR.3"]["status"])
        self.assertEqual(["G122"], ids["NOR.3"]["global_refs"])
        self.assertEqual("planned_reserved", ids["PERSIST.1"]["status"])
        self.assertEqual([], ids["PERSIST.1"]["global_refs"])

        candidate = registry["current_candidate"]
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertIsNone(candidate["block"])
        self.assertIsNone(candidate["revision"])
        self.assertIsNone(candidate["revision_scope"])
        self.assertEqual(
            "unassigned_pending_replanning",
            candidate["state"],
        )
        self.assertEqual(155, candidate["planning_issue"])

    def test_manifest_actual_materializa_nor3(self):
        manifest = json.loads(
            (
                ROOT / "data/governance/release-publication-manifest.json"
            ).read_text(encoding="utf-8")
        )

        self.assertEqual("0.1.23.01-beta", manifest["version"])
        self.assertEqual("MANT.2", manifest["block"])
        self.assertEqual("R1", manifest["revision"])

        next_step = manifest["next_step"]
        self.assertEqual(124, next_step["global_revision"])
        self.assertIsNone(next_step["revision_aware"])
        self.assertIsNone(next_step["block"])
        self.assertIn("G124", next_step["description"])
        self.assertIn("#155", next_step["description"])

    def test_matriz_ubica_nor3_antes_de_persist1(self):
        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")

        self.assertLess(
            matrix.index("**UX.6 R1–R8**"),
            matrix.index("**NOR.3 R1–R8**"),
        )
        self.assertLess(
            matrix.index("**NOR.3 R1–R8**"),
            matrix.index("**PERSIST.1 R1**"),
        )
        self.assertIn("G122/E01", matrix)
        self.assertIn("sin Global preasignado", matrix)

    def test_documentacion_viva_declara_nor3_y_g122(self):
        files = (
            "README.md",
            "VERSIONING.md",
            "docs/README.md",
            "docs/governance/master-plan-to-1-0.md",
            "docs/governance/pre-1-0-revision-ledger.md",
            "docs/governance/roadmap.md",
            "docs/operations/release-process.md",
        )

        for rel in files:
            text = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertIn("NOR.3", text)
                self.assertIn("G122", text)

    def test_releases_documenta_promocion_nor3(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("Promoción G122/E01 — NOR.3 R8", releases)
        self.assertIn("PERSIST.1", releases)
        self.assertIn("sin Global preasignado", releases)

    def test_programa_ux_granular_sigue_planificado(self):
        registry = json.loads(
            (
                ROOT / "data/governance/work-block-registry.json"
            ).read_text(encoding="utf-8")
        )
        ids = {
            item["identifier"]: item
            for item in registry["identifiers"]
        }
        self.assertEqual("planned_reserved", ids["UX.7"]["status"])
        self.assertEqual("planned_reserved", ids["UX.8"]["status"])
        self.assertEqual([], ids["UX.7"]["global_refs"])
        self.assertEqual([], ids["UX.8"]["global_refs"])


if __name__ == "__main__":
    unittest.main()
