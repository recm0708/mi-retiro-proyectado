"""Regresiones de UX.4.6b para Simular / Paso 1 — Datos personales."""

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.services.mi_retiro_seguro_reference import extraer_referencia_desde_texto


ROOT = Path(__file__).resolve().parents[1]


TEXTO_IDENTIFICADO = """
COMPROBANTE DE DECISIÓN DEL PROGRAMA DE INVALIDEZ, VEJEZ Y MUERTE
REGISTRO DE DECISIÓN DEL ASEGURADO
Primer Nombre: ANA
Segundo Nombre: MARÍA
Primer Apellido: PÉREZ
Segundo Apellido: LÓPEZ
Apellido de Casada: DE RIVERA
Cédula: 8-123-456
Número de Seguro Social: 123-4567
Fecha de Comprobante: 10/08/2026
Fecha de Nacimiento: 16/11/1969
Sexo: Femenino
Fecha de Ingreso CSS: 23/07/1997
Total cuotas históricas aportadas a la fecha: 281
PROYECCIÓN Y DECISIÓN
Edad de retiro elegida: 57 años
Prestación esperada: PENSIÓN MENSUAL VITALICIA
Monto estimado de prestación: B/. 741.59
Sistema elegido: Subsistema Exclusivo de Beneficio Definido (SEBD)
1992 23 Histórico 356.98 1
Total de cuotas acumuladas: 281 cuotas
"""


TEXTO_NOMBRE_COMPLETO = """
COMPROBANTE DE DECISIÓN DEL PROGRAMA DE INVALIDEZ, VEJEZ Y MUERTE
Nombre completo: ANA MARÍA DEL CARMEN PÉREZ LÓPEZ
Fecha de Comprobante: 10/08/2026
Fecha de Nacimiento: 16/11/1969
Sexo: Femenino
Fecha de Ingreso CSS: 23/07/1997
Total cuotas históricas aportadas a la fecha: 281
Edad de retiro elegida: 57 años
Prestación esperada: PENSIÓN MENSUAL VITALICIA
Monto estimado de prestación: B/. 741.59
Sistema elegido: Subsistema Exclusivo de Beneficio Definido (SEBD)
Total de cuotas acumuladas: 281 cuotas
"""


