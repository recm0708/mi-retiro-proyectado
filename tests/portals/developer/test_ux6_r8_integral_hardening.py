"""Regresiones UX.6 R8 para hardening integral previo a promoción."""

from __future__ import annotations
from tests.shared._runtime_http_source import runtime_http_source

from pathlib import Path
import unittest
from unittest.mock import patch

import app.portals.developer.admin_session as admin_session
from app.portals.developer.admin_session import (
    crear_sesion_admin,
    obtener_sesion_admin,
    obtener_sesiones_activas_usuario,
    revocar_todas_las_sesiones_admin,
    validar_sesion_admin,
)
from app.portals.developer.developer_identity import RolDeveloper


ROOT = Path(__file__).resolve().parents[3]


class TestUX6R8IntegralHardening(unittest.TestCase):
    def setUp(self) -> None:
        revocar_todas_las_sesiones_admin()

    def tearDown(self) -> None:
        revocar_todas_las_sesiones_admin()

    @staticmethod
    def _crear(usuario_id: str, usuario: str) -> str:
        return crear_sesion_admin(
            usuario_id=usuario_id,
            usuario=usuario,
            rol=RolDeveloper.OPERADOR,
            revision_seguridad=1,
        )

    def test_limite_de_sesiones_es_por_cuenta_y_conserva_la_nueva(self):
        with patch.object(admin_session, "ADMIN_MAX_SESSIONS", 2):
            a1 = self._crear("cuenta-a", "cuenta.a")
            b1 = self._crear("cuenta-b", "cuenta.b")
            a2 = self._crear("cuenta-a", "cuenta.a")
            a3 = self._crear("cuenta-a", "cuenta.a")

            nueva = obtener_sesion_admin(
                a3,
                actualizar_actividad=False,
            )

            self.assertIsNotNone(nueva)
            self.assertEqual(1, nueva.sesiones_cerradas_por_limite)
            self.assertFalse(validar_sesion_admin(a1))
            self.assertTrue(validar_sesion_admin(a2))
            self.assertTrue(validar_sesion_admin(a3))
            self.assertTrue(validar_sesion_admin(b1))
            self.assertEqual(
                2,
                len(obtener_sesiones_activas_usuario("cuenta-a")),
            )
            self.assertEqual(
                1,
                len(obtener_sesiones_activas_usuario("cuenta-b")),
            )

    def test_sesiones_legacy_se_limitan_sin_afectar_identidades(self):
        with patch.object(admin_session, "ADMIN_MAX_SESSIONS", 2):
            legacy_1 = crear_sesion_admin()
            identificada = self._crear("cuenta-c", "cuenta.c")
            legacy_2 = crear_sesion_admin()
            legacy_3 = crear_sesion_admin()

            self.assertFalse(validar_sesion_admin(legacy_1))
            self.assertTrue(validar_sesion_admin(legacy_2))
            self.assertTrue(validar_sesion_admin(legacy_3))
            self.assertTrue(validar_sesion_admin(identificada))

    def test_login_alinea_cookie_con_duracion_absoluta_y_avisa_limite(self):
        main = runtime_http_source()
        dashboard = (
            ROOT / "app/templates/developer/dev_dashboard.html"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "max_age=ADMIN_SESSION_MAX_HOURS * 60 * 60",
            main,
        )
        self.assertIn('"/dev?sesion=limite"', main)
        self.assertIn("sesiones_cerradas_por_limite", main)
        self.assertIn(
            "Se cerró automáticamente la sesión más antigua",
            dashboard,
        )

    def test_navegacion_developer_oculta_destinos_sin_permiso(self):
        base = (
            ROOT / "app/templates/developer/dev_base.html"
        ).read_text(encoding="utf-8")
        dashboard = (
            ROOT / "app/templates/developer/dev_dashboard.html"
        ).read_text(encoding="utf-8")

        self.assertIn(
            '{% if "maintenance.read" in dev_permisos %}',
            base,
        )
        self.assertIn(
            '{% if "maintenance.read" in dev_permisos %}',
            dashboard,
        )
        self.assertIn(
            '{% if "tokens.read" in dev_permisos %}',
            base,
        )

    def test_assets_compartidos_y_developer_tienen_revision_correcta(self):
        base = (
            ROOT / "app/templates/developer/dev_base.html"
        ).read_text(encoding="utf-8")

        for asset in (
            "/shared/css/design-system.css",
            "/shared/css/accessibility.css",
            "/shared/css/motion.css",
            "/shared/js/theme.js",
            "/shared/js/datetime_ui.js",
            "/shared/js/shell_ui.js",
            "/shared/js/interaction_ui.js",
        ):
            with self.subTest(asset=asset):
                esperado = (
                    "path='" + asset + "') }}"
                    "?v={{ static_revision }}"
                )
                self.assertIn(esperado, base)

        for asset in (
            "/developer/css/developer-portal.css",
            "/developer/js/developer_portal.js",
            "/developer/js/developer_forms.js",
        ):
            with self.subTest(asset=asset):
                esperado = (
                    "path='" + asset + "') }}"
                    "?v={{ dev_assets_revision }}"
                )
                self.assertIn(esperado, base)

    def test_privacidad_publica_mantiene_version_material(self):
        privacy_js = (
            ROOT / "app/static/asegurado/js/privacy.js"
        ).read_text(encoding="utf-8")

        self.assertIn(
            'VERSION_PRIVACIDAD = "2026-08-16.1"',
            privacy_js,
        )

    def test_documentacion_declara_limite_por_cuenta_y_favicon_oficial(self):
        centro = (
            ROOT / "docs/architecture/development-center.md"
        ).read_text(encoding="utf-8")
        seguridad = (
            ROOT / "docs/security/security-and-privacy.md"
        ).read_text(encoding="utf-8")
        guia = (
            ROOT / "docs/operations/development-guide.md"
        ).read_text(encoding="utf-8")

        self.assertIn("sesiones simultáneas por cuenta", centro)
        self.assertIn("sesiones simultáneas por cuenta", seguridad)
        self.assertIn("el favicon oficial", guia)
        self.assertNotIn("puede responder 204", guia)


if __name__ == "__main__":
    unittest.main()
