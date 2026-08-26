"""Regresiones focales de DOC.1 R3 para referencias navegables."""

from __future__ import annotations

from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger


ROOT = Path(__file__).resolve().parents[1]


class TestDOC1R3MarkdownLinks(unittest.TestCase):
    def test_inventarios_tecnicos_tienen_enlaces_deterministas(self):
        data_model = (
            ROOT / "docs/architecture/data-model.md"
        ).read_text(encoding="utf-8")
        architecture = (
            ROOT / "docs/architecture/system-architecture.md"
        ).read_text(encoding="utf-8")

        expected_data_model = (
            "[`app/models/pension.py`](../../app/models/pension.py)",
            "[`app/models/comparacion.py`](../../app/models/comparacion.py)",
        )
        for token in expected_data_model:
            with self.subTest(token=token):
                self.assertIn(token, data_model)

        expected_architecture = (
            "[`app/core/constants.py`](../../app/core/constants.py)",
            "[`app/models/comparacion.py`](../../app/models/comparacion.py)",
            "[`app/models/pension.py`](../../app/models/pension.py)",
            "[`app/engines/elegibilidad.py`](../../app/engines/elegibilidad.py)",
            "[`app/engines/sebd_modalidades.py`]"
            "(../../app/engines/sebd_modalidades.py)",
        )
        for token in expected_architecture:
            with self.subTest(token=token):
                self.assertIn(token, architecture)

    def test_marco_normativo_usa_etiquetas_documentales_humanas(self):
        content = (
            ROOT / "docs/regulatory/regulatory-framework.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "[Modalidades de retiro por vejez — SEBD](sebd-modalities.md)",
            content,
        )
        self.assertIn(
            "[Subsistema Mixto — diseño y alcance del motor]"
            "(mixto-modalities.md)",
            content,
        )
        self.assertIn(
            "[Sistema Único de Capitalización con Garantía Solidaria (SUCGS)]"
            "(sucgs-modalities.md)",
            content,
        )
        self.assertNotIn(
            "[sebd-modalities.md](sebd-modalities.md)",
            content,
        )

    def test_politica_prohibe_resolucion_masiva_ambigua(self):
        content = (
            ROOT / "docs/standards/documentation-standards.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Presentación de referencias navegables", content)
        self.assertIn(
            "una coincidencia de nombre de archivo, por sí sola, no autoriza",
            content,
        )
        self.assertIn(
            "la existencia de un archivo actual no implica que cada mención",
            content,
        )
        self.assertIn("no se infiere un destino", content)

    def test_evidencia_historica_y_contractual_permanece_literal(self):
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        traceability = (
            ROOT / "docs/product/traceability-matrix.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "`data/doc2-legacy-changelog-evidence.json`",
            changelog,
        )
        self.assertIn(
            "`app/models/traceability.py`, `app/services/traceability.py`",
            traceability,
        )

    def test_auditoria_doc1_r3_esta_indexada(self):
        audit = (
            ROOT
            / "docs/audits/documentation/"
            "documentation-markdown-links-doc1-r3.md"
        )
        index = (ROOT / "docs/README.md").read_text(encoding="utf-8")

        self.assertTrue(audit.is_file())
        self.assertIn(
            "documentation-markdown-links-doc1-r3.md",
            index,
        )
        self.assertIn(
            "**11 cambios inequívocos**",
            audit.read_text(encoding="utf-8"),
        )

    def test_candidato_no_promueve_g113(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        ledger = cargar_ledger()

        self.assertEqual("0.1.12.07-beta", version)
        self.assertEqual(112, ledger["accepted_count"])
        self.assertEqual(113, ledger["next_global"])
        self.assertEqual("0.1.13.03-beta", ledger["next_candidate"])
        self.assertEqual("DOC.1", ledger["next_candidate_block"])


if __name__ == "__main__":
    unittest.main()
