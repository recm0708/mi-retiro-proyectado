"""Regresiones de promoción UX.6 R8 -> G121/E01."""

from __future__ import annotations
import json
from pathlib import Path
import unittest
from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision
from app.core.version_ledger import cargar_ledger
ROOT = Path(__file__).resolve().parents[1]

class TestG121PromotionPostMerge(unittest.TestCase):
    def test_version_materializa_g121_e01(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.21.01-beta", version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((121, 1), descomponer_version_beta_revision(version))

    def test_ledger_acepta_g121_y_reserva_g122(self):
        ledger = cargar_ledger()
        self.assertEqual(121, ledger["accepted_count"])
        self.assertEqual(122, ledger["next_global"])
        self.assertEqual("0.1.22.01-beta", ledger["next_candidate"])
        self.assertEqual("NOR.3", ledger["next_candidate_block"])
        entry = ledger["entries"][-1]
        self.assertEqual(121, entry["global_revision"])
        self.assertEqual("UX.6", entry["block"])
        self.assertEqual(1, entry["ordinal"])
        self.assertEqual("R8", entry["functional_revision"])
        self.assertEqual("0.1.21.01-beta", entry["revision_aware"])
        self.assertIn("PR #124", entry["evidence"])
        self.assertIn("f2b7ed0", entry["evidence"])

    def test_registro_cierra_ux6_y_activa_nor3_como_candidato(self):
        data = json.loads((ROOT / "data/work-block-registry.json").read_text(encoding="utf-8"))
        ids = {x["identifier"]: x for x in data["identifiers"]}
        self.assertEqual("closed", ids["UX.6"]["status"])
        self.assertIn("G121", ids["UX.6"]["global_refs"])
        self.assertEqual("planned_reserved", ids["PERSIST.1"]["status"])
        self.assertEqual("candidate_r1", ids["NOR.3"]["status"])
        self.assertEqual("planned_reserved", ids["UX.7"]["status"])
        self.assertIn("Inicio de App Asegurado", ids["UX.7"]["meaning"])
        self.assertIn("/dev", ids["UX.7"]["meaning"])
        self.assertEqual("planned_reserved", ids["UX.8"]["status"])
        self.assertIn("/simulacion", ids["UX.8"]["meaning"])
        candidate = data["current_candidate"]
        self.assertEqual(122, candidate["global_revision"])
        self.assertEqual("0.1.22.01-beta", candidate["revision_aware"])
        self.assertEqual("NOR.3", candidate["block"])
        self.assertEqual("R1", candidate["revision"])
        self.assertEqual("reserved_not_accepted", candidate["state"])
        self.assertIsNone(candidate["next_functional_block_if_accepted"])

    def test_manifiesto_materializa_ux6_r8(self):
        data = json.loads((ROOT / "data/release-publication-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("0.1.21.01-beta", data["version"])
        self.assertEqual("UX.6", data["block"])
        self.assertEqual("R8", data["revision"])
        self.assertEqual(122, data["next_step"]["global_revision"])
        self.assertEqual("0.1.22.01-beta", data["next_step"]["revision_aware"])
        self.assertEqual("NOR.3", data["next_step"]["block"])

    def test_ux6_r1_r8_consumen_un_solo_estado(self):
        entries = [x for x in cargar_ledger()["entries"] if x["block"] == "UX.6"]
        self.assertEqual(1, len(entries))
        self.assertEqual(1, entries[0]["ordinal"])
        self.assertEqual("R8", entries[0]["functional_revision"])

    def test_privacidad_publica_mantiene_version_material(self):
        self.assertIn('VERSION_PRIVACIDAD = "2026-08-16.1"', (ROOT / "app/static/js/privacy.js").read_text(encoding="utf-8"))

if __name__ == "__main__": unittest.main()
