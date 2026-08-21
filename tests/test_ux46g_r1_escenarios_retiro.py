"""Regresiones UX.4.6g R1 para escenarios de retiro contextuales."""

from datetime import date
from pathlib import Path
import unittest

from app.modelos.simulacion import DatosRetiro
from app.servicios.retiro import analizar_retiro

ROOT = Path(__file__).resolve().parents[1]


class UX46GR1EscenariosRetiroTests(unittest.TestCase):
    """Protege selección, banda anticipada, documentación y presentación."""

    def _datos(self, **cambios):
        base = dict(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            fecha_corte=date(2026, 8, 20),
            ultimo_mes_cuotas="2026-06",
            cuotas_reales=282,
            cuotas_anio_actual=6,
            cuotas_esperadas_cierre_anio=12,
            continua_cotizando=True,
            cuotas_esperadas_por_anio=12,
            anio_fin_proyeccion_salarial=2031,
            anios_adicionales=[0],
        )
        base.update(cambios)
        return DatosRetiro(**base)

    def test_modelo_por_defecto_solo_incluye_referencia(self):
        datos = self._datos()
        datos = DatosRetiro(**{
            key: value
            for key, value in datos.model_dump().items()
            if key not in {
                "anios_adicionales",
                "incluir_fecha_evaluacion_como_retiro",
            }
        })
        self.assertEqual(datos.anios_adicionales, [0])
        self.assertFalse(datos.incluir_fecha_evaluacion_como_retiro)

    def test_menos_uno_y_menos_dos_siguen_disponibles_si_se_solicitan(self):
        resumen = analizar_retiro(self._datos(
            fecha_corte=date(2024, 8, 20),
            ultimo_mes_cuotas="2024-06",
            anios_adicionales=[-2, -1, 0],
        ))
        self.assertEqual(
            [e.tipo for e in resumen.escenarios],
            ["ANTICIPADO", "ANTICIPADO", "REFERENCIA"],
        )

    def test_mas_cuatro_anos_es_un_escenario_valido(self):
        resumen = analizar_retiro(self._datos(anios_adicionales=[0, 4]))
        self.assertTrue(
            any(
                e.nombre == "Edad de referencia + 4 años"
                for e in resumen.escenarios
            )
        )

    def test_fecha_evaluacion_dentro_banda_crea_escenario_explicito(self):
        resumen = analizar_retiro(self._datos(
            incluir_fecha_evaluacion_como_retiro=True,
        ))
        escenario = next(
            e for e in resumen.escenarios
            if e.tipo == "EVALUACION"
        )
        self.assertEqual(escenario.fecha_retiro, date(2026, 8, 20))
        self.assertEqual(
            escenario.nombre,
            "Retiro en la fecha de evaluación",
        )
        self.assertFalse(escenario.fecha_ya_transcurrida)

    def test_fecha_evaluacion_fuera_banda_se_rechaza(self):
        with self.assertRaisesRegex(ValueError, "banda previa"):
            analizar_retiro(self._datos(
                fecha_corte=date(2023, 8, 20),
                ultimo_mes_cuotas="2023-06",
                incluir_fecha_evaluacion_como_retiro=True,
            ))

    def test_template_no_precarga_anticipados_ni_posteriores(self):
        html = (
            ROOT / "app/templates/partials/retiro.html"
        ).read_text(encoding="utf-8")
        for identificador in (
            "retiro-anticipado-2",
            "retiro-anticipado-1",
            "retiro-adicional-1",
            "retiro-adicional-2",
            "retiro-adicional-3",
            "retiro-adicional-4",
            "retiro-adicional-5",
        ):
            fragmento = html.split(
                f'id="{identificador}"', 1
            )[1].split(">", 1)[0]
            self.assertNotIn("checked", fragmento)

    def test_template_conserva_referencia_fija_y_agrega_mas_cuatro(self):
        html = (
            ROOT / "app/templates/partials/retiro.html"
        ).read_text(encoding="utf-8")
        self.assertIn('id="retiro-referencia"', html)
        ref = html.split(
            'id="retiro-referencia"', 1
        )[1].split(">", 1)[0]
        self.assertIn("checked", ref)
        self.assertIn("disabled", ref)
        self.assertIn('id="retiro-adicional-4"', html)

    def test_template_incluye_fecha_evaluacion_anticipada_opcional(self):
        html = (
            ROOT / "app/templates/partials/retiro.html"
        ).read_text(encoding="utf-8")
        self.assertIn('id="retiro-fecha-evaluacion"', html)
        self.assertIn("Retirarme en la fecha de evaluación", html)
        self.assertIn("puede aplicar una reducción", html)

    def test_js_distingue_sugerencia_y_edicion_usuario(self):
        js = (
            ROOT / "app/static/js/retiro.js"
        ).read_text(encoding="utf-8")
        self.assertIn('"SUGERIDO_PASO4"', js)
        self.assertIn('"EDITADO_USUARIO"', js)
        self.assertIn("preferencias_retiro", js)
        self.assertIn("obtenerAnioFinProyeccionRetiro", js)

    def test_js_bloquea_fechas_transcurridas_y_no_autoelige_anticipados(self):
        js = (
            ROOT / "app/static/js/retiro.js"
        ).read_text(encoding="utf-8")
        self.assertIn("elemento.disabled = transcurrida", js)
        self.assertIn(
            ".retiro-adicional:not(.retiro-anticipado)",
            js,
        )
        self.assertIn("Fecha ya transcurrida", js)

    def test_template_recupera_cuadricula_compacta_y_tabla_comun(self):
        html = (
            ROOT / "app/templates/partials/retiro.html"
        ).read_text(encoding="utf-8")
        self.assertEqual(html.count('class="retirement-option-grid"'), 1)
        self.assertNotIn("retirement-scenario-section", html)
        self.assertNotIn('id="retiro-sugerencia-proyeccion"', html)
        self.assertIn("retirement-table-wrapper", html)
        self.assertIn("table-scroll-compact", html)
        self.assertIn("app-table-shell", html)

        boton = html.split(
            'id="btn-ajustar-proyeccion-retiro"', 1
        )[1].split(">", 1)[0]
        self.assertIn("btn-primary", boton)
        self.assertNotIn("btn-outline-dark", boton)

    def test_css_distingue_seleccion_y_no_disponible(self):
        css = (
            ROOT / "app/static/css/style.css"
        ).read_text(encoding="utf-8")
        self.assertIn(".retirement-option-selected", css)
        self.assertIn(".retirement-option-unavailable", css)

    def test_documentacion_traza_r1(self):
        decisiones = (
            ROOT / "docs/DECISIONES.md"
        ).read_text(encoding="utf-8")
        especificacion = (
            ROOT / "docs/ESPECIFICACION_FUNCIONAL.md"
        ).read_text(encoding="utf-8")
        matriz = (
            ROOT / "docs/MATRIZ_TRAZABILIDAD.md"
        ).read_text(encoding="utf-8")
        self.assertIn("ADR-174", decisiones)
        self.assertIn("ADR-175", decisiones)
        self.assertIn("RF-366", especificacion)
        self.assertIn("RF-374", especificacion)
        self.assertIn("TR-022", matriz)
        self.assertIn("TR-023", matriz)

    def test_js_reconoce_sexo_abreviado_para_referencia_contextual(self):
        js = (ROOT / "app/static/js/retiro.js").read_text(encoding="utf-8")
        self.assertIn('["F", "FEMENINO", "MUJER"]', js)
        self.assertIn('["M", "MASCULINO", "HOMBRE"]', js)
        self.assertIn("opcion-retiro-fecha-evaluacion", js)

    def test_fecha_personalizada_explica_cobertura_del_paso4(self):
        html = (ROOT / "app/templates/partials/retiro.html").read_text(encoding="utf-8")
        js = (ROOT / "app/static/js/retiro.js").read_text(encoding="utf-8")
        self.assertIn('id="estado-cobertura-fecha-personalizada"', html)
        self.assertIn("Esta fecha está cubierta por tu proyección salarial vigente", js)
        self.assertIn("Esta fecha supera tu proyección salarial actual", js)

    def test_fechas_usan_contrato_transversal_estricto(self):
        js = (ROOT / "app/static/js/accesibilidad.js").read_text(encoding="utf-8")
        self.assertIn('FECHA_MINIMA_GLOBAL = "1900-01-01"', js)
        self.assertIn('FECHA_MAXIMA_GLOBAL = "2200-12-31"', js)
        self.assertIn("validarCampoFechaEstricto", js)
        self.assertIn("coincidencia[1].length !== 4", js)
        self.assertIn("fecha.getUTCFullYear() === anio", js)
        self.assertIn("prepararCamposFecha();", js)

    def test_observador_accesibilidad_no_observa_sus_propias_mutaciones(self):
        js = (ROOT / "app/static/js/accesibilidad.js").read_text(encoding="utf-8")
        self.assertIn('if (!control.classList.contains("app-date-input"))', js)
        self.assertIn("observador.disconnect();", js)
        self.assertIn("observador.observe(document.body, opcionesObservacion);", js)

    def test_fechas_tienen_ancho_compacto_y_responsive(self):
        css = (ROOT / "app/static/css/accesibilidad.css").read_text(encoding="utf-8")
        self.assertIn(".app-date-input.form-control", css)
        self.assertIn("max-width: 20rem", css)
        self.assertIn("max-width: 575.98px", css)
        self.assertIn("max-width: 100%", css)

    def test_documentacion_incorpora_contrato_fecha_r14(self):
        decisiones = (ROOT / "docs/DECISIONES.md").read_text(encoding="utf-8")
        especificacion = (ROOT / "docs/ESPECIFICACION_FUNCIONAL.md").read_text(encoding="utf-8")
        matriz = (ROOT / "docs/MATRIZ_TRAZABILIDAD.md").read_text(encoding="utf-8")
        validacion = (ROOT / "docs/VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("ADR-176", decisiones)
        self.assertIn("RF-375", especificacion)
        self.assertIn("RF-379", especificacion)
        self.assertIn("TR-024", matriz)
        self.assertIn("780 pruebas", validacion)


    def test_r143_alinea_periodo_historial_con_control_anio(self):
        html = (ROOT / "app/templates/partials/historial_salarial.html").read_text(encoding="utf-8")
        css = (ROOT / "app/static/css/design-system.css").read_text(encoding="utf-8")
        self.assertIn('class="row g-4 history-period-row"', html)
        self.assertIn("history-period-summary-column", html)
        self.assertIn(".history-period-summary-column", css)
        self.assertIn("padding-top: 2.3rem", css)

    def test_r143_alinea_campos_del_periodo_de_proyeccion(self):
        html = (ROOT / "app/templates/simulacion.html").read_text(encoding="utf-8")
        css = (ROOT / "app/static/css/design-system.css").read_text(encoding="utf-8")
        self.assertGreaterEqual(html.count("projection-period-label"), 2)
        self.assertIn(".projection-period-label", css)
        self.assertIn("min-height: 1.8rem", css)

    def test_r143_resumen_retiro_reserva_ancho_para_cierre_esperado(self):
        html = (ROOT / "app/templates/partials/retiro.html").read_text(encoding="utf-8")
        bloque_sexo = html.split("Sexo", 1)[0].rsplit('<div class="', 1)[1].split('"', 1)[0]
        bloque_cierre = html.split("Cierre esperado este año", 1)[0].rsplit('<div class="', 1)[1].split('"', 1)[0]
        self.assertIn("col-xl-1", bloque_sexo)
        self.assertIn("col-xl-3", bloque_cierre)


if __name__ == "__main__":
    unittest.main()
