"""Regresiones SEC.2 R1 para hardening CodeQL y workflows.

Protege la construcción segura del informe imprimible y los nombres
canónicos de los workflows propios de GitHub Actions.
"""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "app/static/js/results_orchestration.js"


class TestSEC2R1CodeQLWorkflowHardening(unittest.TestCase):

    def test_informe_dinamico_no_reinterpreta_datos_como_html(self):
        texto = JS.read_text(encoding="utf-8")

        bloque = texto.split(
            "function construirDocumentoImpresion",
            1,
        )[1].split(
            "function crearCabeceraImpresion",
            1,
        )[0]

        self.assertNotIn("documento.innerHTML", bloque)
        self.assertNotIn("pie.innerHTML", bloque)
        self.assertIn("textContent", bloque)
        self.assertIn("document.createTextNode", bloque)
        self.assertIn("document.createElement", bloque)

    def test_workflows_tienen_nombres_tecnicos_en_ingles(self):
        esperados = {
            "quality-gate.yml":
                "name: Repository Quality Gate",
            "dependency-security.yml":
                "name: Dependency Security",
            "scheduled-health.yml":
                "name: Scheduled Repository Health",
            "pr-labeler.yml":
                "name: PR Auto Labeler",
            "visual-a11y.yml":
                "name: Visual & Accessibility",
            "verificar-tags.yml":
                "name: Git Tag Signature Verification",
        }

        for archivo, nombre in esperados.items():
            with self.subTest(
                archivo=archivo
            ):
                contenido = (
                    ROOT
                    / ".github/workflows"
                    / archivo
                ).read_text(
                    encoding="utf-8"
                )

                self.assertIn(
                    nombre,
                    contenido,
                )



if __name__ == "__main__":
    unittest.main()
