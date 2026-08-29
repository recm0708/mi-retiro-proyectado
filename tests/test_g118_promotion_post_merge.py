"""Regresiones de promoción DEV.2 R5 -> G118/E04."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG118PromotionPostMerge(unittest.TestCase):
    def test_version_y_runtime_materializan_g118_e04(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.18.04-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((118, 4), descomponer_version_beta_revision(version))

    def test_ledger_acepta_g118_y_reserva_g119_e05(self):
        ledger = cargar_ledger()
        self.assertEqual(118, ledger["accepted_count"])
        self.assertEqual(119, ledger["next_global"])
        self.assertEqual("0.1.19.05-beta", ledger["next_candidate"])
        self.assertEqual("DEV.2", ledger["next_candidate_block"])
        entry = ledger["entries"][-1]
        self.assertEqual(118, entry["global_revision"])
        self.assertEqual("DEV.2", entry["block"])
        self.assertEqual(4, entry["ordinal"])
        self.assertEqual("R5", entry["functional_revision"])
        self.assertEqual("0.1.18.04-beta", entry["revision_aware"])
        self.assertIn("PR #107", entry["evidence"])
        self.assertIn("bc97db0", entry["evidence"])

    def test_registro_preserva_r5_y_abre_r6(self):
        data = json.loads((ROOT / "data/work-block-registry.json").read_text(encoding="utf-8"))
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertIn("G118", ids["DEV.2"]["global_refs"])
        self.assertEqual("reopened_candidate_r6", ids["DEV.2"]["status"])
        candidate = data["current_candidate"]
        self.assertEqual(119, candidate["global_revision"])
        self.assertEqual("0.1.19.05-beta", candidate["revision_aware"])
        self.assertEqual("DEV.2", candidate["block"])
        self.assertEqual("R6", candidate["revision"])
        self.assertEqual(5, candidate["edition"])
        self.assertEqual("reserved_not_accepted", candidate["state"])

    def test_manifiesto_distingue_r5_de_e04(self):
        manifest = json.loads((ROOT / "data/release-publication-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("0.1.18.04-beta", manifest["version"])
        self.assertEqual("DEV.2", manifest["block"])
        self.assertEqual("R5", manifest["revision"])
        self.assertEqual("0.1.19.05-beta", manifest["next_step"]["revision_aware"])

    def test_documentacion_viva_declara_g118_y_g119(self):
        for rel in (
            "README.md",
            "GOVERNANCE.md",
            "VERSIONING.md",
            "SECURITY.md",
            "docs/README.md",
            "docs/governance/roadmap.md",
            "docs/governance/master-plan-to-1-0.md",
            "docs/governance/pre-1-0-pending-matrix.md",
            "docs/governance/pre-1-0-revision-ledger.md",
            "docs/operations/release-process.md",
            "docs/architecture/development-center.md",
        ):
            with self.subTest(rel=rel):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn("G118", text)
                self.assertIn("G119", text)
                self.assertIn("DEV.2 R6", text)

    def test_readme_estructura_refleja_directorios_versionados_clave(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for fragment in (
            "├── .githooks/",
            "├── .github/",
            "├── scripts/",
            "├── tests/",
            "├── SECURITY.md",
            "├── SUPPORT.md",
            "├── THIRD_PARTY_NOTICES.md",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, readme)
        self.assertNotIn("├── _deliverables/", readme)
        self.assertNotIn("├── .venv/", readme)

    def test_trazabilidad_documenta_portal_developer_r5(self):
        trace = (ROOT / "docs/product/traceability-matrix.md").read_text(encoding="utf-8")
        self.assertIn("TR-029", trace)
        self.assertIn("Portal Developer", trace)
        self.assertIn("G118/E04", trace)


if __name__ == "__main__":
    unittest.main()
