"""Regresiones DEV.2 R2: visor diagnóstico y exportación segura."""

from __future__ import annotations

import json
import os
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from zipfile import ZipFile

from fastapi.testclient import TestClient

from app.core.observabilidad import registrar_evento, ruta_log_actual
from app.main import app
from app.servicios.centro_desarrollo import (
    construir_estado_centro_desarrollo,
    exportar_zip_diagnostico_sanitizado,
)


class TestDev2R2VisorDiagnostico(unittest.TestCase):
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

    def test_visor_normaliza_eventos_sin_exponer_metadata_sensible(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=True):
                ruta = ruta_log_actual()
                ruta.parent.mkdir(parents=True, exist_ok=True)
                ruta.write_text(
                    json.dumps(
                        {
                            "timestamp": "2026-08-23T10:00:00.000+00:00",
                            "level": "INFO",
                            "event": "http.request",
                            "component": "fastapi",
                            "outcome": "success",
                            "correlation_id": "a" * 32,
                            "duration_ms": 12.34567,
                            "metadata": {
                                "method": "GET",
                                "operation": "dev.centro_desarrollo",
                                "status_code": 200,
                                "nombre": "Juan Pérez",
                                "cedula": "4-123-456",
                                "salario": "B/. 999.99",
                            },
                        },
                        ensure_ascii=False,
                    )
                    + "\n",
                    encoding="utf-8",
                )

                estado = construir_estado_centro_desarrollo()

        self.assertEqual("DEV.2 R2", estado["revision_actual"])
        self.assertEqual(1, estado["total_eventos_visibles"])
        self.assertEqual(1, estado["resumen_eventos"]["INFO"])
        evento = estado["eventos_recientes"][0]
        self.assertEqual("http.request", evento["event"])
        self.assertEqual("dev.centro_desarrollo", evento["metadata"]["operation"])
        self.assertEqual("GET", evento["metadata"]["method"])
        self.assertEqual(200, evento["metadata"]["status_code"])

        serializado = json.dumps(estado, ensure_ascii=False).casefold()
        for prohibido in (
            "juan",
            "4-123-456",
            "999.99",
            "salario",
            "cedula",
            "cédula",
            "nss",
            "token=",
        ):
            self.assertNotIn(prohibido, serializado)

    def test_visor_cuenta_lineas_jsonl_invalidas_sin_mostrar_contenido(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=True):
                ruta = ruta_log_actual()
                ruta.parent.mkdir(parents=True, exist_ok=True)
                ruta.write_text(
                    "{linea-invalida-con-dato-privado}\n"
                    + json.dumps(
                        {
                            "timestamp": "2026-08-23T10:01:00.000+00:00",
                            "level": "WARNING",
                            "event": "http.request",
                            "component": "fastapi",
                            "outcome": "client_error",
                            "metadata": {
                                "operation": "http.other",
                                "status_code": 404,
                            },
                        }
                    )
                    + "\n",
                    encoding="utf-8",
                )

                estado = construir_estado_centro_desarrollo()

        self.assertEqual(1, estado["total_eventos_invalidos"])
        self.assertEqual(1, estado["total_eventos_visibles"])
        self.assertNotIn(
            "linea-invalida-con-dato-privado",
            json.dumps(estado, ensure_ascii=False),
        )

    def test_exportacion_zip_sanitizada_requiere_modo_activo_y_archivo_existente(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=False):
                with self.assertRaises(PermissionError):
                    exportar_zip_diagnostico_sanitizado()

            with self._env(temp, activo=True):
                with self.assertRaises(FileNotFoundError):
                    exportar_zip_diagnostico_sanitizado()

                registrar_evento(
                    level="INFO",
                    event="dev.export",
                    component="dev.centro_desarrollo",
                    outcome="success",
                    metadata={"operation": "dev.centro_desarrollo"},
                )
                zip_path = exportar_zip_diagnostico_sanitizado()

                self.assertEqual("mrp-diagnostics-export.zip", zip_path.name)
                self.assertTrue(zip_path.is_file())
                with ZipFile(zip_path) as paquete:
                    self.assertIn("mrp-diagnostics.jsonl", paquete.namelist())
                    self.assertNotIn("VERSION", paquete.namelist())

    def test_ruta_centro_desarrollo_renderiza_visor_r2(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=True):
                registrar_evento(
                    level="ERROR",
                    event="dev.test",
                    component="dev.centro_desarrollo",
                    outcome="error",
                    metadata={
                        "operation": "dev.centro_desarrollo",
                        "method": "GET",
                        "status_code": 500,
                    },
                )
                respuesta = TestClient(app).get("/dev/centro-desarrollo")

        self.assertEqual(200, respuesta.status_code)
        self.assertIn("DEV.2 R2", respuesta.text)
        self.assertIn("Eventos recientes", respuesta.text)
        self.assertIn("Resumen del visor diagnóstico", respuesta.text)
        self.assertIn("dev.centro_desarrollo", respuesta.text)
        self.assertNotIn("request.body", respuesta.text)
        self.assertNotIn("token=", respuesta.text.casefold())


if __name__ == "__main__":
    unittest.main()
