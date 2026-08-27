"""Regresiones de la promoción DOC.1 R5 -> G116/E05."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG116PromotionPostMerge(unittest.TestCase):
    def test_version_y_runtime_materializan_g116_e05(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.16.05-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((116, 5), descomponer_version_beta_revision(version))

    def test_ledger_acepta_g116_y_reserva_g117(self):
        ledger = cargar_ledger()
        self.assertEqual(116, ledger["accepted_count"])
        self.assertEqual(117, ledger["next_global"])
        self.assertEqual("0.1.17.02-beta", ledger["next_candidate"])
        self.assertEqual("REL.GOV.1", ledger["next_candidate_block"])
        entry = ledger["entries"][-1]
        self.assertEqual(116, entry["global_revision"])
        self.assertEqual("DOC.1", entry["block"])
        self.assertEqual(5, entry["ordinal"])
        self.assertEqual("0.1.16.05-beta", entry["revision_aware"])
        self.assertIn("PR #101", entry["evidence"])
        self.assertIn("6f4266d", entry["evidence"])

    def test_registro_cierra_r5_y_abre_rel_gov_r2(self):
        data = json.loads(
            (ROOT / "data/work-block-registry.json").read_text(encoding="utf-8")
        )
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertIn("G116", ids["DOC.1"]["global_refs"])
        self.assertEqual("reopened_planned_r6", ids["DOC.1"]["status"])
        candidate = data["current_candidate"]
        self.assertEqual(117, candidate["global_revision"])
        self.assertEqual("0.1.17.02-beta", candidate["revision_aware"])
        self.assertEqual("REL.GOV.1", candidate["block"])
        self.assertEqual("R2", candidate["revision"])
        self.assertEqual(2, candidate["edition"])
        self.assertEqual("reserved_not_accepted", candidate["state"])
        self.assertEqual("DEV.2", candidate["next_functional_block_if_accepted"])

    def test_matriz_declara_g116_cerrado_y_g117_candidato(self):
        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Cerrado/aceptado G116/E05", matrix)
        self.assertIn("Candidato G117/E02", matrix)
        self.assertIn("REL.GOV.1 R2", matrix)

    def test_documentacion_viva_declara_transicion_g116_g117(self):
        for rel in (
            "README.md",
            "GOVERNANCE.md",
            "VERSIONING.md",
            "SECURITY.md",
            "docs/README.md",
            "docs/governance/roadmap.md",
            "docs/governance/master-plan-to-1-0.md",
            "docs/governance/pre-1-0-revision-ledger.md",
            "docs/operations/release-process.md",
        ):
            with self.subTest(rel=rel):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn("G116", text)
                self.assertIn("G117", text)
                self.assertIn("REL.GOV.1 R2", text)


if __name__ == "__main__":
    unittest.main()
