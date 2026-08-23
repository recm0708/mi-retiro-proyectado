"""Regresiones de GOV.1.5 R1: modelo de amenazas."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "MODELO_AMENAZAS.md"


class TestGov15ModeloAmenazasR1(unittest.TestCase):
    def setUp(self):
        self.texto = DOC.read_text(encoding="utf-8")
        self.version_base = "0.0.23-beta"

    def test_documento_existe_declara_estado_version_y_limite(self):
        self.assertTrue(DOC.is_file())
        self.assertIn(self.version_base, self.texto)
        self.assertIn("GOV.1.5 R1", self.texto)
        self.assertIn("No constituye auditoría de penetración", self.texto)
        self.assertIn("garantía de riesgo cero", self.texto)

    def test_alcance_refleja_arquitectura_local_actual(self):
        for esperado in (
            "localhost",
            "ausencia de cuentas de usuario",
            "ausencia de base de datos permanente",
            "documentos PDF procesados en memoria",
            "Developer Diagnostics",
            "jsDelivr",
            "infraestructura CSS",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, self.texto)

    def test_activos_cubren_datos_codigo_normativa_y_logs(self):
        for esperado in (
            "Datos de identidad opcionales",
            "Cuotas e historial salarial",
            "Resultados previsionales",
            "PDF seleccionado",
            "Logs Developer Diagnostics",
            "Parámetros `regulations/*.json`",
            "Código de motores y servicios",
            "Historial Git, tags y CI",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, self.texto)

    def test_fronteras_de_confianza_cubren_superficies_reales(self):
        for esperado in (
            "F1 — Navegador ↔ FastAPI local",
            "F2 — Archivo elegido ↔ Parser PDF",
            "F3 — Runtime ↔ Sistema de archivos diagnóstico",
            "F4 — Backend ↔ Infraestructura CSS",
            "F5 — Navegador ↔ jsDelivr",
            "F6 — Repositorio/CI ↔ Cadena de suministro",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, self.texto)

    def test_matriz_cubre_amenazas_criticas_y_riesgo_residual(self):
        for amenaza in range(1, 16):
            with self.subTest(amenaza=amenaza):
                self.assertIn(f"T-{amenaza:02d}", self.texto)
        for esperado in (
            "PDF malformado",
            "Divulgación de datos por logging",
            "XSS",
            "Denegación de servicio",
            "CSRF",
            "Clickjacking",
            "cadena de suministro",
            "Riesgo residual / acción",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, self.texto)

    def test_controles_documentados_corresponden_a_componentes_reales(self):
        for ruta in (
            "app/core/pdf_files.py",
            "app/core/observability.py",
            "app/main.py",
            "app/services/reference_date.py",
            ".github/workflows/ci.yml",
        ):
            with self.subTest(ruta=ruta):
                self.assertTrue((ROOT / ruta).is_file(), ruta)

        for esperado in (
            "Cache-Control: no-store",
            "Content-Security-Policy",
            "MRP_DEV_MODE=1",
            "Subresource Integrity",
            "rulesets",
            "Dependabot",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, self.texto)

    def test_modelo_define_disparadores_y_no_declara_internet_listo(self):
        self.assertIn("Disparadores de revisión", self.texto)
        self.assertIn("No se considera listo para exposición pública", self.texto)
        for esperado in (
            "cuentas/autenticación",
            "base de datos",
            "analítica o telemetría",
            "nuevo tercero",
            "OCR",
            "incidente de seguridad",
            "cambio normativo aplicable",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, self.texto)


if __name__ == "__main__":
    unittest.main()
