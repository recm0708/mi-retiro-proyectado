"""Regresiones R8.1 de procedencia editable y exclusión documental."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "app/templates/base.html"
JS = ROOT / "app/static/js/editable_provenance.js"
CSS = ROOT / "app/static/css/editable-provenance.css"


class TestUx46eR81ProcedenciaEditable(unittest.TestCase):
    """Protege el control del usuario sin perder la referencia documental."""

    @classmethod
    def setUpClass(cls):
        cls.base = BASE.read_text(encoding="utf-8")
        cls.js = JS.read_text(encoding="utf-8")
        cls.css = CSS.read_text(encoding="utf-8")

    def test_base_carga_capa_css_de_procedencia(self):
        self.assertIn("/css/editable-provenance.css", self.base)

    def test_script_se_carga_despues_de_scripts_especificos(self):
        bloque = self.base.index("{% block scripts %}")
        capa = self.base.index("/js/editable_provenance.js")
        self.assertGreater(capa, bloque)
        self.assertIn("subtree: false", self.js)
        self.assertIn("hayFilasNuevas", self.js)

    def test_procedencia_incluye_estado_excluido(self):
        self.assertIn("EXCLUIDO_USUARIO", self.js)
        self.assertIn('"Excluido por ti"', self.js)
        self.assertIn('"excluded"', self.js)

    def test_referencia_original_se_preserva_por_documento(self):
        self.assertIn("referencia_mi_retiro_seguro_original", self.js)
        self.assertIn("ficha_digital_importada_original", self.js)
        self.assertIn("structuredClone", self.js)

    def test_datos_personales_importados_conservan_revision_editable_y_bloqueo_principal(self):
        self.assertIn("window.bloquearFormularioPersonal", self.js)
        self.assertIn("aplicarBloqueoVistaPrincipal", self.js)
        self.assertIn('control.closest(".modal")', self.js)

    def test_estado_personal_reacciona_a_dato_no_detectado_completado(self):
        self.assertIn("MI_RETIRO_SEGURO_COMPLETADO_MANUAL", self.js)
        self.assertIn("actualizarProcedenciaPersonalDesdeControl", self.js)
        self.assertIn("mostrarProcedenciaCampo(control, origen)", self.js)

    def test_cuotas_importadas_se_corrigen_desde_revision(self):
        self.assertIn("window.actualizarOrigenCamposCuotas", self.js)
        self.assertIn("Los valores detectados se consultan en modo de solo lectura", self.js)
        self.assertIn("MI_RETIRO_SEGURO_EDITADO", self.js)

    def test_historial_importado_bloquea_detectados_y_deja_pendientes_editables(self):
        self.assertIn("window.aplicarOrigenCampoHistorial", self.js)
        self.assertIn("detectadoOriginalmente", self.js)
        self.assertIn("Campo no detectado por el documento", self.js)

    def test_detalle_importado_recupera_bloqueo_en_vista_principal(self):
        self.assertIn("window.marcarCampoDetalleImportado", self.js)
        self.assertIn('control.dataset.importedLocked = "true"', self.js)
        self.assertIn('control.classList.remove("detail-field-imported-editable")', self.js)

    def test_excluir_periodo_anula_cuota_y_salario_en_payload(self):
        self.assertIn("periodos_excluidos_importacion_ficha", self.js)
        self.assertIn('estado: "SIN_INFORMACION"', self.js)
        self.assertIn("salario_mensual: null", self.js)
        self.assertIn("cuota_acreditada: false", self.js)

    def test_exclusion_reconcilia_paso2(self):
        self.assertIn("sincronizarCuotasPaso2DesdeDetalle", self.js)
        self.assertIn('fuente: "DETALLE_MANUAL"', self.js)
        self.assertIn("FICHA_DIGITAL_EXCLUIDO", self.js)

    def test_preview_ficha_permite_decidir_sobre_cuota_detectada(self):
        self.assertIn("window.establecerEdicionPreviewFicha", self.js)
        self.assertIn(".preview-ficha-cuota", self.js)
        self.assertIn("control.disabled = !habilitada", self.js)

    def test_aviso_explica_que_el_documento_original_no_cambia(self):
        self.assertIn(
            "El documento original se conserva como referencia",
            self.js,
        )
        self.assertIn("imported-adjustment-warning", self.js)

    def test_css_adapta_exclusion_a_oscuro_y_alto_contraste(self):
        self.assertIn('html[data-bs-theme="dark"]', self.css)
        self.assertIn('html[data-app-theme="contrast"]', self.css)
        self.assertIn(".detail-row-excluded", self.css)

    def test_checkbox_importado_editable_se_limita_a_la_revision(self):
        self.assertIn(
            ".preview-ficha-cuota.form-check-input:checked",
            self.css,
        )
        self.assertNotIn(
            ".detail-field-imported-editable.form-check-input:checked",
            self.css,
        )
        self.assertIn("background-image: url(", self.css)
        self.assertIn("stroke='%23fff'", self.css)
        self.assertIn("cursor: pointer !important", self.css)

    def test_aviso_es_reactivo_y_puede_ocultarse_al_revertir(self):
        self.assertIn("function actualizarAviso(", self.js)
        self.assertIn('aviso.classList.toggle("d-none", !activo)', self.js)
        self.assertIn("function actualizarAvisosAjustes(", self.js)
        self.assertIn("actualizarAvisosAjustes(simulacion)", self.js)

    def test_ficha_reincluida_deja_de_generar_aviso_si_no_hay_ajustes(self):
        self.assertIn(
            "periodos_excluidos_importacion_ficha || []).length > 0",
            self.js,
        )
        self.assertIn("accionesFicha", self.js)
        self.assertIn(
            '"aviso-ajustes-ficha"',
            self.js,
        )

    def test_formulario_personal_sincroniza_copia_de_trabajo_del_comprobante(self):
        self.assertIn(
            "simulacion.referencia_mi_retiro_seguro[definicion.referencia]",
            self.js,
        )
        self.assertIn(
            "referencia_mi_retiro_seguro_original",
            self.js,
        )

    def test_iconografia_de_procedencia_es_uniforme(self):
        for icono in ('content: "✓"', 'content: "✎"', 'content: "⊘"',
                      'content: "!"', 'content: "↳"'):
            with self.subTest(icono=icono):
                self.assertIn(icono, self.css)
        for clase in (".detected::before", ".edited::before", ".manual::before",
                      ".excluded::before", ".missing::before", ".automatic::before"):
            with self.subTest(clase=clase):
                self.assertIn(clase, self.css)
        self.assertIn("border-radius: 0 !important", self.css)
        self.assertNotIn('content: "●"', self.css)

    def test_r8_preserva_0_0_24_como_version_base_historica(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("UX.4.6e R8 — validación funcional hasta Paso 3", texto)
        self.assertIn(
            "`VERSION` permanece en `0.0.24-beta` hasta R9",
            texto,
        )


if __name__ == "__main__":
    unittest.main()
