"""Regresiones de NOR.2 R2 — matriz de decisión de migración."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestNOR2R2MigrationMatrix(unittest.TestCase):

    def test_matriz_existe_y_define_categorias(self):
        ruta = (
            ROOT
            / "docs"
            / "audits"
            / "repository"
            / "repository-normalization-migration-matrix-nor2-r2.md"
        )
        self.assertTrue(ruta.exists())
        texto = ruta.read_text(encoding="utf-8")
        for valor in (
            "MIGRAR",
            "CONSERVAR COMO EXCEPCIÓN",
            "CONSOLIDAR",
            "ARCHIVAR",
            "MIGRAR LOCAL",
        ):
            self.assertIn(valor, texto)

    def test_matriz_cubre_hallazgos_clave(self):
        texto = (
            ROOT
            / "docs"
            / "audits"
            / "repository"
            / "repository-normalization-migration-matrix-nor2-r2.md"
        ).read_text(encoding="utf-8")
        for valor in (
            "79",
            "28",
            "data/revision_ledger_pre_1_0.json",
            "regulations/general-parameters.json",
            "assets/",
            "_entregas/",
            "README.md",
        ):
            self.assertIn(valor, texto)

    def test_r2_preserva_evidencia_y_readme_declara_estado_actual(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        matriz_r2 = (
            ROOT
            / "docs"
            / "audits"
            / "repository"
            / "repository-normalization-migration-matrix-nor2-r2.md"
        ).read_text(encoding="utf-8")

        self.assertIn("NOR.2 R2", matriz_r2)
        self.assertIn("NOR.1:** cerrado", readme)
        self.assertIn("NOR.2 R4:** cerrado", readme)
        self.assertIn("NOR.2 R5:** cerrado", readme)
        self.assertIn("NOR.2 R6:** cerrado", readme)
        self.assertIn("NOR.2 R7:** activo", readme)
        self.assertNotIn("NOR.2 R2:** activo", readme)
        self.assertNotIn("NOR.2 R3:** activo", readme)
        self.assertIn("DOC.1 R1:** cerrado", readme)
        self.assertIn("v0.0.71.01-beta", readme)
        self.assertNotIn("Bloque documental activo:** DOC.1 R1", readme)
        self.assertNotIn(
            "tag formal `v0.0.71.01-beta` queda pendiente",
            readme,
        )
        self.assertNotIn("tag formal queda pendiente", readme)
        self.assertNotIn(
            "queda reservado para el cierre firmado post-merge",
            readme,
        )

    def test_readme_usa_directorios_runtime_actuales(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for carpeta in ("engines/", "models/", "services/"):
            self.assertIn(carpeta, readme)
        for carpeta in ("motores/", "modelos/", "servicios/"):
            self.assertNotIn(carpeta, readme)

    def test_documentacion_transversal_registra_r2(self):
        matriz_r2 = (
            ROOT
            / "docs"
            / "audits"
            / "repository"
            / "repository-normalization-migration-matrix-nor2-r2.md"
        ).read_text(encoding="utf-8")

        self.assertIn("NOR.2 R2", matriz_r2)

        for ruta in (
            "CHANGELOG.md",
            "README.md",
            "docs/README.md",
            "docs/governance/roadmap.md",
            "docs/operations/validation.md",
            "docs/governance/master-plan-to-1-0.md",
        ):
            texto = (ROOT / ruta).read_text(encoding="utf-8")
            self.assertIn("NOR.2 R4", texto, ruta)

    def test_version_no_cambia(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.0.71.01-beta", version)

    def test_aplicador_temporal_no_queda_en_arbol(self):
        self.assertFalse((ROOT / "apply_nor2_r2.py").exists())


if __name__ == "__main__":
    unittest.main()
