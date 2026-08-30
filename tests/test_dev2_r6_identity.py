"""DEV.2 R6 — Regresiones de identidad y autorización Developer."""

from __future__ import annotations

import unittest

from app.core.developer_identity import (
    PermisoDeveloper,
    RolDeveloper,
    generar_codigo_recuperacion_propietario,
    hashear_codigo_recuperacion,
    hashear_password,
    normalizar_nombre_visible,
    normalizar_usuario,
    password_necesita_rehash,
    permisos_para_rol,
    rol_puede_asignar,
    rol_tiene_permiso,
    verificar_codigo_recuperacion,
    verificar_password,
)


class TestDev2R6DeveloperIdentity(unittest.TestCase):

    def test_password_se_hashea_con_argon2id(self):
        password = "MRP-prueba-segura-2026"
        password_hash = hashear_password(password)

        self.assertTrue(password_hash.startswith("$argon2id$"))
        self.assertNotEqual(password, password_hash)
        self.assertTrue(verificar_password(password, password_hash))
        self.assertFalse(
            verificar_password(
                "MRP-password-incorrecta",
                password_hash,
            )
        )
        self.assertFalse(password_necesita_rehash(password_hash))

    def test_password_corta_es_rechazada(self):
        with self.assertRaises(ValueError):
            hashear_password("corta")

    def test_usuario_se_normaliza_y_valida(self):
        self.assertEqual(
            "recm0708",
            normalizar_usuario("  RECm0708  "),
        )

        with self.assertRaises(ValueError):
            normalizar_usuario("usuario con espacios")

    def test_nombre_visible_conserva_unicode(self):
        self.assertEqual(
            "Rubén Enrique Cañizares Miranda",
            normalizar_nombre_visible(
                "  Rubén   Enrique Cañizares   Miranda  "
            ),
        )

    def test_codigo_recuperacion_no_se_almacena_en_claro(self):
        codigo = generar_codigo_recuperacion_propietario()
        codigo_hash = hashear_codigo_recuperacion(codigo)

        self.assertTrue(codigo.startswith("MRP-OWNER-RECOVERY-"))
        self.assertTrue(codigo_hash.startswith("$argon2id$"))
        self.assertNotEqual(codigo, codigo_hash)
        self.assertTrue(
            verificar_codigo_recuperacion(
                codigo,
                codigo_hash,
            )
        )
        self.assertFalse(
            verificar_codigo_recuperacion(
                generar_codigo_recuperacion_propietario(),
                codigo_hash,
            )
        )

    def test_propietario_posee_todos_los_permisos_definidos(self):
        permisos = permisos_para_rol(
            RolDeveloper.PROPIETARIO,
        )

        self.assertEqual(
            set(PermisoDeveloper),
            set(permisos),
        )

    def test_administrador_no_puede_gestionar_propietario(self):
        self.assertFalse(
            rol_tiene_permiso(
                RolDeveloper.ADMINISTRADOR,
                PermisoDeveloper.PROPIETARIO_GESTIONAR,
            )
        )

        self.assertFalse(
            rol_puede_asignar(
                RolDeveloper.ADMINISTRADOR,
                RolDeveloper.PROPIETARIO,
            )
        )

    def test_solo_propietario_puede_asignar_administrador(self):
        self.assertTrue(
            rol_puede_asignar(
                RolDeveloper.PROPIETARIO,
                RolDeveloper.ADMINISTRADOR,
            )
        )

        self.assertFalse(
            rol_puede_asignar(
                RolDeveloper.ADMINISTRADOR,
                RolDeveloper.ADMINISTRADOR,
            )
        )

    def test_administrador_puede_asignar_roles_basicos(self):
        self.assertTrue(
            rol_puede_asignar(
                RolDeveloper.ADMINISTRADOR,
                RolDeveloper.OPERADOR,
            )
        )
        self.assertTrue(
            rol_puede_asignar(
                RolDeveloper.ADMINISTRADOR,
                RolDeveloper.AUDITOR,
            )
        )

    def test_operador_y_auditor_no_administran_usuarios(self):
        for rol in (
            RolDeveloper.OPERADOR,
            RolDeveloper.AUDITOR,
        ):
            self.assertFalse(
                rol_tiene_permiso(
                    rol,
                    PermisoDeveloper.USUARIOS_CREAR,
                )
            )
            self.assertFalse(
                rol_puede_asignar(
                    rol,
                    RolDeveloper.AUDITOR,
                )
            )


    def test_password_sin_mayuscula_es_rechazada(self):
        with self.assertRaises(ValueError):
            hashear_password(
                "mrp-password-segura-2026!"
            )

    def test_password_sin_caracter_especial_es_rechazada(self):
        with self.assertRaises(ValueError):
            hashear_password(
                "MRPPasswordSegura2026"
            )

    def test_verificacion_no_revalida_politica_historica(self):
        from argon2 import PasswordHasher

        password_historica = (
            "passwordhistorica2026"
        )
        password_hash = PasswordHasher().hash(
            password_historica
        )

        self.assertTrue(
            verificar_password(
                password_historica,
                password_hash,
            )
        )


if __name__ == "__main__":
    unittest.main()
