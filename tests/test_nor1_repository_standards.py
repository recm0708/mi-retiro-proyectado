"""Validaciones básicas de NOR.1 R1."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestNOR1Standards(unittest.TestCase):

    def test_documentos_canónicos_existen(self):
        docs = ROOT / "docs" / "standards"
        archivos = [
            "README.md",
            "repository-structure.md",
            "naming-conventions.md",
            "file-standards.md",
            "documentation-standards.md",
            "artifact-lifecycle.md",
        ]

        for archivo in archivos:
            self.assertTrue((docs / archivo).exists())

if __name__ == "__main__":
    unittest.main()
