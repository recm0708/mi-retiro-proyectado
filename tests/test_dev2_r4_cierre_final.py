"""Regresiones DEV.2 R4: cierre final documental."""

from __future__ import annotations

from pathlib import Path
import unittest

from app.core.version import APP_VERSION


ROOT = Path(__file__).resolve().parents[1]


class TestDev2R4CierreFinal(unittest.TestCase):
    @staticmethod
    def _leer(ruta: str) -> str:
        return (ROOT / ruta).read_text(encoding="utf-8")

    def test_dev2_queda_cerrado_sin_promover_version(self):
        documento = self._leer("docs/DEV2_CENTRO_DESARROLLO.md")

        self.assertIn("**Estado:** DEV.2 cerrado documentalmente en R4.", documento)
        self.assertIn("**Estado:** R1 integrado en `main` mediante PR #37.", documento)
        self.assertIn("**Estado R2:** integrado en `main` mediante PR #39.", documento)
        self.assertIn("**Estado R3:** integrado en `main` mediante PR #40.", documento)
        self.assertIn("DEV.2 R4 no crea tag", documento)
        self.assertIn("DEV.2 R4 no cambia VERSION", documento)
        self.assertIn("0.0.26-beta", documento)
        self.assertIn("882 passed, 695 subtests passed", documento)

        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual("0.0.26-beta", version)
        self.assertEqual("0.0.26-beta", APP_VERSION)

    def test_superficies_principales_no_presentan_dev2_como_no_iniciado(self):
        superficies = {
            "README.md": self._leer("README.md"),
            "CHANGELOG.md": self._leer("CHANGELOG.md"),
            "docs/ARQUITECTURA.md": self._leer("docs/ARQUITECTURA.md"),
            "docs/ADR_179_VERSIONADO_REVISION_AWARE.md": self._leer(
                "docs/ADR_179_VERSIONADO_REVISION_AWARE.md"
            ),
        }
        combinado = "\n".join(superficies.values())

        for prohibido in (
            "DEV.2 permanece como siguiente bloque funcional y no comienza hasta cerrar VER.2",
            "DEV.2 no comienza hasta cerrar VER.2",
            "mientras DEV.2 R1 permanezca en desarrollo",
            "R2 en desarrollo",
            "R3 en desarrollo",
        ):
            self.assertNotIn(prohibido, combinado)

    def test_readme_y_changelog_marcan_dev2_cerrado_y_ver2_pendiente(self):
        readme = self._leer("README.md")
        changelog = self._leer("CHANGELOG.md")

        self.assertIn("**Bloque funcional cerrado:** DEV.2", readme)
        self.assertIn("**Siguiente bloque funcional:** DEV.2", readme)
        self.assertIn("referencia histórica preservada", readme)
        self.assertIn("cerrado documentalmente en R4", readme)
        self.assertIn("**Bloque transversal pendiente:** VER.2", readme)
        self.assertIn("### DEV.2 — cierre del Centro de desarrollo", changelog)
        self.assertIn("cierra documentalmente DEV.2", changelog)
        self.assertIn("deja VER.2 como siguiente cierre transversal", changelog)

    def test_arquitectura_conserva_alcance_tecnico_sin_rutas_publicas_nuevas(self):
        arquitectura = self._leer("docs/ARQUITECTURA.md")

        self.assertIn("**Última actualización técnica:** DEV.2 R4", arquitectura)
        self.assertIn("/dev/centro-desarrollo", arquitectura)
        self.assertIn("no añade rutas públicas nuevas", arquitectura)
        self.assertIn("no modifica motores previsionales", arquitectura)
        self.assertIn("conserva `0.0.26-beta` como versión visible", arquitectura)
        self.assertNotIn("mientras DEV.2 R1 permanezca en desarrollo", arquitectura)


if __name__ == "__main__":
    unittest.main()
