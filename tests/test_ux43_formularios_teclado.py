"""Regresiones de UX.4.3 para errores, foco y operación por teclado."""

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


ROOT = Path(__file__).resolve().parents[1]


class TestUX43FormulariosTeclado(unittest.TestCase):
    """Protege semántica de errores y navegación por teclado de UX.4.3."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(app)
        cls.a11y = (ROOT / "app/static/js/accessibility.js").read_text(encoding="utf-8")
        cls.retiro = (ROOT / "app/static/js/retirement.js").read_text(encoding="utf-8")
        cls.css = (ROOT / "app/static/css/accessibility.css").read_text(encoding="utf-8")

    def test_error_nativo_crea_mensaje_asociado_al_control(self):
        self.assertIn("a11y-error-${control.id}", self.a11y)
        self.assertIn('aria-errormessage', self.a11y)
        self.assertIn("obtenerMensajeValidacionControl", self.a11y)
        self.assertIn("a11y-field-error", self.a11y)

    def test_error_nativo_se_limpia_cuando_el_control_vuelve_a_ser_valido(self):
        self.assertIn("limpiarErrorDeCampo", self.a11y)
        self.assertIn('removeAttribute("aria-invalid")', self.a11y)
        self.assertIn('removeAttribute("aria-errormessage")', self.a11y)
        self.assertIn('formulario.addEventListener("reset"', self.a11y)

    def test_errores_dinamicos_usan_alert_sin_region_viva_duplicada(self):
        self.assertIn('elemento.setAttribute("role", "alert")', self.a11y)
        self.assertIn('elemento.removeAttribute("aria-live")', self.a11y)
        self.assertIn('elemento.setAttribute("aria-atomic", "true")', self.a11y)
        self.assertNotIn('setAttribute("aria-live", "assertive")', self.a11y)

    def test_error_dinamico_recibe_foco_solo_al_hacerse_visible(self):
        self.assertIn("prepararEstadoVisibilidadMensaje", self.a11y)
        self.assertIn("dataset.a11yVisible", self.a11y)
        self.assertIn('elemento.focus({ preventScroll: false })', self.a11y)
        self.assertIn('elemento.setAttribute("tabindex", "-1")', self.a11y)

    def test_advertencias_no_urgentes_pueden_usar_status_polite(self):
        self.assertIn('elemento.setAttribute("role", "status")', self.a11y)
        self.assertIn('elemento.setAttribute("aria-live", "polite")', self.a11y)

    def test_foco_programatico_de_mensajes_es_visible(self):
        self.assertIn(".a11y-message-focus:focus", self.css)
        self.assertIn("outline: 3px solid var(--app-focus)", self.css)
        self.assertIn('data-app-theme="contrast"', self.css)

    def test_radio_de_retiro_acepta_enter_sin_crear_tab_stop_extra(self):
        self.assertIn('evento.key !== "Enter"', self.retiro)
        self.assertIn("evento.preventDefault()", self.retiro)
        self.assertIn("selector.checked = true", self.retiro)
        self.assertNotIn('fila.tabIndex = 0', self.retiro)


    def test_mutaciones_de_clase_de_accesibilidad_son_idempotentes(self):
        self.assertIn('!elemento.classList.contains("a11y-message-focus")', self.a11y)
        self.assertIn('!contenedor.classList.contains("table-scroll-focus")', self.a11y)

    def test_limpieza_de_error_no_redespacha_invalid(self):
        self.assertIn('control.validity?.valid === true', self.a11y)
        self.assertNotIn('control.checkValidity()', self.a11y)

    def test_error_de_campo_es_visible_y_no_solo_para_lector_de_pantalla(self):
        self.assertIn('error.className = "a11y-field-error"', self.a11y)
        self.assertNotIn('visually-hidden a11y-field-error', self.a11y)
        self.assertIn('.a11y-field-error {', self.css)
        self.assertIn('display: block', self.css)

    def test_validacion_no_depende_del_globo_nativo_del_navegador(self):
        self.assertIn('formulario.addEventListener("invalid"', self.a11y)
        self.assertIn('evento.preventDefault()', self.a11y)
        self.assertIn('asegurarErrorDeCampo(control)', self.a11y)

    def test_paginas_principales_conservan_un_h1(self):
        for ruta in ("/", "/simulacion", "/comparar", "/metodologia"):
            with self.subTest(ruta=ruta):
                respuesta = self.cliente.get(ruta)
                self.assertEqual(respuesta.status_code, 200)
                self.assertEqual(respuesta.text.count("<h1"), 1)


if __name__ == "__main__":
    unittest.main()
