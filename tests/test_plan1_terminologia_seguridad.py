"""Regresiones de PLAN.1 R3A para terminología viva de seguridad y release."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestPlan1TerminologiaSeguridad(unittest.TestCase):
    """Protege la etapa beta actual y la frontera oficial futura."""

    def setUp(self):
        self.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    def test_security_declara_desarrollo_beta_y_version_oficial_futura(self):
        texto = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("**desarrollo beta**", texto)
        self.assertIn("`0.0.N-beta`", texto)
        self.assertIn("`1.0.0.0`", texto)
        self.assertNotIn("desarrollo pre-beta", texto)

    def test_support_no_presenta_el_producto_como_pre_beta(self):
        texto = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
        self.assertIn("**desarrollo beta**", texto)
        self.assertNotIn("desarrollo pre-beta", texto)
        self.assertIn("no ofrece un SLA contractual", texto)

    def test_seguridad_privacidad_distingue_revision_actual_y_base_historica(self):
        texto = (DOCS / "SEGURIDAD_PRIVACIDAD.md").read_text(encoding="utf-8")
        self.assertIn(f"**Versión de aplicación revisada:** `{self.version}`", texto)
        self.assertIn("**Versión base histórica preservada:** `0.0.23-beta`", texto)
        self.assertIn("Pendiente antes de la primera versión oficial", texto)
        self.assertNotIn("Pendiente antes de beta pública de producto", texto)

    def test_evaluacion_terceros_actualiza_gate_sin_borrar_gov15(self):
        texto = (DOCS / "EVALUACION_TERCEROS_DESPLIEGUE.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(f"**Versión de aplicación revisada:** `{self.version}`", texto)
        self.assertIn("**Versión base histórica:** `0.0.23-beta`", texto)
        self.assertIn("GOV.1.5", texto)
        self.assertIn("Antes de la primera versión oficial", texto)
        self.assertIn("PLAN.1 R3A", texto)

    def test_documentos_vivos_r3a_no_usan_beta_publica_como_gate_actual(self):
        for ruta in (
            ROOT / "SECURITY.md",
            ROOT / "SUPPORT.md",
            DOCS / "SEGURIDAD_PRIVACIDAD.md",
        ):
            with self.subTest(ruta=ruta.name):
                texto = ruta.read_text(encoding="utf-8").casefold()
                self.assertNotIn("beta pública", texto)

        evaluacion = (DOCS / "EVALUACION_TERCEROS_DESPLIEGUE.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "la expresión histórica “beta pública” deja de utilizarse como gate futuro vigente",
            evaluacion,
        )

    def test_validacion_conserva_cierre_r3a(self):
        texto = (DOCS / "VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("cerró con **689 pruebas en `OK`**", texto)
        self.assertIn("cerró con **695 pruebas en `OK`**", texto)
        self.assertTrue(self.version)


if __name__ == "__main__":
    unittest.main()
