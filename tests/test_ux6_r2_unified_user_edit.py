"""Regresiones UX.6 R2 para edición unificada de usuarios."""

from __future__ import annotations
from tests._runtime_http_source import runtime_http_source

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestUX6R2UnifiedUserEdit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.main = runtime_http_source()

        cls.template = (
            ROOT / "app/templates/developer/dev_users.html"
        ).read_text(encoding="utf-8")

        cls.js = (
            ROOT / "app/static/js/developer_forms.js"
        ).read_text(encoding="utf-8")

        cls.css = (
            ROOT / "app/static/css/developer-portal.css"
        ).read_text(encoding="utf-8")

    def test_edicion_usa_un_formulario_y_una_revalidacion(self):
        self.assertIn(
            '/dev/usuarios/{{ fila.usuario.identificador }}/editar',
            self.template,
        )

        bloque = re.search(
            r'action="/dev/usuarios/\{\{ fila\.usuario\.identificador \}\}/editar"'
            r'.*?</form>',
            self.template,
            re.S,
        )

        self.assertIsNotNone(
            bloque
        )

        bloque_texto = bloque.group(0)

        for nombre in (
            'name="nombre_visible"',
            'name="nuevo_rol"',
            'name="estado"',
        ):
            with self.subTest(
                nombre=nombre
            ):
                self.assertIn(
                    nombre,
                    bloque_texto,
                )

        self.assertEqual(
            1,
            bloque_texto.count(
                "password_control("
            ),
        )

        self.assertIn(
            '{% macro password_control(id, name="password_actual"',
            self.template,
        )

        self.assertIn(
            "Los campos vacíos",
            self.template,
        )

    def test_reset_y_delete_permanecen_separados(self):
        self.assertIn(
            "/password-temporal",
            self.template,
        )
        self.assertIn(
            "/eliminar",
            self.template,
        )
        self.assertIn(
            "Restablecer contraseña",
            self.template,
        )
        self.assertIn(
            "Zona crítica",
            self.template,
        )

    def test_passwords_usan_ojo_canonico(self):
        self.assertIn(
            "data-dev-password-toggle",
            self.template,
        )
        self.assertIn(
            "data-dev-password-target",
            self.template,
        )
        self.assertIn(
            "Mostrar contraseña",
            self.template,
        )

    def test_temporal_tiene_boton_copiar_acotado(self):
        self.assertIn(
            "data-dev-temporary-password",
            self.template,
        )
        self.assertIn(
            "data-dev-copy-password",
            self.template,
        )
        self.assertIn(
            "navigator.clipboard.writeText",
            self.js,
        )
        self.assertIn(
            ".dev-copy-secret svg",
            self.css,
        )

    def test_error_password_estiliza_input_y_boton(self):
        self.assertIn(
            "aria-invalid",
            self.js,
        )
        self.assertIn(
            ".dev-secret-group:has(",
            self.css,
        )

    def test_backend_edita_solo_campos_solicitados(self):
        inicio = self.main.index(
            "async def editar_usuario_developer_web("
        )

        fin = self.main.find(
            "\n\n@app.",
            inicio,
        )

        bloque = self.main[
            inicio:fin if fin > 0 else len(self.main)
        ]

        for contrato in (
            "nombre_visible.strip()",
            "nuevo_rol.strip()",
            "estado.strip()",
            "actualizar_nombre_usuario_administrado(",
            "cambiar_rol_usuario_administrado(",
            "cambiar_estado_usuario_administrado(",
            "revalidar_password_usuario(",
        ):
            self.assertIn(
                contrato,
                bloque,
            )


if __name__ == "__main__":
    unittest.main()
