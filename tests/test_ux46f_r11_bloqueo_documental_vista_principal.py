"""Regresiones UX.4.6f R1.1 para bloqueo documental y revisión explícita."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def leer(ruta: str) -> str:
    return (ROOT / ruta).read_text(encoding="utf-8")


class UX46fR11BloqueoDocumentalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.procedencia = leer("app/static/js/editable_provenance.js")
        cls.importacion = leer("app/static/js/official_data_import.js")
        cls.historial = leer("app/static/js/salary_history.js")
        cls.detalle = leer("app/static/js/current_year_detail.js")
        cls.simulacion = leer("app/static/js/simulation.js")
        cls.css = leer("app/static/css/editable-provenance.css")
        cls.design = leer("app/static/css/design-system.css")

    def test_01_detectados_se_bloquean_fuera_del_modal(self):
        self.assertIn("function aplicarBloqueoVistaPrincipal(control, bloqueado)", self.procedencia)
        self.assertIn('control.closest(".modal")', self.procedencia)
        self.assertIn('control.classList.toggle("field-imported-readonly"', self.procedencia)

    def test_02_personales_bloquean_segun_valor_original_detectado(self):
        self.assertIn("referenciaComprobanteOriginal(simulacion)", self.procedencia)
        self.assertIn("valorDetectado(original)", self.procedencia)
        self.assertIn("aplicarBloqueoVistaPrincipal(control, detectadoOriginalmente)", self.procedencia)

    def test_03_cuotas_e_historial_respetan_deteccion_original(self):
        self.assertIn("valorOriginalCuotasAnioActual", self.procedencia)
        self.assertIn('original?.salario_anual', self.procedencia)
        self.assertIn("Campo no detectado por el documento", self.procedencia)
        self.assertIn("control.readOnly || control.disabled", self.procedencia)

    def test_04_ficha_bloquea_detalle_y_edita_en_revision(self):
        self.assertIn("registroFichaOriginal", self.procedencia)
        self.assertIn('control.dataset.importedLocked = "true"', self.procedencia)
        self.assertIn("window.establecerEdicionPreviewFicha", self.procedencia)
        self.assertIn("control.disabled = !habilitada", self.procedencia)

    def test_05_marca_visual_no_editable_es_transversal(self):
        self.assertIn("box-shadow: inset 3px 0 0 var(--app-primary) !important", self.design)
        self.assertIn('html[data-app-theme="contrast"]', self.design)
        self.assertIn("field-imported-readonly", self.design)

    def test_06_iconos_recuperan_lapiz_y_exclusion_semantica(self):
        self.assertGreaterEqual(self.css.count('content: "✎"'), 2)
        self.assertIn('content: "⊘"', self.css)
        self.assertIn('content: "✓"', self.css)
        self.assertIn('content: "!"', self.css)
        self.assertNotIn('content: "+"', self.css)
        self.assertNotIn('content: "×"', self.css)

    def test_07_importar_historial_no_responde_disponibilidad(self):
        self.assertIn('simulacion.modo_historial = ""', self.importacion)
        self.assertIn("simulacion.modo_historial_confirmado_usuario = false", self.importacion)
        self.assertIn("simulacion.modo_historial_confirmado_usuario === true", self.historial)
        self.assertIn("simulacion.modo_historial_confirmado_usuario = true", self.historial)
        self.assertIn("modo_historial_confirmado_usuario: false", self.simulacion)

    def test_08_bases_automaticas_explican_su_condicion(self):
        self.assertIn("Las bases automáticas se habilitan después de analizar y validar", self.detalle)
        self.assertIn("resumen?.salario_ultimo_mes_completo", self.detalle)
        self.assertIn("promedio_ultimos_3_meses_completos", self.detalle)

    def test_09_documentacion_registra_r11_y_adr171(self):
        decisiones = leer("docs/DECISIONES.md")
        especificacion = leer("docs/ESPECIFICACION_FUNCIONAL.md")
        matriz = leer("docs/MATRIZ_TRAZABILIDAD.md")
        changelog = leer("CHANGELOG.md")
        self.assertIn("## ADR-171 —", decisiones)
        for rf in range(351, 358):
            self.assertIn(f"**RF-{rf}.**", especificacion)
        self.assertIn("| TR-019 |", matriz)
        self.assertIn("### UX.4.6f R1.1", changelog)


if __name__ == "__main__":
    unittest.main()
