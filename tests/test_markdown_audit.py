"""Regresiones del auditor permanente de documentación Markdown."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts import audit_markdown


ROOT = Path(__file__).resolve().parents[1]


class TestMarkdownAudit(unittest.TestCase):
    """Protege las reglas estructurales básicas del auditor Markdown."""

    def test_repositorio_actual_supera_auditoria(self):
        issues, counts, total = audit_markdown.audit_repository(ROOT)

        self.assertEqual([], issues)
        self.assertGreaterEqual(total, 137)
        self.assertEqual(total, sum(counts.values()))
        self.assertGreater(counts["VIVO"], 0)
        self.assertGreater(counts["HISTORICO"], 0)

    def test_clasificacion_documental(self):
        casos = {
            "docs/archive/governance/example.md": "HISTORICO",
            "docs/audits/documentation/example.md": "AUDITORIA",
            "docs/templates/example.md": "PLANTILLA",
            "scripts/README.md": "SOPORTE",
            "docs/product/example.md": "VIVO",
        }

        for ruta, esperado in casos.items():
            with self.subTest(ruta=ruta):
                self.assertEqual(
                    esperado,
                    audit_markdown.classify(ruta),
                )

    def test_documento_vivo_detecta_problemas_basicos(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            rel = "docs/product/example.md"
            path = root / rel
            path.parent.mkdir(parents=True)

            path.write_text(
                "# Ejemplo\n"
                "\n"
                "Estado: vigente\n"
                "**Versión de aplicación revisada:** "
                "`0.0.1-beta`\n"
                "\n"
                "[Documento inexistente](missing.md)\n",
                encoding="utf-8",
            )

            issues = audit_markdown.audit_file(
                root,
                rel,
                "0.1.10.01-beta",
            )

            codes = {issue.code for issue in issues}

            self.assertIn("METADATA_SIN_NEGRITA", codes)
            self.assertIn("VERSION_VIVA_NO_ACTUAL", codes)
            self.assertIn("ENLACE_LOCAL_ROTO", codes)

    def test_historico_conserva_version_y_enlaces_antiguos(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            rel = "docs/archive/example.md"
            path = root / rel
            path.parent.mkdir(parents=True)

            path.write_text(
                "# Evidencia histórica\n"
                "\n"
                "**Versión de aplicación revisada:** "
                "`0.0.1-beta`\n"
                "\n"
                "[Ruta histórica](ruta-inexistente.md)\n",
                encoding="utf-8",
            )

            issues = audit_markdown.audit_file(
                root,
                rel,
                "0.1.10.01-beta",
            )

            codes = {issue.code for issue in issues}

            self.assertNotIn("VERSION_VIVA_NO_ACTUAL", codes)
            self.assertNotIn("ENLACE_LOCAL_ROTO", codes)

    def test_stub_documental_de_compatibilidad_es_bloqueante(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            rel = "docs/product/stub.md"
            path = root / rel
            path.parent.mkdir(parents=True)

            path.write_text(
                "# Stub\n"
                "\n"
                "Este archivo permanece únicamente como ruta "
                "de compatibilidad para enlaces históricos.\n",
                encoding="utf-8",
            )

            issues = audit_markdown.audit_file(
                root,
                rel,
                "0.1.10.01-beta",
            )

            self.assertIn(
                "STUB_COMPATIBILIDAD",
                {issue.code for issue in issues},
            )

    def test_bloque_codigo_sin_cerrar_es_bloqueante(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            rel = "docs/product/code-fence.md"
            path = root / rel
            path.parent.mkdir(parents=True)

            path.write_text(
                "# Ejemplo\n"
                "\n"
                "```powershell\n"
                "python scripts/audit_markdown.py\n",
                encoding="utf-8",
            )

            issues = audit_markdown.audit_file(
                root,
                rel,
                "0.1.10.01-beta",
            )

            self.assertIn(
                "BLOQUE_CODIGO_SIN_CERRAR",
                {issue.code for issue in issues},
            )

    def test_workflow_markdown_audit_esta_versionado(self):
        workflow = ROOT / ".github/workflows/markdown-audit.yml"

        self.assertTrue(
            workflow.is_file(),
            "Falta el workflow permanente de auditoría Markdown.",
        )

        contenido = workflow.read_text(encoding="utf-8")

        esperados = (
            "name: Markdown Audit",
            "pull_request:",
            "push:",
            "workflow_dispatch:",
            'python-version: "3.14"',
            "python scripts/audit_markdown.py",
            "python -m unittest tests.test_markdown_audit -v",
        )

        for esperado in esperados:
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, contenido)


if __name__ == "__main__":
    unittest.main()
