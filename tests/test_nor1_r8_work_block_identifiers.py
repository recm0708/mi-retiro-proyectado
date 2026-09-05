"""Regresiones de NOR.1 R8 para identificadores de bloques."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from app.core.version import construir_version_beta_revision
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

        self.assertEqual("closed", ids["PLAN.2"]["status"])
        self.assertIn("G114", ids["PLAN.2"]["global_refs"])
        self.assertEqual("closed", ids["UX.5"]["status"])
        self.assertEqual("candidate_r1", ids["UX.6"]["status"])

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

    def test_g112_permanece_aceptado_y_ux6_r1_es_candidato_actual(self):
        ledger = cargar_ledger()
        entry = next(
            x for x in ledger["entries"] if x["global_revision"] == 112
        )
        self.assertEqual("NOR.1", entry["block"])
        self.assertEqual(7, entry["ordinal"])
        self.assertEqual("0.1.12.07-beta", entry["revision_aware"])

        candidate = self.data["current_candidate"]
        self.assertEqual(121, candidate["global_revision"])
        self.assertEqual("UX.6", candidate["block"])
        self.assertEqual("R1", candidate["revision"])
        self.assertEqual(1, candidate["edition"])
        self.assertEqual("reserved_not_accepted", candidate["state"])
        self.assertEqual(
            "PERSIST.1",
            candidate["next_functional_block_if_accepted"],
        )
        self.assertIsNone(
            candidate["next_functional_global_if_accepted"]
        )

    def test_candidato_reabierto_continua_ordinal_del_bloque(self):
        ledger = cargar_ledger()
        ordinales = [
            entry["ordinal"]
            for entry in ledger["entries"]
            if entry["block"] == "NOR.1"
        ]
        self.assertEqual([1, 2, 3, 4, 5, 6, 7], ordinales)

        siguiente_global = ledger["next_global"]

        candidato = copy.deepcopy(ledger)
        candidato["next_candidate_block"] = "NOR.1"
        candidato["next_candidate"] = construir_version_beta_revision(
            siguiente_global,
            8,
        )
        validar_ledger(candidato)

        invalido = copy.deepcopy(ledger)
        invalido["next_candidate_block"] = "NOR.1"
        invalido["next_candidate"] = construir_version_beta_revision(
            siguiente_global,
            1,
        )
        with self.assertRaises(LedgerRevisionError):
            validar_ledger(invalido)

    def test_bloque_nuevo_comienza_en_e01(self):
        ledger = cargar_ledger()
        candidato = copy.deepcopy(ledger)
        candidato["next_candidate_block"] = "UX.6"
        candidato["next_candidate"] = construir_version_beta_revision(
            ledger["next_global"],
            1,
        )

        validar_ledger(candidato)

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

    def test_historia_y_planificacion_se_validan_en_fuentes_canonicas(self):
        ledger = cargar_ledger()
        entries = {
            entry["global_revision"]: entry
            for entry in ledger["entries"]
        }

        expected = {
            112: ("NOR.1", 7, "0.1.12.07-beta"),
            113: ("DOC.1", 3, "0.1.13.03-beta"),
            114: ("PLAN.2", 1, "0.1.14.01-beta"),
            115: ("DOC.1", 4, "0.1.15.04-beta"),
        }
        for global_revision, expected_entry in expected.items():
            entry = entries[global_revision]
            with self.subTest(global_revision=global_revision):
                self.assertEqual(expected_entry[0], entry["block"])
                self.assertEqual(expected_entry[1], entry["ordinal"])
                self.assertEqual(
                    expected_entry[2],
                    entry["revision_aware"],
                )

        ids = {
            item["identifier"]: item
            for item in self.data["identifiers"]
        }
        self.assertEqual("closed", ids["NOR.1"]["status"])
        self.assertEqual("closed", ids["PLAN.2"]["status"])
        self.assertEqual(
            "reopened_planned_r6",
            ids["DOC.1"]["status"],
        )
        self.assertEqual(
            "planned_reserved",
            ids["PERSIST.1"]["status"],
        )

        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")
        for fragment in (
            "Cerrado/aceptado G114/E01",
            "DOC.1 R4",
            "PERSIST.1 R1",
            "Cerrado/aceptado G118/E04",
            "DEV.2 R5",
            "Cerrado/aceptado/publicado G119/E05",
            "Cerrado/aceptado G120/E01",
            "Candidato G121/E01",
            "UX.6 R1",
            "DEV.2 R6",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, matrix)

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
