"""SEC.2 R6 - Seguridad de sesiones administrativas."""

import unittest

from app.core.admin_session import (
    crear_sesion_admin,
    eliminar_sesion_admin,
    obtener_sesiones_activas,
    revocar_todas_las_sesiones_admin,
    validar_sesion_admin,
)


class TestSec2R6AdminSessionSecurity(unittest.TestCase):
    def tearDown(self):
        revocar_todas_las_sesiones_admin()

    def test_sesion_creada_es_valida(self):
        sesion = crear_sesion_admin()
        self.assertTrue(validar_sesion_admin(sesion))

    def test_logout_revoca_sesion(self):
        sesion = crear_sesion_admin()
        eliminar_sesion_admin(sesion)
        self.assertFalse(validar_sesion_admin(sesion))

    def test_revocacion_global_elimina_sesiones(self):
        crear_sesion_admin()
        revocar_todas_las_sesiones_admin()
        self.assertEqual([], obtener_sesiones_activas())


if __name__ == "__main__":
    unittest.main()
