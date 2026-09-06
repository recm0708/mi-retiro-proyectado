"""Regresiones UX.6 R2 para administración humana de usuarios Developer."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from app.core.developer_identity import (
    RolDeveloper,
    hashear_password,
    validar_password,
)
from app.core.developer_provisioning import (
    bootstrap_propietario,
)
from app.core.developer_store import (
    crear_usuario_developer,
)
from app.core.developer_user_admin import (
    actualizar_nombre_usuario_administrado,
    cambiar_estado_usuario_administrado,
    cambiar_rol_usuario_administrado,
    consumir_credencial_temporal_para_sesion,
    crear_usuario_administrado,
    eliminar_usuario_administrado,
    generar_password_temporal_developer,
    guardar_credencial_temporal_para_sesion,
    restablecer_password_temporal_usuario,
    roles_asignables_por_actor,
)


class TestUX6R2UserAdmin(unittest.TestCase):
    """Protege jerarquía, credenciales temporales y autogestión."""

    def _owner(
        self,
        ruta: Path,
    ):
        owner, _ = bootstrap_propietario(
            usuario="owner.test",
            nombre_visible="Owner Test",
            password="OwnerSeguro!2026",
            ruta=ruta,
        )

        return owner

    def _crear_admin(
        self,
        owner,
        ruta: Path,
    ):
        admin, _ = crear_usuario_administrado(
            actor=owner,
            usuario="admin.test",
            nombre_visible="Admin Test",
            rol=RolDeveloper.ADMINISTRADOR,
            ruta=ruta,
        )

        return admin

    def test_password_temporal_cumple_politica(self):
        password = generar_password_temporal_developer()

        self.assertEqual(
            password,
            validar_password(
                password
            ),
        )

    def test_owner_crea_admin_con_cambio_obligatorio(self):
        with TemporaryDirectory() as temp:
            ruta = (
                Path(temp)
                / "portal.sqlite3"
            )

            owner = self._owner(
                ruta
            )

            creado, password = crear_usuario_administrado(
                actor=owner,
                usuario="admin.nuevo",
                nombre_visible="Administrador Nuevo",
                rol=RolDeveloper.ADMINISTRADOR,
                ruta=ruta,
            )

            self.assertEqual(
                RolDeveloper.ADMINISTRADOR,
                creado.rol,
            )
            self.assertTrue(
                creado.debe_cambiar_password
            )
            validar_password(
                password
            )

    def test_admin_no_puede_crear_otro_admin(self):
        with TemporaryDirectory() as temp:
            ruta = (
                Path(temp)
                / "portal.sqlite3"
            )

            owner = self._owner(
                ruta
            )
            admin = self._crear_admin(
                owner,
                ruta,
            )

            with self.assertRaises(
                PermissionError
            ):
                crear_usuario_administrado(
                    actor=admin,
                    usuario="admin.otro",
                    nombre_visible="Otro Admin",
                    rol=RolDeveloper.ADMINISTRADOR,
                    ruta=ruta,
                )

    def test_admin_gestiona_operador_pero_no_su_cuenta(self):
        with TemporaryDirectory() as temp:
            ruta = (
                Path(temp)
                / "portal.sqlite3"
            )

            owner = self._owner(
                ruta
            )
            admin = self._crear_admin(
                owner,
                ruta,
            )

            operador = crear_usuario_developer(
                actor_rol=owner.rol,
                usuario="operador.test",
                nombre_visible="Operador Test",
                rol=RolDeveloper.OPERADOR,
                password_hash=hashear_password(
                    "OperadorSeguro!2026"
                ),
                debe_cambiar_password=True,
                ruta=ruta,
            )

            actualizado = actualizar_nombre_usuario_administrado(
                actor=admin,
                identificador=operador.identificador,
                nombre_visible="Operador Actualizado",
                ruta=ruta,
            )

            self.assertEqual(
                "Operador Actualizado",
                actualizado.nombre_visible,
            )

            with self.assertRaises(
                PermissionError
            ):
                cambiar_rol_usuario_administrado(
                    actor=admin,
                    identificador=admin.identificador,
                    nuevo_rol=RolDeveloper.AUDITOR,
                    ruta=ruta,
                )

    def test_owner_y_cuenta_propia_estan_protegidos(self):
        with TemporaryDirectory() as temp:
            ruta = (
                Path(temp)
                / "portal.sqlite3"
            )

            owner = self._owner(
                ruta
            )
            admin = self._crear_admin(
                owner,
                ruta,
            )

            with self.assertRaises(
                PermissionError
            ):
                cambiar_estado_usuario_administrado(
                    actor=admin,
                    identificador=owner.identificador,
                    activo=False,
                    ruta=ruta,
                )

            with self.assertRaises(
                PermissionError
            ):
                cambiar_estado_usuario_administrado(
                    actor=admin,
                    identificador=admin.identificador,
                    activo=False,
                    ruta=ruta,
                )

    def test_reset_temporal_obliga_cambio_y_rota_revision(self):
        with TemporaryDirectory() as temp:
            ruta = (
                Path(temp)
                / "portal.sqlite3"
            )

            owner = self._owner(
                ruta
            )

            operador, _ = crear_usuario_administrado(
                actor=owner,
                usuario="operador.reset",
                nombre_visible="Operador Reset",
                rol=RolDeveloper.OPERADOR,
                ruta=ruta,
            )

            revision_anterior = (
                operador.revision_seguridad
            )

            actualizado, password = restablecer_password_temporal_usuario(
                actor=owner,
                identificador=operador.identificador,
                ruta=ruta,
            )

            self.assertTrue(
                actualizado.debe_cambiar_password
            )
            self.assertGreater(
                actualizado.revision_seguridad,
                revision_anterior,
            )
            validar_password(
                password
            )

    def test_roles_asignables_respetan_jerarquia(self):
        with TemporaryDirectory() as temp:
            ruta = (
                Path(temp)
                / "portal.sqlite3"
            )

            owner = self._owner(
                ruta
            )
            admin = self._crear_admin(
                owner,
                ruta,
            )

            self.assertIn(
                RolDeveloper.ADMINISTRADOR,
                roles_asignables_por_actor(
                    owner
                ),
            )

            self.assertNotIn(
                RolDeveloper.ADMINISTRADOR,
                roles_asignables_por_actor(
                    admin
                ),
            )

    def test_credencial_temporal_se_muestra_una_sola_vez(self):
        password = (
            generar_password_temporal_developer()
        )

        guardar_credencial_temporal_para_sesion(
            sesion="sesion-prueba",
            usuario="operador.test",
            password=password,
            operacion="crear",
        )

        primera = (
            consumir_credencial_temporal_para_sesion(
                "sesion-prueba"
            )
        )

        segunda = (
            consumir_credencial_temporal_para_sesion(
                "sesion-prueba"
            )
        )

        self.assertIsNotNone(
            primera
        )
        self.assertEqual(
            password,
            primera.password,
        )
        self.assertIsNone(
            segunda
        )

    def test_solo_owner_puede_eliminar_cuenta_ordinaria(self):
        with TemporaryDirectory() as temp:
            ruta = Path(temp) / "portal.sqlite3"

            owner = self._owner(ruta)
            admin = self._crear_admin(owner, ruta)

            operador, _ = crear_usuario_administrado(
                actor=owner,
                usuario="operador.delete",
                nombre_visible="Operador Delete",
                rol=RolDeveloper.OPERADOR,
                ruta=ruta,
            )

            with self.assertRaises(PermissionError):
                eliminar_usuario_administrado(
                    actor=admin,
                    identificador=operador.identificador,
                    ruta=ruta,
                )

            eliminado = eliminar_usuario_administrado(
                actor=owner,
                identificador=operador.identificador,
                ruta=ruta,
            )

            self.assertEqual(
                operador.identificador,
                eliminado.identificador,
            )

            with self.assertRaises(LookupError):
                eliminar_usuario_administrado(
                    actor=owner,
                    identificador=operador.identificador,
                    ruta=ruta,
                )

            with self.assertRaises(PermissionError):
                eliminar_usuario_administrado(
                    actor=owner,
                    identificador=owner.identificador,
                    ruta=ruta,
                )



if __name__ == "__main__":
    unittest.main()
