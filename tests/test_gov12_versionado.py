"""Regresiones de GOV.1.2 para gobierno y versionado centralizado."""

import re
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.core.config import APP_VERSION
from app.main import app


ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION"
CONFIG = ROOT / "app/core/config.py"
BASE = ROOT / "app/templates/base.html"


class TestGov12Versionado(unittest.TestCase):
    """Evita divergencias entre versión, API, interfaz y gobierno."""

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_version_file_es_fuente_canonica(self):
        version = VERSION_FILE.read_text(encoding="utf-8").strip()
        self.assertTrue(version)
        self.assertRegex(
            version,
            re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?$"),
        )
        self.assertEqual(APP_VERSION, version)

    def test_config_importa_version_en_lugar_de_duplicarla(self):
        contenido = CONFIG.read_text(encoding="utf-8")
        self.assertIn("from app.core.version import APP_VERSION", contenido)
        self.assertNotIn('APP_VERSION = "0.1.0"', contenido)
        self.assertNotRegex(
            contenido,
            re.compile(r'(?m)^\\s*APP_VERSION\\s*=\\s*["\\\']'),
        )

    def test_fastapi_expone_la_version_canonica(self):
        self.assertEqual(app.version, APP_VERSION)

    def test_footer_renderiza_la_version_canonica(self):
        base = BASE.read_text(encoding="utf-8")
        self.assertIn("v{{ app_version }}", base)
        respuesta = self.client.get("/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn(f"v{APP_VERSION}", respuesta.text)

    def test_documentos_de_gobierno_existen(self):
        for ruta in ("GOVERNANCE.md", "VERSIONING.md", "RELEASES.md"):
            with self.subTest(ruta=ruta):
                self.assertTrue((ROOT / ruta).is_file())

    def test_releases_declara_reconstruccion_y_primera_version_formal(self):
        contenido = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        self.assertIn("80 commits", contenido)
        self.assertIn("0.0.1-beta", contenido)
        self.assertIn("0.0.21-beta", contenido)
        self.assertIn("0.0.22-beta", contenido)
        version = VERSION_FILE.read_text(encoding="utf-8").strip()
        self.assertIn(version, contenido)
        self.assertIn("reconstru", contenido.lower())

    def test_codeowners_define_responsable_actual(self):
        contenido = (ROOT / ".github/CODEOWNERS").read_text(encoding="utf-8")
        self.assertIn("* @recm0708", contenido)
        self.assertIn("/normativa/ @recm0708", contenido)


if __name__ == "__main__":
    unittest.main()
