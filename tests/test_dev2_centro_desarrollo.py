"""Regresiones DEV.2 R1: Centro de desarrollo."""

from __future__ import annotations

import json
import os
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.observabilidad import ruta_log_actual
from app.main import app
from app.servicios.centro_desarrollo import construir_estado_centro_desarrollo


class TestDev2CentroDesarrolloR1(unittest.TestCase):
    @staticmethod
    def _env(temp: str, *, activo: bool):
        return patch.dict(
            os.environ,
            {
                "MRP_DIAGNOSTIC_DIR": temp,
                "MRP_DEV_MODE": "1" if activo else "",
            },
            clear=False,
        )

    def test_estado_no_expone_ruta_absoluta_ni_datos_sensibles(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=False):
                estado = construir_estado_centro_desarrollo()

        self.assertEqual("DEV.2 R1", estado["bloque"])
        self.assertEqual("Centro de desarrollo", estado["titulo"])
        self.assertFalse(estado["dev_mode_activo"])
        self.assertEqual("0.0.26-beta", estado["app_version"])
        self.assertEqual("mrp-diagnostics.jsonl", estado["archivo_log_actual"])
        self.assertNotIn(temp, json.dumps(estado, ensure_ascii=False))

        serializado = json.dumps(estado, ensure_ascii=False).casefold()
        for prohibido in (
            "cedula",
            "cédula",
            "nss",
            "cuotas_totales",
            "cookie",
            "token=",
        ):
            self.assertNotIn(prohibido, serializado)

    def test_ruta_centro_desarrollo_renderiza_sin_modo_activo(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=False):
                respuesta = TestClient(app).get("/dev/centro-desarrollo")

        self.assertEqual(200, respuesta.status_code)
        self.assertNotIn("x-correlation-id", respuesta.headers)
        self.assertIn("Centro de desarrollo", respuesta.text)
        self.assertIn("MRP_DEV_MODE", respuesta.text)
        self.assertIn("0.0.26-beta", respuesta.text)
        self.assertIn("Developer Diagnostics", respuesta.text)
        self.assertIn("Desactivado", respuesta.text)

    def test_ruta_activa_registra_operacion_dev_sin_datos_sensibles(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=True):
                respuesta = TestClient(app).get("/dev/centro-desarrollo")
                self.assertEqual(200, respuesta.status_code)
                self.assertRegex(
                    respuesta.headers.get("x-correlation-id") or "",
                    r"^[0-9a-f]{32}$",
                )

                contenido = ruta_log_actual().read_text(encoding="utf-8")
                evento = json.loads(contenido.splitlines()[0])

        self.assertEqual("http.request", evento["event"])
        self.assertEqual("dev.centro_desarrollo", evento["metadata"]["operation"])
        self.assertEqual("GET", evento["metadata"]["method"])
        self.assertEqual(200, evento["metadata"]["status_code"])
        self.assertNotIn("/dev/centro-desarrollo", contenido)
        self.assertNotIn("request.body", contenido)
        self.assertNotIn("cookie", contenido.casefold())
        self.assertNotIn("token", contenido.casefold())

    def test_documentacion_dev2_existe_y_preserva_alcance(self):
        from pathlib import Path

        documento = Path("docs/DEV2_CENTRO_DESARROLLO.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("DEV.2 R1", documento)
        self.assertIn("Centro de desarrollo", documento)
        self.assertIn("MRP_DEV_MODE=1", documento)
        self.assertIn("no cambia cálculos", documento.casefold())
        self.assertIn("no cambia VERSION", documento)


if __name__ == "__main__":
    unittest.main()
