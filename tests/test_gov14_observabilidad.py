"""Regresiones de GOV.1.4 R1: núcleo de Developer Diagnostics."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from zipfile import ZipFile

import app.core.observabilidad as observabilidad
from app.core.observabilidad import (
    SCHEMA_VERSION,
    contexto_correlacion,
    correlacion_actual,
    exportar_diagnostico,
    modo_desarrollo_activo,
    registrar_evento,
    registrar_excepcion,
    ruta_log_actual,
)


class TestGov14ObservabilidadR1(unittest.TestCase):
    def _entorno(self, directorio: str, *, activo: bool = True):
        valores = {
            "MRP_DIAGNOSTIC_DIR": directorio,
        }
        if activo:
            valores["MRP_DEV_MODE"] = "1"
        return patch.dict(os.environ, valores, clear=True)

    def test_modo_desarrollo_desactivado_por_defecto_y_no_escribe(self):
        with TemporaryDirectory() as temp:
            with self._entorno(temp, activo=False):
                self.assertFalse(modo_desarrollo_activo())
                escrito = registrar_evento(
                    level="INFO",
                    event="test.off",
                    component="tests",
                    outcome="success",
                )
                self.assertFalse(escrito)
                self.assertFalse(ruta_log_actual().exists())

    def test_modo_activo_escribe_schema_jsonl_esperado(self):
        with TemporaryDirectory() as temp:
            with self._entorno(temp):
                with contexto_correlacion("a" * 32):
                    self.assertTrue(
                        registrar_evento(
                            level="info",
                            event="test.schema",
                            component="tests",
                            outcome="success",
                            duration_ms=12.34567,
                            metadata={"count": 3},
                        )
                    )

                linea = ruta_log_actual().read_text(
                    encoding="utf-8"
                ).splitlines()[0]
                evento = json.loads(linea)

                self.assertEqual(SCHEMA_VERSION, evento["schema_version"])
                self.assertEqual("INFO", evento["level"])
                self.assertEqual("test.schema", evento["event"])
                self.assertEqual("tests", evento["component"])
                self.assertEqual("success", evento["outcome"])
                self.assertEqual("a" * 32, evento["correlation_id"])
                self.assertEqual(12.346, evento["duration_ms"])
                self.assertEqual({"count": 3}, evento["metadata"])
                self.assertIn("app_version", evento)
                self.assertIn("+00:00", evento["timestamp"])

    def test_correlacion_es_aleatoria_no_derivada_y_se_restaura(self):
        self.assertIsNone(correlacion_actual())

        with contexto_correlacion() as primera:
            self.assertRegex(primera, r"^[0-9a-f]{32}$")
            self.assertEqual(primera, correlacion_actual())

        self.assertIsNone(correlacion_actual())

        with contexto_correlacion() as segunda:
            self.assertRegex(segunda, r"^[0-9a-f]{32}$")

        self.assertNotEqual(primera, segunda)
        self.assertIsNone(correlacion_actual())

    def test_metadata_sensible_se_redacta(self):
        with TemporaryDirectory() as temp:
            with self._entorno(temp):
                registrar_evento(
                    level="INFO",
                    event="test.redaction",
                    component="tests",
                    outcome="success",
                    metadata={
                        "cedula": "99-9999-9999",
                        "nombre": "Persona Sintética",
                        "salario": 1234.56,
                        "pdf_filename": "ficha.pdf",
                        "safe_count": 5,
                        "safe_label": "cache_hit",
                    },
                )

                contenido = ruta_log_actual().read_text(encoding="utf-8")
                self.assertNotIn("99-9999-9999", contenido)
                self.assertNotIn("Persona Sintética", contenido)
                self.assertNotIn("1234", contenido)
                self.assertNotIn("ficha.pdf", contenido)

                evento = json.loads(contenido)
                self.assertEqual("[REDACTED]", evento["metadata"]["cedula"])
                self.assertEqual("[REDACTED]", evento["metadata"]["nombre"])
                self.assertEqual("[REDACTED]", evento["metadata"]["salario"])
                self.assertEqual(
                    "[REDACTED]",
                    evento["metadata"]["pdf_filename"],
                )
                self.assertEqual(5, evento["metadata"]["safe_count"])

    def test_excepcion_no_persiste_mensaje_original(self):
        with TemporaryDirectory() as temp:
            with self._entorno(temp):
                error = ValueError(
                    "Error para 99-9999-9999 con salario B/.1234.56"
                )
                registrar_excepcion(
                    event="test.exception",
                    component="tests",
                    error=error,
                    metadata={"operation": "synthetic"},
                )

                contenido = ruta_log_actual().read_text(encoding="utf-8")
                self.assertNotIn("99-9999-9999", contenido)
                self.assertNotIn("1234", contenido)
                self.assertNotIn(str(error), contenido)

                evento = json.loads(contenido)
                self.assertEqual(
                    "ValueError",
                    evento["metadata"]["exception_type"],
                )

    def test_rotacion_conserva_respaldo_sin_salir_del_directorio(self):
        with TemporaryDirectory() as temp:
            with self._entorno(temp):
                with patch.object(observabilidad, "_MAX_BYTES", 350):
                    for indice in range(5):
                        registrar_evento(
                            level="INFO",
                            event="test.rotation",
                            component="tests",
                            outcome="success",
                            metadata={"count": indice},
                        )

                actual = ruta_log_actual()
                respaldo = actual.with_suffix(actual.suffix + ".1")
                self.assertTrue(actual.is_file())
                self.assertTrue(respaldo.is_file())
                self.assertEqual(actual.parent, respaldo.parent)

    def test_exportacion_controlada_incluye_solo_logs_diagnosticos(self):
        with TemporaryDirectory() as temp:
            base = Path(temp)
            with self._entorno(str(base)):
                registrar_evento(
                    level="INFO",
                    event="test.export",
                    component="tests",
                    outcome="success",
                )
                (base / "documento_personal.pdf").write_bytes(b"secret")
                (base / "otra_cosa.txt").write_text(
                    "no exportar",
                    encoding="utf-8",
                )

                salida = exportar_diagnostico(base / "export.zip")
                self.assertTrue(salida.is_file())

                with ZipFile(salida) as paquete:
                    nombres = paquete.namelist()

                self.assertEqual(["mrp-diagnostics.jsonl"], nombres)
                self.assertNotIn("documento_personal.pdf", nombres)
                self.assertNotIn("otra_cosa.txt", nombres)


if __name__ == "__main__":
    unittest.main()
