"""Regresiones PLAN.1 R3B1 para licencia, terceros y privacidad viva."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestPlan1LicenciaPrivacidadViva(unittest.TestCase):
    """Alinea documentos vivos sin borrar la base histórica GOV.1."""

    def setUp(self):
        self.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    def test_licencia_distingue_version_actual_y_base_historica(self):
        texto = (DOCS / "governance/licensing-and-distribution.md").read_text(encoding="utf-8")
        self.assertIn(f"**Versión de aplicación revisada:** `{self.version}`", texto)
        self.assertIn("**Versión base histórica preservada:** `0.0.23-beta`", texto)
        self.assertIn("Decisión GOV.1.7", texto)
        self.assertIn("etapa beta", texto)
        self.assertNotIn("El proyecto contempla una beta futura", texto)

    def test_dependencias_actualiza_repo_y_gate_de_bootstrap(self):
        texto = (DOCS / "operations/third-party-dependencies.md").read_text(encoding="utf-8")
        self.assertIn(f"**Versión de aplicación revisada:** `{self.version}`", texto)
        self.assertIn("**Versión base histórica preservada:** `0.0.23-beta`", texto)
        self.assertIn("GitHub aloja el repositorio público", texto)
        self.assertIn("antes de `1.0.0.0`", texto)
        self.assertNotIn("objetivo pre-beta", texto)
        self.assertNotIn("gate pre-beta", texto)

    def test_politica_privacidad_conserva_version_material(self):
        texto = (DOCS / "security/privacy-policy.md").read_text(encoding="utf-8")
        self.assertIn(f"**Versión de aplicación revisada:** `{self.version}`", texto)
        self.assertIn("**Versión base histórica preservada:** `0.0.23-beta`", texto)
        self.assertIn("GOV.1.3 R3", texto)
        self.assertIn("`2026-08-16.1`", texto)
        self.assertIn("primera versión oficial", texto)
        self.assertNotIn("antes de una beta pública", texto)

    def test_terminos_reconocen_procedimiento_existente_y_gate_oficial(self):
        texto = (DOCS / "security/terms-and-privacy.md").read_text(encoding="utf-8")
        self.assertIn(f"**Versión de aplicación revisada:** `{self.version}`", texto)
        self.assertIn("**Versión base histórica preservada:** `0.0.23-beta`", texto)
        self.assertIn("GOV.1.3 R3", texto)
        self.assertIn("data-subject-rights-procedure.md", texto)
        self.assertIn("REV.1", texto)
        self.assertNotIn("Hasta que exista un procedimiento formal pre-beta", texto)

    def test_matriz_ley81_reemplaza_gate_beta_publica(self):
        texto = (DOCS / "regulatory/law-81-compliance.md").read_text(encoding="utf-8")
        self.assertIn(f"**Versión de aplicación revisada:** `{self.version}`", texto)
        self.assertIn("**Versión base histórica preservada:** `0.0.23-beta`", texto)
        self.assertIn("GOV.1.3 R3", texto)
        self.assertIn("Pendiente antes de publicación", texto)
        self.assertIn("## 7. Pendientes obligatorios antes de la primera versión oficial", texto)
        self.assertNotIn("pre-beta pública", texto)

    def test_documentos_r3b1_no_usan_beta_publica_como_gate_vigente(self):
        for nombre in (
            "governance/licensing-and-distribution.md",
            "operations/third-party-dependencies.md",
            "security/privacy-policy.md",
            "security/terms-and-privacy.md",
            "regulatory/law-81-compliance.md",
        ):
            with self.subTest(nombre=nombre):
                texto = (DOCS / nombre).read_text(encoding="utf-8").casefold()
                self.assertNotIn("beta pública", texto)

    def test_validacion_conserva_cierre_r3b1(self):
        texto = (DOCS / "operations/validation.md").read_text(encoding="utf-8")
        self.assertIn("cerró con **695 pruebas en `OK`**", texto)
        self.assertIn("cerró con **702 pruebas en `OK`**", texto)
        self.assertTrue(self.version)


if __name__ == "__main__":
    unittest.main()
