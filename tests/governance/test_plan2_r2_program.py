"""Regresiones contractuales de PLAN.2 R2 antes de materializar G126."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger


ROOT = Path(__file__).resolve().parents[2]
ROADMAP = ROOT / "docs/governance/roadmap.md"
MASTER = ROOT / "docs/governance/master-plan-to-1-0.md"
MATRIX = ROOT / "docs/governance/pre-1-0-pending-matrix.md"
REGISTRY = ROOT / "data/governance/work-block-registry.json"


class TestPLAN2R2Program(unittest.TestCase):
    def _planning_text(self) -> str:
        return "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROADMAP, MASTER, MATRIX)
        )

    def test_g126_permanece_libre_durante_planificacion(self):
        self.assertEqual(
            "0.1.25.01-beta",
            (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        )

        ledger = cargar_ledger()
        self.assertEqual(125, max(e["global_revision"] for e in ledger["entries"]))

        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        candidate = registry["current_candidate"]
        self.assertEqual("unassigned", candidate["state"])
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertEqual(155, candidate["planning_issue"])
        self.assertEqual(126, candidate["next_global_available"])

        refs = {
            ref
            for item in registry["identifiers"]
            for ref in item.get("global_refs", [])
        }
        self.assertNotIn("G126", refs)

    def test_grafo_principal_coloca_ux_despues_de_deploy(self):
        text = self._planning_text()
        for token in (
            "VER.2 R6",
            "DOC.4 R1",
            "#142",
            "PERSIST.1",
            "REP.1",
            "DEPLOY.1",
            "UX.7",
            "UX.x final",
            "SEC.2 R7",
            "A11Y.2",
            "REV.1",
            "DOC.1 R6",
            "QA.1",
            "REL.1",
            "1.0.0.0",
        ):
            self.assertIn(token, text)

    def test_baseline_ux_7_a_32_es_granular_y_extensible(self):
        text = self._planning_text()
        for ux in range(7, 33):
            self.assertIn(f"UX.{ux}", text)

        self.assertIn("UX.33+", text)
        self.assertIn("#189", text)
        self.assertIn("UX.x final", text)

    def test_pasos_de_simulacion_tienen_ux_individual(self):
        matrix = MATRIX.read_text(encoding="utf-8")
        expected = {
            "UX.9": "Paso 1",
            "UX.10": "Paso 2",
            "UX.11": "Paso 3",
            "UX.12": "Paso 4",
            "UX.13": "Paso 5",
            "UX.14": "Paso 6",
        }
        for ux, step in expected.items():
            self.assertIn(ux, matrix)
            self.assertIn(step, matrix)

    def test_superficies_developer_conocidas_tienen_owner_ux(self):
        matrix = MATRIX.read_text(encoding="utf-8")
        for token in (
            "inicio de sesión",
            "Diagnóstico",
            "Eventos",
            "Archivos",
            "Mantenimiento",
            "Usuarios/RBAC",
            "Privacidad",
            "Perfil/credenciales web",
            "Acceso técnico",
            "Centro de desarrollo legacy",
        ):
            self.assertIn(token, matrix)

    def test_sec2_depende_del_cierre_real_de_la_ola_ux(self):
        text = self._planning_text()
        self.assertIn("#189 sin drift", text)
        self.assertIn("UX.x final", text)
        self.assertIn("SEC.2 R7", text)

    def test_plan_vivo_no_fija_el_rango_antiguo_ux_7_a_20(self):
        text = self._planning_text()
        self.assertNotIn("UX.7–UX.20", text)


if __name__ == "__main__":
    unittest.main()
