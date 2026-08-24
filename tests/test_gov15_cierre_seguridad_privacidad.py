"""Regresiones de cierre GOV.1.5 — seguridad, privacidad y transparencia."""

from pathlib import Path
import re
import unittest

from fastapi.testclient import TestClient

from app.main import app


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestGov15CierreSeguridadPrivacidad(unittest.TestCase):
    def setUp(self):
        self.version_base = "0.0.23-beta"

    def test_evaluacion_terceros_declara_escenario_local_y_no_internet_ready(self):
        texto = (DOCS / "security/third-party-deployment-assessment.md").read_text(
            encoding="utf-8"
        )
        for esperado in (
            "127.0.0.1",
            "cdn.jsdelivr.net",
            "infraestructura CSS",
            "GitHub",
            "TLS pasa a ser obligatorio",
            "--forwarded-allow-ips",
            "No declarar un despliegue remoto como soportado",
            "revisión jurídica externa",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_documentos_gov15_existen_y_siguen_version_canonica(self):
        for nombre in (
            "security/threat-model.md",
            "security/data-subject-rights-procedure.md",
            "security/security-incident-procedure.md",
            "security/third-party-deployment-assessment.md",
        ):
            with self.subTest(nombre=nombre):
                texto = (DOCS / nombre).read_text(encoding="utf-8")
                self.assertIn(self.version_base, texto)
                self.assertIn("GOV.1.5", texto)

    def test_roadmap_conserva_cierre_gov15_sin_congelar_estado_futuro(self):
        texto = (DOCS / "governance/roadmap.md").read_text(encoding="utf-8")
        self.assertIn(
            "- [x] **GOV.1.5 — Seguridad, privacidad y transparencia**",
            texto,
        )
        self.assertIn("GOV.1.6 — Controles GitHub y auditoría automática", texto)
        self.assertIn("revisión jurídica externa", texto)

    def test_readme_conserva_cierre_gov15_sin_fijar_bloque_activo(self):
        texto = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "**GOV.1.5:** Seguridad, privacidad y transparencia cerrado internamente",
            texto,
        )
        self.assertIn("(docs/security/threat-model.md)", texto)

    def test_privacidad_conserva_version_material_y_documenta_procedimientos(self):
        texto = (DOCS / "security/privacy-policy.md").read_text(encoding="utf-8")
        js = (ROOT / "app/static/js/privacy.js").read_text(encoding="utf-8")
        match = re.search(r'VERSION_PRIVACIDAD\s*=\s*"([^"]+)"', js)
        self.assertIsNotNone(match)
        version = match.group(1)
        self.assertEqual("2026-08-16.1", version)
        self.assertIn(f"`{version}`", texto)
        self.assertIn("data-subject-rights-procedure.md", texto)
        self.assertIn("security-incident-procedure.md", texto)

    def test_matriz_cumplimiento_actualiza_controles_sin_certificar(self):
        texto = (DOCS / "regulatory/law-81-compliance.md").read_text(
            encoding="utf-8"
        )
        for esperado in (
            "Implementado documental GOV.1.5",
            "Implementado base GOV.1.4/GOV.1.5",
            "Gate documentado; no aplica al localhost actual",
            "No constituye certificación jurídica",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_headers_defensivos_siguen_activos(self):
        with TestClient(app) as client:
            response = client.get("/")
        self.assertEqual("nosniff", response.headers["x-content-type-options"])
        self.assertEqual("DENY", response.headers["x-frame-options"])
        self.assertEqual("no-referrer", response.headers["referrer-policy"])
        self.assertIn(
            "frame-ancestors 'none'",
            response.headers["content-security-policy"],
        )
        self.assertIn("camera=()", response.headers["permissions-policy"])

    def test_api_simulacion_mantiene_no_store(self):
        main = (ROOT / "app/main.py").read_text(encoding="utf-8")
        self.assertIn('request.url.path.startswith("/api/simulacion/")', main)
        self.assertIn('respuesta.headers["Cache-Control"] = "no-store"', main)

    def test_terceros_y_logs_tienen_riesgo_residual_visible(self):
        terceros = (DOCS / "operations/third-party-dependencies.md").read_text(
            encoding="utf-8"
        )
        logs = (DOCS / "operations/observability-and-logs.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("riesgo residual", terceros.casefold())
        self.assertIn("Revisión de seguridad GOV.1.5", logs)
        self.assertIn("metadata futura", logs)

    def test_documentos_cierre_sin_espacios_finales(self):
        nombres = (
            "security/third-party-deployment-assessment.md",
            "security/security-and-privacy.md",
            "security/privacy-policy.md",
            "regulatory/law-81-compliance.md",
            "operations/third-party-dependencies.md",
            "product/transparency.md",
            "product/known-limitations.md",
            "operations/observability-and-logs.md",
            "README.md",
            "governance/roadmap.md",
            "operations/validation.md",
        )
        errores = []
        for nombre in nombres:
            for numero, linea in enumerate(
                (DOCS / nombre).read_text(encoding="utf-8").splitlines(),
                start=1,
            ):
                if linea.endswith((" ", "\t")):
                    errores.append(f"{nombre}:{numero}")
        self.assertEqual([], errores, "Espacios finales: " + ", ".join(errores))


if __name__ == "__main__":
    unittest.main()
