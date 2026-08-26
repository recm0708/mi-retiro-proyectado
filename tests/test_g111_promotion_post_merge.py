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
    def test_g111_permanece_materializado_en_ledger(self):
        ledger = cargar_ledger()
        entry = next(e for e in ledger["entries"] if e["global_revision"] == 111)
        self.assertEqual("0.1.11.01-beta", entry["revision_aware"])
        self.assertEqual("DOC.2", entry["block"])
        self.assertIn("PR #87", entry["evidence"])

    def test_ledger_preserva_g111_sin_congelar_el_candidato_futuro(self):
        ledger = cargar_ledger()
        entry = next(e for e in ledger["entries"] if e["global_revision"] == 111)
        self.assertEqual("DOC.2", entry["block"])
        self.assertEqual("0.1.11.01-beta", entry["revision_aware"])
        self.assertIn("PR #87", entry["evidence"])

    def test_evidencia_doc2_marca_g111_aceptado(self):
        data = json.loads(
            (ROOT / "data/doc2-legacy-changelog-evidence.json").read_text(encoding="utf-8")
        )
        self.assertTrue(data["reserved_candidate"]["consumed"])
        self.assertEqual(111, data["accepted_state"]["global_revision"])
        self.assertEqual(87, data["accepted_state"]["pull_request"])

    def test_documentacion_preserva_evidencia_historica_g111(self):
        audit = (ROOT / "docs/audits/documentation/changelog-reconstruction-doc2-r1.md").read_text(encoding="utf-8")
        self.assertIn("**Versión vigente durante la revisión:** `0.1.10.01-beta` — G110/E01", audit)
        self.assertIn("G111/E01", (ROOT / "RELEASES.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
