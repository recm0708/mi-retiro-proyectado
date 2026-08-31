"""Regresiones REL.GOV.1 R2 para publicación determinista."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "release_publication.py"
MANIFEST = ROOT / "data/release-publication-manifest.json"

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

    def test_manifest_actual_es_g119_y_apunta_a_g120(self):
        data = json.loads(
            MANIFEST.read_text(encoding="utf-8")
        )
        self.assertEqual(
            "0.1.19.05-beta",
            data["version"],
        )
        self.assertEqual("DEV.2", data["block"])
        self.assertEqual("R6", data["revision"])
        self.assertEqual(
            120,
            data["next_step"]["global_revision"],
        )
        self.assertEqual(
            "0.1.20.01-beta",
            data["next_step"]["revision_aware"],
        )
        self.assertEqual(
            "UX.5",
            data["next_step"]["block"],
        )

    def test_manifiesto_supera_validacion(self):
        result = self.run_script("--check-manifest")
        self.assertEqual(
            0,
            result.returncode,
            result.stdout + result.stderr,
        )
        self.assertIn(
            "G119/E05 validado",
            result.stdout,
        )

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
            "G119/E05",
            "DEV.2 R6",
            PUBLISHED_COMMIT,
            TAG_OBJECT,
            "**G120/E01**",
            "`0.1.20.01-beta`",
            "UX.5",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_manifiesto_contiene_evidencia_g119(self):
        data = json.loads(
            MANIFEST.read_text(encoding="utf-8")
        )
        corpus = json.dumps(
            data,
            ensure_ascii=False,
        )
        for fragment in (
            "PR #111",
            "bd2accbea421fc719d9330015533001039648d05",
            "1309 passed / 6045 subtests passed",
            "1269 tests `unittest` OK",
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
                        "tagName": "v0.1.19.05-beta",
                        "name": (
                            "Mi Retiro Proyectado "
                            "v0.1.19.05-beta — G119/E05"
                        ),
                        "isDraft": False,
                        "isPrerelease": True,
                        "body": notes.read_text(
                            encoding="utf-8"
                        ),
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
            data = json.loads(
                MANIFEST.read_text(encoding="utf-8")
            )
            data["version"] = "0.1.18.04-beta"

            stale.write_text(
                json.dumps(
                    data,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            result = self.run_script(
                "--manifest",
                str(stale),
                "--check-manifest",
            )

        self.assertNotEqual(0, result.returncode)
        self.assertIn(
            "no corresponde a VERSION",
            result.stdout,
        )


if __name__ == "__main__":
    unittest.main()
