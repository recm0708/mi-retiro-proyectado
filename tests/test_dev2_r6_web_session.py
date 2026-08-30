"""DEV.2 R6 — Regresiones de sesiones web vinculadas a identidad."""

from __future__ import annotations

import unittest

from app.core.admin_session import (
    crear_sesion_admin,
    eliminar_sesion_admin,
    obtener_sesion_admin,
    revocar_sesiones_usuario,
    revocar_todas_las_sesiones_admin,
    validar_sesion_admin,
    validar_sesion_admin_con_identidad,
    validar_sesion_admin_para_usuario,
)
from app.core.developer_identity import (
    RolDeveloper,
)


class TestDev2R6WebSession(unittest.TestCase):
    """Protege el contrato de identidad de las sesiones Developer."""

    def setUp(self):
        """Aísla el almacén de sesiones antes de cada prueba."""

        revocar_todas_las_sesiones_admin()

    def tearDown(self):
        """Limpia el almacén de sesiones después de cada prueba."""

        revocar_todas_las_sesiones_admin()

    @staticmethod
    def _crear_identificada(
        *,
        usuario_id: str,
        usuario: str,
        rol: RolDeveloper,
        revision: int = 1,
    ) -> str:
        """Crea una sesión R6 completa para las pruebas."""

        return crear_sesion_admin(
            usuario_id=usuario_id,
            usuario=usuario,
            rol=rol,
            revision_seguridad=revision,
        )

    def test_sesion_r6_conserva_identidad_rol_y_revision(self):
        """Una sesión humana conserva identidad, rol y revisión."""

        identificador = self._crear_identificada(
            usuario_id="usuario-id-001",
            usuario="recm0708",
            rol=RolDeveloper.PROPIETARIO,
        )

        sesion = obtener_sesion_admin(
            identificador,
            actualizar_actividad=False,
        )

        self.assertIsNotNone(sesion)
        self.assertEqual(
            "usuario-id-001",
            sesion.usuario_id,
        )
        self.assertEqual(
            "recm0708",
            sesion.usuario,
        )
        self.assertEqual(
            RolDeveloper.PROPIETARIO,
            sesion.rol,
        )
        self.assertEqual(
            1,
            sesion.revision_seguridad,
        )
        self.assertTrue(
            sesion.tiene_identidad
        )

    def test_sesion_r6_es_valida_con_identidad(self):
        """La validación R6 distingue sesiones humanas identificadas."""

        identificador = self._crear_identificada(
            usuario_id="usuario-id-002",
            usuario="operador01",
            rol=RolDeveloper.OPERADOR,
        )

        self.assertTrue(
            validar_sesion_admin(
                identificador
            )
        )
        self.assertTrue(
            validar_sesion_admin_con_identidad(
                identificador
            )
        )

    def test_sesion_legacy_sigue_valida_pero_no_identificada(self):
        """La API histórica permanece disponible durante la migración."""

        identificador = crear_sesion_admin()

        self.assertTrue(
            validar_sesion_admin(
                identificador
            )
        )
        self.assertFalse(
            validar_sesion_admin_con_identidad(
                identificador
            )
        )

    def test_identidad_parcial_es_rechazada(self):
        """No se crean sesiones con identidad incompleta."""

        with self.assertRaises(
            ValueError
        ):
            crear_sesion_admin(
                usuario_id="usuario-id-003",
                usuario="auditor01",
                rol=RolDeveloper.AUDITOR,
            )

    def test_rol_invalido_es_rechazado(self):
        """Un rol desconocido no puede persistirse en una sesión."""

        with self.assertRaises(
            ValueError
        ):
            crear_sesion_admin(
                usuario_id="usuario-id-004",
                usuario="usuario04",
                rol="superadmin",
                revision_seguridad=1,
            )

    def test_revocacion_por_usuario_no_afecta_otras_cuentas(self):
        """La revocación de una identidad preserva sesiones ajenas."""

        sesion_uno = self._crear_identificada(
            usuario_id="usuario-id-005",
            usuario="operador05",
            rol=RolDeveloper.OPERADOR,
        )
        sesion_dos = self._crear_identificada(
            usuario_id="usuario-id-005",
            usuario="operador05",
            rol=RolDeveloper.OPERADOR,
        )
        sesion_otra = self._crear_identificada(
            usuario_id="usuario-id-006",
            usuario="auditor06",
            rol=RolDeveloper.AUDITOR,
        )

        revocadas = revocar_sesiones_usuario(
            "usuario-id-005"
        )

        self.assertEqual(
            2,
            revocadas,
        )
        self.assertFalse(
            validar_sesion_admin(sesion_uno)
        )
        self.assertFalse(
            validar_sesion_admin(sesion_dos)
        )
        self.assertTrue(
            validar_sesion_admin(sesion_otra)
        )

    def test_eliminar_sesion_invalida_identificador(self):
        """El cierre individual elimina completamente una sesión."""

        identificador = self._crear_identificada(
            usuario_id="usuario-id-007",
            usuario="admin07",
            rol=RolDeveloper.ADMINISTRADOR,
        )

        eliminar_sesion_admin(
            identificador
        )

        self.assertIsNone(
            obtener_sesion_admin(
                identificador
            )
        )

    def test_revision_antigua_invalida_sesion(self):
        """Una revisión persistente nueva revoca una sesión anterior."""

        identificador = self._crear_identificada(
            usuario_id="usuario-id-008",
            usuario="operador08",
            rol=RolDeveloper.OPERADOR,
            revision=1,
        )

        self.assertFalse(
            validar_sesion_admin_para_usuario(
                identificador,
                usuario_id="usuario-id-008",
                revision_seguridad=2,
            )
        )

        self.assertIsNone(
            obtener_sesion_admin(
                identificador
            )
        )


if __name__ == "__main__":
    unittest.main()
