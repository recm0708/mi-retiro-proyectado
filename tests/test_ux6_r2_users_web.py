"""Regresiones UX.6 R2 para la superficie web de usuarios Developer."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestUX6R2UsersWeb(unittest.TestCase):
    """Protege navegación, RBAC, operaciones sensibles y documentación."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.main = (
            ROOT
            / "app/main.py"
        ).read_text(
            encoding="utf-8"
        )
        cls.base = (
            ROOT
            / "app/templates/dev_base.html"
        ).read_text(
            encoding="utf-8"
        )
        cls.usuarios = (
            ROOT
            / "app/templates/dev_users.html"
        ).read_text(
            encoding="utf-8"
        )
        cls.css = (
            ROOT
            / "app/static/css/developer-portal.css"
        ).read_text(
            encoding="utf-8"
        )

    def test_get_usuarios_exige_permiso_de_lectura(self):
        inicio = self.main.index(
            "async def usuarios_developer("
        )

        fin = self.main.find(
            "\n\n@app.",
            inicio,
        )

        if fin < 0:
            fin = len(
                self.main
            )

        bloque = self.main[
            inicio:fin
        ]

        self.assertIn(
            "PermisoDeveloper.USUARIOS_LEER",
            bloque,
        )

        self.assertIn(
            "actor.debe_cambiar_password",
            bloque,
        )

        self.assertIn(
            'name="dev_users.html"',
            bloque,
        )

        self.assertIn(
            'contexto["dev_auditoria_usuarios"]',
            bloque,
        )

        self.assertIn(
            "PermisoDeveloper.SEGURIDAD_AUDITAR",
            bloque,
        )


    def test_sidebar_solo_muestra_usuarios_con_permiso(self):
        self.assertIn(
            '{% if "users.read" in dev_permisos %}',
            self.base,
        )
        self.assertIn(
            'href="/dev/usuarios"',
            self.base,
        )
        self.assertIn(
            "pagina_activa == 'usuarios'",
            self.base,
        )

    def test_formularios_de_usuarios_tienen_csrf(self):
        acciones = {
            "/dev/usuarios/crear",
            "/dev/usuarios/{{ fila.usuario.identificador }}/editar",
            "/dev/usuarios/{{ fila.usuario.identificador }}/password-temporal",
            "/dev/usuarios/{{ fila.usuario.identificador }}/eliminar",
        }

        for accion in acciones:
            with self.subTest(accion=accion):
                self.assertIn(
                    f'action="{accion}"',
                    self.usuarios,
                )

        self.assertGreaterEqual(
            self.usuarios.count('name="csrf_token"'),
            4,
        )


    def test_operaciones_sensibles_revalidan_password(self):
        funciones = (
            "crear_usuario_developer_web",
            "cambiar_rol_usuario_developer_web",
            "cambiar_estado_usuario_developer_web",
            "restablecer_password_usuario_developer_web",
            "eliminar_usuario_developer_web",
        )

        for nombre in funciones:
            inicio = self.main.index(
                f"async def {nombre}("
            )

            fin = self.main.find(
                "\n\n@app.",
                inicio,
            )

            if fin < 0:
                fin = len(self.main)

            bloque = self.main[
                inicio:fin
            ]

            with self.subTest(
                funcion=nombre
            ):
                self.assertTrue(
                    (
                        "revalidar_password_usuario("
                        in bloque
                    )
                    or (
                        "_revalidar_operacion_developer("
                        in bloque
                    )
                )

        self.assertIn(
            "PermisoDeveloper.ROLES_ASIGNAR_ADMIN",
            self.main,
        )

        self.assertIn(
            "PermisoDeveloper.ROLES_ASIGNAR_BASICOS",
            self.main,
        )


    def test_cambios_de_seguridad_revocan_sesiones_objetivo(self):
        for nombre in (
            "cambiar_rol_usuario_developer_web",
            "cambiar_estado_usuario_developer_web",
            "restablecer_password_usuario_developer_web",
        ):
            inicio = self.main.index(
                f"async def {nombre}("
            )

            fin = self.main.find(
                "\n\n@app.",
                inicio,
            )

            if fin < 0:
                fin = len(
                    self.main
                )

            bloque = self.main[
                inicio:fin
            ]

            self.assertIn(
                "revocar_sesiones_usuario(",
                bloque,
                nombre,
            )

    def test_password_temporal_no_viaja_por_url(self):
        usuarios_normalizado = " ".join(
            self.usuarios.lower().split()
        )

        self.assertNotIn(
            "password_temporal=",
            self.main,
        )

        self.assertIn(
            "dev_credencial_temporal",
            self.main,
        )

        self.assertIn(
            "se muestra una sola vez",
            usuarios_normalizado,
        )

        self.assertIn(
            "data-dev-temporary-password",
            self.usuarios,
        )

    def test_username_no_tiene_edicion_administrativa(self):
        self.assertNotIn(
            'name="usuario_nuevo" value=',
            self.usuarios,
        )
        self.assertNotIn(
            'name="usuario"',
            self.usuarios,
        )
        self.assertNotIn(
            "/usuario\"",
            self.main,
        )

    def test_eliminacion_es_owner_only_y_reforzada(self):
        identidad = (
            ROOT / "app/core/developer_identity.py"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'USUARIOS_ELIMINAR = "users.delete"',
            identidad,
        )
        self.assertIn(
            'action="/dev/usuarios/{{ fila.usuario.identificador }}/eliminar"',
            self.usuarios,
        )
        self.assertIn(
            '{% if "users.delete" in dev_permisos %}',
            self.usuarios,
        )
        self.assertIn(
            "PermisoDeveloper.USUARIOS_ELIMINAR",
            self.main,
        )
        self.assertIn(
            '"ELIMINAR USUARIO"',
            self.main,
        )


    def test_css_usuarios_es_responsive_y_usa_tokens(self):
        self.assertIn(
            ".dev-users-layout",
            self.css,
        )
        self.assertIn(
            "@media (max-width: 767.98px)",
            self.css,
        )
        self.assertIn(
            "var(--app-border)",
            self.css,
        )
        self.assertNotIn(
            "--dev-",
            self.css,
        )

    def test_documentacion_registra_rutas_de_usuarios(self):
        arquitectura = (
            ROOT
            / "docs/architecture/system-architecture.md"
        ).read_text(
            encoding="utf-8"
        )

        centro = (
            ROOT
            / "docs/architecture/development-center.md"
        ).read_text(
            encoding="utf-8"
        )

        for ruta in (
            "/dev/usuarios",
            "/dev/usuarios/crear",
            "/dev/usuarios/{identificador}/datos",
            "/dev/usuarios/{identificador}/rol",
            "/dev/usuarios/{identificador}/estado",
            "/dev/usuarios/{identificador}/password-temporal",
        ):
            with self.subTest(
                ruta=ruta
            ):
                self.assertIn(
                    f"`{ruta}`",
                    arquitectura,
                )
                self.assertIn(
                    f"`{ruta}`",
                    centro,
                )


    def test_fecha_hora_operativa_usa_formateador_compartido(self):
        javascript = (
            ROOT
            / "app/static/js/datetime_ui.js"
        ).read_text(
            encoding="utf-8"
        )

        base = (
            ROOT
            / "app/templates/base.html"
        ).read_text(
            encoding="utf-8"
        )

        dev_base = (
            ROOT
            / "app/templates/dev_base.html"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "datetime_ui.js",
            base,
        )

        self.assertIn(
            "datetime_ui.js",
            dev_base,
        )

        self.assertIn(
            "data-app-local-datetime",
            self.usuarios,
        )

        self.assertNotIn(
            "data-dev-local-datetime",
            self.usuarios,
        )

        self.assertIn(
            'new Intl.DateTimeFormat(',
            javascript,
        )

        self.assertIn(
            '"es-PA"',
            javascript,
        )

        self.assertIn(
            'hour12: true',
            javascript,
        )


    def test_fechas_eventos_y_archivos_no_exponen_iso_como_presentacion(self):
        for nombre in (
            "dev_events.html",
            "dev_files.html",
            "dev_development_center.html",
        ):
            texto = (
                ROOT
                / "app/templates"
                / nombre
            ).read_text(
                encoding="utf-8"
            )

            with self.subTest(
                plantilla=nombre
            ):
                self.assertIn(
                    "data-app-local-datetime",
                    texto,
                )

                self.assertNotIn(
                    "Fecha UTC",
                    texto,
                )

                self.assertNotIn(
                    "Actualizado UTC",
                    texto,
                )

    def test_usuarios_tooltip_y_mantenimiento_son_explicitos(self):
        base = (
            ROOT
            / "app/templates/dev_base.html"
        ).read_text(
            encoding="utf-8"
        )

        enlace = re.search(
            r'<a\b'
            r'(?=[^>]*href="/dev/usuarios")'
            r'[^>]*>',
            base,
            re.S,
        )

        self.assertIsNotNone(
            enlace
        )

        self.assertIn(
            'data-sidebar-label="Usuarios"',
            enlace.group(0),
        )

        self.assertIn(
            'aria-label="Usuarios"',
            enlace.group(0),
        )

        mantenimiento = (
            ROOT
            / "app/templates/dev_maintenance.html"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'placeholder="Ingresa tu contraseña actual"',
            mantenimiento,
        )

        self.assertIn(
            'placeholder="Escribe exactamente REVOCAR SESIONES"',
            mantenimiento,
        )

        self.assertIn(
            "Escribe exactamente REVOCAR SESIONES para confirmar esta operación.",
            mantenimiento,
        )

    def test_portal_no_usa_humano_para_sesion_identidad_o_credencial(self):
        patron = re.compile(
            r"\b(?:"
            r"sesiones?|identidades?|credenciales?|"
            r"contraseñas?|cuentas?|acceso|login|"
            r"operaciones?|secretos?|navegación"
            r")\s+human(?:a|o|as|os)\b",
            re.I,
        )

        encontrados = []

        for ruta in sorted(
            (
                ROOT
                / "app/templates"
            ).glob(
                "dev_*.html"
            )
        ):
            texto = ruta.read_text(
                encoding="utf-8"
            )

            encontrados.extend(
                (
                    ruta.name,
                    coincidencia.group(0),
                )
                for coincidencia
                in patron.finditer(
                    texto
                )
            )

        self.assertEqual(
            [],
            encontrados,
        )


    def test_revalidacion_incorrecta_vuelve_a_usuarios_sin_json(self):
        self.assertGreaterEqual(
            self.main.count(
                'url="/dev/usuarios?resultado=revalidacion-invalida"'
            ),
            5,
        )
        self.assertIn(
            "La contraseña actual no coincide.",
            self.main,
        )



if __name__ == "__main__":
    unittest.main()
