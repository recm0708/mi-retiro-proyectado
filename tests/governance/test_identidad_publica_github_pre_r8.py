"""Regresiones del checkpoint público de identidad visual previo a R8."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


class TestIdentidadPublicaGithubPreR8(unittest.TestCase):
    """Protege marca y publicación sin congelar la versión posterior."""

    @classmethod
    def setUpClass(cls):
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        cls.support = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
        cls.versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        cls.identity = (DOCS / "product/visual-identity.md").read_text(encoding="utf-8")
        cls.prep = (DOCS / "operations/github-public-repository.md").read_text(encoding="utf-8")
        cls.audit = (DOCS / "archive/governance/github-audit.md").read_text(encoding="utf-8")
        cls.transparency = (DOCS / "product/transparency.md").read_text(encoding="utf-8")
        cls.security_privacy = (DOCS / "security/security-and-privacy.md").read_text(
            encoding="utf-8"
        )
        cls.index = (DOCS / "README.md").read_text(encoding="utf-8")
        cls.changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        cls.roadmap = (DOCS / "governance/roadmap.md").read_text(encoding="utf-8")
        cls.validation = (DOCS / "operations/validation.md").read_text(encoding="utf-8")

    def test_readme_usa_logo_y_separa_checkpoint_publico_historico(self):
        self.assertIn("assets/brand/logos/logo-mark-512.png", self.readme)
        self.assertIn("repositorio público no", self.readme)
        self.assertNotIn("Social Preview e identidad visual oficial configurados", self.readme)
        self.assertNotIn("0.1.0-beta.1", self.readme)
        self.assertIn(
            "Checkpoint pre-R8 — identidad visual y repositorio público",
            self.changelog,
        )
        self.assertIn("0.0.24-beta", self.changelog)
        self.assertIn("**Visibilidad actual:** pública", self.prep)

    def test_identidad_visual_define_fuente_derivados_runtime_y_social(self):
        for esperado in (
            "icono-simple-master-1254.png",
            "icono-simple-1024.png",
            "assets/brand/icons/",
            "assets/brand/logos/",
            "app/static/shared/img/brand/",
            "assets/social/github-social-preview.png",
            "1280 × 640",
            "Herramienta independiente · No oficial",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, self.identity)

    def test_documentacion_publica_declara_estado_vigente_y_preserva_checkpoint_labels(self):
        self.assertIn("**Visibilidad actual:** pública", self.prep)
        self.assertIn("20/20 topics", self.prep)
        self.assertIn("28 labels", self.prep)
        self.assertIn("16 labels canónicos", self.prep)
        self.assertIn("12 labels suplementarios", self.prep)
        self.assertIn("labels: 21", self.audit)
        self.assertIn("`sebd-panama`", self.prep)
        self.assertIn("assets/social/github-social-preview.png", self.prep)


    def test_security_usa_private_vulnerability_reporting_como_canal_activo(self):
        self.assertIn("## Reportar una vulnerabilidad", self.security)
        self.assertIn("Canal preferido:", self.security)
        self.assertIn("GitHub Private vulnerability reporting", self.security)
        self.assertIn("CodeQL", self.security)
        self.assertIn("secret scanning y push protection", self.security)

    def test_support_no_envia_vulnerabilidades_a_issues_publicos(self):
        self.assertIn("No publiques detalles explotables en un issue", self.support)
        self.assertIn("GitHub Private vulnerability reporting", self.support)

    def test_auditoria_preserva_historia_privada_y_declara_estado_publico_actual(self):
        self.assertIn("repositorio privado en el momento del cierre GOV.1", self.audit)
        self.assertIn("visibilidad actual: **pública**", self.audit)
        self.assertIn("Secret Protection", self.audit)
        self.assertIn("Push protection", self.audit)
        self.assertIn("0 alertas abiertas", self.audit)

    def test_transparencia_separa_repo_publico_beta_y_despliegue(self):
        self.assertIn("repositorio de código es público", self.transparency)
        self.assertIn("no constituye un despliegue remoto", self.transparency)
        self.assertIn("no declara completada la primera beta pública", self.transparency)


    def test_documento_publico_separa_visibilidad_de_version_de_producto(self):
        self.assertIn("**Visibilidad actual:** pública", self.prep)
        self.assertIn(
            "La publicación del **repositorio de código** no equivale a declarar una versión oficial",
            self.prep,
        )
        self.assertIn("`1.0.0.0`", self.prep)
        self.assertIn("0.0.N-beta", self.prep)

    def test_seguridad_privacidad_documenta_controles_publicos_sin_cambiar_runtime(self):
        self.assertIn(
            "La visibilidad pública del repositorio no cambia este modelo de ejecución",
            self.security_privacy,
        )
        for esperado in (
            "CodeQL con Default setup",
            "Secret Protection / secret scanning",
            "Push protection",
            "Private vulnerability reporting",
        ):
            self.assertIn(esperado, self.security_privacy)


    def test_identidad_pre_r8_y_estado_vivo_usan_owners_correctos(self):
        self.assertIn("product/visual-identity.md", self.index)
        self.assertNotIn("Social Preview", self.index)

        self.assertIn("**Visibilidad actual:** pública", self.prep)
        self.assertIn(
            "assets/social/github-social-preview.png",
            self.prep,
        )

        self.assertIn(
            "Checkpoint pre-R8 — identidad visual y repositorio público",
            self.changelog,
        )
        self.assertIn("624 pruebas en `OK`", self.changelog)
        self.assertIn("**624 pruebas en `OK`**", self.validation)

        ledger = json.loads(
            (
                ROOT
                / "data/governance/"
                "pre-1-0-revision-ledger.json"
            ).read_text(encoding="utf-8")
        )
        g48 = next(
            item
            for item in ledger["entries"]
            if item["global_revision"] == 48
        )
        self.assertEqual("UX.4.6e", g48["block"])
        self.assertEqual(
            "identidad visual oficial y publicación",
            g48["state"],
        )
        self.assertIn("PR #20", g48["evidence"])
        self.assertIn("624 pruebas", g48["evidence"])

        self.assertIn("G129/E03/C0", self.roadmap)
        self.assertIn("DOC.4 R1", self.roadmap)
        self.assertNotIn("PLAN.2 R2", self.roadmap)

if __name__ == "__main__":
    unittest.main()
