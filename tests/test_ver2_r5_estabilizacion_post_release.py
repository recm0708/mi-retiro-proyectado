"""Regresión VER.2 R5 posterior al release G071/E01."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestVer2R5EstabilizacionPostRelease(unittest.TestCase):
    def test_documento_r5_existe(self):
        doc = ROOT / "docs" / "VER2_R5_ESTABILIZACION_POST_RELEASE.md"
        self.assertTrue(doc.exists())
        texto = doc.read_text(encoding="utf-8")
        self.assertIn("0.0.71.01-beta", texto)
        self.assertIn("v0.0.71.01-beta", texto)
        self.assertIn("cb1dc24", texto)

    def test_version_actual(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, "0.0.71.01-beta")


if __name__ == "__main__":
    unittest.main()
