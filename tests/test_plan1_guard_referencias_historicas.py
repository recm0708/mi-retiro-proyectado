"""PLAN.1 R3B2 — guard de referencias históricas y contratos GOV.1.5."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# Estos documentos son ledgers/evidencias que pueden mencionar planes anteriores.
# La excepción es documental: no autoriza a usarlos como objetivo vigente.
LEGACY_CONTEXT_FILES = {
    "README.md",
    "CHANGELOG.md",
    "RELEASES.md",
    "VERSIONING.md",
    "GOVERNANCE.md",
    "docs/ROADMAP.md",
    "docs/VALIDACION.md",
    "docs/CIERRE_GOV1.md",
    "docs/TRANSPARENCIA.md",
    "docs/DECISIONES.md",
    "docs/PROCESO_RELEASE.md",
    "docs/PLAN_MAESTRO_HACIA_1_0.md",
    "docs/AUDITORIA_GITHUB.md",
    "docs/AUDITORIA_REPOSITORIO_2026-08-18.md",
    "docs/PREPARACION_PUBLICA_GITHUB.md",
    "docs/EVALUACION_TERCEROS_DESPLIEGUE.md",
    "docs/GESTION_DATOS_SIMULACION.md",
}

OPERATIVE_DOCS = (
    "SECURITY.md",
    "SUPPORT.md",
    "docs/MODELO_AMENAZAS.md",
    "docs/PROCEDIMIENTO_DERECHOS_TITULAR.md",
    "docs/PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md",
    "docs/SEGURIDAD_PRIVACIDAD.md",
    "docs/POLITICA_PRIVACIDAD.md",
    "docs/TERMINOS_USO_PRIVACIDAD.md",
    "docs/CUMPLIMIENTO_LEY_81.md",
    "docs/DEPENDENCIAS_TERCEROS.md",
    "docs/LICENCIA_Y_DISTRIBUCION.md",
    "docs/LIMITACIONES_CONOCIDAS.md",
)

STALE_PROSPECTIVE_PHRASES = (
    "desarrollo pre-beta",
    "desarrollo/pre-beta",
    "vigente como procedimiento interno pre-beta",
    "pendiente antes de beta pública",
    "pendiente antes de una beta pública",
    "objetivo pre-beta",
    "gate pre-beta",
    "pre-beta pública",
    "contempla una beta futura",
)


def markdown_vigentes():
    """Devuelve Markdown fuera del archivo histórico físico."""
    for path in ROOT.rglob("*.md"):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith("docs/historico/"):
            continue
        yield rel, path.read_text(encoding="utf-8")


class TestPlan1GuardReferenciasHistoricas(unittest.TestCase):
    """Impide que la planificación sustituida vuelva a ser prospectiva."""

    def setUp(self):
        self.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    def test_documentos_operativos_no_contienen_planificacion_obsoleta(self):
        for rel in OPERATIVE_DOCS:
            texto = (ROOT / rel).read_text(encoding="utf-8").casefold()
            with self.subTest(rel=rel):
                self.assertNotIn("0.1.0-beta.1", texto)
                self.assertNotIn("beta pública", texto)
                for frase in STALE_PROSPECTIVE_PHRASES:
                    self.assertNotIn(frase, texto)

    def test_beta_publica_fuera_historico_solo_aparece_en_contextos_permitidos(self):
        hallazgos = []
        for rel, texto in markdown_vigentes():
            if "beta pública" in texto.casefold() and rel not in LEGACY_CONTEXT_FILES:
                hallazgos.append(rel)
        self.assertEqual([], hallazgos)

    def test_0_1_0_beta_1_fuera_historico_solo_aparece_en_ledgers_permitidos(self):
        hallazgos = []
        for rel, texto in markdown_vigentes():
            if "0.1.0-beta.1" in texto and rel not in LEGACY_CONTEXT_FILES:
                hallazgos.append(rel)
        self.assertEqual([], hallazgos)

    def test_referencias_0_1_0_beta_1_permitidas_declaran_sustitucion(self):
        for rel, texto in markdown_vigentes():
            if "0.1.0-beta.1" not in texto:
                continue
            minusculas = texto.casefold()
            with self.subTest(rel=rel):
                self.assertIn(rel, LEGACY_CONTEXT_FILES)
                self.assertIn("1.0.0.0", texto)
                self.assertTrue(
                    any(
                        marcador in minusculas
                        for marcador in (
                            "sustitu",
                            "históric",
                            "planificación anterior",
                            "planificación antigua",
                            "nota posterior",
                        )
                    ),
                    f"{rel} conserva 0.1.0-beta.1 sin marcar su contexto histórico.",
                )

    def test_modelo_amenazas_declara_revision_actual_y_base_historica(self):
        texto = (DOCS / "MODELO_AMENAZAS.md").read_text(encoding="utf-8")
        self.assertIn(f"**Versión de aplicación revisada:** `{self.version}`", texto)
        self.assertIn("**Versión base histórica:** `0.0.23-beta`", texto)
        self.assertIn("GOV.1.5 R1", texto)
        self.assertIn("antes de `1.0.0.0`", texto)

    def test_procedimientos_gov15_declaran_revision_actual_y_base_historica(self):
        for nombre in (
            "PROCEDIMIENTO_DERECHOS_TITULAR.md",
            "PROCEDIMIENTO_INCIDENTES_SEGURIDAD.md",
        ):
            texto = (DOCS / nombre).read_text(encoding="utf-8")
            with self.subTest(nombre=nombre):
                self.assertIn(f"**Versión de aplicación revisada:** `{self.version}`", texto)
                self.assertIn("**Versión base histórica:** `0.0.23-beta`", texto)
                self.assertIn("GOV.1.5 R2", texto)
                self.assertNotIn("procedimiento interno pre-beta", texto)

    def test_versioning_documenta_guard_y_conserva_heading_historico(self):
        texto = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        self.assertIn("## 12. Guard de referencias históricas", texto)
        self.assertIn("### 3.1. Desarrollo pre-beta", texto)
        self.assertIn("no pueden volver a utilizarse como objetivo vigente", texto)
        self.assertIn("tests/test_plan1_guard_referencias_historicas.py", texto)

    def test_validacion_conserva_cierre_r3b2(self):
        texto = (DOCS / "VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("cerró con **702 pruebas en `OK`**", texto)
        self.assertIn("cerró con **710 pruebas en `OK`**", texto)
        self.assertTrue(self.version)


if __name__ == "__main__":
    unittest.main()
