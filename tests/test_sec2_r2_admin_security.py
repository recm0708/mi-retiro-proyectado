"""Regresiones SEC.2 R2: seguridad administrativa base."""

from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from app.core.admin_security import (
    autenticacion_admin_habilitada,
    validar_token_administrativo,
)


class TestSec2R2AdminSecurity(unittest.TestCase):
    def test_sin_token_no_habilita_autenticacion(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertFalse(autenticacion_admin_habilitada())

    def test_token_configurado_habilita_autenticacion(self):
        with patch.dict(os.environ, {"MRP_ADMIN_TOKEN": "abc123"}, clear=False):
            self.assertTrue(autenticacion_admin_habilitada())

    def test_token_correcto_valida(self):
        with patch.dict(os.environ, {"MRP_ADMIN_TOKEN": "abc123"}, clear=False):
            self.assertTrue(validar_token_administrativo("abc123"))

    def test_token_incorrecto_no_valida(self):
        with patch.dict(os.environ, {"MRP_ADMIN_TOKEN": "abc123"}, clear=False):
            self.assertFalse(validar_token_administrativo("otro"))

    def test_token_vacio_no_valida(self):
        with patch.dict(os.environ, {"MRP_ADMIN_TOKEN": "abc123"}, clear=False):
            self.assertFalse(validar_token_administrativo(None))


if __name__ == "__main__":
    unittest.main()
