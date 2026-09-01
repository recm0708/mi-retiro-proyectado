"""Regresiones NOR.2 R8 — auditoría integral y cierre formal."""

from pathlib import Path
import json
import subprocess
import unittest

from app.core.config import APP_VERSION


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_ROOT_DIRS = {
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
}


def git_ls_files():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.splitlines()


class TestNOR2R8FinalAudit(unittest.TestCase):

    def test_raiz_versionada_cumple_estructura_canonica(self):
        tracked = git_ls_files()

        physical = [
            rel
            for rel in tracked
            if (ROOT / rel).exists()
        ]

        root_dirs = {
            rel.split("/", 1)[0]
            for rel in physical
            if "/" in rel
        }

        self.assertEqual(
            EXPECTED_ROOT_DIRS,
            root_dirs,
        )

    def test_docs_raiz_queda_solo_con_readme(self):
        files = sorted(
            p.name
            for p in (ROOT / "docs").iterdir()
            if p.is_file()
        )

        self.assertEqual(
            ["README.md"],
            files,
        )

        self.assertFalse(
            (ROOT / "docs/CHANGELOG_ADD_R5.txt").exists()
        )
        self.assertFalse(
            (ROOT / "docs/INDICE_ADD_R5.txt").exists()
        )

    def test_artefactos_locales_quedan_fuera_de_git(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

        self.assertIn("_deliverables/", gitignore)
        self.assertIn("_entregas/", gitignore)

        tracked = git_ls_files()

        leaked = [
            rel
            for rel in tracked
            if rel.startswith("_deliverables/")
            or rel.startswith("_entregas/")
        ]

        self.assertEqual(
            [],
            leaked,
        )

    def test_version_actual_permanece_canonica_sin_reescribir_g087(self):
        version = (
            ROOT / "VERSION"
        ).read_text(
            encoding="utf-8"
        ).strip()

        self.assertEqual(
            version,
            APP_VERSION,
        )

    def test_ledger_canonico_preserva_prefijo_historico_y_puede_evolucionar(self):
        new = (
            ROOT
            / "data"
            / "pre-1-0-revision-ledger.json"
        )

        old = (
            ROOT
            / "data"
            / "revision_ledger_pre_1_0.json"
        )

        self.assertTrue(
            new.is_file()
        )

        self.assertFalse(
            old.exists()
        )

        raw = json.loads(
            new.read_text(encoding="utf-8")
        )

        self.assertEqual(
            1,
            raw["schema_version"],
        )

        accepted = raw["accepted_count"]
        self.assertGreaterEqual(accepted, 109)

        self.assertEqual(
            accepted,
            len(raw["entries"]),
        )

        self.assertEqual(
            list(range(1, accepted + 1)),
            [
                item["global_revision"]
                for item in raw["entries"]
            ],
        )

        self.assertEqual(
            accepted + 1,
            raw["next_global_if_ver2_accepted"],
        )

        self.assertEqual(
            accepted + 1,
            raw["next_global"],
        )

    def test_estado_documental_preserva_r8_y_refleja_estado_posterior(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        docs = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        traceability = (
            ROOT / "docs/product/traceability-matrix.md"
        ).read_text(encoding="utf-8")
        ledger = json.loads(
            (ROOT / "data/pre-1-0-revision-ledger.json").read_text(
                encoding="utf-8"
            )
        )

        for text in (readme, docs, traceability):
            self.assertIn("NOR.2", text)

        self.assertIn("SEC.2", readme)
        self.assertIn("R1–R6", readme)
        self.assertIn("AUD.SEC2 R1", docs)
        self.assertIn("checkpoint histórico de NOR.2", traceability)

        entries = {
            item["global_revision"]: item
            for item in ledger["entries"]
        }
        self.assertEqual("AUD.SEC2", entries[109]["block"])
        self.assertEqual(1, entries[109]["ordinal"])
        self.assertEqual("0.1.09.01-beta", entries[109]["revision_aware"])

        evidence = (
            ROOT / "docs/audits/repository/repository-normalization-final-audit-nor2-r8.md"
        ).read_text(encoding="utf-8")
        self.assertIn("NOR.2 R8", evidence)

    def test_ver2_no_figura_como_pendiente_en_estado_vivo(self):
        live = [
            ROOT / "README.md",
            ROOT / "RELEASES.md",
            ROOT / "docs/README.md",
            ROOT / "docs/governance/roadmap.md",
            ROOT / "docs/governance/master-plan-to-1-0.md",
            ROOT / "docs/product/traceability-matrix.md",
        ]

        combined = "\n".join(
            path.read_text(
                encoding="utf-8"
            )
            for path in live
        )

        forbidden = (
            "bloque transversal en reconciliación pendiente",
            "es únicamente el candidato de VER.2",
            "NOR.2 R7:** activo",
            "NOR.2 R8:** activo",
            "NOR.2 R8:** siguiente revisión",
            "NOR.1 queda preparado para cierre",
            "tag formal legacy vigente hasta el cierre",
        )

        for value in forbidden:
            with self.subTest(value=value):
                self.assertNotIn(
                    value,
                    combined,
                )

        self.assertIn(
            "v0.0.71.01-beta",
            combined,
        )

    def test_no_queda_aplicador_temporal_r8(self):
        self.assertFalse(
            (ROOT / "apply_nor2_r8.py").exists()
        )


    def test_evidencia_formal_r8_existe(self):
        evidence = (
            ROOT
            / "docs"
            / "audits"
            / "repository"
            / "repository-normalization-final-audit-nor2-r8.md"
        )

        self.assertTrue(evidence.is_file())

        text = evidence.read_text(encoding="utf-8")

        for value in (
            "NOR.2 R8",
            "115 filas",
            "11 contradicciones",
            "G001–G070",
            "SEC.2 permanece pausado",
        ):
            with self.subTest(value=value):
                self.assertIn(value, text)

    def test_superficies_transversales_registran_r8(self):
        expected = {
            "CHANGELOG.md": "NOR.2 R8",
            "docs/operations/validation.md": "Validación NOR.2 R8",
            "docs/product/traceability-matrix.md": "Trazabilidad NOR.2 R8",
            "docs/governance/roadmap.md": "NOR.2 R8 — auditoría integral",
            "docs/governance/master-plan-to-1-0.md": "NOR.2 R8",
            "docs/README.md": "repository-normalization-final-audit-nor2-r8.md",
        }

        for rel, value in expected.items():
            with self.subTest(rel=rel):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn(value, text)

if __name__ == "__main__":
    unittest.main()
