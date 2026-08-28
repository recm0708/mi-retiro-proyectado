"""Regresiones REL.GOV.1 R2 para automatización del workflow de tags."""

from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "verificar-tags.yml"


class TestReleaseWorkflowAutomation(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = WORKFLOW.read_text(encoding="utf-8")

    def test_creacion_del_tag_permanece_fuera_de_actions(self):
        self.assertNotIn("git tag -s", self.text)
        self.assertNotIn("git tag -a", self.text)
        self.assertNotIn("git tag --sign", self.text)

    def test_verificacion_usa_estado_etiquetado(self):
        self.assertIn("ref: ${{ github.ref }}", self.text)
        self.assertIn('git tag -v "$GITHUB_REF_NAME"', self.text)
        self.assertIn(
            'tag_commit="$(git rev-parse "$GITHUB_REF_NAME^{}")"',
            self.text,
        )
        self.assertIn(
            'git merge-base --is-ancestor "$tag_commit" origin/main',
            self.text,
        )

    def test_verificacion_permanece_solo_lectura(self):
        self.assertIn("verificar-tag-publicado:", self.text)
        self.assertIn("permissions:\n      contents: read", self.text)

    def test_publicacion_depende_de_verificacion(self):
        self.assertIn("publicar-release:", self.text)
        self.assertIn(
            "needs:\n      - verificar-tag-publicado",
            self.text,
        )
        self.assertIn("contents: write", self.text)

    def test_workflow_valida_manifiesto_y_notas(self):
        self.assertIn(
            "python scripts/release_publication.py --check-manifest",
            self.text,
        )
        self.assertIn("--render-notes", self.text)
        self.assertIn("--check-notes", self.text)
        self.assertIn("--check-title", self.text)

    def test_publicacion_es_idempotente(self):
        self.assertIn(
            'gh release view "$RELEASE_TAG"',
            self.text,
        )
        self.assertIn("--check-release-json", self.text)
        self.assertIn(
            "Release existente correcto; no se modifica.",
            self.text,
        )

    def test_creacion_exige_tag_existente_y_preserva_beta(self):
        self.assertIn("--verify-tag", self.text)
        self.assertIn("args+=(--prerelease)", self.text)
        self.assertIn(
            'if [[ "$RELEASE_VERSION" == *-beta ]]',
            self.text,
        )

    def test_checkout_no_persiste_credenciales_git(self):
        self.assertEqual(
            3,
            self.text.count("persist-credentials: false"),
        )

    def test_solo_http_404_autoriza_creacion(self):
        self.assertIn('case "$http_status" in', self.text)
        self.assertIn("200)", self.text)
        self.assertIn("404)", self.text)
        self.assertIn(
            "Release no existente (HTTP 404); se autoriza su creación.",
            self.text,
        )
        self.assertIn(
            "GitHub API devolvió HTTP $http_status; no se creará",
            self.text,
        )

    def test_errores_api_fallan_cerrado(self):
        self.assertIn('--write-out "%{http_code}"', self.text)
        self.assertIn(
            "X-GitHub-Api-Version: 2022-11-28",
            self.text,
        )
        self.assertIn(
            "No se puede determinar de forma segura el estado del Release.",
            self.text,
        )
        self.assertIn("exit 1", self.text)

    def test_publicacion_revalida_release_creado(self):
        marker = 'gh "${args[@]}"'
        self.assertIn(marker, self.text)
        after_create = self.text.split(marker, 1)[1]
        self.assertIn('gh release view "$RELEASE_TAG"', after_create)
        self.assertIn("--check-release-json", after_create)

    def test_auditoria_manual_no_publica(self):
        self.assertIn("auditar-todos-los-tags:", self.text)
        self.assertIn(
            "if: github.event_name == 'workflow_dispatch'",
            self.text,
        )


if __name__ == "__main__":
    unittest.main()
