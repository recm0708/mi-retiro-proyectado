"""Regresiones de NOR.1 R8 para identificadores de bloques."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from app.core.version_ledger import (
    LedgerRevisionError,
    cargar_ledger,
    validar_ledger,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/work-block-registry.json"


class TestNOR1R8WorkBlockIdentifiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_familias_e_identificadores_son_unicos(self):
        families = [item["prefix"] for item in self.data["families"]]
        identifiers = [item["identifier"] for item in self.data["identifiers"]]
        self.assertEqual(len(families), len(set(families)))
        self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_historicos_y_planificados_quedan_reservados(self):
        ids = {item["identifier"]: item for item in self.data["identifiers"]}
        for ident in (
            "UX.2.1", "UX.3", "UX.4.6a", "GOV.1.8",
            "DOC.1", "DOC.2", "AUD.SEC2", "REL.GOV.1",
        ):
            self.assertIn(ident, ids)
            self.assertFalse(ids[ident]["reusable_for_different_scope"])

        for ident in ("PERSIST.1", "REP.1", "A11Y.2", "REV.1", "QA.1", "REL.1"):
            self.assertEqual("planned_reserved", ids[ident]["status"])

    def test_revisiones_y_etiquetas_no_son_familias(self):
        self.assertTrue(
            self.data["rules"]["revision_tokens_are_not_block_identifiers"]
        )
        labels = {
            item["label"]: item
            for item in self.data["historical_ledger_labels"]
        }
        for label in ("LEGACY", "INTEGRIDAD", "POST-GOV"):
            self.assertFalse(labels[label]["reusable_as_family"])

    def test_g112_se_reserva_para_nor1_r8_sin_consumirlo(self):
        ledger = cargar_ledger()
        self.assertEqual(
            "0.1.11.01-beta",
            (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        )
        self.assertEqual(111, ledger["accepted_count"])
        self.assertEqual(112, ledger["next_global"])
        self.assertEqual("0.1.12.07-beta", ledger["next_candidate"])
        self.assertEqual("NOR.1", ledger["next_candidate_block"])

        candidate = self.data["current_candidate"]
        self.assertEqual(112, candidate["global_revision"])
        self.assertEqual("NOR.1", candidate["block"])
        self.assertEqual("R8", candidate["revision"])
        self.assertEqual("reserved_not_accepted", candidate["state"])
        self.assertEqual(
            "PERSIST.1",
            candidate["next_functional_block_if_accepted"],
        )

    def test_candidato_reabierto_continua_ordinal_del_bloque(self):
        ledger = cargar_ledger()
        ordinales_nor1 = [
            entry["ordinal"]
            for entry in ledger["entries"]
            if entry["block"] == "NOR.1"
        ]
        self.assertEqual([1, 2, 3, 4, 5, 6], ordinales_nor1)
        self.assertEqual("0.1.12.07-beta", ledger["next_candidate"])

        invalido = copy.deepcopy(ledger)
        invalido["next_candidate"] = "0.1.12.01-beta"
        with self.assertRaises(LedgerRevisionError):
            validar_ledger(invalido)

    def test_bloque_nuevo_comienza_en_e01(self):
        ledger = cargar_ledger()
        candidato_persist = copy.deepcopy(ledger)
        candidato_persist["next_candidate_block"] = "PERSIST.1"
        candidato_persist["next_candidate"] = "0.1.12.01-beta"
        validar_ledger(candidato_persist)

    def test_politica_y_auditoria_estan_indexadas(self):
        standards = (
            ROOT / "docs/standards/README.md"
        ).read_text(encoding="utf-8")
        docs_index = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        self.assertIn("work-block-identifiers.md", standards)
        self.assertIn("work-block-identifier-audit-nor1-r8.md", docs_index)

    def test_atributos_python_minuscula_no_son_identificadores(self):
        script = (ROOT / "scripts/audit_block_identifiers.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("[A-Z][A-Z0-9]*", script)
        self.assertIn(r"\d+[A-Za-z0-9]*", script)
        self.assertNotIn("DOC.exists", self.data["non_block_tokens"])

    def test_documentacion_viva_declara_reserva_nor1_r8(self):
        for rel in (
            "VERSIONING.md",
            "GOVERNANCE.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "docs/README.md",
            "docs/product/traceability-matrix.md",
            "docs/product/transparency.md",
            "docs/security/privacy-policy.md",
        ):
            content = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertIn("G112", content)
                self.assertIn("NOR.1 R8", content)

    def test_auditor_automatico_queda_limpio(self):
        proc = subprocess.run(
            [sys.executable, "scripts/audit_block_identifiers.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertEqual(0, proc.returncode, proc.stdout + proc.stderr)
        self.assertIn("OK:", proc.stdout)


if __name__ == "__main__":
    unittest.main()
