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

    def test_dev2_queda_cerrado_y_version_actual_sigue_canonica(self):
        documento = self._leer("docs/architecture/development-center.md")

        self.assertIn(
            "**Estado general:** DEV.2 R1–R4 preservados; "
            "R5 integrado y aceptado como G118/E04; "
            "R6 queda como candidato G119/E05.",
            documento,
        )
        self.assertIn("## Alcance de R5", documento)
        self.assertIn("G118/E04", documento)
        self.assertIn("DEV.2 R4 cierra documentalmente el bloque funcional", documento)
        self.assertIn("**Estado R1:** integrado en `main` mediante PR #37.", documento)
        self.assertIn("**Estado R2:** integrado en `main` mediante PR #39.", documento)
        self.assertIn("**Estado R3:** integrado en `main` mediante PR #40.", documento)
        self.assertIn("DEV.2 R4 no crea tag", documento)
        self.assertIn("DEV.2 R4 no cambia VERSION", documento)
        self.assertIn("0.0.26-beta", documento)
        self.assertIn("882 passed, 695 subtests passed", documento)

        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(APP_VERSION, version)

    def test_superficies_principales_no_presentan_dev2_como_no_iniciado(self):
        superficies = {
            "README.md": self._leer("README.md"),
            "CHANGELOG.md": self._leer("CHANGELOG.md"),
            "docs/architecture/system-architecture.md": self._leer("docs/architecture/system-architecture.md"),
            "docs/decisions/adr-179-revision-aware-versioning.md": self._leer(
                "docs/decisions/adr-179-revision-aware-versioning.md"
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

    def test_readme_refleja_dev2_cerrado_y_evidencia_preserva_su_historia(self):
        readme = self._leer("README.md")
        documento = self._leer("docs/architecture/development-center.md")
        changelog = self._leer("CHANGELOG.md")
        sec2 = self._leer("docs/audits/security/sec2-final-closure.md")

        self.assertIn("**DEV.2:** cerrado.", readme)
        self.assertIn("**NOR.2 R4:** cerrado", readme)
        self.assertIn("**NOR.2 R5:** cerrado", readme)
        self.assertIn("**NOR.2 R6:** cerrado", readme)
        self.assertIn("**NOR.2 R7:** cerrado", readme)
        self.assertIn(
            "**SEC.2:** R1 cerrado; hardening CodeQL del informe "
            "imprimible y normalización técnica de GitHub Actions "
            "completados.",
            readme,
        )
        self.assertIn("**Estado:** SEC.2 cerrado", sec2)
        self.assertIn("**Alcance completado:** SEC.2 R1–R6", sec2)
        self.assertIn("SEC.2 permanece **cerrado en R1–R6**", sec2)
        self.assertIn("DEV.2 R4 cierra documentalmente el bloque funcional", documento)
        self.assertIn(
            "R5 está integrado mediante PR #107 / merge `bc97db0`",
            documento,
        )
        self.assertIn("aceptado como G118/E04", documento)
        self.assertIn("G119/E05", documento)
        self.assertIn("### DEV.2 — cierre del Centro de desarrollo", changelog)
        self.assertIn("cierra documentalmente DEV.2", changelog)
        self.assertIn("deja VER.2 como siguiente cierre transversal", changelog)

    def test_arquitectura_conserva_alcance_tecnico_sin_rutas_publicas_nuevas(self):
        arquitectura = self._leer("docs/architecture/system-architecture.md")

        self.assertIn(
            "**Última actualización técnica:** DEV.2 R5 — Portal Developer "
            "y separación de acceso web/Bearer — 2026-08-28",
            arquitectura,
        )
        self.assertIn("`/dev` como entrada humana canónica", arquitectura)
        self.assertIn("/dev/centro-desarrollo", arquitectura)
        self.assertIn("no añade rutas públicas nuevas", arquitectura)
        self.assertIn("no modifica motores previsionales", arquitectura)
        self.assertIn("conserva `0.0.26-beta` como versión visible", arquitectura)
        self.assertNotIn("mientras DEV.2 R1 permanezca en desarrollo", arquitectura)


if __name__ == "__main__":
    unittest.main()
