"""DEV.2 R6 — Bootstrap y recuperación protegida del Propietario."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from app.core.developer_identity import (
    RolDeveloper,
    hashear_password,
    verificar_codigo_recuperacion,
    verificar_password,
)
from app.core.developer_provisioning import (
    autenticar_usuario_developer,
    bootstrap_propietario,
    recuperar_propietario,
    restablecer_password_developer,
)
from app.core.developer_store import (
    crear_usuario_developer,
    obtener_propietario,
    obtener_usuario_por_login,
)


class TestDev2R6Provisioning(unittest.TestCase):

    @staticmethod
    def _ruta(temp: str) -> Path:
        return Path(temp) / "portal.sqlite3"

    def _bootstrap(self, ruta: Path):
        return bootstrap_propietario(
            usuario="propietario",
            nombre_visible="Propietario de prueba",
            password="MRP-Owner-Inicial-2026",
            ruta=ruta,
        )

    def test_bootstrap_crea_owner_y_codigo_separado(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)

            propietario, codigo = self._bootstrap(
                ruta
            )

            self.assertTrue(
                propietario.es_propietario
            )
            self.assertEqual(
                RolDeveloper.PROPIETARIO,
                propietario.rol,
            )
            self.assertNotIn(
                codigo,
                propietario.recovery_code_hash,
            )
            self.assertTrue(
                verificar_codigo_recuperacion(
                    codigo,
                    propietario.recovery_code_hash,
                )
            )

    def test_bootstrap_no_puede_repetirse(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            self._bootstrap(ruta)

            with self.assertRaises(ValueError):
                self._bootstrap(ruta)

    def test_autenticacion_valida_e_invalida(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            self._bootstrap(ruta)

            valido = autenticar_usuario_developer(
                "propietario",
                "MRP-Owner-Inicial-2026",
                ruta,
            )
            invalido = autenticar_usuario_developer(
                "propietario",
                "MRP-Password-Incorrecta",
                ruta,
            )

            self.assertIsNotNone(valido)
            self.assertIsNone(invalido)

    def test_reset_ordinario_rechaza_propietario(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            propietario, _ = self._bootstrap(
                ruta
            )

            with self.assertRaises(
                PermissionError
            ):
                restablecer_password_developer(
                    actor=propietario,
                    usuario_objetivo="propietario",
                    nueva_password=(
                        "MRP-Nueva-Owner-2026"
                    ),
                    ruta=ruta,
                )

    def test_admin_puede_resetear_operador(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            propietario, _ = self._bootstrap(
                ruta
            )

            admin = crear_usuario_developer(
                actor_rol=RolDeveloper.PROPIETARIO,
                usuario="admin01",
                nombre_visible="Administrador Uno",
                rol=RolDeveloper.ADMINISTRADOR,
                password_hash=hashear_password(
                    "MRP-Admin-Inicial-2026"
                ),
                ruta=ruta,
            )

            crear_usuario_developer(
                actor_rol=RolDeveloper.ADMINISTRADOR,
                usuario="operador01",
                nombre_visible="Operador Uno",
                rol=RolDeveloper.OPERADOR,
                password_hash=hashear_password(
                    "MRP-Operador-Inicial-2026"
                ),
                ruta=ruta,
            )

            actualizado = (
                restablecer_password_developer(
                    actor=admin,
                    usuario_objetivo="operador01",
                    nueva_password=(
                        "MRP-Operador-Nueva-2026"
                    ),
                    ruta=ruta,
                )
            )

            self.assertTrue(
                actualizado.debe_cambiar_password
            )
            self.assertTrue(
                verificar_password(
                    "MRP-Operador-Nueva-2026",
                    actualizado.password_hash,
                )
            )

    def test_admin_no_puede_resetear_admin(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            propietario, _ = self._bootstrap(
                ruta
            )

            admin1 = crear_usuario_developer(
                actor_rol=RolDeveloper.PROPIETARIO,
                usuario="admin01",
                nombre_visible="Administrador Uno",
                rol=RolDeveloper.ADMINISTRADOR,
                password_hash=hashear_password(
                    "MRP-Admin-Uno-2026"
                ),
                ruta=ruta,
            )

            crear_usuario_developer(
                actor_rol=RolDeveloper.PROPIETARIO,
                usuario="admin02",
                nombre_visible="Administrador Dos",
                rol=RolDeveloper.ADMINISTRADOR,
                password_hash=hashear_password(
                    "MRP-Admin-Dos-2026"
                ),
                ruta=ruta,
            )

            with self.assertRaises(
                PermissionError
            ):
                restablecer_password_developer(
                    actor=admin1,
                    usuario_objetivo="admin02",
                    nueva_password=(
                        "MRP-Admin-Nueva-2026"
                    ),
                    ruta=ruta,
                )

    def test_recovery_invalido_no_cambia_password(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            self._bootstrap(ruta)

            with self.assertRaises(
                PermissionError
            ):
                recuperar_propietario(
                    codigo_recuperacion=(
                        "MRP-OWNER-RECOVERY-invalido"
                    ),
                    nueva_password=(
                        "MRP-Owner-Nueva-2026"
                    ),
                    ruta=ruta,
                )

            propietario = obtener_propietario(
                ruta
            )

            self.assertTrue(
                verificar_password(
                    "MRP-Owner-Inicial-2026",
                    propietario.password_hash,
                )
            )

    def test_recovery_valido_rota_password_y_codigo(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            _, codigo_anterior = self._bootstrap(
                ruta
            )

            actualizado, codigo_nuevo = (
                recuperar_propietario(
                    codigo_recuperacion=(
                        codigo_anterior
                    ),
                    nueva_password=(
                        "MRP-Owner-Nueva-2026"
                    ),
                    ruta=ruta,
                )
            )

            self.assertNotEqual(
                codigo_anterior,
                codigo_nuevo,
            )
            self.assertTrue(
                verificar_password(
                    "MRP-Owner-Nueva-2026",
                    actualizado.password_hash,
                )
            )
            self.assertFalse(
                verificar_codigo_recuperacion(
                    codigo_anterior,
                    actualizado.recovery_code_hash,
                )
            )
            self.assertTrue(
                verificar_codigo_recuperacion(
                    codigo_nuevo,
                    actualizado.recovery_code_hash,
                )
            )

            with self.assertRaises(
                PermissionError
            ):
                recuperar_propietario(
                    codigo_recuperacion=(
                        codigo_anterior
                    ),
                    nueva_password=(
                        "MRP-Owner-Otra-2026"
                    ),
                    ruta=ruta,
                )

    def test_hashes_no_aparecen_en_repr_del_usuario(self):
        with TemporaryDirectory() as temp:
            ruta = self._ruta(temp)
            propietario, _ = self._bootstrap(
                ruta
            )

            representacion = repr(
                propietario
            )

            self.assertNotIn(
                "$argon2id$",
                representacion,
            )
            self.assertNotIn(
                "recovery_code_hash=",
                representacion,
            )

            recuperado = obtener_usuario_por_login(
                "propietario",
                ruta,
            )
            self.assertIsNotNone(recuperado)


if __name__ == "__main__":
    unittest.main()