class TestUX46bPaso1DatosPersonales(unittest.TestCase):
    """Protege el nuevo flujo manual/PDF y la navegación no flotante."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(app)
        cls.simulacion = (ROOT / "app/templates/simulation.html").read_text(encoding="utf-8")
        cls.comprobante = (
            ROOT / "app/templates/partials/official_data_import.html"
        ).read_text(encoding="utf-8")
        cls.ficha = (
            ROOT / "app/templates/partials/ficha_digital_import.html"
        ).read_text(encoding="utf-8")
        cls.detalle = (
            ROOT / "app/templates/partials/current_year_detail.html"
        ).read_text(encoding="utf-8")
        cls.simulacion_js = (ROOT / "app/static/js/simulation.js").read_text(encoding="utf-8")
        cls.importacion_js = (
            ROOT / "app/static/js/official_data_import.js"
        ).read_text(encoding="utf-8")
        cls.navegacion_js = (
            ROOT / "app/static/js/wizard_navigation.js"
        ).read_text(encoding="utf-8")
        cls.privacidad = (
            ROOT / "app/templates/partials/privacy_consent.html"
        ).read_text(encoding="utf-8")
        cls.design = (ROOT / "app/static/css/design-system.css").read_text(encoding="utf-8")

    def test_simulacion_responde_con_modalidad_manual_por_defecto(self):
        self.assertIn(
            "¿Cómo quieres preparar tu simulación?",
            self.simulacion,
        )

        self.assertIn(
            'data-simulation-mode-choice="MANUAL"',
            self.simulacion,
        )

        self.assertIn(
            'data-simulation-mode-choice="ASISTIDO"',
            self.simulacion,
        )

        self.assertIn(
            'id="simulation-workspace"',
            self.simulacion,
        )

        position = self.simulacion.index(
            'id="simulation-workspace"'
        )

        fragment = self.simulacion[
            max(
                0,
                position - 100,
            ):
            position + 200
        ]

        self.assertIn(
            'class="d-none"',
            fragment,
        )

        self.assertIn(
            "hidden",
            fragment,
        )

    def test_paso_uno_agrega_identificacion_opcional_sin_usarla_como_requisito(self):
        for identificador in (
            "primer_nombre",
            "segundo_nombre",
            "primer_apellido",
            "segundo_apellido",
            "apellido_casada",
            "cedula",
            "numero_seguro_social",
        ):
            self.assertIn(f'id="{identificador}"', self.simulacion)
        self.assertIn("Los datos de identificación son opcionales", self.simulacion)
        self.assertNotIn('id="primer_nombre" maxlength="80" required', self.simulacion)

    def test_apellido_casada_es_condicional_para_sexo_femenino(self):
        self.assertIn('id="apellido-casada-wrapper" class="col-md-6 d-none"', self.simulacion)
        self.assertIn('const mostrar = sexo === "F"', self.importacion_js)
        self.assertIn('actualizarApellidoCasada()', self.importacion_js)

    def test_manual_y_pdf_son_modalidades_mutuamente_excluyentes(self):
        mode = (
            ROOT
            / "app/static/js/simulation_mode.js"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'data-simulation-mode-choice="MANUAL"',
            self.simulacion,
        )

        self.assertIn(
            'data-simulation-mode-choice="ASISTIDO"',
            self.simulacion,
        )

        self.assertIn(
            "aplicarVisibilidadModalidad",
            mode,
        )

        self.assertNotIn(
            "seccion-importacion-comprobante",
            self.importacion_js,
        )

        self.assertNotIn(
            'input[name="modo_datos_personales"]',
            self.simulacion,
        )

    def test_ficha_digital_sale_del_paso_uno_y_se_ubica_en_historial(self):
        paso1 = self.simulacion.split(
            'data-panel="1"',
            1,
        )[1].split(
            'data-panel="2"',
            1,
        )[0]

        paso3 = self.simulacion.split(
            'data-panel="3"',
            1,
        )[1].split(
            'data-panel="4"',
            1,
        )[0]

        assisted = (
            ROOT
            / "app/templates/partials/assisted_preparation.html"
        ).read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            "ficha_digital_import.html",
            paso1,
        )

        self.assertIn(
            "current_year_detail.html",
            paso3,
        )

        self.assertNotIn(
            "ficha_digital_import.html",
            self.detalle,
        )

        self.assertIn(
            "partials/ficha_digital_import.html",
            assisted,
        )

    def test_navegacion_comun_tiene_barra_superior_e_inferior(self):
        self.assertLess(
            self.simulacion.index('id="wizard-sticky-nav"'),
            self.simulacion.index('data-panel="1"'),
        )
        self.assertGreater(
            self.simulacion.index('id="wizard-navigation-bottom"'),
            self.simulacion.index('partials/results.html'),
        )
        self.assertIn('data-wizard-nav="top"', self.simulacion)
        self.assertIn('data-wizard-nav="bottom"', self.simulacion)
        self.assertIn(".wizard-navigation-bar-top", self.design)
        self.assertIn("position: sticky;", self.design)

    def test_paso_uno_elimina_acciones_duplicadas_dentro_del_formulario(self):
        paso1 = self.simulacion.split('data-panel="1"', 1)[1].split('data-panel="2"', 1)[0]
        self.assertNotIn("wizard-actions", paso1)
        self.assertNotIn(">Volver<", paso1.replace("\n", ""))
        self.assertIn('id="wizard-sticky-primary"', self.simulacion)

    def test_modal_comprobante_inicia_en_revision_y_solo_edita_por_decision(self):
        self.assertIn("Vista previa del documento", self.comprobante)
        self.assertIn("Modo revisión", self.comprobante)
        self.assertIn('id="btn-editar-import-comprobante"', self.comprobante)
        self.assertIn("Editar campos", self.comprobante)
        self.assertIn("Importar datos", self.comprobante)
        self.assertIn("establecerEdicionPreviewComprobante(false)", self.importacion_js)
        self.assertIn("control.readOnly = !habilitada", self.importacion_js)
        self.assertIn("control.disabled = !habilitada", self.importacion_js)

    def test_importacion_requiere_pdf_confirmado_antes_de_continuar(self):
        self.assertIn('modoDatos === "MI_RETIRO_SEGURO" && !importacionLista', self.navegacion_js)
        self.assertIn('etiqueta: "Importa datos para continuar"', self.navegacion_js)
        self.assertIn("deshabilitado: true", self.navegacion_js)
        self.assertIn("La importación no completó toda la información previsional obligatoria", self.simulacion_js)

    def test_parser_extrae_identificadores_solo_cuando_estan_etiquetados(self):
        referencia = extraer_referencia_desde_texto(TEXTO_IDENTIFICADO)
        self.assertEqual(referencia.primer_nombre, "ANA")
        self.assertEqual(referencia.segundo_nombre, "MARÍA")
        self.assertEqual(referencia.primer_apellido, "PÉREZ")
        self.assertEqual(referencia.segundo_apellido, "LÓPEZ")
        self.assertEqual(referencia.apellido_casada, "DE RIVERA")
        self.assertEqual(referencia.cedula, "8-123-456")
        self.assertEqual(referencia.numero_seguro_social, "123-4567")

    def test_parser_divide_nombre_completo_de_forma_revisable(self):
        referencia = extraer_referencia_desde_texto(TEXTO_NOMBRE_COMPLETO)
        self.assertEqual(referencia.primer_nombre, "ANA")
        self.assertEqual(referencia.segundo_nombre, "MARÍA DEL CARMEN")
        self.assertEqual(referencia.primer_apellido, "PÉREZ")
        self.assertEqual(referencia.segundo_apellido, "LÓPEZ")
        self.assertNotIn("Nombre completo detectado:", self.comprobante)

    def test_origen_persona_distingue_manual_importado_y_editado(self):
        self.assertIn('origen_persona: "MANUAL"', self.simulacion_js)
        self.assertIn('"MI_RETIRO_SEGURO_EDITADO"', self.importacion_js)
        self.assertIn('"MI_RETIRO_SEGURO"', self.importacion_js)
        self.assertIn("previewComprobanteFueEditado", self.importacion_js)

    def test_privacidad_se_centraliza_en_consentimiento_y_sale_del_cargador(self):
        self.assertNotIn("no intervienen en los motores", self.comprobante)
        self.assertIn("Consulta cómo protegemos y utilizamos tus datos", self.comprobante)
        self.assertIn("Términos, privacidad y tratamiento de datos", self.privacidad)
        self.assertIn("Ley 81 de 2019", self.privacidad)
        self.assertIn("Decreto Ejecutivo 285 de 2021", self.privacidad)


if __name__ == "__main__":
    unittest.main()
