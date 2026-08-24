"""Regresiones de UX.4.6f R1 para procedencia, decisiones y adjuntos."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from app.core.version import version_valida


ROOT = Path(__file__).resolve().parents[1]


def leer(ruta: str) -> str:
    """Lee un archivo del repositorio como UTF-8."""

    return (ROOT / ruta).read_text(encoding="utf-8")


class UX46fR1ConsistenciaProcedenciaAdjuntosTests(unittest.TestCase):
    """Protege el contrato transversal introducido antes de auditar Paso 4."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.simulacion = leer("app/templates/simulation.html")
        cls.historial = leer("app/templates/partials/salary_history.html")
        cls.detalle = leer("app/templates/partials/current_year_detail.html")
        cls.referencia = leer("app/templates/partials/mi_retiro_seguro_reference.html")
        cls.base = leer("app/templates/base.html")
        cls.simulacion_js = leer("app/static/js/simulation.js")
        cls.historial_js = leer("app/static/js/salary_history.js")
        cls.detalle_js = leer("app/static/js/current_year_detail.js")
        cls.importacion_js = leer("app/static/js/official_data_import.js")
        cls.referencia_js = leer("app/static/js/mi_retiro_seguro_reference.js")
        cls.procedencia_js = leer("app/static/js/editable_provenance.js")
        cls.procesamiento_js = leer("app/static/js/attachment_processing.js")
        cls.gestion_js = leer("app/static/js/data_management.js")
        cls.css = leer("app/static/css/editable-provenance.css")
        cls.design_system_css = leer("app/static/css/design-system.css")
        cls.accesibilidad_js = leer("app/static/js/accessibility.js")

    def test_01_cierre_r1_preserva_0_0_26_sin_congelar_version_actual(self):
        version_actual = leer("VERSION").strip()
        self.assertTrue(version_valida(version_actual))
        changelog = leer("CHANGELOG.md")
        self.assertIn(
            "`VERSION` permanece en `0.0.26-beta`; R1 no modifica motores previsionales",
            changelog,
        )
        self.assertIn("v0.0.26-beta", leer("RELEASES.md"))

    def test_02_cuatro_decisiones_del_paso3_comienzan_sin_seleccion(self):
        contratos = (
            (self.historial, 'id="modo_historial"', "Seleccione una opción"),
            (self.detalle, 'id="usar_detalle_anio_actual"', "Seleccione una opción"),
            (self.detalle, 'id="modo_detalle_anio_actual"', "Seleccione una opción"),
            (self.simulacion, 'id="origen_salario_proyeccion"', "Seleccione una opción"),
        )
        for texto, identificador, placeholder in contratos:
            with self.subTest(identificador=identificador):
                inicio = texto.index(identificador)
                bloque = texto[inicio : inicio + 900]
                self.assertIn(placeholder, bloque)
                self.assertIn("required", bloque)

        self.assertNotIn('<option value="MANUAL" selected>', self.historial)
        self.assertNotIn('<option value="false" selected>', self.detalle)
        self.assertNotIn('<option value="MENSUAL" selected>', self.detalle)
        self.assertNotIn('<option value="MANUAL" selected>', self.simulacion)

    def test_03_estado_limpio_no_persiste_decisiones_silenciosas(self):
        for contrato in (
            'modo_historial: ""',
            "origen_historial_anio_inicio: null",
            "detalle_anio_actual_habilitado: null",
            'origen_salario_proyeccion: ""',
            "origen_proyeccion_anio_fin: null",
        ):
            with self.subTest(contrato=contrato):
                self.assertIn(contrato, self.simulacion_js)

        self.assertIn('simulacion.modo_historial = ""', self.gestion_js)
        self.assertIn("simulacion.detalle_anio_actual_habilitado = null", self.gestion_js)
        self.assertIn('simulacion.origen_salario_proyeccion = ""', self.gestion_js)
        self.assertNotIn('origen_salario_proyeccion || "MANUAL"', self.simulacion_js)

    def test_04_continuidad_sugiere_12_solo_como_valor_editable_explicado(self):
        self.assertIn('cierre.value = 12', self.simulacion_js)
        self.assertIn('futuras.value = 12', self.simulacion_js)
        self.assertIn('continua === "true"', self.simulacion_js)
        self.assertIn('id="cuotas-sugerencia-continuidad"', self.simulacion)
        self.assertIn("Son valores editables", self.simulacion)
        self.assertIn("la aplicación sugiere inicialmente 12", self.accesibilidad_js)

    def test_05_anio_inicial_historial_distingue_automatico_y_editado(self):
        self.assertIn('id="origen-historial-anio-inicio"', self.historial)
        self.assertIn("Calculado automáticamente", self.historial)
        self.assertIn('"CALCULADO_AUTOMATICAMENTE"', self.historial_js)
        self.assertIn('"EDITADO_USUARIO"', self.historial_js)
        self.assertIn("actualizarProcedenciaAnioInicioHistorial", self.historial_js)

    def test_06_horizonte_paso4_explica_cinco_anios_y_cambio_de_procedencia(self):
        self.assertIn("const ANIOS_PROYECCION_PREDETERMINADOS = 5", self.simulacion_js)
        self.assertIn("ANIO_ACTUAL\n    + ANIOS_PROYECCION_PREDETERMINADOS", self.simulacion_js)
        self.assertIn('id="origen-proyeccion-anio-fin"', self.simulacion)
        self.assertIn("horizonte inicial sugerido de 5 años", self.simulacion)
        self.assertIn('simulacion.origen_proyeccion_anio_fin = "EDITADO_USUARIO"', self.simulacion_js)
        self.assertIn("calculado automáticamente", self.accesibilidad_js)

    def test_07_procedencia_contempla_los_seis_estados_comunes(self):
        textos = {
            "DETECTADO": "Detectado",
            "EDITADO_USUARIO": "Editado por ti",
            "COMPLETADO_MANUAL": "Completado manualmente",
            "EXCLUIDO_USUARIO": "Excluido por ti",
            "NO_DETECTADO": "No detectado",
            "CALCULADO_AUTOMATICAMENTE": "Calculado automáticamente",
        }
        for codigo, etiqueta in textos.items():
            with self.subTest(codigo=codigo):
                self.assertIn(f'{codigo}: "{etiqueta}"', self.procedencia_js)
        self.assertIn('CALCULADO_AUTOMATICAMENTE: "automatic"', self.procedencia_js)

    def test_08_iconografia_de_procedencia_conserva_simbolos_semanticos(self):
        for icono in ('content: "✓"', 'content: "✎"', 'content: "⊘"',
                      'content: "!"', 'content: "↳"'):
            with self.subTest(icono=icono):
                self.assertIn(icono, self.css)
        css_procedencia = self.design_system_css + self.css
        self.assertNotIn('content: "●"', css_procedencia)
        self.assertIn("border-radius: 0 !important", self.css)
        self.assertIn("display: inline-flex", self.css)
        self.assertIn("justify-content: center", self.css)

    def test_09_avisos_amarillos_describen_solo_las_acciones_activas(self):
        for mensaje in (
            "Completaste manualmente información que el documento no detectó.",
            "Editaste información importada para esta simulación.",
            "Excluiste información importada de esta simulación.",
        ):
            with self.subTest(mensaje=mensaje):
                self.assertIn(mensaje, self.procedencia_js)
        self.assertIn("function mensajeAjusteContextual(acciones)", self.procedencia_js)
        self.assertNotIn("Has ajustado, completado o excluido", self.procedencia_js)

    def test_10_helper_global_de_adjuntos_carga_antes_de_scripts_de_pagina(self):
        helper = self.base.index("/js/attachment_processing.js")
        bloque_pagina = self.base.index("{% block scripts %}")
        self.assertLess(helper, bloque_pagina)

    def test_11_helper_de_adjuntos_expone_estado_accesible_y_antiduplicado(self):
        for contrato in (
            "Analizando documento… Esto puede tardar unos segundos.",
            "spinner-border spinner-border-sm me-2",
            'estado.setAttribute("role", "status")',
            'estado.setAttribute("aria-live", "polite")',
            'estado.setAttribute("aria-atomic", "true")',
            'estado.setAttribute("aria-busy", "true")',
            'boton.dataset.procesandoAdjunto = "true"',
            "if (!boton || estaActivo(boton))",
            "boton.disabled = true",
            "input.disabled = true",
            "input.disabled = inputDeshabilitadoOriginal",
        ):
            with self.subTest(contrato=contrato):
                self.assertIn(contrato, self.procesamiento_js)

    def test_12_tres_analizadores_reutilizan_inicio_y_finalizacion_global(self):
        self.assertEqual(
            self.importacion_js.count("window.ProcesamientoAdjuntos.iniciar({"),
            2,
        )
        self.assertEqual(
            self.importacion_js.count("window.ProcesamientoAdjuntos.finalizar(procesamiento);"),
            2,
        )
        self.assertEqual(
            self.referencia_js.count("window.ProcesamientoAdjuntos.iniciar({"),
            1,
        )
        self.assertEqual(
            self.referencia_js.count("window.ProcesamientoAdjuntos.finalizar(procesamiento);"),
            1,
        )

    def test_13_todos_los_inputs_de_archivo_actuales_estan_cubiertos(self):
        plantillas = list((ROOT / "app/templates").rglob("*.html"))
        ids_archivo: set[str] = set()
        patron = re.compile(r'<input\b(?=[^>]*\btype="file")(?=[^>]*\bid="([^"]+)")[^>]*>', re.I)
        for plantilla in plantillas:
            ids_archivo.update(patron.findall(plantilla.read_text(encoding="utf-8")))

        self.assertEqual(
            ids_archivo,
            {
                "import-comprobante-pdf",
                "import-ficha-digital-pdf",
                "referencia-mi-retiro-pdf",
            },
        )
        codigo_analizadores = self.importacion_js + self.referencia_js
        for identificador in ids_archivo:
            with self.subTest(identificador=identificador):
                self.assertIn(f'getElementById("{identificador}")', codigo_analizadores)
        self.assertIn('id="estado-procesamiento-referencia-mi-retiro"', self.referencia)

    def test_14_listener_y_documentacion_r1_quedan_trazados(self):
        self.assertIn(
            'document.getElementById("btn-revisar-detalle-importado")?.addEventListener(\n    "click",\n    () =>',
            self.detalle_js,
        )
        self.assertNotIn('addEventListener(\n    "click",\n    "click",', self.detalle_js)

        decisiones = leer("docs/decisions/README.md")
        especificacion = leer("docs/product/functional-specification.md")
        matriz = leer("docs/product/traceability-matrix.md")
        roadmap = leer("docs/governance/roadmap.md")
        changelog = leer("CHANGELOG.md")
        self.assertIn("## ADR-169 —", decisiones)
        self.assertIn("## ADR-170 —", decisiones)
        for rf in range(337, 351):
            with self.subTest(rf=rf):
                self.assertIn(f"**RF-{rf}.**", especificacion)
        self.assertIn("| TR-017 |", matriz)
        self.assertIn("| TR-018 |", matriz)
        self.assertIn("UX.4.6f", roadmap)
        self.assertIn("R1/R1.1", roadmap)
        self.assertIn("### UX.4.6f R1 — consistencia de procedencia", changelog)


if __name__ == "__main__":
    unittest.main()
