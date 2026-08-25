"""Pruebas SEC.2 R3 - Protección administrativa centralizada."""

import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class TestSec2R3AdminProtection(unittest.TestCase):
    """Valida la protección centralizada del endpoint administrativo."""

    def test_superficie_admin_deshabilitada_bloquea(self):
        """La ruta administrativa no debe estar disponible sin habilitación."""

        with patch.dict(
            os.environ,
            {
                "MRP_ADMIN_ENABLED": "",
                "MRP_ADMIN_SECRET": "abc123",
            },
            clear=True,
        ):
            respuesta = TestClient(app).get(
                "/dev/centro-desarrollo",
                headers={"Authorization": "Bearer abc123"},
            )

        self.assertEqual(403, respuesta.status_code)

    def test_sin_bearer_requiere_autenticacion(self):
        """Una solicitud sin credenciales debe ser rechazada."""

        with patch.dict(
            os.environ,
            {
                "MRP_ADMIN_ENABLED": "1",
                "MRP_ADMIN_SECRET": "abc123",
            },
            clear=True,
        ):
            respuesta = TestClient(app).get(
                "/dev/centro-desarrollo"
            )

        self.assertEqual(401, respuesta.status_code)

    def test_bearer_incorrecto_bloquea(self):
        """Un token diferente al secreto configurado debe bloquear acceso."""

        with patch.dict(
            os.environ,
            {
                "MRP_ADMIN_ENABLED": "1",
                "MRP_ADMIN_SECRET": "abc123",
            },
            clear=True,
        ):
            respuesta = TestClient(app).get(
                "/dev/centro-desarrollo",
                headers={"Authorization": "Bearer otro"},
            )

        self.assertEqual(403, respuesta.status_code)

    def test_bearer_correcto_permite_acceso(self):
        """Un token válido permite acceder al centro administrativo."""

        with patch.dict(
            os.environ,
            {
                "MRP_ADMIN_ENABLED": "1",
                "MRP_ADMIN_SECRET": "abc123",
            },
            clear=True,
        ):
            respuesta = TestClient(app).get(
                "/dev/centro-desarrollo",
                headers={"Authorization": "Bearer abc123"},
            )

        self.assertEqual(200, respuesta.status_code)

    def test_respuesta_no_expone_secretos(self):
        """La respuesta no debe revelar variables sensibles."""

        with patch.dict(
            os.environ,
            {
                "MRP_ADMIN_ENABLED": "1",
                "MRP_ADMIN_SECRET": "abc123",
            },
            clear=True,
        ):
            respuesta = TestClient(app).get(
                "/dev/centro-desarrollo",
                headers={"Authorization": "Bearer abc123"},
            )

        self.assertNotIn("abc123", respuesta.text)
        self.assertNotIn("MRP_ADMIN_SECRET", respuesta.text)
        self.assertNotIn("MRP_ADMIN_TOKEN", respuesta.text)


if __name__ == "__main__":
    unittest.main()