"""Regresiones de PLAN.2 R1 después de su promoción G114/E01."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestPLAN2R1MasterPendingMatrix(unittest.TestCase):
    def test_plan2_materializa_g114_y_doc1_r4_es_candidato(self):
        self.assertEqual(
            "0.1.14.01-beta",
            (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        )
        ledger = cargar_ledger()
        self.assertEqual(114, ledger["accepted_count"])
        self.assertEqual(115, ledger["next_global"])
        self.assertEqual("0.1.15.04-beta", ledger["next_candidate"])
        self.assertEqual("DOC.1", ledger["next_candidate_block"])
        entry = ledger["entries"][-1]
        self.assertEqual(114, entry["global_revision"])
        self.assertEqual("PLAN.2", entry["block"])
        self.assertEqual(1, entry["ordinal"])
        self.assertIn("PR #94", entry["evidence"])

    def test_registro_cierra_plan2_y_reabre_doc1_r4(self):
        data = json.loads(
            (ROOT / "data/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertEqual("closed", ids["PLAN.2"]["status"])
        self.assertIn("G114", ids["PLAN.2"]["global_refs"])
        self.assertEqual("planned_reserved", ids["UX.5"]["status"])

        candidate = data["current_candidate"]
        self.assertEqual("DOC.1", candidate["block"])
        self.assertEqual("R4", candidate["revision"])
        self.assertEqual(115, candidate["global_revision"])
        self.assertEqual(4, candidate["edition"])
        self.assertEqual("reserved_not_accepted", candidate["state"])

    def test_matriz_contiene_frentes_obligatorios(self):
        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")
        for token in (
            "PLAN.2 R1",
            "DOC.1 R4",
            "REL.GOV.1 R2",
            "DEV.2 R5",
            "DEV.2 R6",
            "UX.5 R1",
            "UX.5 R6",
            "PERSIST.1 R1",
            "REP.1 R1",
            "SEC.2 R7",
            "A11Y.2",
            "REV.1",
            "DOC.1 R5",
            "QA.1",
            "REL.1",
            "1.0.0.0",
        ):
            with self.subTest(token=token):
                self.assertIn(token, matrix)
        self.assertIn("Cerrado/aceptado G114/E01", matrix)
        self.assertIn("Candidato G115/E04", matrix)

    def test_matriz_documenta_developer_y_modalidades(self):
        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")
        for token in (
            "/dev/login",
            "/dev/centro-desarrollo",
            "Authorization: Bearer <token>",
            "Manual",
            "Asistida",
        ):
            with self.subTest(token=token):
                self.assertIn(token, matrix)

    def test_limitaciones_vivas_reflejan_estado_actual(self):
        text = (
            ROOT / "docs/product/known-limitations.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("cierre de SEC.2", text)
        self.assertIn("SEC.2 R1–R6 ya está cerrado", text)
        self.assertIn("`0.GG.RR.EE-beta`", text)
        self.assertIn("0.1.14.01-beta", text)

    def test_publicacion_g113_permanece_preservada(self):
        for rel in (
            "README.md",
            "SECURITY.md",
            "VERSIONING.md",
            "RELEASES.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertIn("v0.1.13.03-beta", text)
                self.assertIn("PLAN.2", text)

    def test_matriz_y_auditoria_estan_indexadas(self):
        index = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        self.assertIn(
            "governance/pre-1-0-pending-matrix.md",
            index,
        )
        self.assertIn(
            "audits/documentation/"
            "post-g113-live-documentation-audit-plan2-r1.md",
            index,
        )


if __name__ == "__main__":
    unittest.main()
