"""Pruebas de mantenimiento técnico del repositorio y recursos base."""

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


ROOT = Path(__file__).resolve().parents[2]


class TestMantenimientoTecnico(unittest.TestCase):
    """Protege convenciones del repositorio y respuestas auxiliares."""

    def test_gitattributes_fuerza_lf_para_todo_texto(self):
        contenido = (ROOT / ".gitattributes").read_text(encoding="utf-8")

        self.assertIn("* text=auto eol=lf", contenido)

    def test_favicon_oficial_se_entrega_desde_la_ruta_estandar(self):
        cliente = TestClient(app)
        respuesta = cliente.get("/favicon.ico")

        self.assertEqual(respuesta.status_code, 200)
        self.assertGreater(len(respuesta.content), 0)
        self.assertEqual(
            respuesta.headers.get("content-type"),
            "image/x-icon",
        )
        self.assertIn(
            "max-age=86400",
            respuesta.headers.get("cache-control", ""),
        )


if __name__ == "__main__":
    unittest.main()
