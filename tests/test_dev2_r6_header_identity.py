"""DEV.2 R6 — Identidad visual y menú humano del Portal Developer."""

from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path
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


class TestDev2R6HeaderIdentity(unittest.TestCase):
    """Protege el shell autenticado y el menú de identidad Developer."""

    PASSWORD = "MRP-Header!Owner-2026"

    def tearDown(self):
        """Revoca las sesiones generadas por cada prueba."""

        revocar_todas_las_sesiones_admin()

    @staticmethod
    @contextmanager
    def _env(temp: str):
        """Crea un propietario aislado para las pruebas del header."""

        store = Path(temp) / "portal.sqlite3"

        with patch.dict(
            os.environ,
            {
                "MRP_DIAGNOSTIC_DIR": temp,
                "MRP_DEV_MODE": "1",
                "MRP_ADMIN_ENABLED": "1",
                "MRP_DEVELOPER_STORE_PATH": str(store),
            },
            clear=True,
        ):
            bootstrap_propietario(
                usuario="propietario",
                nombre_visible="Rubén Cañizares",
                password=TestDev2R6HeaderIdentity.PASSWORD,
            )
            yield

    @classmethod
    def _login(cls, cliente: TestClient) -> None:
        """Inicia la sesión del propietario de pruebas."""

        respuesta = cliente.post(
            "/dev",
            data={
                "usuario": "propietario",
                "password": cls.PASSWORD,
            },
            follow_redirects=False,
        )

        if respuesta.status_code != 303:
            raise AssertionError(
                "No se pudo preparar la sesión Developer."
            )

    def test_header_muestra_nombre_rol_e_iniciales(self):
        """La sesión expone identidad reconocible sin mostrar secretos."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                self._login(cliente)
                respuesta = cliente.get("/dev")

        self.assertEqual(
            200,
            respuesta.status_code,
        )
        self.assertIn(
            "Rubén Cañizares",
            respuesta.text,
        )
        self.assertIn(
            "Propietario",
            respuesta.text,
        )
        self.assertRegex(
            respuesta.text,
            r'class="dev-avatar"[^>]*>\s*RC\s*</span>',
        )

    def test_menu_usuario_enlaza_perfil_y_acceso_tecnico(self):
        """La cuenta centraliza sus superficies personales."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                self._login(cliente)
                respuesta = cliente.get("/dev")

        self.assertIn(
            'href="/dev/perfil"',
            respuesta.text,
        )
        self.assertIn(
            'href="/dev/acceso-tecnico"',
            respuesta.text,
        )

    def test_perfil_exige_sesion(self):
        """El perfil no se expone sin autenticación humana."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(app).get(
                    "/dev/perfil",
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

    def test_acceso_tecnico_exige_sesion(self):
        """La gestión técnica visual tampoco es pública."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                respuesta = TestClient(app).get(
                    "/dev/acceso-tecnico",
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

    def test_perfil_renderiza_datos_no_secretos(self):
        """El perfil muestra metadata de cuenta pero no hashes."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                self._login(cliente)

                respuesta = cliente.get(
                    "/dev/perfil"
                )

        self.assertEqual(
            200,
            respuesta.status_code,
        )
        self.assertIn(
            "Rubén Cañizares",
            respuesta.text,
        )
        self.assertIn(
            "@propietario",
            respuesta.text,
        )
        self.assertNotIn(
            "$argon2id$",
            respuesta.text,
        )
        self.assertNotIn(
            self.PASSWORD,
            respuesta.text,
        )

    def test_acceso_tecnico_declara_bearer_separado(self):
        """La página técnica conserva la separación de credenciales."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                self._login(cliente)

                respuesta = cliente.get(
                    "/dev/acceso-tecnico"
                )

        self.assertEqual(
            200,
            respuesta.status_code,
        )
        self.assertIn(
            "Authorization: Bearer",
            respuesta.text,
        )
        self.assertIn(
            "separadas de tu contraseña",
            respuesta.text,
        )


if __name__ == "__main__":
    unittest.main()
