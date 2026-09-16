"""Regresiones de PLAN.1 para la transición futura a versión oficial 1.x."""

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import version_valida


ROOT = Path(__file__).resolve().parents[2]


class TestPlan1VersionadoOficial(unittest.TestCase):
    """Protege el contrato beta actual y la línea oficial futura."""

    def test_version_actual_permanece_valida_y_sincronizada(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, APP_VERSION)
        self.assertTrue(version_valida(version))

    def test_validador_admite_beta_y_version_oficial_de_cuatro_componentes(self):
        validas = (
            "0.0.1-beta",
            "0.0.25-beta",
            "0.0.999-beta",
            "1.0.0.0",
            "1.0.0.1",
            "1.0.1.0",
            "1.1.0.0",
            "2.0.0.0",
        )
        for version in validas:
            with self.subTest(version=version):
                self.assertTrue(version_valida(version))

    def test_validador_rechaza_familias_no_adoptadas(self):
        invalidas = (
            "0.1.0-beta.1",
            "0.1.0",
            "1.0.0",
            "1.0.0-beta",
            "1.0.0.0-beta",
            "v1.0.0.0",
            "Build 000001",
            "1.0.0.0+000001",
        )
        for version in invalidas:
            with self.subTest(version=version):
                self.assertFalse(version_valida(version))

    def test_politica_define_version_oficial_y_build_independiente(self):
        texto = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        for esperado in (
            "1.0.0.0",
            "Build 000001",
            "MAYOR.MENOR.PARCHE.REVISIÓN",
            "seis dígitos",
            "no forma parte del archivo `VERSION`",
            "No reintroducir `0.1.0-beta.1` como objetivo vigente",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_programa_historico_plan1_y_plan_vivo_quedan_separados(self):
        registry = json.loads(
            (
                ROOT
                / "data/governance/"
                "work-block-registry.json"
            ).read_text(encoding="utf-8")
        )

        ids = {
            item["identifier"]
            for item in registry["identifiers"]
        }

        programa_historico = (
            "PLAN.1",
            "UX.4.6f",
            "UX.4.6g",
            "UX.4.6h",
            "UX.4.6i",
            "DEV.2",
            "SEC.2",
            "DOC.2",
            "PERSIST.1",
            "REP.1",
            "A11Y.2",
            "REV.1",
            "QA.1",
            "REL.1",
        )

        for bloque in programa_historico:
            with self.subTest(bloque=bloque):
                self.assertIn(
                    bloque,
                    ids,
                )

        ledger = json.loads(
            (
                ROOT
                / "data/governance/"
                "pre-1-0-revision-ledger.json"
            ).read_text(encoding="utf-8")
        )

        plan1 = [
            item
            for item in ledger["entries"]
            if item["block"] == "PLAN.1"
        ]

        self.assertEqual(
            60,
            max(
                item["global_revision"]
                for item in plan1
            ),
        )

        texto = (
            ROOT
            / "docs/governance/"
            "master-plan-to-1-0.md"
        ).read_text(encoding="utf-8")

        for esperado in (
            "G125/E01",
            "PLAN.2 R2",
            "VER.2 R6",
            "DOC.4 R1",
            "PERSIST.1",
            "REP.1",
            "DEPLOY.1",
            "UX.x final realmente necesario",
            "SEC.2 R7",
            "REL.1",
            "1.0.0.0",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(
                    esperado,
                    texto,
                )

if __name__ == "__main__":
    unittest.main()
