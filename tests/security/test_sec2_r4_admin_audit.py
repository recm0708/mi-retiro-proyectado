"""SEC.2 R4 - Auditoría de accesos administrativos."""

import json
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.observability import ruta_log_actual
from app.main import app


class TestSec2R4AdminAudit(unittest.TestCase):
    """Valida la generación segura de eventos administrativos."""

    def _env(self, temp: str, enabled: str = "1"):
        return patch.dict(
            os.environ,
            {
                "MRP_DIAGNOSTIC_DIR": temp,
                "MRP_DEV_MODE": "1",
                "MRP_ADMIN_ENABLED": enabled,
                "MRP_ADMIN_SECRET": "test-admin-secret",
            },
            clear=False,
        )

    def _leer_eventos(self):
        ruta = Path(ruta_log_actual())
        if not ruta.exists():
            return []

        return [
            json.loads(line)
            for line in ruta.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_acceso_admin_correcto_registra_evento(self):
        """Un acceso administrativo válido genera auditoría."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(app).get(
                    "/dev/centro-desarrollo",
                    headers={
                        "Authorization": "Bearer test-admin-secret"
                    },
                )

                eventos = self._leer_eventos()

        self.assertEqual(200, respuesta.status_code)

        nombres = [
            evento["event"]
            for evento in eventos
        ]

        self.assertIn(
            "admin.access.granted",
            nombres,
        )

    def test_token_invalido_registra_denegacion(self):
        """Un token inválido genera evento de seguridad."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(app).get(
                    "/dev/centro-desarrollo",
                    headers={
                        "Authorization": "Bearer incorrecto"
                    },
                )

                eventos = self._leer_eventos()

        self.assertEqual(403, respuesta.status_code)

        nombres = [
            evento["event"]
            for evento in eventos
        ]

        self.assertIn(
            "admin.access.denied",
            nombres,
        )

    def test_eventos_no_exponen_secretos(self):
        """Los eventos administrativos no deben almacenar credenciales."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                TestClient(app).get(
                    "/dev/centro-desarrollo",
                    headers={
                        "Authorization": "Bearer test-admin-secret"
                    },
                )

                contenido = Path(
                    ruta_log_actual()
                ).read_text(
                    encoding="utf-8"
                )

        self.assertNotIn(
            "test-admin-secret",
            contenido,
        )

        self.assertNotIn(
            "Authorization",
            contenido,
        )


if __name__ == "__main__":
    unittest.main()