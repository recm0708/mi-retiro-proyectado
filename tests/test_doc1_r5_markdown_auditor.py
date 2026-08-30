"""DOC.1 R5 — regresiones del auditor Markdown endurecido."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
AUDITOR_PATH = ROOT / "scripts" / "audit_markdown.py"

SPEC = importlib.util.spec_from_file_location(
    "audit_markdown_doc1_r5",
    AUDITOR_PATH,
)
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


class TestDoc1R5MarkdownAuditor(unittest.TestCase):
    """Protege etiquetas documentales y candidato revision-aware vigente."""

    def test_etiqueta_tecnica_en_lista_documental_falla(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "docs").mkdir()
            (root / "docs" / "target.md").write_text(
                "# Título humano\n",
                encoding="utf-8",
            )

            issues = AUDIT.check_document_link_labels(
                root,
                "README.md",
                ["- [`docs/target.md`](docs/target.md) — referencia."],
            )

            self.assertEqual(1, len(issues))
            self.assertEqual(
                "ETIQUETA_DOCUMENTAL_TECNICA",
                issues[0].code,
            )

    def test_etiqueta_humana_en_lista_documental_es_valida(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "docs").mkdir()
            (root / "docs" / "target.md").write_text(
                "# Título humano\n",
                encoding="utf-8",
            )

            issues = AUDIT.check_document_link_labels(
                root,
                "README.md",
                ["- **[Título humano](docs/target.md)** — referencia."],
            )

            self.assertEqual([], issues)

    def test_fuente_historica_no_se_moderniza(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "docs" / "archive").mkdir(parents=True)
            (root / "target.md").write_text(
                "# Título humano\n",
                encoding="utf-8",
            )

            issues = AUDIT.check_document_link_labels(
                root,
                "docs/archive/evidencia.md",
                ["- [`target.md`](../../target.md) — evidencia."],
            )

            self.assertEqual([], issues)

    def test_reserva_revision_aware_obsoleta_falla(self):
        issues = AUDIT.check_current_candidate_state(
            "docs/README.md",
            [
                "REL.GOV.1 R2 queda como candidato "
                "G116/E02 (`0.1.16.02-beta`)."
            ],
            next_global=116,
            next_candidate="0.1.16.05-beta",
        )

        self.assertEqual(1, len(issues))
        self.assertEqual(
            "CANDIDATO_REVISION_AWARE_OBSOLETO",
            issues[0].code,
        )

    def test_reserva_revision_aware_actual_es_valida(self):
        issues = AUDIT.check_current_candidate_state(
            "docs/README.md",
            [
                "DOC.1 R5 queda como candidato "
                "G116/E05 (`0.1.16.05-beta`)."
            ],
            next_global=116,
            next_candidate="0.1.16.05-beta",
        )

        self.assertEqual([], issues)

    def test_version_sincronizada_obsoleta_en_estado_vigente_falla(self):
        issues = AUDIT.check_current_state_version(
            "docs/decisions/README.md",
            [
                "## Nota de lectura",
                "",
                "Estado vigente para lectura transversal:",
                "",
                "- `VERSION` está sincronizado en "
                "`0.1.11.01-beta` (G111/E01).",
            ],
            "0.1.18.04-beta",
        )

        self.assertEqual(1, len(issues))
        self.assertEqual(
            "VERSION_ANTIGUA_EN_ESTADO_VIGENTE",
            issues[0].code,
        )

    def test_version_sincronizada_actual_en_estado_vigente_es_valida(self):
        issues = AUDIT.check_current_state_version(
            "docs/decisions/README.md",
            [
                "## Nota de lectura",
                "",
                "Estado vigente para lectura transversal:",
                "",
                "- `VERSION` está sincronizado en "
                "`0.1.18.04-beta` (G118/E04).",
            ],
            "0.1.18.04-beta",
        )

        self.assertEqual([], issues)

    def test_changelog_y_releases_preservan_contexto_historico(self):
        for rel in ("CHANGELOG.md", "RELEASES.md"):
            with self.subTest(rel=rel):
                issues = AUDIT.check_current_candidate_state(
                    rel,
                    [
                        "Al publicar G115, G116/E02 "
                        "(`0.1.16.02-beta`) quedó reservado."
                    ],
                    next_global=116,
                    next_candidate="0.1.16.05-beta",
                )

                self.assertEqual([], issues)


if __name__ == "__main__":
    unittest.main()
