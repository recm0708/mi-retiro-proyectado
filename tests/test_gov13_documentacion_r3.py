"""Regresiones de normativa, seguridad y privacidad de GOV.1.3 R3."""

from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
R3_DOCS = [
    "NORMATIVA.md",
    "FUENTES_NORMATIVAS.md",
    "MODALIDADES_SEBD.md",
    "MODALIDADES_MIXTO.md",
    "MODALIDADES_SUCGS.md",
    "SEGURIDAD_PRIVACIDAD.md",
    "POLITICA_PRIVACIDAD.md",
    "TERMINOS_USO_PRIVACIDAD.md",
    "CUMPLIMIENTO_LEY_81.md",
]
PRIVACY_DOCS = [
    "SEGURIDAD_PRIVACIDAD.md",
    "POLITICA_PRIVACIDAD.md",
    "TERMINOS_USO_PRIVACIDAD.md",
    "CUMPLIMIENTO_LEY_81.md",
]


class TestGov13DocumentacionR3(unittest.TestCase):
    def setUp(self):
        self.version_base = "0.0.23-beta"

    def test_r3_documentos_declaran_metadata(self):
        for nombre in R3_DOCS:
            with self.subTest(nombre=nombre):
                texto = (DOCS / nombre).read_text(encoding="utf-8")
                self.assertIn(self.version_base, texto)
                self.assertIn("GOV.1.3 R3", texto)
                self.assertIn("**Estado:**", texto)

    def test_snapshots_r3_existen(self):
        for nombre in R3_DOCS:
            snapshot = (
                DOCS
                / "archive"
                / "regulatory-privacy"
                / nombre.replace(".md", "_PRE_GOV1_3_R3.md")
            )
            with self.subTest(nombre=nombre):
                self.assertTrue(snapshot.is_file(), str(snapshot))

    def test_version_privacidad_coincide_con_frontend(self):
        js = (ROOT / "app/static/js/privacy.js").read_text(encoding="utf-8")
        match = re.search(r'VERSION_PRIVACIDAD\s*=\s*"([^"]+)"', js)
        self.assertIsNotNone(match)
        version = match.group(1)

        for nombre in ("POLITICA_PRIVACIDAD.md", "TERMINOS_USO_PRIVACIDAD.md"):
            with self.subTest(nombre=nombre):
                texto = (DOCS / nombre).read_text(encoding="utf-8")
                self.assertIn(f"`{version}`", texto)

    def test_documentos_vigentes_no_arrastran_version_privacidad_anterior(self):
        for nombre in PRIVACY_DOCS:
            with self.subTest(nombre=nombre):
                texto = (DOCS / nombre).read_text(encoding="utf-8")
                self.assertNotIn("2026-08-15.1", texto)

    def test_privacidad_no_es_diario_ux(self):
        patron = re.compile(r"(?m)^#{2,4}\s+.*UX\.\d")
        for nombre in PRIVACY_DOCS:
            with self.subTest(nombre=nombre):
                texto = (DOCS / nombre).read_text(encoding="utf-8")
                self.assertIsNone(patron.search(texto))

    def test_fuentes_declaran_verificacion_actual(self):
        texto = (DOCS / "FUENTES_NORMATIVAS.md").read_text(encoding="utf-8")
        self.assertIn("2026-08-17", texto)
        self.assertIn("https://www.css.gob.pa/normativas-ley-organica/", texto)
        self.assertIn("https://antai.gob.pa/", texto)

    def test_normativa_refleja_metadata_json_base(self):
        params = json.loads(
            (ROOT / "regulations/general_parameters.json").read_text(encoding="utf-8")
        )
        texto = (DOCS / "NORMATIVA.md").read_text(encoding="utf-8")
        self.assertIn(params["gaceta_oficial"], texto)
        self.assertIn(params["fecha_gaceta"], texto)
        self.assertIn(str(params["edades_referencia"]["FEMENINO"]), texto)
        self.assertIn(str(params["edades_referencia"]["MASCULINO"]), texto)

    def test_fecha_operativa_2026_se_trata_como_temporal(self):
        for nombre in ("NORMATIVA.md", "FUENTES_NORMATIVAS.md", "MODALIDADES_MIXTO.md"):
            with self.subTest(nombre=nombre):
                texto = (DOCS / nombre).read_text(encoding="utf-8")
                self.assertIn("18/08/2026", texto)
                self.assertRegex(texto.lower(), r"temporal")

    def test_seguridad_documenta_conexiones_y_no_store(self):
        texto = (DOCS / "SEGURIDAD_PRIVACIDAD.md").read_text(encoding="utf-8")
        self.assertIn("cdn.jsdelivr.net", texto)
        self.assertIn("encabezado HTTP `Date`", texto)
        self.assertIn("Cache-Control: no-store", texto)

    def test_politica_documenta_local_y_session_storage(self):
        texto = (DOCS / "POLITICA_PRIVACIDAD.md").read_text(encoding="utf-8")
        self.assertIn("almacenamiento local", texto.lower())
        self.assertIn("sesión", texto.lower())
        self.assertIn("2026-08-16.1", texto)

    def test_matriz_declara_no_certificacion_y_pendientes(self):
        texto = (DOCS / "CUMPLIMIENTO_LEY_81.md").read_text(encoding="utf-8")
        self.assertIn("No constituye certificación jurídica", texto)
        self.assertIn("Revisión jurídica", texto)
        self.assertIn("Pendiente antes de publicación", texto)
        self.assertIn("Implementado", texto)

    def test_modalidades_tienen_sistema_y_metadata(self):
        casos = {
            "MODALIDADES_SEBD.md": "SEBD",
            "MODALIDADES_MIXTO.md": "Mixto",
            "MODALIDADES_SUCGS.md": "SUCGS",
        }
        for nombre, sistema in casos.items():
            with self.subTest(nombre=nombre):
                texto = (DOCS / nombre).read_text(encoding="utf-8")
                self.assertIn(sistema, texto)
                self.assertIn("GOV.1.3 R3", texto)

    def test_documentos_r3_sin_espacios_finales(self):
        errores = []
        for nombre in R3_DOCS:
            for numero, linea in enumerate(
                (DOCS / nombre).read_text(encoding="utf-8").splitlines(),
                start=1,
            ):
                if linea.endswith((" ", "\t")):
                    errores.append(f"{nombre}:{numero}")
        self.assertEqual([], errores, "Espacios finales: " + ", ".join(errores))

    def test_indice_registra_historico_r3(self):
        texto = (DOCS / "INDICE.md").read_text(encoding="utf-8")
        self.assertIn("archive/regulatory-privacy/", texto)
        self.assertIn("GOV.1.3 R3", texto)

    def test_validacion_registra_baseline_y_objetivo_r3(self):
        texto = (DOCS / "VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("Ran 423 tests", texto)
        self.assertIn("438 pruebas", texto)
        self.assertIn("15 regresiones documentales", texto)


if __name__ == "__main__":
    unittest.main()
