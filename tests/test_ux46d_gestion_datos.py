"""Regresiones de UX.4.6d R6 para gestión local de datos y privacidad."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestUX46DGestionDatos(unittest.TestCase):
    """Protege limpieza por paso, reinicio y borrado local integral."""

    @classmethod
    def setUpClass(cls):
        cls.simulacion = (ROOT / "app/templates/simulacion.html").read_text(encoding="utf-8")
        cls.base = (ROOT / "app/templates/base.html").read_text(encoding="utf-8")
        cls.metodologia = (ROOT / "app/templates/metodologia.html").read_text(encoding="utf-8")
        cls.modal = (
            ROOT / "app/templates/partials/gestion_datos.html"
        ).read_text(encoding="utf-8")
        cls.terminos = (
            ROOT / "app/templates/partials/privacidad_consentimiento.html"
        ).read_text(encoding="utf-8")
        cls.gestion = (
            ROOT / "app/static/js/gestion_datos.js"
        ).read_text(encoding="utf-8")
        cls.privacidad = (
            ROOT / "app/static/js/privacidad.js"
        ).read_text(encoding="utf-8")
        cls.css = (
            ROOT / "app/static/css/design-system.css"
        ).read_text(encoding="utf-8")

    def test_opciones_solo_se_agregan_a_barra_superior(self):
        superior = self.simulacion.split('id="wizard-sticky-nav"', 1)[1].split(
            "PASO 1 — DATOS PERSONALES", 1
        )[0]
        inferior = self.simulacion.split('id="wizard-navigation-bottom"', 1)[1]
        self.assertIn("Opciones", superior)
        self.assertIn('data-data-action="clear-step"', superior)
        self.assertIn('data-data-action="restart-simulation"', superior)
        self.assertNotIn('data-data-action="clear-step"', inferior)
        self.assertNotIn('data-data-action="restart-simulation"', inferior)

    def test_limpiar_paso_se_deshabilita_si_no_hay_datos(self):
        self.assertIn("function actualizarDisponibilidadGestionDatos", self.gestion)
        self.assertIn("control.disabled = !disponible", self.gestion)
        simulacion_js = (ROOT / "app/static/js/simulacion.js").read_text(encoding="utf-8")
        self.assertIn("actualizarDisponibilidadGestionDatos", simulacion_js)

    def test_modal_destructivo_es_unico_y_reutilizable(self):
        self.assertIn('id="modal-gestion-datos"', self.modal)
        self.assertIn('id="gestion-datos-mensaje"', self.modal)
        self.assertIn('id="btn-gestion-datos-confirmar"', self.modal)
        self.assertIn('partials/gestion_datos.html', self.base)

    def test_limpiar_paso_respeta_jerarquia_descendente(self):
        self.assertIn("function limpiarDesdePaso2", self.gestion)
        self.assertIn("limpiarDesdePaso3(simulacion);", self.gestion)
        self.assertIn("function limpiarDesdePaso3", self.gestion)
        self.assertIn("limpiarDesdePaso4(simulacion);", self.gestion)
        self.assertIn("function limpiarDesdePaso4", self.gestion)
        self.assertIn("limpiarDesdePaso5(simulacion);", self.gestion)
        self.assertIn("function limpiarDesdePaso5", self.gestion)
        self.assertIn("limpiarResultadosPaso6(simulacion);", self.gestion)

    def test_limpiar_paso3_elimina_historial_ficha_detalle_y_base(self):
        bloque = self.gestion.split("function limpiarDesdePaso3", 1)[1].split(
            "function limpiarDesdePaso2", 1
        )[0]
        for fragmento in (
            'simulacion.historial = null',
            'simulacion.origen_campos_historial = {}',
            'simulacion.ficha_digital_importada = null',
            'simulacion.importacion_ficha_digital_confirmada = false',
            'simulacion.detalle_anio_actual = null',
            'simulacion.origen_campos_detalle_anio_actual = {}',
            'simulacion.salario = {}',
            'simulacion.resumen_salario = null',
        ):
            self.assertIn(fragmento, bloque)

    def test_reinicio_conserva_privacidad_y_tema(self):
        bloque = self.gestion.split("function solicitarReiniciarSimulacion", 1)[1].split(
            "function solicitarBorrarDatosAplicacion", 1
        )[0]
        self.assertIn("apariencia y la aceptación vigente", bloque)
        ejecucion = self.gestion.split("accionGestionDatosPendiente === \"simulation\"", 1)[1].split(
            "accionGestionDatosPendiente === \"browser\"", 1
        )[0]
        self.assertNotIn("CLAVE_GESTION_PRIVACIDAD", ejecucion)
        self.assertNotIn("CLAVE_GESTION_TEMA", ejecucion)

    def test_borrado_integral_elimina_solo_claves_de_la_aplicacion(self):
        bloque = self.gestion.split('accionGestionDatosPendiente === "browser"', 1)[1]
        self.assertIn("CLAVE_GESTION_SIMULACION", bloque)
        self.assertIn("CLAVE_GESTION_PRIVACIDAD_SESION", bloque)
        self.assertIn("CLAVE_GESTION_PRIVACIDAD", bloque)
        self.assertIn("CLAVE_GESTION_TEMA", bloque)
        self.assertNotIn("localStorage.clear", self.gestion)
        self.assertNotIn("sessionStorage.clear", self.gestion)

    def test_fuentes_ofrece_borrado_local_integral(self):
        self.assertIn(
            "Borrar datos de esta aplicación en este navegador",
            self.metodologia,
        )
        self.assertIn('data-data-action="clear-browser-data"', self.metodologia)

    def test_terminos_describen_los_tres_niveles_de_control(self):
        self.assertIn("Limpiar este paso", self.terminos)
        self.assertIn("Reiniciar simulación", self.terminos)
        self.assertIn("Borrar datos de esta aplicación en este navegador", self.terminos)
        self.assertIn("no equivale a una solicitud de eliminación ante un servicio remoto", self.terminos)

    def test_version_privacidad_se_actualiza_por_cambio_material(self):
        self.assertIn('VERSION_PRIVACIDAD = "2026-08-16.1"', self.privacidad)

    def test_estilos_para_opciones_y_modal_existen(self):
        self.assertIn(".wizard-data-options", self.css)
        self.assertIn(".data-management-modal", self.css)

    def test_documentacion_transversal_esta_versionada(self):
        for relativo in (
            "docs/GESTION_DATOS_SIMULACION.md",
            "docs/POLITICA_PRIVACIDAD.md",
            "docs/TERMINOS_USO_PRIVACIDAD.md",
            "docs/CUMPLIMIENTO_LEY_81.md",
            "docs/SEGURIDAD_PRIVACIDAD.md",
        ):
            contenido = (ROOT / relativo).read_text(encoding="utf-8")
            self.assertTrue(contenido.strip())
        self.assertIn(
            "2026-08-16.1",
            (ROOT / "docs/POLITICA_PRIVACIDAD.md").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
