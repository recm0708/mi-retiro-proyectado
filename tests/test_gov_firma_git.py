from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
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
        texto = (ROOT / ".github" / "workflows" / "verificar-tags.yml").read_text(encoding="utf-8")
        self.assertIn("gpg.format ssh", texto)
        self.assertIn("gpg.ssh.allowedSignersFile", texto)
        self.assertIn(".github/allowed_signers", texto)
        self.assertIn("fetch-depth: 0", texto)

        ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(
            encoding="utf-8"
        )
        for action in (
            "actions/checkout@v7",
            "actions/setup-python@v7",
            "actions/setup-node@v7",
        ):
            self.assertIn(action, ci)

        self.assertNotIn("actions/checkout@v6", ci)
        self.assertNotIn("actions/setup-python@v6", ci)
        self.assertNotIn("actions/setup-node@v6", ci)

    def test_versioning_distingue_tags_retrospectivos_de_fecha_historica(self):
        texto = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        self.assertIn("tags retrospectivos firmados", texto)
        self.assertIn("no existieron como tags en sus fechas históricas", texto)
        self.assertIn("no reescribe commits históricos", texto)

    def test_versioning_exige_firma_en_nuevos_commits_y_tags(self):
        texto = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        self.assertIn("Todo commit nuevo", texto)
        self.assertIn("Todo tag formal nuevo", texto)
        self.assertIn("`git tag -s`", texto)

    def test_governance_y_contributing_exigen_firma(self):
        gov = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
        con = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("firma criptográfica", gov)
        self.assertIn("git verify-commit", gov)
        self.assertIn("commit.gpgSign", con)
        self.assertIn("git verify-commit", con)

    def test_proceso_release_verifica_commit_y_tag_firmados(self):
        texto = (DOCS / "PROCESO_RELEASE.md").read_text(encoding="utf-8")
        self.assertIn("git verify-commit", texto)
        self.assertIn("git tag -s", texto)
        self.assertIn("git tag -v", texto)

    def test_documento_migracion_contiene_23_tags(self):
        texto = (DOCS / "MIGRACION_FIRMAS_GIT_2026-08-17.md").read_text(encoding="utf-8")
        tags = set(re.findall(r"`v0\.0\.(\d+)-beta`", texto))
        self.assertEqual({str(i) for i in range(1, 24)}, tags)

    def test_documento_migracion_preserva_objetos_y_targets_originales(self):
        texto = (DOCS / "MIGRACION_FIRMAS_GIT_2026-08-17.md").read_text(encoding="utf-8")
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
        self.assertIn("Materialización criptográfica completada", texto)
        self.assertIn("23/23 tags", texto)
        self.assertIn("23/23 objetos tag remotos", texto)
        self.assertIn("23/23 targets remotos", texto)

    def test_adr159_documenta_migracion_y_adr158_sustitucion_parcial(self):
        texto = (DOCS / "DECISIONES.md").read_text(encoding="utf-8")
        self.assertIn("## ADR-159 —", texto)
        self.assertIn("Parcialmente sustituida por ADR-159", texto)
        ids = [int(x) for x in re.findall(r"(?m)^## ADR-(\d{3})\s+—", texto)]
        self.assertEqual(list(range(1, 160)), ids)

    def test_roadmap_declara_version_canonica_y_prebloque_firma(self):
        texto = (DOCS / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn(f"**Versión de aplicación:** `{self.version}`", texto)
        self.assertIn("Firma e integridad Git/GitHub", texto)
        self.assertIn("- [x] primer commit nuevo firmado y verificado por GitHub;", texto)
        self.assertIn("- [x] materialización firmada de `v0.0.1-beta` a `v0.0.21-beta`;", texto)
        self.assertIn("- [x] reemisión firmada única de `v0.0.22-beta` y `v0.0.23-beta`;", texto)
        self.assertIn("- [x] auditoría local/remota 23/23 tags;", texto)
        self.assertIn("- [x] ruleset de tags;", texto)
        self.assertIn("- [x] protección/ruleset de `main`;", texto)
        self.assertIn("- [ ] **Prebloque transversal — Firma e integridad Git/GitHub**", texto)

    def test_indice_changelog_y_validacion_registran_firma(self):
        indice = (DOCS / "INDICE.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        validacion = (DOCS / "VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("MIGRACION_FIRMAS_GIT_2026-08-17.md", indice)
        self.assertIn(".github/allowed_signers", indice)
        self.assertIn("firma SSH", changelog)
        self.assertIn("23/23", changelog)
        self.assertIn("12 regresiones", validacion)
        self.assertIn("470 pruebas en `OK`", validacion)
        self.assertIn("23/23 objetos remotos", validacion)

if __name__ == "__main__":
    unittest.main()
