"""MANT.1 R3 — documentación de YAML de GitHub."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


YAML_GITHUB = {
    ".github/dependabot.yml": (
        "MANT.1 R3",
        "Propósito:",
        "No modifica",
        "package-ecosystem: pip",
        "package-ecosystem: github-actions",
    ),
    ".github/ISSUE_TEMPLATE/bug_report.yml": (
        "MANT.1 R3",
        "Propósito:",
        "No modifica",
        'labels: ["bug", "needs-triage"]',
        "Confirmo que no he incluido datos personales reales ni secretos.",
    ),
    ".github/ISSUE_TEMPLATE/config.yml": (
        "MANT.1 R3",
        "Propósito:",
        "No modifica",
        "blank_issues_enabled: false",
        "security/policy",
    ),
    ".github/ISSUE_TEMPLATE/feature_request.yml": (
        "MANT.1 R3",
        "Propósito:",
        "No modifica",
        'labels: ["enhancement", "needs-triage"]',
        "Entiendo que una propuesta normativa necesita una fuente oficial verificable.",
    ),
    ".github/ISSUE_TEMPLATE/question.yml": (
        "MANT.1 R3",
        "Propósito:",
        "No modifica",
        'labels: ["question", "needs-triage"]',
        "Confirmo que esta consulta no contiene una vulnerabilidad",
    ),
    ".github/workflows/auditoria-gobernanza.yml": (
        "MANT.1 R3",
        "Propósito:",
        "No modifica",
        "pull_request:",
        "python -m unittest tests.test_gov16_controles_github -v",
    ),
    ".github/workflows/ci.yml": (
        "MANT.1 R3",
        "Propósito:",
        "No modifica",
        'python-version: ["3.13", "3.14"]',
        "python -m unittest discover -s tests -v",
    ),
    ".github/workflows/verificar-tags.yml": (
        "MANT.1 R3",
        "Propósito:",
        "No modifica",
        'tags:',
        'git tag -v "$GITHUB_REF_NAME"',
    ),
}


class TestMant1R3YamlGithubDocumentados(unittest.TestCase):
    """Protege encabezados documentales sin congelar el contenido operativo completo."""

    def _leer(self, ruta):
        return (ROOT / ruta).read_text(encoding="utf-8")

    def test_yaml_github_declara_encabezado_mant1_r3(self):
        """Cada YAML de GitHub inicia con comentario de propósito y límites."""

        for ruta, patrones in YAML_GITHUB.items():
            texto = self._leer(ruta)
            primeras_lineas = "\n".join(texto.splitlines()[:4])
            with self.subTest(ruta=ruta):
                self.assertTrue(texto.startswith("# MANT.1 R3"))
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
            "docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md",
            "docs/VALIDACION.md",
            "docs/ARQUITECTURA.md",
            "docs/ROADMAP.md",
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

        version = self._leer("VERSION").strip()
        self.assertEqual("0.0.26-beta", version)

        changelog = self._leer("CHANGELOG.md")
        roadmap = self._leer("docs/ROADMAP.md")
        seccion_r3 = changelog.split("### MANT.1 R3", 1)[1].split("### MANT.1 R2", 1)[0]

        self.assertIn("antes de SEC.2", seccion_r3)
        self.assertIn("no cambia `VERSION`, `APP_VERSION`", seccion_r3)
        self.assertIn("antes de SEC.2", roadmap)

        for texto in (changelog, roadmap):
            with self.subTest():
                self.assertNotIn("SEC.2 — Hardening integral iniciado", texto)


if __name__ == "__main__":
    unittest.main()
