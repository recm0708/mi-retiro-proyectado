"""Regresiones UX.4.6e R5 para ayuda visible y preparación pública de GitHub."""

from pathlib import Path
import unittest
import yaml


ROOT = Path(__file__).resolve().parents[1]


class TestUX46ePreparacionPublica(unittest.TestCase):
    """Protege la frontera entre información útil al usuario y gobierno interno."""

    @classmethod
    def setUpClass(cls):
        cls.base = (ROOT / "app/templates/base.html").read_text(encoding="utf-8")
        cls.metodologia = (ROOT / "app/templates/methodology.html").read_text(encoding="utf-8")
        cls.terminos = (ROOT / "app/templates/partials/privacy_consent.html").read_text(encoding="utf-8")
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.publicacion = (ROOT / "docs/operations/github-public-repository.md").read_text(encoding="utf-8")
        cls.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    def test_footer_enlaza_ayuda_sin_exponer_gobierno_interno(self):
        self.assertIn('href="/metodologia#ayuda-contacto"', self.base)
        self.assertIn("Ayuda y contacto", self.base)
        for termino in ("CODEOWNERS", "Dependabot", "ruleset", "Python 3.13"):
            self.assertNotIn(termino, self.base)

    def test_metodologia_ofrece_ayuda_repositorio_y_verificacion(self):
        for esperado in (
            'id="ayuda-contacto"',
            "Contactar sobre la aplicación",
            "Abrir repositorio del proyecto",
            "Ver recursos oficiales",
            "https://github.com/recm0708/mi-retiro-proyectado",
        ):
            self.assertIn(esperado, self.metodologia)

    def test_recursos_individuales_usan_fuente_oficial(self):
        self.assertIn("Recursos oficiales para verificar información individual", self.metodologia)
        self.assertIn("Abrir fuente oficial", self.metodologia)
        self.assertNotIn("Abrir recurso oficial", self.metodologia)

    def test_terminos_no_prometen_visibilidad_publica_del_repo(self):
        self.assertIn("se mantienen en el", self.terminos)
        self.assertIn("repositorio de Mi Retiro Proyectado", self.terminos)
        self.assertNotIn("repositorio público", self.terminos.lower())
        self.assertNotIn("disponible públicamente", self.terminos.lower())

    def test_readme_muestra_badges_reales_y_estado_actual(self):
        for workflow in (
            "quality-gate.yml",
            "dependency-security.yml",
            "visual-a11y.yml",
        ):
            with self.subTest(workflow=workflow):
                self.assertIn(
                    (
                        "actions/workflows/"
                        + workflow
                        + "/badge.svg?branch=main"
                    ),
                    self.readme,
                )
        badge_version = self.version.replace("-", "--")
        self.assertIn(
            f"img.shields.io/badge/versi%C3%B3n-{badge_version}",
            self.readme,
        )
        self.assertIn("Python-3.13%20%7C%203.14", self.readme)
        self.assertIn("licencia-propietaria", self.readme)
        self.assertIn("UX.4.6e", self.readme)
        self.assertIn("21 labels y 20/20 topics configurados", self.readme)
        self.assertIn("`sebd-panama` adoptado", self.readme)

    def test_documento_publicacion_define_topics_aprobados(self):
        topics = (
            "accesibilidad",
            "caja-seguro-social",
            "calculadora-pension",
            "estimacion-previsional",
            "fastapi",
            "jubilacion",
            "panama",
            "pension",
            "pensiones-panama",
            "planificacion-retiro",
            "privacidad",
            "proyeccion-retiro",
            "proyeccion-salarial",
            "python",
            "retiro",
            "simulador-pension",
            "seguridad-social-panama",
            "sistema-mixto",
            "sucgs",
            "sebd-panama",
        )

        self.assertIn(
            "**20 topics**",
            self.publicacion,
        )

        for topic in topics:
            with self.subTest(topic=topic):
                self.assertIn(
                    f"`{topic}`",
                    self.publicacion,
                )

        for legacy in (
            "prevision-social",
            "seguridad-social",
        ):
            with self.subTest(legacy=legacy):
                self.assertNotIn(
                    f"- `{legacy}`",
                    self.publicacion,
                )

    def test_documento_publicacion_define_labels_y_aclara_commits(self):
        for label in (
            "bug", "enhancement", "question", "documentation", "tests",
            "maintenance", "dependencies", "github-actions", "ui", "backend",
            "regulations", "privacy", "security", "accessibility",
            "needs-triage", "blocked", "duplicate", "good first issue",
            "help wanted", "invalid", "wontfix",
        ):
            self.assertIn(f"`{label}`", self.publicacion)
        self.assertIn("no se asignan a commits", self.publicacion)

    def test_issue_forms_declaran_labels_iniciales(self):
        esperadas = {
            "bug_report.yml": ["bug", "needs-triage"],
            "feature_request.yml": ["enhancement", "needs-triage"],
            "question.yml": ["question", "needs-triage"],
        }
        for nombre, labels in esperadas.items():
            with self.subTest(nombre=nombre):
                data = yaml.safe_load((ROOT / ".github/ISSUE_TEMPLATE" / nombre).read_text(encoding="utf-8"))
                self.assertEqual(labels, data["labels"])

    def test_terceros_documentan_shields_fuera_del_runtime(self):
        notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
        deps = (ROOT / "docs/operations/third-party-dependencies.md").read_text(encoding="utf-8")
        eval_terceros = (ROOT / "docs/security/third-party-deployment-assessment.md").read_text(encoding="utf-8")
        for texto in (notices, deps, eval_terceros):
            self.assertIn("Shields.io", texto)
            self.assertIn("runtime", texto)

    def test_adr163_y_documentacion_enlazan_preparacion_publica(self):
        decisiones = (ROOT / "docs/decisions/README.md").read_text(encoding="utf-8")
        indice = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        auditoria = (ROOT / "docs/archive/governance/github-audit.md").read_text(encoding="utf-8")
        self.assertIn("## ADR-163 —", decisiones)
        self.assertIn("operations/github-public-repository.md", indice)
        self.assertIn("PREPARACION_PUBLICA_GITHUB.md", auditoria)


if __name__ == "__main__":
    unittest.main()
