"""Regresiones DEV.2 R3: autodiagnóstico técnico local."""

from __future__ import annotations

import json
import os
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.observabilidad import registrar_evento, ruta_log_actual
from app.main import app
from app.services.centro_desarrollo import (
    construir_estado_centro_desarrollo,
    ejecutar_autodiagnostico,
)


class TestDev2R3Autodiagnostico(unittest.TestCase):
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

    @staticmethod
    def _por_codigo(resultados: list[dict[str, str]]) -> dict[str, dict[str, str]]:
        return {resultado["codigo"]: resultado for resultado in resultados}

    def test_estado_incluye_autodiagnostico_sin_exponer_rutas_ni_datos_sensibles(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=False):
                estado = construir_estado_centro_desarrollo()

        self.assertEqual("DEV.2 R2", estado["revision_actual"])
        self.assertEqual("DEV.2 R3", estado["revision_autodiagnostico"])
        self.assertIn("autodiagnostico", estado)
        self.assertIn("resumen_autodiagnostico", estado)
        self.assertGreaterEqual(estado["resumen_autodiagnostico"]["total"], 8)

        serializado = json.dumps(estado, ensure_ascii=False).casefold()
        self.assertNotIn(temp.casefold(), serializado)
        for prohibido in (
            "4-123-456",
            "salario",
            "cedula",
            "cédula",
            "nss",
            "token=",
            "request.body",
        ):
            self.assertNotIn(prohibido, serializado)

    def test_autodiagnostico_activo_valida_permisos_log_exportacion_y_visor(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=True):
                registrar_evento(
                    level="INFO",
                    event="dev.autodiagnostico",
                    component="dev.centro_desarrollo",
                    outcome="success",
                    metadata={
                        "operation": "dev.centro_desarrollo",
                        "method": "GET",
                        "status_code": 200,
                    },
                )

                estado = construir_estado_centro_desarrollo()

        resultados = self._por_codigo(estado["autodiagnostico"])
        self.assertEqual("OK", resultados["dev_mode"]["estado"])
        self.assertEqual("OK", resultados["permisos_diagnostico"]["estado"])
        self.assertEqual("OK", resultados["log_vigente"]["estado"])
        self.assertEqual("OK", resultados["exportacion_zip"]["estado"])
        self.assertEqual("OK", resultados["visor_eventos"]["estado"])
        self.assertEqual("OK", resultados["privacidad"]["estado"])
        self.assertEqual("OK", estado["resumen_autodiagnostico"]["estado_global"])

    def test_autodiagnostico_activo_sin_log_advierte_sin_crear_eventos_falsos(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=True):
                self.assertFalse(ruta_log_actual().exists())
                resultados = ejecutar_autodiagnostico(
                    activo=True,
                    archivos=None,
                    eventos=[],
                    invalidos=0,
                )

        por_codigo = {
            resultado.codigo: resultado
            for resultado in resultados
        }
        self.assertEqual("OK", por_codigo["dev_mode"].estado)
        self.assertEqual("OK", por_codigo["permisos_diagnostico"].estado)
        self.assertEqual("ADVERTENCIA", por_codigo["log_vigente"].estado)
        self.assertEqual("ADVERTENCIA", por_codigo["exportacion_zip"].estado)
        self.assertEqual("ADVERTENCIA", por_codigo["visor_eventos"].estado)

    def test_ruta_centro_desarrollo_renderiza_autodiagnostico_r3(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=True):
                registrar_evento(
                    level="WARNING",
                    event="dev.autodiagnostico",
                    component="dev.centro_desarrollo",
                    outcome="warning",
                    metadata={
                        "operation": "dev.centro_desarrollo",
                        "method": "GET",
                        "status_code": 200,
                    },
                )
                respuesta = TestClient(app).get("/dev/centro-desarrollo")

        self.assertEqual(200, respuesta.status_code)
        self.assertIn("DEV.2 R2", respuesta.text)
        self.assertIn("DEV.2 R3", respuesta.text)
        self.assertIn("Autodiagnóstico técnico", respuesta.text)
        self.assertIn("Estado global", respuesta.text)
        self.assertIn("Permisos locales", respuesta.text)
        self.assertIn("Visor diagnóstico", respuesta.text)
        self.assertNotIn(temp, respuesta.text)
        self.assertNotIn("request.body", respuesta.text)
        self.assertNotIn("token=", respuesta.text.casefold())


if __name__ == "__main__":
    unittest.main()
