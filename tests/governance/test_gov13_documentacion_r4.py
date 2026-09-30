"""Regresiones de auditoría documental y trazabilidad de GOV.1.3 R4."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
R4_DOCS = [
    "product/transparency.md",
    "product/traceability-matrix.md",
    "archive/technical/calculation-audit.md",
    "product/known-limitations.md",
    "operations/third-party-dependencies.md",
    "operations/release-process.md",
    "decisions/README.md",
]


class TestGov13DocumentacionR4(unittest.TestCase):
    def setUp(self):
        self.version_base = "0.0.23-beta"


    def test_documentos_r4_existen_y_respetan_su_tipo_documental(self):
        live_contracts = {
            "operations/release-process.md": "# Proceso de release",
            "decisions/README.md": "# Registro de decisiones",
        }

        for nombre in R4_DOCS:
            with self.subTest(nombre=nombre):
                path = DOCS / nombre
                self.assertTrue(path.is_file())
                texto = path.read_text(encoding="utf-8")

                if nombre in live_contracts:
                    self.assertIn(live_contracts[nombre], texto)
                    self.assertNotIn(
                        "GOV.1.3 R4",
                        texto,
                        "un documento vivo no debe depender del marcador histórico R4",
                    )
                else:
                    self.assertIn(f"`{self.version_base}`", texto)
                    self.assertIn("GOV.1.3 R4", texto)


    def test_indices_enlazan_documentos_r4_segun_su_owner(self):
        indice = (DOCS / "README.md").read_text(encoding="utf-8")
        archive = (DOCS / "archive/README.md").read_text(encoding="utf-8")

        for nombre in (
            "product/transparency.md",
            "product/traceability-matrix.md",
            "product/known-limitations.md",
            "operations/third-party-dependencies.md",
            "operations/release-process.md",
            "decisions/README.md",
        ):
            with self.subTest(nombre=nombre):
                self.assertIn(f"({nombre})", indice)

        self.assertIn("[`technical/`](technical/)", archive)
        self.assertNotIn(
            "(archive/technical/calculation-audit.md)",
            indice,
        )

    def test_historia_r4_y_objetivo_vigente_usan_owners_correctos(self):
        history = (
            DOCS
            / "archive/governance/"
            "historical-change-registry.md"
        ).read_text(encoding="utf-8")
        ledger = (
            DOCS
            / "governance/pre-1-0-revision-ledger.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "R4 — transparencia, auditoría y trazabilidad",
            history,
        )
        self.assertIn("GOV.1.3 R4", ledger)
        self.assertIn("0.0.26.04-beta", ledger)

        roadmap = (
            DOCS / "governance/roadmap.md"
        ).read_text(encoding="utf-8")
        self.assertIn("1.0.0.0", roadmap)
        self.assertIn("G129/E03/C0", roadmap)
        self.assertIn("DOC.4 R1", roadmap)
        self.assertNotIn("PLAN.2 R2", roadmap)

    def test_adr_ids_son_unicos_y_consecutivos(self):
        texto = (DOCS / "decisions/README.md").read_text(encoding="utf-8")
        ids = [int(x) for x in re.findall(r"(?m)^## ADR-(\d{3})\s+—", texto)]
        self.assertGreaterEqual(len(ids), 158)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(list(range(1, max(ids) + 1)), ids)

    def test_adr_indice_cubre_todas_las_decisiones(self):
        texto = (DOCS / "decisions/README.md").read_text(encoding="utf-8")
        ledger_ids = re.findall(r"(?m)^## ADR-(\d{3})\s+—", texto)
        index_ids = re.findall(r"(?m)^\| ADR-(\d{3}) \|", texto)
        self.assertGreaterEqual(len(ledger_ids), 158)
        self.assertEqual(ledger_ids, index_ids)

    def test_adr_sustitucion_101_155_y_gobierno(self):
        texto = (DOCS / "decisions/README.md").read_text(encoding="utf-8")
        for esperado in ("ADR-101", "ADR-155", "ADR-157", "ADR-158"):
            self.assertIn(esperado, texto)
        self.assertIn("Sustituida parcialmente", texto)

    def test_adr_anomalias_estado_se_documentan_sin_inventar(self):
        texto = (DOCS / "decisions/README.md").read_text(encoding="utf-8")
        self.assertIn("Anomalías históricas de metadata", texto)
        self.assertIn("No declarado explícitamente en el registro pre-R4", texto)
        self.assertIn("no inventa un estado retroactivo", texto)
        self.assertTrue(
            (
                DOCS
                / "archive"
                / "governance"
                / "decisions-pre-gov1-3-r4.md"
            ).is_file()
        )

    def test_transparencia_delimita_afirmaciones(self):
        texto = (DOCS / "product/transparency.md").read_text(encoding="utf-8")
        self.assertIn("no es un sistema oficial", texto)
        self.assertIn("no certifica", texto)
        self.assertIn("no vuelve a calcular", texto)
        self.assertIn("cobertura individual completa", texto)

    def test_matriz_tiene_esquema_completo(self):
        texto = (DOCS / "product/traceability-matrix.md").read_text(encoding="utf-8")
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
        texto = (DOCS / "product/traceability-matrix.md").read_text(encoding="utf-8")
        self.assertIn("N/A — técnico/UX", texto)
        self.assertIn("No se inventan artículos legales", texto)

    def test_matriz_referencia_archivos_criticos_existentes(self):
        texto = (DOCS / "product/traceability-matrix.md").read_text(encoding="utf-8")
        rutas = (
            "app/models/traceability.py",
            "app/services/traceability.py",
            "app/portals/asegurado/pdf_files.py",
            "app/engines/sebd.py",
            "app/engines/mixto.py",
            "app/engines/sucgs.py",
            "tests/domain/test_traceability.py",
        )
        for rel in rutas:
            with self.subTest(rel=rel):
                self.assertIn(f"`{rel}`", texto)
                self.assertTrue((ROOT / rel).is_file())

    def test_auditoria_no_duplica_motor(self):
        texto = (DOCS / "archive/technical/calculation-audit.md").read_text(encoding="utf-8")
        self.assertIn("No recalcula fórmulas", texto)
        self.assertIn("version_metodologia", texto)
        self.assertIn("SHA del commit", texto)
        self.assertIn("regulations/*.json", texto)

    def test_auditoria_declara_limite_objeto_trazabilidad(self):
        texto = (DOCS / "archive/technical/calculation-audit.md").read_text(encoding="utf-8")
        self.assertIn("no incorpora por sí mismo", texto)
        self.assertIn("hash criptográfico", texto)
        self.assertIn("GOV.1.4", texto)

    def test_limitaciones_cubren_areas_criticas(self):
        texto = (DOCS / "product/known-limitations.md").read_text(encoding="utf-8")
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
        doc = (DOCS / "operations/third-party-dependencies.md").read_text(encoding="utf-8")
        pins = {}
        for linea in req.splitlines():
            limpia = linea.strip()
            if limpia and not limpia.startswith("#") and "==" in limpia:
                nombre, version = limpia.split("==", 1)
                pins[nombre.casefold()] = version

        esperadas = {
            "fastapi": "MIT",
            "Jinja2": "BSD-3-Clause",
            "pydantic": "MIT",
            "python-multipart": "Apache-2.0",
            "pypdf": "BSD-3-Clause",
            "uvicorn": "BSD-3-Clause",
        }
        for nombre, licencia in esperadas.items():
            with self.subTest(nombre=nombre):
                version = pins.get(nombre.casefold())
                self.assertIsNotNone(version, f"Falta pin directo para {nombre}")
                self.assertRegex(
                    doc,
                    rf"(?mi)^\|\s*{re.escape(nombre)}\s*\|\s*{re.escape(version)}\s*\|.*\|\s*{re.escape(licencia)}\s*\|",
                )

    def test_dependencias_documentan_bootstrap_y_servicio_css(self):
        texto = (DOCS / "operations/third-party-dependencies.md").read_text(encoding="utf-8")
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
        texto = (
            DOCS / "operations/release-process.md"
        ).read_text(encoding="utf-8")

        for esperado in (
            "Quality Gate completo",
            "`VERSION`",
            "ledger",
            "registry/manifest",
            "git verify-commit HEAD",
            "Repository Quality Gate",
            "Python Compatibility",
            'git tag -s "v$version"',
            'git tag -v "v$version"',
            "GitHub Release",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)



    def test_proceso_release_prohibe_mover_tag(self):
        texto = (
            DOCS / "operations/release-process.md"
        ).read_text(encoding="utf-8")

        self.assertIn("un tag publicado no se mueve", texto)
        self.assertIn("reutiliza ni elimina", texto)
        self.assertIn(
            "una corrección posterior sigue el modelo revision-aware",
            texto,
        )
        self.assertIn(
            "El tag se deriva exactamente de `VERSION`",
            texto,
        )
        self.assertIn(
            "revalidar:",
            texto,
        )

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
        texto = (DOCS / "operations/validation.md").read_text(encoding="utf-8")
        self.assertIn("438 pruebas", texto)
        self.assertIn("20 regresiones", texto)
        self.assertIn("458 pruebas", texto)


if __name__ == "__main__":
    unittest.main()
