"""Regresiones de UX.4.4 para el detalle salarial del año actual."""

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.modelos.simulacion import (
    DatosDetalleAnioActual,
    RegistroDetalleAnioActual,
)
from app.servicios.detalle_anio_actual import (
    analizar_detalle_anio_actual,
)


ROOT = Path(__file__).resolve().parents[1]


class TestUX44DetalleAnioActual(unittest.TestCase):
    """Protege separación entre salario disponible, cuota y proyección."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(app)
        cls.parcial = (
            ROOT / "app/templates/partials/detalle_anio_actual.html"
        ).read_text(encoding="utf-8")
        cls.simulacion = (ROOT / "app/templates/simulacion.html").read_text(
            encoding="utf-8"
        )
        cls.js = (ROOT / "app/static/js/detalle_anio_actual.js").read_text(
            encoding="utf-8"
        )
        cls.retiro = (ROOT / "app/static/js/retiro.js").read_text(
            encoding="utf-8"
        )
        cls.historial = (ROOT / "app/static/js/historial_salarios.js").read_text(
            encoding="utf-8"
        )

    def test_mensual_separa_salario_disponible_de_salario_acreditado(self):
        datos = DatosDetalleAnioActual(
            anio=2026,
            modo_captura="MENSUAL",
            cuotas_anio_actual_referencia=2,
            registros=[
                RegistroDetalleAnioActual(
                    mes=1,
                    cuota_acreditada=True,
                    estado="COMPLETO",
                    salario_mensual=1000,
                ),
                RegistroDetalleAnioActual(
                    mes=2,
                    cuota_acreditada=True,
                    estado="COMPLETO",
                    salario_mensual=1100,
                ),
                RegistroDetalleAnioActual(
                    mes=3,
                    cuota_acreditada=False,
                    estado="COMPLETO",
                    salario_mensual=1200,
                ),
            ],
        )

        resumen = analizar_detalle_anio_actual(datos)

        self.assertEqual(resumen.total_salario_acreditado, 2100.0)
        self.assertEqual(resumen.promedio_por_cuota_acreditada, 1050.0)
        self.assertEqual(resumen.total_salario_disponible, 3300.0)
        self.assertEqual(resumen.ultimo_mes_cuota_acreditada, "2026-02")
        self.assertEqual(resumen.ultimo_mes_con_salario_completo, "2026-03")
        self.assertTrue(resumen.cuotas_coinciden)

    def test_quincenal_deriva_mes_parcial_y_mes_completo(self):
        datos = DatosDetalleAnioActual(
            anio=2026,
            modo_captura="QUINCENAL",
            cuotas_anio_actual_referencia=2,
            registros=[
                RegistroDetalleAnioActual(
                    mes=1,
                    cuota_acreditada=True,
                    primera_quincena=500,
                    segunda_quincena=520,
                ),
                RegistroDetalleAnioActual(
                    mes=2,
                    cuota_acreditada=True,
                    primera_quincena=510,
                ),
            ],
        )

        resumen = analizar_detalle_anio_actual(datos)

        self.assertEqual(resumen.registros[0].estado, "COMPLETO")
        self.assertEqual(resumen.registros[0].salario_total, 1020.0)
        self.assertEqual(resumen.registros[1].estado, "PARCIAL")
        self.assertEqual(resumen.registros[1].salario_total, 510.0)
        self.assertEqual(resumen.total_salario_acreditado, 1530.0)

    def test_bases_sugeridas_solo_usan_meses_completos(self):
        datos = DatosDetalleAnioActual(
            anio=2026,
            modo_captura="MENSUAL",
            cuotas_anio_actual_referencia=2,
            registros=[
                RegistroDetalleAnioActual(
                    mes=1,
                    cuota_acreditada=True,
                    estado="COMPLETO",
                    salario_mensual=900,
                ),
                RegistroDetalleAnioActual(
                    mes=2,
                    cuota_acreditada=True,
                    estado="PARCIAL",
                    salario_mensual=400,
                ),
                RegistroDetalleAnioActual(
                    mes=3,
                    cuota_acreditada=False,
                    estado="COMPLETO",
                    salario_mensual=1200,
                ),
                RegistroDetalleAnioActual(
                    mes=4,
                    cuota_acreditada=False,
                    estado="COMPLETO",
                    salario_mensual=1500,
                ),
            ],
        )

        resumen = analizar_detalle_anio_actual(datos)

        self.assertEqual(resumen.salario_ultimo_mes_completo, 1500.0)
        self.assertEqual(resumen.promedio_meses_completos, 1200.0)
        self.assertEqual(resumen.promedio_ultimos_3_meses_completos, 1200.0)

    def test_diferencia_de_cuotas_se_informa_sin_inventar_mes(self):
        datos = DatosDetalleAnioActual(
            anio=2026,
            modo_captura="MENSUAL",
            cuotas_anio_actual_referencia=3,
            registros=[
                RegistroDetalleAnioActual(
                    mes=1,
                    cuota_acreditada=True,
                    estado="COMPLETO",
                    salario_mensual=1000,
                ),
                RegistroDetalleAnioActual(
                    mes=2,
                    cuota_acreditada=True,
                    estado="COMPLETO",
                    salario_mensual=1000,
                ),
            ],
        )

        resumen = analizar_detalle_anio_actual(datos)

        self.assertFalse(resumen.cuotas_coinciden)
        self.assertEqual(resumen.cuotas_acreditadas_identificadas, 2)
        self.assertEqual(resumen.ultimo_mes_cuota_acreditada, "2026-02")

    def test_endpoint_detalle_anio_actual_responde(self):
        respuesta = self.cliente.post(
            "/api/simulacion/detalle-anio-actual",
            json={
                "anio": 2026,
                "modo_captura": "MENSUAL",
                "cuotas_anio_actual_referencia": 1,
                "registros": [
                    {
                        "mes": 1,
                        "cuota_acreditada": True,
                        "estado": "COMPLETO",
                        "salario_mensual": 1000,
                    }
                ],
            },
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(
            respuesta.json()["ultimo_mes_cuota_acreditada"],
            "2026-01",
        )

    def test_interfaz_ofrece_ficha_digital_y_captura_manual(self):
        self.assertIn("Abrir Mi Caja Digital", self.parcial)
        self.assertIn('value="MENSUAL"', self.parcial)
        self.assertIn('value="QUINCENAL"', self.parcial)
        self.assertIn("Puedes importarlos desde el Paso 1", self.parcial)
        self.assertIn("detalle-cuota-acreditada", self.js)

    def test_base_salarial_permite_ultimo_mes_y_promedios(self):
        self.assertIn('value="ULTIMO_MES_COMPLETO"', self.simulacion)
        self.assertIn('value="PROMEDIO_ANIO_ACTUAL"', self.simulacion)
        self.assertIn('value="PROMEDIO_3_MESES"', self.simulacion)
        self.assertIn('value="PROMEDIO_CUOTA_ACREDITADA"', self.simulacion)
        self.assertIn("promedio_por_cuota_acreditada", self.js)
        self.assertIn("function obtenerValorBaseSalarial", self.js)
        self.assertIn("salario_ultimo_mes_completo", self.js)

    def test_detalle_sincroniza_total_acreditado_con_historial(self):
        self.assertIn("total_salario_acreditado", self.js)
        self.assertIn("await analizarHistorialSalarial()", self.js)
        self.assertIn("resumen_detalle_anio_actual?.cuotas_coinciden", self.historial)
        self.assertIn("inputSalario.readOnly = true", self.historial)

    def test_retiro_deriva_ultimo_mes_solo_si_cuotas_coinciden(self):
        self.assertIn("function aplicarUltimoMesCuotasDerivado", self.retiro)
        self.assertIn(".cuotas_coinciden", self.retiro)
        self.assertIn("campo.readOnly = true", self.retiro)
        self.assertIn("ultimo_mes_cuota_acreditada", self.retiro)

    def test_simulacion_carga_modulo_de_detalle(self):
        respuesta = self.cliente.get("/simulacion")
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("detalle_anio_actual.js", respuesta.text)
        self.assertIn("Detalle salarial del año actual", respuesta.text)


if __name__ == "__main__":
    unittest.main()
