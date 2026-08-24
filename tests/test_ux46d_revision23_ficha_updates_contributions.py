"""Regresiones UX.4.6d R23: Ficha Digital más reciente actualiza Paso 2."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision23FichaActualizaCuotas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.detalle_js = (ROOT / "app/static/js/current_year_detail.js").read_text(encoding="utf-8")
        cls.import_js = (ROOT / "app/static/js/official_data_import.js").read_text(encoding="utf-8")

    def test_ficha_confirmada_puede_ampliar_referencia_del_paso2(self):
        self.assertIn('return "FICHA_DIGITAL";', self.detalle_js)
        self.assertIn('if (resumen.cuotas > cuotasPaso2)', self.detalle_js)
        self.assertIn('fuente === "FICHA_DIGITAL" && resumen.cuotas < cuotasAnteriores', self.detalle_js)
        self.assertIn('FICHA_DIGITAL_ACTUALIZADO', self.detalle_js)

    def test_importacion_sincroniza_si_aporta_mas_cuotas(self):
        confirmar = self.import_js.split("async function confirmarFichaDigitalImportacion()", 1)[1]
        self.assertIn("cuotasMarcadas > cuotasReferenciaAntes", confirmar)
        self.assertIn('fuente: "FICHA_DIGITAL"', confirmar)
        self.assertIn("await analizarCuotas(", confirmar)
        self.assertIn("El Paso 2 se actualizó automáticamente", confirmar)

    def test_ficha_con_menos_meses_no_reduce_paso2(self):
        self.assertIn("una ficha con menos", self.detalle_js.lower())
        confirmar = self.import_js.split("async function confirmarFichaDigitalImportacion()", 1)[1]
        self.assertIn("cuotasMarcadas < cuotasReferenciaPaso2", confirmar)
        self.assertIn("Se conserva la referencia superior del Paso 2", confirmar)

    def test_referencia_persistida_del_detalle_se_actualiza(self):
        self.assertIn(
            "simulacion.detalle_anio_actual.cuotas_anio_actual_referencia = resumen.cuotas",
            self.detalle_js,
        )


if __name__ == "__main__":
    unittest.main()
