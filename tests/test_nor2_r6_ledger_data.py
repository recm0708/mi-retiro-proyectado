"""Regresiones NOR.2 R6 — migración del ledger y datos de alto impacto."""

from pathlib import Path
import hashlib
import json
import subprocess
import unittest

from app.core.version_ledger import LEDGER_FILE, cargar_ledger


ROOT = Path(__file__).resolve().parents[1]

OLD = ROOT / "data/revision_ledger_pre_1_0.json"
NEW = ROOT / "data/pre-1-0-revision-ledger.json"

EXPECTED_SHA256 = (
    "f5e0020643b324119855693588469eb8c98a0abafdb8f6108d60d5fb03a2288e"
)


class TestNOR2R6LedgerData(unittest.TestCase):

    def test_ruta_normalizada(self):
        self.assertFalse(OLD.exists())
        self.assertTrue(NEW.is_file())
        self.assertEqual(NEW.resolve(), LEDGER_FILE.resolve())

    def test_contenido_permanece_identico(self):
        digest = hashlib.sha256(NEW.read_bytes()).hexdigest()
        self.assertEqual(EXPECTED_SHA256, digest)

    def test_invariantes_del_ledger(self):
        raw = json.loads(NEW.read_text(encoding="utf-8"))

        self.assertEqual(1, raw["schema_version"])
        self.assertEqual(70, raw["accepted_count"])
        self.assertEqual(70, len(raw["entries"]))
        self.assertEqual(71, raw["next_global_if_ver2_accepted"])
        self.assertEqual("0.0.71.01-beta", raw["next_candidate"])

        globales = [
            item["global_revision"]
            for item in raw["entries"]
        ]

        self.assertEqual(list(range(1, 71)), globales)

        # También ejecuta el validador canónico del proyecto.
        validado = cargar_ledger()
        self.assertEqual(70, validado["accepted_count"])

    def test_no_quedan_consumidores_vivos_de_ruta_anterior(self):
        old_path = "data/revision_ledger_pre_1_0.json"
        old_name = "revision_ledger_pre_1_0.json"

        allowed = {
            "tests/test_mant1_r5f_nombres_archivos.py",
            "tests/test_nor2_r2_migration_matrix.py",
            "tests/test_nor2_r6_ledger_data.py",
        }

        result = subprocess.run(
            ["git", "ls-files"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        findings = []

        for rel in result.stdout.splitlines():
            if (
                rel.startswith("docs/archive/")
                or rel.startswith("docs/audits/")
                or rel in allowed
            ):
                continue

            path = ROOT / rel

            if not path.is_file():
                continue

            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            if old_path in text or old_name in text:
                findings.append(rel)

        self.assertEqual([], findings)

    def test_estado_transversal(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        docs = (ROOT / "docs/README.md").read_text(encoding="utf-8")

        self.assertIn("**NOR.2 R5:** cerrado", readme)
        self.assertIn("**NOR.2 R6:** activo", readme)
        self.assertIn("NOR.2 R6", docs)
        self.assertIn("NOR.2 R7", docs)
        self.assertIn("**SEC.2:** pausado", readme)

    def test_version_no_cambia(self):
        self.assertEqual(
            "0.0.71.01-beta",
            (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        )


if __name__ == "__main__":
    unittest.main()
