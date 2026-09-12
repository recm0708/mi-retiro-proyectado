"""Regresiones UX.6 R2 para formularios Developer resilientes."""

from __future__ import annotations
from tests._runtime_http_source import runtime_http_source

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from app.portals.developer.developer_identity import RolDeveloper
from app.portals.developer.developer_provisioning import bootstrap_propietario
from app.portals.developer.developer_user_admin import crear_usuario_administrado


ROOT = Path(__file__).resolve().parents[1]


class TestUX6R2FormResilience(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.main = runtime_http_source()
        cls.login = (
            ROOT / "app/templates/developer/dev_login.html"
        ).read_text(encoding="utf-8")
        cls.base = (
            ROOT / "app/templates/developer/dev_base.html"
        ).read_text(encoding="utf-8")
        cls.js = (
            ROOT / "app/static/js/developer_forms.js"
        ).read_text(encoding="utf-8")

    def test_login_preserva_usuario_no_password_y_error_inline(self):
        self.assertIn("usuario_recordado", self.main)
        self.assertIn(
            'value="{{ usuario_recordado|default(\'\') }}"',
            self.login,
        )
        self.assertIn("dev-login-password-error", self.login)
        self.assertNotIn('value="{{ password', self.login)

    def test_formularios_no_persisten_secretos(self):
        self.assertIn(
            "function esSensible(control)",
            self.js,
        )

        for contrato in (
            'tipo === "password"',
            'nombre.includes("password")',
            'nombre.includes("csrf")',
            'nombre.includes("token")',
            "sessionStorage.setItem(",
            "restaurarNoSensibles",
        ):
            with self.subTest(
                contrato=contrato
            ):
                self.assertIn(
                    contrato,
                    self.js,
                )

    def test_passwords_tienen_placeholder_y_ojo(self):
        portal_js = (
            ROOT / "app/static/js/developer_portal.js"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'placeholder="Ingresa tu contraseña"',
            self.login,
        )

        for contrato in (
            "data-dev-password-toggle",
            "data-dev-password-target",
            "Mostrar contraseña",
        ):
            with self.subTest(
                contrato=contrato
            ):
                self.assertIn(
                    contrato,
                    self.login,
                )

        for contrato in (
            "`Ocultar ${nombre}`",
            "`Mostrar ${nombre}`",
            "[data-dev-password-icon-hidden]",
            "[data-dev-password-icon-visible]",
            'input.type === "password"',
        ):
            with self.subTest(
                contrato=contrato
            ):
                self.assertIn(
                    contrato,
                    portal_js,
                )

    def test_credencial_temporal_tiene_copia_directa(self):
        self.assertIn("navigator.clipboard.writeText", self.js)
        self.assertIn("Copiar contraseña temporal", self.js)
        self.assertIn("Contraseña copiada", self.js)

    def test_credenciales_temporales_son_distintas(self):
        with TemporaryDirectory() as temp:
            ruta = Path(temp) / "portal.sqlite3"

            owner, _ = bootstrap_propietario(
                usuario="owner.unique",
                nombre_visible="Owner Unique",
                password="OwnerUnique!2026",
                ruta=ruta,
            )

            passwords = set()

            for indice in range(12):
                _, temporal = crear_usuario_administrado(
                    actor=owner,
                    usuario=f"operador.unique.{indice}",
                    nombre_visible=f"Operador {indice}",
                    rol=RolDeveloper.OPERADOR,
                    ruta=ruta,
                )
                passwords.add(temporal)

            self.assertEqual(12, len(passwords))

    def test_shell_carga_script_de_formularios(self):
        self.assertIn("developer_forms.js", self.base)


if __name__ == "__main__":
    unittest.main()
