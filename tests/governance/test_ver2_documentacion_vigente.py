"""Regresiones de documentación vigente para VER.2."""

from pathlib import Path
import json
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"
VERSION_CANONICA = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
ULTIMO_TAG_LEGACY = "v0.0.26-beta"


class TestVer2DocumentacionVigente(unittest.TestCase):
    def test_version_canonica_promovida_a_g071_e01(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

        self.assertEqual(VERSION_CANONICA, version)
        self.assertEqual(version, APP_VERSION)
        ledger = json.loads(
            (ROOT / "data/governance/pre-1-0-revision-ledger.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            (ledger["accepted_count"], ledger["entries"][-1]["ordinal"]),
            descomponer_version_beta_revision(version),
        )

    def test_historia_ver2_y_estado_vivo_usan_autoridades_correctas(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (DOCS / "governance/roadmap.md").read_text(encoding="utf-8")
        plan = (DOCS / "governance/master-plan-to-1-0.md").read_text(
            encoding="utf-8"
        )
        indice = (DOCS / "README.md").read_text(encoding="utf-8")
        ledger = (
            DOCS / "governance/pre-1-0-revision-ledger.md"
        ).read_text(encoding="utf-8")
        audit = (
            DOCS / "archive/governance/pre-1-0-versioning-audit.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            f"**Versión de desarrollo:** `{VERSION_CANONICA}`",
            readme,
        )
        self.assertNotIn("G071", readme)
        self.assertNotIn("G087", readme)
        self.assertNotIn("VER.2 R6", readme)

        for documento in (roadmap, plan):
            self.assertIn("G129/E03/C0", documento)
            self.assertIn("DOC.4 R1", documento)

        self.assertIn(
            "| Versionado | [Política de versionado](../VERSIONING.md)",
            indice,
        )
        self.assertIn("G071", ledger + audit)
        self.assertIn("G087", ledger + audit)


    def test_tag_legacy_y_reconciliacion_g071_g087_permanecen_documentados(self):
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        ledger = (
            DOCS / "governance/pre-1-0-revision-ledger.md"
        ).read_text(encoding="utf-8")

        self.assertIn(ULTIMO_TAG_LEGACY, releases)
        self.assertIn("G071 / E01 -> 0.0.71.01-beta", versioning)
        self.assertIn("No crear tags revision-aware retrospectivos", versioning)
        self.assertIn("G071", ledger)
        self.assertIn("G087", ledger)


    def test_ledger_y_auditoria_siguen_reconociendo_g071(self):
        ledger = (
            DOCS / "governance/pre-1-0-revision-ledger.md"
        ).read_text(encoding="utf-8")
        auditoria = (
            DOCS / "archive/governance/pre-1-0-versioning-audit.md"
        ).read_text(encoding="utf-8")
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        indice = (DOCS / "README.md").read_text(encoding="utf-8")

        self.assertIn("G071", ledger)
        self.assertIn(VERSION_CANONICA, ledger)
        self.assertIn("G071", auditoria)
        self.assertIn("G071 / E01 -> 0.0.71.01-beta", versioning)
        self.assertIn(
            "[Ledger pre-1.0](governance/pre-1-0-revision-ledger.md)",
            indice,
        )


    def test_no_tags_revision_aware_retroactivos(self):
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")

        for version in range(22, 27):
            tag = f"v0.0.{version}-beta"
            self.assertIn(tag, releases)

        self.assertIn(
            "No crear tags revision-aware retrospectivos para G001–G070",
            versioning,
        )

