"""Regresiones de la línea base de normalización NOR.2."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestNOR2RepositoryNormalization(unittest.TestCase):

    def test_evidencias_r1_existen_en_audits(self):
        base = ROOT / "docs" / "audits" / "repository"
        for nombre in (
            "repository-normalization-baseline-nor2-r1.md",
            "repository-normalization-inventory-nor2-r1.txt",
        ):
            self.assertTrue((base / nombre).exists(), nombre)

    def test_evidencia_declara_auditoria_sin_migracion(self):
        texto = (
            ROOT
            / "docs"
            / "audits"
            / "repository"
            / "repository-normalization-baseline-nor2-r1.md"
        ).read_text(encoding="utf-8")

        self.assertIn("NOR.2 R1", texto)
        self.assertIn("no ejecuta renombres ni movimientos", texto)
        self.assertIn("NOR.2 R2", texto)
        self.assertIn("SEC.2", texto)

    def test_documentacion_transversal_registra_nor2_r1(self):
        evidencia = (
            ROOT
            / "docs"
            / "audits"
            / "repository"
            / "repository-normalization-baseline-nor2-r1.md"
        ).read_text(encoding="utf-8")

        self.assertIn("NOR.2 R1", evidencia)

        for ruta in (
            "CHANGELOG.md",
            "docs/README.md",
            "docs/governance/roadmap.md",
            "docs/operations/validation.md",
            "docs/governance/master-plan-to-1-0.md",
        ):
            texto = (ROOT / ruta).read_text(encoding="utf-8")
            self.assertIn("NOR.2 R4", texto, ruta)

    def test_version_permanece_sin_cambios(self):
        from app.core.version import APP_VERSION
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(APP_VERSION, version)

    def test_aplicador_temporal_no_forma_parte_del_arbol_final(self):
        self.assertFalse((ROOT / "apply_nor2_r1.py").exists())


if __name__ == "__main__":
    unittest.main()
