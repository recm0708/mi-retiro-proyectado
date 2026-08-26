"""Regresiones documentales mínimas del cierre DEV.2 R1."""

from __future__ import annotations

from pathlib import Path
import unittest

from app.core.version import APP_VERSION


ROOT = Path(__file__).resolve().parents[1]


class TestDev2R1CierreDocumental(unittest.TestCase):
    def test_documento_dev2_refleja_cierre_r1(self):
        documento = (ROOT / "docs/architecture/development-center.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("**Estado R1:** integrado en `main` mediante PR #37.", documento)
        self.assertIn("/dev/centro-desarrollo", documento)
        self.assertIn("PR #37", documento)
        self.assertIn("06e2821", documento)
        self.assertIn("DEV.2 R2", documento)
        self.assertIn("868 passed, 695 subtests passed", documento)
        self.assertIn("0.0.26-beta", documento)

    def test_cierre_documental_no_cambia_version_visible(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

        self.assertEqual("0.1.10.01-beta", version)
        self.assertEqual("0.1.10.01-beta", APP_VERSION)


if __name__ == "__main__":
    unittest.main()
