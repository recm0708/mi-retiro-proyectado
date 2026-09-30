"""Regresiones de firma Git, tags y evidencia de la migración criptográfica."""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"

class TestGovFirmaGit(unittest.TestCase):
    def setUp(self):
        self.version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    def test_allowed_signers_contiene_solo_clave_publica_autorizada(self):
        p = ROOT / ".github" / "allowed_signers"
        self.assertTrue(p.is_file())
        texto = p.read_text(encoding="utf-8").strip()
        self.assertIn("ruben.canizares@outlook.com ssh-ed25519 ", texto)
        self.assertNotIn("PRIVATE KEY", texto)
        self.assertNotIn("BEGIN OPENSSH", texto)

    def test_workflow_de_firmas_existe_y_tiene_doble_modo(self):
        texto = (ROOT / ".github" / "workflows" / "verificar-tags.yml").read_text(encoding="utf-8")
        self.assertIn('tags:', texto)
        self.assertIn('"v*"', texto)
        self.assertIn("workflow_dispatch:", texto)
        self.assertIn("git tag -v", texto)
        self.assertIn("actions/checkout@v7", texto)
        self.assertNotIn("actions/checkout@v6", texto)

    def test_workflow_usa_allowed_signers_versionado(self):
        texto = (
            ROOT
            / ".github"
            / "workflows"
            / "verificar-tags.yml"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "gpg.format ssh",
            texto,
        )
        self.assertIn(
            "gpg.ssh.allowedSignersFile",
            texto,
        )
        self.assertIn(
            ".github/allowed_signers",
            texto,
        )
        self.assertIn(
            "fetch-depth: 0",
            texto,
        )

        gate = (
            ROOT
            / ".github"
            / "workflows"
            / "quality-gate.yml"
        ).read_text(
            encoding="utf-8"
        )

        for action in (
            "actions/checkout@v7",
            "actions/setup-python@v7",
            "actions/setup-node@v7",
        ):
            with self.subTest(action=action):
                self.assertIn(
                    action,
                    gate,
                )

        for old in (
            "actions/checkout@v6",
            "actions/setup-python@v6",
            "actions/setup-node@v6",
        ):
            self.assertNotIn(
                old,
                gate,
            )


    def test_versioning_distingue_firmas_actuales_de_historia(self):
        texto = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        self.assertIn(
            "No crear tags revision-aware retrospectivos para G001–G070",
            texto,
        )
        self.assertIn(
            "No reescribir commits históricos para añadir firmas",
            texto,
        )
        self.assertIn("No falsear fechas históricas de tags", texto)


    def test_versioning_exige_firma_en_nuevos_commits_y_tags(self):
        texto = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        release = (
            DOCS / "operations/release-process.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "los commits canónicos nuevos siguen la política de firma SSH",
            texto,
        )
        self.assertIn(
            "todo tag formal nuevo se firma y verifica",
            texto,
        )
        self.assertIn(".github/allowed_signers", texto)
        self.assertIn('git tag -s "v$version"', release)


    def test_governance_y_contributing_exigen_firma(self):
        gov = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
        con = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("firma criptográfica SSH", gov)
        self.assertIn("git verify-commit HEAD", gov)
        self.assertIn("Los commits canónicos deben estar firmados", con)
        self.assertIn("firma SSH", con)
        self.assertIn("git verify-commit HEAD", con)

    def test_proceso_release_verifica_commit_y_tag_firmados(self):
        texto = (DOCS / "operations/release-process.md").read_text(encoding="utf-8")
        self.assertIn("git verify-commit", texto)
        self.assertIn("git tag -s", texto)
        self.assertIn("git tag -v", texto)

    def test_documento_migracion_contiene_23_tags(self):
        texto = (DOCS / "archive/governance/git-signature-migration-2026-08-17.md").read_text(encoding="utf-8")
        tags = set(re.findall(r"`v0\.0\.(\d+)-beta`", texto))
        self.assertEqual({str(i) for i in range(1, 24)}, tags)

    def test_documento_migracion_preserva_objetos_y_targets_originales(self):
        texto = (DOCS / "archive/governance/git-signature-migration-2026-08-17.md").read_text(encoding="utf-8")
        for valor in (
            "31accfc9a6014367179c97cfe54c5a223be8988f",
            "609edf4bfed33c64770c88fab401002cd90f8e66",
            "bda764edb84ccaeb610a629fca1283bbd97e69a4",
            "06b9260dadbcb2f0a7711841e1fad228e1badee8",
            "1222de61a6d2ca48fb8731fe4755f5b7eeef38f5",
            "07278f7a193ce964612d9697da57350691bf62c0",
            "90e66a13eec554d616bb71a04e00da4ada68df54",
        ):
            self.assertIn(valor, texto)
        self.assertIn("**Materialización criptográfica:** completada el 2026-08-17.", texto)
        self.assertIn("23/23 tags", texto)
        self.assertIn("23/23 objetos tag remotos", texto)
        self.assertIn("23/23 targets remotos", texto)

    def test_adr159_documenta_migracion_y_adr158_sustitucion_parcial(self):
        texto = (DOCS / "decisions/README.md").read_text(encoding="utf-8")
        self.assertIn("## ADR-159 —", texto)
        self.assertIn("Parcialmente sustituida por ADR-159", texto)
        ids = [int(x) for x in re.findall(r"(?m)^## ADR-(\d{3})\s+—", texto)]
        # ADR-001..ADR-159 constituyen la evidencia histórica de la migración.
        # Las ADR posteriores pueden crecer sin invalidar esta regresión, pero la
        # numeración completa debe seguir siendo única y estrictamente consecutiva.
        self.assertGreaterEqual(len(ids), 159)
        self.assertEqual(list(range(1, max(ids) + 1)), ids)
        self.assertEqual(list(range(1, 160)), ids[:159])


    def test_firma_historica_y_roadmap_vivo_usan_fuentes_correctas(self):
        roadmap = (
            DOCS / "governance/roadmap.md"
        ).read_text(encoding="utf-8")

        self.assertIn(
            "**Versión publicada:** `0.129.3.0-beta`",
            roadmap,
        )
        self.assertIn(
            "**Fase material activa:** DOC.4 R1 / #171",
            roadmap,
        )
        self.assertIn("G129/E03/C0", roadmap)
        self.assertIn("G130, libre y sin candidato", roadmap)

        migracion = (
            DOCS
            / "archive/governance/"
            "git-signature-migration-2026-08-17.md"
        ).read_text(encoding="utf-8")
        for esperado in (
            "Materialización criptográfica:",
            "primer commit posterior a la frontera histórica firmado",
            "`v0.0.1-beta` a `v0.0.21-beta`",
            "`v0.0.22-beta` y `v0.0.23-beta`",
            "23/23 tags verificaron localmente",
            "23/23 objetos tag remotos",
            "23/23 targets remotos",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, migracion)

        auditoria = (
            DOCS / "archive/governance/github-audit.md"
        ).read_text(encoding="utf-8").casefold()
        for esperado in ("ruleset", "dependabot", "main"):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, auditoria)


    def test_historia_y_contratos_vigentes_registran_firma(self):
        migracion = (
            DOCS
            / "archive/governance/"
            "git-signature-migration-2026-08-17.md"
        ).read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        governance = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")

        self.assertIn("23/23 tags", migracion)
        self.assertTrue((ROOT / ".github/allowed_signers").is_file())
        self.assertIn("firma SSH", changelog)
        self.assertIn("git verify-commit HEAD", governance)

        for ruta in (
            ROOT / "CONTRIBUTING.md",
            DOCS / "operations/release-process.md",
            DOCS / "operations/validation.md",
        ):
            contenido = ruta.read_text(encoding="utf-8")
            controles = [
                char for char in contenido
                if ord(char) < 32 and char not in "\n\r\t"
            ]
            self.assertEqual([], controles, f"carácter de control en {ruta}")

if __name__ == "__main__":
    unittest.main()
