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

    def test_version_permanece_en_g071_e01(self):
        version = (
            ROOT / "VERSION"
        ).read_text(
            encoding="utf-8"
        ).strip()

        self.assertEqual(
            "0.0.71.01-beta",
            version,
        )

        self.assertEqual(
            version,
            APP_VERSION,
        )

    def test_ledger_permanece_canonico_e_inmutable(self):
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

        self.assertEqual(
            70,
            raw["accepted_count"],
        )

        self.assertEqual(
            70,
            len(raw["entries"]),
        )

        self.assertEqual(
            list(range(1, 71)),
            [
                item["global_revision"]
                for item in raw["entries"]
            ],
        )

        self.assertEqual(
            71,
            raw["next_global_if_ver2_accepted"],
        )

        self.assertEqual(
            "0.0.71.01-beta",
            raw["next_candidate"],
        )

    def test_estado_documental_vigente_es_r8(self):
        readme = (
            ROOT / "README.md"
        ).read_text(encoding="utf-8")

        docs = (
            ROOT / "docs/README.md"
        ).read_text(encoding="utf-8")

        traceability = (
            ROOT
            / "docs/product/traceability-matrix.md"
        ).read_text(encoding="utf-8")

        for text in (
            readme,
            docs,
            traceability,
        ):
            self.assertIn(
                "NOR.2 R7",
                text,
            )
            self.assertIn(
                "NOR.2 R8",
                text,
            )

        self.assertIn(
            "**NOR.2 R7:** cerrado",
            readme,
        )

        self.assertIn(
            "**NOR.2 R8:** activo",
            readme,
        )

        self.assertIn(
            "**SEC.2:** pausado",
            readme,
        )

        self.assertIn(
            "NOR.2 R8 — auditoría integral",
            docs,
        )

        self.assertIn(
            "NOR.2 R8 permanece activo",
            traceability,
        )

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
            "docs/governance/master-plan-to-1-0.md": "Actualización NOR.2 R8",
            "docs/README.md": "repository-normalization-final-audit-nor2-r8.md",
        }

        for rel, value in expected.items():
            with self.subTest(rel=rel):
                text = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn(value, text)

if __name__ == "__main__":
    unittest.main()
