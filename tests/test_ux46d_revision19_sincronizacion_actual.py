"""Regresiones UX.4.6d R19: detalle mensual sincroniza 2026 y cuotas de Paso 2."""

import unittest
from pathlib import Path

from app.models.simulation import DatosDetalleAnioActual, RegistroDetalleAnioActual
from app.services.detalle_anio_actual import analizar_detalle_anio_actual

ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision19SincronizacionActual(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detalle_js = (ROOT / "app/static/js/detalle_anio_actual.js").read_text(encoding="utf-8")
        cls.historial_js = (ROOT / "app/static/js/salary_history.js").read_text(encoding="utf-8")
        cls.detalle_html = (ROOT / "app/templates/partials/detalle_anio_actual.html").read_text(encoding="utf-8")

    def test_seis_meses_acreditados_calculan_totales_y_promedio_correctos(self):
        salarios = [1486.88, 1555.51, 1381.01, 1565.83, 1331.90, 1562.37]
        datos = DatosDetalleAnioActual(
            anio=2026,
            modo_captura="MENSUAL",
            cuotas_anio_actual_referencia=6,
            registros=[
                RegistroDetalleAnioActual(
                    mes=indice,
                    cuota_acreditada=True,
                    estado="COMPLETO",
                    salario_mensual=salario,
                )
                for indice, salario in enumerate(salarios, start=1)
            ],
        )

        resumen = analizar_detalle_anio_actual(datos)

        self.assertEqual(resumen.cuotas_acreditadas_identificadas, 6)
        self.assertEqual(resumen.total_salario_disponible, 8883.50)
        self.assertEqual(resumen.total_salario_acreditado, 8883.50)
        self.assertEqual(resumen.promedio_meses_completos, 1480.58)
        self.assertEqual(resumen.promedio_ultimos_3_meses_completos, 1486.70)
        self.assertEqual(resumen.promedio_por_cuota_acreditada, 1480.58)
        self.assertTrue(resumen.cuotas_coinciden)

    def test_fila_anual_se_deriva_de_casillas_y_salarios_del_detalle(self):
        self.assertIn("function sincronizarFilaAnualDesdeDetalleLocal", self.detalle_js)
        self.assertIn('cuotas.value = String(resumen.cuotas)', self.detalle_js)
        self.assertIn('salario_acreditado: salarioAcreditado', self.detalle_js)
        self.assertIn('cuotas.dataset.sincronizadoDetalle = "true"', self.detalle_js)
        self.assertIn('salario.dataset.sincronizadoDetalle = "true"', self.detalle_js)
        self.assertIn("sincronizarFilaAnualDesdeDetalleLocal();", self.historial_js)

    def test_checkbox_manual_actualiza_referencia_del_paso2_sin_navegar_atras(self):
        self.assertIn("function sincronizarCuotasPaso2DesdeDetalle", self.detalle_js)
        self.assertIn("cuotasPreviasAlAnioActual", self.detalle_js)
        self.assertIn('cuotas_totales: nuevoTotal', self.detalle_js)
        self.assertIn('cuotas_anio_actual: resumen.cuotas', self.detalle_js)
        self.assertIn('DETALLE_ANIO_ACTUAL_EDITADO', self.detalle_js)
        self.assertIn('id="detalle-cuotas-sincronizadas"', self.detalle_html)

    def test_sincronizacion_backend_no_depende_de_coincidencia_previa(self):
        self.assertIn("await sincronizarDetalleConHistorial(contenido);", self.detalle_js)
        bloque = self.detalle_js.split("await sincronizarDetalleConHistorial(contenido);", 1)[0][-180:]
        self.assertNotIn("if (contenido.cuotas_coinciden)", bloque)


if __name__ == "__main__":
    unittest.main()
