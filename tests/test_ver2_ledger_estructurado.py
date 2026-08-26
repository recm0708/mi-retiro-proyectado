"""Regresiones del ledger estructurado reconstruido durante VER.2."""

from copy import deepcopy
import json
from pathlib import Path
import unittest

from app.core.version_ledger import (
    LEDGER_FILE,
    LedgerRevisionError,
    cargar_ledger,
    validar_ledger,
)


ROOT = Path(__file__).resolve().parents[1]
LEDGER_MD = ROOT / "docs" / "governance/pre-1-0-revision-ledger.md"
MATRIZ = ROOT / "docs" / "archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md"


class TestVer2LedgerEstructurado(unittest.TestCase):
    """Impide huecos, duplicados y divergencias entre ledger y auditoría."""

    @classmethod
    def setUpClass(cls):
        cls.ledger = cargar_ledger()

    def test_json_es_valido_y_declara_reconciliacion_post_g070(self):
        self.assertTrue(LEDGER_FILE.is_file())
        accepted = self.ledger["accepted_count"]
        self.assertGreaterEqual(accepted, 109)
        self.assertEqual(accepted, len(self.ledger["entries"]))
        self.assertEqual(accepted + 1, self.ledger["next_global_if_ver2_accepted"])
        self.assertEqual(accepted + 1, self.ledger["next_global"])

    def test_globales_son_contiguos_y_ids_coinciden(self):
        globales = [entry["global_revision"] for entry in self.ledger["entries"]]
        accepted = self.ledger["accepted_count"]
        self.assertEqual(list(range(1, accepted + 1)), globales)
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(version, self.ledger["entries"][-1]["revision_aware"])

    def test_markdown_preserva_g070_y_documenta_reconciliacion(self):
        ledger_md = LEDGER_MD.read_text(encoding="utf-8")
        matriz = MATRIZ.read_text(encoding="utf-8")
        self.assertIn("**G070**", ledger_md)
        self.assertIn("G070 | `0.0.70.02-beta`", ledger_md)
        self.assertIn("**Total aceptado antes de VER.2** | **70**", matriz)
        self.assertIn("G071–G108", ledger_md)
        self.assertIn("G109", ledger_md)
        self.assertIn("**G111**", ledger_md)
        self.assertIn("G110 | `0.1.10.01-beta`", ledger_md)
        self.assertIn("`0.1.11.01-beta`", ledger_md)
        self.assertIn("`0.0.71.01-beta`", ledger_md)

    def test_exclusiones_clave_se_preservan(self):
        exclusiones = "\n".join(
            f"{item['state']} — {item['reason']}" for item in self.ledger["excluded"]
        )
        for texto in (
            "UX.2.1",
            "UX.4.6d R1–R22",
            "PR #19 checkpoint pre-R8",
            "UX.4.6h R1",
            "UX.4.6i R1.1",
            "UX.4.6i R1.2/R1.3",
        ):
            with self.subTest(texto=texto):
                self.assertIn(texto, exclusiones)

    def test_validador_rechaza_hueco_global(self):
        alterado = deepcopy(self.ledger)
        alterado["entries"][9]["global_revision"] = 99
        with self.assertRaises(LedgerRevisionError):
            validar_ledger(alterado)

    def test_validador_rechaza_id_revision_aware_incoherente(self):
        alterado = deepcopy(self.ledger)
        alterado["entries"][-1]["revision_aware"] = "0.0.70.03-beta"
        with self.assertRaises(LedgerRevisionError):
            validar_ledger(alterado)

    def test_validador_rechaza_siguiente_global_incorrecto(self):
        alterado = deepcopy(self.ledger)
        alterado["next_global_if_ver2_accepted"] = 999
        with self.assertRaises(LedgerRevisionError):
            validar_ledger(alterado)

    def test_archivo_json_no_tiene_bom_y_parsea_directamente(self):
        raw = LEDGER_FILE.read_bytes()
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
        self.assertIsInstance(json.loads(raw.decode("utf-8")), dict)


if __name__ == "__main__":
    unittest.main()
