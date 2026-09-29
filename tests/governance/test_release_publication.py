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
LEDGER = ROOT / "data/governance/pre-1-0-revision-ledger.json"
PUBLISHED_COMMIT = "1111111111111111111111111111111111111111"
TAG_OBJECT = "2222222222222222222222222222222222222222"


class TestReleasePublication(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
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
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def current(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
        return manifest, ledger

    def test_manifest_actual_coincide_con_ledger_y_deja_siguiente_libre(self):
        data, ledger = self.current()
        last = ledger["entries"][-1]
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, data["version"])
        self.assertEqual(last["global_revision"], data["global_revision"])
        self.assertEqual(last["edition"], data["edition"])
        self.assertEqual(last["identifier_schema"], data["identifier_schema"])
        self.assertEqual(last["correction_ordinal"], data["correction_ordinal"])
        self.assertEqual(last["maintenance_ordinal"], data["maintenance_ordinal"])
        self.assertEqual(last["block"], data["block"])
        self.assertEqual(last["functional_revision"], data["revision"])
        self.assertEqual(ledger["next_global"], data["next_step"]["global_revision"])
        self.assertIsNone(data["next_step"]["revision_aware"])
        self.assertIsNone(data["next_step"]["block"])

    def test_manifiesto_supera_validacion(self):
        data, _ = self.current()
        result = self.run_script("--check-manifest")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn(
            f"G{data['global_revision']}/E{data['edition']:02d} validado",
            result.stdout,
        )

    def test_renderer_incluye_campos_dinamicos_y_secciones(self):
        data, ledger = self.current()
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
            f"G{data['global_revision']}/E{data['edition']:02d}",
            f"{data['block']} {data['revision']}",
            PUBLISHED_COMMIT,
            TAG_OBJECT,
            f"**G{ledger['next_global']}**",
            f"`{data['version']}`",
            data["block"],
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_manifiesto_contiene_evidencia_mant2_r3(self):
        data, _ = self.current()
        corpus = json.dumps(data, ensure_ascii=False)
        for fragment in (
            "Issue #211",
            "Draft PR #212",
            "Política #203",
            "Preflight #166",
            "Baseline publicado G128/E02",
            "DOC.4 R1/#171",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, corpus)

    def test_release_existente_identico_es_idempotente(self):
        data, _ = self.current()
        title = (
            f"Mi Retiro Proyectado v{data['version']} — "
            f"G{data['global_revision']}/E{data['edition']:02d}"
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            notes = root / "notes.md"
            snapshot = root / "release.json"
            self.render(notes)
            snapshot.write_text(
                json.dumps(
                    {
                        "tagName": f"v{data['version']}",
                        "name": title,
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
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("idempotente", result.stdout)

    def test_manifiesto_obsoleto_falla_cerrado(self):
        with tempfile.TemporaryDirectory() as tmp:
            stale = Path(tmp) / "manifest.json"
            data = json.loads(MANIFEST.read_text(encoding="utf-8"))
            data["version"] = "0.1.24.13-beta"
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
