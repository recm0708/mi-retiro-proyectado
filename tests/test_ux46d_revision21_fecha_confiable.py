"""Regresiones UX.4.6d R21: vigencia mensual con fecha externa verificable."""

import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from app.servicios import fecha_referencia
from app.servicios.ficha_digital import extraer_ficha_digital_desde_texto

ROOT = Path(__file__).resolve().parents[1]


FICHA_TEXTO = """
FICHA DIGITAL
SALARIOS DEL ÚLTIMO AÑO
2026 - Mayo 1,331.90
2026 - Junio 1,562.37
"""


class TestUX46DRevision21FechaConfiable(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.importacion_js = (
            ROOT / "app/static/js/importacion_datos_oficiales.js"
        ).read_text(encoding="utf-8")
        cls.main_py = (ROOT / "app/main.py").read_text(encoding="utf-8")
        cls.modelo = (ROOT / "app/modelos/simulacion.py").read_text(encoding="utf-8")
        cls.servicio = (ROOT / "app/servicios/fecha_referencia.py").read_text(encoding="utf-8")
        cls.privacidad_js = (ROOT / "app/static/js/privacidad.js").read_text(encoding="utf-8")
        cls.privacidad_html = (ROOT / "app/templates/partials/privacidad_consentimiento.html").read_text(encoding="utf-8")

    def test_cualquier_mes_anterior_requiere_revision(self):
        self.assertIn("diferenciaMeses > 0", self.importacion_js)
        self.assertNotIn("FICHA_VIGENCIA_TOLERANCIA_MESES", self.importacion_js)
        self.assertIn('estado = "DESACTUALIZADA"', self.importacion_js)

    def test_vigencia_no_usa_reloj_del_navegador(self):
        self.assertNotIn("new Date()", self.importacion_js)
        self.assertIn("fecha_referencia_confiable", self.importacion_js)
        self.assertIn("descomponerFechaReferenciaFicha", self.importacion_js)

    def test_fecha_se_consulta_en_backend_y_se_expone_en_resumen(self):
        self.assertIn("obtener_fecha_referencia_confiable", self.main_py)
        self.assertIn('"/api/sistema/fecha-referencia"', self.main_py)
        self.assertIn("fecha_referencia: date | None", self.modelo)
        self.assertIn("fecha_referencia_confiable: bool", self.modelo)

    def test_fuentes_de_fecha_son_dominios_oficiales_css(self):
        self.assertIn("https://www.css.gob.pa/", self.servicio)
        self.assertIn("https://tramites.css.gob.pa/", self.servicio)
        self.assertIn('fuente="NO_DISPONIBLE"', self.servicio)

    def test_si_no_hay_fecha_externa_la_interfaz_no_confia_en_reloj_local(self):
        self.assertIn('estado: "FECHA_NO_VERIFICADA"', self.importacion_js)
        self.assertIn("No fue posible verificar en línea la fecha actual", self.importacion_js)
        self.assertIn("requiereDecision: true", self.importacion_js)

    def test_servicio_acepta_fecha_oficial_sin_depender_de_date_today(self):
        with patch.object(
            fecha_referencia,
            "_consultar_fecha_http",
            side_effect=[date(2026, 8, 16), date(2026, 8, 16)],
        ):
            resultado = fecha_referencia._consultar_fuentes()
        self.assertTrue(resultado.confiable)
        self.assertEqual(resultado.fecha, date(2026, 8, 16))
        self.assertIn("CSS", resultado.fuente)

    def test_parser_toma_el_anio_mas_reciente_del_documento_sin_reloj_local(self):
        resumen = extraer_ficha_digital_desde_texto(FICHA_TEXTO)
        self.assertEqual(resumen.anio_mas_reciente, 2026)
        self.assertEqual(resumen.mes_mas_reciente, 6)
        self.assertEqual(len(resumen.registros), 2)

    def test_importacion_persistida_revalida_fecha_actual(self):
        self.assertIn("refrescarFechaReferenciaFichaPersistida", self.importacion_js)
        self.assertIn('fetch("/api/sistema/fecha-referencia"', self.importacion_js)
        self.assertIn('cache: "no-store"', self.importacion_js)

    def test_privacidad_informa_consulta_de_fecha_y_actualiza_version(self):
        self.assertIn('VERSION_PRIVACIDAD = "2026-08-16.1"', self.privacidad_js)
        self.assertIn("fecha de referencia desde infraestructura web oficial", self.privacidad_html)
        self.assertIn("no envía el documento", self.privacidad_html)
        self.assertIn("dirección IP", self.privacidad_html)


if __name__ == "__main__":
    unittest.main()
