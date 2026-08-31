"""Regresiones históricas y de estado vivo para REL.GOV.1 R2."""

from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestRelGovR2LivePublicationState(unittest.TestCase):
    def test_referencias_g116_que_permanezcan_no_lo_presentan_pendiente(self):
        # Solo superficies de estado vivo. CHANGELOG/RELEASES conservan
        # deliberadamente afirmaciones históricas como "quedó reservado"
        # cuando describen el estado que existía en un hito anterior.
        paths = (
            "README.md",
            "GOVERNANCE.md",
            "SECURITY.md",
            "VERSIONING.md",
            "docs/operations/release-process.md",
            "docs/governance/pre-1-0-revision-ledger.md",
        )

        markers = (
            "G116",
            "G116/E05",
            "0.1.16.05-beta",
            "v0.1.16.05-beta",
        )

        found = []
        for rel in paths:
            text = (ROOT / rel).read_text(encoding="utf-8")
            for line in text.splitlines():
                clauses = re.split(r"(?<=[.;])\s+", line)
                for clause in clauses:
                    if any(marker in clause for marker in markers):
                        found.append((rel, clause.strip()))

        self.assertTrue(found, "No se encontró evidencia viva/histórica de G116.")

        for rel, clause in found:
            lowered = clause.lower()
            with self.subTest(path=rel, clause=clause):
                self.assertNotIn("pendiente", lowered)
                self.assertNotIn("se publicará únicamente", lowered)
                self.assertIsNone(re.search(r"\breservado\b", lowered))

    def test_publicacion_g117_real_se_preserva_en_release_canonico(self):
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")

        # RELEASES.md conserva el inventario histórico completo de
        # publicaciones. README.md puede resumir los estados recientes
        # sin repetir necesariamente todos los tags anteriores.

        self.assertIn("v0.1.17.02-beta", releases)
        self.assertIn(
            "3ab9fefbdfc969c546feb83182e3c0e6879ba771",
            releases,
        )
        self.assertIn(
            "d2e493d16a2768ea5e6284c577c21b4f84897fae",
            releases,
        )
        self.assertIn("v0.1.16.05-beta", releases)

    def test_security_preserva_g118_y_declara_g119_vigente(self):
        text = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn(
            "| `0.1.18.04-beta` | Beta previa G118/E04 publicada",
            text,
        )
        self.assertIn(
            "| `0.1.19.05-beta` | Beta vigente G119/E05 publicada",
            text,
        )

    def test_proceso_documenta_automatizacion_r2(self):
        text = (ROOT / "docs/operations/release-process.md").read_text(
            encoding="utf-8"
        )
        for fragment in (
            "data/release-publication-manifest.json",
            "scripts\\release_publication.py --check-manifest",
            "Publicar GitHub Release",
            "falla cerrado",
            "no crea commits post-publicación",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, text)

    def test_scripts_readme_documenta_release_publication(self):
        text = (ROOT / "scripts/README.md").read_text(encoding="utf-8")
        self.assertIn("release_publication.py", text)
        self.assertIn("--check-manifest", text)

    def test_g118_historico_g119_aceptado_y_g120_reservado(self):
        docs = (
            (ROOT / "README.md").read_text(encoding="utf-8")
            + (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
            + (ROOT / "docs/governance/pre-1-0-revision-ledger.md").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("G118/E04", docs)
        self.assertIn("G119/E05", docs)
        self.assertIn("G120/E01", docs)
        self.assertIn("DEV.2 R6", docs)
        self.assertIn("UX.5 R1", docs)



    def test_publicacion_g118_real_se_refleja_en_estado_vivo(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")

        for fragment in (
            "v0.1.18.04-beta",
            "290e84aab70a257e8b718d172e37365af49ef048",
            "1ee2561785d2413ffffd60ea03a69d1e4dae5660",
            "378842155",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, readme + releases)

        self.assertIn("Beta previa G118/E04 publicada", security)
        self.assertIn("G119/E05", versioning)

        live_state = "\n".join((
            readme,
            security,
            versioning,
            (ROOT / "docs/governance/roadmap.md").read_text(encoding="utf-8"),
            (ROOT / "docs/governance/master-plan-to-1-0.md").read_text(encoding="utf-8"),
            (ROOT / "docs/operations/validation.md").read_text(encoding="utf-8"),
        ))
        for stale in (
            "Publicación revision-aware vigente al preparar esta promoción",
            "G117/E02 aceptado para REL.GOV.1 R2; DEV.2 R5 candidato G118/E04",
            "G118/E04 reservado para DEV.2 R5",
        ):
            with self.subTest(stale=stale):
                self.assertNotIn(stale, live_state)


if __name__ == "__main__":
    unittest.main()
