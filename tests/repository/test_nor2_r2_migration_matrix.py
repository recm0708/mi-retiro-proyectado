"""Regresiones de NOR.2 R2 — matriz de decisión de migración."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


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

    def test_r2_preserva_evidencia_y_readme_no_duplica_cierres_historicos(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        matriz_r2 = (
            ROOT
            / "docs"
            / "audits"
            / "repository"
            / "repository-normalization-migration-matrix-nor2-r2.md"
        ).read_text(encoding="utf-8")
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

        self.assertIn("NOR.2 R2", matriz_r2)
        self.assertIn(f"**Versión de desarrollo:** `{version}`", readme)
        self.assertIn("[Estándares del repositorio](docs/standards/README.md)", readme)

        for marcador in (
            "NOR.1:** cerrado",
            "NOR.2 R4:** cerrado",
            "NOR.2 R5:** cerrado",
            "NOR.2 R6:** cerrado",
            "NOR.2 R7:** cerrado",
            "NOR.2 R2:** activo",
            "NOR.2 R3:** activo",
            "DOC.1 R1:** cerrado",
            "v0.0.71.01-beta",
            "tag formal queda pendiente",
        ):
            self.assertNotIn(marcador, readme)

    def test_estandar_estructural_usa_directorios_runtime_actuales(self):
        estructura = (
            ROOT / "docs/standards/repository-structure.md"
        ).read_text(encoding="utf-8")
        for carpeta in ("engines/", "models/", "services/"):
            self.assertIn(carpeta, estructura)
        for carpeta in ("motores/", "modelos/", "servicios/"):
            self.assertNotIn(carpeta, estructura)

    def test_historia_r2_r4_y_programa_vivo_usan_fuentes_correctas(self):
        matriz_r2 = (
            ROOT
            / "docs"
            / "audits"
            / "repository"
            / "repository-normalization-migration-matrix-nor2-r2.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "NOR.2 R2",
            matriz_r2,
        )

        ledger = (
            ROOT
            / "docs"
            / "governance"
            / "pre-1-0-revision-ledger.md"
        ).read_text(encoding="utf-8")

        for esperado in (
            "G095",
            "NOR.2 R2",
            "G097",
            "NOR.2 R4",
        ):
            self.assertIn(
                esperado,
                ledger,
            )

        for ruta in (
            "docs/governance/roadmap.md",
            "docs/governance/master-plan-to-1-0.md",
        ):
            texto = (
                ROOT / ruta
            ).read_text(encoding="utf-8")

            with self.subTest(ruta=ruta):
                self.assertIn(
                    "G129/E03/C0",
                    texto,
                )
                self.assertIn(
                    "DOC.4 R1",
                    texto,
                )
                self.assertIn(
                    "G130",
                    texto,
                )
                self.assertNotIn(
                    "G125/E01",
                    texto,
                )
                self.assertNotIn(
                    "PLAN.2 R2",
                    texto,
                )
    def test_version_no_cambia(self):
        from app.core.version import APP_VERSION
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(APP_VERSION, version)

    def test_aplicador_temporal_no_queda_en_arbol(self):
        self.assertFalse((ROOT / "apply_nor2_r2.py").exists())


if __name__ == "__main__":
    unittest.main()
