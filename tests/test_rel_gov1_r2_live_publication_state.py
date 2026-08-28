"""Regresiones de estado vivo y documentación para REL.GOV.1 R2."""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestRelGovR2LivePublicationState(unittest.TestCase):
    def test_superficies_vivas_no_presentan_g116_como_pendiente(self):
        paths = (
            "README.md",
            "GOVERNANCE.md",
            "SECURITY.md",
            "VERSIONING.md",
            "docs/operations/release-process.md",
            "docs/governance/pre-1-0-revision-ledger.md",
        )
        forbidden = (
            "v0.1.16.05-beta` se publicará únicamente",
            "pendientes hasta integrar/revalidar esta promoción",
            "tag y GitHub Release pendientes",
            "último tag revision-aware publicado hasta completar",
        )
        for rel in paths:
            text = (ROOT / rel).read_text(encoding="utf-8")
            for fragment in forbidden:
                with self.subTest(path=rel, fragment=fragment):
                    self.assertNotIn(fragment, text)

    def test_readme_declara_publicacion_g116_real(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("v0.1.16.05-beta", text)
        self.assertIn(
            "dfb7dc60cf81951c701c126d6fecbcfdbca7aa7b",
            text,
        )

    def test_security_declara_g116_publicada(self):
        text = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        self.assertIn(
            "| `0.1.16.05-beta` | Beta vigente G116/E05 publicada;",
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

    def test_g117_permanece_reservado_no_aceptado(self):
        docs = (
            (ROOT / "README.md").read_text(encoding="utf-8")
            + (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
            + (ROOT / "docs/governance/pre-1-0-revision-ledger.md").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("G117/E02", docs)
        self.assertIn("reservado", docs)
        self.assertNotIn("G117/E02 queda aceptado", docs)


if __name__ == "__main__":
    unittest.main()
