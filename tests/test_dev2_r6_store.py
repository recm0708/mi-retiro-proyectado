"""DEV.2 R6 — Regresiones del almacenamiento de identidades Developer."""

from __future__ import annotations

from pathlib import Path
import os
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from app.portals.developer.developer_identity import (
    RolDeveloper,
    generar_codigo_recuperacion_propietario,
    hashear_codigo_recuperacion,
    hashear_password,
)
from app.portals.developer.developer_avatar import (
    directorio_avatares_developer,
    eliminar_avatar_developer,
    guardar_avatar_developer,
    resolver_avatar_developer,
    ruta_media_developer,
)
from app.portals.developer.developer_store import (
    actualizar_avatar_usuario,
    actualizar_nombre_visible_usuario,
    cambiar_estado_usuario,
    cambiar_rol_usuario,
    contar_propietarios,
    crear_propietario,
    crear_usuario_developer,
    inicializar_almacen_developer,
    listar_usuarios_developer,
    obtener_usuario_por_login,
    registrar_acceso_usuario,
)


class TestDev2R6DeveloperStore(unittest.TestCase):

    @staticmethod
    def _ruta(temp: str) -> Path:
        return Path(temp) / "portal.sqlite3"

    def _crear_propietario(self, ruta: Path):
        codigo = generar_codigo_recuperacion_propietario()

        return crear_propietario(
            usuario="propietario",
            nombre_visible="Propietario de prueba",
            password_hash=hashear_password(
                "MRP-Propietario-Prueba-2026"
            ),
            recovery_code_hash=(
                hashear_codigo_recuperacion(codigo)
            ),
            ruta=ruta,
        )

    def test_inicializacion_crea_base_local(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)

            resultado = inicializar_almacen_developer(
                ruta
            )

            self.assertEqual(ruta.resolve(), resultado)
            self.assertTrue(ruta.exists())
            self.assertEqual(
                0,
                contar_propietarios(ruta),
            )

    def test_creacion_propietario_es_unica(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)

            propietario = self._crear_propietario(
                ruta
            )

            self.assertTrue(
                propietario.es_propietario
            )
            self.assertTrue(propietario.activo)
            self.assertEqual(
                RolDeveloper.PROPIETARIO,
                propietario.rol,
            )
            self.assertEqual(
                1,
                contar_propietarios(ruta),
            )

            with self.assertRaises(ValueError):
                self._crear_propietario(ruta)

    def test_propietario_no_puede_borrarse_ni_por_sql_directo(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            propietario = self._crear_propietario(
                ruta
            )

            conexion = sqlite3.connect(ruta)

            try:
                with self.assertRaises(
                    sqlite3.IntegrityError
                ):
                    conexion.execute(
                        """
                        DELETE FROM developer_users
                        WHERE id = ?
                        """,
                        (propietario.identificador,),
                    )
            finally:
                conexion.close()

            self.assertEqual(
                1,
                contar_propietarios(ruta),
            )

    def test_propietario_no_puede_desactivarse_o_degradarse_por_sql(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            propietario = self._crear_propietario(
                ruta
            )

            conexion = sqlite3.connect(ruta)

            try:
                with self.assertRaises(
                    sqlite3.IntegrityError
                ):
                    conexion.execute(
                        """
                        UPDATE developer_users
                        SET is_active = 0
                        WHERE id = ?
                        """,
                        (propietario.identificador,),
                    )

                with self.assertRaises(
                    sqlite3.IntegrityError
                ):
                    conexion.execute(
                        """
                        UPDATE developer_users
                        SET role = 'admin',
                            is_owner = 0
                        WHERE id = ?
                        """,
                        (propietario.identificador,),
                    )
            finally:
                conexion.close()

    def test_usuario_normal_no_puede_promoverse_a_propietario_por_sql(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            self._crear_propietario(ruta)

            operador = crear_usuario_developer(
                actor_rol=RolDeveloper.PROPIETARIO,
                usuario="operador01",
                nombre_visible="Operador Uno",
                rol=RolDeveloper.OPERADOR,
                password_hash=hashear_password(
                    "MRP-Operador-Prueba-2026"
                ),
                ruta=ruta,
            )

            conexion = sqlite3.connect(ruta)

            try:
                with self.assertRaises(
                    sqlite3.IntegrityError
                ):
                    conexion.execute(
                        """
                        UPDATE developer_users
                        SET role = 'owner',
                            is_owner = 1
                        WHERE id = ?
                        """,
                        (operador.identificador,),
                    )
            finally:
                conexion.close()

    def test_propietario_puede_crear_administrador(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            self._crear_propietario(ruta)

            admin = crear_usuario_developer(
                actor_rol=RolDeveloper.PROPIETARIO,
                usuario="admin01",
                nombre_visible="Administrador Uno",
                rol=RolDeveloper.ADMINISTRADOR,
                password_hash=hashear_password(
                    "MRP-Admin-Prueba-2026"
                ),
                ruta=ruta,
            )

            self.assertEqual(
                RolDeveloper.ADMINISTRADOR,
                admin.rol,
            )
            self.assertTrue(
                admin.debe_cambiar_password
            )
            self.assertFalse(
                admin.es_propietario
            )

    def test_administrador_no_puede_crear_otro_administrador(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            self._crear_propietario(ruta)

            with self.assertRaises(
                PermissionError
            ):
                crear_usuario_developer(
                    actor_rol=(
                        RolDeveloper.ADMINISTRADOR
                    ),
                    usuario="admin02",
                    nombre_visible=(
                        "Administrador Dos"
                    ),
                    rol=(
                        RolDeveloper.ADMINISTRADOR
                    ),
                    password_hash=hashear_password(
                        "MRP-Admin-Dos-Prueba-2026"
                    ),
                    ruta=ruta,
                )

    def test_administrador_puede_crear_operador(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            self._crear_propietario(ruta)

            operador = crear_usuario_developer(
                actor_rol=RolDeveloper.ADMINISTRADOR,
                usuario="OPERADOR02",
                nombre_visible="Operador Dos",
                rol=RolDeveloper.OPERADOR,
                password_hash=hashear_password(
                    "MRP-Operador-Dos-2026"
                ),
                ruta=ruta,
            )

            recuperado = obtener_usuario_por_login(
                "operador02",
                ruta,
            )

            self.assertIsNotNone(recuperado)
            self.assertEqual(
                operador.identificador,
                recuperado.identificador,
            )
            self.assertEqual(
                "operador02",
                recuperado.usuario,
            )

    def test_solo_propietario_puede_elevar_a_administrador(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            self._crear_propietario(ruta)

            operador = crear_usuario_developer(
                actor_rol=RolDeveloper.ADMINISTRADOR,
                usuario="operador03",
                nombre_visible="Operador Tres",
                rol=RolDeveloper.OPERADOR,
                password_hash=hashear_password(
                    "MRP-Operador-Tres-2026"
                ),
                ruta=ruta,
            )

            with self.assertRaises(
                PermissionError
            ):
                cambiar_rol_usuario(
                    actor_rol=(
                        RolDeveloper.ADMINISTRADOR
                    ),
                    identificador=(
                        operador.identificador
                    ),
                    nuevo_rol=(
                        RolDeveloper.ADMINISTRADOR
                    ),
                    ruta=ruta,
                )

            actualizado = cambiar_rol_usuario(
                actor_rol=RolDeveloper.PROPIETARIO,
                identificador=(
                    operador.identificador
                ),
                nuevo_rol=(
                    RolDeveloper.ADMINISTRADOR
                ),
                ruta=ruta,
            )

            self.assertEqual(
                RolDeveloper.ADMINISTRADOR,
                actualizado.rol,
            )
            self.assertEqual(
                2,
                actualizado.revision_seguridad,
            )


    def test_perfil_actualiza_nombre_avatar_y_listado(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)

            self._crear_propietario(
                ruta
            )

            operador = crear_usuario_developer(
                actor_rol=RolDeveloper.PROPIETARIO,
                usuario="perfil01",
                nombre_visible="Perfil Uno",
                rol=RolDeveloper.OPERADOR,
                password_hash=hashear_password(
                    "MRP-Perfil-Uno!2026"
                ),
                ruta=ruta,
            )

            actualizado = actualizar_nombre_visible_usuario(
                identificador=operador.identificador,
                nombre_visible="Perfil Actualizado",
                ruta=ruta,
            )

            self.assertEqual(
                "Perfil Actualizado",
                actualizado.nombre_visible,
            )

            avatar = actualizar_avatar_usuario(
                identificador=operador.identificador,
                avatar_relativo="avatars/prueba.png",
                ruta=ruta,
            )

            self.assertEqual(
                "avatars/prueba.png",
                avatar.avatar_relativo,
            )

            usuarios = listar_usuarios_developer(
                ruta
            )

            self.assertEqual(
                2,
                len(usuarios),
            )

            self.assertTrue(
                usuarios[0].es_propietario
            )


    def test_media_avatar_admite_raiz_persistente_configurable(self):
        with TemporaryDirectory() as temp:
            raiz = (
                Path(temp)
                / "media-persistente"
            )

            almacen = (
                Path(temp)
                / "store"
                / "portal.sqlite3"
            )

            with patch.dict(
                os.environ,
                {
                    "MRP_DEVELOPER_MEDIA_DIR": str(
                        raiz
                    ),
                },
                clear=False,
            ):
                self.assertEqual(
                    raiz.resolve(),
                    ruta_media_developer(
                        almacen
                    ),
                )

                self.assertEqual(
                    (
                        raiz
                        / "avatars"
                    ).resolve(),
                    directorio_avatares_developer(
                        almacen
                    ),
                )

                referencia = guardar_avatar_developer(
                    identificador="persistente01",
                    contenido=(
                        b"\x89PNG\r\n\x1a\n"
                        b"avatar-persistente"
                    ),
                    ruta_almacen=almacen,
                )

                self.assertEqual(
                    "avatars",
                    Path(
                        referencia
                    ).parts[0],
                )

                self.assertTrue(
                    (
                        raiz
                        / referencia
                    ).is_file()
                )


    def test_avatar_local_valida_ruta_y_formato(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)

            referencia = guardar_avatar_developer(
                identificador="usuario01",
                contenido=(
                    b"\x89PNG\r\n\x1a\n"
                    b"contenido-prueba"
                ),
                ruta_almacen=ruta,
            )

            destino = resolver_avatar_developer(
                referencia,
                ruta,
            )

            self.assertIsNotNone(
                destino
            )

            self.assertTrue(
                destino.is_file()
            )

            eliminar_avatar_developer(
                referencia,
                ruta,
            )

            self.assertFalse(
                destino.exists()
            )


    def test_estado_cuenta_incrementa_revision_y_protege_owner(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)

            propietario = self._crear_propietario(
                ruta
            )

            operador = crear_usuario_developer(
                actor_rol=RolDeveloper.PROPIETARIO,
                usuario="estado01",
                nombre_visible="Estado Uno",
                rol=RolDeveloper.OPERADOR,
                password_hash=hashear_password(
                    "MRP-Estado-Uno!2026"
                ),
                ruta=ruta,
            )

            desactivado = cambiar_estado_usuario(
                actor_rol=RolDeveloper.ADMINISTRADOR,
                identificador=operador.identificador,
                activo=False,
                ruta=ruta,
            )

            self.assertFalse(
                desactivado.activo
            )

            self.assertEqual(
                operador.revision_seguridad + 1,
                desactivado.revision_seguridad,
            )

            with self.assertRaises(
                PermissionError
            ):
                cambiar_estado_usuario(
                    actor_rol=RolDeveloper.PROPIETARIO,
                    identificador=propietario.identificador,
                    activo=False,
                    ruta=ruta,
                )


    def test_login_correcto_registra_ultimo_acceso(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)

            propietario = self._crear_propietario(
                ruta
            )

            self.assertIsNone(
                propietario.ultimo_acceso_utc
            )

            actualizado = registrar_acceso_usuario(
                identificador=propietario.identificador,
                ruta=ruta,
            )

            self.assertIsNotNone(
                actualizado.ultimo_acceso_utc
            )


    def test_esquema_previo_migra_revision_seguridad(self):
        """Una base R6 inicial previa recibe security_version sin perderse."""

        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)

            inicializar_almacen_developer(
                ruta
            )

            conexion = sqlite3.connect(
                ruta
            )

            try:
                conexion.execute(
                    """
                    ALTER TABLE developer_users
                    DROP COLUMN security_version
                    """
                )
                conexion.commit()
            finally:
                conexion.close()

            inicializar_almacen_developer(
                ruta
            )

            conexion = sqlite3.connect(
                ruta
            )

            try:
                columnas = {
                    fila[1]
                    for fila in conexion.execute(
                        "PRAGMA table_info(developer_users)"
                    ).fetchall()
                }
            finally:
                conexion.close()

            self.assertIn(
                "security_version",
                columnas,
            )


    def test_media_developer_permanece_fuera_de_git(self):
        """Los medios personales Developer permanecen fuera del repositorio."""

        raiz = Path(
            __file__
        ).resolve().parents[1]

        gitignore = (
            raiz
            / ".gitignore"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "data/developer/",
            gitignore,
        )

        with patch.dict(
            os.environ,
            {},
            clear=False,
        ):
            os.environ.pop(
                "MRP_DEVELOPER_MEDIA_DIR",
                None,
            )

            almacen = (
                raiz
                / "data"
                / "developer"
                / "portal.sqlite3"
            )

            esperado = (
                raiz
                / "data"
                / "developer"
                / "media"
            ).resolve()

            self.assertEqual(
                esperado,
                ruta_media_developer(
                    almacen
                ),
            )


if __name__ == "__main__":
    unittest.main()
