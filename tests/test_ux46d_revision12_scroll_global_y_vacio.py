"""Regresiones UX.4.6d R12 para scroll global, tablas vacías y carga estable."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision12ScrollGlobalYVacio(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.design = (ROOT / "app/static/css/design-system.css").read_text(encoding="utf-8")
        cls.historial = (ROOT / "app/templates/partials/historial_salarial.html").read_text(encoding="utf-8")
        cls.historial_js = (ROOT / "app/static/js/historial_salarios.js").read_text(encoding="utf-8")
        cls.comparar = (ROOT / "app/templates/comparar.html").read_text(encoding="utf-8")

    def test_scrollbar_tematico_se_extiende_a_terminos_modales_y_pagina(self):
        for selector in (
            "html::-webkit-scrollbar-button",
            "body::-webkit-scrollbar-button",
            ".modal-body::-webkit-scrollbar-button",
            ".privacy-consent-body::-webkit-scrollbar-button",
            ".app-table-shell::-webkit-scrollbar-button",
        ):
            self.assertIn(selector, self.design)
        self.assertIn("display: none !important", self.design)
        self.assertIn("scrollbar-width: thin", self.design)

    def test_tabla_usa_radio_menor_que_las_tarjetas(self):
        self.assertIn("--app-table-radius: var(--app-radius-md)", self.design)
        self.assertIn("margin-block: 0.4rem", self.design)

    def test_pendientes_sin_filas_oculta_tabla_y_muestra_estado_vacio(self):
        self.assertIn('id="historial-filtro-vacio"', self.historial)
        self.assertIn("No hay años pendientes por completar.", self.historial)
        self.assertIn('filtroHistorialActual === "PENDIENTES" && visibles === 0', self.historial_js)
        self.assertIn('contenedor.classList.toggle("d-none", sinPendientesVisibles)', self.historial_js)
        self.assertIn('vacio.classList.toggle("d-none", !sinPendientesVisibles)', self.historial_js)

    def test_selector_archivo_no_cambia_por_hover_del_nombre(self):
        self.assertIn('input[type="file"].form-control:hover::file-selector-button', self.design)
        self.assertIn('input[type="file"].form-control::file-selector-button:hover', self.design)
        self.assertIn("--app-file-button-bg", self.design)
        self.assertIn("--app-file-button-hover-bg", self.design)

    def test_comparador_conserva_contrato_tabular_comun(self):
        self.assertIn('class="table-responsive app-table-shell"', self.comparar)


if __name__ == "__main__":
    unittest.main()
