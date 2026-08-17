"""Regresiones de UX.4.6b Revisiones 3–4: términos y navegación dual."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestUX46bRevision3TerminosNavegacion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.terminos = (
            ROOT / "app/templates/partials/privacidad_consentimiento.html"
        ).read_text(encoding="utf-8")
        cls.privacidad_js = (
            ROOT / "app/static/js/privacidad.js"
        ).read_text(encoding="utf-8")
        cls.simulacion = (
            ROOT / "app/templates/simulacion.html"
        ).read_text(encoding="utf-8")
        cls.navegacion_js = (
            ROOT / "app/static/js/navegacion_wizard.js"
        ).read_text(encoding="utf-8")
        cls.design = (
            ROOT / "app/static/css/design-system.css"
        ).read_text(encoding="utf-8")
        cls.metodologia = (
            ROOT / "app/templates/metodologia.html"
        ).read_text(encoding="utf-8")

    def test_terminos_ampliados_cubren_apartados_juridicos_y_operativos(self):
        for titulo in (
            "Objeto y alcance",
            "Responsable y canales de contacto",
            "Marco legal de referencia",
            "Obtención de la información",
            "Datos que pueden tratarse",
            "Finalidades del tratamiento",
            "Consentimiento y carácter voluntario",
            "Custodia, confidencialidad y seguridad",
            "Cesión, destinatarios y transferencias",
            "Derechos del titular",
            "Incidentes y vulneraciones de seguridad",
            "Legislación aplicable y fuentes oficiales",
        ):
            self.assertIn(titulo, self.terminos)

    def test_terminos_visibles_no_exponen_nombres_de_web_storage(self):
        self.assertNotIn("sessionStorage", self.terminos)
        self.assertNotIn("localStorage", self.terminos)
        self.assertNotIn("sessionStorage", self.metodologia)
        self.assertNotIn("localStorage", self.metodologia)

    def test_casilla_inicia_deshabilitada_y_requiere_final_de_lectura(self):
        self.assertIn('id="aceptar-privacidad-check" disabled', self.terminos)
        self.assertNotIn('id="privacidad-fin-documento"', self.terminos)
        self.assertNotIn("Fin de los términos", self.terminos)
        self.assertNotIn("Lectura completada", self.privacidad_js)
        self.assertIn("lecturaPrivacidadCompletada", self.privacidad_js)
        self.assertIn("MARGEN_FINAL_LECTURA", self.privacidad_js)
        self.assertIn("check.disabled = false", self.privacidad_js)
        self.assertIn("estado.hidden = true", self.privacidad_js)
        self.assertIn("!check?.checked || !lecturaPrivacidadCompletada()", self.privacidad_js)

    def test_version_de_privacidad_cambia_en_revision3(self):
        self.assertIn('VERSION_PRIVACIDAD = "2026-08-16.1"', self.privacidad_js)

    def test_navegacion_superior_e_inferior_comparten_contrato(self):
        self.assertIn('data-wizard-nav="top"', self.simulacion)
        self.assertIn('data-wizard-nav="bottom"', self.simulacion)
        self.assertEqual(self.simulacion.count('data-wizard-action="back"'), 2)
        self.assertEqual(self.simulacion.count('data-wizard-action="primary"'), 2)
        self.assertEqual(self.simulacion.count('data-wizard-step-jump'), 2)
        self.assertEqual(self.simulacion.count('data-wizard-status'), 2)

    def test_javascript_sincroniza_todos_los_controles_de_navegacion(self):
        self.assertIn('querySelectorAll("[data-wizard-step-jump]")', self.navegacion_js)
        self.assertIn("querySelectorAll('[data-wizard-action=\"back\"]')", self.navegacion_js)
        self.assertIn("querySelectorAll('[data-wizard-action=\"primary\"]')", self.navegacion_js)
        self.assertIn('querySelectorAll("[data-wizard-status]")', self.navegacion_js)

    def test_barra_superior_es_sticky_y_ambas_conservan_mismo_ancho(self):
        self.assertIn(".wizard-navigation-bar {", self.design)
        self.assertIn("width: 100%;", self.design)
        zona = self.design.split(".wizard-navigation-bar-top", 1)[1][:500]
        self.assertIn("position: sticky;", zona)
        self.assertIn("top: 86px;", zona)
        self.assertIn(".wizard-navigation-bar-bottom", self.design)

    def test_ayudas_contextuales_no_se_recortan_por_tarjeta(self):
        zonas = [
            parte[:250]
            for parte in self.design.split(".simulation-card {")[1:]
        ]
        self.assertTrue(any("overflow: visible;" in zona for zona in zonas))

    def test_modal_explica_ausencia_de_cookies_sin_pedir_consentimiento_inexistente(self):
        self.assertIn("no utiliza cookies para publicidad", self.terminos.lower())
        self.assertIn("Si en el futuro se incorporan cookies no esenciales", self.terminos)
        self.assertNotIn("Aceptar cookies", self.terminos)


    def test_copy_visible_no_posiciona_la_aplicacion_como_educativa(self):
        plantillas = "\n".join(
            archivo.read_text(encoding="utf-8").lower()
            for archivo in (ROOT / "app/templates").rglob("*.html")
        )
        for termino in (
            "aplicación educativa",
            "herramienta educativa",
            "recurso educativo",
            "finalidad educativa",
            "uso educativo",
            "didáctic",
            "pedagóg",
        ):
            self.assertNotIn(termino, plantillas)



if __name__ == "__main__":
    unittest.main()
