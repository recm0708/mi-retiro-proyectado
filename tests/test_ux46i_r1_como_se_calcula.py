"""Regresiones para la guía pública de transparencia del cálculo."""

from pathlib import Path
import unittest

from fastapi.testclient import TestClient

from app.core.normativa import (
    cargar_parametros_generales,
    cargar_parametros_mixto,
    cargar_parametros_sebd,
    cargar_parametros_sucgs,
)
from app.main import app
from app.services.como_se_calcula import construir_guia_calculo


ROOT = Path(__file__).resolve().parents[1]


class TestUX46iR1ComoSeCalcula(unittest.TestCase):
    """Protege el contrato público sin duplicar los motores previsionales."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(app)
        cls.respuesta = cls.cliente.get("/como-se-calcula")
        cls.html = cls.respuesta.text
        cls.servicio = (ROOT / "app/services/como_se_calcula.py").read_text(
            encoding="utf-8"
        )
        cls.plantilla = (ROOT / "app/templates/como_se_calcula.html").read_text(
            encoding="utf-8"
        )
        cls.css = (ROOT / "app/static/css/como-se-calcula.css").read_text(
            encoding="utf-8"
        )
        cls.resultados = (
            ROOT / "app/static/js/results_orchestration.js"
        ).read_text(encoding="utf-8")
        cls.metodologia = (ROOT / "app/templates/metodologia.html").read_text(
            encoding="utf-8"
        )

    def test_01_ruta_publica_renderiza_sin_simulacion(self):
        self.assertEqual(200, self.respuesta.status_code)
        self.assertIn("Cómo se calcula una estimación de retiro", self.html)
        self.assertIn("Esta página explica el procedimiento sin modificar tu simulación.", self.html)
        self.assertIn("Gaceta Oficial 30284-B · 22/05/2025", self.html)
        self.assertNotIn("texto_unico_ley_51_reformas_hasta_ley_462_2025", self.html)

    def test_02_guia_cubre_los_tres_sistemas_y_flujo_general(self):
        for ancla in ('id="sebd"', 'id="mixto"', 'id="sucgs"'):
            self.assertIn(ancla, self.html)
        for texto in (
            "Datos personales",
            "Cuotas",
            "Historial salarial",
            "Proyección",
            "Retiro",
            "Resultado",
        ):
            self.assertIn(texto, self.html)

    def test_03_parametros_generales_y_sebd_provienen_de_normativa(self):
        guia = construir_guia_calculo()
        generales = cargar_parametros_generales()
        sebd = cargar_parametros_sebd()["pension_vejez"]

        self.assertEqual(generales["edades_referencia"], guia["edades_referencia"])
        self.assertEqual(sebd["cuotas_referencia"], guia["sebd"]["cuotas_referencia"])
        self.assertEqual(
            sebd["tasa_reemplazo_base_pct"],
            guia["sebd"]["tasa_base_pct"],
        )
        self.assertEqual(24, len(guia["sebd"]["factores_anticipacion"]))

    def test_04_capa_explicativa_no_importa_ni_ejecuta_motores(self):
        self.assertNotIn("app.engines", self.servicio)
        self.assertNotIn("calcular_sebd", self.servicio)
        self.assertNotIn("calcular_mixto", self.servicio)
        self.assertNotIn("calcular_sucgs", self.servicio)
        self.assertIn("cargar_parametros_sebd", self.servicio)
        self.assertIn("cargar_parametros_mixto", self.servicio)
        self.assertIn("cargar_parametros_sucgs", self.servicio)

    def test_05_sebd_explica_modalidades_formula_factores_y_indemnizacion(self):
        for texto in (
            "Pensión mensual sin factor proporcional",
            "Proporcional anticipada",
            "monto inicial = salario base × tasa de reemplazo",
            "proporcional = monto previo × (cuotas ÷",
            "Ver tabla mensual de reducción anticipada",
            "pago único = mensualidad hipotética × factor",
        ):
            self.assertIn(texto, self.html)

    def test_06_sebd_publica_maximos_desde_parametros_versionados(self):
        guia = construir_guia_calculo()
        maximos = guia["sebd"]["maximos"]
        self.assertEqual([1500.0, 2000.0, 2500.0], [x["monto_maximo"] for x in maximos])
        self.assertEqual([10, 15, 20], [x["mejores_anios"] for x in maximos])
        self.assertIn("Máximos SEBD versionados", self.html)

    def test_07_mixto_explica_bd_cap_decision_y_transicion_versionada(self):
        guia = construir_guia_calculo()
        mixto = cargar_parametros_mixto()
        self.assertEqual(
            mixto["transicion"]["fecha_inicio_calculo_bajo_sucgs"],
            guia["mixto"]["fecha_inicio_sucgs"],
        )
        for texto in (
            "Componente BD",
            "Componente CAP",
            "CAP mensual = (saldo CAP + bono aplicable) ÷ valor actuarial",
            "decisión explícita",
            "Inicio del cálculo bajo SUCGS",
        ):
            self.assertIn(texto, self.html)

    def test_08_ejemplo_mixto_identifica_divisor_hipotetico(self):
        self.assertIn("divisor actuarial 250.0000", self.html)
        self.assertIn(
            "únicamente ilustrativo; no representa un parámetro actuarial oficial vigente",
            self.html,
        )

    def test_09_sucgs_explica_componente_contributivo_y_tabla_actuarial(self):
        guia = construir_guia_calculo()
        sucgs = cargar_parametros_sucgs()
        self.assertEqual(
            sucgs["componente_contributivo"]["divisor_formula"],
            guia["sucgs"]["divisor"],
        )
        self.assertEqual(46, len(guia["sucgs"]["factores"]))
        self.assertIn("pensión contributiva = saldo ÷ 1000 × factor actuarial por edad", self.html)
        self.assertIn("Ver factores actuariales SUCGS por edad", self.html)

    def test_10_sucgs_distingue_referencias_solidarias_y_articulo_197(self):
        for texto in (
            "Valor mínimo universal de referencia",
            "Pensión Garantizada Solidaria de referencia",
            "Garantía de reemplazo mínimo del artículo 197",
            "estabilidad salarial no se presume automáticamente",
        ):
            self.assertIn(texto, self.html)

    def test_11_paso6_enlaza_guia_por_sistema_sin_datos_personales(self):
        self.assertIn('id="resultado-ver-como-se-calcula"', self.resultados)
        self.assertIn('SEBD: "sebd"', self.resultados)
        self.assertIn('MIXTO: "mixto"', self.resultados)
        self.assertIn('SUCGS: "sucgs"', self.resultados)
        self.assertIn("/como-se-calcula#${ancla}", self.resultados)
        self.assertNotIn("fecha_nacimiento=", self.resultados)
        self.assertNotIn("salario=", self.resultados)

    def test_12_metodologia_ofrece_entrada_visible_a_la_guia(self):
        self.assertIn('href="/como-se-calcula"', self.metodologia)
        self.assertIn("Ver cómo se calcula", self.metodologia)
        self.assertIn("fórmulas, variables, requisitos", self.metodologia)

    def test_13_estructura_es_accesible_responsive_y_compatible_con_temas(self):
        self.assertIn('aria-label="Contenido de Cómo se calcula"', self.plantilla)
        self.assertIn("<details", self.plantilla)
        self.assertIn("scroll-margin-top", self.css)
        self.assertIn("@media (max-width: 575.98px)", self.css)
        self.assertIn('html[data-app-theme="contrast"]', self.css)
        self.assertIn("var(--app-text)", self.css)
        self.assertIn("var(--app-surface)", self.css)

    def test_14_documentacion_traza_adr_rf_tr_y_estado_r1(self):
        decisiones = (ROOT / "docs/DECISIONES.md").read_text(encoding="utf-8")
        especificacion = (ROOT / "docs/ESPECIFICACION_FUNCIONAL.md").read_text(
            encoding="utf-8"
        )
        matriz = (ROOT / "docs/MATRIZ_TRAZABILIDAD.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs/ROADMAP.md").read_text(encoding="utf-8")
        plan = (ROOT / "docs/PLAN_MAESTRO_HACIA_1_0.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

        self.assertIn("## ADR-178 —", decisiones)
        for rf in range(383, 390):
            self.assertIn(f"**RF-{rf}.**", especificacion)
        self.assertIn("| TR-026 |", matriz)
        self.assertIn("UX.4.6i", readme)
        self.assertIn("**841 pruebas**", readme)
        self.assertIn("R1.4", roadmap)
        self.assertIn("**841 pruebas**", roadmap)
        self.assertIn("R1.2", plan)
        self.assertIn("R1.3", plan)
        self.assertIn("R1.4", plan)
        self.assertNotIn("UX.4.6i R1.1", plan)
        self.assertIn("### UX.4.6i R1 —", changelog)
        self.assertIn("### UX.4.6i — cierre de Cómo se calcula", changelog)
        self.assertTrue((ROOT / "docs/COMO_SE_CALCULA.md").exists())
        self.assertTrue((ROOT / "docs/UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md").exists())

    def test_15_navbar_ofrece_acceso_directo_y_estado_activo(self):
        base = (ROOT / "app/templates/base.html").read_text(encoding="utf-8")
        main = (ROOT / "app/main.py").read_text(encoding="utf-8")
        self.assertIn('href="/como-se-calcula"', base)
        self.assertIn("Cómo se calcula", base)
        self.assertIn("pagina_activa == 'como_se_calcula'", base)
        self.assertIn('"pagina_activa": "como_se_calcula"', main)
        self.assertIn('aria-current="page"', self.html)

    def test_16_flujo_detalla_transformacion_de_datos_pasos_1_a_6(self):
        for texto in (
            "Cómo se transforman tus datos de los Pasos 1 al 6",
            "cuotas proyectadas al cierre = cuotas acreditadas totales",
            "salario anual = mensual × 12 = quincenal × 24 = semanal × 52",
            "salario cotizado proyectado = salario anual proyectado × cuotas esperadas ÷ 12",
            "cuotas estimadas al retiro = cuotas acreditadas + cuotas adicionales estimadas",
            "modalidad → cálculo del sistema",
        ):
            self.assertIn(texto, self.html)

    def test_17_guia_no_expone_lenguaje_de_implementacion_en_alerta_principal(self):
        self.assertNotIn("motores Python", self.html)
        self.assertNotIn("sessionStorage", self.html)
        self.assertNotIn("app/services", self.html)
        self.assertIn("Ver cálculo completo", self.html)

    def test_18_importes_visibles_usan_separador_de_miles_y_dos_decimales(self):
        for importe in (
            "B/.1,500.00",
            "B/.2,000.00",
            "B/.2,500.00",
            "B/.24,000.00",
            "B/.100,000.00",
        ):
            self.assertIn(importe, self.html)
        self.assertNotIn("B/.24000.00", self.html)
        self.assertNotIn("B/.100000.00", self.html)

    def test_19_tablas_de_factores_reducen_filas_en_escritorio(self):
        self.assertIn("calculation-guide-factor-grid-anticipada", self.plantilla)
        self.assertIn("calculation-guide-factor-grid-sucgs", self.plantilla)
        self.assertIn("repeat(8, minmax(0, 1fr))", self.css)
        self.assertIn("repeat(10, minmax(0, 1fr))", self.css)
        self.assertIn("(24 factores)", self.html)
        self.assertIn("(35 a 80+)", self.html)

    def test_20_refinamiento_visual_usa_tokens_y_responde_a_los_tres_temas(self):
        self.assertIn("var(--app-primary)", self.css)
        self.assertIn("var(--app-surface-soft)", self.css)
        self.assertIn("var(--app-focus)", self.css)
        self.assertIn('html[data-app-theme="contrast"]', self.css)
        self.assertIn("@media (max-width: 1199.98px)", self.css)
        self.assertNotIn("background: #", self.css)

    def test_21_terminos_generales_se_definen_en_contexto(self):
        for texto in (
            "Términos que conviene distinguir",
            "Cuota acreditada",
            "Cuota proyectada",
            "Salario cotizado",
            "Fecha de corte",
        ):
            self.assertIn(texto, self.html)

    def test_22_mixto_expande_siglas_y_conceptos_clave(self):
        for texto in (
            "Qué significan los términos del Subsistema Mixto",
            "Beneficio Definido",
            "Componente de Ahorro Personal",
            "Saldo CAP",
            "Tasa resultante",
            "Pensión programada CAP",
            "Valor actuarial",
            "Prestación Mixto",
        ):
            self.assertIn(texto, self.html)

    def test_23_sucgs_define_terminologia_solidaria_y_actuarial(self):
        for texto in (
            "Qué significan los términos de SUCGS",
            "Capitalización Solidaria",
            "Componente contributivo",
            "Factor actuarial",
            "Capa solidaria",
            "PGS",
            "Garantía de reemplazo mínimo",
            "Salario promedio base",
        ):
            self.assertIn(texto, self.html)

    def test_24_formulas_conservan_regla_y_anaden_sustitucion_numerica(self):
        self.assertGreaterEqual(self.plantilla.count("calculation-guide-example-label"), 28)
        for texto in (
            "edad = años transcurridos desde el nacimiento",
            "21/08/2026 − 16/11/1974 = 51 años",
            "B/.1,500.00 × 12 = B/.18,000.00",
            "B/.1,500.00 × 62.50 % = B/.937.50",
            "(B/.24,000.00 + B/.1,000.00) ÷ 250.0000 = B/.100.00",
            "B/.100,000.00 ÷ 1000 × 5.15 = B/.515.00",
        ):
            self.assertIn(texto, self.html)

    def test_25_guia_expone_tasa_equivalente_y_fraccion_de_anio(self):
        self.assertIn("tasa equivalente = ((salario futuro ÷ salario actual)", self.html)
        self.assertIn("6.2659 % anual equivalente", self.html)
        self.assertIn("cuotas de una fracción de año", self.html)
        self.assertIn("parte entera(6 × 12 ÷ 12) = 6 cuotas", self.html)

    def test_26_espaciado_separa_titulo_tabla_ejemplo_y_fuentes(self):
        self.assertIn("calculation-guide-table-title", self.plantilla)
        self.assertIn("margin: 1.9rem 0 1rem;", self.css)
        self.assertIn("calculation-guide-example-note", self.plantilla)
        self.assertIn("margin-top: 0.8rem !important;", self.css)
        self.assertIn("padding: 1.15rem 0 0.15rem;", self.css)

    def test_27_terminos_y_ejemplos_respetan_temas_sin_colores_fijos(self):
        for esperado in (
            ".calculation-guide-terms",
            ".calculation-guide-term-grid",
            "var(--app-border)",
            "var(--app-surface-soft)",
            'html[data-app-theme="contrast"] .calculation-guide-terms',
        ):
            self.assertIn(esperado, self.css)
        self.assertNotIn("background: #", self.css)

    def test_28_documentacion_registra_cierre_r14_y_gate_841(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs/ROADMAP.md").read_text(encoding="utf-8")
        plan = (ROOT / "docs/PLAN_MAESTRO_HACIA_1_0.md").read_text(encoding="utf-8")
        validacion = (ROOT / "docs/VALIDACION.md").read_text(encoding="utf-8")
        guia = (ROOT / "docs/COMO_SE_CALCULA.md").read_text(encoding="utf-8")

        self.assertIn("**DEV.2:** cerrado.", readme)
        self.assertIn("**NOR.2 R2:** activo", readme)
        for revision in (
            "R1 — ruta pública",
            "R1.2 — navegación",
            "R1.3 — ejemplos sustituidos",
            "R1.4 — etiqueta **Ejemplo**",
        ):
            self.assertIn(revision, roadmap)
        self.assertIn("R1.4", roadmap)
        self.assertIn("841 pruebas", roadmap)
        self.assertIn("R1.2", plan)
        self.assertIn("R1.3", plan)
        self.assertIn("R1.4", plan)
        self.assertIn("DEV.2 — Centro de desarrollo", plan)
        self.assertNotIn("UX.4.6i R1.1", plan)
        self.assertIn("841 pruebas en `OK`", validacion)
        self.assertIn("## Cierre de UX.4.6i", guia)

    def test_29_r14_etiqueta_visible_usa_ejemplo_sin_coletilla(self):
        self.assertNotIn("Ejemplo con números", self.plantilla)
        self.assertGreaterEqual(
            self.plantilla.count(
                '<span class="calculation-guide-example-label">Ejemplo</span>'
            ),
            28,
        )


if __name__ == "__main__":
    unittest.main()
