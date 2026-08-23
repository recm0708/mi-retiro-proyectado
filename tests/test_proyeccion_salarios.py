"""Pruebas del motor de proyección salarial."""

import unittest

from app.models.simulacion import (
    DatosProyeccionSalario,
)
from app.services.proyeccion_salarios import (
    proyectar_salario,
)


class ProyeccionSalariosTests(unittest.TestCase):
    """Valida precisión y crecimiento salarial."""

    def test_caso_femenino_un_por_ciento(self):
        resumen = proyectar_salario(
            DatosProyeccionSalario(
                salario_mensual_actual=1331.90,
                anio_inicio=2026,
                anio_fin=2027,
                modalidad="PORCENTAJE",
                porcentaje_anual=1,
            )
        )

        registro_2027 = (
            resumen.escenarios[0].registros[1]
        )

        self.assertEqual(
            registro_2027.salario_mensual,
            1345.22,
        )
        self.assertEqual(
            registro_2027.salario_anual,
            16142.63,
        )

    def test_no_admite_tres_decimales_editables(self):
        with self.assertRaises(ValueError):
            DatosProyeccionSalario(
                salario_mensual_actual=1000,
                anio_inicio=2026,
                anio_fin=2027,
                modalidad="PORCENTAJE",
                porcentaje_anual=1.234,
            )


if __name__ == "__main__":
    unittest.main()
