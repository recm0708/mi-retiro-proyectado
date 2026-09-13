"""NOR.3 R7 — ownership permanente de data y scripts."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
SCRIPTS = ROOT / "scripts"

EXPECTED_DATA = {
    "data/audits/doc2-legacy-changelog-evidence.json",
    "data/audits/git-history-attestation.json",
    "data/governance/pre-1-0-revision-ledger.json",
    "data/governance/release-publication-manifest.json",
    "data/governance/repository-structure-policy.json",
    "data/governance/work-block-registry.json",
}


class TestNOR3R7DataAndScripts(unittest.TestCase):
    def test_data_tiene_solo_owners_canonicos(self):
        actual = {
            line.strip().replace(chr(92), "/")
            for line in subprocess.run(
                ["git", "ls-files", "data"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            ).stdout.splitlines()
            if line.strip()
        }
        self.assertEqual(EXPECTED_DATA, actual)

    def test_data_no_tiene_raiz_plana_y_gitkeep(self):
        self.assertEqual([], list(DATA.glob("*.json")))
        self.assertFalse((DATA / ".gitkeep").exists())

    def test_data_developer_es_local_ignorado_no_versionado(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("data/developer/", gitignore)

        tracked = subprocess.run(
            ["git", "ls-files", "data/developer"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()

        self.assertEqual("", tracked)

    def test_policy_activa_ownership_r7(self):
        policy = json.loads(
            (
                DATA
                / "governance"
                / "repository-structure-policy.json"
            ).read_text(encoding="utf-8")
        )
        data_contract = policy["data_ownership_contract"]
        scripts_contract = policy["scripts_ownership_contract"]

        self.assertTrue(data_contract["enforced"])
        self.assertEqual("NOR.3 R7", data_contract["activation"])
        self.assertEqual(
            ["data/audits", "data/governance"],
            data_contract["versioned_roots"],
        )
        self.assertIn(
            "data/developer",
            data_contract["forbidden_versioned_roots"],
        )
        self.assertIn(
            "data/developer",
            data_contract["local_ignored_roots"],
        )
        self.assertFalse(data_contract["root_files_allowed"])
        self.assertFalse(data_contract["gitkeep_allowed"])

        self.assertTrue(scripts_contract["enforced"])
        self.assertEqual("flat_entry_points", scripts_contract["layout"])
        self.assertFalse(scripts_contract["nested_directories_allowed"])
        self.assertIn(
            "scripts/node_modules",
            scripts_contract["local_ignored_directories"],
        )

    def test_scripts_versionados_permanecen_planos(self):
        tracked = [
            line.strip().replace(chr(92), "/")
            for line in subprocess.run(
                ["git", "ls-files", "scripts"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=True,
            ).stdout.splitlines()
            if line.strip()
        ]
        nested = [
            path
            for path in tracked
            if path.count("/") > 1
        ]
        self.assertEqual([], nested)


if __name__ == "__main__":
    unittest.main()
