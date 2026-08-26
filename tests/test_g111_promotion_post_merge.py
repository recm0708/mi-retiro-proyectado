"""Regresiones de la promoción post-merge G111/E01."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG111PromotionPostMerge(unittest.TestCase):
    def test_version_y_runtime_materializan_g111(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.11.01-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((111, 1), descomponer_version_beta_revision(version))

    def test_ledger_preserva_g111_doc2_y_deja_g112_sin_consumir(self):
        ledger = cargar_ledger()
        self.assertEqual(111, ledger["accepted_count"])
        self.assertEqual(112, ledger["next_global"])
        self.assertEqual("1041b5938607b4616c6af6e6847d6e2fbc8b6ec7", ledger["reconciled_through_commit"])
        self.assertEqual("DOC.2", ledger["entries"][-1]["block"])
        self.assertIn("PR #87", ledger["entries"][-1]["evidence"])

    def test_evidencia_doc2_marca_g111_aceptado(self):
        data = json.loads(
            (ROOT / "data/doc2-legacy-changelog-evidence.json").read_text(encoding="utf-8")
        )
        self.assertTrue(data["reserved_candidate"]["consumed"])
        self.assertEqual(111, data["accepted_state"]["global_revision"])
        self.assertEqual(87, data["accepted_state"]["pull_request"])

    def test_documentacion_declara_g112_sin_consumirlo(self):
        for rel in (
            "README.md",
            "RELEASES.md",
            "CONTRIBUTING.md",
            "GOVERNANCE.md",
            "VERSIONING.md",
            "docs/README.md",
            "docs/governance/roadmap.md",
            "docs/governance/pre-1-0-revision-ledger.md",
            "docs/product/traceability-matrix.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("G111", text)
            self.assertIn("G112", text)
            self.assertIn("PERSIST.1", text)

        audit = (
            ROOT
            / "docs/audits/documentation/changelog-reconstruction-doc2-r1.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "**Versión vigente durante la revisión:** `0.1.10.01-beta` — G110/E01",
            audit,
        )


if __name__ == "__main__":
    unittest.main()
