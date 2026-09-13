"""Regresiones de la política estructural NOR.3 R2."""

from pathlib import Path
import json
import unittest

from scripts import audit_pr_policy as pr_policy
from scripts import audit_repository_integrity as audit


ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "data" / "governance" / "repository-structure-policy.json"
QUALITY_GATE = ROOT / "scripts" / "quality_gate.py"


class TestNOR3R2RepositoryStructurePolicy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads(
            POLICY_PATH.read_text(encoding="utf-8")
        )

    def test_policy_machine_readable_existe(self):
        self.assertEqual(self.policy["schema_version"], 1)
        self.assertEqual(self.policy["phase"], "NOR.3 R2")

    def test_raices_autorizadas_son_explicitas(self):
        self.assertEqual(
            set(self.policy["allowed_root_directories"]),
            {
                ".githooks",
                ".github",
                ".vscode",
                "app",
                "assets",
                "data",
                "docs",
                "regulations",
                "scripts",
                "tests",
            },
        )

    def test_excepciones_de_profundidad_regulatoria(self):
        exceptions = {
            item["prefix"]: item
            for item in self.policy["depth_policy"]["exceptions"]
        }
        expected = {
            "docs/regulatory/sources/official/pensions/normative/",
            "docs/regulatory/sources/official/pensions/reference/",
            "docs/regulatory/sources/official/privacy/normative/",
        }
        self.assertEqual(set(exceptions), expected)

        for item in exceptions.values():
            self.assertEqual(item["max_depth"], 6)
            self.assertTrue(item["reason"].strip())

    def test_data_developer_es_local(self):
        self.assertIn(
            "data/developer/",
            self.policy["forbidden_versioned_prefixes"],
        )

    def test_workspace_actual_cumple_policy(self):
        files = audit.repository_files()
        directories = audit.canonical_directories(files)
        blockers = audit.structure_policy_analysis(
            files,
            directories,
            audit.load_structure_policy(),
        )
        self.assertTrue(
            all(not values for values in blockers.values()),
            blockers,
        )

    def test_detecta_raiz_no_autorizada(self):
        files = audit.repository_files() + [
            "intruder/file.txt"
        ]
        blockers = audit.structure_policy_analysis(
            files,
            audit.canonical_directories(files),
            audit.load_structure_policy(),
        )
        self.assertIn(
            "intruder",
            blockers["policy_unknown_root_directories"],
        )

    def test_detecta_data_developer_versionado(self):
        files = audit.repository_files() + [
            "data/developer/users.sqlite"
        ]
        blockers = audit.structure_policy_analysis(
            files,
            audit.canonical_directories(files),
            audit.load_structure_policy(),
        )
        self.assertIn(
            "data/developer/users.sqlite",
            blockers["policy_forbidden_versioned_paths"],
        )

    def test_detecta_profundidad_no_autorizada(self):
        rel = "docs/architecture/a/b/c/d/e/f.txt"
        files = audit.repository_files() + [rel]
        blockers = audit.structure_policy_analysis(
            files,
            audit.canonical_directories(files),
            audit.load_structure_policy(),
        )
        self.assertTrue(
            any(
                rel in item
                for item in blockers["policy_depth_violations"]
            )
        )

    def test_integridad_incorpora_policy(self):
        report = audit.audit_repository()

        for key in (
            "policy_unknown_root_directories",
            "policy_missing_required_paths",
            "policy_forbidden_versioned_paths",
            "policy_forbidden_artifacts",
            "policy_depth_violations",
        ):
            with self.subTest(key=key):
                self.assertIn(key, report["blockers"])

        self.assertEqual(report["result"], "pass")

    def test_post_promocion_cierra_scope_r1_r8(self):
        registry = json.loads(
            (
                ROOT / "data" / "governance"
                / "work-block-registry.json"
            ).read_text(encoding="utf-8")
        )

        candidate = registry["current_candidate"]
        self.assertIsNone(candidate["global_revision"])
        self.assertIsNone(candidate["revision_aware"])
        self.assertIsNone(candidate["block"])
        self.assertIsNone(candidate["revision"])
        self.assertIsNone(candidate["revision_scope"])
        self.assertEqual(
            "unassigned_pending_replanning",
            candidate["state"],
        )

        ids = {
            item["identifier"]: item
            for item in registry["identifiers"]
        }
        self.assertEqual("closed", ids["NOR.3"]["status"])
        self.assertEqual("R1-R8", ids["NOR.3"]["active_scope"])
        self.assertEqual(["G122"], ids["NOR.3"]["global_refs"])

    def test_pr_policy_permite_candidato_sin_version(self):
        files = [
            "data/governance/pre-1-0-revision-ledger.json",
            "data/governance/release-publication-manifest.json",
        ]

        self.assertEqual(
            [],
            pr_policy.revision_state_errors(files),
        )

    def test_pr_policy_exige_metadata_si_cambia_version(self):
        errors = pr_policy.revision_state_errors(
            ["VERSION"]
        )

        self.assertEqual(len(errors), 1)
        self.assertIn(
            "pre-1-0-revision-ledger.json",
            errors[0],
        )
        self.assertIn(
            "release-publication-manifest.json",
            errors[0],
        )

    def test_pr_policy_rechaza_metadata_parcial(self):
        errors = pr_policy.revision_state_errors(
            [
                "data/governance/pre-1-0-revision-ledger.json"
            ]
        )

        self.assertEqual(len(errors), 1)
        self.assertIn(
            "release-publication-manifest.json",
            errors[0],
        )
        self.assertEqual(
            (
                "Los metadatos revision-aware de candidato deben "
                "cambiar de forma coordinada cuando VERSION "
                "permanece estable. Faltan: "
                "data/governance/release-publication-manifest.json"
            ),
            errors[0],
        )

    def test_quality_gate_hereda_integridad(self):
        text = QUALITY_GATE.read_text(encoding="utf-8")
        self.assertIn(
            "scripts/audit_repository_integrity.py",
            text,
        )


if __name__ == "__main__":
    unittest.main()
