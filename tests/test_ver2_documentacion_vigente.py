"""Regresiones de documentación vigente para VER.2."""

from pathlib import Path
import json
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
VERSION_CANONICA = "0.1.10.01-beta"
ULTIMO_TAG_LEGACY = "v0.0.26-beta"


class TestVer2DocumentacionVigente(unittest.TestCase):
    def test_version_canonica_promovida_a_g071_e01(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

        self.assertEqual(VERSION_CANONICA, version)
        self.assertEqual(version, APP_VERSION)
        ledger = json.loads(
            (ROOT / "data/pre-1-0-revision-ledger.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            (ledger["accepted_count"], 1),
            descomponer_version_beta_revision(version),
        )

    def test_documentos_vivos_declaran_promocion_vigente(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (DOCS / "governance/roadmap.md").read_text(encoding="utf-8")
        plan = (DOCS / "governance/master-plan-to-1-0.md").read_text(encoding="utf-8")
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        indice = (DOCS / "README.md").read_text(encoding="utf-8")

        self.assertIn("**Versión canónica vigente:** `0.1.10.01-beta`", readme)
        self.assertIn("G071/E01 promovido en `VERSION`", readme)
        self.assertIn("la reconciliación posterior sitúa ese estado en G087/E01", roadmap)
        self.assertIn("la reconciliación posterior sitúa ese estado en G087/E01", plan)
        self.assertIn("| `0.0.71.01-beta` | Versión promovida históricamente en VER.2 R4", security)
        self.assertIn("**Versión de aplicación:** `0.1.10.01-beta`", indice)

    def test_tag_legacy_permanece_y_tag_g071_no_se_crea_en_pr(self):
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        proceso = (DOCS / "operations/release-process.md").read_text(encoding="utf-8")

        self.assertIn(ULTIMO_TAG_LEGACY, versioning)
        self.assertIn("Un tag formal nuevo no se crea dentro del PR del candidato", versioning)
        self.assertIn("no existe tag `v0.0.71.01-beta` hasta completar merge", releases)
        self.assertIn("`v0.0.71.01-beta` fue publicado originalmente bajo la denominación VER.2 G071/E01", proceso)

    def test_ledger_y_auditoria_siguen_reconociendo_g071(self):
        ledger = (DOCS / "governance/pre-1-0-revision-ledger.md").read_text(encoding="utf-8")
        auditoria = (DOCS / "archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md").read_text(encoding="utf-8")
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        indice = (DOCS / "README.md").read_text(encoding="utf-8")

        self.assertIn("G071", ledger)
        self.assertIn(VERSION_CANONICA, ledger)
        self.assertIn("G071", auditoria)
        self.assertIn("G071 / E01 -> 0.0.71.01-beta", versioning)
        self.assertIn("version_ledger.py", indice)

    def test_no_tags_revision_aware_retroactivos(self):
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")

        for version in range(22, 27):
            tag = f"v0.0.{version}-beta"
            self.assertIn(tag, versioning)

        self.assertIn("No crear tags revision-aware retrospectivos", versioning)
