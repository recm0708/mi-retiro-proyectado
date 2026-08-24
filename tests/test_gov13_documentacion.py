"""Regresiones documentales de la primera revisión de GOV.1.3."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestGov13Documentacion(unittest.TestCase):
    def test_version_visible_en_readme_coincide_con_version_canonica(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"`{version}`", readme)

    def test_documentos_de_entrada_existen(self):
        requeridos = [
            "README.md",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "GOVERNANCE.md",
            "RELEASES.md",
            "VERSIONING.md",
            "docs/README.md",
            "docs/governance/roadmap.md",
            "docs/REGISTRO_CAMBIOS_HISTORICO.md",
            "docs/archive/README.md",
        ]
        for relativo in requeridos:
            with self.subTest(relativo=relativo):
                self.assertTrue((ROOT / relativo).is_file(), relativo)

    def test_bitacoras_ux_preservan_snapshot_y_documento_vivo_r4(self):
        casos = {
            "product/user-interface.md": "UX_4_6A_REDISENO_VISUAL.md",
            "product/workflow-step-1-personal-data.md": "UX_4_6B_PASO1_DATOS_PERSONALES.md",
            "product/workflow-step-2-contributions.md": "UX_4_6C_PASO2_CUOTAS.md",
            "product/workflow-step-3-salary-history.md": "UX_4_6D_PASO3_HISTORIAL.md",
        }
        for vivo, historico_nombre in casos.items():
            with self.subTest(vivo=vivo):
                historico = ROOT / "docs" / "archive" / "ux" / historico_nombre
                actual = ROOT / "docs" / vivo
                self.assertTrue(historico.is_file())
                self.assertTrue(actual.is_file())

    def test_changelog_tiene_estructura_por_version(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertTrue(texto.startswith("# Changelog\n"))
        self.assertIn("## [Unreleased]", texto)
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertIn(f"## [{version}]", texto)

    def test_roadmap_declara_gov13_en_ejecucion(self):
        texto = (ROOT / "docs" / "governance/roadmap.md").read_text(encoding="utf-8")
        self.assertIn("GOV.1.3", texto)
        self.assertIn("R1 — documentos de entrada", texto)
        self.assertIn("GOV.1.4", texto)
        self.assertIn("GOV.1.7", texto)

    def test_indice_separa_documentacion_historica(self):
        texto = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        self.assertIn("## 12. Historial de evolución", texto)
        self.assertIn("archive/ux/", texto)
        self.assertIn("## 13. Releases", texto)

    def test_editorconfig_exige_limpieza_markdown(self):
        texto = (ROOT / ".editorconfig").read_text(encoding="utf-8")
        bloque = re.search(r"\[\*\.md\](.*?)(?:\n\[|\Z)", texto, re.S)
        self.assertIsNotNone(bloque)
        self.assertIn("trim_trailing_whitespace = true", bloque.group(1))

    def test_documentacion_r1_sin_espacios_finales(self):
        archivos = [
            ROOT / "README.md",
            ROOT / "CHANGELOG.md",
            ROOT / "CONTRIBUTING.md",
            ROOT / "docs" / "README.md",
            ROOT / "docs" / "governance/roadmap.md",
            ROOT / "docs" / "REGISTRO_CAMBIOS_HISTORICO.md",
            ROOT / "docs" / "archive" / "README.md",
        ]
        errores = []
        for archivo in archivos:
            if not archivo.is_file():
                continue
            for numero, linea in enumerate(
                archivo.read_text(encoding="utf-8").splitlines(), start=1
            ):
                if linea.endswith((" ", "\t")):
                    errores.append(f"{archivo.relative_to(ROOT)}:{numero}")
        self.assertEqual([], errores, "Espacios finales: " + ", ".join(errores))
