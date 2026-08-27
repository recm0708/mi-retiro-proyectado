"""Regresiones de saneamiento semántico DOC.1 R4."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestDOC1R4LiveStateSanitization(unittest.TestCase):
    def test_candidato_no_consume_g115(self):
        self.assertEqual(
            "0.1.14.01-beta",
            (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        )
        ledger = json.loads(
            (ROOT / "data/pre-1-0-revision-ledger.json").read_text(encoding="utf-8")
        )
        self.assertEqual(114, ledger["accepted_count"])
        self.assertEqual(115, ledger["next_global"])
        self.assertEqual("0.1.15.04-beta", ledger["next_candidate"])
        self.assertEqual("DOC.1", ledger["next_candidate_block"])

    def test_raiz_declara_g114_publicado(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        governance = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")

        self.assertIn("Último tag revision-aware publicado:** `v0.1.14.01-beta`", readme)
        self.assertIn("`v0.1.14.01-beta` es el último tag revision-aware publicado", governance)
        self.assertIn("`v0.1.14.01-beta` fue creado como tag anotado y firmado", changelog)
        self.assertIn("Último tag formal publicado: `v0.1.14.01-beta`", releases)
        self.assertIn("`v0.1.14.01-beta` está publicado, firmado y verificado", versioning)

    def test_security_solo_marca_g114_como_beta_vigente(self):
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn("| `0.1.14.01-beta` | Beta vigente G114/E01 publicada;", security)
        self.assertNotIn("Beta vigente G113/E03", security)
        self.assertNotIn("Beta vigente G111/E01", security)

    def test_release_ledger_y_roadmap_reflejan_g115_doc1(self):
        release_process = (ROOT / "docs/operations/release-process.md").read_text(encoding="utf-8")
        ledger_md = (ROOT / "docs/governance/pre-1-0-revision-ledger.md").read_text(encoding="utf-8")
        roadmap = (ROOT / "docs/governance/roadmap.md").read_text(encoding="utf-8")

        self.assertIn("G114/E01 publicado; DOC.1 R4 candidato G115/E04", release_process)
        self.assertIn("Git Tag Signature Verification` terminó en `success`", release_process)
        self.assertIn("| G115 | `0.1.15.04-beta` | DOC.1 R4", ledger_md)
        self.assertIn("G001–G114 y siguiente Global G115", roadmap)

    def test_estado_vivo_de_dev_y_plan_maestro_no_retrocede(self):
        dev = (ROOT / "docs/architecture/development-center.md").read_text(encoding="utf-8")
        plan = (ROOT / "docs/governance/master-plan-to-1-0.md").read_text(encoding="utf-8")

        self.assertIn("`VERSION` está sincronizado en `0.1.14.01-beta`", dev)
        self.assertIn("DOC.1 R4 es el candidato vigente G115/E04", plan)
        self.assertIn("PERSIST.1 como etapa posterior", plan)

    def test_historia_y_evidencia_quedan_preservadas(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        validation = (ROOT / "docs/operations/validation.md").read_text(encoding="utf-8")
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        index = (ROOT / "docs/README.md").read_text(encoding="utf-8")

        self.assertIn("`VERSION` permanece en `0.0.26-beta`", changelog)
        self.assertIn("`VERSION=0.1.13.03-beta`", validation)
        self.assertIn("Promoción G113/E03", releases)
        self.assertIn("documentation-live-state-doc1-r4.md", index)


if __name__ == "__main__":
    unittest.main()
