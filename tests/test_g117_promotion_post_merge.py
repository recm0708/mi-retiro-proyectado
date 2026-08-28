"""Regresiones de la promoción REL.GOV.1 R2 -> G117/E02."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG117PromotionPostMerge(unittest.TestCase):
    def test_version_y_runtime_materializan_g117_e02(self):
        version = (ROOT / "VERSION").read_text(
            encoding="utf-8"
        ).strip()
        self.assertEqual("0.1.17.02-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual(
            (117, 2),
            descomponer_version_beta_revision(version),
        )

    def test_ledger_acepta_g117_y_reserva_g118(self):
        ledger = cargar_ledger()
        self.assertEqual(117, ledger["accepted_count"])
        self.assertEqual(118, ledger["next_global"])
        self.assertEqual(
            "0.1.18.04-beta",
            ledger["next_candidate"],
        )
        self.assertEqual(
            "DEV.2",
            ledger["next_candidate_block"],
        )
        entry = ledger["entries"][-1]
        self.assertEqual(117, entry["global_revision"])
        self.assertEqual("REL.GOV.1", entry["block"])
        self.assertEqual(2, entry["ordinal"])
        self.assertEqual(
            "0.1.17.02-beta",
            entry["revision_aware"],
        )
        self.assertIn("PR #103", entry["evidence"])
        self.assertIn("46c464e", entry["evidence"])

    def test_registro_cierra_rel_gov_y_abre_dev2_r5(self):
        data = json.loads(
            (ROOT / "data/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertIn(
            "G117",
            ids["REL.GOV.1"]["global_refs"],
        )
        self.assertEqual(
            "closed",
            ids["REL.GOV.1"]["status"],
        )
        self.assertEqual(
            "reopened_candidate_r5",
            ids["DEV.2"]["status"],
        )
        candidate = data["current_candidate"]
        self.assertEqual(118, candidate["global_revision"])
        self.assertEqual(
            "0.1.18.04-beta",
            candidate["revision_aware"],
        )
        self.assertEqual("DEV.2", candidate["block"])
        self.assertEqual("R5", candidate["revision"])
        self.assertEqual(4, candidate["edition"])
        self.assertEqual(
            "reserved_not_accepted",
            candidate["state"],
        )

    def test_matriz_declara_g117_cerrado_y_g118_candidato(self):
        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Cerrado/aceptado G117/E02", matrix)
        self.assertIn("Candidato G118/E04", matrix)
        self.assertIn("DEV.2 R5", matrix)

    def test_documentacion_viva_declara_transicion(self):
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
                self.assertIn("G117", text)
                self.assertIn("G118", text)
                self.assertIn("DEV.2 R5", text)

        manifest = (
            ROOT / "data/release-publication-manifest.json"
        ).read_text(encoding="utf-8")
        self.assertIn("1161 tests `unittest` OK", manifest)
        self.assertIn("1201 passed / 5721 subtests passed", manifest)


if __name__ == "__main__":
    unittest.main()
