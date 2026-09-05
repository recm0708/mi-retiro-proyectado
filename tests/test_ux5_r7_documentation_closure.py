"""Regresiones del cierre documental de UX.5."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestUX5R7DocumentationClosure(unittest.TestCase):
    def test_promocion_reserva_ux6_g121_e01(self):
        data = json.loads(
            (
                ROOT
                / "data"
                / "work-block-registry.json"
            ).read_text(
                encoding="utf-8"
            )
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

    def test_ux5_cerrado_y_ux6_es_candidato(self):
        data = json.loads(
            (
                ROOT
                / "data"
                / "work-block-registry.json"
            ).read_text(
                encoding="utf-8"
            )
        )

        identifiers = {
            item["identifier"]: item
            for item in data["identifiers"]
        }

        self.assertEqual(
            "closed",
            identifiers["UX.5"]["status"],
        )
        self.assertEqual(
            "candidate_r1",
            identifiers["UX.6"]["status"],
        )
        self.assertEqual(
            [],
            identifiers["UX.6"]["global_refs"],
        )

        candidate = data["current_candidate"]

        self.assertEqual(
            "PERSIST.1",
            candidate[
                "next_functional_block_if_accepted"
            ],
        )
        self.assertIsNone(
            candidate[
                "next_functional_global_if_accepted"
            ]
        )

    def test_matriz_ubica_ux6_antes_de_persistencia(self):
        text = (
            ROOT
            / "docs"
            / "governance"
            / "pre-1-0-pending-matrix.md"
        ).read_text(
            encoding="utf-8"
        )

        ux5 = text.index(
            "**UX.5 R6**"
        )
        ux6 = text.index(
            "**UX.6 R1**"
        )
        persist = text.index(
            "**PERSIST.1 R1**"
        )

        self.assertLess(
            ux5,
            ux6,
        )
        self.assertLess(
            ux6,
            persist,
        )
        self.assertIn(
            "sin Global preasignado",
            text,
        )

    def test_evidencia_de_cierre_existe(self):
        closure = (
            ROOT
            / "docs"
            / "audits"
            / "documentation"
            / "ux5-closure.md"
        )

        self.assertTrue(
            closure.exists()
        )

        text = closure.read_text(
            encoding="utf-8"
        )

        for expected in (
            "G120/E01",
            "UX.5 R6",
            "UX.6",
            "Mi Retiro Seguro",
            "Ficha Digital",
        ):
            with self.subTest(
                expected=expected
            ):
                self.assertIn(
                    expected,
                    text,
                )

    def test_assets_locales_tienen_revision(self):
        main = (
            ROOT
            / "app"
            / "main.py"
        ).read_text(
            encoding="utf-8"
        )

        base = (
            ROOT
            / "app"
            / "templates"
            / "base.html"
        ).read_text(
            encoding="utf-8"
        )

        simulation = (
            ROOT
            / "app"
            / "templates"
            / "simulation.html"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "static_revision=STATIC_REVISION",
            main,
        )
        self.assertIn(
            "?v={{ static_revision }}",
            base,
        )
        self.assertIn(
            "path='/js/simulation_mode.js'",
            simulation,
        )
        self.assertIn(
            "path='/js/assisted_flow.js'",
            simulation,
        )

    def test_version_materializa_g120(self):
        version = (
            ROOT
            / "VERSION"
        ).read_text(
            encoding="utf-8"
        ).strip()

        self.assertEqual(
            "0.1.20.01-beta",
            version,
        )


if __name__ == "__main__":
    unittest.main()
