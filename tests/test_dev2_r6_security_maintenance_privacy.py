"""Regresiones DEV.2 R6.5-R6.7: seguridad, mantenimiento y privacidad."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from app.core.developer_identity import (
    PermisoDeveloper,
    RolDeveloper,
    hashear_password,
    rol_tiene_permiso,
    verificar_password,
)
from app.core.developer_store import (
    cambiar_password_propio,
    crear_propietario,
)
from app.core.developer_web_security import (
    token_csrf_para_sesion,
    validar_token_csrf_sesion,
)


ROOT = Path(__file__).resolve().parents[1]


class TestDev2R6SecurityMaintenancePrivacy(unittest.TestCase):

    def test_csrf_esta_ligado_a_sesion(self):
        token_a = token_csrf_para_sesion(
            "sesion-a"
        )
        token_b = token_csrf_para_sesion(
            "sesion-b"
        )

        self.assertTrue(token_a)
        self.assertNotEqual(token_a, token_b)
        self.assertTrue(
            validar_token_csrf_sesion(
                "sesion-a",
                token_a,
            )
        )
        self.assertFalse(
            validar_token_csrf_sesion(
                "sesion-b",
                token_a,
            )
        )

    def test_rbac_diferencia_mantenimiento_destructivo(self):
        self.assertTrue(
            rol_tiene_permiso(
                RolDeveloper.PROPIETARIO,
                PermisoDeveloper.MANTENIMIENTO_DESTRUCTIVO,
            )
        )
        self.assertTrue(
            rol_tiene_permiso(
                RolDeveloper.ADMINISTRADOR,
                PermisoDeveloper.MANTENIMIENTO_DESTRUCTIVO,
            )
        )
        self.assertFalse(
            rol_tiene_permiso(
                RolDeveloper.OPERADOR,
                PermisoDeveloper.MANTENIMIENTO_DESTRUCTIVO,
            )
        )
        self.assertFalse(
            rol_tiene_permiso(
                RolDeveloper.AUDITOR,
                PermisoDeveloper.MANTENIMIENTO_EJECUTAR,
            )
        )

    def test_owner_puede_cambiar_password_propio_y_subir_revision(self):
        with TemporaryDirectory() as temp:
            ruta = Path(temp) / "portal.sqlite3"

            propietario = crear_propietario(
                usuario="owner",
                nombre_visible="Owner",
                password_hash=hashear_password(
                    "MRP-Owner-Inicial!2026"
                ),
                recovery_code_hash=hashear_password(
                    "MRP-Recovery-Owner!2026"
                ),
                ruta=ruta,
            )

            revision = propietario.revision_seguridad

            actualizado = cambiar_password_propio(
                identificador=propietario.identificador,
                password_hash=hashear_password(
                    "MRP-Owner-Nueva!2026"
                ),
                ruta=ruta,
            )

            self.assertEqual(
                revision + 1,
                actualizado.revision_seguridad,
            )
            self.assertFalse(
                actualizado.debe_cambiar_password
            )
            self.assertTrue(
                verificar_password(
                    "MRP-Owner-Nueva!2026",
                    actualizado.password_hash,
                )
            )

    def test_main_no_expone_acciones_destructivas_por_get(self):
        main = (
            ROOT
            / "app/main.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            '@app.post(\n    "/dev/mantenimiento/revocar-sesiones"',
            main,
        )
        self.assertNotIn(
            '@app.get(\n    "/dev/mantenimiento/revocar-sesiones"',
            main,
        )

    def test_rutas_sensibles_exigen_csrf_y_revalidacion(self):
        main = (
            ROOT
            / "app/main.py"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "_validar_csrf_developer(",
            main,
        )
        self.assertIn(
            "_revalidar_operacion_developer(",
            main,
        )
        self.assertIn(
            "PermisoDeveloper.MANTENIMIENTO_DESTRUCTIVO",
            main,
        )
        self.assertIn(
            "PermisoDeveloper.ARCHIVOS_DESCARGAR",
            main,
        )

    def test_formularios_humanos_incluyen_csrf(self):
        for nombre in (
            "dev_base.html",
            "dev_files.html",
            "dev_maintenance.html",
            "dev_profile.html",
        ):
            texto = (
                ROOT
                / "app/templates"
                / nombre
            ).read_text(encoding="utf-8")

            self.assertIn(
                'name="csrf_token"',
                texto,
                nombre,
            )

    def test_privacidad_documenta_barreras_de_sesion(self):
        texto = (
            ROOT
            / "app/templates/dev_privacy.html"
        ).read_text(encoding="utf-8")

        for contrato in (
            "Cuerpos HTTP",
            "PDF / uploads",
            "CSRF",
            "revalidación",
            "RBAC",
        ):
            self.assertIn(
                contrato,
                texto,
            )



class TestDev2R6GetRbacRegression(unittest.TestCase):
    """Contratos RBAC de lectura de las páginas Developer."""

    def test_paginas_get_declaran_permiso_rbac(self):
        codigo = (
            Path(__file__).resolve().parents[1]
            / "app/main.py"
        ).read_text(
            encoding="utf-8"
        )

        contratos = (
            (
                'plantilla="dev_diagnostics.html"',
                "PermisoDeveloper.DIAGNOSTICO_LEER",
            ),
            (
                'plantilla="dev_events.html"',
                "PermisoDeveloper.EVENTOS_LEER",
            ),
            (
                'plantilla="dev_files.html"',
                "PermisoDeveloper.ARCHIVOS_LEER",
            ),
            (
                'plantilla="dev_maintenance.html"',
                "PermisoDeveloper.MANTENIMIENTO_LEER",
            ),
            (
                'plantilla="dev_privacy.html"',
                "PermisoDeveloper.PRIVACIDAD_LEER",
            ),
            (
                'plantilla="dev_profile.html"',
                "PermisoDeveloper.PERFIL_LEER",
            ),
            (
                'plantilla="dev_technical_access.html"',
                "PermisoDeveloper.TOKENS_LEER",
            ),
        )

        for plantilla, permiso in contratos:
            posicion = codigo.find(plantilla)

            self.assertGreaterEqual(
                posicion,
                0,
                plantilla,
            )

            fragmento = codigo[
                posicion:posicion + 260
            ]

            self.assertIn(
                permiso,
                fragmento,
            )

    def test_helper_get_aplica_deny_default_rbac(self):
        codigo = (
            Path(__file__).resolve().parents[1]
            / "app/main.py"
        ).read_text(
            encoding="utf-8"
        )

        inicio = codigo.index(
            "def _render_pagina_developer_autenticada("
        )

        fin = codigo.find(
            "\ndef ",
            inicio + 1,
        )

        if fin < 0:
            fin = len(codigo)

        helper = codigo[inicio:fin]

        self.assertIn(
            "permiso: PermisoDeveloper | None = None",
            helper,
        )

        self.assertIn(
            "rol_tiene_permiso(",
            helper,
        )

        self.assertIn(
            "status_code=403",
            helper,
        )

if __name__ == "__main__":
    unittest.main()
