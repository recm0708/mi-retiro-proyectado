"""Regresiones de saneamiento post-cierre para SEC.2.

Protege el kill switch administrativo, la prioridad de errores 403 sobre la
sesión web, el cierre de sesión mediante POST y la no reutilización de páginas
administrativas desde caché HTTP.
"""

from __future__ import annotations

import os
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.admin_session import revocar_todas_las_sesiones_admin
from app.main import app


class TestSec2PostClosureHardening(unittest.TestCase):
    """Valida correcciones detectadas durante la auditoría post-SEC.2."""

    def tearDown(self):
        revocar_todas_las_sesiones_admin()

    @staticmethod
    def _env(temp: str, enabled: str = "1"):
        return patch.dict(
            os.environ,
            {
                "MRP_DIAGNOSTIC_DIR": temp,
                "MRP_DEV_MODE": "1",
                "MRP_ADMIN_ENABLED": enabled,
                "MRP_ADMIN_SECRET": "test-admin-secret",
            },
            clear=True,
        )

    def test_post_login_respeta_kill_switch(self):
        with TemporaryDirectory() as temp:
            with self._env(temp, enabled=""):
                respuesta = TestClient(app).post(
                    "/dev/login",
                    data={"token": "test-admin-secret"},
                    follow_redirects=False,
                )

        self.assertEqual(403, respuesta.status_code)
        self.assertNotIn(
            "mrp_admin_session",
            respuesta.headers.get("set-cookie", ""),
        )

    def test_sesion_existente_no_anula_kill_switch(self):
        with TemporaryDirectory() as temp:
            cliente = TestClient(app)

            with self._env(temp):
                login = cliente.post(
                    "/dev/login",
                    data={"token": "test-admin-secret"},
                    follow_redirects=False,
                )
                self.assertEqual(303, login.status_code)

            with self._env(temp, enabled=""):
                respuesta = cliente.get(
                    "/dev/centro-desarrollo",
                    headers={"Accept": "text/html"},
                    follow_redirects=False,
                )

        self.assertEqual(403, respuesta.status_code)

    def test_bearer_invalido_no_se_sustituye_por_sesion(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                cliente.post(
                    "/dev/login",
                    data={"token": "test-admin-secret"},
                )

                respuesta = cliente.get(
                    "/dev/centro-desarrollo",
                    headers={
                        "Authorization": "Bearer incorrecto",
                        "Accept": "text/html",
                    },
                    follow_redirects=False,
                )

        self.assertEqual(403, respuesta.status_code)

    def test_logout_solo_modifica_estado_mediante_post(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                cliente.post(
                    "/dev/login",
                    data={"token": "test-admin-secret"},
                )

                get_logout = cliente.get(
                    "/dev/logout",
                    follow_redirects=False,
                )
                post_logout = cliente.post(
                    "/dev/logout",
                    follow_redirects=False,
                )

        self.assertEqual(405, get_logout.status_code)
        self.assertEqual(303, post_logout.status_code)
        self.assertEqual("/dev/login", post_logout.headers["location"])

    def test_paginas_admin_no_se_guardan_en_cache(self):
        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                login_get = cliente.get("/dev/login")
                cliente.post(
                    "/dev/login",
                    data={"token": "test-admin-secret"},
                )
                centro = cliente.get("/dev/centro-desarrollo")

        self.assertEqual("no-store", login_get.headers.get("cache-control"))
        self.assertEqual("no-store", centro.headers.get("cache-control"))

    def test_portal_expone_cierre_de_sesion_post(self):
        plantilla = (
            __import__("pathlib").Path(__file__).resolve().parents[1]
            / "app/templates/dev_development_center.html"
        ).read_text(encoding="utf-8")

        self.assertIn('method="post"', plantilla)
        self.assertIn('action="/dev/logout"', plantilla)
        self.assertIn("Cerrar sesión", plantilla)


if __name__ == "__main__":
    unittest.main()
