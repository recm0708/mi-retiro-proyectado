"""Regresiones de UX.4.6d R7: consulta de privacidad sin reconsentimiento."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision7PrivacidadConsulta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = (ROOT / "app/templates/base.html").read_text(encoding="utf-8")
        cls.simulacion = (ROOT / "app/templates/simulation.html").read_text(encoding="utf-8")
        cls.metodologia = (ROOT / "app/templates/metodologia.html").read_text(encoding="utf-8")
        cls.terminos = (
            ROOT / "app/templates/partials/privacy_consent.html"
        ).read_text(encoding="utf-8")
        cls.privacidad = (ROOT / "app/static/js/privacy.js").read_text(encoding="utf-8")
        cls.design = (ROOT / "app/static/css/design-system.css").read_text(encoding="utf-8")

    def test_modal_y_controlador_de_privacidad_son_globales_y_unicos(self):
        self.assertEqual(self.base.count('partials/privacy_consent.html'), 1)
        self.assertEqual(self.base.count("/js/privacy.js"), 1)
        self.assertNotIn('partials/privacy_consent.html', self.simulacion)
        self.assertNotIn("/js/privacy.js", self.simulacion)

    def test_fuentes_abre_revision_en_la_misma_pagina(self):
        self.assertIn('data-privacy-action="review"', self.metodologia)
        self.assertNotIn('/simulacion?privacidad=1', self.metodologia)
        self.assertIn('consentimiento ? "revision" : "consentimiento"', self.privacidad)
        self.assertIn('"fuentes"', self.privacidad)

    def test_revision_no_muestra_controles_de_consentimiento(self):
        bloque = self.privacidad.split('if (modoPrivacidadActual === "revision")', 1)[1].split(
            'if (kicker) kicker.textContent = "Antes de comenzar"', 1
        )[0]
        self.assertIn('footer.hidden = true', bloque)
        self.assertIn('no modifica tu aceptación', self.privacidad)

    def test_modal_tiene_cierre_superior_contextual(self):
        self.assertIn('id="btn-privacidad-cerrar"', self.terminos)
        self.assertIn('aria-label="Cerrar términos y privacidad"', self.terminos)
        self.assertIn('function cerrarModalPrivacidad()', self.privacidad)
        self.assertIn('modoPrivacidadActual === "revision"', self.privacidad)
        self.assertIn('contextoPrivacidadActual !== "simulacion"', self.privacidad)
        self.assertIn('"fuentes"', self.privacidad)
        self.assertIn('rechazarPrivacidad();', self.privacidad)
        self.assertIn('.privacy-modal-close', self.design)

    def test_consentimiento_automatico_solo_se_exige_en_simulacion(self):
        self.assertIn('function esRutaSimulacion()', self.privacidad)
        self.assertIn('if (esRutaSimulacion() && !consentimiento)', self.privacidad)

    def test_consulta_no_cambia_version_material_de_privacidad(self):
        self.assertIn('VERSION_PRIVACIDAD = "2026-08-16.1"', self.privacidad)
        self.assertIn('Si ya existe una aceptación válida', self.terminos)
        self.assertIn('no exige aceptarlos de nuevo', self.terminos)

    def test_fuentes_mantiene_repositorio_en_area_de_ayuda(self):
        self.assertIn('id="ayuda-contacto"', self.metodologia)
        self.assertIn('Abrir repositorio del proyecto', self.metodologia)
        self.assertIn('href="https://github.com/recm0708/mi-retiro-proyectado"', self.metodologia)
        self.assertNotIn('https://github.com/recm0708/calculadora-pension-css', self.metodologia)

    def test_opciones_destructivas_siguen_fuera_de_barra_inferior(self):
        superior = self.simulacion.split('id="wizard-sticky-nav"', 1)[1].split(
            'PASO 1 — DATOS PERSONALES', 1
        )[0]
        inferior = self.simulacion.split('id="wizard-navigation-bottom"', 1)[1]
        self.assertIn('wizard-data-options', superior)
        self.assertNotIn('wizard-data-options', inferior)
        self.assertIn('.wizard-navigation-bar-bottom .wizard-data-options', self.design)

    def test_documento_legal_no_duplica_seccion_ejercicio(self):
        self.assertEqual(self.terminos.count('aria-labelledby="privacidad-ejercicio"'), 1)


if __name__ == "__main__":
    unittest.main()
