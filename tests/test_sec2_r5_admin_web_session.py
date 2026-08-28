"""SEC.2 R5 - Regresiones de sesión administrativa web."""

from __future__ import annotations

import os
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class TestSec2AdminWebSession(unittest.TestCase):

    @staticmethod
    def _env(temp: str):
        return patch.dict(
            os.environ,
            {
                "MRP_DIAGNOSTIC_DIR": temp,
                "MRP_DEV_MODE": "1",
                "MRP_ADMIN_ENABLED": "1",
                "MRP_ADMIN_SECRET": "test-admin-secret",
            },
            clear=False,
        )

    def test_login_renderiza_formulario(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(app).get("/dev/login")

        self.assertEqual(200, respuesta.status_code)
        self.assertIn("Acceso restringido", respuesta.text)
        self.assertIn("Iniciar sesión", respuesta.text)

    def test_login_valido_crea_cookie_y_redirecciona(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(app).post(
                    "/dev/login",
                    data={"token": "test-admin-secret"},
                    follow_redirects=False,
                )

        self.assertEqual(303, respuesta.status_code)
        self.assertIn(
            "mrp_admin_session",
            respuesta.headers.get("set-cookie", ""),
        )

    def test_centro_desarrollo_permite_sesion_valida(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)

                cliente.post(
                    "/dev/login",
                    data={"token": "test-admin-secret"},
                )

                respuesta = cliente.get("/dev/centro-desarrollo")

        self.assertEqual(200, respuesta.status_code)
        self.assertIn("Centro de desarrollo", respuesta.text)

    def test_logout_redirecciona_login(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)

                cliente.post(
                    "/dev/login",
                    data={"token": "test-admin-secret"},
                )

                respuesta = cliente.post(
                    "/dev/logout",
                    follow_redirects=False,
                )

        self.assertEqual(303, respuesta.status_code)
        self.assertEqual("/dev", respuesta.headers["location"])


if __name__ == "__main__":
    unittest.main()
