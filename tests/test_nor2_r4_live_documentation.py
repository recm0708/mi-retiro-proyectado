"""Regresiones NOR.2 R4 — documentación viva en áreas canónicas."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/audits/repository/repository-normalization-migration-matrix-nor2-r2.md"

CONSOLIDATE = {
    "docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md": "docs/standards/code-and-comments.md",
    "docs/POLITICA_ESTRUCTURA_ARCHIVOS.md": "docs/standards/file-structure-by-extension.md",
}


def parse_moves():
    text = MATRIX.read_text(encoding="utf-8")
    moves = dict(re.findall(
        r"\| `(docs/[^`]+)` \| \*\*MIGRAR\*\* \| `(docs/[^`]+)` \| R4 \|",
        text,
    ))
    return {**moves, **CONSOLIDATE}


MOVES = parse_moves()

RETIRED_COMPATIBILITY_STUBS = {
    "docs/product/user-interface.md":
        "docs/archive/ux/UX_4_6A_REDISENO_VISUAL.md",
    "docs/product/workflow-step-1-personal-data.md":
        "docs/archive/ux/UX_4_6B_PASO1_DATOS_PERSONALES.md",
    "docs/product/workflow-step-2-contributions.md":
        "docs/archive/ux/UX_4_6C_PASO2_CUOTAS.md",
    "docs/product/workflow-step-3-salary-history.md":
        "docs/archive/ux/UX_4_6D_PASO3_HISTORIAL.md",
}


class TestNOR2R4LiveDocumentation(unittest.TestCase):

    def test_43_rutas_migradas_y_estado_posterior_preservado(self):
        self.assertEqual(43, len(MOVES))
        self.assertEqual(4, len(RETIRED_COMPATIBILITY_STUBS))

        for old, new in MOVES.items():
            with self.subTest(old=old, new=new):
                self.assertFalse((ROOT / old).exists(), old)

                if new in RETIRED_COMPATIBILITY_STUBS:
                    historico = RETIRED_COMPATIBILITY_STUBS[new]

                    self.assertFalse(
                        (ROOT / new).exists(),
                        f"stub de compatibilidad todavía presente: {new}",
                    )
                    self.assertTrue(
                        (ROOT / historico).is_file(),
                        f"snapshot histórico ausente: {historico}",
                    )
                else:
                    self.assertTrue((ROOT / new).is_file(), new)

    def test_areas_documentales_canonicas_existen(self):
        docs = ROOT / "docs"
        for area in (
            "architecture", "decisions", "governance", "operations",
            "product", "regulatory", "security", "standards", "audits",
            "archive", "templates",
        ):
            with self.subTest(area=area):
                self.assertTrue((docs / area).is_dir(), area)
        self.assertTrue((docs / "README.md").is_file())

    def test_documentacion_viva_declara_r4(self):
        for rel in (
            "README.md",
            "CHANGELOG.md",
            "docs/README.md",
            "docs/governance/roadmap.md",
            "docs/governance/master-plan-to-1-0.md",
            "docs/operations/validation.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("NOR.2 R4", text, rel)

        docs_index = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        self.assertIn(
            "**NOR.2 R4:** cerrado",
            docs_index,
        )

        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "├── docs/\n│   ├── README.md\n│   ├── architecture/",
            root_readme,
        )
        self.assertIn(
            "│   └── templates/\n├── regulations/",
            root_readme,
        )

    def test_evidencia_r4_existe(self):
        path = ROOT / "docs/audits/repository/repository-normalization-live-docs-nor2-r4.md"
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("41 documentos vivos", text)
        self.assertIn("2 estándares heredados", text)
        self.assertIn("43 movimientos Git", text)
        self.assertIn("NOR.2 R5", text)

    def test_estandares_especializados_indexados(self):
        text = (ROOT / "docs/standards/README.md").read_text(encoding="utf-8")
        self.assertIn("code-and-comments.md", text)
        self.assertIn("file-structure-by-extension.md", text)

    def test_version_permanece(self):
        self.assertEqual(
            "0.0.71.01-beta",
            (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        )

    def test_aplicador_temporal_no_permanece(self):
        self.assertFalse((ROOT / "apply_nor2_r4.py").exists())


if __name__ == "__main__":
    unittest.main()
