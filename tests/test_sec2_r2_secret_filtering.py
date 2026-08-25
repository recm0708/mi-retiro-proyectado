"""Regresiones SEC.2 R2: filtrado de secretos sensibles."""

from __future__ import annotations

import unittest

from app.core.observability import _SENSITIVE_KEY_PARTS


class TestSec2R2SecretFiltering(unittest.TestCase):
    def test_claves_administrativas_sensibles_estan_protegidas(self):
        for clave in (
            "authorization",
            "bearer",
            "credential",
            "password",
            "secret",
            "apikey",
            "api_key",
        ):
            self.assertIn(clave, _SENSITIVE_KEY_PARTS)


if __name__ == "__main__":
    unittest.main()
