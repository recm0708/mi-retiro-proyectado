"""Regresiones UX.6 R2 para auditoría persistente de usuarios Developer."""

from __future__ import annotations

from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from app.portals.developer.developer_identity import RolDeveloper
from app.portals.developer.developer_provisioning import bootstrap_propietario
from app.portals.developer.developer_user_admin import (
    actualizar_nombre_usuario_administrado,
    cambiar_estado_usuario_administrado,
    cambiar_rol_usuario_administrado,
    crear_usuario_administrado,
    eliminar_usuario_administrado,
    restablecer_password_temporal_usuario,
)
from app.portals.developer.developer_user_audit import (
    listar_auditoria_usuarios_developer,
)


class TestUX6R2UserAudit(unittest.TestCase):
    def test_ciclo_administrativo_registra_quien_hizo_que(self):
        with TemporaryDirectory() as temp:
            ruta = Path(temp) / "portal.sqlite3"

            owner, _ = bootstrap_propietario(
                usuario="owner.audit",
                nombre_visible="Owner Audit",
                password="OwnerAudit!2026",
                ruta=ruta,
            )

            operador, _ = crear_usuario_administrado(
                actor=owner,
                usuario="operador.audit",
                nombre_visible="Operador Audit",
                rol=RolDeveloper.OPERADOR,
                ruta=ruta,
            )

            operador = actualizar_nombre_usuario_administrado(
                actor=owner,
                identificador=operador.identificador,
                nombre_visible="Operador Actualizado",
                ruta=ruta,
            )

            operador = cambiar_rol_usuario_administrado(
                actor=owner,
                identificador=operador.identificador,
                nuevo_rol=RolDeveloper.AUDITOR,
                ruta=ruta,
            )

            operador = cambiar_estado_usuario_administrado(
                actor=owner,
                identificador=operador.identificador,
                activo=False,
                ruta=ruta,
            )

            operador = cambiar_estado_usuario_administrado(
                actor=owner,
                identificador=operador.identificador,
                activo=True,
                ruta=ruta,
            )

            operador, _ = restablecer_password_temporal_usuario(
                actor=owner,
                identificador=operador.identificador,
                ruta=ruta,
            )

            eliminado = eliminar_usuario_administrado(
                actor=owner,
                identificador=operador.identificador,
                ruta=ruta,
            )

            eventos = listar_auditoria_usuarios_developer(
                limite=20,
                ruta=ruta,
            )

            acciones = {
                evento.accion
                for evento in eventos
            }

            self.assertTrue(
                {
                    "user.created",
                    "user.display_name.updated",
                    "user.role.changed",
                    "user.disabled",
                    "user.reactivated",
                    "user.password.reset",
                    "user.deleted",
                }.issubset(acciones)
            )

            for evento in eventos:
                self.assertEqual(
                    owner.identificador,
                    evento.actor_id,
                )
                self.assertEqual(
                    owner.usuario,
                    evento.actor_usuario,
                )
                self.assertEqual(
                    eliminado.identificador,
                    evento.objetivo_id,
                )
                self.assertEqual(
                    eliminado.usuario,
                    evento.objetivo_usuario,
                )

    def test_ledger_es_append_only(self):
        with TemporaryDirectory() as temp:
            ruta = Path(temp) / "portal.sqlite3"

            owner, _ = bootstrap_propietario(
                usuario="owner.append",
                nombre_visible="Owner Append",
                password="OwnerAppend!2026",
                ruta=ruta,
            )

            crear_usuario_administrado(
                actor=owner,
                usuario="operador.append",
                nombre_visible="Operador Append",
                rol=RolDeveloper.OPERADOR,
                ruta=ruta,
            )

            conexion = sqlite3.connect(ruta)

            try:
                with self.assertRaises(sqlite3.IntegrityError):
                    conexion.execute(
                        "DELETE FROM developer_user_audit"
                    )
                    conexion.commit()
            finally:
                conexion.rollback()
                conexion.close()


if __name__ == "__main__":
    unittest.main()
