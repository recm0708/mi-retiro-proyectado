"""Regresiones de la promoción NOR.1 R8 -> G112/E07."""
from __future__ import annotations
import json,re,unittest
from pathlib import Path
from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger
ROOT=Path(__file__).resolve().parents[1]
class TestG112PromotionPostMerge(unittest.TestCase):
    def test_version_y_runtime_materializan_g112_e07(self):
        v=(ROOT/'VERSION').read_text(encoding='utf-8').strip(); self.assertEqual('0.1.12.07-beta',v); self.assertEqual(v,APP_VERSION); self.assertEqual((112,7),descomponer_version_beta_revision(v))
    def test_ledger_acepta_nor1_r8_y_reserva_doc1_r3(self):
        l=cargar_ledger(); self.assertEqual(112,l['accepted_count']); self.assertEqual(113,l['next_global']); self.assertEqual('0.1.13.03-beta',l['next_candidate']); self.assertEqual('DOC.1',l['next_candidate_block']); e=l['entries'][-1]; self.assertEqual((112,'NOR.1',7,'0.1.12.07-beta'),(e['global_revision'],e['block'],e['ordinal'],e['revision_aware'])); self.assertIn('PR #89',e['evidence']); self.assertIn('PR #90',e['evidence'])
    def test_registro_reserva_doc1_r3(self):
        d=json.loads((ROOT/'data/work-block-registry.json').read_text(encoding='utf-8')); c=d['current_candidate']; self.assertEqual((113,'DOC.1','R3',3),(c['global_revision'],c['block'],c['revision'],c['edition'])); self.assertEqual('PERSIST.1',c['next_functional_block_if_accepted']); ids={i['identifier']:i for i in d['identifiers']}; self.assertEqual('closed',ids['NOR.1']['status']); self.assertIn('G112',ids['NOR.1']['global_refs']); self.assertEqual('reopened_candidate_r3',ids['DOC.1']['status'])
    def test_documentacion_viva_no_asocia_nor1_r8_con_e01(self):
        files = (
            "README.md",
            "RELEASES.md",
            "VERSIONING.md",
            "GOVERNANCE.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "docs/README.md",
            "docs/governance/master-plan-to-1-0.md",
            "docs/governance/roadmap.md",
            "docs/governance/pre-1-0-revision-ledger.md",
            "docs/operations/validation.md",
            "docs/standards/work-block-identifiers.md",
        )
        bad = re.compile(
            r"NOR\.1 R8.*(?:G112/E01|0\.1\.12\.01-beta)"
            r"|(?:G112/E01|0\.1\.12\.01-beta).*NOR\.1 R8"
        )
        findings = []
        for rel in files:
            for lineno, line in enumerate(
                (ROOT / rel).read_text(encoding="utf-8").splitlines(),
                start=1,
            ):
                if bad.search(line):
                    findings.append(f"{rel}:{lineno}")
        self.assertEqual([], findings)

    def test_historia_doc2_puede_conservar_e01_para_persist1(self):
        v=(ROOT/'docs/operations/validation.md').read_text(encoding='utf-8'); self.assertIn('0.1.12.01-beta',v); self.assertIn('next_candidate_block = PERSIST.1',v)
if __name__=='__main__': unittest.main()
