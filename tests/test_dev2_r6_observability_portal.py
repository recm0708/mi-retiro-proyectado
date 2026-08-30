"""Regresiones DEV.2 R6.2-R6.4: observabilidad del Portal Developer."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from app.core.observability import ruta_log_actual
from app.services.development_center import (
    construir_estado_centro_desarrollo,
)


ROOT = Path(__file__).resolve().parents[1]


class TestDev2R6ObservabilityPortal(unittest.TestCase):
    @staticmethod
    def _env(temp: str, *, activo: bool = True):
        return patch.dict(
            os.environ,
            {
                "MRP_DIAGNOSTIC_DIR": temp,
                "MRP_DEV_MODE": "1" if activo else "",
                "MRP_ADMIN_ENABLED": "1",
            },
            clear=False,
        )

    def test_estado_expone_runtime_seguro_y_tamanos_legibles(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                ruta = ruta_log_actual()
                ruta.parent.mkdir(parents=True, exist_ok=True)
                ruta.write_text(
                    json.dumps(
                        {
                            "timestamp": "2026-08-30T00:00:00+00:00",
                            "level": "INFO",
                            "event": "dev.observability",
                            "component": "developer",
                            "outcome": "success",
                            "metadata": {
                                "operation": "dev.eventos",
                                "salario": "B/. 999.99",
                                "cedula": "4-123-456",
                            },
                        }
                    ) + "\n",
                    encoding="utf-8",
                )

                estado = construir_estado_centro_desarrollo()

        self.assertEqual(
            "DEV.2 R6.4",
            estado["revision_portal_observabilidad"],
        )
        self.assertIn("python", estado["entorno_runtime"])
        self.assertIn("sistema", estado["entorno_runtime"])
        self.assertIn("arquitectura", estado["entorno_runtime"])
        self.assertIn("total_bytes_legible", estado)
        self.assertEqual(
            200,
            estado["limite_eventos_visibles"],
        )

        serializado = json.dumps(
            estado,
            ensure_ascii=False,
        ).casefold()

        self.assertNotIn(temp.casefold(), serializado)
        self.assertNotIn("4-123-456", serializado)
        self.assertNotIn("999.99", serializado)
        self.assertNotIn("salario", serializado)
        self.assertNotIn("cedula", serializado)

    def test_visor_acota_eventos_a_doscientos(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                ruta = ruta_log_actual()
                ruta.parent.mkdir(parents=True, exist_ok=True)

                lineas = []

                for indice in range(225):
                    lineas.append(
                        json.dumps(
                            {
                                "timestamp": (
                                    "2026-08-30T"
                                    f"{indice % 24:02d}:"
                                    f"{indice % 60:02d}:00+00:00"
                                ),
                                "level": "INFO",
                                "event": f"dev.event.{indice}",
                                "component": "developer",
                                "outcome": "success",
                                "metadata": {
                                    "operation": "dev.eventos",
                                },
                            }
                        )
                    )

                ruta.write_text(
                    "\n".join(lineas) + "\n",
                    encoding="utf-8",
                )

                estado = construir_estado_centro_desarrollo()

        self.assertEqual(
            200,
            estado["total_eventos_visibles"],
        )

    def test_eventos_incluye_busqueda_filtro_y_paginacion(self):
        plantilla = (
            ROOT
            / "app"
            / "templates"
            / "dev_events.html"
        ).read_text(encoding="utf-8")

        for contrato in (
            "data-dev-event-search",
            "data-dev-event-level",
            "data-dev-event-page-size",
            "data-dev-event-prev",
            "data-dev-event-next",
            "data-dev-event-reset",
        ):
            self.assertIn(contrato, plantilla)

    def test_javascript_implementa_visor_sin_persistencia(self):
        script = (
            ROOT
            / "app"
            / "static"
            / "js"
            / "developer_portal.js"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "function iniciarVisorEventos()",
            script,
        )
        self.assertNotIn("localStorage", script)
        self.assertNotIn("sessionStorage", script)

    def test_archivos_expone_exportacion_sanitizada(self):
        plantilla = (
            ROOT
            / "app"
            / "templates"
            / "dev_files.html"
        ).read_text(encoding="utf-8")

        self.assertIn(
            'action="/dev/archivos/exportar"',
            plantilla,
        )
        self.assertIn(
            "Descargar ZIP sanitizado",
            plantilla,
        )
        self.assertIn(
            "Nunca se muestra la ruta absoluta",
            plantilla,
        )

    def test_main_protege_exportacion_con_sesion_humana(self):
        main = (
            ROOT
            / "app"
            / "main.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            '"/dev/archivos/exportar"',
            main,
        )
        self.assertIn(
            "_obtener_usuario_sesion_web(request)",
            main,
        )
        self.assertIn(
            "exportar_zip_diagnostico_sanitizado",
            main,
        )


if __name__ == "__main__":
    unittest.main()
