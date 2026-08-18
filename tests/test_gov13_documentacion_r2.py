from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASE_VERSION = "0.0.23-beta"
R2_DOCS = [
    "ARQUITECTURA.md",
    "MODELO_DE_DATOS.md",
    "GESTION_DATOS_SIMULACION.md",
    "MOTOR_DE_CALCULO.md",
    "ESPECIFICACION_FUNCIONAL.md",
    "GUIA_INTERNA_DESARROLLO.md",
    "VALIDACION.md",
]


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
            snapshot = DOCS / "historico" / "tecnico" / nombre.replace(
                ".md", "_PRE_GOV1_3_R2.md"
            )
            with self.subTest(nombre=nombre):
                self.assertTrue(snapshot.is_file(), str(snapshot))

    def test_arquitectura_documenta_modulos_criticos(self):
        texto = (DOCS / "ARQUITECTURA.md").read_text(encoding="utf-8")
        for esperado in (
            "app/core/archivos_pdf.py",
            "app/core/version.py",
            "app/servicios/fecha_referencia.py",
            "app/servicios/ficha_digital.py",
            "app/servicios/detalle_anio_actual.py",
            "app/static/js/gestion_datos.js",
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
        arquitectura = (DOCS / "ARQUITECTURA.md").read_text(encoding="utf-8")
        faltantes = sorted(
            ruta for ruta in rutas if f"`{ruta}`" not in arquitectura
        )
        self.assertEqual([], faltantes)

    def test_modelo_documenta_contratos_transversales(self):
        texto = (DOCS / "MODELO_DE_DATOS.md").read_text(encoding="utf-8")
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
        texto = (DOCS / "MODELO_DE_DATOS.md").read_text(encoding="utf-8")
        self.assertIn("No contiene `cuota_acreditada`", texto)
        self.assertIn("RegistroDetalleAnioActual", texto)

    def test_gestion_documenta_reconciliacion_ascendente_vigente(self):
        texto = (DOCS / "GESTION_DATOS_SIMULACION.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Reconciliación ascendente controlada", texto)
        self.assertIn("puede ampliar", texto)
        self.assertIn("no reduce automáticamente", texto)

    def test_motor_declara_importadores_fuera_del_motor(self):
        texto = (DOCS / "MOTOR_DE_CALCULO.md").read_text(encoding="utf-8")
        self.assertIn("capas de entrada", texto)
        self.assertIn("no se calibra", texto)

    def test_guia_no_contiene_diario_de_fases_ux(self):
        texto = (DOCS / "GUIA_INTERNA_DESARROLLO.md").read_text(
            encoding="utf-8"
        )
        self.assertNotRegex(texto, r"(?m)^##\s+UX\.")
        self.assertIn("docs/historico/", texto)

    def test_changelog_preserva_cierre_r2(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("GOV.1.3 R2 completada", texto)
        self.assertIn("Validación R2:", texto)
        self.assertIn("423 pruebas automatizadas en `OK`", texto)
        self.assertIn("12/12 regresiones específicas de R2", texto)
        self.assertIn("8/8 regresiones documentales de R1", texto)

    def test_especificacion_preserva_rf_y_marca_sustitucion(self):
        texto = (DOCS / "ESPECIFICACION_FUNCIONAL.md").read_text(
            encoding="utf-8"
        )
        historico = (
            DOCS
            / "historico"
            / "tecnico"
            / "ESPECIFICACION_FUNCIONAL_PRE_GOV1_3_R2.md"
        ).read_text(encoding="utf-8")

        ids_actuales = re.findall(r"\*\*RF-(\d{3})\.\*\*", texto)
        ids_historicos = re.findall(r"\*\*RF-(\d{3})\.\*\*", historico)

        self.assertEqual(ids_historicos, ids_actuales)

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
