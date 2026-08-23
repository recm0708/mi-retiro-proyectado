"""Regresiones de UX.4.6b Revisión 2: privacidad y refinamientos visuales."""

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.services.referencia_mi_retiro_seguro import extraer_referencia_desde_texto


ROOT = Path(__file__).resolve().parents[1]


TEXTO_CASADA = """
COMPROBANTE DE DECISIÓN DEL PROGRAMA DE INVALIDEZ, VEJEZ Y MUERTE
Nombre: Anabel Estela Miranda Madrid de Cañizares
Cédula: 4-710-1295
No. Seguro Social: 2738720
Fecha de Comprobante: 10/08/2026
Fecha de Nacimiento: 16/11/1969
Sexo: Femenino
Fecha de Ingreso CSS: 23/07/1997
Total cuotas históricas aportadas a la fecha: 281
Edad de retiro elegida: 57 años
Prestación esperada: PENSIÓN MENSUAL VITALICIA
Monto estimado de prestación: B/. 741.59
Sistema elegido: Subsistema Exclusivo de Beneficio Definido (SEBD)
1992 23 Histórico 356.98 1
Total de cuotas acumuladas: 281 cuotas
"""


class TestUX46bRevision2Privacidad(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.simulacion = (ROOT / "app/templates/simulacion.html").read_text(encoding="utf-8")
        cls.importacion = (
            ROOT / "app/templates/partials/importacion_datos_oficiales.html"
        ).read_text(encoding="utf-8")
        cls.privacidad_html = (
            ROOT / "app/templates/partials/privacidad_consentimiento.html"
        ).read_text(encoding="utf-8")
        cls.privacidad_js = (ROOT / "app/static/js/privacidad.js").read_text(encoding="utf-8")
        cls.accesibilidad_js = (ROOT / "app/static/js/accesibilidad.js").read_text(encoding="utf-8")
        cls.design = (ROOT / "app/static/css/design-system.css").read_text(encoding="utf-8")
        cls.metodologia = (ROOT / "app/templates/metodologia.html").read_text(encoding="utf-8")
        cls.base = (ROOT / "app/templates/base.html").read_text(encoding="utf-8")

    def test_campos_obligatorios_tienen_asterisco_y_ayuda_semantica(self):
        self.assertIn("Campo obligatorio", self.simulacion)
        for campo in ("fecha_nacimiento", "sexo", "sistema"):
            zona = self.simulacion.split(f'for="{campo}"', 1)[1][:300]
            self.assertIn("required-marker", zona)
            self.assertIn("(obligatorio)", zona)

    def test_cargador_pdf_es_compacto_y_alineado(self):
        self.assertIn("official-import-upload-grid", self.importacion)
        self.assertIn("official-import-upload-action", self.importacion)
        self.assertIn("height: 2.8rem", self.design)
        self.assertNotIn("no intervienen en los motores", self.importacion)

    def test_consentimiento_es_previo_rechazable_y_versionado(self):
        self.assertIn('data-bs-backdrop="static"', self.privacidad_html)
        self.assertIn('id="btn-privacidad-rechazar"', self.privacidad_html)
        self.assertIn('id="btn-privacidad-aceptar"', self.privacidad_html)
        self.assertIn("VERSION_PRIVACIDAD", self.privacidad_js)
        self.assertIn("CLAVE_PRIVACIDAD_SESION", self.privacidad_js)
        self.assertIn("window.sessionStorage.setItem", self.privacidad_js)
        self.assertIn("window.location.replace(\"/\")", self.privacidad_js)
        self.assertIn("window.sessionStorage.removeItem", self.privacidad_js)

    def test_politica_visible_evitar_jerga_tecnica_y_declara_ausencia_de_cookies(self):
        self.assertIn("no utiliza cookies", self.privacidad_html.lower())
        self.assertNotIn("sessionStorage", self.privacidad_html)
        self.assertNotIn("localStorage", self.privacidad_html)
        codigo_js = "\n".join(
            p.read_text(encoding="utf-8")
            for p in (ROOT / "app/static/js").glob("*.js")
        )
        self.assertNotIn("document.cookie", codigo_js)

    def test_fuentes_incorpora_ley_81_decreto_285_y_antai(self):
        self.assertIn('id="privacidad-datos"', self.metodologia)
        self.assertIn("Ley 81 de 2019", self.metodologia)
        self.assertIn("Decreto Ejecutivo 285 de 2021", self.metodologia)
        self.assertIn("antai.gob.pa", self.metodologia)

    def test_nombre_completo_se_descompone_y_de_identifica_apellido_casada(self):
        ref = extraer_referencia_desde_texto(TEXTO_CASADA)
        self.assertEqual(ref.primer_nombre, "Anabel")
        self.assertEqual(ref.segundo_nombre, "Estela")
        self.assertEqual(ref.primer_apellido, "Miranda")
        self.assertEqual(ref.segundo_apellido, "Madrid")
        self.assertEqual(ref.apellido_casada, "Cañizares")
        self.assertEqual(ref.cedula, "4-710-1295")
        self.assertEqual(ref.numero_seguro_social, "2738720")

    def test_mensajes_redundantes_de_preview_fueron_eliminados(self):
        self.assertNotIn("Detectado = proviene del PDF", self.importacion)
        self.assertNotIn("Nombre completo detectado:", self.importacion)
        self.assertNotIn("no se dividió automáticamente", self.importacion)

    def test_hover_de_tablas_tiene_mayor_diferenciacion(self):
        self.assertIn("var(--app-primary) 11%", self.design)
        self.assertIn("box-shadow: inset 3px 0 0 var(--app-primary)", self.design)

    def test_ayuda_contextual_usa_icono_y_se_reposiciona(self):
        self.assertIn("context-help-icon", self.accesibilidad_js)
        self.assertNotIn('<span aria-hidden="true">Info</span>', self.accesibilidad_js)
        self.assertIn("context-help-panel-up", self.accesibilidad_js)
        self.assertIn("context-help-panel-end", self.accesibilidad_js)

    def test_identificacion_agrupa_casada_cedula_y_seguro_social(self):
        self.assertIn('id="apellido-casada-wrapper" class="col-md-6 d-none"', self.simulacion)
        zona = self.simulacion.split('id="apellido-casada-wrapper"', 1)[1][:1200]
        self.assertIn('id="cedula"', zona)
        self.assertIn('id="numero_seguro_social"', zona)

    def test_headers_defensivos_incluyen_csp_y_no_store_para_api(self):
        respuesta = self.client.post("/api/simulacion/cuotas", json={})
        self.assertEqual(respuesta.headers.get("cache-control"), "no-store")
        csp = respuesta.headers.get("content-security-policy", "")
        self.assertIn("default-src 'self'", csp)
        self.assertIn("frame-ancestors 'none'", csp)

    def test_bootstrap_cdn_usa_integridad_subresource(self):
        self.assertIn("sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB", self.base)
        self.assertIn("sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI", self.base)


if __name__ == "__main__":
    unittest.main()
