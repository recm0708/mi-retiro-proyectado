"""DEV.2 R6 — Regresiones de interacción de la CLI Developer."""

from __future__ import annotations

import unittest
from unittest.mock import patch

from app.cli.admin import _password_confirmada


class TestDev2R6DeveloperCli(unittest.TestCase):

    @patch(
        "app.cli.admin.getpass",
        side_effect=[
            "corta",
            "MRP-Nueva!Segura-2026",
            "MRP-Nueva!Segura-2026",
        ],
    )
    def test_password_invalida_vuelve_a_solicitarse(
        self,
        getpass_mock,
    ):
        resultado = _password_confirmada(
            "Contraseña: "
        )

        self.assertEqual(
            "MRP-Nueva!Segura-2026",
            resultado,
        )
        self.assertEqual(
            3,
            getpass_mock.call_count,
        )

    @patch(
        "app.cli.admin.getpass",
        side_effect=[
            "MRP-Primera!Segura-2026",
            "MRP-NoCoincide!2026",
            "MRP-Segunda!Segura-2026",
            "MRP-Segunda!Segura-2026",
        ],
    )
    def test_confirmacion_incorrecta_vuelve_a_solicitarse(
        self,
        getpass_mock,
    ):
        resultado = _password_confirmada(
            "Contraseña: "
        )

        self.assertEqual(
            "MRP-Segunda!Segura-2026",
            resultado,
        )
        self.assertEqual(
            4,
            getpass_mock.call_count,
        )


if __name__ == "__main__":
    unittest.main()
