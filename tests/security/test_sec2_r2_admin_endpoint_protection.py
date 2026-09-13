"""Regresiones SEC.2 R2: protección del Centro de Desarrollo."""

from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class TestSec2R2AdminEndpointProtection(unittest.TestCase):
    def test_sin_habilitacion_admin_bloquea(self):
        with patch.dict(os.environ, {}, clear=True):
            respuesta = TestClient(app).get("/dev/centro-desarrollo")
        self.assertEqual(403, respuesta.status_code)

    def test_sin_token_devuelve_no_autorizado(self):
        with patch.dict(os.environ, {"MRP_ADMIN_ENABLED": "1", "MRP_ADMIN_TOKEN": "abc"}, clear=True):
            respuesta = TestClient(app).get("/dev/centro-desarrollo")
        self.assertEqual(401, respuesta.status_code)

    def test_token_incorrecto_bloquea(self):
        with patch.dict(os.environ, {"MRP_ADMIN_ENABLED": "1", "MRP_ADMIN_TOKEN": "abc"}, clear=True):
            respuesta = TestClient(app).get("/dev/centro-desarrollo", headers={"Authorization": "Bearer otro"})
        self.assertEqual(403, respuesta.status_code)

    def test_token_correcto_permite_acceso(self):
        with patch.dict(os.environ, {"MRP_ADMIN_ENABLED": "1", "MRP_ADMIN_TOKEN": "abc"}, clear=True):
            respuesta = TestClient(app).get("/dev/centro-desarrollo", headers={"Authorization": "Bearer abc"})
        self.assertEqual(200, respuesta.status_code)


if __name__ == "__main__":
    unittest.main()
