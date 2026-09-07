"""Regresiones del cierre documental UX.6 R7 previo a R8."""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestUX6R7DocumentationClosure(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        def load(path: str) -> str:
            return (ROOT / path).read_text(encoding="utf-8")

        cls.version = load("VERSION").strip()
        cls.readme = load("README.md")
        cls.releases = load("RELEASES.md")
        cls.security = load("SECURITY.md")
        cls.versioning = load("VERSIONING.md")
        cls.docs_index = load("docs/README.md")
        cls.audits_index = load("docs/audits/README.md")
        cls.audit = load("docs/audits/documentation/ux6-r7-documentation-audit.md")
        cls.architecture = load("docs/architecture/system-architecture.md")
        cls.dev_center = load("docs/architecture/development-center.md")
        cls.data_model = load("docs/architecture/data-model.md")
        cls.dev_guide = load("docs/operations/development-guide.md")
        cls.observability = load("docs/operations/observability-and-logs.md")
        cls.release_process = load("docs/operations/release-process.md")
        cls.functional = load("docs/product/functional-specification.md")
        cls.traceability = load("docs/product/traceability-matrix.md")
        cls.visual = load("docs/product/visual-identity.md")
        cls.public_privacy = load("docs/security/privacy-policy.md")
        cls.public_terms = load("docs/security/terms-and-privacy.md")

    def test_r7_no_promueve_g121(self):
        self.assertEqual("0.1.20.01-beta", self.version)
        for text in (self.readme, self.releases, self.security, self.versioning, self.release_process):
            self.assertNotIn("G121/E01 queda aceptado", text)
            self.assertNotIn("G121/E01 está aceptado", text)

    def test_g120_publicado_reconciliado(self):
        for text in (self.readme, self.releases, self.security, self.versioning, self.release_process):
            self.assertIn("v0.1.20.01-beta", text)
        self.assertIn("383133233", self.readme)
        self.assertIn("7dbcca8071e2726b6aa4f17704bf41b92f6cd5bd", self.releases)

    def test_auditoria_r7_indexada(self):
        target = "ux6-r7-documentation-audit.md"
        self.assertIn(target, self.docs_index)
        self.assertIn(target, self.audits_index)
        self.assertIn("166 Markdown", self.audit)
        self.assertIn("0 enlaces Markdown locales rotos", self.audit)
        self.assertIn("46 documentos VIVO", self.audit)

    def test_developer_ux6_documentado(self):
        self.assertIn("developer_user_audit", self.data_model)
        self.assertIn("avatar_relativo", self.data_model)
        self.assertIn("developer_user_audit", self.observability)
        self.assertIn("MRP_DEVELOPER_MEDIA_DIR", self.dev_center)
        self.assertIn("Extensión UX.6", self.functional)

    def test_design_system_compartido(self):
        for token in ("design-system.css", "motion.css", "prefers-reduced-motion"):
            self.assertIn(token, self.dev_guide)
            self.assertIn(token, self.architecture)
        self.assertIn("--dev-*", self.visual)
        self.assertIn("futuras superficies", self.visual)

    def test_trazabilidad_ux6(self):
        self.assertIn("| TR-035 |", self.traceability)
        self.assertIn("| TR-036 |", self.traceability)
        self.assertIn("| TR-037 |", self.traceability)

    def test_terminos_publicos_siguen_separados(self):
        for text in (self.public_privacy, self.public_terms):
            self.assertNotIn("mrp_admin_session", text)
            self.assertNotIn("Developer Diagnostics", text)
            self.assertNotIn("MRP_ADMIN_COOKIE", text)


if __name__ == "__main__":
    unittest.main()
