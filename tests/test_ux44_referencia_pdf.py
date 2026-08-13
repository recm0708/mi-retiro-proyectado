"""Regresiones UX.4.4 para referencia personal importada desde PDF."""

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.servicios.referencia_mi_retiro_seguro import (
    extraer_referencia_desde_texto,
)


ROOT = Path(__file__).resolve().parents[1]


TEXTO_FEMENINO = """
COMPROBANTE DE DECISIÓN DEL PROGRAMA DE INVALIDEZ, VEJEZ Y MUERTE
REGISTRO DE DECISIÓN DEL ASEGURADO
Fecha de Comprobante: 10/08/2026
Fecha de Nacimiento: 16/11/1969
Sexo: Femenino
Fecha de Ingreso CSS: 23/07/1997
Total cuotas históricas
 aportadas a la fecha:
281
PROYECCIÓN Y DECISIÓN
Edad de retiro elegida: 57 años
Prestación esperada: PENSIÓN MENSUAL VITALICIA
Monto estimado de prestación: B/. 741.59
Sistema elegido: Subsistema Exclusivo de Beneficio Definido (SEBD)
Fecha de decisión: 24 de julio de 2026
Código de documento:
CSS-PENSION-PRUEBA-F
1992 23 Histórico 356.98 1
2026 57 Histórico + Proyectado 6,659.50 5
2027 58 Proyectado 16,142.63 12
Total de cuotas acumuladas: 293 cuotas
"""


TEXTO_MASCULINO = """
COMPROBANTE DE DECISIÓN DEL PROGRAMA DE INVALIDEZ, VEJEZ Y MUERTE
REGISTRO DE DECISIÓN DEL ASEGURADO
Fecha de Comprobante: 10/08/2026
Fecha de Nacimiento: 04/12/1966
Sexo: Masculino
Fecha de Ingreso CSS: 27/01/1986
Total cuotas históricas
 aportadas a la fecha:
461
PROYECCIÓN Y DECISIÓN
Edad de retiro elegida: 62 años
Prestación esperada: PENSIÓN MENSUAL VITALICIA
Monto estimado de prestación: B/. 1,265.23
Sistema elegido: Subsistema Exclusivo de Beneficio Definido (SEBD)
Fecha de decisión: 10 de mayo de 2026
Código de documento:
CSS-PENSION-PRUEBA-M
1986 20 Histórico 3,927.05 11
2029 63 Proyectado 19,221.21 12
Total de cuotas acumuladas: 497 cuotas
"""


class TestUX44ReferenciaPDF(unittest.TestCase):
    """Protege extracción variable, privacidad y comparación en Paso 6."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(app)
        cls.simulacion = (ROOT / "app/templates/simulacion.html").read_text(
            encoding="utf-8"
        )
        cls.parcial = (
            ROOT / "app/templates/partials/importacion_datos_oficiales.html"
        ).read_text(encoding="utf-8")
        cls.resultados_html = (
            ROOT / "app/templates/partials/resultados.html"
        ).read_text(encoding="utf-8")
        cls.referencia_js = (
            ROOT / "app/static/js/referencia_mi_retiro_seguro.js"
        ).read_text(encoding="utf-8")
        cls.resultados_js = (
            ROOT / "app/static/js/resultados.js"
        ).read_text(encoding="utf-8")
        cls.css = (ROOT / "app/static/css/style.css").read_text(encoding="utf-8")
        cls.requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")

    def test_parser_extrae_referencia_femenina_variable(self):
        referencia = extraer_referencia_desde_texto(TEXTO_FEMENINO)

        self.assertEqual(referencia.monto_estimado_prestacion, 741.59)
        self.assertEqual(referencia.cuotas_historicas, 281)
        self.assertEqual(referencia.edad_retiro_elegida, 57)
        self.assertEqual(referencia.sistema_elegido, "SEBD")
        self.assertEqual(referencia.naturaleza_prestacion, "PENSION_MENSUAL")
        self.assertEqual(len(referencia.registros), 3)

    def test_parser_no_depende_del_monto_de_un_unico_pdf(self):
        referencia = extraer_referencia_desde_texto(TEXTO_MASCULINO)

        self.assertEqual(referencia.monto_estimado_prestacion, 1265.23)
        self.assertEqual(referencia.cuotas_historicas, 461)
        self.assertEqual(referencia.edad_retiro_elegida, 62)

    def test_parser_rechaza_documento_ajeno(self):
        with self.assertRaises(ValueError):
            extraer_referencia_desde_texto("Documento cualquiera sin marcador")

    def test_contrato_no_expone_identificadores_personales(self):
        referencia = extraer_referencia_desde_texto(TEXTO_FEMENINO).model_dump()

        self.assertNotIn("nombre", referencia)
        self.assertNotIn("cedula", referencia)
        self.assertNotIn("seguro_social", referencia)
        self.assertNotIn("codigo_documento", referencia)

    def test_endpoint_rechaza_archivo_no_pdf(self):
        respuesta = self.cliente.post(
            "/api/simulacion/referencia-mi-retiro-seguro",
            files={"archivo": ("referencia.txt", b"texto", "text/plain")},
        )

        self.assertEqual(respuesta.status_code, 415)

    def test_interfaz_ofrece_carga_revisable_y_aclara_que_no_hay_monto_fijo(self):
        self.assertIn('id="import-comprobante-pdf"', self.parcial)
        self.assertIn('accept=".pdf,application/pdf"', self.parcial)
        self.assertIn("previa editable", self.parcial)
        self.assertIn("No existe un monto predeterminado", self.resultados_html)
        self.assertIn("referencia_mi_retiro_seguro.js", self.simulacion)
        self.assertIn("resultado-comparacion-referencia", self.resultados_html)

    def test_comparacion_usa_monto_extraido_y_resultado_actual(self):
        self.assertIn("referencia.monto_estimado_prestacion", self.referencia_js)
        self.assertIn("Number(actual) - Number(referencia.monto_estimado_prestacion)", self.referencia_js)
        self.assertIn("referencia.edad_retiro_elegida", self.referencia_js)
        self.assertIn("referencia.fecha_ingreso_css", self.referencia_js)
        self.assertIn("referencia.sistema_elegido === resumenActual.sistema", self.referencia_js)
        self.assertIn("mostrarComparacionReferenciaMiRetiroSeguro(resumen)", self.resultados_js)

    def test_produccion_no_hardcodea_montos_de_los_dos_comprobantes(self):
        rutas = [
            ROOT / "app/static/js/referencia_mi_retiro_seguro.js",
            ROOT / "app/templates/partials/resultados.html",
            ROOT / "app/templates/partials/importacion_datos_oficiales.html",
            ROOT / "app/servicios/referencia_mi_retiro_seguro.py",
        ]
        contenido = "\n".join(ruta.read_text(encoding="utf-8") for ruta in rutas)

        self.assertNotIn("741.59", contenido)
        self.assertNotIn("1265.23", contenido)

    def test_pypdf_esta_versionado_y_boton_mi_caja_queda_centrado(self):
        self.assertIn("pypdf==5.9.0", self.requirements)
        self.assertIn(".current-year-detail-source {", self.css)
        self.assertIn("align-items: center;", self.css)
        self.assertIn(".current-year-detail-source .btn", self.css)


if __name__ == "__main__":
    unittest.main()
