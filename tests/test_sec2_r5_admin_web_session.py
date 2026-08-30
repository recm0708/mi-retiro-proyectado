"""SEC.2 R5 — Regresiones históricas de sesión web reconciliadas con R6."""

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


class TestSec2AdminWebSession(unittest.TestCase):
    """Preserva propiedades SEC.2 sobre el contrato humano vigente."""

    PASSWORD = "MRP-Sec2!Owner-2026"

    def tearDown(self):
        """Revoca sesiones web después de cada prueba."""

        revocar_todas_las_sesiones_admin()

    @staticmethod
    @contextmanager
    def _env(temp: str):
        """Aísla la base Developer y el entorno administrativo."""

        store = Path(temp) / "portal.sqlite3"

        with patch.dict(
            os.environ,
            {
                "MRP_DIAGNOSTIC_DIR": temp,
                "MRP_DEV_MODE": "1",
                "MRP_ADMIN_ENABLED": "1",
                "MRP_ADMIN_SECRET": "test-admin-secret",
                "MRP_DEVELOPER_STORE_PATH": str(store),
            },
            clear=True,
        ):
            bootstrap_propietario(
                usuario="propietario",
                nombre_visible="Propietario SEC.2",
                password=TestSec2AdminWebSession.PASSWORD,
            )

            yield

    @classmethod
    def _login_data(cls) -> dict[str, str]:
        """Devuelve las credenciales humanas usadas por la regresión."""

        return {
            "usuario": "propietario",
            "password": cls.PASSWORD,
        }

    def test_login_renderiza_formulario(self):
        """La URL histórica conduce al formulario humano vigente."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(
                    app
                ).get(
                    "/dev/login"
                )

        self.assertEqual(
            200,
            respuesta.status_code,
        )
        self.assertIn(
            "Acceso restringido",
            respuesta.text,
        )
        self.assertIn(
            "Iniciar sesión",
            respuesta.text,
        )
        self.assertIn(
            'name="usuario"',
            respuesta.text,
        )
        self.assertIn(
            'name="password"',
            respuesta.text,
        )

    def test_login_valido_crea_cookie_y_redirecciona(self):
        """Una identidad válida crea la cookie web administrativa."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(
                    app
                ).post(
                    "/dev/login",
                    data=self._login_data(),
                    follow_redirects=False,
                )

        self.assertEqual(
            303,
            respuesta.status_code,
        )
        self.assertEqual(
            "/dev",
            respuesta.headers["location"],
        )
        self.assertIn(
            "mrp_admin_session",
            respuesta.headers.get(
                "set-cookie",
                "",
            ),
        )

    def test_centro_desarrollo_permite_sesion_valida(self):
        """Una sesión humana válida se dirige a la entrada canónica."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)

                login = cliente.post(
                    "/dev/login",
                    data=self._login_data(),
                    follow_redirects=False,
                )

                self.assertEqual(
                    303,
                    login.status_code,
                )

                respuesta = cliente.get(
                    "/dev/centro-desarrollo",
                    headers={
                        "Accept": "text/html",
                    },
                    follow_redirects=False,
                )

        self.assertEqual(
            303,
            respuesta.status_code,
        )
        self.assertEqual(
            "/dev",
            respuesta.headers["location"],
        )

    def test_logout_redirecciona_login(self):
        """El cierre de sesión devuelve al acceso canónico Developer."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)

                cliente.post(
                    "/dev/login",
                    data=self._login_data(),
                )

                pagina = cliente.get("/dev")
                self.assertEqual(200, pagina.status_code)

                marca_csrf = 'name="csrf_token"'
                self.assertIn(
                    marca_csrf,
                    pagina.text,
                )

                fragmento_csrf = pagina.text.split(
                    marca_csrf,
                    1,
                )[1]

                csrf_token = fragmento_csrf.split(
                    'value="',
                    1,
                )[1].split(
                    '"',
                    1,
                )[0]

                respuesta = cliente.post(
                    "/dev/logout",
                    data={
                        "csrf_token": csrf_token,
                    },
                    follow_redirects=False,
                )

        self.assertEqual(
            303,
            respuesta.status_code,
        )
        self.assertEqual(
            "/dev",
            respuesta.headers["location"],
        )


if __name__ == "__main__":
    unittest.main()
