"""Regresiones de UX.5 R3 y R4 para modalidades y flujo Manual."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]

SIMULATION = (
    ROOT / "app/templates/simulation.html"
)

CURRENT_YEAR = (
    ROOT
    / "app/templates/partials/current_year_detail.html"
)

SALARY_HISTORY = (
    ROOT
    / "app/templates/partials/salary_history.html"
)

SIMULATION_JS = (
    ROOT / "app/static/js/simulation.js"
)

MODE_JS = (
    ROOT / "app/static/js/simulation_mode.js"
)

NAVIGATION_JS = (
    ROOT / "app/static/js/wizard_navigation.js"
)

RESULTS_JS = (
    ROOT / "app/static/js/results.js"
)

ACCESSIBILITY_JS = (
    ROOT / "app/static/js/accessibility.js"
)

ACCESSIBILITY_CSS = (
    ROOT / "app/static/css/accessibility.css"
)

CURRENT_YEAR_JS = (
    ROOT / "app/static/js/current_year_detail.js"
)

RETIREMENT_JS = (
    ROOT / "app/static/js/retirement.js"
)

RETIREMENT_TEMPLATE = (
    ROOT / "app/templates/partials/retirement.html"
)


class TestUX5R3R4SimulationFlows(
    unittest.TestCase
):
    """Protege entrada por modalidad y flujo Manual."""

    @classmethod
    def setUpClass(cls):
        cls.simulation = SIMULATION.read_text(
            encoding="utf-8"
        )

        cls.current = CURRENT_YEAR.read_text(
            encoding="utf-8"
        )

        cls.history = SALARY_HISTORY.read_text(
            encoding="utf-8"
        )

        cls.simulation_js = SIMULATION_JS.read_text(
            encoding="utf-8"
        )

        cls.mode = MODE_JS.read_text(
            encoding="utf-8"
        )

        cls.navigation = NAVIGATION_JS.read_text(
            encoding="utf-8"
        )

        cls.results = RESULTS_JS.read_text(
            encoding="utf-8"
        )

        cls.accessibility = (
            ACCESSIBILITY_JS.read_text(
                encoding="utf-8"
            )
        )

        cls.accessibility_css = (
            ACCESSIBILITY_CSS.read_text(
                encoding="utf-8"
            )
        )

        cls.current_year_js = (
            CURRENT_YEAR_JS.read_text(
                encoding="utf-8"
            )
        )

        cls.retirement_js = (
            RETIREMENT_JS.read_text(
                encoding="utf-8"
            )
        )

        cls.retirement_template = (
            RETIREMENT_TEMPLATE.read_text(
                encoding="utf-8"
            )
        )

    def test_r3_exige_eleccion_consciente_de_modalidad(self):
        for expected in (
            'id="simulation-mode-gate"',
            'data-simulation-mode-choice="MANUAL"',
            'data-simulation-mode-choice="ASISTIDO"',
            'id="simulation-wizard-shell"',
            "El modo Asistido prepara datos; nunca toma decisiones por ti.",
        ):
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    self.simulation,
                )

    def test_controlador_carga_despues_del_estado_canonico(self):
        simulation_position = (
            self.simulation.index(
                "simulation.js"
            )
        )

        mode_position = (
            self.simulation.index(
                "simulation_mode.js"
            )
        )

        history_position = (
            self.simulation.index(
                "salary_history.js"
            )
        )

        self.assertLess(
            simulation_position,
            mode_position,
        )

        self.assertLess(
            mode_position,
            history_position,
        )

    def test_modalidad_pertenece_al_estado_de_session(self):
        self.assertIn(
            "modo_flujo: null",
            self.simulation_js,
        )

        self.assertIn(
            "modo_flujo_confirmado: false",
            self.simulation_js,
        )

        self.assertIn(
            "sessionStorage.setItem",
            self.simulation_js,
        )

        self.assertNotIn(
            "localStorage",
            self.mode,
        )

    def test_manual_oculta_superficies_documentales(self):
        self.assertIn(
            "data-assisted-only",
            self.simulation,
        )

        self.assertIn(
            "data-assisted-only",
            self.current,
        )

        self.assertIn(
            "data-assisted-only",
            self.history,
        )

        # El controlador actual normaliza primero la
        # modalidad a un booleano semántico.
        self.assertIn(
            'const esAsistido = (',
            self.mode,
        )

        self.assertIn(
            'modo === "ASISTIDO"',
            self.mode,
        )

        # Toda superficie exclusiva de Asistido se
        # oculta cuando esAsistido es falso.
        self.assertIn(
            'elemento.hidden = !esAsistido;',
            self.mode,
        )

    def test_cambio_a_manual_invalida_dependencias(self):
        for expected in (
            "limpiarReferenciasDocumentalesParaManual",
            "limpiarDesdePaso2",
            "window.confirm",
            "Los datos personales introducidos manualmente",
        ):
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    self.mode,
                )

    def test_manual_no_infiere_decisiones_del_usuario(self):
        for expected in (
            "modo_historial_confirmado_usuario",
            "escenario_retiro_seleccionado",
            "modo_flujo_confirmado",
        ):
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    self.mode,
                )

    def test_gate_manual_conserva_seis_dimensiones(self):
        for key in (
            "datos",
            "decisiones",
            "fechas",
            "importados",
            "dependencias",
            "accion",
        ):
            with self.subTest(key=key):
                self.assertIn(
                    f'data-completeness-key="{key}"',
                    self.simulation,
                )

    def test_paso6_queda_bloqueado_si_manual_incompleto(self):
        self.assertGreaterEqual(
            self.navigation.count(
                "manualFlowCompleto(simulacion)"
            ),
            3,
        )

        self.assertIn(
            "manualFlowCompleto(simulacion)",
            self.results,
        )

        self.assertIn(
            "Revisar datos pendientes",
            self.navigation,
        )

    def test_required_tiene_contrato_semantico_y_visual(self):
        for expected in (
            "prepararCamposObligatorios",
            "aria-required",
            "aria-invalid",
            "asegurarErrorDeCampo",
            "control.focus",
        ):
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    self.accessibility,
                )

        self.assertIn(
            "var(--app-danger-border)",
            self.accessibility_css,
        )

        self.assertIn(
            "var(--app-danger-text)",
            self.accessibility_css,
        )

    def test_resumen_informa_cantidad_de_campos_invalidos(self):
        self.assertIn(
            'id="wizard-validation-summary"',
            self.simulation,
        )

        self.assertIn(
            "actualizarResumenValidacionWizard",
            self.accessibility,
        )

        self.assertIn(
            "Hay 1 campo que debes revisar",
            self.accessibility,
        )

        self.assertIn(
            "Hay ${cantidad} campos que debes revisar",
            self.accessibility,
        )

    def test_wizard_sigue_teniendo_seis_controles(self):
        steps = re.findall(
            r'class="wizard-step(?:\s+[^"]*)?"',
            self.simulation,
        )

        self.assertEqual(
            6,
            len(steps),
        )

    def test_paso2_obligatoriedad_depende_de_continuidad(self):
        self.assertIn(
            "function actualizarEstadoContinuidad()",
            self.simulation_js,
        )

        for expected in (
            "cierre.required = false;",
            "futuras.required = false;",
            "cierre.required = true;",
            "futuras.required = true;",
        ):
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    self.simulation_js,
                )

    def test_paso3_decisiones_fuera_de_form_son_accesibles(self):
        for expected in (
            "prepararValidacionWizardSinFormulario",
            "a11yStandaloneValidation",
            "programarResumenValidacionWizard",
            "asegurarErrorDeCampo",
        ):
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    self.accessibility,
                )

        self.assertIn(
            'id="modo_historial"',
            self.history,
        )

        self.assertIn(
            'id="usar_detalle_anio_actual"',
            self.current,
        )

        self.assertIn(
            'id="modo_detalle_anio_actual"',
            self.current,
        )

    def test_paso3_base_salarial_condiciona_captura_manual(self):
        self.assertIn(
            "function aplicarOrigenBaseSalarial",
            self.current_year_js,
        )

        self.assertIn(
            "monto.required",
            self.current_year_js,
        )

        self.assertIn(
            "periodicidad.required",
            self.current_year_js,
        )

        self.assertIn(
            '"MANUAL"',
            self.current_year_js,
        )

    def test_paso4_obligatoriedad_depende_de_modalidad(self):
        self.assertIn(
            "function actualizarConfiguracionProyeccion()",
            self.simulation_js,
        )

        for expected in (
            "porcentaje.required = false;",
            "salarioFuturo.required = false;",
            "anioFuturo.required = false;",
            "escenarios.required = false;",
            "porcentaje.required = true;",
            "salarioFuturo.required = true;",
            "anioFuturo.required = true;",
            "escenarios.required = true;",
        ):
            with self.subTest(expected=expected):
                self.assertIn(
                    expected,
                    self.simulation_js,
                )

    def test_paso5_fecha_personalizada_es_condicional(self):
        self.assertIn(
            "function actualizarEstadoFechaPersonalizada()",
            self.retirement_js,
        )

        self.assertIn(
            "campo.required = activada;",
            self.retirement_js,
        )

        for field_id in (
            "fecha_corte_retiro",
            "ultimo_mes_cuotas",
            "fecha_retiro_personalizada",
        ):
            with self.subTest(field_id=field_id):
                self.assertIn(
                    f'id="{field_id}"',
                    self.retirement_template,
                )


if __name__ == "__main__":
    unittest.main()
