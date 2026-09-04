"""DEV.2 R6 — Arquitectura multipágina del Portal Developer."""

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


class TestDev2R6MultipageShell(unittest.TestCase):
    """Protege las rutas y navegación humana multipágina."""

    PASSWORD = "MRP-Multipage!2026"

    def tearDown(self):
        """Revoca las sesiones creadas durante cada prueba."""

        revocar_todas_las_sesiones_admin()

    @staticmethod
    @contextmanager
    def _env(temp: str):
        """Aísla la base y configuración Developer."""

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
                nombre_visible="Propietario Multipágina",
                password=TestDev2R6MultipageShell.PASSWORD,
            )
            yield

    @classmethod
    def _login(cls, cliente: TestClient) -> None:
        """Inicia una sesión humana de prueba."""

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
                "El login de preparación no devolvió 303."
            )

    def test_subpaginas_sin_sesion_redirigen_a_dev(self):
        """Las herramientas no son accesibles sin sesión humana."""

        rutas = (
            "/dev/diagnostico",
            "/dev/eventos",
            "/dev/archivos",
            "/dev/mantenimiento",
            "/dev/privacidad",
        )

        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)

                for ruta in rutas:
                    with self.subTest(ruta=ruta):
                        respuesta = cliente.get(
                            ruta,
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

    def test_rutas_multipagina_renderizan_con_sesion(self):
        """Cada dominio Developer dispone de una página humana real."""

        casos = {
            "/dev": "Centro de control del entorno local",
            "/dev/diagnostico": "Autodiagnóstico técnico",
            "/dev/eventos": "<h1",
            "/dev/archivos": "<h1",
            "/dev/mantenimiento": "Mantenimiento",
            "/dev/privacidad": "Privacidad",
        }

        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                self._login(cliente)

                for ruta, contenido in casos.items():
                    with self.subTest(ruta=ruta):
                        respuesta = cliente.get(
                            ruta
                        )

                        self.assertEqual(
                            200,
                            respuesta.status_code,
                        )

                        self.assertIn(
                            contenido,
                            respuesta.text,
                        )

    def test_navegacion_usa_rutas_y_no_anclas_r5(self):
        """El shell enlaza páginas reales en lugar de anchors internos."""

        base = (
            Path(__file__).resolve().parents[1]
            / "app/templates/dev_base.html"
        ).read_text(encoding="utf-8")

        for ruta in (
            'href="/dev"',
            'href="/dev/diagnostico"',
            'href="/dev/eventos"',
            'href="/dev/archivos"',
            'href="/dev/mantenimiento"',
            'href="/dev/privacidad"',
        ):
            self.assertIn(
                ruta,
                base,
            )

        for ancla in (
            'href="#resumen"',
            'href="#diagnostico"',
            'href="#eventos"',
            'href="#archivos"',
            'href="#privacidad"',
        ):
            self.assertNotIn(
                ancla,
                base,
            )

    def test_pagina_activa_publica_aria_current(self):
        """La navegación expone el estado activo accesiblemente."""

        with TemporaryDirectory() as temp:
            with self._env(temp):
                cliente = TestClient(app)
                self._login(cliente)

                respuesta = cliente.get(
                    "/dev/eventos"
                )

        self.assertEqual(
            200,
            respuesta.status_code,
        )
        self.assertIn(
            'href="/dev/eventos"',
            respuesta.text,
        )
        self.assertIn(
            'aria-current="page"',
            respuesta.text,
        )

    def test_footer_comparte_copyright_publico(self):
        """El shell Developer utiliza el copyright de la aplicación."""

        base = (
            Path(__file__).resolve().parents[1]
            / "app/templates/dev_base.html"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "© 2026 {{ app_author }}. Todos los derechos reservados.",
            base,
        )

    def test_centro_legacy_se_conserva_fuera_del_menu_humano(self):
        """El endpoint técnico R5 no forma parte de la navegación humana."""

        base = (
            Path(__file__).resolve().parents[1]
            / "app/templates/dev_base.html"
        ).read_text(encoding="utf-8")

        self.assertNotIn(
            'href="/dev/centro-desarrollo"',
            base,
        )


if __name__ == "__main__":
    unittest.main()
