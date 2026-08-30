"""Regresiones de saneamiento post-cierre para SEC.2.

Protege el kill switch administrativo, la prioridad de errores 403 sobre la
sesión web, el cierre de sesión mediante POST y la no reutilización de páginas
administrativas desde caché HTTP.
"""

from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path
import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.admin_session import (
    revocar_todas_las_sesiones_admin,
)
from app.core.developer_provisioning import (
    bootstrap_propietario,
)
from app.main import app


class TestSec2PostClosureHardening(unittest.TestCase):
    """Valida correcciones de seguridad conservadas después de SEC.2."""

    PASSWORD = "MRP-Sec2!Owner-2026"

    def tearDown(self):
        """Revoca las sesiones creadas durante cada regresión."""

        revocar_todas_las_sesiones_admin()

    @staticmethod
    @contextmanager
    def _env(
        temp: str,
        enabled: str = "1",
    ):
        """Aísla la identidad humana y el Bearer técnico de la prueba."""

        store = Path(temp) / "portal.sqlite3"

        with patch.dict(
            os.environ,
            {
                "MRP_DIAGNOSTIC_DIR": temp,
                "MRP_DEV_MODE": "1",
                "MRP_ADMIN_ENABLED": enabled,
                "MRP_ADMIN_SECRET": "test-admin-secret",
                "MRP_DEVELOPER_STORE_PATH": str(store),
            },
            clear=True,
        ):
            if not store.exists():
                bootstrap_propietario(
                    usuario="propietario",
                    nombre_visible="Propietario SEC.2",
                    password=(
                        TestSec2PostClosureHardening.PASSWORD
                    ),
                )

            yield

    @classmethod
    def _login_data(cls) -> dict[str, str]:
        """Devuelve credenciales humanas aisladas para las pruebas."""

        return {
            "usuario": "propietario",
            "password": cls.PASSWORD,
        }

    def test_post_login_respeta_kill_switch(self):
        """El kill switch prevalece incluso sobre formularios inválidos."""

        with TemporaryDirectory() as temp:
            with self._env(
                temp,
                enabled="",
            ):
                respuesta = TestClient(
                    app
                ).post(
                    "/dev/login",
                    data={
                        "token": "test-admin-secret",
                    },
                    follow_redirects=False,
                )

        self.assertEqual(
            403,
            respuesta.status_code,
        )
        self.assertNotIn(
            "mrp_admin_session",
            respuesta.headers.get(
                "set-cookie",
                "",
            ),
        )

    def test_sesion_existente_no_anula_kill_switch(self):
        """Una sesión válida deja de autorizar cuando se desactiva DEV."""

        with TemporaryDirectory() as temp:
            cliente = TestClient(app)

            with self._env(temp):
                login = cliente.post(
                    "/dev/login",
                    data=self._login_data(),
                    follow_redirects=False,
                )

                self.assertEqual(
                    303,
                    login.status_code,
                )

            with self._env(
                temp,
                enabled="",
            ):
                respuesta = cliente.get(
                    "/dev/centro-desarrollo",
                    headers={
                        "Accept": "text/html",
                    },
                    follow_redirects=False,
                )

        self.assertEqual(
            403,
            respuesta.status_code,
        )

    def test_bearer_invalido_no_se_sustituye_por_sesion(self):
        """Un Bearer explícito inválido no cae a la sesión humana."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)

                cliente.post(
                    "/dev/login",
                    data=self._login_data(),
                )

                respuesta = cliente.get(
                    "/dev/centro-desarrollo",
                    headers={
                        "Authorization": (
                            "Bearer incorrecto"
                        ),
                        "Accept": "text/html",
                    },
                    follow_redirects=False,
                )

        self.assertEqual(
            403,
            respuesta.status_code,
        )

    def test_logout_solo_modifica_estado_mediante_post(self):
        """El cierre de sesión continúa siendo una operación POST."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)

                cliente.post(
                    "/dev/login",
                    data=self._login_data(),
                )

                get_logout = cliente.get(
                    "/dev/logout",
                    follow_redirects=False,
                )
                post_logout = cliente.post(
                    "/dev/logout",
                    follow_redirects=False,
                )

        self.assertEqual(
            405,
            get_logout.status_code,
        )
        self.assertEqual(
            303,
            post_logout.status_code,
        )
        self.assertEqual(
            "/dev",
            post_logout.headers["location"],
        )

    def test_paginas_admin_no_se_guardan_en_cache(self):
        """Las páginas Developer mantienen Cache-Control no-store."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)

                login_get = cliente.get(
                    "/dev/login"
                )

                cliente.post(
                    "/dev/login",
                    data=self._login_data(),
                )

                centro = cliente.get(
                    "/dev/centro-desarrollo"
                )

        self.assertEqual(
            "no-store",
            login_get.headers.get(
                "cache-control"
            ),
        )
        self.assertEqual(
            "no-store",
            centro.headers.get(
                "cache-control"
            ),
        )

    def test_portal_expone_cierre_de_sesion_post(self):
        """El shell mantiene el formulario POST de cierre de sesión."""

        plantilla = (
            Path(__file__).resolve().parents[1]
            / "app/templates/dev_base.html"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'method="post"',
            plantilla,
        )
        self.assertIn(
            'action="/dev/logout"',
            plantilla,
        )
        self.assertIn(
            "Cerrar sesión",
            plantilla,
        )


if __name__ == "__main__":
    unittest.main()
