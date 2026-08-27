"""Regresiones históricas y contractuales de PLAN.2 R1."""
from __future__ import annotations
import json
from pathlib import Path
import unittest
from app.core.version_ledger import cargar_ledger
ROOT=Path(__file__).resolve().parents[1]
class TestPLAN2R1MasterPendingMatrix(unittest.TestCase):
    def test_plan2_permanece_materializado_como_g114(self):
        ledger=cargar_ledger(); entry=next(e for e in ledger["entries"] if e["global_revision"]==114)
        self.assertEqual("PLAN.2",entry["block"]); self.assertEqual(1,entry["ordinal"]); self.assertEqual("0.1.14.01-beta",entry["revision_aware"]); self.assertIn("PR #94",entry["evidence"])
    def test_registro_preserva_plan2_y_ux5(self):
        data=json.loads((ROOT/"data/work-block-registry.json").read_text(encoding="utf-8")); ids={x["identifier"]:x for x in data["identifiers"]}
        self.assertEqual("closed",ids["PLAN.2"]["status"]); self.assertIn("G114",ids["PLAN.2"]["global_refs"]); self.assertIn("UX.5",ids)
    def test_matriz_contiene_frentes_obligatorios(self):
        matrix=(ROOT/"docs/governance/pre-1-0-pending-matrix.md").read_text(encoding="utf-8")
        for token in ("PLAN.2 R1","DOC.1 R4","REL.GOV.1 R2","DEV.2 R5","DEV.2 R6","UX.5 R1","UX.5 R6","PERSIST.1 R1","REP.1 R1","SEC.2 R7","A11Y.2","REV.1","DOC.1 R5","QA.1","REL.1","1.0.0.0"):
            self.assertIn(token,matrix)
        self.assertIn("Cerrado/aceptado G114/E01",matrix); self.assertIn("Cerrado/aceptado G115/E04",matrix)
    def test_matriz_documenta_developer_y_modalidades(self):
        matrix=(ROOT/"docs/governance/pre-1-0-pending-matrix.md").read_text(encoding="utf-8")
        for token in ("/dev/login","/dev/centro-desarrollo","Authorization: Bearer <token>","Manual","Asistida"): self.assertIn(token,matrix)
    def test_limitaciones_vivas_reflejan_version_canonica(self):
        text=(ROOT/"docs/product/known-limitations.md").read_text(encoding="utf-8"); version=(ROOT/"VERSION").read_text(encoding="utf-8").strip()
        self.assertNotIn("cierre de SEC.2",text); self.assertIn("SEC.2 R1–R6 ya está cerrado",text); self.assertIn("`0.GG.RR.EE-beta`",text); self.assertIn(version,text)
    def test_publicacion_g113_permanece_preservada_sin_fijarla_en_todo_documento_vivo(self):
        ledger=cargar_ledger()
        entry=next(e for e in ledger["entries"] if e["global_revision"]==113)
        self.assertEqual("DOC.1",entry["block"])
        self.assertEqual("0.1.13.03-beta",entry["revision_aware"])
        releases=(ROOT/"RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("v0.1.13.03-beta",releases)
        self.assertIn("PLAN.2",releases)
    def test_matriz_y_auditoria_estan_indexadas(self):
        index=(ROOT/"docs/README.md").read_text(encoding="utf-8"); self.assertIn("governance/pre-1-0-pending-matrix.md",index); self.assertIn("audits/documentation/post-g113-live-documentation-audit-plan2-r1.md",index)
if __name__ == "__main__": unittest.main()
