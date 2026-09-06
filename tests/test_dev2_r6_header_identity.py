"""DEV.2 R6 — Identidad visual y menú humano del Portal Developer."""

from __future__ import annotations

from contextlib import contextmanager
import os
import re
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.core.admin_session import (
    revocar_todas_las_sesiones_admin,
)
from app.core.developer_identity import (
    RolDeveloper,
    hashear_password,
)
from app.core.developer_provisioning import (
    bootstrap_propietario,
)
from app.core.developer_store import (
    crear_usuario_developer,
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

    def test_perfil_publica_edicion_y_avatar(self):
        """El perfil ofrece nombre y foto sin exponer secretos."""

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

        for esperado in (
            'action="/dev/perfil/datos"',
            'action="/dev/perfil/avatar"',
            'name="nombre_visible"',
            'name="avatar"',
            'accept="image/png,image/jpeg,image/webp"',
        ):
            with self.subTest(
                esperado=esperado
            ):
                self.assertIn(
                    esperado,
                    respuesta.text,
                )


    def test_password_temporal_obliga_a_perfil(self):
        """Una credencial temporal no permite navegar por Developer."""

        password = "MRP-Temporal-Perfil!2026"

        with TemporaryDirectory() as temp:
            with self._env(temp):
                crear_usuario_developer(
                    actor_rol=RolDeveloper.PROPIETARIO,
                    usuario="temporal01",
                    nombre_visible="Usuario Temporal",
                    rol=RolDeveloper.OPERADOR,
                    password_hash=hashear_password(
                        password
                    ),
                )

                cliente = TestClient(app)

                login = cliente.post(
                    "/dev",
                    data={
                        "usuario": "temporal01",
                        "password": password,
                    },
                    follow_redirects=False,
                )

                self.assertEqual(
                    303,
                    login.status_code,
                )

                inicio = cliente.get(
                    "/dev",
                    follow_redirects=False,
                )

                diagnostico = cliente.get(
                    "/dev/diagnostico",
                    follow_redirects=False,
                )

                perfil = cliente.get(
                    "/dev/perfil",
                    follow_redirects=False,
                )

        self.assertEqual(
            303,
            inicio.status_code,
        )

        self.assertEqual(
            "/dev/perfil?cambio_password=obligatorio",
            inicio.headers["location"],
        )

        self.assertEqual(
            303,
            diagnostico.status_code,
        )

        self.assertEqual(
            "/dev/perfil?cambio_password=obligatorio",
            diagnostico.headers["location"],
        )

        self.assertEqual(
            200,
            perfil.status_code,
        )

        self.assertIn(
            "Cambio de contraseña requerido",
            perfil.text,
        )


    def test_perfil_avatar_reutiliza_selector_archivo_compartido(self):
        """El avatar consume el selector visual compartido de archivos."""

        plantilla = (
            Path(__file__).resolve().parents[1]
            / "app/templates/dev_profile.html"
        ).read_text(
            encoding="utf-8"
        )

        patron = re.compile(
            r'<input\b(?=[^>]*\bid="dev-profile-avatar")[^>]*>',
            flags=re.S,
        )

        coincidencia = patron.search(
            plantilla
        )

        self.assertIsNotNone(
            coincidencia
        )

        self.assertIn(
            "official-import-file-input",
            coincidencia.group(0),
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
