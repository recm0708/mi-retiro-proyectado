"""Pruebas de mantenimiento técnico del repositorio y recursos base."""

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


ROOT = Path(__file__).resolve().parents[1]


class TestMantenimientoTecnico(unittest.TestCase):
    """Protege convenciones del repositorio y respuestas auxiliares."""

    def test_gitattributes_fuerza_lf_para_todo_texto(self):
        contenido = (ROOT / ".gitattributes").read_text(encoding="utf-8")

        self.assertIn("* text=auto eol=lf", contenido)

    def test_favicon_temporal_no_genera_404(self):
        cliente = TestClient(app)
        respuesta = cliente.get("/favicon.ico")

        self.assertEqual(respuesta.status_code, 204)
        self.assertEqual(respuesta.content, b"")
        self.assertEqual(respuesta.headers.get("cache-control"), "no-store")


if __name__ == "__main__":
    unittest.main()
