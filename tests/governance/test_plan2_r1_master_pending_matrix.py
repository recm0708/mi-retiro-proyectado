"""Regresiones históricas de PLAN.2 R1/G114.

PLAN.2 R2 puede reconstruir la matriz viva sin reescribir el estado aceptado
G114. Estas pruebas protegen la historia; el contrato vigente de R2 vive en
``test_plan2_r2_program.py``.
"""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger


ROOT = Path(__file__).resolve().parents[2]


class TestPLAN2R1History(unittest.TestCase):
    def test_plan2_r1_permanece_materializado_como_g114(self):
        ledger = cargar_ledger()
        entry = next(e for e in ledger["entries"] if e["global_revision"] == 114)
        self.assertEqual("PLAN.2", entry["block"])
        self.assertEqual(1, entry["ordinal"])
        self.assertEqual("0.1.14.01-beta", entry["revision_aware"])
        self.assertIn("PR #94", entry["evidence"])

    def test_registry_preserva_referencia_historica_g114(self):
        data = json.loads(
            (ROOT / "data/governance/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertIn("PLAN.2", ids)
        self.assertIn("G114", ids["PLAN.2"]["global_refs"])
        self.assertIn("UX.5", ids)

    def test_publicacion_y_evidencia_historica_siguen_localizables(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("PLAN.2", releases)
        self.assertIn("0.1.14.01-beta", releases)

        audit = ROOT / "docs/audits/documentation/post-g113-live-documentation-audit-plan2-r1.md"
        self.assertTrue(audit.is_file())

    def test_matriz_viva_no_es_fuente_historica_de_r1(self):
        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")
        self.assertIn("PLAN.2 R2", matrix)
        self.assertIn("1.0.0.0", matrix)


if __name__ == "__main__":
    unittest.main()
