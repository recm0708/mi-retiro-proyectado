"""Regresiones de UX.4.6d R8 para estados, tablas y carga de archivos."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision8Tablas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.historial = (
            ROOT / "app/templates/partials/salary_history.html"
        ).read_text(encoding="utf-8")
        cls.historial_js = (
            ROOT / "app/static/js/salary_history.js"
        ).read_text(encoding="utf-8")
        cls.importacion_js = (
            ROOT / "app/static/js/official_data_import.js"
        ).read_text(encoding="utf-8")
        cls.style = (ROOT / "app/static/css/style.css").read_text(encoding="utf-8")
        cls.design = (
            ROOT / "app/static/css/design-system.css"
        ).read_text(encoding="utf-8")

    def test_historial_define_estados_progresivos_segun_datos_disponibles(self):
        for etiqueta in (
            "Pendiente",
            "Falta salario",
            "Faltan cuotas",
            "Revisar",
            "Sin cotización",
            "Parcial",
            "Completo",
        ):
            self.assertIn(f'etiqueta: "{etiqueta}"', self.historial_js)
        self.assertIn("function evaluarEstadoFilaHistorial", self.historial_js)

    def test_estado_de_fila_se_actualiza_al_escribir_cuotas_o_salario(self):
        self.assertIn("function manejarEdicionDelegadaHistorial", self.historial_js)
        self.assertIn('cuerpo.addEventListener("input", manejarEdicionDelegadaHistorial)', self.historial_js)
        self.assertIn('cuerpo.addEventListener("change", manejarEdicionDelegadaHistorial)', self.historial_js)
        self.assertIn("actualizarEstadoFila(fila)", self.historial_js)

    def test_filtro_pendientes_usa_estado_semantico_y_compacta_tabla_corta(self):
        self.assertIn("return evaluarEstadoFilaHistorial(fila).pendiente", self.historial_js)
        self.assertIn('classList.toggle("table-scroll-compact", tablaCorta)', self.historial_js)
        self.assertIn(".table-scroll-compact", self.style)
        self.assertIn("overflow: visible !important", self.style)
        self.assertIn("overflow-y: clip !important", self.style)
        self.assertIn("scrollbar-gutter: auto", self.style)

    def test_historial_muestra_resumen_local_despues_del_analisis(self):
        for identificador in (
            "historial-resumen-analizado",
            "historial-resumen-cuotas-referencia",
            "historial-resumen-cuotas-identificadas",
            "historial-resumen-diferencia",
            "historial-resumen-total-salarios",
        ):
            self.assertIn(f'id="{identificador}"', self.historial)
        self.assertIn("mostrarResumenHistorialAnalizado(resumen)", self.historial_js)
        self.assertIn("ocultarResumenHistorialAnalizado()", self.historial_js)

    def test_selector_archivo_usa_tratamiento_visual_global_en_tres_temas(self):
        selector = (
            'input[type="file"].form-control'
            '::file-selector-button'
        )

        self.assertNotIn(
            selector,
            self.style,
        )

        self.assertIn(
            selector,
            self.design,
        )

        self.assertIn(
            'html[data-bs-theme="dark"] '
            'input[type="file"].form-control {',
            self.design,
        )

        self.assertIn(
            'html[data-app-theme="contrast"] '
            'input[type="file"].form-control {',
            self.design,
        )

        for token in (
            "--app-file-button-color",
            "--app-file-button-bg",
            "--app-file-button-hover-bg",
            "--app-file-button-border",
        ):
            with self.subTest(token=token):
                self.assertIn(
                    token,
                    self.design,
                )

    def test_mensaje_del_ultimo_mes_no_desalinea_la_celda_de_estado(self):
        self.assertNotIn('nota.textContent = "Revisa si este mes está completo o parcial."', self.importacion_js)
        self.assertIn("Revisa si el último mes detectado está completo o parcial", self.importacion_js)
        self.assertIn("const controles = [mes, salarioGrupo, estado, cuota]", self.importacion_js)


if __name__ == "__main__":
    unittest.main()
