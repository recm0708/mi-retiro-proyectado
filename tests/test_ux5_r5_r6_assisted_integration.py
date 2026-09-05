"""Regresiones UX.5 R5+R6 del flujo Asistido."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]

SIMULATION = (
    ROOT / "app/templates/simulation.html"
)

CURRENT = (
    ROOT
    / "app/templates/partials/current_year_detail.html"
)

ASSISTED_TEMPLATE = (
    ROOT
    / "app/templates/partials/assisted_preparation.html"
)

MODE_JS = (
    ROOT / "app/static/js/simulation_mode.js"
)

ASSISTED_JS = (
    ROOT / "app/static/js/assisted_flow.js"
)

SIMULATION_JS = (
    ROOT / "app/static/js/simulation.js"
)

WIZARD_JS = (
    ROOT / "app/static/js/wizard_navigation.js"
)

ATTACHMENT_JS = (
    ROOT / "app/static/js/attachment_processing.js"
)

STYLE = (
    ROOT / "app/static/css/style.css"
)


class TestUX5R5R6AssistedIntegration(
    unittest.TestCase
):

    def test_workspace_oculto_hasta_elegir_modalidad(self):
        text = SIMULATION.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'id="simulation-workspace"',
            text,
        )

        position = text.index(
            'id="simulation-workspace"'
        )

        fragment = text[
            max(0, position - 100):
            position + 160
        ]

        self.assertIn(
            'class="d-none"',
            fragment,
        )


    def test_inicio_no_repite_informacion_de_modalidad(self):
        text = SIMULATION.read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            "simulation-mode-policy",
            text,
        )

        self.assertIn(
            "El modo Asistido prepara datos; "
            "nunca toma decisiones por ti.",
            text,
        )


    def test_selector_interno_manual_pdf_fue_eliminado(self):
        text = SIMULATION.read_text(
            encoding="utf-8"
        )

        for legacy in (
            "personal-data-source",
            "modo-datos-manual",
            "modo-datos-pdf",
            "¿Cómo quieres proporcionar tus datos?",
        ):
            with self.subTest(
                legacy=legacy
            ):
                self.assertNotIn(
                    legacy,
                    text,
                )


    def test_preparacion_asistida_contiene_ambos_importadores(self):
        text = ASSISTED_TEMPLATE.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'include "partials/official_data_import.html"',
            text,
        )

        self.assertIn(
            'include "partials/ficha_digital_import.html"',
            text,
        )


    def test_importadores_no_se_repiten_dentro_de_los_pasos(self):
        simulation = SIMULATION.read_text(
            encoding="utf-8"
        )

        current = CURRENT.read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            'include "partials/official_data_import.html"',
            simulation,
        )

        self.assertNotIn(
            'include "partials/ficha_digital_import.html"',
            current,
        )


    def test_asistido_requiere_al_menos_una_fuente(self):
        text = ASSISTED_JS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "function fuenteAsistidaConfirmada",
            text,
        )

        self.assertIn(
            "fuenteMiRetiroConfirmada",
            text,
        )

        self.assertIn(
            "fuenteFichaConfirmada",
            text,
        )


    def test_wizard_asistido_espera_fuente_confirmada(self):
        text = MODE_JS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'const esAsistido = (',
            text,
        )

        self.assertIn(
            'modo === "ASISTIDO"',
            text,
        )

        self.assertIn(
            "const fuenteConfirmada = Boolean(",
            text,
        )

        # El wizard se muestra en Manual o, en
        # Asistido, únicamente tras confirmar fuente.
        self.assertIn(
            "mostrar(\n    wizard,",
            text,
        )

        self.assertIn(
            "esAsistido\n      && fuenteConfirmada",
            text,
        )

    def test_cambiar_modalidad_advierte_si_existe_progreso(self):
        text = MODE_JS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "function simulacionTieneProgresoUsuario",
            text,
        )

        self.assertIn(
            "window.confirm(",
            text,
        )

        self.assertIn(
            "Cambiar a modo Asistido conservará "
            "los datos manuales",
            text,
        )


    def test_conserva_seis_dimensiones_de_completitud(self):
        text = ASSISTED_TEMPLATE.read_text(
            encoding="utf-8"
        )

        for key in (
            "fuente",
            "datos",
            "decisiones",
            "revision",
            "dependencias",
            "accion",
        ):
            with self.subTest(
                key=key
            ):
                self.assertIn(
                    f'data-assisted-completeness="{key}"',
                    text,
                )


    def test_procedencia_no_depende_solo_del_color(self):
        text = ASSISTED_TEMPLATE.read_text(
            encoding="utf-8"
        )

        for label in (
            "Ficha Digital",
            "Mi Retiro Seguro",
            "Ingresado manualmente",
            "Modificado por el usuario",
            "Calculado",
            "Derivado",
            "Confirmado",
        ):
            with self.subTest(
                label=label
            ):
                self.assertIn(
                    label,
                    text,
                )

        self.assertIn(
            "El color nunca es el único indicador",
            text,
        )


    def test_progreso_documental_es_indeterminado(self):
        text = ATTACHMENT_JS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            '"progressbar"',
            text,
        )

        self.assertIn(
            "progress-bar-striped",
            text,
        )

        self.assertIn(
            "progress-bar-animated",
            text,
        )

        self.assertIn(
            "aria-valuetext",
            text,
        )

        self.assertNotIn(
            "aria-valuenow",
            text,
        )


    def test_resultados_asistidos_siguen_protegidos(self):
        simulation = SIMULATION_JS.read_text(
            encoding="utf-8"
        )

        wizard = WIZARD_JS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "bloquearResultadosAsistidos",
            simulation,
        )

        self.assertIn(
            "!assistedFlowCompleto(simulacion)",
            wizard,
        )


    def test_css_legacy_de_modalidad_interna_fue_retirado(self):
        text = STYLE.read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            ".simulation-mode-policy",
            text,
        )

        self.assertNotIn(
            ".personal-data-source",
            text,
        )

        self.assertIn(
            ".assisted-source-card-header",
            text,
        )


if __name__ == "__main__":
    unittest.main()
