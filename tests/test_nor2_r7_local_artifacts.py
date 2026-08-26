"""Regresiones NOR.2 R7 — artefactos locales."""

from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]

EVIDENCE = (
    ROOT
    / "docs"
    / "audits"
    / "repository"
    / "repository-normalization-local-artifacts-nor2-r7.md"
)


class TestNOR2R7LocalArtifacts(unittest.TestCase):

    def test_directorios_locales_permanecen_ignorados(self):
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

        self.assertIn("_deliverables/", gitignore)
        self.assertIn("_entregas/", gitignore)

        tracked = subprocess.check_output(
            ["git", "ls-files"],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
        ).splitlines()

        self.assertFalse(
            any(
                rel.startswith("_deliverables/")
                or rel.startswith("_entregas/")
                for rel in tracked
            )
        )

    def test_estandar_declara_deliverables_canonico_local(self):
        standard = (
            ROOT
            / "docs"
            / "standards"
            / "root-and-local-artifacts.md"
        ).read_text(encoding="utf-8")

        self.assertIn("_deliverables/", standard)
        self.assertIn(
            "fue auditado y saneado durante NOR.2 R7",
            standard,
        )
        self.assertIn(
            "protección contra su reaparición accidental",
            standard,
        )

    def test_evidencia_r7_documenta_migracion(self):
        text = EVIDENCE.read_text(encoding="utf-8")

        self.assertIn("29 archivos", text)
        self.assertIn("9,874,828 bytes", text)
        self.assertIn(
            "**20 archivos únicos conservados**",
            text,
        )
        self.assertIn("_deliverables/dev2/", text)
        self.assertIn("_deliverables/ver2-r2/", text)

    def test_evidencia_r7_documenta_deduplicacion(self):
        text = EVIDENCE.read_text(encoding="utf-8")

        self.assertIn(
            "**8 duplicados exactos retirados**",
            text,
        )
        self.assertIn(
            "VER2_G071_R2_final_pre_commit.patch",
            text,
        )
        self.assertIn(
            "VER2_G071_R2_final_completo_pre_commit.patch",
            text,
        )

    def test_evidencia_r7_documenta_zip_reproducible(self):
        text = EVIDENCE.read_text(encoding="utf-8")

        self.assertIn(
            "VER2_PR35_NETO_929628d.zip",
            text,
        )
        self.assertIn("8,412,675 bytes", text)
        self.assertIn("archivos Git: **329**", text)
        self.assertIn("archivos ZIP: **329**", text)
        self.assertIn("contenido diferente: **0**", text)
        self.assertIn(
            "929628df38d4750fb103ffc79bdb81f8405535bb",
            text,
        )

    def test_matriz_r2_preserva_decision_historica(self):
        matrix = (
            ROOT
            / "docs"
            / "audits"
            / "repository"
            / "repository-normalization-migration-matrix-nor2-r2.md"
        ).read_text(encoding="utf-8")

        self.assertIn("_entregas/", matrix)
        self.assertIn("_deliverables/", matrix)
        self.assertIn("MIGRAR LOCAL", matrix)

    def test_version_y_estado_transversal(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        docs = (ROOT / "docs/README.md").read_text(encoding="utf-8")

        self.assertIn(
            "**NOR.2 R6:** cerrado",
            readme,
        )
        self.assertIn(
            "**NOR.2 R7:** cerrado",
            readme,
        )
        self.assertIn(
            "**NOR.2 R8:** cerrado",
            readme,
        )
        self.assertIn(
            "**NOR.2:** cerrado",
            readme,
        )
        self.assertIn(
            "**SEC.2:** R1 cerrado; hardening CodeQL del informe imprimible y normalización técnica de GitHub Actions completados.",
            readme,
        )

        self.assertIn("NOR.2 R7", docs)
        self.assertIn("NOR.2 R8", docs)
        self.assertIn("SEC.2 R1–R6", docs)
        self.assertIn("AUD.SEC2 R1", docs)

        version = (
            ROOT / "VERSION"
        ).read_text(encoding="utf-8").strip()

        self.assertEqual(
            "0.1.11.01-beta",
            version,
        )


if __name__ == "__main__":
    unittest.main()
