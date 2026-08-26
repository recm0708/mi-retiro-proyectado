"""MANT.1 R3 — documentación de YAML de GitHub."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


YAML_GITHUB = {
    ".github/dependabot.yml": (
        "# Configuración de mantenimiento automatizado de dependencias.",
        "Propósito:",
        "Alcance:",
        "package-ecosystem: pip",
        "package-ecosystem: github-actions",
    ),
    ".github/ISSUE_TEMPLATE/bug_report.yml": (
        "# Plantilla de reporte de error.",
        "Propósito:",
        "Alcance:",
        'labels: ["bug", "needs-triage"]',
        "Confirmo que no he incluido datos personales reales ni secretos.",
    ),
    ".github/ISSUE_TEMPLATE/config.yml": (
        "# Configuración de entrada para issues.",
        "Propósito:",
        "Alcance:",
        "blank_issues_enabled: false",
        "security/policy",
    ),
    ".github/ISSUE_TEMPLATE/feature_request.yml": (
        "# Plantilla de solicitud de mejora.",
        "Propósito:",
        "Alcance:",
        'labels: ["enhancement", "needs-triage"]',
        "Entiendo que una propuesta normativa necesita una fuente oficial verificable.",
    ),
    ".github/ISSUE_TEMPLATE/question.yml": (
        "# Plantilla de consulta y soporte.",
        "Propósito:",
        "Alcance:",
        'labels: ["question", "needs-triage"]',
        "Confirmo que esta consulta no contiene una vulnerabilidad",
    ),
    ".github/workflows/governance-audit.yml": (
        "# Workflow de auditoría de gobernanza.",
        "Propósito:",
        "Alcance:",
        "pull_request:",
        "python -m unittest tests.test_gov16_controles_github -v",
    ),
    ".github/workflows/ci.yml": (
        "# Workflow de validación continua.",
        "Propósito:",
        "Alcance:",
        'python-version: ["3.13", "3.14"]',
        "python -m unittest discover -s tests -v",
    ),
    ".github/workflows/verificar-tags.yml": (
        "# Workflow de verificación de firmas Git.",
        "Propósito:",
        "Alcance:",
        'tags:',
        'git tag -v "$GITHUB_REF_NAME"',
    ),
}


class TestMant1R3YamlGithubDocumentados(unittest.TestCase):
    """Protege encabezados documentales sin congelar el contenido operativo completo."""

    def _leer(self, ruta):
        return (ROOT / ruta).read_text(encoding="utf-8")

    def test_yaml_github_declara_encabezado_funcional(self):
        """Cada YAML de GitHub inicia con comentario de propósito y límites."""

        for ruta, patrones in YAML_GITHUB.items():
            texto = self._leer(ruta)
            primeras_lineas = "\n".join(texto.splitlines()[:4])
            with self.subTest(ruta=ruta):
                self.assertTrue(texto.startswith(patrones[0]))
                self.assertNotIn("MANT.1", primeras_lineas)
                for patron in patrones[:3]:
                    self.assertIn(patron, primeras_lineas)

    def test_yaml_github_conserva_contratos_operativos_principales(self):
        """Los comentarios no sustituyen ni eliminan claves funcionales críticas."""

        for ruta, patrones in YAML_GITHUB.items():
            texto = self._leer(ruta)
            for patron in patrones[3:]:
                with self.subTest(ruta=ruta, patron=patron):
                    self.assertIn(patron, texto)

    def test_documentacion_transversal_registra_mant1_r1_r2_y_r3(self):
        """La documentación vigente conserva la contabilidad incremental de MANT.1."""

        rutas = (
            "CHANGELOG.md",
            "docs/standards/code-and-comments.md",
            "docs/operations/validation.md",
            "docs/architecture/system-architecture.md",
            "docs/governance/roadmap.md",
        )
        for ruta in rutas:
            texto = self._leer(ruta)
            with self.subTest(ruta=ruta):
                self.assertIn("MANT.1 R1", texto)
                self.assertIn("MANT.1 R2", texto)
                self.assertIn("MANT.1 R3", texto)
                self.assertIn("YAML", texto)

    def test_mant1_r3_no_declara_inicio_de_sec2_ni_cambio_de_version(self):
        """MANT.1 R3 es mantenimiento previo a SEC.2, no cambio funcional."""

        from app.core.version import APP_VERSION
        version = self._leer("VERSION").strip()
        self.assertEqual(APP_VERSION, version)

        changelog = self._leer("CHANGELOG.md")
        roadmap = self._leer("docs/governance/roadmap.md")
        seccion_r3 = changelog.split("### MANT.1 R3", 1)[1].split("### MANT.1 R2", 1)[0]

        self.assertIn("antes de SEC.2", seccion_r3)
        self.assertIn("no cambia `VERSION`, `APP_VERSION`", seccion_r3)
        self.assertIn("antes de SEC.2", roadmap)

        for texto in (changelog, roadmap):
            with self.subTest():
                self.assertNotIn("SEC.2 — Hardening integral iniciado", texto)


if __name__ == "__main__":
    unittest.main()
