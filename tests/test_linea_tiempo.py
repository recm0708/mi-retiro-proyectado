"""Pruebas de la línea temporal histórica y futura."""

import unittest

from app.models.simulacion import (
    DatosCuotas,
    DatosHistorialSalarial,
    DatosLineaTiempo,
    DatosProyeccionSalario,
    DatosSalario,
    RegistroHistorialSalarial,
)
from app.services.linea_tiempo import (
    construir_linea_tiempo,
)


class LineaTiempoTests(unittest.TestCase):
    """Valida estados históricos y salarios proyectados."""

    def test_sin_cotizacion_y_precision_futura(self):
        datos = DatosLineaTiempo(
            historial=DatosHistorialSalarial(
                anio_inicio=2025,
                anio_fin=2026,
                cuotas_totales_referencia=5,
                registros=[
                    RegistroHistorialSalarial(
                        anio=2025,
                        cuotas=0,
                        salario_cotizado=0,
                    ),
                    RegistroHistorialSalarial(
                        anio=2026,
                        cuotas=5,
                        salario_cotizado=6659.50,
                    ),
                ],
            ),
            cuotas=DatosCuotas(
                cuotas_totales=5,
                cuotas_anio_actual=5,
                continua_cotizando=True,
                cuotas_esperadas_cierre_anio=5,
                cuotas_esperadas_por_anio=12,
            ),
            salario_actual=DatosSalario(
                monto=1331.90,
                periodicidad="MENSUAL",
            ),
            proyeccion=DatosProyeccionSalario(
                salario_mensual_actual=1331.90,
                anio_inicio=2026,
                anio_fin=2027,
                modalidad="PORCENTAJE",
                porcentaje_anual=1,
            ),
        )

        resumen = construir_linea_tiempo(
            datos
        )

        registros = (
            resumen.escenarios[0].registros
        )

        self.assertEqual(
            registros[0].estado,
            "SIN_COTIZACION",
        )
        self.assertEqual(
            registros[-1].salario_proyectado,
            16142.63,
        )


if __name__ == "__main__":
    unittest.main()
