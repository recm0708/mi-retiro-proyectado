"""Regresiones del saneamiento final de metadata viva de PLAN.1 R2."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestPlan1SaneamientoMetadata(unittest.TestCase):
    """Distingue estado vigente y base histórica sin reescribir cierres previos."""

    def setUp(self):
        self.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    def test_observabilidad_declara_revision_actual_y_base_historica(self):
        texto = (DOCS / "OBSERVABILIDAD_LOGS.md").read_text(encoding="utf-8")
        self.assertIn(f"**Versión de aplicación revisada:** `{self.version}`", texto)
        self.assertIn("**Versión base histórica:** `0.0.23-beta`", texto)
        self.assertIn("GOV.1.4 no modificó fórmulas previsionales", texto)
        self.assertIn("DEV.2", texto)

    def test_limitaciones_no_duplica_revision_juridica_y_usa_gate_oficial(self):
        texto = (DOCS / "LIMITACIONES_CONOCIDAS.md").read_text(encoding="utf-8")
        self.assertIn(f"**Versión de aplicación revisada:** `{self.version}`", texto)
        self.assertIn("**Versión base histórica:** `0.0.23-beta`", texto)
        self.assertIn("Pendientes antes de la primera versión oficial", texto)
        self.assertNotIn("Pendientes antes de beta pública", texto)
        bloque = texto.split("## 5. Privacidad y seguridad", 1)[1].split(
            "## 6. Dependencias y red", 1
        )[0]
        self.assertEqual(2, bloque.lower().count("revisión jurídica externa"))

    def test_preparacion_publica_separa_repo_publico_de_version_oficial(self):
        texto = (DOCS / "PREPARACION_PUBLICA_GITHUB.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(f"**Versión de aplicación revisada:** `{self.version}`", texto)
        self.assertIn("**Versión base del checkpoint público:** `0.0.24-beta`", texto)
        self.assertIn("no equivale a declarar una versión oficial", texto)
        self.assertIn("no equivalía a declarar una beta pública", texto)
        self.assertIn("primera versión oficial `1.0.0.0`", texto)

    def test_changelog_registra_r2b2_y_r2c_como_evidencia(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("R2B2 cerró con **684 pruebas en `OK`**", texto)
        self.assertIn("R2C saneó metadata viva", texto)
        self.assertIn("**689 pruebas en `OK`**", texto)

    def test_validacion_registra_r2c_como_evidencia_cerrada(self):
        texto = (DOCS / "VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("cerró con **684 pruebas en `OK`**", texto)
        self.assertIn("cerró con **689 pruebas en `OK`**", texto)
        self.assertNotIn(
            "gate esperado de R2C es **689 pruebas en `OK`**",
            texto,
        )
        self.assertTrue(self.version)


if __name__ == "__main__":
    unittest.main()
