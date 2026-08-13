"""Regresión E2E y hardening previo a la primera beta."""

from datetime import date
from io import BytesIO
from pathlib import Path
import unittest

from fastapi.testclient import TestClient
from pypdf import PdfWriter

from app.main import app
from app.modelos.pension import (
    DatosResultadoMixto,
    DatosResultadoSEBD,
    DatosResultadoSUCGS,
)
from app.modelos.simulacion import (
    DatosHistorialSalarial,
    EscenarioLineaTiempo,
    EscenarioRetiro,
    RegistroHistorialSalarial,
    RegistroLineaTiempo,
    ResumenLineaTiempo,
    ResumenRetiro,
)


ROOT = Path(__file__).resolve().parents[1]


class TestPreBetaE2EHardening(unittest.TestCase):
    """Protege API, motores integrados e importación de documentos."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(app)

    @staticmethod
    def _pdf_en_blanco(paginas: int = 1) -> bytes:
        escritor = PdfWriter()
        for _ in range(paginas):
            escritor.add_blank_page(width=612, height=792)
        salida = BytesIO()
        escritor.write(salida)
        return salida.getvalue()

    @staticmethod
    def _retiro(cuotas: int, adicionales: int = 0) -> ResumenRetiro:
        escenario = EscenarioRetiro(
            tipo="REFERENCIA",
            nombre="Edad de referencia",
            fecha_retiro=date(2026, 11, 16),
            edad_retiro_anios=57,
            meses_desde_corte_cuotas=5,
            cuotas_estimadas_adicionales=adicionales,
            cuotas_estimadas_totales=cuotas,
            fecha_ya_transcurrida=False,
        )
        return ResumenRetiro(
            fecha_corte=date(2026, 8, 10),
            fecha_corte_cuotas=date(2026, 5, 31),
            edad_actual_anios=56,
            edad_referencia=57,
            fecha_referencia=date(2026, 11, 16),
            alcanzo_edad_referencia=False,
            dias_hasta_referencia=98,
            escenarios=[escenario],
            anio_fin_proyeccion_salarial=2031,
            proyeccion_salarial_cubre_escenarios=True,
            advertencias=[],
            metodo_estimacion_cuotas="Regresión E2E pre-beta.",
        )

    @staticmethod
    def _datos_sebd(modo: str) -> DatosResultadoSEBD:
        salarios = [
            8920.45,
            10013.23,
            10431.36,
            10910.82,
            11064.62,
            17474.59,
            17538.10,
            17719.86,
            17760.01,
            17760.67,
        ]
        registros = [
            RegistroHistorialSalarial(
                anio=2016 + indice,
                cuotas=12,
                salario_cotizado=salario,
            )
            for indice, salario in enumerate(salarios)
        ]
        registros.append(
            RegistroHistorialSalarial(
                anio=2026,
                cuotas=5,
                salario_cotizado=6659.50,
            )
        )
        historial = DatosHistorialSalarial(
            anio_inicio=2016,
            anio_fin=2026,
            cuotas_totales_referencia=281,
            registros=registros,
        )
        linea = ResumenLineaTiempo(
            anio_inicio_historico=2016,
            anio_actual=2026,
            anio_fin_proyeccion=2031,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Salario constante",
                    tasa_anual_pct=0.0,
                    registros=[
                        RegistroLineaTiempo(
                            anio=2026,
                            cuotas_historicas=5,
                            salario_historico=6659.50,
                            cuotas_proyectadas=7,
                            salario_proyectado=10500.00,
                            cuotas_cierre=12,
                            salario_cierre=17159.50,
                            estado="MIXTO",
                        )
                    ],
                )
            ],
        )
        cuotas = 281 if modo == "SOLO_ACREDITADO" else 286
        adicionales = 0 if modo == "SOLO_ACREDITADO" else 5
        return DatosResultadoSEBD(
            modo_integracion=modo,
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            historial=historial,
            linea_tiempo=linea,
            resumen_retiro=TestPreBetaE2EHardening._retiro(cuotas, adicionales),
            fecha_retiro_seleccionada=date(2026, 11, 16),
            escenario_salarial_nombre="Salario constante",
        )

    @staticmethod
    def _datos_mixto() -> DatosResultadoMixto:
        registros = [
            RegistroHistorialSalarial(
                anio=anio,
                cuotas=12,
                salario_cotizado=12000,
            )
            for anio in range(2002, 2027)
        ]
        historial = DatosHistorialSalarial(
            anio_inicio=2002,
            anio_fin=2026,
            cuotas_totales_referencia=300,
            registros=registros,
        )
        linea = ResumenLineaTiempo(
            anio_inicio_historico=2002,
            anio_actual=2026,
            anio_fin_proyeccion=2026,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Escenario base",
                    tasa_anual_pct=0.0,
                    registros=[],
                )
            ],
        )
        return DatosResultadoMixto(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            historial=historial,
            linea_tiempo=linea,
            resumen_retiro=TestPreBetaE2EHardening._retiro(300, 0),
            fecha_retiro_seleccionada=date(2026, 11, 16),
            escenario_salarial_nombre="Escenario base",
            saldo_ahorro_personal=100000,
            bono_reconocimiento=5000,
            bono_reconocimiento_confirmado_oficialmente=True,
            valor_actuarial_expectativa_vida=200,
            opcion_prestacion_cap="PENSION_PROGRAMADA",
        )

    @staticmethod
    def _datos_sucgs() -> DatosResultadoSUCGS:
        registros = []
        for anio in range(1997, 2017):
            registros.append(
                RegistroHistorialSalarial(
                    anio=anio,
                    cuotas=6,
                    salario_cotizado=6000,
                )
            )
        for anio in range(2017, 2027):
            registros.append(
                RegistroHistorialSalarial(
                    anio=anio,
                    cuotas=12,
                    salario_cotizado=12000,
                )
            )
        historial = DatosHistorialSalarial(
            anio_inicio=1997,
            anio_fin=2026,
            cuotas_totales_referencia=240,
            registros=registros,
        )
        linea = ResumenLineaTiempo(
            anio_inicio_historico=1997,
            anio_actual=2026,
            anio_fin_proyeccion=2026,
            escenarios=[
                EscenarioLineaTiempo(
                    nombre="Escenario base",
                    tasa_anual_pct=0.0,
                    registros=[],
                )
            ],
        )
        return DatosResultadoSUCGS(
            fecha_nacimiento=date(1969, 11, 16),
            sexo="FEMENINO",
            historial=historial,
            linea_tiempo=linea,
            resumen_retiro=TestPreBetaE2EHardening._retiro(240, 0),
            fecha_retiro_seleccionada=date(2026, 11, 16),
            escenario_salarial_nombre="Escenario base",
            saldo_capitalizacion_solidaria=100000,
            saldo_confirmado_oficialmente=True,
            valor_minimo_universal_vigente=144,
            pension_garantizada_solidaria_vigente=265,
            valores_solidarios_confirmados_oficialmente=True,
            historial_laboral_completo_confirmado=True,
            estabilidad_salarial_art197_confirmada=True,
        )

    def test_e2e_api_sebd_acreditado_y_proyectado(self):
        acreditado = self.cliente.post(
            "/api/simulacion/resultados/sebd",
            json=self._datos_sebd("SOLO_ACREDITADO").model_dump(mode="json"),
        )
        proyectado = self.cliente.post(
            "/api/simulacion/resultados/sebd",
            json=self._datos_sebd("PROYECTADO").model_dump(mode="json"),
        )

        self.assertEqual(acreditado.status_code, 200)
        self.assertEqual(proyectado.status_code, 200)
        self.assertEqual(acreditado.json()["calculo"]["pension_mensual_estimada"], 741.59)
        self.assertEqual(proyectado.json()["calculo"]["pension_mensual_estimada"], 769.42)

    def test_e2e_api_mixto_conserva_resultado_controlado(self):
        respuesta = self.cliente.post(
            "/api/simulacion/resultados/mixto",
            json=self._datos_mixto().model_dump(mode="json"),
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["calculo"]["pension_mensual_total_estimada"], 856.25)

    def test_e2e_api_sucgs_conserva_garantia_controlada(self):
        respuesta = self.cliente.post(
            "/api/simulacion/resultados/sucgs",
            json=self._datos_sucgs().model_dump(mode="json"),
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.json()["calculo"]["pension_mensual_total_estimada"], 600.0)

    def test_respuestas_html_incluyen_cabeceras_defensivas(self):
        respuesta = self.cliente.get("/simulacion")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.headers["x-content-type-options"], "nosniff")
        self.assertEqual(respuesta.headers["x-frame-options"], "DENY")
        self.assertEqual(respuesta.headers["referrer-policy"], "no-referrer")
        self.assertIn("camera=()", respuesta.headers["permissions-policy"])

    def test_importador_rechaza_extension_falsa_aunque_mime_diga_pdf(self):
        respuesta = self.cliente.post(
            "/api/simulacion/referencia-mi-retiro-seguro",
            files={"archivo": ("documento.txt", b"%PDF-1.7\n", "application/pdf")},
        )
        self.assertEqual(respuesta.status_code, 415)

    def test_importador_rechaza_mime_incompatible_aunque_extension_sea_pdf(self):
        respuesta = self.cliente.post(
            "/api/simulacion/referencia-mi-retiro-seguro",
            files={"archivo": ("documento.pdf", b"%PDF-1.7\n", "text/plain")},
        )
        self.assertEqual(respuesta.status_code, 415)

    def test_importador_rechaza_archivo_sin_cabecera_pdf(self):
        respuesta = self.cliente.post(
            "/api/simulacion/referencia-mi-retiro-seguro",
            files={"archivo": ("documento.pdf", b"contenido cualquiera", "application/pdf")},
        )
        self.assertEqual(respuesta.status_code, 415)
        self.assertIn("cabecera PDF", respuesta.json()["detail"])

    def test_importador_rechaza_archivo_vacio(self):
        respuesta = self.cliente.post(
            "/api/simulacion/ficha-digital",
            files={"archivo": ("ficha.pdf", b"", "application/pdf")},
        )
        self.assertEqual(respuesta.status_code, 422)

    def test_importador_rechaza_exceso_de_tamano_antes_de_parsear(self):
        contenido = b"%PDF-1.7\n" + (b"0" * (8 * 1024 * 1024))
        respuesta = self.cliente.post(
            "/api/simulacion/referencia-mi-retiro-seguro",
            files={"archivo": ("documento.pdf", contenido, "application/pdf")},
        )
        self.assertEqual(respuesta.status_code, 413)

    def test_pdf_real_pero_ajeno_pasa_firma_y_falla_por_contenido(self):
        respuesta = self.cliente.post(
            "/api/simulacion/referencia-mi-retiro-seguro",
            files={"archivo": ("documento.pdf", self._pdf_en_blanco(), "application/pdf")},
        )
        self.assertEqual(respuesta.status_code, 422)
        self.assertNotIn("cabecera PDF", respuesta.json()["detail"])

    def test_limite_de_paginas_del_comprobante_sigue_protegido(self):
        respuesta = self.cliente.post(
            "/api/simulacion/referencia-mi-retiro-seguro",
            files={"archivo": ("documento.pdf", self._pdf_en_blanco(21), "application/pdf")},
        )
        self.assertEqual(respuesta.status_code, 422)
        self.assertIn("más páginas", respuesta.json()["detail"])

    def test_respuesta_de_importacion_no_permite_cache(self):
        respuesta = self.cliente.post(
            "/api/simulacion/referencia-mi-retiro-seguro",
            files={"archivo": ("documento.pdf", self._pdf_en_blanco(), "application/pdf")},
        )
        self.assertEqual(respuesta.headers.get("cache-control"), "no-store")

    def test_ci_prebeta_cubre_python_node_y_suite(self):
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        self.assertIn('python-version: ["3.13", "3.14"]', workflow)
        self.assertIn('actions/checkout@v6', workflow)
        self.assertIn('actions/setup-python@v6', workflow)
        self.assertIn('actions/setup-node@v6', workflow)
        self.assertIn('node-version: "24"', workflow)
        self.assertIn('python -m pip check', workflow)
        self.assertIn('python -m unittest discover -s tests -v', workflow)
        self.assertIn('contents: read', workflow)

    def test_dependabot_vigila_pip_y_github_actions(self):
        config = (ROOT / ".github/dependabot.yml").read_text(encoding="utf-8")
        self.assertIn('package-ecosystem: pip', config)
        self.assertIn('package-ecosystem: github-actions', config)
        self.assertGreaterEqual(config.count('interval: weekly'), 2)

    def test_documentacion_de_seguridad_y_privacidad_esta_versionada(self):
        documento = ROOT / "docs/SEGURIDAD_PRIVACIDAD.md"
        self.assertTrue(documento.exists())
        texto = documento.read_text(encoding="utf-8")
        self.assertIn("se leen en memoria", texto)
        self.assertIn("Cache-Control: no-store", texto)


if __name__ == "__main__":
    unittest.main()
