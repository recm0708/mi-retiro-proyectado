"""Regresiones de coherencia documental consolidadas en GOV.1.3 R2."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASE_VERSION = "0.0.23-beta"
R2_DOCS = [
    "architecture/system-architecture.md",
    "architecture/data-model.md",
    "product/simulation-data-management.md",
    "architecture/calculation-engine.md",
    "product/functional-specification.md",
    "operations/development-guide.md",
    "operations/validation.md",
]

R2_SNAPSHOTS = {
    "architecture/system-architecture.md": "ARQUITECTURA_PRE_GOV1_3_R2.md",
    "architecture/data-model.md": "MODELO_DE_DATOS_PRE_GOV1_3_R2.md",
    "product/simulation-data-management.md": "GESTION_DATOS_SIMULACION_PRE_GOV1_3_R2.md",
    "architecture/calculation-engine.md": "MOTOR_DE_CALCULO_PRE_GOV1_3_R2.md",
    "product/functional-specification.md": "ESPECIFICACION_FUNCIONAL_PRE_GOV1_3_R2.md",
    "operations/development-guide.md": "GUIA_INTERNA_DESARROLLO_PRE_GOV1_3_R2.md",
    "operations/validation.md": "VALIDACION_PRE_GOV1_3_R2.md",
}


class TestGov13DocumentacionR2(unittest.TestCase):
    def test_r2_documentos_declaran_estado_y_version_base(self):
        for nombre in R2_DOCS:
            with self.subTest(nombre=nombre):
                texto = (DOCS / nombre).read_text(encoding="utf-8")
                self.assertIn(BASE_VERSION, texto)
                self.assertIn("GOV.1.3 R2", texto)
                self.assertIn("**Estado:**", texto)

    def test_snapshots_tecnicos_existen(self):
        for nombre in R2_DOCS:
            snapshot = DOCS / "archive" / "technical" / R2_SNAPSHOTS[nombre]
            with self.subTest(nombre=nombre):
                self.assertTrue(snapshot.is_file(), str(snapshot))

    def test_arquitectura_documenta_modulos_criticos(self):
        texto = (DOCS / "architecture/system-architecture.md").read_text(encoding="utf-8")
        for esperado in (
            "app/core/pdf_files.py",
            "app/core/version.py",
            "app/services/reference_date.py",
            "app/services/ficha_digital.py",
            "app/services/current_year_detail.py",
            "app/static/js/data_management.js",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_arquitectura_documenta_todas_las_rutas_fastapi(self):
        main = (ROOT / "app/main.py").read_text(encoding="utf-8")
        rutas = {
            ruta
            for _, ruta in re.findall(
                r'@app\.(get|post)\(\s*"([^"]+)"',
                main,
                flags=re.S,
            )
        }
        arquitectura = (DOCS / "architecture/system-architecture.md").read_text(encoding="utf-8")
        faltantes = sorted(
            ruta for ruta in rutas if f"`{ruta}`" not in arquitectura
        )
        self.assertEqual([], faltantes)

    def test_modelo_documenta_contratos_transversales(self):
        texto = (DOCS / "architecture/data-model.md").read_text(encoding="utf-8")
        for esperado in (
            "DatosDetalleAnioActual",
            "ResumenFichaDigital",
            "ResumenFechaReferencia",
            "ResumenPrestacionUnificada",
            "DatosComparacionEscenarios",
            "ResumenTrazabilidadCalculo",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_modelo_aclara_ficha_sin_cuota_en_parser(self):
        texto = (DOCS / "architecture/data-model.md").read_text(encoding="utf-8")
        self.assertIn("No contiene `cuota_acreditada`", texto)
        self.assertIn("RegistroDetalleAnioActual", texto)

    def test_gestion_documenta_reconciliacion_ascendente_vigente(self):
        texto = (DOCS / "product/simulation-data-management.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Reconciliación ascendente controlada", texto)
        self.assertIn("puede ampliar", texto)
        self.assertIn("no reduce automáticamente", texto)

    def test_motor_declara_importadores_fuera_del_motor(self):
        texto = (DOCS / "architecture/calculation-engine.md").read_text(encoding="utf-8")
        self.assertIn("capas de entrada", texto)
        self.assertIn("no se calibra", texto)

    def test_guia_no_contiene_diario_de_fases_ux(self):
        texto = (DOCS / "operations/development-guide.md").read_text(
            encoding="utf-8"
        )
        self.assertNotRegex(texto, r"(?m)^##\s+UX\.")
        self.assertIn("docs/archive/", texto)

    def test_changelog_preserva_cierre_r2(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("GOV.1.3 R2 completada", texto)
        self.assertIn("Validación R2:", texto)
        self.assertIn("423 pruebas automatizadas en `OK`", texto)
        self.assertIn("12/12 regresiones específicas de R2", texto)
        self.assertIn("8/8 regresiones documentales de R1", texto)

    def test_especificacion_preserva_rf_y_marca_sustitucion(self):
        texto = (DOCS / "product/functional-specification.md").read_text(
            encoding="utf-8"
        )
        historico = (
            DOCS
            / "archive"
            / "technical"
            / "ESPECIFICACION_FUNCIONAL_PRE_GOV1_3_R2.md"
        ).read_text(encoding="utf-8")

        ids_actuales = re.findall(r"\*\*RF-(\d{3})\.\*\*", texto)
        ids_historicos = re.findall(r"\*\*RF-(\d{3})\.\*\*", historico)

        self.assertEqual(
            ids_historicos,
            ids_actuales[: len(ids_historicos)],
            "Los RF históricos deben conservarse como prefijo inmutable del ledger vigente.",
        )
        for esperado in ("001", "318", "322", "336"):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, ids_actuales)

        self.assertIn("RF-318 → sustituido por RF-322", texto)

    def test_r2_documentos_sin_espacios_finales(self):
        errores = []
        for nombre in R2_DOCS:
            archivo = DOCS / nombre
            for numero, linea in enumerate(
                archivo.read_text(encoding="utf-8").splitlines(),
                start=1,
            ):
                if linea.endswith((" ", "\t")):
                    errores.append(f"{nombre}:{numero}")
        self.assertEqual(
            [],
            errores,
            "Espacios finales: " + ", ".join(errores),
        )


if __name__ == "__main__":
    unittest.main()
