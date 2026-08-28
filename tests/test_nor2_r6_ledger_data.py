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
HISTORICAL_G070 = ROOT / "docs/archive/governance/pre-1-0-revision-ledger-g070.json"

EXPECTED_SHA256 = (
    "f5e0020643b324119855693588469eb8c98a0abafdb8f6108d60d5fb03a2288e"
)


class TestNOR2R6LedgerData(unittest.TestCase):

    def test_ruta_normalizada(self):
        self.assertFalse(OLD.exists())
        self.assertTrue(NEW.is_file())
        self.assertEqual(NEW.resolve(), LEDGER_FILE.resolve())

    def test_snapshot_historico_g070_permanece_identico(self):
        self.assertTrue(HISTORICAL_G070.is_file())
        digest = hashlib.sha256(HISTORICAL_G070.read_bytes()).hexdigest()
        self.assertEqual(EXPECTED_SHA256, digest)

    def test_invariantes_del_ledger(self):
        raw = json.loads(NEW.read_text(encoding="utf-8"))

        self.assertEqual(1, raw["schema_version"])
        accepted = raw["accepted_count"]
        self.assertGreaterEqual(accepted, 109)
        self.assertEqual(accepted, len(raw["entries"]))
        self.assertEqual(accepted + 1, raw["next_global_if_ver2_accepted"])
        self.assertEqual(accepted + 1, raw["next_global"])

        globales = [
            item["global_revision"]
            for item in raw["entries"]
        ]

        self.assertEqual(list(range(1, accepted + 1)), globales)

        # También ejecuta el validador canónico del proyecto.
        validado = cargar_ledger()
        self.assertEqual(accepted, validado["accepted_count"])

    def test_no_quedan_consumidores_vivos_de_ruta_anterior(self):
        old_path = "data/revision_ledger_pre_1_0.json"
        old_name = "revision_ledger_pre_1_0.json"

        allowed = {
            "tests/test_mant1_r5f_nombres_archivos.py",
            "tests/test_nor2_r2_migration_matrix.py",
            "tests/test_nor2_r6_ledger_data.py",
            "tests/test_nor2_r8_final_audit.py",
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

    def test_estado_transversal_evoluciona_sin_perder_nor2(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        docs = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        ledger = cargar_ledger()

        self.assertIn("NOR.2", readme)
        self.assertIn("NOR.2", docs)
        self.assertIn("**SEC.2:** R1–R6 cerrados", readme)

        entries = {
            item["global_revision"]: item
            for item in ledger["entries"]
        }
        self.assertEqual("AUD.SEC2", entries[109]["block"])
        self.assertEqual("DOC.2", entries[111]["block"])
        self.assertEqual("NOR.1", entries[112]["block"])
        self.assertEqual(7, entries[112]["ordinal"])

        registry = json.loads(
            (ROOT / "data/work-block-registry.json").read_text(
                encoding="utf-8"
            )
        )
        ids = {
            item["identifier"]: item
            for item in registry["identifiers"]
        }
        self.assertEqual(
            "planned_reserved",
            ids["PERSIST.1"]["status"],
        )

        matrix = (
            ROOT / "docs/governance/pre-1-0-pending-matrix.md"
        ).read_text(encoding="utf-8")
        self.assertIn("PERSIST.1 R1", matrix)

    def test_version_sigue_derivada_del_ledger_vigente(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        ledger = cargar_ledger()
        self.assertEqual(version, ledger["entries"][-1]["revision_aware"])


if __name__ == "__main__":
    unittest.main()
