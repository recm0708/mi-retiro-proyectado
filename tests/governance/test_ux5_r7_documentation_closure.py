"""Regresiones del cierre documental de UX.5."""

from __future__ import annotations
from tests.shared._runtime_http_source import runtime_http_source

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class TestUX5R7DocumentationClosure(unittest.TestCase):
    def test_estado_vigente_conserva_g121_y_candidato_nor3_g122_e01(self):
        data = json.loads(
            (ROOT / "data/governance/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        candidate = data["current_candidate"]
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertIsNone(candidate["block"])
        self.assertIsNone(candidate["revision"])
        self.assertIsNone(candidate["edition"])
        self.assertEqual("unassigned", candidate["state"])

    def test_ux5_y_ux6_cerrados_nor3_candidato_y_persist1_planificado(self):
        data = json.loads(
            (ROOT / "data/governance/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        identifiers = {
            item["identifier"]: item
            for item in data["identifiers"]
        }
        self.assertEqual("closed", identifiers["UX.5"]["status"])
        self.assertIn("G120", identifiers["UX.5"]["global_refs"])
        self.assertEqual("closed", identifiers["UX.6"]["status"])
        self.assertIn("G121", identifiers["UX.6"]["global_refs"])
        self.assertEqual("planned_reserved", identifiers["PERSIST.1"]["status"])
        self.assertEqual("closed", identifiers["NOR.3"]["status"])

        candidate = data["current_candidate"]
        self.assertIsNone(
            candidate["next_functional_block_if_accepted"]
        )
        self.assertIsNone(
            candidate["next_functional_global_if_accepted"]
        )

    def test_historia_ux5_ux6_y_programa_vivo_usan_fuentes_correctas(self):
        registry = json.loads(
            (
                ROOT / "data/governance/work-block-registry.json"
            ).read_text(encoding="utf-8")
        )

        ids = {
            item["identifier"]: item
            for item in registry["identifiers"]
        }

        # Historia materializada.
        self.assertEqual(
            "closed",
            ids["UX.5"]["status"],
        )
        self.assertIn(
            "G120",
            ids["UX.5"]["global_refs"],
        )

        self.assertEqual(
            "closed",
            ids["UX.6"]["status"],
        )
        self.assertIn(
            "G121",
            ids["UX.6"]["global_refs"],
        )

        self.assertEqual(
            "closed",
            ids["NOR.3"]["status"],
        )
        self.assertIn(
            "G122",
            ids["NOR.3"]["global_refs"],
        )

        releases = (
            ROOT / "RELEASES.md"
        ).read_text(encoding="utf-8")

        for tag in (
            "v0.1.20.01-beta",
            "v0.1.21.01-beta",
            "v0.1.22.01-beta",
        ):
            with self.subTest(tag=tag):
                self.assertIn(tag, releases)

        # Programa vivo.
        matrix = (
            ROOT
            / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")

        graph_start = matrix.index(
            "## 2. Grafo canónico"
        )
        graph_end = matrix.index(
            "## 3. Pendientes obligatorios pre-1.0"
        )

        graph = matrix[
            graph_start:graph_end
        ]

        persist = graph.index("PERSIST.1")
        rep = graph.index("REP.1")
        deploy = graph.index("DEPLOY.1")
        ux7 = graph.index("UX.7")

        self.assertLess(persist, rep)
        self.assertLess(rep, deploy)
        self.assertLess(deploy, ux7)

        self.assertIn(
            "PLAN.2 R2",
            graph,
        )
        self.assertIn(
            "UX.x final necesario",
            graph,
        )

        # La matriz viva no duplica cierres históricos.
        self.assertNotIn(
            "Cerrado/aceptado G121/E01",
            matrix,
        )
        self.assertNotIn(
            "Cerrado/aceptado G122/E01",
            matrix,
        )

    def test_evidencia_de_cierre_existe(self):
        closure = (
            ROOT / "docs/audits/documentation/ux5-closure.md"
        )
        self.assertTrue(closure.exists())
        text = closure.read_text(encoding="utf-8")

        for expected in (
            "G120/E01",
            "UX.5 R6",
            "UX.6",
            "Mi Retiro Seguro",
            "Ficha Digital",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, text)

    def test_assets_locales_tienen_revision(self):
        main = runtime_http_source()
        base = (ROOT / "app/templates/asegurado/base.html").read_text(encoding="utf-8")
        simulation = (
            ROOT / "app/templates/asegurado/simulation.html"
        ).read_text(encoding="utf-8")

        self.assertIn("static_revision=STATIC_REVISION", main)
        self.assertIn("?v={{ static_revision }}", base)
        self.assertIn("path='/asegurado/js/simulation_mode.js'", simulation)
        self.assertIn("path='/asegurado/js/assisted_flow.js'", simulation)

    def test_historial_preserva_g121_sin_congelar_version_actual(self):
        data = json.loads((ROOT / "data/governance/work-block-registry.json").read_text(encoding="utf-8"))
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertIn("G121", ids["UX.6"]["global_refs"])
        self.assertEqual("0.1.27.02-beta", (ROOT / "VERSION").read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    unittest.main()
