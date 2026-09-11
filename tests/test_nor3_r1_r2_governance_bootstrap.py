"""Contrato del bootstrap de gobierno NOR.3 R1-R2."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
FORMS = ROOT / ".github" / "ISSUE_TEMPLATE"
PR_TEMPLATE = ROOT / ".github" / "pull_request_template.md"
GOV_DOC = ROOT / "docs" / "governance" / "github-issues-pr-governance.md"


class TestNOR3R1R2GovernanceBootstrap(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pr = PR_TEMPLATE.read_text(encoding="utf-8")
        cls.gov = GOV_DOC.read_text(encoding="utf-8")

    def test_formularios_nuevos_existen(self):
        expected = {
            "plan.yml",
            "architecture.yml",
            "technical_debt.yml",
            "ux_review.yml",
        }
        actual = {path.name for path in FORMS.glob("*.yml")}
        self.assertTrue(expected.issubset(actual))

    def test_formularios_legacy_se_preservan(self):
        for name in (
            "bug_report.yml",
            "feature_request.yml",
            "question.yml",
            "config.yml",
        ):
            with self.subTest(name=name):
                self.assertTrue((FORMS / name).is_file())

    def test_no_existe_formulario_handoff_ordinario(self):
        names = {path.name.lower() for path in FORMS.glob("*.yml")}
        self.assertNotIn("handoff.yml", names)
        self.assertNotIn("checkpoint.yml", names)

    def test_labels_de_forms_siguen_taxonomia_canonica(self):
        contracts = {
            "plan.yml": 'labels: ["planning"]',
            "architecture.yml": 'labels: ["planning", "architecture"]',
            "technical_debt.yml": 'labels: ["planning", "maintenance"]',
            "ux_review.yml": 'labels: ["planning", "ui"]',
        }
        for name, fragment in contracts.items():
            with self.subTest(name=name):
                text = (FORMS / name).read_text(encoding="utf-8")
                self.assertIn(fragment, text)
                self.assertIn("datos personales sensibles", text)

    def test_pr_template_declara_issues_alcance_y_cierre(self):
        for fragment in (
            "## Issues y alcance",
            "Umbrella:",
            "Issues implementados:",
            "Issues parcialmente cubiertos:",
            "Issues derivados / remanentes:",
            "Fase o par de revisiones:",
            "Alcance incluido:",
            "Fuera de alcance:",
            "Closes #N",
            "## Validación",
            "## Documentación",
            "## Seguridad y privacidad",
            "## Gobierno y versión",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.pr)

    def test_documento_formaliza_pares_y_milestones(self):
        for fragment in (
            "R1 + R2",
            "R3 + R4",
            "R5 + R6",
            "R7 + R8",
            "no usar Milestones",
            "No se crea un Issue Form ordinario de Handoff",
            "`Closes #N`",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, self.gov)

    def test_docs_raiz_enlazan_gobierno(self):
        for path in (
            ROOT / "GOVERNANCE.md",
            ROOT / "CONTRIBUTING.md",
        ):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertIn(
                    "docs/governance/github-issues-pr-governance.md",
                    text,
                )


if __name__ == "__main__":
    unittest.main()
