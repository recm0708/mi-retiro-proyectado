"""MANT.1 R2 — documentación de scripts, hooks y gate local."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestMant1ScriptsHooksDocumentados(unittest.TestCase):
    """Protege la documentación mínima de la infraestructura local del repo."""

    @staticmethod
    def _leer(ruta: str) -> str:
        return (ROOT / ruta).read_text(encoding="utf-8")

    def test_scripts_y_hooks_tienen_readme_operativo(self):
        scripts = self._leer("scripts/README.md")
        hooks = self._leer(".githooks/README.md")

        self.assertIn("configure_git_hooks.ps1", scripts)
        self.assertIn("audit_markdown.py", scripts)
        self.assertIn("validate_precommit.py", scripts)
        self.assertIn("auditoría Markdown", scripts)
        self.assertIn("core.hooksPath=.githooks", scripts)
        self.assertIn("no implementan reglas previsionales", scripts)
        self.assertIn("GitHub Actions", scripts)

        self.assertIn("pre-commit", hooks)
        self.assertIn("scripts/validate_precommit.py", hooks)
        self.assertIn("No sustituye la CI remota", hooks)
        self.assertIn("No debe depender de rutas absolutas", hooks)

    def test_hook_y_scripts_explican_proposito_y_limites(self):
        hook = self._leer(".githooks/pre-commit")
        configurar = self._leer("scripts/configure_git_hooks.ps1")
        validar = self._leer("scripts/validate_precommit.py")

        self.assertIn("Hook versionado de Mi Retiro Proyectado", hook)
        self.assertIn("delegar todas las reglas del gate", hook)
        self.assertIn("no modifica archivos", hook)

        self.assertIn("Configura el hook local versionado", configurar)
        self.assertIn("no cambia código fuente", configurar)
        self.assertIn("core.hooksPath", configurar)

        self.assertIn("proteger el árbol de trabajo", validar)
        self.assertIn("no corrige archivos automáticamente", validar)
        self.assertIn("no reemplaza los checks remotos", validar)

    def test_documentacion_transversal_registra_mant1_r1_y_r2(self):
        changelog = self._leer("CHANGELOG.md")
        estandar = self._leer("docs/standards/code-and-comments.md")
        validacion = self._leer("docs/operations/validation.md")
        arquitectura = self._leer("docs/architecture/system-architecture.md")
        roadmap = self._leer("docs/governance/roadmap.md")

        for texto in (changelog, estandar, validacion, arquitectura, roadmap):
            self.assertIn("MANT.1 R2", texto)
            self.assertIn("MANT.1 R1", texto)

        self.assertIn("Scripts, hooks y automatización local", estandar)
        self.assertIn("Automatización local de calidad", arquitectura)
        self.assertIn("documentación de scripts y hooks antes de SEC.2", roadmap)

    def test_mant1_r2_no_promueve_version_ni_toca_motores(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.1.10.01-beta", version)

        changelog = self._leer("CHANGELOG.md")
        self.assertIn("sin cambiar `VERSION`, `APP_VERSION`, motores previsionales ni normativa", changelog)
        self.assertIn("MANT.1 R1 — auditoría inicial", changelog)
        self.assertIn("MANT.1 R2 — documentación de scripts y hooks", changelog)


if __name__ == "__main__":
    unittest.main()
