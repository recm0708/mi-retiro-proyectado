"""Regresiones UX.4.6d R20: vigencia de Ficha Digital y resumen visible del año actual."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision20VigenciaResumen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.importacion_js = (ROOT / "app/static/js/official_data_import.js").read_text(encoding="utf-8")
        cls.detalle_js = (ROOT / "app/static/js/detalle_anio_actual.js").read_text(encoding="utf-8")
        cls.ficha_html = (ROOT / "app/templates/partials/importacion_ficha_digital.html").read_text(encoding="utf-8")
        cls.detalle_html = (ROOT / "app/templates/partials/detalle_anio_actual.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "app/static/css/design-system.css").read_text(encoding="utf-8")

    def test_ficha_digital_evalua_vigencia_con_fecha_de_referencia(self):
        self.assertIn("function evaluarVigenciaFichaDigital", self.importacion_js)
        self.assertIn('estado = "DESACTUALIZADA"', self.importacion_js)
        self.assertIn("diferenciaMeses > 0", self.importacion_js)
        self.assertNotIn("FICHA_VIGENCIA_TOLERANCIA_MESES", self.importacion_js)

    def test_ficha_desactualizada_pide_decision_sin_bloquear(self):
        self.assertIn('id="modal-vigencia-ficha-digital"', self.ficha_html)
        self.assertIn("Seleccionar una ficha más reciente", self.ficha_html)
        self.assertIn("Continuar con esta ficha", self.ficha_html)
        self.assertIn("mostrarDecisionVigenciaFichaDigital(contenido)", self.importacion_js)
        self.assertIn("continuarConFichaPendienteVigencia", self.importacion_js)
        self.assertIn("seleccionarOtraFichaPorVigencia", self.importacion_js)

    def test_periodo_mas_reciente_permanece_visible_tras_confirmar_importacion(self):
        self.assertIn("Último período detectado:", self.importacion_js)
        self.assertIn("official-import-persisted-recency", self.importacion_js)
        self.assertIn("Considera utilizar una Ficha Digital más reciente", self.importacion_js)
        self.assertIn("official-import-persisted-recency.warning", self.css)

    def test_resumen_detalle_actual_es_visible_y_completo(self):
        self.assertIn('id="detalle-resumen-visible"', self.detalle_html)
        for control in (
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
        ):
            self.assertIn(f'id="{control}"', self.detalle_html)
        self.assertIn("actualizarResumenVisibleDetalleAnioActual", self.detalle_js)
        self.assertIn('seccion.classList.remove("d-none")', self.detalle_js)

    def test_resumen_visible_se_oculta_al_invalidar_para_no_mostrar_datos_obsoletos(self):
        self.assertGreaterEqual(
            self.detalle_js.count('document.getElementById("detalle-resumen-visible")?.classList.add("d-none")'),
            2,
        )


if __name__ == "__main__":
    unittest.main()
