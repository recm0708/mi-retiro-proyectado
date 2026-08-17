"""Regresiones de UX.4.6d R9: reactividad tabular, privacidad y ejemplos genéricos."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class TestUX46DRevision9ReactividadPrivacidad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.historial_js = (ROOT / "app/static/js/historial_salarios.js").read_text(encoding="utf-8")
        cls.style = (ROOT / "app/static/css/style.css").read_text(encoding="utf-8")
        cls.privacidad_js = (ROOT / "app/static/js/privacidad.js").read_text(encoding="utf-8")
        cls.terminos = (
            ROOT / "app/templates/partials/privacidad_consentimiento.html"
        ).read_text(encoding="utf-8")
        cls.accesibilidad = (ROOT / "app/static/js/accesibilidad.js").read_text(encoding="utf-8")

    def test_historial_usa_delegacion_reactiva_para_filas_regeneradas(self):
        self.assertIn("function configurarEventosDelegadosHistorial", self.historial_js)
        self.assertIn('cuerpo.dataset.historyDelegated = "true"', self.historial_js)
        self.assertIn('cuerpo.addEventListener("input", manejarEdicionDelegadaHistorial)', self.historial_js)
        self.assertIn('cuerpo.addEventListener("change", manejarEdicionDelegadaHistorial)', self.historial_js)
        self.assertIn("actualizarEstadoFila(fila);", self.historial_js)
        self.assertIn("invalidarHistorial();", self.historial_js)

    def test_filtro_pendientes_se_reaplica_en_cada_cambio_de_estado(self):
        bloque = self.historial_js.split("function actualizarEstadoFila(fila)", 1)[1].split(
            "// ============================================================\n// Lectura y validación", 1
        )[0]
        self.assertIn("actualizarFiltroHistorial();", bloque)

    def test_tabla_corta_elimina_carril_vertical_en_escritorio(self):
        self.assertIn("overflow: visible !important", self.style)
        self.assertIn("overflow-y: clip !important", self.style)
        self.assertIn('contenedor.dataset.visibleRows = String(visibles)', self.historial_js)

    def test_fuentes_exige_consentimiento_si_no_hay_aceptacion_vigente(self):
        self.assertIn('consentimiento ? "revision" : "consentimiento"', self.privacidad_js)
        self.assertIn('"fuentes"', self.privacidad_js)
        self.assertIn("guardarConsentimientoPrivacidad();", self.privacidad_js)

    def test_escape_tiene_comportamiento_contextual_y_no_activa_animacion_estatica(self):
        self.assertIn("function manejarEscapePrivacidad", self.privacidad_js)
        self.assertIn('evento.key !== "Escape"', self.privacidad_js)
        self.assertIn("evento.stopImmediatePropagation();", self.privacidad_js)
        self.assertIn("cerrarModalPrivacidad();", self.privacidad_js)
        self.assertIn('contextoPrivacidadActual === "fuentes"', self.privacidad_js)

    def test_texto_legal_explica_aceptacion_desde_fuentes_y_cierre_sin_consentimiento(self):
        self.assertIn("Si todavía no existe una aceptación", self.terminos)
        self.assertIn("esa misma consulta permite leer el documento completo y otorgar el consentimiento", self.terminos)
        self.assertIn("la tecla Escape", self.terminos)
        self.assertIn("no registra consentimiento ni habilita la simulación", self.terminos)

    def test_placeholders_personales_son_ficticios_y_genericos(self):
        for texto in ("Anabel", "Estela", "Miranda", "Madrid", "Cañizares", "4-710-1295"):
            self.assertNotIn(texto, self.accesibilidad)
        for texto in (
            'primer_nombre: "Ej.: Nombre"',
            'primer_apellido: "Ej.: Apellido"',
            'cedula: "Ej.: 8-000-0000"',
            'numero_seguro_social: "Ej.: 00000000"',
        ):
            self.assertIn(texto, self.accesibilidad)


if __name__ == "__main__":
    unittest.main()
