"""Regresiones UX.4.6d R18: procedencia transversal y persistencia visual de importaciones."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision18ProcedenciaPersistencia(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.simulacion_js = (ROOT / "app/static/js/simulation.js").read_text(encoding="utf-8")
        cls.importacion_js = (ROOT / "app/static/js/official_data_import.js").read_text(encoding="utf-8")
        cls.detalle_js = (ROOT / "app/static/js/current_year_detail.js").read_text(encoding="utf-8")
        cls.historial_js = (ROOT / "app/static/js/salary_history.js").read_text(encoding="utf-8")
        cls.css = (ROOT / "app/static/css/design-system.css").read_text(encoding="utf-8")
        cls.comprobante_html = (
            ROOT / "app/templates/partials/official_data_import.html"
        ).read_text(encoding="utf-8")
        cls.ficha_html = (
            ROOT / "app/templates/partials/ficha_digital_import.html"
        ).read_text(encoding="utf-8")

    def test_contrato_de_procedencia_tiene_cuatro_estados(self):
        for etiqueta in (
            'DETECTADO: "Detectado"',
            'EDITADO_USUARIO: "Editado por ti"',
            'COMPLETADO_MANUAL: "Completado manualmente"',
            'NO_DETECTADO: "No detectado"',
        ):
            self.assertIn(etiqueta, self.simulacion_js)
        self.assertIn("data-provenance-note", self.css)
        self.assertIn("data-provenance-badge", self.css)

    def test_paso1_guarda_procedencia_por_campo_y_no_bloquea_no_detectados(self):
        self.assertIn("origen_campos_persona", self.simulacion_js)
        self.assertIn("simulacion.origen_campos_persona = origenesPersona", self.importacion_js)
        self.assertIn("origenBloqueaCampo(origenes[control.id])", self.importacion_js)
        self.assertIn("MI_RETIRO_SEGURO_NO_DETECTADO", self.simulacion_js)

    def test_edicion_de_preview_no_se_confunde_con_simple_entrada_a_modo_edicion(self):
        self.assertIn("registrarEdicionCampoPreviewFicha", self.importacion_js)
        self.assertIn("camposEditadosPreviewFicha.add(clave)", self.importacion_js)
        self.assertNotIn("if (habilitar) previewFichaFueEditado = true;", self.importacion_js)
        self.assertIn("camposEditadosPreviewComprobante.add(clave)", self.importacion_js)

    def test_ficha_y_detalle_muestran_procedencia_visible(self):
        self.assertIn("<th scope=\"col\">Procedencia</th>", self.ficha_html)
        self.assertIn("Editado por ti", self.importacion_js)
        self.assertIn("actualizarProcedenciaFilaDetalle", self.detalle_js)
        self.assertIn("COMPLETADO_MANUAL", self.detalle_js)
        self.assertIn("NO_DETECTADO", self.detalle_js)

    def test_historial_conserva_procedencia_por_campo(self):
        self.assertIn("codigoProcedenciaDesdeOrigen", self.historial_js)
        self.assertIn('control.dataset.provenance = control.value.trim()', self.historial_js)
        self.assertIn("MI_RETIRO_SEGURO_EDITADO", self.importacion_js)
        self.assertIn("MI_RETIRO_SEGURO_DETECTADO", self.importacion_js)

    def test_nombre_de_documento_confirmado_se_guarda_como_metadata(self):
        self.assertGreaterEqual(self.importacion_js.count("contenido.nombre_archivo_origen = archivo.name"), 2)
        self.assertIn("nombre_archivo_origen: borradorImportacionFichaDigital.nombre_archivo_origen", self.importacion_js)
        self.assertIn('id="documento-comprobante-importado"', self.comprobante_html)
        self.assertIn('id="documento-ficha-importado"', self.ficha_html)

    def test_f5_no_promete_restaurar_el_input_nativo_pero_mantiene_importacion(self):
        self.assertIn("actualizarDocumentoImportadoPersistente", self.importacion_js)
        self.assertIn("El navegador vacía el selector de archivos al recargar por seguridad", self.importacion_js)
        self.assertIn("no necesitas volver a adjuntar el documento", self.importacion_js)
        self.assertIn("Importación vigente:", self.importacion_js)
        self.assertIn("official-import-persisted-document", self.css)


if __name__ == "__main__":
    unittest.main()
