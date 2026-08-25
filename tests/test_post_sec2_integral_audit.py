"""Regresiones del saneamiento integral posterior al cierre SEC.2."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestPostSec2IntegralAudit(unittest.TestCase):
    def test_cierre_sec2_esta_clasificado_como_auditoria(self):
        self.assertFalse((ROOT / "docs/security/sec2-closure.md").exists())
        cierre = ROOT / "docs/audits/security/sec2-final-closure.md"
        self.assertTrue(cierre.exists())
        texto = cierre.read_text(encoding="utf-8")
        self.assertIn("SEC.2 R1–R6", texto)
        self.assertIn("MRP_ADMIN_ENABLED", texto)
        self.assertIn("G109/E01", texto)

    def test_readme_documenta_acceso_sin_publicar_secreto(self):
        texto = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("http://127.0.0.1:8000/dev/login", texto)
        self.assertIn("http://127.0.0.1:8000/dev/centro-desarrollo", texto)
        self.assertIn("MRP_ADMIN_SECRET", texto)
        self.assertIn("No existe una clave administrativa predeterminada", texto)
        self.assertIn("<define-tu-secreto-local-no-versionado>", texto)

    def test_snapshot_g070_se_preserva_exactamente(self):
        ruta = ROOT / "docs/archive/governance/pre-1-0-revision-ledger-g070.json"
        digest = hashlib.sha256(ruta.read_bytes()).hexdigest()
        self.assertEqual(
            "f5e0020643b324119855693588469eb8c98a0abafdb8f6108d60d5fb03a2288e",
            digest,
        )

    def test_ledger_vivo_esta_reconciliado_hasta_g108(self):
        data = json.loads(
            (ROOT / "data/pre-1-0-revision-ledger.json").read_text(encoding="utf-8")
        )
        self.assertEqual(108, data["accepted_count"])
        self.assertEqual(109, data["next_global"])
        self.assertEqual("0.1.09.01-beta", data["next_candidate"])
        self.assertEqual(list(range(1, 109)), [e["global_revision"] for e in data["entries"]])

    def test_auditoria_documental_cubre_snapshot_140_de_140(self):
        texto = (
            ROOT / "docs/audits/documentation/documentation-audit-post-sec2.md"
        ).read_text(encoding="utf-8")
        self.assertIn("140 Markdown", texto)
        self.assertIn("57 vivos", texto)
        self.assertIn("14 auditorías", texto)
        self.assertIn("64 históricos", texto)
        self.assertIn("1 plantilla", texto)
        self.assertIn("4 soporte", texto)
        filas = [
            line
            for line in texto.splitlines()
            if line.startswith("| ") and line.split("|")[1].strip().isdigit()
        ]
        self.assertEqual(140, len(filas))

    def test_documentacion_viva_reconoce_sesion_admin(self):
        threat = (ROOT / "docs/security/threat-model.md").read_text(encoding="utf-8")
        privacy = (ROOT / "docs/security/privacy-policy.md").read_text(encoding="utf-8")
        security = (ROOT / "docs/security/security-and-privacy.md").read_text(encoding="utf-8")
        for texto in (threat, privacy, security):
            self.assertIn("mrp_admin_session", texto)
        self.assertIn("logout POST", threat)


if __name__ == "__main__":
    unittest.main()
