"""Regresiones UX.4.4 para importación revisable de documentos oficiales."""

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.servicios.ficha_digital import extraer_ficha_digital_desde_texto


ROOT = Path(__file__).resolve().parents[1]


TEXTO_FICHA = """
FICHA DIGITAL
SALARIOS DEL ÚLTIMO AÑO
2026-Junio 1110.00
2026-Mayo 1100.00
2026-Abril 1090.00
2026-Marzo 1080.00
2026-Febrero 1070.00
2026-Enero 1060.00
2025-Diciembre 1050.00
2025-Noviembre 1040.00
2025-Octubre 1030.00
2025-Septiembre 1020.00
2025-Agosto 1010.00
2025-Julio 1000.00
"""


class TestUX44ImportacionOficial(unittest.TestCase):
    """Protege vista previa editable, confirmación explícita e importación salarial."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(app)
        cls.simulacion = (ROOT / "app/templates/simulacion.html").read_text(encoding="utf-8")
        cls.parcial = (
            ROOT / "app/templates/partials/importacion_datos_oficiales.html"
        ).read_text(encoding="utf-8")
        cls.js = (
            ROOT / "app/static/js/importacion_datos_oficiales.js"
        ).read_text(encoding="utf-8")
        cls.css = (ROOT / "app/static/css/style.css").read_text(encoding="utf-8")
        cls.main = (ROOT / "app/main.py").read_text(encoding="utf-8")

    def test_ficha_digital_extrae_solo_salarios_del_anio_actual(self):
        resumen = extraer_ficha_digital_desde_texto(
            TEXTO_FICHA,
            anio_actual=2026,
        )

        self.assertEqual(len(resumen.registros), 6)
        self.assertTrue(all(registro.anio == 2026 for registro in resumen.registros))
        self.assertEqual(resumen.registros[0].mes, 1)
        self.assertEqual(resumen.registros[-1].mes, 6)
        self.assertEqual(resumen.registros[-1].salario, 1110.0)
        self.assertEqual(resumen.anio_mas_reciente, 2026)
        self.assertEqual(resumen.mes_mas_reciente, 6)

    def test_ficha_digital_rechaza_documento_ajeno(self):
        with self.assertRaises(ValueError):
            extraer_ficha_digital_desde_texto("Listado cualquiera 2026-Enero 1000.00")

    def test_endpoint_ficha_rechaza_archivo_no_pdf(self):
        respuesta = self.cliente.post(
            "/api/simulacion/ficha-digital",
            files={"archivo": ("ficha.txt", b"texto", "text/plain")},
        )
        self.assertEqual(respuesta.status_code, 415)

    def test_importadores_estan_en_paso_uno_y_referencia_sale_del_paso_tres(self):
        posicion_paso_1 = self.simulacion.index('data-panel="1"')
        posicion_importacion = self.simulacion.index('partials/importacion_datos_oficiales.html')
        posicion_paso_2 = self.simulacion.index('data-panel="2"')

        self.assertLess(posicion_paso_1, posicion_importacion)
        self.assertLess(posicion_importacion, posicion_paso_2)
        self.assertNotIn('partials/referencia_mi_retiro_seguro.html', self.simulacion)

    def test_interfaz_exige_revision_y_confirmacion_antes_de_aplicar(self):
        self.assertIn("Ningún dato se aplica automáticamente", self.parcial)
        self.assertIn('id="modal-import-comprobante"', self.parcial)
        self.assertIn('id="modal-import-ficha-digital"', self.parcial)
        self.assertIn("Confirmar y aplicar datos", self.parcial)
        self.assertIn("Confirmar y aplicar salarios", self.parcial)
        self.assertIn("Corrige cualquier dato antes de confirmar", self.parcial)

    def test_comprobante_puede_rellenar_persona_cuotas_historial_y_referencia(self):
        self.assertIn("simulacion.persona =", self.js)
        self.assertIn("cuotas_totales: referencia.cuotas_historicas", self.js)
        self.assertIn("simulacion.historial =", self.js)
        self.assertIn("simulacion.referencia_mi_retiro_seguro = referencia", self.js)
        self.assertIn("aplicar_historial", self.js)
        self.assertIn('registro.tipo === "HISTORICO"', self.js)

    def test_filas_proyectadas_no_se_importan_como_historial_real_por_defecto(self):
        self.assertIn('aplicar.checked = registro.tipo === "HISTORICO"', self.js)
        self.assertIn('if (tipo.value === "PROYECTADO") aplicar.checked = false', self.js)

    def test_ficha_no_inventa_cuotas_y_solo_aplica_anio_actual_al_detalle(self):
        self.assertIn('cuota.type = "checkbox"', self.js)
        self.assertIn("La importación no marca cuotas por su cuenta", self.parcial)
        self.assertIn('registros.filter((registro) => registro.anio === ANIO_ACTUAL)', self.js)
        self.assertIn('modo_captura: "MENSUAL"', self.js)
        self.assertIn("detalle_anio_actual_habilitado = true", self.js)
        self.assertIn("cuotas_anio_actual: cuotasConfirmadas", self.js)
        self.assertNotIn("preview-ficha-anio", self.js)
        self.assertIn("preview-ficha-mes", self.js)

    def test_input_file_corrige_hueco_inferior_y_modal_responde_a_temas(self):
        self.assertIn(".official-import-file-input {", self.css)
        self.assertIn("padding: 0;", self.css)
        self.assertIn("::file-selector-button", self.css)
        self.assertIn(".official-import-modal", self.css)
        self.assertIn('html[data-app-theme="contrast"] .official-import-card', self.css)


    def test_ficha_digital_no_conserva_periodos_de_anios_anteriores(self):
        resumen = extraer_ficha_digital_desde_texto(
            TEXTO_FICHA,
            anio_actual=2026,
        )

        self.assertNotIn(2025, {registro.anio for registro in resumen.registros})
        self.assertIn("Solo se muestran y conservan", self.parcial)
        self.assertNotIn("se conservan como contexto", self.parcial)

    def test_ficha_digital_avisa_si_no_hay_salarios_del_anio_actual(self):
        with self.assertRaisesRegex(ValueError, "año actual 2027"):
            extraer_ficha_digital_desde_texto(
                TEXTO_FICHA,
                anio_actual=2027,
            )

    def test_monedas_de_vista_previa_usan_separador_de_miles_y_dos_decimales(self):
        self.assertIn('class="form-control money-input"', self.parcial)
        self.assertIn('preview-comprobante-salario money-input', self.js)
        self.assertIn('preview-ficha-salario money-input', self.js)
        self.assertIn("formatearNumeroMonetario(registro.salario_anual)", self.js)
        self.assertIn("formatearNumeroMonetario(registro.salario)", self.js)
        self.assertIn("obtenerValorMonetario", self.js)

    def test_preview_ficha_se_limita_al_anio_actual_y_elimina_columnas_redundantes(self):
        self.assertIn("registro.anio === ANIO_ACTUAL", self.js)
        ficha_modal = self.parcial.split('id="modal-import-ficha-digital"', 1)[1]
        self.assertNotIn('<th scope="col">Año</th>', ficha_modal)
        self.assertNotIn('<th scope="col">Aplicación</th>', ficha_modal)
        self.assertNotIn('aplicacion.textContent = "Contexto"', self.js)

    def test_simulacion_carga_modulo_y_backend_expone_ficha(self):
        respuesta = self.cliente.get("/simulacion")
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("importacion_datos_oficiales.js", respuesta.text)
        self.assertIn("Importar datos oficiales", respuesta.text)
        self.assertIn('/api/simulacion/ficha-digital', self.main)


if __name__ == "__main__":
    unittest.main()
