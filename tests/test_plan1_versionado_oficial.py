"""Regresiones de PLAN.1 para la transición futura a versión oficial 1.x."""

from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import version_valida


ROOT = Path(__file__).resolve().parents[1]


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

    def test_plan_maestro_contiene_los_catorce_bloques(self):
        texto = (
            ROOT / "docs" / "governance/master-plan-to-1-0.md"
        ).read_text(encoding="utf-8")
        esperados = (
            "### 1. PLAN.1",
            "### 2. UX.4.6f",
            "### 3. UX.4.6g",
            "### 4. UX.4.6h",
            "### 5. UX.4.6i",
            "### 6. DEV.2",
            "### 7. SEC.2",
            "### 8. DOC.2",
            "### 9. PERSIST.1",
            "### 10. REP.1",
            "### 11. A11Y.2",
            "### 12. REV.1",
            "### 13. QA.1",
            "### 14. REL.1",
        )
        for esperado in esperados:
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)


if __name__ == "__main__":
    unittest.main()
