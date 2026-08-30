"""DOC.1 R5 — regresiones de estándares y plantillas Markdown."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "docs" / "templates"


class TestDoc1R5MarkdownStandards(unittest.TestCase):
    """Protege la cobertura formal de Markdown y sus tipos documentales."""

    def test_indice_de_plantillas_separa_familias(self):
        index = (TEMPLATES / "README.md").read_text(encoding="utf-8")

        self.assertIn("file-structure/README.md", index)
        self.assertIn("documentation/README.md", index)
        self.assertIn("estructura técnica", index)
        self.assertIn("estructura editorial", index)

    def test_markdown_tiene_plantilla_por_extension(self):
        template = TEMPLATES / "file-structure" / "template.md"

        self.assertTrue(template.is_file())
        text = template.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("# "))
        self.assertIn("## Propósito", text)
        self.assertIn("## Alcance", text)
        self.assertIn("títulos humanos", text)

    def test_familia_documental_cubre_tipos_canonicos(self):
        expected = {
            "README.md",
            "live-document.md",
            "standard-policy.md",
            "audit-evidence.md",
            "historical-record.md",
            "adr.md",
        }

        found = {
            path.name
            for path in (TEMPLATES / "documentation").glob("*.md")
        }

        self.assertEqual(expected, found)

    def test_politica_por_extension_declara_markdown(self):
        policy = (
            ROOT / "docs" / "standards" / "file-structure-by-extension.md"
        ).read_text(encoding="utf-8")

        self.assertIn("| `.md` |", policy)
        self.assertIn("documentation-standards.md", policy)
        self.assertIn("docs/templates/documentation/", policy)
        self.assertIn("template.md", policy)

    def test_estandar_documental_define_estructura_por_tipo(self):
        standard = (
            ROOT / "docs" / "standards" / "documentation-standards.md"
        ).read_text(encoding="utf-8")

        self.assertIn("## Estructura por tipo documental", standard)
        for fragment in (
            "Documento vigente",
            "Estándar o política",
            "Auditoría o evidencia",
            "Registro histórico",
            "ADR",
            "../templates/documentation/README.md",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, standard)


    def test_registro_vivo_acumulativo_esta_formalizado(self):
        standard = (
            ROOT / "docs" / "standards" / "documentation-standards.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Registro vivo acumulativo", standard)
        self.assertIn("docs/decisions/README.md", standard)
        self.assertIn("docs/operations/validation.md", standard)

        for rel in (
            "docs/decisions/README.md",
            "docs/operations/validation.md",
        ):
            with self.subTest(rel=rel):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn(
                    "**Naturaleza documental:** Registro vivo acumulativo",
                    text,
                )

    def test_validacion_inventaria_todos_los_modulos_reales(self):
        validation = (
            ROOT / "docs" / "operations" / "validation.md"
        ).read_text(encoding="utf-8")

        match = re.search(
            r"## 3\. Inventario actual de pruebas\s+"
            r"Inventario vigente:\s+\*\*(\d+) módulos\*\*\.(.*?)"
            r"\n## 4\. Categorías",
            validation,
            flags=re.S,
        )

        self.assertIsNotNone(match)

        declared = int(match.group(1))
        documented = sorted(
            set(
                re.findall(
                    r"`(tests/test_[^`]+\.py)`",
                    match.group(2),
                )
            )
        )
        actual = sorted(
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "tests").glob("test_*.py")
            if path.is_file()
        )

        self.assertEqual(len(actual), declared)
        self.assertEqual(actual, documented)

    def test_indice_dev2_refleja_r5_y_reserva_r6(self):
        index = (ROOT / "docs" / "README.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "DEV.2 R1–R5 — Centro de desarrollo",
            index,
        )
        self.assertIn(
            "R6 permanece como siguiente candidato funcional",
            index,
        )
        self.assertNotIn(
            "DEV.2 R1/R2/R3/R4 — Centro de desarrollo",
            index,
        )


if __name__ == "__main__":
    unittest.main()
