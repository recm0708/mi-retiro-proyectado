"""Regresiones de la promoción NOR.1 R8 -> G112/E07."""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]


class TestG112PromotionPostMerge(unittest.TestCase):
    def test_g112_permanece_preservado_en_ledger(self):
        ledger = cargar_ledger()
        entry = next(x for x in ledger["entries"] if x["global_revision"] == 112)
        self.assertEqual("NOR.1", entry["block"])
        self.assertEqual(7, entry["ordinal"])
        self.assertEqual("0.1.12.07-beta", entry["revision_aware"])
        self.assertIn("PR #89", entry["evidence"])
        self.assertIn("PR #90", entry["evidence"])

    def test_registro_preserva_nor1_y_avanza_candidato(self):
        data = json.loads((ROOT / "data/work-block-registry.json").read_text(encoding="utf-8"))
        ids = {x["identifier"]: x for x in data["identifiers"]}
        candidate = data["current_candidate"]
        self.assertEqual("closed", ids["NOR.1"]["status"])
        self.assertIn("G112", ids["NOR.1"]["global_refs"])
        self.assertEqual("closed", ids["DOC.1"]["status"])
        self.assertIn("G113", ids["DOC.1"]["global_refs"])
        self.assertEqual(114, candidate["global_revision"])
        self.assertEqual("PERSIST.1", candidate["block"])
        self.assertEqual("R1", candidate["revision"])
        self.assertEqual(1, candidate["edition"])

    def test_documentacion_viva_no_asocia_nor1_r8_con_e01(self):
        files = (
            "README.md", "RELEASES.md", "VERSIONING.md", "GOVERNANCE.md",
            "CONTRIBUTING.md", "SECURITY.md", "docs/README.md",
            "docs/governance/master-plan-to-1-0.md", "docs/governance/roadmap.md",
            "docs/governance/pre-1-0-revision-ledger.md", "docs/operations/validation.md",
            "docs/standards/work-block-identifiers.md",
        )
        bad = re.compile(r"NOR\.1 R8.*(?:G112/E01|0\.1\.12\.01-beta)|(?:G112/E01|0\.1\.12\.01-beta).*NOR\.1 R8")
        findings = []
        for rel in files:
            for lineno,line in enumerate((ROOT / rel).read_text(encoding="utf-8").splitlines(), start=1):
                if bad.search(line): findings.append(f"{rel}:{lineno}")
        self.assertEqual([], findings)

    def test_historia_doc2_puede_conservar_e01_para_persist1(self):
        validation = (ROOT / "docs/operations/validation.md").read_text(encoding="utf-8")
        self.assertIn("0.1.12.01-beta", validation)
        self.assertIn("next_candidate_block = PERSIST.1", validation)


if __name__ == "__main__":
    unittest.main()
