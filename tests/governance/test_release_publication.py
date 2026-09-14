"""Regresiones REL.GOV.1 R2 para publicación determinista."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "release_publication.py"
MANIFEST = ROOT / "data/governance/release-publication-manifest.json"

PUBLISHED_COMMIT = "1111111111111111111111111111111111111111"
TAG_OBJECT = "2222222222222222222222222222222222222222"


class TestReleasePublication(unittest.TestCase):
    def run_script(
        self,
        *args: str,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
        )

    def render(self, output: Path) -> None:
        result = self.run_script(
            "--render-notes",
            str(output),
            "--published-commit",
            PUBLISHED_COMMIT,
            "--tag-object",
            TAG_OBJECT,
        )
        self.assertEqual(
            0,
            result.returncode,
            result.stdout + result.stderr,
        )

    def test_manifest_actual_es_g124_y_no_preasigna_g125(self):
        data = json.loads(
            MANIFEST.read_text(encoding="utf-8")
        )
        self.assertEqual("0.1.24.13-beta", data["version"])
        self.assertEqual("MANT.1", data["block"])
        self.assertEqual("R8", data["revision"])
        self.assertEqual(125, data["next_step"]["global_revision"])
        self.assertIsNone(data["next_step"]["revision_aware"])
        self.assertIsNone(data["next_step"]["block"])

    def test_manifiesto_supera_validacion(self):
        result = self.run_script("--check-manifest")
        self.assertEqual(
            0,
            result.returncode,
            result.stdout + result.stderr,
        )
        self.assertIn("G124/E13 validado", result.stdout)

    def test_renderer_incluye_campos_dinamicos_y_secciones(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "notes.md"
            self.render(output)
            text = output.read_text(encoding="utf-8")

        for fragment in (
            "## Estado publicado",
            "## Resumen",
            "## Cambios principales",
            "## Validación",
            "## Evidencia",
            "## Siguiente paso",
            "G124/E13",
            "MANT.1 R8",
            PUBLISHED_COMMIT,
            TAG_OBJECT,
            "**G125**",
            "`0.1.24.13-beta`",
            "MANT.1",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_manifiesto_contiene_evidencia_mant2(self):
        data = json.loads(
            MANIFEST.read_text(encoding="utf-8")
        )
        corpus = json.dumps(data, ensure_ascii=False)

        for fragment in (
            "Issue de fase: #163",
            "16 scripts operativos",
            "219 módulos",
            "Taxonomía remota: 28 labels",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, corpus)

    def test_release_existente_identico_es_idempotente(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            notes = root / "notes.md"
            snapshot = root / "release.json"
            self.render(notes)

            snapshot.write_text(
                json.dumps(
                    {
                        "tagName": "v0.1.24.13-beta",
                        "name": (
                            "Mi Retiro Proyectado "
                            "v0.1.24.13-beta — G124/E13"
                        ),
                        "isDraft": False,
                        "isPrerelease": True,
                        "body": notes.read_text(encoding="utf-8"),
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            result = self.run_script(
                "--check-release-json",
                str(snapshot),
                "--notes",
                str(notes),
            )

        self.assertEqual(
            0,
            result.returncode,
            result.stdout + result.stderr,
        )
        self.assertIn("idempotente", result.stdout)

    def test_manifiesto_obsoleto_falla_cerrado(self):
        with tempfile.TemporaryDirectory() as tmp:
            stale = Path(tmp) / "manifest.json"
            data = json.loads(MANIFEST.read_text(encoding="utf-8"))
            data["version"] = "0.1.20.01-beta"

            stale.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

            result = self.run_script(
                "--manifest",
                str(stale),
                "--check-manifest",
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn("no corresponde a VERSION", result.stdout)


if __name__ == "__main__":
    unittest.main()
