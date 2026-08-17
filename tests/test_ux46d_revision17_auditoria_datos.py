"""Regresiones UX.4.6d R17 derivadas de la auditoría Paso 1–3."""

import unittest
from pathlib import Path

from app.servicios.referencia_mi_retiro_seguro import extraer_referencia_desde_texto


ROOT = Path(__file__).resolve().parents[1]


TEXTO_AUDITORIA = """
COMPROBANTE DE DECISIÓN DEL PROGRAMA DE INVALIDEZ, VEJEZ Y MUERTE
REGISTRO DE DECISIÓN DEL ASEGURADO
Nombre completo: Anabel Estela Miranda Madrid
Cédula: 4-710-1295
No. Seguro Social: 3759832
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
1992 23 Histórico 356.98 1
2025 56 Histórico 17,760.67 12
2026 57 Histórico + Proyectado 6,659.50 5
2027 58 Proyectado 16,142.63 12
Total de cuotas acumuladas: 293 cuotas
"""


class TestUX46DRevision17AuditoriaDatos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.importacion_js = (
            ROOT / "app/static/js/importacion_datos_oficiales.js"
        ).read_text(encoding="utf-8")
        cls.detalle_js = (
            ROOT / "app/static/js/detalle_anio_actual.js"
        ).read_text(encoding="utf-8")
        cls.css = (
            ROOT / "app/static/css/design-system.css"
        ).read_text(encoding="utf-8")
        cls.parcial = (
            ROOT / "app/templates/partials/importacion_datos_oficiales.html"
        ).read_text(encoding="utf-8")

    def test_checkbox_bloqueado_solo_pinta_gancho_si_valor_real_esta_checked(self):
        bloque = self.css.split("UX.4.6d R17", 1)[1]
        self.assertIn('[data-imported-locked="true"]:checked', bloque)
        self.assertIn('[data-imported-locked="true"]:not(:checked)', bloque)
        self.assertIn("background-image: none !important", bloque)

    def test_preview_mantiene_proyectados_excluidos_por_logica(self):
        self.assertIn('aplicar.checked = registro.tipo === "HISTORICO"', self.importacion_js)
        self.assertIn('aplicar.checked = tipo.value === "HISTORICO"', self.importacion_js)

    def test_parser_advierte_historial_anterior_a_fecha_ingreso_css(self):
        referencia = extraer_referencia_desde_texto(TEXTO_AUDITORIA)
        mensaje = " ".join(referencia.advertencias)
        self.assertIn("historial desde 1992", mensaje)
        self.assertIn("23/07/1997", mensaje)

    def test_parser_no_inventa_apellido_de_casada_si_documento_no_lo_aporta(self):
        referencia = extraer_referencia_desde_texto(TEXTO_AUDITORIA)
        self.assertIsNone(referencia.apellido_casada)

    def test_preview_distingue_cuotas_acreditadas_de_total_con_proyeccion(self):
        self.assertIn('id="preview-comprobante-cuotas-contexto"', self.parcial)
        self.assertIn("cuotas acumuladas al incluir períodos proyectados", self.importacion_js)
        self.assertIn("cuotas ya acreditadas", self.importacion_js)

    def test_preview_distingue_campos_editados_de_campos_detectados(self):
        self.assertIn("camposEditadosPreviewComprobante", self.importacion_js)
        self.assertIn('"Editado por ti"', self.importacion_js)
        self.assertIn('"Completado manualmente"', self.importacion_js)
        self.assertIn("campos_editados_importacion_comprobante", self.importacion_js)
        self.assertIn(".import-field-status.edited", self.css)

    def test_incoherencia_mensual_explica_salario_visible_vs_cuota_acreditada(self):
        self.assertIn("Si un mes tiene salario pero la cuota todavía no aparece acreditada", self.detalle_js)
        self.assertIn("deja su casilla sin marcar", self.detalle_js)
        self.assertIn("revisa el dato del Paso 2", self.detalle_js)


if __name__ == "__main__":
    unittest.main()
