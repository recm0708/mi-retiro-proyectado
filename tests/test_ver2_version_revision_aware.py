"""VER.2 — regresiones del esquema beta revision-aware y su ledger."""

from pathlib import Path
import re
import unittest

from app.core.version import (
    construir_version_beta_revision,
    descomponer_version_beta_revision,
    version_valida,
)


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "governance/pre-1-0-revision-ledger.md"
AUDITORIA = ROOT / "docs" / "AUDITORIA_VERSIONADO_PRE_1_0.md"


class TestVer2VersionRevisionAware(unittest.TestCase):
    """Protege la codificación nueva sin reescribir la historia publicada."""

    def test_constructor_codifica_contador_global_y_revision_local(self):
        self.assertEqual("0.0.01.01-beta", construir_version_beta_revision(1, 1))
        self.assertEqual("0.0.70.02-beta", construir_version_beta_revision(70, 2))
        self.assertEqual("0.0.71.01-beta", construir_version_beta_revision(71, 1))
        self.assertEqual("0.1.00.03-beta", construir_version_beta_revision(100, 3))
        self.assertEqual("0.4.25.12-beta", construir_version_beta_revision(425, 12))

    def test_constructor_rechaza_origen_y_ordinal_fuera_de_rango(self):
        with self.assertRaises(ValueError):
            construir_version_beta_revision(0, 1)
        with self.assertRaises(ValueError):
            construir_version_beta_revision(71, 0)
        with self.assertRaises(ValueError):
            construir_version_beta_revision(71, 100)

    def test_descomposicion_recupera_contadores(self):
        self.assertEqual((70, 2), descomponer_version_beta_revision("0.0.70.02-beta"))
        self.assertEqual((71, 1), descomponer_version_beta_revision("0.0.71.01-beta"))
        self.assertEqual((100, 3), descomponer_version_beta_revision("0.1.00.03-beta"))
        self.assertEqual((425, 12), descomponer_version_beta_revision("0.4.25.12-beta"))

    def test_familias_legacy_revision_aware_y_oficial_siguen_validas(self):
        self.assertTrue(version_valida("0.0.1-beta"))
        self.assertTrue(version_valida("0.0.26-beta"))
        self.assertTrue(version_valida("0.0.71.01-beta"))
        self.assertTrue(version_valida("1.0.0.0"))
        self.assertTrue(version_valida("1.0.0.1"))

    def test_revision_aware_rechaza_cero_y_formatos_ambiguos(self):
        invalidas = (
            "0.0.00.01-beta",
            "0.0.71.00-beta",
            "0.00.71.01-beta",
            "0.0.071.01-beta",
            "0.0.71.1-beta",
            "0.0.71.001-beta",
        )
        for version in invalidas:
            with self.subTest(version=version):
                self.assertFalse(version_valida(version))

    def test_ledger_contiene_g001_a_g070_sin_huecos_ni_duplicados(self):
        texto = LEDGER.read_text(encoding="utf-8")
        globales = [
            int(valor)
            for valor in re.findall(r"^\| G(\d{3}) \| `0\.", texto, flags=re.MULTILINE)
        ]
        # La tabla del ledger contiene G001–G070; la fila candidata G071 se
        # mantiene separada en la sección Próximo estado.
        self.assertEqual(list(range(1, 71)), globales[:70])
        self.assertEqual(70, len(globales[:70]))
        self.assertEqual(len(globales[:70]), len(set(globales[:70])))

    def test_ids_del_ledger_codifican_su_global(self):
        texto = LEDGER.read_text(encoding="utf-8")
        filas = re.findall(
            r"^\| G(\d{3}) \| `(0\.[^`]+-beta)` \|",
            texto,
            flags=re.MULTILINE,
        )
        aceptadas = filas[:70]
        self.assertEqual(70, len(aceptadas))
        for global_texto, version in aceptadas:
            with self.subTest(global_texto=global_texto, version=version):
                descompuesta = descomponer_version_beta_revision(version)
                self.assertIsNotNone(descompuesta)
                self.assertEqual(int(global_texto), descompuesta[0])

    def test_g071_permanece_condicionado_al_cierre_ver2(self):
        ledger = LEDGER.read_text(encoding="utf-8")
        auditoria = AUDITORIA.read_text(encoding="utf-8")
        self.assertIn("G071", ledger)
        self.assertIn("`0.0.71.01-beta`", ledger)
        self.assertIn("VER.2", auditoria)
        self.assertNotRegex(
            ledger,
            r"^\| G071 \| `0\.0\.71\.01-beta` \| VER\.2 R1.*aceptado",
        )


if __name__ == "__main__":
    unittest.main()
