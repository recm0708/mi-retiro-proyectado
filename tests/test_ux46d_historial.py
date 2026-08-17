"""Regresiones de UX.4.6d para el Paso 3: historial y base salarial."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestUX46DHistorial(unittest.TestCase):
    """Protege el rediseño integral y los contratos transversales del Paso 3."""

    @classmethod
    def setUpClass(cls):
        cls.simulacion = (ROOT / "app/templates/simulacion.html").read_text(encoding="utf-8")
        cls.historial = (
            ROOT / "app/templates/partials/historial_salarial.html"
        ).read_text(encoding="utf-8")
        cls.ficha = (
            ROOT / "app/templates/partials/importacion_ficha_digital.html"
        ).read_text(encoding="utf-8")
        cls.detalle = (
            ROOT / "app/templates/partials/detalle_anio_actual.html"
        ).read_text(encoding="utf-8")
        cls.retiro = (
            ROOT / "app/templates/partials/retiro.html"
        ).read_text(encoding="utf-8")
        cls.historial_js = (
            ROOT / "app/static/js/historial_salarios.js"
        ).read_text(encoding="utf-8")
        cls.detalle_js = (
            ROOT / "app/static/js/detalle_anio_actual.js"
        ).read_text(encoding="utf-8")
        cls.importacion_js = (
            ROOT / "app/static/js/importacion_datos_oficiales.js"
        ).read_text(encoding="utf-8")
        cls.simulacion_js = (
            ROOT / "app/static/js/simulacion.js"
        ).read_text(encoding="utf-8")
        cls.navegacion_js = (
            ROOT / "app/static/js/navegacion_wizard.js"
        ).read_text(encoding="utf-8")
        cls.css = (
            ROOT / "app/static/css/design-system.css"
        ).read_text(encoding="utf-8")

    def test_paso3_usa_titulo_y_tres_secciones_conceptuales(self):
        self.assertIn("Historial salarial y base para proyección", self.simulacion)
        self.assertIn("Historial salarial anual", self.historial)
        self.assertIn("Detalle salarial del año actual", self.detalle)
        self.assertIn("Base salarial para proyección", self.simulacion)
        self.assertNotIn("Historial salarial y salario actual", self.simulacion)

    def test_paso3_no_repite_numero_de_paso_dentro_de_tarjeta(self):
        paso3 = self.simulacion.split("PASO 3 — HISTORIAL Y BASE SALARIAL", 1)[1].split(
            "PASO 4 — PROYECCIÓN", 1
        )[0]
        self.assertNotIn("Paso 3 de 6\n", paso3)

    def test_no_hay_acciones_principales_duplicadas_en_paso3(self):
        conjunto = self.historial + self.detalle + self.simulacion
        self.assertNotIn('id="btn-analizar-historial"', conjunto)
        self.assertNotIn('id="btn-validar-detalle-anio-actual"', conjunto)
        self.assertNotIn('id="btn-volver-paso-2"', conjunto)
        self.assertNotIn('id="btn-continuar-paso-4"', conjunto)

    def test_navegacion_comun_controla_analisis_y_continuacion_de_paso3(self):
        self.assertIn("function analizarPasoHistorialCompleto()", self.simulacion_js)
        self.assertIn("function continuarDesdePasoHistorial()", self.simulacion_js)
        self.assertIn("paso3EstaCompleto", self.navegacion_js)
        self.assertIn("Analizar historial", self.navegacion_js)
        self.assertIn("Continuar a proyección", self.navegacion_js)

    def test_accion_unificada_valida_detalle_historial_y_salario(self):
        cuerpo = self.simulacion_js.split("async function analizarPasoHistorialCompleto()", 1)[1].split(
            "function continuarDesdePasoHistorial()", 1
        )[0]
        self.assertIn("await validarDetalleAnioActual()", cuerpo)
        self.assertIn("await analizarHistorialSalarial()", cuerpo)
        self.assertIn("await analizarSalario()", cuerpo)
        self.assertIn('enfocarSeccionPaso3("seccion-historial-salarial")', cuerpo)

    def test_historial_no_ofrece_importador_futuro_ni_relleno_masivo(self):
        self.assertNotIn("Importar desde Mi Caja Digital — próximamente", self.historial)
        self.assertNotIn("Completar cuotas vacías con 12", self.historial)
        self.assertNotIn("btn-completar-cuotas", self.historial)
        self.assertNotIn("completarCuotasVacias", self.historial_js)

    def test_periodo_simplifica_anio_final_y_regenera_automaticamente(self):
        self.assertIn('id="historial-periodo-visible"', self.historial)
        self.assertIn('type="hidden" id="historial_anio_fin"', self.historial)
        self.assertNotIn("Generar / actualizar años", self.historial)
        self.assertNotIn("btn-generar-historial", self.historial_js)
        self.assertIn("generarTablaHistorial();", self.historial_js)
        self.assertIn("actualizarPeriodoHistorialVisible", self.historial_js)

    def test_tabla_historial_usa_filtros_y_estado_pendiente(self):
        self.assertIn('data-history-filter="TODOS"', self.historial)
        self.assertIn('data-history-filter="PENDIENTES"', self.historial)
        self.assertIn("Salario anual reportado", self.historial)
        self.assertIn('inputCuotas.placeholder = "0–12"', self.historial_js)
        self.assertIn('inputSalario.placeholder = "Ej.: 12,000.00"', self.historial_js)
        self.assertIn('etiqueta: "Pendiente"', self.historial_js)
        self.assertIn('etiqueta: "Falta salario"', self.historial_js)
        self.assertIn('etiqueta: "Parcial"', self.historial_js)
        self.assertIn('etiqueta: "Completo"', self.historial_js)

    def test_datos_importados_del_historial_se_bloquean_por_campo(self):
        self.assertIn("origen_campos_historial", self.importacion_js)
        self.assertIn("aplicarOrigenCampoHistorial", self.historial_js)
        self.assertIn("control.readOnly = true", self.historial_js)
        self.assertIn('control.classList.add("history-field-imported")', self.historial_js)
        self.assertIn("Revisar importación", self.historial)

    def test_revision_del_comprobante_desde_paso3_es_contextual(self):
        self.assertIn("revisarComprobanteImportado(3)", self.historial_js)
        preview = (ROOT / "app/templates/partials/importacion_datos_oficiales.html").read_text(encoding="utf-8")
        self.assertIn("Historial anual detectado", preview)
        self.assertIn("(Paso 3)", preview)
        self.assertIn('data-preview-step="3"', preview)

    def test_ficha_digital_adopta_cargador_estandar(self):
        self.assertIn("1. Selecciona el documento", self.ficha)
        self.assertIn("2. Analiza el documento", self.ficha)
        self.assertIn('id="btn-analizar-ficha-digital-importacion"', self.ficha)
        self.assertIn("disabled", self.ficha)
        self.assertIn("Analizar documento", self.ficha)
        self.assertIn("official-import-upload-grid", self.ficha)

    def test_ficha_digital_no_muestra_texto_tecnico_de_memoria(self):
        self.assertNotIn("se procesa en memoria", self.ficha.lower())
        self.assertNotIn("no se guarda", self.ficha.lower())
        self.assertIn("Consulta cómo protegemos y utilizamos tus datos", self.detalle)

    def test_ficha_digital_usa_revision_edicion_e_importacion(self):
        self.assertIn("Modo revisión", self.ficha)
        self.assertIn("Editar campos", self.ficha)
        self.assertIn("Importar datos", self.ficha)
        self.assertIn("establecerEdicionPreviewFicha(false)", self.importacion_js)
        self.assertIn("importar.disabled = habilitada", self.importacion_js)
        self.assertIn("Finalizar edición", self.importacion_js)

    def test_ficha_digital_registra_origen_y_bloquea_solo_lo_importado(self):
        self.assertIn("origen_campos_detalle_anio_actual", self.importacion_js)
        self.assertIn("marcarCampoDetalleImportado", self.detalle_js)
        self.assertIn('control.classList.add("detail-field-imported")', self.detalle_js)
        self.assertIn("const origenDirecto = origenCampoDetalle", self.detalle_js)
        self.assertIn("if (!origenDirecto && !cuotaDeMesImportado) return", self.detalle_js)

    def test_detalle_actual_no_repite_enlace_ni_referencia_al_paso1(self):
        self.assertNotIn("Abrir Mi Caja Digital", self.detalle)
        self.assertNotIn("desde el Paso 1", self.detalle)
        self.assertIn("Abrir Mi Caja Digital", self.ficha)

    def test_base_automatica_es_solo_lectura_y_manual_es_obligatoria(self):
        self.assertIn("monto.readOnly = false", self.detalle_js)
        self.assertIn("periodicidad.disabled = false", self.detalle_js)
        self.assertIn("monto.required = true", self.detalle_js)
        self.assertIn("periodicidad.required = true", self.detalle_js)
        self.assertIn("monto.readOnly = true", self.detalle_js)
        self.assertIn("periodicidad.disabled = true", self.detalle_js)
        self.assertIn("Base calculada automáticamente", self.detalle_js)

    def test_base_salarial_no_expone_explicacion_interna_de_origen(self):
        self.assertNotIn("La aplicación conservará el origen de la base utilizada", self.simulacion)
        self.assertIn('id="origen-salario-proyeccion-ayuda"', self.simulacion)

    def test_paso3_finaliza_con_un_resumen_unificado(self):
        for identificador in (
            "paso3-cuotas-referencia",
            "paso3-cuotas-identificadas",
            "paso3-diferencia-cuotas",
            "paso3-total-salarios",
            "paso3-base-mensual",
        ):
            self.assertIn(f'id="{identificador}"', self.simulacion)
        self.assertIn("function actualizarResumenPaso3()", self.simulacion_js)

    def test_no_existen_paneles_proximo_paso_en_plantillas_publicas(self):
        textos = "\n".join(
            archivo.read_text(encoding="utf-8")
            for archivo in (ROOT / "app/templates").rglob("*.html")
        )
        self.assertNotIn("Próximo paso:", textos)


    def test_revision2_alinea_selectores_del_detalle_desde_arriba(self):
        self.assertIn('class="row g-4 align-items-start mb-4"', self.detalle)
        self.assertIn('id="detalle-importado-inactivo"', self.detalle)

    def test_revision2_ficha_no_redefine_cuotas_del_paso2(self):
        bloque = self.importacion_js.split("async function confirmarFichaDigitalImportacion()", 1)[1].split(
            "function revisarFichaDigitalImportada()", 1
        )[0]
        self.assertIn("cuotasReferenciaPaso2", bloque)
        self.assertIn("cuotas_anio_actual_referencia: cuotasReferenciaPaso2", bloque)
        self.assertNotIn("cuotas_anio_actual: cuotasConfirmadas", bloque)
        self.assertNotIn("delete simulacion.origen_campos_cuotas.cuotas_anio_actual", bloque)

    def test_revision3_ficha_marca_y_bloquea_cuotas_de_registros_importados(self):
        self.assertIn("registroImportadoAutomaticamente", self.importacion_js)
        self.assertIn("cuota.checked = registroImportadoAutomaticamente", self.importacion_js)
        self.assertIn('cuota.dataset.importedLocked = "true"', self.importacion_js)
        self.assertIn('control.dataset.importedLocked === "true" || !habilitada', self.importacion_js)

    def test_revision3_ficha_no_redefine_total_paso2_pero_compara_coherencia(self):
        self.assertIn("cuotasReferenciaPaso2", self.importacion_js)
        self.assertIn("La Ficha Digital aporta ${cuotasMarcadas} mes(es) con datos confirmados", self.importacion_js)
        self.assertIn('coincidenCuotas ? "success" : "warning"', self.importacion_js)

    def test_revision3_detalle_distingue_filas_importadas_y_manuales(self):
        self.assertIn("filaDetalleTieneDatosImportados", self.detalle_js)
        self.assertIn('fila.classList.add("data-row-imported")', self.detalle_js)
        self.assertIn('fila.classList.add("data-row-manual")', self.detalle_js)
        self.assertIn("data-row-imported", self.css)
        self.assertIn("data-row-manual", self.css)

    def test_revision3_historial_anual_marca_visual_origen_de_fila(self):
        self.assertIn("filaTieneImportacion", self.historial_js)
        self.assertIn('"data-row-imported" : "data-row-manual"', self.historial_js)

    def test_revision3_preview_comprobante_bloquea_clasificacion_automatica(self):
        self.assertIn('aplicar.dataset.importedLocked = "true"', self.importacion_js)
        self.assertIn('aplicar.checked = tipo.value === "HISTORICO"', self.importacion_js)
        self.assertIn('fila.classList.add("data-row-imported")', self.importacion_js)

    def test_revision2_detalle_importado_inactivo_se_explica_sin_ocultar_eleccion_manual(self):
        self.assertIn("detalle-importado-inactivo", self.detalle_js)
        self.assertIn("!importado || habilitado", self.detalle_js)
        self.assertIn("Primera y segunda quincena", self.detalle)
        self.assertIn("Total mensual", self.detalle)

    def test_revision2_anio_actual_no_disfraza_salario_pendiente_como_cero(self):
        self.assertIn("Un cero no confirmado no debe parecer un salario válido", self.historial_js)
        self.assertIn('inputSalario.value = ""', self.historial_js)
        self.assertIn("activa el detalle del año actual", self.historial_js)

    def test_estilos_distinguen_importados_hover_y_resumen(self):
        self.assertIn(".history-field-imported", self.css)
        self.assertIn(".detail-field-imported", self.css)
        self.assertIn(".history-table tbody tr:hover", self.css)
        self.assertIn(".step3-summary", self.css)

    def test_revision4_origen_importado_usa_paleta_primaria_y_no_verde_exito(self):
        bloque = self.css.split("UX.4.6d R4", 1)[1]
        self.assertIn("var(--app-selected-bg)", bloque)
        self.assertIn("var(--app-selected-border)", bloque)
        self.assertNotIn("var(--app-success-bg)", bloque)

    def test_revision4_checkbox_importado_del_detalle_se_fuerza_marcado(self):
        bloque = self.detalle_js.split("function marcarCampoDetalleImportado", 1)[1].split(
            "function filaDetalleTieneDatosImportados", 1
        )[0]
        self.assertIn('control.checked = true', bloque)
        self.assertIn('control.dataset.importedLocked = "true"', bloque)
        self.assertIn('control.disabled = true', bloque)

    def test_revision4_checkbox_bloqueado_conserva_gancho_si_esta_marcado(self):
        self.assertIn('.form-check-input[data-imported-locked="true"]:checked', self.css)
        self.assertIn("stroke='%23fff'", self.css)
        self.assertIn("background-size: 0.9rem 0.9rem", self.css)

    def test_revision4_alto_contraste_conserva_distincion_simetrica(self):
        self.assertIn('html[data-app-theme="contrast"] .table tbody tr.data-row-imported', self.css)
        self.assertIn('background: var(--app-selected-bg);', self.css)
        self.assertIn("stroke='%23000'", self.css)

    def test_revision5_checkbox_detalle_reconoce_mes_importado_aunque_falte_metadata_de_cuota(self):
        bloque = self.detalle_js.split("function marcarCampoDetalleImportado", 1)[1].split(
            "function filaDetalleTieneDatosImportados", 1
        )[0]
        self.assertIn("origenMes.salario_mensual || origenMes.estado || origenDirecto", bloque)
        self.assertIn('control.setAttribute("checked", "checked")', bloque)
        self.assertIn('control.setAttribute("aria-checked", "true")', bloque)

    def test_revision5_lectura_trata_checkbox_importado_como_cuota_seleccionada(self):
        bloque = self.detalle_js.split("function leerDetalleAnioActual()", 1)[1].split(
            "function guardarBorradorDetalleAnioActual", 1
        )[0]
        self.assertIn('campoCuota.dataset.importedLocked === "true"', bloque)
        self.assertIn("|| campoCuota.checked", bloque)

    def test_revision5_preview_ficha_preserva_estado_importado_en_lectura(self):
        bloque = self.importacion_js.split("function leerRegistrosPreviewFicha()", 1)[1].split(
            "async function confirmarFichaDigitalImportacion", 1
        )[0]
        self.assertIn('cuota.dataset.importedLocked === "true" || cuota.checked', bloque)
        self.assertIn('cuota.setAttribute("checked", "checked")', self.importacion_js)

    def test_revision17_css_distingue_bloqueado_de_marcado(self):
        bloque = self.css.split("UX.4.6d R17", 1)[1]
        self.assertIn('.form-check-input[data-imported-locked="true"]:checked', bloque)
        self.assertIn('.form-check-input[data-imported-locked="true"]:not(:checked)', bloque)
        self.assertIn("background-image: none !important", bloque)


if __name__ == "__main__":
    unittest.main()
