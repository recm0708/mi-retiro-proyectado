"""Regresiones históricas de la promoción UX.6 R8 -> G121/E01."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[2]


class TestG121PromotionPostMerge(unittest.TestCase):
    def test_historial_conserva_g121_e01(self):
        ledger = cargar_ledger()
        entry = next(item for item in ledger["entries"] if item["global_revision"] == 121)
        self.assertEqual("UX.6", entry["block"])
        self.assertEqual(1, entry["ordinal"])
        self.assertEqual("R8", entry["functional_revision"])
        self.assertEqual("0.1.21.01-beta", entry["revision_aware"])
        self.assertEqual((121, 1), descomponer_version_beta_revision(entry["revision_aware"]))
        self.assertIn("PR #124", entry["evidence"])
        self.assertIn("f2b7ed0", entry["evidence"])

    def test_estado_actual_materializa_g127_e02_y_deja_g128_libre(self):
        ledger = cargar_ledger()
        self.assertEqual(127, ledger["accepted_count"])
        self.assertEqual(128, ledger["next_global"])
        self.assertIsNone(ledger["next_candidate"])
        self.assertIsNone(ledger["next_candidate_block"])

        current = ledger["entries"][-1]
        self.assertEqual(127, current["global_revision"])
        self.assertEqual("MANT.2", current["block"])
        self.assertEqual(2, current["ordinal"])
        self.assertEqual("R2", current["functional_revision"])
        self.assertEqual("0.1.27.02-beta", current["revision_aware"])

    def test_registry_preserva_ux6_y_nor3_historicos(self):
        data = json.loads((ROOT / "data/governance/work-block-registry.json").read_text(encoding="utf-8"))
        ids = {item["identifier"]: item for item in data["identifiers"]}
        self.assertEqual("closed", ids["UX.6"]["status"])
        self.assertIn("G121", ids["UX.6"]["global_refs"])
        self.assertEqual("closed", ids["NOR.3"]["status"])
        self.assertEqual(["G122"], ids["NOR.3"]["global_refs"])
        self.assertEqual("planned_reserved", ids["PERSIST.1"]["status"])
        candidate = data["current_candidate"]
        self.assertEqual("unassigned", candidate["state"])
        self.assertIsNone(candidate["global_revision"])
        self.assertEqual(128, candidate["next_global_available"])

    def test_manifest_actual_materializa_mant2_r2(self):
        data = json.loads(
            (ROOT / "data/governance/release-publication-manifest.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("0.1.27.02-beta", data["version"])
        self.assertEqual("MANT.2", data["block"])
        self.assertEqual("R2", data["revision"])
        self.assertEqual(128, data["next_step"]["global_revision"])
        self.assertIsNone(data["next_step"]["revision_aware"])
        self.assertIsNone(data["next_step"]["block"])

    def test_ux6_r1_r8_consumen_un_solo_estado(self):
        entries = [item for item in cargar_ledger()["entries"] if item["block"] == "UX.6"]
        self.assertEqual(1, len(entries))
        self.assertEqual(1, entries[0]["ordinal"])
        self.assertEqual("R8", entries[0]["functional_revision"])

    def test_privacidad_publica_mantiene_version_material(self):
        text = (ROOT / "app/static/asegurado/js/privacy.js").read_text(encoding="utf-8")
        self.assertIn('VERSION_PRIVACIDAD = "2026-08-16.1"', text)


if __name__ == "__main__":
    unittest.main()
