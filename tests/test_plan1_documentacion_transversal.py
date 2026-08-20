"""Regresiones PLAN.1 R2B1 para documentación transversal y release."""

from pathlib import Path
import unittest

from app.core.config import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestPlan1DocumentacionTransversal(unittest.TestCase):
    """Protege índice, transparencia y release durante la transición a 1.0."""

    def test_indice_enlaza_plan_maestro_y_nuevo_contrato(self):
        texto = (DOCS / "INDICE.md").read_text(encoding="utf-8")
        self.assertIn("PLAN_MAESTRO_HACIA_1_0.md", texto)
        self.assertIn("`0.0.N-beta`", texto)
        self.assertIn("versiones oficiales de cuatro componentes", texto)
        self.assertIn("Build independiente", texto)

    def test_transparencia_declara_beta_actual_y_version_oficial_futura(self):
        texto = (DOCS / "TRANSPARENCIA.md").read_text(encoding="utf-8")
        self.assertIn("**desarrollo beta**", texto)
        self.assertIn("`0.0.N-beta`", texto)
        self.assertIn("`1.0.0.0`", texto)
        self.assertIn("primera versión oficial", texto)

    def test_transparencia_preserva_evidencia_historica_sin_hacerla_objetivo(self):
        texto = (DOCS / "TRANSPARENCIA.md").read_text(encoding="utf-8")
        self.assertIn("no declara completada la primera beta pública de producto", texto)
        self.assertIn("PLAN.1 sustituyó posteriormente esa meta", texto)
        self.assertIn("cierre de UX.4.6e y del alcance funcional UX.4.6f–h", texto)

    def test_proceso_release_deriva_tag_desde_version(self):
        texto = (DOCS / "PROCESO_RELEASE.md").read_text(encoding="utf-8")
        self.assertIn(r'$version = (Get-Content .\VERSION).Trim()', texto)
        self.assertIn('git tag -s "v$version"', texto)
        self.assertIn('git tag -v "v$version"', texto)
        self.assertIn("v1.0.0.0", texto)

    def test_proceso_release_separa_build_de_version(self):
        texto = (DOCS / "PROCESO_RELEASE.md").read_text(encoding="utf-8")
        self.assertIn("`Build` no forma parte de `VERSION` ni del tag", texto)
        self.assertIn("Build 000001", texto)
        self.assertIn("Hasta entonces no se publica un Build ficticio", texto)

    def test_version_canonica_permanece_sincronizada_tras_r2b1(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, APP_VERSION)


if __name__ == "__main__":
    unittest.main()
