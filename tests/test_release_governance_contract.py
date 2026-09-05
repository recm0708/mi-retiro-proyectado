"""Regresiones REL.GOV.1 para el contrato de tags y Releases."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "release_contract.py"


class TestReleaseGovernanceContract(unittest.TestCase):
    def run_contract(
        self,
        *args: str,
        child_encoding: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        if child_encoding is not None:
            env["PYTHONIOENCODING"] = child_encoding

        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            encoding="utf-8",
            env=env,
        )

    def test_salida_cli_es_utf8_aun_con_pipe_windows_legacy(self):
        result = self.run_contract(
            "--json",
            child_encoding="cp1252",
        )
        self.assertEqual(
            0,
            result.returncode,
            result.stdout + result.stderr,
        )
        data = json.loads(result.stdout)
        self.assertEqual(
            "Mi Retiro Proyectado v0.1.20.01-beta — G120/E01",
            data["title"],
        )

    def test_contrato_actual_deriva_titulo_g119(self):
        result = self.run_contract("--json")
        self.assertEqual(
            0,
            result.returncode,
            result.stdout + result.stderr,
        )

        data = json.loads(result.stdout)
        self.assertEqual("0.1.20.01-beta", data["version"])
        self.assertEqual("v0.1.20.01-beta", data["tag"])
        self.assertEqual(120, data["global_revision"])
        self.assertEqual(1, data["edition"])
        self.assertEqual(
            "Mi Retiro Proyectado v0.1.20.01-beta — G120/E01",
            data["title"],
        )
        self.assertTrue(data["prerelease"])
        self.assertEqual(120, data["accepted_count"])
        self.assertEqual(121, data["next_global"])
        self.assertEqual(
            "0.1.21.01-beta",
            data["next_candidate"],
        )
        self.assertEqual(
            "UX.6",
            data["next_candidate_block"],
        )

    def test_tag_debe_coincidir_con_version(self):
        ok = self.run_contract(
            "--check-tag",
            "v0.1.20.01-beta",
        )
        self.assertEqual(
            0,
            ok.returncode,
            ok.stdout + ok.stderr,
        )

        bad = self.run_contract(
            "--check-tag",
            "v0.1.19.05-beta",
        )
        self.assertNotEqual(0, bad.returncode)
        self.assertIn("Tag inválido", bad.stdout)

    def test_titulo_debe_ser_canonico(self):
        title = (
            "Mi Retiro Proyectado "
            "v0.1.20.01-beta — G120/E01"
        )
        ok = self.run_contract(
            "--check-title",
            title,
        )
        self.assertEqual(
            0,
            ok.returncode,
            ok.stdout + ok.stderr,
        )

    def test_notas_requieren_secciones_minimas(self):
        good = "\n\n".join(
            (
                "## Estado publicado\n- Versión: prueba",
                "## Resumen\nResumen.",
                "## Cambios principales\n- Cambio.",
                "## Validación\n- OK.",
                "## Evidencia\n- PR.",
                "## Siguiente paso\nSiguiente.",
            )
        )
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "notes.md"
            file.write_text(good, encoding="utf-8")
            ok = self.run_contract(
                "--check-notes",
                str(file),
            )
            self.assertEqual(
                0,
                ok.returncode,
                ok.stdout + ok.stderr,
            )

    def test_workflow_valida_firma_y_contrato(self):
        workflow = (
            ROOT / ".github/workflows/verificar-tags.yml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            'git tag -v "$GITHUB_REF_NAME"',
            workflow,
        )
        self.assertIn(
            'python scripts/release_contract.py '
            '--check-tag "$GITHUB_REF_NAME"',
            workflow,
        )

    def test_release_yml_configura_categorias(self):
        text = (
            ROOT / ".github/release.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("changelog:", text)
        self.assertIn("Seguridad y privacidad", text)

    def test_politica_documenta_formato_y_publicacion(self):
        text = (
            ROOT / "docs/operations/release-process.md"
        ).read_text(encoding="utf-8")
        for fragment in (
            "Mi Retiro Proyectado v<VERSION> — GNNN/ENN",
            "## Estado publicado",
            "## Resumen",
            "## Cambios principales",
            "## Validación",
            "## Evidencia",
            "## Siguiente paso",
            "todo tag formal nuevo",
            "no recibe un Release retroactivo",
            "gh release edit",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_g120_aceptado_y_g121_reservado_para_ux6(self):
        ledger = json.loads(
            (
                ROOT / "data/pre-1-0-revision-ledger.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(120, ledger["accepted_count"])
        self.assertEqual(121, ledger["next_global"])
        self.assertEqual(
            "0.1.21.01-beta",
            ledger["next_candidate"],
        )
        self.assertEqual(
            "UX.6",
            ledger["next_candidate_block"],
        )
        self.assertEqual(
            "0.1.20.01-beta",
            (ROOT / "VERSION").read_text(
                encoding="utf-8"
            ).strip(),
        )


if __name__ == "__main__":
    unittest.main()
