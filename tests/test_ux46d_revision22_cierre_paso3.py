"""Regresiones UX.4.6d R22: cierre del Paso 3 sin bloqueos silenciosos."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision22CierrePaso3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detalle_js = (ROOT / "app/static/js/current_year_detail.js").read_text(encoding="utf-8")
        cls.detalle_html = (ROOT / "app/templates/partials/current_year_detail.html").read_text(encoding="utf-8")

    def test_validacion_reconcilia_cuotas_manuales_antes_del_payload(self):
        self.assertIn("function detallePuedeReconciliarCuotasPaso2", self.detalle_js)
        validar = self.detalle_js.split("async function validarDetalleAnioActual()", 1)[1]
        posicion_sync = validar.index("sincronizarCuotasPaso2DesdeDetalle({")
        posicion_leer = validar.index("datos = leerDetalleAnioActual()")
        self.assertLess(posicion_sync, posicion_leer)
        self.assertIn('control.dataset.importedLocked !== "true"', self.detalle_js)
        self.assertIn('origenes.cuotas_anio_actual === "DETALLE_ANIO_ACTUAL_EDITADO"', self.detalle_js)
        self.assertIn('fuenteReconciliacionCuotasPaso2()', self.detalle_js)

    def test_si_cambia_referencia_revalida_paso2_sin_navegar(self):
        validar = self.detalle_js.split("async function validarDetalleAnioActual()", 1)[1]
        self.assertIn("const cuotasRevalidadas = await analizarCuotas(", validar)
        self.assertIn("mostrarMensajes: false", validar)
        self.assertIn("reportarValidez: false", validar)
        self.assertIn("no fue posible revalidar el Paso 2", validar)

    def test_incoherencia_del_detalle_muestra_error_explicito(self):
        self.assertIn("if (!contenido.cuotas_coinciden)", self.detalle_js)
        self.assertIn("El detalle identifica ${contenido.cuotas_acreditadas_identificadas}", self.detalle_js)
        self.assertIn("pero el Paso 2 registra ${cuotasPaso2}", self.detalle_js)
        self.assertIn("Revisa únicamente las casillas de Cuota acreditada", self.detalle_js)

    def test_resumen_visible_conserva_metricas_no_redundantes(self):
        ids = [
            "detalle-resumen-cuotas",
            "detalle-resumen-salario-disponible",
            "detalle-resumen-salario-acreditado",
            "detalle-resumen-meses-info",
            "detalle-resumen-meses-completos",
            "detalle-resumen-ultimo-mes-completo",
            "detalle-resumen-ultimo-mes-cuota",
            "detalle-resumen-ultimo-salario",
            "detalle-resumen-promedio-completos",
            "detalle-resumen-promedio-tres",
            "detalle-resumen-promedio-cuota",
        ]
        for element_id in ids:
            with self.subTest(element_id=element_id):
                self.assertIn(f'id="{element_id}"', self.detalle_html)


if __name__ == "__main__":
    unittest.main()
