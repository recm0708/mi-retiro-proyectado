"""Regresiones de UX.4.6c: Paso 2, cuotas importadas y apariencia."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIMULACION = ROOT / "app/templates/simulacion.html"
BASE = ROOT / "app/templates/base.html"
SIMULACION_JS = ROOT / "app/static/js/simulacion.js"
IMPORTACION_JS = ROOT / "app/static/js/importacion_datos_oficiales.js"
NAVEGACION_JS = ROOT / "app/static/js/navegacion_wizard.js"
DESIGN = ROOT / "app/static/css/design-system.css"


class TestUX46CCuotas(unittest.TestCase):
    """Protege las decisiones transversales introducidas en UX.4.6c."""

    def test_paso2_separa_acreditadas_de_cotizacion_futura(self):
        html = SIMULACION.read_text(encoding="utf-8")
        self.assertIn("Cuotas acreditadas y cotización futura", html)
        self.assertIn('id="cuotas-acreditadas-titulo"', html)
        self.assertIn('id="cotizacion-futura-titulo"', html)
        self.assertNotIn("Las cuotas futuras son una proyección.", html)

    def test_paso2_marca_campos_obligatorios(self):
        html = SIMULACION.read_text(encoding="utf-8")
        for control in (
            "cuotas_totales",
            "cuotas_anio_actual",
            "continua_cotizando",
            "cuotas_esperadas_cierre_anio",
            "cuotas_esperadas_por_anio",
        ):
            self.assertIn(f'id="{control}"', html)
        self.assertGreaterEqual(html.count("required-marker"), 6)
        self.assertIn("Campo obligatorio", html)
        self.assertNotIn("Campo obligatorio cuando corresponda", html)

    def test_campos_importados_tienen_estado_de_origen(self):
        html = SIMULACION.read_text(encoding="utf-8")
        js = SIMULACION_JS.read_text(encoding="utf-8")
        self.assertIn('id="origen-cuotas-totales"', html)
        self.assertIn('id="origen-cuotas-anio-actual"', html)
        self.assertIn("actualizarOrigenCamposCuotas", js)
        self.assertIn("Dato completado desde la importación.", js)

    def test_campos_no_detectados_permanecen_editables(self):
        js = SIMULACION_JS.read_text(encoding="utf-8")
        self.assertIn('control.readOnly = importado;', js)
        self.assertIn(
            "Este dato no estaba disponible en el comprobante. Complétalo manualmente.",
            js,
        )
        self.assertNotIn('control.disabled = importado;', js)

    def test_origen_de_cuotas_se_registra_por_campo(self):
        js = IMPORTACION_JS.read_text(encoding="utf-8")
        self.assertIn("origen_campos_cuotas", js)
        self.assertIn("cuotas_totales = origenImportado", js)
        self.assertIn("cuotas_anio_actual = origenImportado", js)
        self.assertIn("delete simulacion.origen_campos_cuotas.cuotas_totales", js)
        self.assertIn("delete simulacion.origen_campos_cuotas.cuotas_anio_actual", js)

    def test_quitar_importacion_libera_origenes(self):
        js = IMPORTACION_JS.read_text(encoding="utf-8")
        self.assertIn("simulacion.origen_campos_cuotas = {};", js)
        self.assertIn("restaurarDatosCuotas(simulacion);", js)

    def test_revision_de_pdf_es_unica_via_para_corregir_importados(self):
        html = SIMULACION.read_text(encoding="utf-8")
        js = SIMULACION_JS.read_text(encoding="utf-8")
        self.assertIn('id="btn-revisar-cuotas-importadas"', html)
        self.assertIn("Revisar importación", html)
        self.assertIn("revisarComprobanteImportado", js)

    def test_no_hay_acciones_duplicadas_dentro_del_paso2(self):
        html = SIMULACION.read_text(encoding="utf-8")
        paso2 = html.split("PASO 2 — CUOTAS", 1)[1].split(
            "PASO 3 — HISTORIAL Y SALARIO ACTUAL", 1
        )[0]
        self.assertNotIn('id="btn-volver-paso-1"', paso2)
        self.assertNotIn('id="btn-continuar-paso-3"', paso2)
        self.assertNotIn("wizard-actions", paso2)

    def test_navegacion_comun_continua_al_historial_sin_boton_duplicado(self):
        js = NAVEGACION_JS.read_text(encoding="utf-8")
        simulacion_js = SIMULACION_JS.read_text(encoding="utf-8")
        self.assertIn("continuarDesdePasoCuotas", js)
        self.assertIn("function continuarDesdePasoCuotas()", simulacion_js)
        self.assertNotIn('"btn-continuar-paso-3"', js)

    def test_no_continuar_desactiva_proyeccion_y_obligatoriedad(self):
        js = SIMULACION_JS.read_text(encoding="utf-8")
        self.assertIn("cierre.required = false;", js)
        self.assertIn("futuras.required = false;", js)
        self.assertIn("cierre.required = true;", js)
        self.assertIn("futuras.required = true;", js)
        self.assertIn("cuotas-sin-continuidad", js)

    def test_resultado_usa_lenguaje_orientado_al_usuario(self):
        html = SIMULACION.read_text(encoding="utf-8")
        self.assertIn("Situación de tus cuotas", html)
        self.assertIn("Ya acreditadas por la CSS", html)
        self.assertIn("Estimación al cierre del año", html)
        self.assertNotIn("Históricas reales", html)
        self.assertNotIn("Resumen preliminar", html)

    def test_selector_de_apariencia_usa_iconos_svg_semanticos(self):
        base = BASE.read_text(encoding="utf-8")
        css = DESIGN.read_text(encoding="utf-8")
        self.assertIn('class="theme-trigger-icon"', base)
        for tema in ("system", "light", "dark", "contrast"):
            self.assertIn(f'data-theme-icon="{tema}"', base)
        self.assertIn(".theme-choice-icon", css)
        self.assertNotIn('class="theme-trigger-symbol"', base)

    def test_revision_importada_mueve_modal_fuera_del_panel_oculto(self):
        js = IMPORTACION_JS.read_text(encoding="utf-8")
        self.assertIn("document.body.appendChild(elemento);", js)
        self.assertIn("elemento.parentElement !== document.body", js)

    def test_campos_editables_usan_pistas_que_desaparecen_con_el_valor(self):
        html = SIMULACION.read_text(encoding="utf-8")
        accesibilidad = (ROOT / "app/static/js/accesibilidad.js").read_text(encoding="utf-8")
        self.assertIn('placeholder="Ej.: 281"', html)
        self.assertIn('placeholder="Ej.: 5"', html)
        self.assertIn('placeholder="Ej.: 12"', html)
        self.assertIn("PISTAS_CAMPOS", accesibilidad)
        self.assertIn("prepararPistasCampos", accesibilidad)
        self.assertNotIn("Usa 12 si esperas cotizar todos los meses del año.", html)

    def test_ayuda_contextual_es_solo_icono_sin_palabra_info(self):
        accesibilidad = (ROOT / "app/static/js/accesibilidad.js").read_text(encoding="utf-8")
        self.assertIn('class="context-help-icon"', accesibilidad)
        self.assertNotIn('<span aria-hidden="true">Info</span>', accesibilidad)
        self.assertIn("Más información sobre", accesibilidad)

    def test_css_diferencia_importado_y_faltante(self):
        css = DESIGN.read_text(encoding="utf-8")
        self.assertIn(".field-origin-note.imported", css)
        self.assertIn(".field-origin-note.missing", css)
        self.assertIn("#form-cuotas input[readonly]", css)
        self.assertIn(".imported-data-actions", css)

    def test_revision_importada_filtra_secciones_por_paso(self):
        parcial = (
            ROOT / "app/templates/partials/importacion_datos_oficiales.html"
        ).read_text(encoding="utf-8")
        js = IMPORTACION_JS.read_text(encoding="utf-8")
        simulacion_js = SIMULACION_JS.read_text(encoding="utf-8")

        self.assertIn('data-preview-step="1"', parcial)
        self.assertIn('data-preview-step="2"', parcial)
        self.assertIn('data-preview-step="3"', parcial)
        self.assertIn('data-preview-step="5,6"', parcial)
        self.assertIn("configurarVistaPreviewComprobante", js)
        self.assertIn("pasos.includes(pasoVistaPreviewComprobante)", js)
        self.assertIn("revisarComprobanteImportado(2);", simulacion_js)

    def test_vista_previa_nombra_grupos_por_etapa(self):
        parcial = (
            ROOT / "app/templates/partials/importacion_datos_oficiales.html"
        ).read_text(encoding="utf-8")

        self.assertIn("Datos personales", parcial)
        self.assertIn("(Paso 1)", parcial)
        self.assertIn("Información previsional básica", parcial)
        self.assertIn("Cuotas acreditadas", parcial)
        self.assertIn("(Paso 2)", parcial)
        self.assertIn("Historial anual detectado", parcial)
        self.assertIn("(Paso 3)", parcial)
        self.assertIn("Referencia de retiro y prestación", parcial)
        self.assertIn("(Pasos 5 y 6)", parcial)
        self.assertNotIn("Datos para pasos posteriores", parcial)

    def test_paso2_revisa_total_y_cuotas_del_anio_actual(self):
        parcial = (
            ROOT / "app/templates/partials/importacion_datos_oficiales.html"
        ).read_text(encoding="utf-8")
        js = IMPORTACION_JS.read_text(encoding="utf-8")

        self.assertIn('id="preview-comprobante-cuotas"', parcial)
        self.assertIn('id="preview-comprobante-cuotas-anio-actual"', parcial)
        self.assertIn("obtenerCuotasAnioActualReferencia", js)
        self.assertIn("cuotas_anio_actual: leerNumeroOpcionalPreview", js)

    def test_ayuda_contextual_no_dibuja_doble_circulo(self):
        css = (ROOT / "app/static/css/accesibilidad.css").read_text(encoding="utf-8")
        bloque = css.split(".context-help-trigger {", 1)[1].split("}", 1)[0]
        self.assertIn("border: 0;", bloque)
        self.assertIn(".context-help-icon", css)
        self.assertIn("border-radius: 50%;", css)


if __name__ == "__main__":
    unittest.main()
