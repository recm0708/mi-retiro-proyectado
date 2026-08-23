"""Regresiones de auditoría documental y trazabilidad de GOV.1.3 R4."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
R4_DOCS = [
    "TRANSPARENCIA.md",
    "MATRIZ_TRAZABILIDAD.md",
    "AUDITORIA_CALCULOS.md",
    "LIMITACIONES_CONOCIDAS.md",
    "DEPENDENCIAS_TERCEROS.md",
    "PROCESO_RELEASE.md",
    "DECISIONES.md",
]


class TestGov13DocumentacionR4(unittest.TestCase):
    def setUp(self):
        self.version_base = "0.0.23-beta"

    def test_documentos_r4_existen_y_siguen_version_canonica(self):
        for nombre in R4_DOCS:
            with self.subTest(nombre=nombre):
                p = DOCS / nombre
                self.assertTrue(p.is_file())
                texto = p.read_text(encoding="utf-8")
                self.assertIn(f"`{self.version_base}`", texto)
                self.assertIn("GOV.1.3 R4", texto)

    def test_indice_enlaza_documentos_r4(self):
        texto = (DOCS / "INDICE.md").read_text(encoding="utf-8")
        for nombre in R4_DOCS[:-1]:
            with self.subTest(nombre=nombre):
                self.assertIn(f"({nombre})", texto)

    def test_roadmap_conserva_r4_y_objetivo_version(self):
        texto = (DOCS / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("R4 — capa de auditoría documental", texto)
        self.assertIn("0.0.23-beta", texto)

    def test_adr_ids_son_unicos_y_consecutivos(self):
        texto = (DOCS / "DECISIONES.md").read_text(encoding="utf-8")
        ids = [int(x) for x in re.findall(r"(?m)^## ADR-(\d{3})\s+—", texto)]
        self.assertGreaterEqual(len(ids), 158)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(list(range(1, max(ids) + 1)), ids)

    def test_adr_indice_cubre_todas_las_decisiones(self):
        texto = (DOCS / "DECISIONES.md").read_text(encoding="utf-8")
        ledger_ids = re.findall(r"(?m)^## ADR-(\d{3})\s+—", texto)
        index_ids = re.findall(r"(?m)^\| ADR-(\d{3}) \|", texto)
        self.assertGreaterEqual(len(ledger_ids), 158)
        self.assertEqual(ledger_ids, index_ids)

    def test_adr_sustitucion_101_155_y_gobierno(self):
        texto = (DOCS / "DECISIONES.md").read_text(encoding="utf-8")
        for esperado in ("ADR-101", "ADR-155", "ADR-157", "ADR-158"):
            self.assertIn(esperado, texto)
        self.assertIn("Sustituida parcialmente", texto)

    def test_adr_anomalias_estado_se_documentan_sin_inventar(self):
        texto = (DOCS / "DECISIONES.md").read_text(encoding="utf-8")
        self.assertIn("Anomalías históricas de metadata", texto)
        self.assertIn("No declarado explícitamente en el registro pre-R4", texto)
        self.assertIn("no inventa un estado retroactivo", texto)
        self.assertTrue(
            (
                DOCS
                / "archive"
                / "governance"
                / "DECISIONES_PRE_GOV1_3_R4.md"
            ).is_file()
        )

    def test_transparencia_delimita_afirmaciones(self):
        texto = (DOCS / "TRANSPARENCIA.md").read_text(encoding="utf-8")
        self.assertIn("no es un sistema oficial", texto)
        self.assertIn("no certifica", texto)
        self.assertIn("no vuelve a calcular", texto)
        self.assertIn("cobertura individual completa", texto)

    def test_matriz_tiene_esquema_completo(self):
        texto = (DOCS / "MATRIZ_TRAZABILIDAD.md").read_text(encoding="utf-8")
        for campo in (
            "Requisito/contrato",
            "Fuente/criterio",
            "ADR",
            "Implementación",
            "Prueba",
            "Estado",
        ):
            self.assertIn(campo, texto)

    def test_matriz_no_inventa_fuente_legal_para_ux(self):
        texto = (DOCS / "MATRIZ_TRAZABILIDAD.md").read_text(encoding="utf-8")
        self.assertIn("N/A — técnico/UX", texto)
        self.assertIn("No se inventan artículos legales", texto)

    def test_matriz_referencia_archivos_criticos_existentes(self):
        texto = (DOCS / "MATRIZ_TRAZABILIDAD.md").read_text(encoding="utf-8")
        rutas = (
            "app/models/trazabilidad.py",
            "app/services/trazabilidad.py",
            "app/core/archivos_pdf.py",
            "app/engines/sebd.py",
            "app/engines/mixto.py",
            "app/engines/sucgs.py",
            "tests/test_traceability.py",
        )
        for rel in rutas:
            with self.subTest(rel=rel):
                self.assertIn(f"`{rel}`", texto)
                self.assertTrue((ROOT / rel).is_file())

    def test_auditoria_no_duplica_motor(self):
        texto = (DOCS / "AUDITORIA_CALCULOS.md").read_text(encoding="utf-8")
        self.assertIn("No recalcula fórmulas", texto)
        self.assertIn("version_metodologia", texto)
        self.assertIn("SHA del commit", texto)
        self.assertIn("regulations/*.json", texto)

    def test_auditoria_declara_limite_objeto_trazabilidad(self):
        texto = (DOCS / "AUDITORIA_CALCULOS.md").read_text(encoding="utf-8")
        self.assertIn("no incorpora por sí mismo", texto)
        self.assertIn("hash criptográfico", texto)
        self.assertIn("GOV.1.4", texto)

    def test_limitaciones_cubren_areas_criticas(self):
        texto = (DOCS / "LIMITACIONES_CONOCIDAS.md").read_text(encoding="utf-8")
        for esperado in (
            "Granularidad histórica",
            "No existe OCR",
            "revisión jurídica externa",
            "Developer Diagnostics",
            "RF por RF",
            "`LICENSE`",
        ):
            self.assertIn(esperado, texto)

    def test_dependencias_directas_version_y_licencia(self):
        req = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        doc = (DOCS / "DEPENDENCIAS_TERCEROS.md").read_text(encoding="utf-8")
        esperadas = {
            "fastapi": ("0.141.1", "MIT"),
            "Jinja2": ("3.1.6", "BSD-3-Clause"),
            "pydantic": ("2.13.4", "MIT"),
            "python-multipart": ("0.0.32", "Apache-2.0"),
            "pypdf": ("6.16.1", "BSD-3-Clause"),
            "uvicorn": ("0.52.3", "BSD-3-Clause"),
        }
        for nombre, (version, licencia) in esperadas.items():
            with self.subTest(nombre=nombre):
                self.assertRegex(req, rf"(?mi)^{re.escape(nombre)}=={re.escape(version)}$")
                self.assertIn(version, doc)
                self.assertIn(licencia, doc)

    def test_dependencias_documentan_bootstrap_y_servicio_css(self):
        texto = (DOCS / "DEPENDENCIAS_TERCEROS.md").read_text(encoding="utf-8")
        self.assertIn("Bootstrap 5.3.8", texto)
        self.assertIn("cdn.jsdelivr.net", texto)
        self.assertIn("servicio externo operativo", texto)
        self.assertIn("No se envía:", texto)
        self.assertIn("actions/checkout@v7", texto)
        self.assertIn("actions/setup-python@v7", texto)
        self.assertIn("actions/setup-node@v7", texto)
        self.assertNotIn("actions/checkout@v6", texto)
        self.assertNotIn("actions/setup-python@v6", texto)
        self.assertNotIn("actions/setup-node@v6", texto)

    def test_proceso_release_define_gates(self):
        texto = (DOCS / "PROCESO_RELEASE.md").read_text(encoding="utf-8")
        for esperado in (
            "git diff --check",
            "compileall",
            "unittest",
            "`VERSION`",
            "`CHANGELOG.md`",
            "`RELEASES.md`",
            "CI remota",
            "tag anotado",
        ):
            self.assertIn(esperado, texto)

    def test_proceso_release_prohibe_mover_tag(self):
        texto = (DOCS / "PROCESO_RELEASE.md").read_text(encoding="utf-8")
        self.assertIn("no se mueve", texto)
        self.assertIn("no se reutiliza", texto)
        self.assertIn("no crear tag", texto)

    def test_documentos_r4_sin_espacios_finales(self):
        errores = []
        for nombre in R4_DOCS:
            for numero, linea in enumerate(
                (DOCS / nombre).read_text(encoding="utf-8").splitlines(),
                start=1,
            ):
                if linea.endswith((" ", "\t")):
                    errores.append(f"{nombre}:{numero}")
        self.assertEqual([], errores, "Espacios finales: " + ", ".join(errores))

    def test_validacion_registra_baseline_y_objetivo_r4(self):
        texto = (DOCS / "VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("438 pruebas", texto)
        self.assertIn("20 regresiones", texto)
        self.assertIn("458 pruebas", texto)


if __name__ == "__main__":
    unittest.main()
