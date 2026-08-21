"""Regresiones de UX.4.6h R1 — resultados y exportación.

Estas pruebas fijan contratos de interfaz del Paso 6 sin duplicar las
fórmulas previsionales de los motores Python.
"""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
LOADER = ROOT / "app" / "templates" / "partials" / "gestion_datos.html"
ORQUESTACION = ROOT / "app" / "static" / "js" / "resultados_orquestacion.js"
ESTILOS = ROOT / "app" / "static" / "css" / "resultados.css"


class TestUX46hR1ResultadosExportacion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loader = LOADER.read_text(encoding="utf-8")
        cls.js = ORQUESTACION.read_text(encoding="utf-8")
        cls.css = ESTILOS.read_text(encoding="utf-8")

    def test_01_loader_carga_orquestacion_del_paso_6(self):
        self.assertIn("/js/resultados_orquestacion.js", self.loader)
        self.assertIn("antes de los scripts", self.loader)
        self.assertIn('pagina_activa == "simulacion"', self.loader)

    def test_02_orquestacion_carga_css_solo_al_existir_paso_6(self):
        self.assertIn("/static/css/resultados.css", self.js)
        self.assertIn("cargarEstilosResultados", self.js)
        self.assertIn('.wizard-panel[data-panel="6"]', self.js)

    def test_03_orquestacion_no_afecta_paginas_sin_paso_6(self):
        self.assertIn('.wizard-panel[data-panel="6"]', self.js)
        self.assertIn("if (!panelResultados)", self.js)

    def test_04_varios_escenarios_exigen_decision_explicita(self):
        self.assertIn('placeholder.textContent = "Seleccione una opción"', self.js)
        self.assertIn("Tienes varios escenarios salariales del Paso 4", self.js)

    def test_05_unico_escenario_puede_autoseleccionarse(self):
        self.assertIn("if (opciones.length === 1)", self.js)
        self.assertIn("Solo existe un escenario salarial disponible", self.js)

    def test_06_se_conservan_elecciones_salariales_previas(self):
        self.assertIn("configuracion_mixto_resultados", self.js)
        self.assertIn("configuracion_sucgs_resultados", self.js)
        self.assertIn("escenario_salarial_seleccionado", self.js)

    def test_07_invalidacion_oculta_resumen_traza_y_exportacion(self):
        for identificador in (
            "resultado-resumen-unificado",
            "resultado-comparacion-origen-datos",
            "resultado-comparacion-referencia",
            "resultado-trazabilidad-calculo",
            "resultado-exportacion",
        ):
            self.assertIn(f'"{identificador}"', self.js)

    def test_08_recalculo_oculta_salidas_especificas_antes_de_responder(self):
        self.assertIn("incluirEspecificos: true", self.js)
        for boton in (
            "btn-calcular-resultado-sebd",
            "btn-calcular-resultado-mixto",
            "btn-calcular-resultado-sucgs",
        ):
            self.assertIn(f'"{boton}"', self.js)

    def test_09_transicion_mixto_sucgs_es_explicita(self):
        self.assertIn("TRANSICION_SUCGS", self.js)
        self.assertIn("Preparar cálculo SUCGS", self.js)
        self.assertIn("resultado-mixto-transicion-sucgs", self.js)

    def test_10_transicion_no_reescribe_el_sistema_personal(self):
        self.assertNotIn('persona.sistema = "SUCGS"', self.js)
        self.assertIn("sin cambiar silenciosamente el sistema", self.js)

    def test_11_sucgs_permita_calculo_desde_transicion_validada(self):
        self.assertIn("persona.sistema !== \"SUCGS\"", self.js)
        self.assertIn("&& !transicionMixto", self.js)
        self.assertIn("construirSolicitudSUCGSConTransicion", self.js)

    def test_12_referencias_sucgs_no_se_presentan_como_vigentes_sin_confirmar(self):
        self.assertIn("Referencia legal del valor mínimo universal", self.js)
        self.assertIn(
            "Referencia legal de Pensión Garantizada Solidaria",
            self.js,
        )
        self.assertIn("referencia legal versionada al 22/05/2025", self.js)

    def test_13_bono_cero_mixto_se_explica_como_neutro(self):
        self.assertIn(
            "B/.0.00 significa que no se incorpora un bono de reconocimiento",
            self.js,
        )

    def test_14_resumen_unificado_usa_lenguaje_para_el_usuario(self):
        self.assertIn("Los pagos mensuales y", self.js)
        self.assertIn("los pagos únicos se muestran por separado", self.js)
        self.assertNotIn("misma semántica para SEBD", self.js)

    def test_15_impresion_nativa_es_copia_no_oficial(self):
        self.assertIn("window.print()", self.js)
        self.assertIn("Preparar informe para imprimir", self.js)
        self.assertIn("No es un documento oficial de la CSS", self.js)

    def test_16_css_impresion_aisla_documento_y_expande_trazabilidad(self):
        self.assertIn("@media print", self.css)
        self.assertIn("body > *:not(#resultado-print-document)", self.css)
        self.assertIn(".print-report-trace .collapse", self.css)
        self.assertIn("display: block !important", self.css)


    def test_17_ayuda_salarial_reutiliza_texto_existente_sin_duplicarlo(self):
        self.assertIn("select.nextElementSibling", self.js)
        self.assertIn('classList.contains("form-text")', self.js)
        self.assertIn("ayudaExistente || document.createElement", self.js)

    def test_18_comparacion_acreditado_proyectado_explica_el_efecto_util(self):
        self.assertIn("Ambas columnas evalúan la misma fecha de retiro", self.js)
        self.assertIn(
            "La diferencia muestra el efecto de incorporar las",
            self.js,
        )
        self.assertNotIn(
            "los saldos y parámetros específicos introducidos en el Paso 6",
            self.js,
        )

    def test_19_referencia_no_comparable_explicita_la_diferencia_de_edad(self):
        self.assertIn("la edad de retiro del comprobante", self.js)
        self.assertIn("es distinta de la edad del escenario actual", self.js)
        self.assertIn("El comprobante se conserva como referencia", self.js)

    def test_20_pension_normal_oculta_factores_que_no_aplican(self):
        self.assertIn('"ANTICIPADA"', self.js)
        self.assertIn('"PROPORCIONAL"', self.js)
        self.assertIn('"PROPORCIONAL_ANTICIPADA"', self.js)
        self.assertIn("modalidadesConFactores.has", self.js)

    def test_21_anio_actual_mixto_se_rotula_historico_mas_proyectado(self):
        self.assertIn('"Histórico + proyectado"', self.js)
        self.assertIn("results-origin-mixed", self.js)
        self.assertIn("table-scroll-compact", self.js)
        self.assertIn(".results-origin-mixed", self.css)

    def test_22_trazabilidad_fecha_legible_y_sin_anterior_local_duplicado(self):
        self.assertIn("Fecha de retiro evaluada", self.js)
        self.assertIn("formatearFechaRetiro", self.js)
        self.assertIn("btn-volver-paso-5", self.js)
        self.assertIn("retirarNavegacionLocalRedundante", self.js)

    def test_23_impresion_construye_documento_independiente_de_la_pantalla(self):
        self.assertIn("resultado-print-document", self.js)
        self.assertIn("construirDocumentoImpresion", self.js)
        self.assertIn("document.body.appendChild(documento)", self.js)
        self.assertIn("body > *:not(#resultado-print-document)", self.css)

    def test_24_informe_impreso_usa_formato_a4_compacto(self):
        self.assertIn("size: A4 portrait", self.css)
        self.assertIn("font-size: 8.7pt", self.css)
        self.assertIn("print-report-meta", self.css)
        self.assertIn("grid-template-columns: repeat(3", self.css)

    def test_25_informe_no_imprime_controles_de_la_interfaz(self):
        self.assertIn("button, select, input, textarea", self.js)
        self.assertIn(".skip-link", self.js)
        self.assertIn("results-calculation-card", self.js)

    def test_26_informe_conserva_resumen_comparaciones_resultado_y_traza(self):
        for identificador in (
            "resultado-resumen-unificado",
            "resultado-comparacion-origen-datos",
            "resultado-comparacion-referencia",
            "resultado-sebd",
            "resultado-mixto",
            "resultado-sucgs",
            "resultado-trazabilidad-calculo",
        ):
            self.assertIn(f'"{identificador}"', self.js)

    def test_27_informe_incluye_identificacion_y_aviso_no_oficial(self):
        self.assertIn("Informe de simulación", self.js)
        self.assertIn("Proyección de jubilación", self.js)
        self.assertIn("Resultado estimado.", self.js)
        self.assertIn("no es una resolución", self.js)

    def test_28_trazabilidad_impresa_inicia_en_pagina_nueva(self):
        self.assertIn(".print-report-trace", self.css)
        self.assertIn("break-before: page", self.css)


if __name__ == "__main__":
    unittest.main()
