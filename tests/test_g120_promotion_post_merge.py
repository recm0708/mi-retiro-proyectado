"""Regresiones de promoción UX.5 R6 -> G120/E01."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger


ROOT = Path(__file__).resolve().parents[1]


class TestG120PromotionPostMerge(unittest.TestCase):
    def test_version_materializa_g120_e01(self):
        version = (
            ROOT / "VERSION"
        ).read_text(
            encoding="utf-8"
        ).strip()

        self.assertEqual(
            "0.1.20.01-beta",
            version,
        )
        self.assertEqual(
            version,
            APP_VERSION,
        )
        self.assertEqual(
            (120, 1),
            descomponer_version_beta_revision(version),
        )

    def test_ledger_acepta_g120_y_reserva_g121(self):
        ledger = cargar_ledger()

        self.assertEqual(
            120,
            ledger["accepted_count"],
        )
        self.assertEqual(
            121,
            ledger["next_global"],
        )
        self.assertEqual(
            "0.1.21.01-beta",
            ledger["next_candidate"],
        )
        self.assertEqual(
            "UX.6",
            ledger["next_candidate_block"],
        )

        entry = ledger["entries"][-1]

        self.assertEqual(
            120,
            entry["global_revision"],
        )
        self.assertEqual(
            "UX.5",
            entry["block"],
        )
        self.assertEqual(
            1,
            entry["ordinal"],
        )
        self.assertEqual(
            "R6",
            entry["functional_revision"],
        )
        self.assertEqual(
            "0.1.20.01-beta",
            entry["revision_aware"],
        )
        self.assertIn(
            "PR #122",
            entry["evidence"],
        )
        self.assertIn(
            "4c43a816",
            entry["evidence"],
        )

    def test_registro_cierra_ux5_y_reserva_ux6(self):
        data = json.loads(
            (
                ROOT / "data/work-block-registry.json"
            ).read_text(
                encoding="utf-8"
            )
        )

        ids = {
            item["identifier"]: item
            for item in data["identifiers"]
        }

        self.assertEqual(
            "closed",
            ids["UX.5"]["status"],
        )
        self.assertIn(
            "G120",
            ids["UX.5"]["global_refs"],
        )
        self.assertEqual(
            "candidate_r1",
            ids["UX.6"]["status"],
        )

        candidate = data["current_candidate"]

        self.assertEqual(
            121,
            candidate["global_revision"],
        )
        self.assertEqual(
            "0.1.21.01-beta",
            candidate["revision_aware"],
        )
        self.assertEqual(
            "UX.6",
            candidate["block"],
        )
        self.assertEqual(
            "R1",
            candidate["revision"],
        )
        self.assertEqual(
            1,
            candidate["edition"],
        )
        self.assertEqual(
            "reserved_not_accepted",
            candidate["state"],
        )
        self.assertEqual(
            "PERSIST.1",
            candidate[
                "next_functional_block_if_accepted"
            ],
        )

    def test_manifiesto_materializa_ux5_r6(self):
        data = json.loads(
            (
                ROOT
                / "data"
                / "release-publication-manifest.json"
            ).read_text(
                encoding="utf-8"
            )
        )

        self.assertEqual(
            "0.1.20.01-beta",
            data["version"],
        )
        self.assertEqual(
            "UX.5",
            data["block"],
        )
        self.assertEqual(
            "R6",
            data["revision"],
        )
        self.assertEqual(
            121,
            data["next_step"]["global_revision"],
        )
        self.assertEqual(
            "0.1.21.01-beta",
            data["next_step"]["revision_aware"],
        )
        self.assertEqual(
            "UX.6",
            data["next_step"]["block"],
        )

    def test_ux5_r1_r6_consumen_un_solo_estado(self):
        ledger = cargar_ledger()

        entries = [
            item
            for item in ledger["entries"]
            if item["block"] == "UX.5"
        ]

        self.assertEqual(
            1,
            len(entries),
        )
        self.assertEqual(
            1,
            entries[0]["ordinal"],
        )
        self.assertEqual(
            "R6",
            entries[0]["functional_revision"],
        )


if __name__ == "__main__":
    unittest.main()
