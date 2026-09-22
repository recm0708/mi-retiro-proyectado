"""NOR.3 R8 — contrato permanente del cierre estructural."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
POLICY = ROOT / "data/governance/repository-structure-policy.json"
REGISTRY = ROOT / "data/governance/work-block-registry.json"
AUDIT = ROOT / "docs/audits/repository/nor3-r8-closure-audit.md"


class TestNOR3R8Closure(unittest.TestCase):
    def test_cierre_r8_preserva_g122_y_estado_actual(self):
        data = json.loads(
            REGISTRY.read_text(
                encoding="utf-8"
            )
        )

        candidate = data["current_candidate"]

        self.assertEqual(128, candidate["global_revision"])
        self.assertEqual("0.128.2.0-beta", candidate["revision_aware"])
        self.assertEqual("VER.2", candidate["block"])
        self.assertEqual("R6", candidate["revision"])
        self.assertEqual("final_revision_aware_reform", candidate["revision_scope"])
        self.assertEqual("accepted_pending_integration", candidate["state"])
        self.assertEqual(129, candidate["next_global_available"])

        identifiers = {
            item["identifier"]: item
            for item in data["identifiers"]
        }

        self.assertEqual(
            "closed",
            identifiers["NOR.3"]["status"],
        )
        self.assertEqual(
            "R1-R8",
            identifiers["NOR.3"]["active_scope"],
        )
        self.assertEqual(
            ["G122"],
            identifiers["NOR.3"]["global_refs"],
        )

        self.assertEqual(
            "closed",
            identifiers["DOC.3"]["status"],
        )
        self.assertEqual(
            ["G125"],
            identifiers["DOC.3"]["global_refs"],
        )

        self.assertEqual(
            "closed_r2",
            identifiers["MANT.2"]["status"],
        )
        self.assertEqual(
            "accepted_r6_pending_integration",
            identifiers["VER.2"]["status"],
        )

        active = data["active_phase"]

        self.assertEqual("VER.2", active["block"])
        self.assertEqual("R6", active["revision"])
        self.assertEqual(164, active["issue"])
        self.assertEqual("accepted_pending_integration", active["state"])
        self.assertEqual(128, active["global_revision"])

    def test_policy_declara_cierre_r8_sin_simular_auditoria_posterior(self):
        data = json.loads(POLICY.read_text(encoding="utf-8"))

        self.assertEqual("NOR.3 R2", data["phase"])
        self.assertEqual(
            "active_physical_ownership",
            data["status"],
        )

        closure = data["nor3_closure_contract"]
        self.assertTrue(closure["enforced"])
        self.assertEqual("R1-R8", closure["revision_scope"])
        self.assertEqual("G122/E01", closure["candidate_global"])
        self.assertEqual(
            "integrated_accepted_post_merge",
            closure["candidate_state"],
        )
        self.assertFalse(
            closure["post_nor3_transversal_audit"]["included_in_r8"]
        )

    def test_data_versionado_tiene_owners_r7(self):
        output = subprocess.run(
            ["git", "ls-files", "data"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout

        actual = {
            line.strip().replace(chr(92), "/")
            for line in output.splitlines()
            if line.strip()
        }

        expected = {
            "data/audits/doc2-legacy-changelog-evidence.json",
            "data/audits/git-history-attestation.json",
            "data/governance/pre-1-0-revision-ledger.json",
            "data/governance/release-publication-manifest.json",
            "data/governance/repository-structure-policy.json",
            "data/governance/work-block-registry.json",
        }

        self.assertEqual(expected, actual)

    def test_tests_no_regresan_a_raiz_plana(self):
        self.assertEqual([], list((ROOT / "tests").glob("test_*.py")))

    def test_auditoria_cierre_existe_y_declara_limite(self):
        text = AUDIT.read_text(encoding="utf-8")

        self.assertIn("NOR.3 R1–R8", text)
        self.assertIn("PR #162", text)
        self.assertIn("0.1.22.01-beta", text)
        self.assertIn("reservado/no aceptado", text)
        self.assertIn("auditoría transversal post-NOR.3", text)


if __name__ == "__main__":
    unittest.main()
