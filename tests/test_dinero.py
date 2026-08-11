"""Pruebas de precisión monetaria."""

import unittest

from app.core.dinero import (
    redondear_moneda,
    tiene_maximo_dos_decimales,
)


class DineroTests(unittest.TestCase):
    """Valida el criterio monetario común."""

    def test_round_half_up(self):
        self.assertEqual(
            redondear_moneda("1.005"),
            1.01,
        )

    def test_maximo_dos_decimales(self):
        self.assertTrue(
            tiene_maximo_dos_decimales("10.90")
        )
        self.assertFalse(
            tiene_maximo_dos_decimales("10.901")
        )


if __name__ == "__main__":
    unittest.main()
