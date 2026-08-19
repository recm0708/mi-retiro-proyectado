"""Regresiones del checkpoint público de identidad visual previo a R8."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestIdentidadPublicaGithubPreR8(unittest.TestCase):
    """Protege marca, visibilidad pública y controles documentados de GitHub."""

    @classmethod
    def setUpClass(cls):
        cls.readme = (ROOT / "README.md").read_text(encoding="utf-8")
        cls.security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")
        cls.support = (ROOT / "SUPPORT.md").read_text(encoding="utf-8")
        cls.versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        cls.identity = (DOCS / "IDENTIDAD_VISUAL.md").read_text(encoding="utf-8")
        cls.prep = (DOCS / "PREPARACION_PUBLICA_GITHUB.md").read_text(encoding="utf-8")
        cls.audit = (DOCS / "AUDITORIA_GITHUB.md").read_text(encoding="utf-8")
        cls.transparency = (DOCS / "TRANSPARENCIA.md").read_text(encoding="utf-8")
        cls.security_privacy = (DOCS / "SEGURIDAD_PRIVACIDAD.md").read_text(
            encoding="utf-8"
        )
        cls.index = (DOCS / "INDICE.md").read_text(encoding="utf-8")
        cls.changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        cls.roadmap = (DOCS / "ROADMAP.md").read_text(encoding="utf-8")
        cls.validation = (DOCS / "VALIDACION.md").read_text(encoding="utf-8")

    def test_readme_usa_logo_y_declara_estado_publico_sin_promover_version(self):
        self.assertIn("assets/brand/logos/logo-mark-512.png", self.readme)
        self.assertIn("repositorio de código público", self.readme)
        self.assertIn("Social Preview e identidad visual oficial configurados", self.readme)
        self.assertIn("0.1.0-beta.1", self.readme)
        self.assertEqual(
            (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
            "0.0.24-beta",
        )

    def test_identidad_visual_define_fuente_derivados_runtime_y_social(self):
        for esperado in (
            "icono-simple-master-1254.png",
            "icono-simple-1024.png",
            "assets/brand/icons/",
            "assets/brand/logos/",
            "app/static/img/brand/",
            "assets/social/github-social-preview.png",
            "1280 × 640",
            "Herramienta independiente · No oficial",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, self.identity)

    def test_documentacion_publica_declara_20_topics_21_labels_y_social_preview(self):
        self.assertIn("**Visibilidad actual:** pública", self.prep)
        self.assertIn("20/20 topics", self.prep)
        self.assertIn("21 labels", self.prep)
        self.assertIn("`sebd-panama`", self.prep)
        self.assertIn("assets/social/github-social-preview.png", self.prep)

    def test_security_usa_private_vulnerability_reporting_como_canal_activo(self):
        self.assertIn("GitHub Private vulnerability reporting", self.security)
        self.assertIn("Esta función está habilitada", self.security)
        self.assertIn("Push protection", self.security)
        self.assertIn("CodeQL con Default setup", self.security)
        self.assertNotIn("Si la visibilidad/plan permite habilitarla en el futuro", self.security)

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

    def test_versioning_separa_visibilidad_de_version_de_producto(self):
        self.assertIn("### 3.1. Desarrollo pre-beta", self.versioning)
        self.assertIn(
            "visibilidad pública del repositorio de código no cambia por sí sola",
            self.versioning,
        )
        self.assertIn("visibilidad del repositorio", self.versioning)

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

    def test_indice_y_cierre_documental_son_coherentes(self):
        self.assertIn("IDENTIDAD_VISUAL.md", self.index)
        self.assertIn("repositorio público", self.index)
        self.assertIn("Social Preview", self.index)
        self.assertIn("Checkpoint pre-R8 — identidad visual y repositorio público", self.changelog)
        self.assertIn("624 pruebas en `OK`", self.changelog)
        self.assertIn("checkpoint pre-R8 — identidad visual oficial", self.roadmap)
        self.assertIn("**624 pruebas en `OK`**", self.validation)


if __name__ == "__main__":
    unittest.main()
