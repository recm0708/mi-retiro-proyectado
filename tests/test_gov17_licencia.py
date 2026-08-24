"""GOV.1.7 — licencia y estrategia de distribución."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestGov17Licencia(unittest.TestCase):
    def test_license_propietaria_existe_y_reserva_derechos(self):
        texto = (ROOT / "LICENSE").read_text(encoding="utf-8")
        for esperado in (
            "Rubén Enrique Cañizares Miranda",
            "All rights reserved",
            "PROPRIETARY LICENSE NOTICE",
            "No license is granted",
            "THIRD_PARTY_NOTICES.md",
        ):
            self.assertIn(esperado, texto)

    def test_avisos_terceros_cubren_directas_y_bootstrap(self):
        texto = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
        for esperado in (
            "FastAPI | 0.141.1 | MIT",
            "Jinja2 | 3.1.6 | BSD-3-Clause",
            "Pydantic | 2.13.4 | MIT",
            "python-multipart | 0.0.32 | Apache-2.0",
            "pypdf | 6.16.1 | BSD-3-Clause",
            "Uvicorn | 0.52.3 | BSD-3-Clause",
            "Bootstrap | 5.3.8 | MIT",
        ):
            self.assertIn(esperado, texto)

    def test_decision_documenta_alternativas_y_no_relicencia(self):
        texto = (DOCS / "governance/licensing-and-distribution.md").read_text(
            encoding="utf-8"
        )
        for esperado in (
            "MIT",
            "Apache-2.0",
            "GPL-3.0 / AGPL-3.0",
            "Propietaria / todos los derechos reservados",
            "Decisión GOV.1.7",
            "no relicencia",
            "revisión jurídica externa",
        ):
            self.assertIn(esperado, texto)

    def test_readme_declara_licencia_y_cierre_gov17(self):
        texto = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("**GOV.1.7:** Licencia propietaria pre-beta", texto)
        self.assertIn("cerrado", texto)
        self.assertIn("(LICENSE)", texto)
        self.assertIn("(THIRD_PARTY_NOTICES.md)", texto)

    def test_roadmap_preserva_cierre_gov17(self):
        texto = (DOCS / "governance/roadmap.md").read_text(encoding="utf-8")
        self.assertIn("- [x] **GOV.1.7 — Licencia**", texto)
        self.assertIn("**GOV.1.8 — Auditoría final y cierre pre-beta de gobierno**", texto)

    def test_governance_respeta_decision_propietaria(self):
        texto = (ROOT / "GOVERNANCE.md").read_text(encoding="utf-8")
        self.assertIn("licencia propietaria pre-beta", texto)
        self.assertIn("THIRD_PARTY_NOTICES.md", texto)
        self.assertIn("relicencia", texto)

    def test_release_exige_avisos_de_terceros(self):
        texto = (DOCS / "operations/release-process.md").read_text(encoding="utf-8")
        self.assertIn("THIRD_PARTY_NOTICES.md", texto)
        self.assertIn("inventario exacto del artefacto", texto)
        self.assertIn("licencias/NOTICE upstream", texto)

    def test_version_no_cambia_y_archivos_limpios(self):
        licencia_doc = (DOCS / "governance/licensing-and-distribution.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("`0.0.23-beta`", licencia_doc)
        for path in (
            ROOT / "LICENSE",
            ROOT / "THIRD_PARTY_NOTICES.md",
            DOCS / "governance/licensing-and-distribution.md",
        ):
            texto = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                self.assertNotIn(
                    r"\n",
                    texto,
                    "Se detectaron saltos de línea escapados literalmente.",
                )
                self.assertGreater(
                    len(texto.splitlines()),
                    5,
                    "El documento debe contener saltos de línea reales.",
                )
                self.assertFalse(
                    any(ord(c) < 32 and c not in "\n\r\t" for c in texto)
                )
                self.assertFalse(
                    any(
                        linea.endswith((" ", "\t"))
                        for linea in texto.splitlines()
                    )
                )


if __name__ == "__main__":
    unittest.main()
