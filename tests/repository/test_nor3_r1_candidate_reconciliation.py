'Regresiones NOR.3 R1 y continuidad post-promoción G122/E01.'

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger


ROOT = Path(__file__).resolve().parents[2]


class TestNOR3R1CandidateReconciliation(unittest.TestCase):
    def test_version_actual_preserva_promocion_historica_g122(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.129.3.0-beta", version)
        ledger = cargar_ledger()
        self.assertEqual(129, ledger["accepted_count"])
        entry = next(x for x in ledger["entries"] if x["global_revision"] == 122)
        self.assertEqual("0.1.22.01-beta", entry["revision_aware"])
        self.assertEqual("NOR.3", entry["block"])


    def test_g130_disponible_sin_candidato_preasignado(self):
        ledger = cargar_ledger()
        self.assertEqual(130, ledger["next_global"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])


    def test_registry_separa_nor3_cerrado_de_doc4_activo_y_persist1(self):
        registry = json.loads(
            (ROOT / "data/governance/work-block-registry.json")
            .read_text(encoding="utf-8")
        )
        ids = {
            item["identifier"]: item
            for item in registry["identifiers"]
        }

        self.assertEqual("closed", ids["NOR.3"]["status"])
        self.assertEqual(["G122"], ids["NOR.3"]["global_refs"])
        self.assertEqual("in_progress", ids["DOC.4"]["status"])
        self.assertEqual([], ids["DOC.4"]["global_refs"])
        self.assertEqual("planned_reserved", ids["PERSIST.1"]["status"])

        candidate = registry["current_candidate"]
        self.assertEqual("unassigned", candidate["state"])
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertIsNone(candidate["block"])
        self.assertIsNone(candidate["revision"])
        self.assertIsNone(candidate["planning_issue"])
        self.assertEqual(130, candidate["next_global_available"])

        active = registry["active_phase"]
        self.assertEqual("DOC.4", active["block"])
        self.assertEqual("R1", active["revision"])
        self.assertEqual(171, active["issue"])
        self.assertEqual(129, active["base_global_revision"])


    def test_manifest_materializa_g129_publicado_y_siguiente_global_libre(self):
        manifest = json.loads(
            (ROOT / "data/governance/release-publication-manifest.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual("0.129.3.0-beta", manifest["version"])
        self.assertEqual("MANT.2", manifest["block"])
        self.assertEqual("R3", manifest["revision"])

        next_step = manifest["next_step"]
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


    def test_historia_nor3_y_programa_vivo_quedan_separados(self):
        ledger = cargar_ledger()
        g122 = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 122
        )
        self.assertEqual("NOR.3", g122["block"])
        self.assertEqual("0.1.22.01-beta", g122["revision_aware"])

        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("Promoción G122/E01 — NOR.3 R8", releases)

        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")
        graph_start = matrix.index("## 3. Grafo canónico")
        graph_end = matrix.index("## 4. Pendientes obligatorios pre-1.0")
        graph = matrix[graph_start:graph_end]

        self.assertLess(graph.index("DOC.4 R1"), graph.index("#142 auditoría previsional"))
        self.assertLess(graph.index("#142 auditoría previsional"), graph.index("PERSIST.1"))
        self.assertLess(graph.index("PERSIST.1"), graph.index("REP.1"))
        self.assertLess(graph.index("REP.1"), graph.index("DEPLOY.1"))
        self.assertLess(graph.index("DEPLOY.1"), graph.index("UX.7"))

        for historical in (
            "G126/E01",
            "PLAN.2 R2",
            "MANT.2 R2",
            "VER.2 R6",
            "**UX.6 R1–R8**",
            "**NOR.3 R1–R8**",
        ):
            self.assertNotIn(historical, graph)


    def test_nor3_historico_y_estado_vivo_tienen_owners_distintos(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("**Versión de desarrollo:** `0.129.3.0-beta`", readme)
        self.assertNotIn("G122/E01", readme)
        self.assertNotIn("G126", readme)
        self.assertNotIn("G127/E02", readme)

        for rel in (
            "docs/governance/master-plan-to-1-0.md",
            "docs/governance/roadmap.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertIn("G129/E03/C0", text)
                self.assertIn("DOC.4 R1", text)
                self.assertNotIn("G127/E02", text)

        historical_sources = (
            "CHANGELOG.md",
            "RELEASES.md",
            "VERSIONING.md",
            "docs/governance/pre-1-0-revision-ledger.md",
        )
        corpus = "\n".join(
            (ROOT / rel).read_text(encoding="utf-8")
            for rel in historical_sources
        )
        self.assertIn("NOR.3", corpus)
        self.assertIn("G122/E01", corpus)
        self.assertIn("0.1.22.01-beta", corpus)

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
