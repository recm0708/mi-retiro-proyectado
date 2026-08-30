"""DEV.2 R6 — Autenticación humana del Portal Developer."""

from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.admin_session import (
    revocar_todas_las_sesiones_admin,
)
from app.core.developer_provisioning import (
    bootstrap_propietario,
)
from app.main import app


class TestDev2R6WebAccess(unittest.TestCase):
    """Protege la separación entre sesión humana y Bearer técnico."""

    PASSWORD = "MRP-Web!Owner-2026"

    def tearDown(self):
        """Revoca sesiones globales después de cada prueba."""

        revocar_todas_las_sesiones_admin()

    @staticmethod
    @contextmanager
    def _env(
        temp: str,
        *,
        bearer: bool = True,
    ):
        """Crea un entorno Developer completamente aislado."""

        store = str(
            Path(temp)
            / "portal.sqlite3"
        )

        entorno = {
            "MRP_DIAGNOSTIC_DIR": temp,
            "MRP_DEV_MODE": "1",
            "MRP_ADMIN_ENABLED": "1",
            "MRP_DEVELOPER_STORE_PATH": store,
        }

        if bearer:
            entorno["MRP_ADMIN_SECRET"] = (
                "test-admin-secret"
            )

        with patch.dict(
            os.environ,
            entorno,
            clear=True,
        ):
            bootstrap_propietario(
                usuario="propietario",
                nombre_visible=(
                    "Propietario de prueba"
                ),
                password=TestDev2R6WebAccess.PASSWORD,
            )
            yield Path(store)

    @classmethod
    def _credenciales(cls) -> dict[str, str]:
        """Devuelve el login humano de prueba."""

        return {
            "usuario": "propietario",
            "password": cls.PASSWORD,
        }

    def test_login_muestra_usuario_y_password(self):
        """El formulario humano ya no solicita el secreto Bearer."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(
                    app
                ).get("/dev")

        self.assertEqual(
            200,
            respuesta.status_code,
        )
        self.assertIn(
            'name="usuario"',
            respuesta.text,
        )
        self.assertIn(
            'name="password"',
            respuesta.text,
        )
        self.assertNotIn(
            'name="token"',
            respuesta.text,
        )
        self.assertNotIn(
            "Credencial administrativa",
            respuesta.text,
        )

    def test_login_humano_no_depende_del_bearer(self):
        """La cuenta web funciona aunque no exista MRP_ADMIN_SECRET."""

        with TemporaryDirectory() as temp:
            with self._env(
                temp,
                bearer=False,
            ):
                respuesta = TestClient(
                    app
                ).post(
                    "/dev",
                    data=self._credenciales(),
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

    def test_login_invalido_usa_error_generico(self):
        """Un fallo no revela si usuario o contraseña fue incorrecto."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(
                    app
                ).post(
                    "/dev",
                    data={
                        "usuario": "propietario",
                        "password": "Incorrecta!2026",
                    },
                    follow_redirects=False,
                )

        self.assertEqual(
            401,
            respuesta.status_code,
        )
        self.assertIn(
            "Usuario o contraseña incorrectos.",
            respuesta.text,
        )
        self.assertNotIn(
            "mrp_admin_session=",
            respuesta.headers.get(
                "set-cookie",
                "",
            ),
        )

    def test_secreto_bearer_no_inicia_sesion_humana(self):
        """El contrato token= de R5 deja de autenticar navegadores."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(
                    app
                ).post(
                    "/dev",
                    data={
                        "token": "test-admin-secret",
                    },
                    follow_redirects=False,
                )

        self.assertEqual(
            422,
            respuesta.status_code,
        )
        self.assertNotIn(
            "mrp_admin_session=",
            respuesta.headers.get(
                "set-cookie",
                "",
            ),
        )

    def test_login_valido_crea_sesion_identificada(self):
        """Una cuenta válida recibe cookie sin exponer su contraseña."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(
                    app
                ).post(
                    "/dev",
                    data=self._credenciales(),
                    follow_redirects=False,
                )

        cookie = respuesta.headers.get(
            "set-cookie",
            "",
        )

        self.assertEqual(
            303,
            respuesta.status_code,
        )
        self.assertIn(
            "mrp_admin_session=",
            cookie,
        )
        self.assertIn(
            "HttpOnly",
            cookie,
        )
        self.assertIn(
            "Path=/dev",
            cookie,
        )
        self.assertNotIn(
            self.PASSWORD,
            cookie,
        )

    def test_revision_seguridad_nueva_revoca_cookie(self):
        """Una revisión persistente distinta invalida la sesión previa."""

        with TemporaryDirectory() as temp:
            with self._env(temp) as store:
                cliente = TestClient(app)

                login = cliente.post(
                    "/dev",
                    data=self._credenciales(),
                    follow_redirects=False,
                )
                self.assertEqual(
                    303,
                    login.status_code,
                )

                conexion = sqlite3.connect(
                    store
                )
                try:
                    conexion.execute(
                        """
                        UPDATE developer_users
                        SET security_version =
                            security_version + 1
                        WHERE username = ?
                        """,
                        ("propietario",),
                    )
                    conexion.commit()
                finally:
                    conexion.close()

                respuesta = cliente.get(
                    "/dev"
                )

        self.assertEqual(
            200,
            respuesta.status_code,
        )
        self.assertIn(
            "Iniciar sesión",
            respuesta.text,
        )
        self.assertNotIn(
            "Centro de desarrollo",
            respuesta.text,
        )

    def test_bearer_legacy_continua_separado(self):
        """El Bearer R5 permanece disponible en su endpoint técnico."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(
                    app
                ).get(
                    "/dev/centro-desarrollo",
                    headers={
                        "Authorization": (
                            "Bearer "
                            "test-admin-secret"
                        )
                    },
                    follow_redirects=False,
                )

        self.assertEqual(
            200,
            respuesta.status_code,
        )
        self.assertIn(
            "Centro de desarrollo",
            respuesta.text,
        )


if __name__ == "__main__":
    unittest.main()
