"""Regresiones de GOV.1.5 R2: derechos del titular e incidentes."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DERECHOS = DOCS / "PROCEDIMIENTO_DERECHOS_TITULAR.md"
INCIDENTES = DOCS / "PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md"


class TestGov15ProcedimientosR2(unittest.TestCase):
    def setUp(self):
        self.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.derechos = DERECHOS.read_text(encoding="utf-8")
        self.incidentes = INCIDENTES.read_text(encoding="utf-8")

    def test_documentos_existen_declaran_r2_version_y_revision_externa(self):
        for path, texto in (
            (DERECHOS, self.derechos),
            (INCIDENTES, self.incidentes),
        ):
            with self.subTest(path=path.name):
                self.assertTrue(path.is_file())
                self.assertIn(self.version, texto)
                self.assertIn("GOV.1.5 R2", texto)
                self.assertIn("Revisión jurídica externa", texto)

    def test_derechos_y_plazos_publicados_por_antai(self):
        esperados = {
            "Acceso": "10 días hábiles",
            "Rectificación": "5 días hábiles",
            "Cancelación": "10 días hábiles",
            "Portabilidad": "10 días hábiles",
            "Oposición": "Efecto inmediato",
        }
        for derecho, plazo in esperados.items():
            with self.subTest(derecho=derecho):
                self.assertIn(derecho, self.derechos)
                self.assertIn(plazo, self.derechos)
        self.assertIn("motivos legítimos imperiosos", self.derechos)

    def test_procedimiento_responde_aun_si_no_hay_datos_remotos(self):
        self.assertIn(
            "no mantiene datos almacenados del solicitante",
            self.derechos,
        )
        self.assertIn("debe responder", self.derechos)
        for esperado in (
            "no dispone de cuentas",
            "no mantiene una base de datos permanente",
            "`sessionStorage`",
            "procesa PDF en memoria",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, self.derechos)

    def test_verificacion_es_proporcional_y_minimiza_identidad(self):
        for esperado in (
            "no pedir copia de cédula de forma automática",
            "no recopilar más datos de los necesarios",
            "resultado de la verificación",
            "no una copia íntegra",
            "no guardar documentos de identidad en el repositorio",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, self.derechos)

    def test_registro_minimo_no_se_versiona_en_git(self):
        self.assertIn("case_id", self.derechos)
        self.assertIn("no se versiona en Git", self.derechos)
        self.assertIn("incident_id", self.incidentes)
        self.assertIn("fuera de Git", self.incidentes)
        for prohibido in (
            "NSS completos",
            "historia salarial completa",
            "tokens/secretos",
        ):
            with self.subTest(prohibido=prohibido):
                self.assertIn(prohibido, self.incidentes)

    def test_incidentes_definen_contencion_evaluacion_notificacion_y_cierre(self):
        for esperado in (
            "Fase A — Detección y apertura",
            "Fase B — Contención",
            "Fase C — Preservación de evidencia",
            "Fase D — Evaluación",
            "Fase E — Comunicación y notificación",
            "Recuperación",
            "Post-mortem",
            "Criterio de cierre",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, self.incidentes)

    def test_incidentes_exigen_inmediatez_y_no_inventan_72_horas(self):
        self.assertIn("con inmediatez", self.incidentes)
        self.assertIn("informar al titular", self.incidentes)
        self.assertIn(
            "no establece 72 horas como plazo legal general",
            self.incidentes,
        )
        self.assertIn(
            "requerimiento específico",
            self.incidentes,
        )
        self.assertIn("no plazos legales", self.incidentes)

    def test_fuentes_oficiales_y_canales_antai_estan_documentados(self):
        self.assertIn("antai.gob.pa/preguntas-frecuentes", self.derechos)
        self.assertIn("protecciondedatos@antai.gob.pa", self.derechos)
        self.assertIn("ANTAI Smart CID", self.derechos)
        self.assertIn("antai-se-pronuncia", self.incidentes)
        self.assertIn("comunicado-proteccion-de-datos-personales", self.incidentes)


if __name__ == "__main__":
    unittest.main()
