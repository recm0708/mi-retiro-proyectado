"""GOV.1.4 R2: integración HTTP y consulta externa observable."""

from __future__ import annotations

from datetime import date
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app import main as main_module
from app.core.observability import contexto_correlacion, ruta_log_actual
from app.main import app
from app.services import reference_date

fecha_referencia = reference_date


ROOT = Path(__file__).resolve().parents[1]


class TestGov14ObservabilidadIntegracion(unittest.TestCase):
    @staticmethod
    def _eventos() -> list[dict]:
        ruta = ruta_log_actual()
        if not ruta.is_file():
            return []
        return [
            json.loads(linea)
            for linea in ruta.read_text(encoding="utf-8").splitlines()
            if linea.strip()
        ]

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

    def setUp(self):
        reference_date._cache_resultado = None
        reference_date._cache_instante = 0.0

    def test_middleware_apagado_no_agrega_header_ni_log(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=False):
                respuesta = TestClient(app).get("/salud")
                self.assertEqual(200, respuesta.status_code)
                self.assertNotIn("x-correlation-id", respuesta.headers)
                self.assertEqual([], self._eventos())

    def test_middleware_activo_registra_solo_metadata_tecnica(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=True):
                respuesta = TestClient(app).get("/salud")
                self.assertEqual(200, respuesta.status_code)
                correlation = respuesta.headers.get("x-correlation-id")
                self.assertRegex(correlation or "", r"^[0-9a-f]{32}$")

                eventos = [
                    e for e in self._eventos()
                    if e["event"] == "http.request"
                ]
                self.assertEqual(1, len(eventos))
                evento = eventos[0]
                self.assertEqual(correlation, evento["correlation_id"])
                self.assertEqual("GET", evento["metadata"]["method"])
                self.assertEqual(
                    "system.health",
                    evento["metadata"]["operation"],
                )
                self.assertEqual(200, evento["metadata"]["status_code"])
                contenido = ruta_log_actual().read_text(encoding="utf-8")
                self.assertNotIn("request.body", contenido)
                self.assertNotIn("cookie", contenido.casefold())

    def test_observabilidad_no_ejecuta_dos_veces_el_calculo(self):
        payload = {
            "cuotas_totales": 281,
            "cuotas_anio_actual": 5,
            "continua_cotizando": True,
            "cuotas_esperadas_cierre_anio": 12,
            "cuotas_esperadas_por_anio": 12,
        }
        original = main_module.analizar_cuotas

        with TemporaryDirectory() as temp:
            with self._env(temp, activo=True):
                with patch.object(
                    main_module,
                    "analizar_cuotas",
                    wraps=original,
                ) as calculo:
                    respuesta = TestClient(app).post(
                        "/api/simulacion/cuotas",
                        json=payload,
                    )

                self.assertEqual(200, respuesta.status_code)
                self.assertEqual(1, calculo.call_count)
                contenido = ruta_log_actual().read_text(encoding="utf-8")
                self.assertNotIn("cuotas_totales", contenido)
                self.assertNotIn("cuotas_anio_actual", contenido)

    def test_error_no_controlado_no_expone_mensaje_ni_datos_en_log(self):
        secreto = "ID-SINTETICO-XYZ con monto B/.1234.56"
        cliente = TestClient(app, raise_server_exceptions=False)

        with TemporaryDirectory() as temp:
            with self._env(temp, activo=True):
                with patch.object(
                    main_module,
                    "analizar_cuotas",
                    side_effect=RuntimeError(secreto),
                ):
                    respuesta = cliente.post(
                        "/api/simulacion/cuotas",
                        json={
                            "cuotas_totales": 10,
                            "cuotas_anio_actual": 1,
                            "continua_cotizando": True,
                            "cuotas_esperadas_cierre_anio": 12,
                            "cuotas_esperadas_por_anio": 12,
                        },
                    )

                self.assertEqual(500, respuesta.status_code)
                self.assertNotIn(secreto, respuesta.text)
                contenido = ruta_log_actual().read_text(encoding="utf-8")
                self.assertNotIn(secreto, contenido)
                self.assertNotIn("1234.56", contenido)
                eventos = [
                    e for e in self._eventos()
                    if e["event"] == "http.request"
                ]
                self.assertEqual(1, len(eventos))
                self.assertEqual("error", eventos[0]["outcome"])
                self.assertTrue(
                    eventos[0]["metadata"].get("exception_type")
                )

    def test_fecha_externa_registra_cache_y_consulta_sin_urls_ni_fecha(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, activo=True):
                with contexto_correlacion("b" * 32):
                    with patch.object(
                        fecha_referencia,
                        "_consultar_fecha_http",
                        return_value=date(2026, 8, 17),
                    ) as consulta:
                        primera = reference_date.obtener_fecha_referencia_confiable(
                            forzar=True
                        )
                        segunda = reference_date.obtener_fecha_referencia_confiable()

                self.assertTrue(primera.confiable)
                self.assertEqual(primera, segunda)
                self.assertEqual(2, consulta.call_count)

                eventos = self._eventos()
                outcomes_cache = [
                    e["outcome"]
                    for e in eventos
                    if e["event"] == "external.date_reference.cache"
                ]
                self.assertEqual(["miss", "hit"], outcomes_cache)
                consultas = [
                    e for e in eventos
                    if e["event"] == "external.date_reference.query"
                ]
                self.assertEqual(1, len(consultas))
                self.assertEqual("success", consultas[0]["outcome"])
                self.assertEqual(2, consultas[0]["metadata"]["source_count"])
                self.assertEqual(2, consultas[0]["metadata"]["success_count"])
                self.assertTrue(
                    all(e["correlation_id"] == "b" * 32 for e in eventos)
                )

                contenido = ruta_log_actual().read_text(encoding="utf-8")
                self.assertNotIn("https://", contenido)
                self.assertNotIn("2026-08-17", contenido)

    def test_gitignore_y_documentacion_protegen_logs_locales(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        documento = (ROOT / "docs/OBSERVABILIDAD_LOGS.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("logs/", gitignore)
        self.assertIn("MRP_DEV_MODE", documento)
        self.assertIn("no existe telemetría remota", documento.casefold())
        self.assertIn("cuerpos de solicitudes", documento)
        self.assertIn("mensajes originales de excepciones", documento)
        self.assertIn("**Estado:** Vigente — GOV.1.4 cerrado", documento)
        self.assertIn("487/487", documento)

        roadmap = (ROOT / "docs/ROADMAP.md").read_text(encoding="utf-8")
        indice = (ROOT / "docs/INDICE.md").read_text(encoding="utf-8")
        seguridad = (ROOT / "docs/SEGURIDAD_PRIVACIDAD.md").read_text(
            encoding="utf-8"
        )
        transparencia = (ROOT / "docs/TRANSPARENCIA.md").read_text(
            encoding="utf-8"
        )
        limitaciones = (ROOT / "docs/LIMITACIONES_CONOCIDAS.md").read_text(
            encoding="utf-8"
        )
        validacion = (ROOT / "docs/VALIDACION.md").read_text(
            encoding="utf-8"
        )
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn(
            "- [x] **GOV.1.4 — Observabilidad y Developer Diagnostics**",
            roadmap,
        )
        self.assertIn("(OBSERVABILIDAD_LOGS.md)", indice)
        self.assertIn("Developer Diagnostics", seguridad)
        self.assertIn("no es analítica de producto", transparencia)
        self.assertNotIn(
            "Developer Diagnostics todavía no existe",
            limitaciones,
        )
        self.assertIn("487 pruebas en `OK`", validacion)
        self.assertIn(
            "**GOV.1.4:** Observabilidad y Developer Diagnostics cerrado",
            readme,
        )


if __name__ == "__main__":
    unittest.main()
