"""Regresiones de gobierno para la transición futura a la versión oficial."""

from pathlib import Path
import re
import unittest

from app.core.config import APP_VERSION


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


class TestPlan1GobiernoVersionadoOficial(unittest.TestCase):
    """Protege ADR-168 y la alineación de gobierno sin cambiar la beta actual."""

    def test_adr_168_es_consecutiva_y_esta_indexada(self):
        texto = (DOCS / "decisions/README.md").read_text(encoding="utf-8")
        ids = [int(x) for x in re.findall(r"(?m)^## ADR-(\d{3})\s+—", texto)]
        indice = [int(x) for x in re.findall(r"(?m)^\| ADR-(\d{3}) \|", texto)]
        self.assertGreaterEqual(ids[-1], 168)
        self.assertEqual(list(range(1, ids[-1] + 1)), ids)
        self.assertEqual(ids, indice)
        self.assertIn("ADR-168", texto)
        self.assertIn(f"ADR indexadas:** {ids[-1]}", texto)

    def test_adr_168_define_version_oficial_y_build_independiente(self):
        texto = (DOCS / "decisions/README.md").read_text(encoding="utf-8")
        for esperado in (
            "## ADR-168 — La etapa `0.0.N-beta`",
            "`1.0.0.0`",
            "MAYOR.MENOR.PARCHE.REVISIÓN",
            "Build 000001",
            "no forma parte de `VERSION`",
            "no se incrementa por cada commit",
            "REL.1",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_adr_168_sustituye_plan_actual_sin_reescribir_historia(self):
        texto = (DOCS / "decisions/README.md").read_text(encoding="utf-8")
        self.assertIn("`0.1.0-beta.1`", texto)
        self.assertIn("queda sustituida como **objetivo vigente**", texto)
        self.assertIn(
            "Las menciones conservadas en releases, cierres, snapshots o regresiones "
            "históricas no se borran",
            texto,
        )


    def test_governance_delega_modelo_beta_y_objetivo_oficial(self):
        governance = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")

        self.assertIn("[Política de versionado](VERSIONING.md)", governance)
        self.assertIn("Beta legacy histórica", versioning)
        self.assertIn("Revision-aware v2 vigente para beta", versioning)
        self.assertIn("1.0.0.0", versioning)
        self.assertIn("MAYOR.MENOR.PARCHE.REVISIÓN", versioning)

        self.assertNotIn("0.GG.RR.EE-beta", governance)
        self.assertNotIn("MAYOR.MENOR.PARCHE.REVISIÓN", governance)


    def test_governance_delega_build_y_versionado_a_sus_autoridades(self):
        governance = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        proceso = (
            DOCS / "operations/release-process.md"
        ).read_text(encoding="utf-8")

        self.assertIn("[Política de versionado](VERSIONING.md)", governance)
        self.assertIn("[Proceso de release]", governance)
        self.assertIn("Build oficial", versioning)
        self.assertIn("seis dígitos decimales", versioning)
        self.assertIn("no forma parte de `VERSION`", versioning)
        self.assertIn("Build es independiente de `VERSION` y del tag", proceso)
        self.assertIn("Hasta entonces no se publica un Build ficticio", proceso)

    def test_changelog_unreleased_registra_plan1_sin_reescribir_hitos(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("### PLAN.1 — alineación hacia la primera versión oficial", texto)
        self.assertIn("R2B1 con **676 pruebas en `OK`**", texto)
        self.assertIn("ADR-168", texto)
        self.assertIn(
            "se mantiene `0.1.0-beta.1` como futura primera beta pública",
            texto,
        )

    def test_validacion_conserva_evidencia_acumulada_plan1(self):
        texto = (DOCS / "operations/validation.md").read_text(encoding="utf-8")
        for esperado in (
            "R1 — política de versionado",
            "**665 pruebas en `OK`**",
            "**670 pruebas en `OK`**",
            "**676 pruebas en `OK`**",
            "cerró con **684 pruebas en `OK`**",
            "cerró con **689 pruebas en `OK`**",
            "cerró con **695 pruebas en `OK`**",
            "cerró con **702 pruebas en `OK`**",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_version_canonica_permanece_sincronizada(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, APP_VERSION)


if __name__ == "__main__":
    unittest.main()
