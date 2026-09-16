"""MANT.1 R4 — limpieza de trazabilidad en encabezados operativos."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


ARCHIVOS_OPERATIVOS = (
    ".github/dependabot.yml",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/ISSUE_TEMPLATE/question.yml",
    ".github/workflows/verificar-tags.yml",
    ".githooks/README.md",
    "scripts/README.md",
)

TRAZABILIDAD_DE_REVISION = (
    "MANT.1",
    "MANT. 1",
    "DEV.2",
    "UX.4.6",
    "VER.2",
    "PR #",
)


class TestMant1R4EncabezadosOperativosLimpios(unittest.TestCase):
    """Evita que la trazabilidad histórica aparezca como encabezado operativo."""

    def _leer(self, ruta: str) -> str:
        return (ROOT / ruta).read_text(encoding="utf-8")

    def test_encabezados_operativos_no_declaran_revision(self):
        """Los primeros renglones describen el archivo, no la revisión que lo tocó."""

        for ruta in ARCHIVOS_OPERATIVOS:
            primeras_lineas = "\n".join(self._leer(ruta).splitlines()[:8])
            for patron in TRAZABILIDAD_DE_REVISION:
                with self.subTest(ruta=ruta, patron=patron):
                    self.assertNotIn(patron, primeras_lineas)

    def test_yaml_github_mantiene_encabezado_funcional(self):
        """Los YAML históricos vigentes conservan encabezado funcional."""

        yaml_paths = [
            ruta
            for ruta in ARCHIVOS_OPERATIVOS
            if ruta.endswith(
                (".yml", ".yaml")
            )
        ]

        for ruta in yaml_paths:
            primeras_lineas = (
                self._leer(ruta)
                .splitlines()[:4]
            )

            with self.subTest(ruta=ruta):
                self.assertTrue(
                    primeras_lineas[0].startswith("# ")
                )
                self.assertIn(
                    "# Propósito:",
                    primeras_lineas[1],
                )
                self.assertIn(
                    "# Alcance:",
                    primeras_lineas[2],
                )

    def test_readme_operativos_no_contienen_bloque_ni_origen_de_revision(self):
        """Los README técnicos explican uso permanente, no bitácora de MANT.1."""

        for ruta in (".githooks/README.md", "scripts/README.md"):
            texto = self._leer(ruta)
            with self.subTest(ruta=ruta):
                self.assertNotIn("**Bloque:**", texto)
                self.assertNotIn("**Origen:**", texto)
                self.assertIn("**Estado:** vigente", texto)
                self.assertIn("**Clasificación:** técnica / mantenimiento local", texto)

    def test_historia_mant1_r4_y_roadmap_vivo_usan_fuentes_correctas(self):
        historicos = (
            "CHANGELOG.md",
            "docs/standards/code-and-comments.md",
            "docs/operations/validation.md",
            "docs/architecture/system-architecture.md",
        )

        for ruta in historicos:
            texto = self._leer(ruta)

            with self.subTest(ruta=ruta):
                self.assertIn("MANT.1 R4", texto)
                self.assertIn(
                    "encabezados operativos",
                    texto,
                )

        ledger = self._leer(
            "docs/governance/pre-1-0-revision-ledger.md"
        )

        self.assertIn("G076", ledger)
        self.assertIn("MANT.1 R4", ledger)

        roadmap = self._leer(
            "docs/governance/roadmap.md"
        )

        self.assertIn("G125/E01", roadmap)
        self.assertIn("PLAN.2 R2", roadmap)

if __name__ == "__main__":
    unittest.main()
