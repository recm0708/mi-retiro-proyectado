"""Validaciones estructurales de los estándares NOR.1."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestNOR1Standards(unittest.TestCase):

    def test_documentos_canonicos_existen(self):
        docs = ROOT / "docs" / "standards"
        archivos = [
            "README.md",
            "repository-structure.md",
            "naming-conventions.md",
            "file-standards.md",
            "documentation-standards.md",
            "artifact-lifecycle.md",
            "root-and-local-artifacts.md",
        ]

        for archivo in archivos:
            self.assertTrue((docs / archivo).exists(), archivo)

    def test_estructura_documental_estandar_existe(self):
        docs = ROOT / "docs"
        for carpeta in ["standards", "audits", "archive", "templates"]:
            self.assertTrue((docs / carpeta).exists(), carpeta)

    def test_evidencias_nor1_versionadas_estan_en_audits(self):
        esperados = [
            ROOT / "docs" / "audits" / "repository"
            / "nor1-r4-directory-inventory.txt",
            ROOT / "docs" / "audits" / "documentation"
            / "nor1-r5-documentation-inventory.txt",
        ]

        for archivo in esperados:
            self.assertTrue(archivo.exists(), str(archivo))

    def test_raiz_no_contiene_inventarios_nor1_txt(self):
        hallazgos = sorted(ROOT.glob("nor1-*.txt"))
        self.assertEqual([], hallazgos)

    def test_directorios_locales_de_entrega_estan_ignorados(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

        self.assertIn("_deliverables/", gitignore)
        self.assertIn("_entregas/", gitignore)


if __name__ == "__main__":
    unittest.main()
