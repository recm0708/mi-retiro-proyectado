"""Regresiones NOR.3 R1 para reconciliación del candidato G122/E01."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger


ROOT = Path(__file__).resolve().parents[2]


class TestNOR3R1CandidateReconciliation(unittest.TestCase):
    def test_version_material_aceptada_permanece_g121(self):
        version = (ROOT / "VERSION").read_text(
            encoding="utf-8"
        ).strip()

        self.assertEqual("0.1.21.01-beta", version)

        ledger = cargar_ledger()
        self.assertEqual(121, ledger["accepted_count"])
        self.assertEqual(
            "0.1.21.01-beta",
            ledger["entries"][-1]["revision_aware"],
        )

    def test_g122_es_candidato_nor3_no_aceptado(self):
        ledger = cargar_ledger()

        self.assertEqual(122, ledger["next_global"])
        self.assertEqual(
            "0.1.22.01-beta",
            ledger["next_candidate"],
        )
        self.assertEqual("NOR.3", ledger["next_candidate_block"])

    def test_registry_separa_nor3_de_persist1(self):
        registry = json.loads(
            (ROOT / "data/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )

        ids = {
            item["identifier"]: item
            for item in registry["identifiers"]
        }

        self.assertIn("NOR.3", ids)
        self.assertEqual("NOR", ids["NOR.3"]["family"])
        self.assertEqual("candidate_r1", ids["NOR.3"]["status"])
        self.assertEqual(
            "planned_reserved",
            ids["PERSIST.1"]["status"],
        )
        self.assertEqual([], ids["PERSIST.1"]["global_refs"])

        candidate = registry["current_candidate"]
        self.assertEqual(122, candidate["global_revision"])
        self.assertEqual(
            "0.1.22.01-beta",
            candidate["revision_aware"],
        )
        self.assertEqual("NOR.3", candidate["block"])
        self.assertEqual("R1", candidate["revision"])
        self.assertEqual(
            "reserved_not_accepted",
            candidate["state"],
        )
        self.assertIsNone(
            candidate["next_functional_block_if_accepted"]
        )
        self.assertIsNone(
            candidate["next_functional_global_if_accepted"]
        )

    def test_manifiesto_apunta_al_mismo_candidato(self):
        manifest = json.loads(
            (
                ROOT / "data/release-publication-manifest.json"
            ).read_text(encoding="utf-8")
        )

        self.assertEqual("0.1.21.01-beta", manifest["version"])
        self.assertEqual("UX.6", manifest["block"])
        self.assertEqual("R8", manifest["revision"])

        next_step = manifest["next_step"]
        self.assertEqual(122, next_step["global_revision"])
        self.assertEqual(
            "0.1.22.01-beta",
            next_step["revision_aware"],
        )
        self.assertEqual("NOR.3", next_step["block"])
        self.assertIn("PERSIST.1", next_step["description"])
        self.assertIn(
            "sin Global preasignado",
            next_step["description"],
        )


    def test_matriz_ubica_nor3_antes_de_persist1(self):
        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")

        ux6 = matrix.index("**UX.6 R1–R8**")
        nor3 = matrix.index("**NOR.3 R1–R8**")
        persist = matrix.index("**PERSIST.1 R1**")

        self.assertLess(ux6, nor3)
        self.assertLess(nor3, persist)
        self.assertIn(
            "NOR.3 R1–R2 — G122/E01",
            matrix,
        )
        self.assertIn(
            "sin Global preasignado",
            matrix,
        )

    def test_documentacion_viva_declara_nor3_como_candidato(self):
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

    def test_releases_preserva_snapshot_y_documenta_reconciliacion(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")

        self.assertIn(
            "PERSIST.1 R1 queda reservado como G122/E01",
            releases,
        )
        self.assertIn(
            "NOR3-R1-CANDIDATE-RECONCILIATION",
            releases,
        )
        self.assertIn(
            "candidato NOR.3 R1",
            releases,
        )


    def test_programa_ux_granular_esta_registrado_sin_iniciarse(self):
        registry = json.loads(
            (ROOT / "data/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )

        ids = {
            item["identifier"]: item
            for item in registry["identifiers"]
        }

        self.assertEqual(
            "planned_reserved",
            ids["UX.7"]["status"],
        )
        self.assertEqual(
            "planned_reserved",
            ids["UX.8"]["status"],
        )
        self.assertIn(
            "Inicio de App Asegurado",
            ids["UX.7"]["meaning"],
        )
        self.assertIn(
            "/dev",
            ids["UX.7"]["meaning"],
        )
        self.assertIn(
            "/simulacion",
            ids["UX.8"]["meaning"],
        )
        self.assertIn(
            "Manual/Asistida",
            ids["UX.8"]["meaning"],
        )
        self.assertEqual([], ids["UX.7"]["global_refs"])
        self.assertEqual([], ids["UX.8"]["global_refs"])


if __name__ == "__main__":
    unittest.main()
