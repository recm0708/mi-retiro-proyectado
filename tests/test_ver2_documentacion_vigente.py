"""VER.2 — coherencia entre versión candidata, ledger y documentación vigente."""

from pathlib import Path
import unittest

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
VERSION_CANDIDATA = "0.0.58.01-beta"


class TestVer2DocumentacionVigente(unittest.TestCase):
    """Evita que la reconciliación revision-aware vuelva a divergir."""

    def test_version_candidata_es_g058_e01_y_runtime_coincide(self):
        version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertEqual(VERSION_CANDIDATA, version)
        self.assertEqual(version, APP_VERSION)
        self.assertEqual((58, 1), descomponer_version_beta_revision(version))

    def test_superficies_de_estado_declaran_candidato_y_legacy(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (DOCS / "ROADMAP.md").read_text(encoding="utf-8")
        plan = (DOCS / "PLAN_MAESTRO_HACIA_1_0.md").read_text(encoding="utf-8")
        security = (ROOT / "SECURITY.md").read_text(encoding="utf-8")

        self.assertIn(f"**Versión candidata de VER.2:** `{VERSION_CANDIDATA}`", readme)
        self.assertIn("**Última versión formal legacy etiquetada:** `0.0.26-beta`", readme)
        self.assertIn(f"**Versión candidata:** `{VERSION_CANDIDATA}`", roadmap)
        self.assertIn("**Último tag formal legacy:** `v0.0.26-beta`", roadmap)
        self.assertIn(f"**Versión candidata transversal VER.2:** `{VERSION_CANDIDATA}`", plan)
        self.assertIn(f"| `{VERSION_CANDIDATA}` | Candidata vigente de VER.2", security)

    def test_dev2_es_siguiente_y_no_bloque_iniciado(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        roadmap = (DOCS / "ROADMAP.md").read_text(encoding="utf-8")
        plan = (DOCS / "PLAN_MAESTRO_HACIA_1_0.md").read_text(encoding="utf-8")

        self.assertIn("**Bloque transversal activo:** VER.2", readme)
        self.assertIn("**Siguiente bloque funcional:** DEV.2", readme)
        self.assertIn("VER.2 es un bloque transversal", roadmap)
        self.assertIn("**Estado:** siguiente bloque funcional; pendiente de inicio hasta cerrar VER.2.", plan)
        self.assertNotIn("### 6. DEV.2 — Centro de desarrollo\n\n**Estado:** activo.", plan)

    def test_ux46i_no_inventa_r1_1_en_documentacion_vigente(self):
        rutas = (
            ROOT / "README.md",
            DOCS / "ROADMAP.md",
            DOCS / "PLAN_MAESTRO_HACIA_1_0.md",
            ROOT / "CHANGELOG.md",
            DOCS / "VALIDACION.md",
            DOCS / "MATRIZ_TRAZABILIDAD.md",
            DOCS / "ARQUITECTURA.md",
        )
        patrones_invalidos = (
            "UX.4.6i R1.1",
            "UX.4.6i R1/R1.1",
            "R1/R1.1/R1.2/R1.3/R1.4",
        )
        for ruta in rutas:
            texto = ruta.read_text(encoding="utf-8")
            for patron in patrones_invalidos:
                with self.subTest(ruta=ruta.name, patron=patron):
                    self.assertNotIn(patron, texto)

    def test_ledger_y_auditoria_declaran_57_y_reservan_58(self):
        ledger = (DOCS / "LEDGER_REVISIONES_PRE_1_0.md").read_text(encoding="utf-8")
        auditoria = (DOCS / "AUDITORIA_VERSIONADO_PRE_1_0.md").read_text(encoding="utf-8")
        self.assertIn("**Contador aceptado en la base:** **G057**", ledger)
        self.assertIn("**57 estados aceptados**", auditoria)
        self.assertIn("G058", ledger)
        self.assertIn(VERSION_CANDIDATA, ledger)
        self.assertIn("G058 solo queda consumido", (ROOT / "VERSIONING.md").read_text(encoding="utf-8"))

    def test_tags_legacy_permanecen_historicos_e_inmutables(self):
        versioning = (ROOT / "VERSIONING.md").read_text(encoding="utf-8")
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")
        for version in range(22, 27):
            tag = f"v0.0.{version}-beta"
            with self.subTest(tag=tag):
                self.assertIn(tag, versioning)
                self.assertIn(tag, releases)
        self.assertIn("No se crean tags revision-aware retrospectivos", versioning)


if __name__ == "__main__":
    unittest.main()