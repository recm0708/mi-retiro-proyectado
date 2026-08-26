"""Regresiones NOR.2 R5 — archivo y consolidación histórica."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/audits/repository/repository-normalization-migration-matrix-nor2-r2.md"


def parse_moves():
    text = MATRIX.read_text(encoding="utf-8")
    rows = re.findall(
        r"\| `(docs/[^`]+\.md)` "
        r"\| \*\*ARCHIVAR\*\* "
        r"\| `(docs/archive/(governance|technical|ux)/)` "
        r"\| R5 \|",
        text,
    )
    return [
        (src, dest_dir + Path(src).name, category)
        for src, dest_dir, category in rows
    ]


MOVES = parse_moves()


class TestNOR2R5HistoricalDocumentation(unittest.TestCase):

    def test_36_documentos_archivados(self):
        self.assertEqual(36, len(MOVES))
        counts = {
            category: sum(c == category for _, _, c in MOVES)
            for category in ("governance", "technical", "ux")
        }
        self.assertEqual(
            {"governance": 25, "technical": 8, "ux": 3},
            counts,
        )

        for old, new, _ in MOVES:
            with self.subTest(old=old, new=new):
                self.assertFalse((ROOT / old).exists(), old)
                self.assertTrue((ROOT / new).is_file(), new)

    def test_raiz_docs_queda_solo_con_indice_markdown(self):
        markdown = sorted(p.name for p in (ROOT / "docs").glob("*.md"))
        self.assertEqual(["README.md"], markdown)

    def test_no_hay_markdown_con_contenido_identico(self):
        import hashlib

        hashes = {}
        duplicates = []

        for path in sorted((ROOT / "docs").rglob("*.md")):
            content = path.read_text(encoding="utf-8-sig")
            normalized = (
                content
                .replace("\r\n", "\n")
                .replace("\r", "\n")
                .strip()
            )
            digest = hashlib.sha256(
                normalized.encode("utf-8")
            ).hexdigest()

            if digest in hashes:
                duplicates.append(
                    (
                        hashes[digest],
                        path.relative_to(ROOT).as_posix(),
                    )
                )
            else:
                hashes[digest] = path.relative_to(ROOT).as_posix()

        self.assertEqual([], duplicates)

    def test_indices_historicos_sin_rutas_obsoletas(self):
        for rel in (
            "docs/archive/README.md",
            "docs/archive/governance/README.md",
            "docs/archive/technical/README.md",
            "docs/archive/ux/README.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertNotIn("docs/INDICE.md", text)
                self.assertNotIn("../INDICE.md", text)
                self.assertNotIn(
                    "se mantienen como archivos de compatibilidad",
                    text,
                )

    def test_estado_transversal_r5(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        docs = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        self.assertIn("**NOR.2 R4:** cerrado", readme)
        self.assertIn("**NOR.2 R5:** cerrado", readme)
        self.assertIn("**NOR.2 R6:** cerrado", readme)
        self.assertIn("**NOR.2 R7:** cerrado", readme)
        self.assertIn("NOR.2 R5", docs)
        self.assertIn("NOR.2 R6", docs)
        self.assertIn("**SEC.2:** R1 cerrado; hardening CodeQL del informe imprimible y normalización técnica de GitHub Actions completados.", readme)
        self.assertIn("**Estado de SEC.2:** cerrado después de R1–R6", readme)

    def test_evidencia_r5_existe(self):
        path = ROOT / (
            "docs/audits/repository/"
            "repository-normalization-historical-docs-nor2-r5.md"
        )
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("36 documentos cerrados", text)
        self.assertIn("NOR.2 R6", text)

    def test_version_y_estado_transversal(self):
        self.assertEqual(
            "0.1.09.01-beta",
            (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        )

    def test_aplicador_temporal_no_permanece(self):
        self.assertFalse((ROOT / "apply_nor2_r5.py").exists())


if __name__ == "__main__":
    unittest.main()
