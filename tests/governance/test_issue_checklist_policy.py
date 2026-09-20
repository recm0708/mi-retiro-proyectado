"""Política transversal: toda Issue nueva debe incluir checklist de trabajo/cierre."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"
ISSUE_FORMS = (
    "architecture.yml",
    "bug_report.yml",
    "feature_request.yml",
    "plan.yml",
    "question.yml",
    "technical_debt.yml",
    "ux_review.yml",
)


class TestIssueChecklistPolicy(unittest.TestCase):
    def test_governance_documenta_politica_obligatoria(self):
        texto = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")

        for esperado in (
            "### 4.5. Ciclo de vida obligatorio de Issues",
            "Toda Issue nueva",
            "`- [ ]` / `- [x]`",
            "criterio de cierre",
            "owner/Issue explícito",
            ".github/ISSUE_TEMPLATE/",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_issue_forms_pregeneran_checklist_real_y_requerido(self):
        for nombre in ISSUE_FORMS:
            with self.subTest(nombre=nombre):
                path = TEMPLATE_DIR / nombre
                data = yaml.safe_load(path.read_text(encoding="utf-8"))

                body = data.get("body", [])
                bloques = [
                    bloque
                    for bloque in body
                    if bloque.get("id") == "checklist_trabajo"
                ]

                self.assertEqual(
                    1,
                    len(bloques),
                    f"{nombre} debe tener exactamente un checklist_trabajo",
                )

                bloque = bloques[0]
                self.assertEqual("textarea", bloque.get("type"))
                self.assertTrue(
                    bloque.get("validations", {}).get("required"),
                    f"{nombre}: checklist_trabajo debe ser required",
                )

                value = bloque.get("attributes", {}).get("value", "")
                self.assertGreaterEqual(
                    value.count("- [ ]"),
                    5,
                    f"{nombre}: faltan tareas iniciales verificables",
                )
                self.assertIn("criterio de cierre", value.casefold())
                self.assertIn("cerrar esta issue", value.casefold())

    def test_blank_issues_permanecen_deshabilitadas(self):
        config = yaml.safe_load(
            (TEMPLATE_DIR / "config.yml").read_text(encoding="utf-8")
        )
        self.assertIs(config.get("blank_issues_enabled"), False)


if __name__ == "__main__":
    unittest.main()
