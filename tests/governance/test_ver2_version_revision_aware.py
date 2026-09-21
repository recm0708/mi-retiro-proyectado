"""VER.2 — regresiones del esquema beta revision-aware y su ledger."""

from pathlib import Path
import re
import sys
import unittest

from app.core.version import (
    construir_version_beta_revision,
    construir_version_beta_revision_v2,
    descomponer_version_beta_revision,
    descomponer_version_beta_revision_v2,
    version_valida,
)


ROOT = Path(__file__).resolve().parents[2]
LEDGER = (
    ROOT
    / "docs"
    / "governance"
    / "pre-1-0-revision-ledger.md"
)
AUDITORIA = (
    ROOT
    / "docs"
    / "archive"
    / "governance"
    / "pre-1-0-versioning-audit.md"
)

SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(
        0,
        str(SCRIPTS),
    )

from release_contract import (  # noqa: E402
    parse_revision_aware,
    parse_revision_aware_components,
)


class TestVer2VersionRevisionAware(unittest.TestCase):
    """Protege v1/v2 sin reescribir la historia publicada."""

    def test_constructor_codifica_contador_global_y_revision_local(self):
        self.assertEqual(
            "0.0.01.01-beta",
            construir_version_beta_revision(
                1,
                1,
            ),
        )
        self.assertEqual(
            "0.0.70.02-beta",
            construir_version_beta_revision(
                70,
                2,
            ),
        )
        self.assertEqual(
            "0.0.71.01-beta",
            construir_version_beta_revision(
                71,
                1,
            ),
        )
        self.assertEqual(
            "0.1.00.03-beta",
            construir_version_beta_revision(
                100,
                3,
            ),
        )
        self.assertEqual(
            "0.4.25.12-beta",
            construir_version_beta_revision(
                425,
                12,
            ),
        )

    def test_constructor_rechaza_origen_y_ordinal_fuera_de_rango(self):
        with self.assertRaises(
            ValueError
        ):
            construir_version_beta_revision(
                0,
                1,
            )

        with self.assertRaises(
            ValueError
        ):
            construir_version_beta_revision(
                71,
                0,
            )

        with self.assertRaises(
            ValueError
        ):
            construir_version_beta_revision(
                71,
                100,
            )

    def test_descomposicion_recupera_contadores(self):
        self.assertEqual(
            (70, 2),
            descomponer_version_beta_revision(
                "0.0.70.02-beta"
            ),
        )
        self.assertEqual(
            (71, 1),
            descomponer_version_beta_revision(
                "0.0.71.01-beta"
            ),
        )
        self.assertEqual(
            (100, 3),
            descomponer_version_beta_revision(
                "0.1.00.03-beta"
            ),
        )
        self.assertEqual(
            (425, 12),
            descomponer_version_beta_revision(
                "0.4.25.12-beta"
            ),
        )

    def test_familias_legacy_revision_aware_y_oficial_siguen_validas(self):
        self.assertTrue(
            version_valida(
                "0.0.1-beta"
            )
        )
        self.assertTrue(
            version_valida(
                "0.0.26-beta"
            )
        )
        self.assertTrue(
            version_valida(
                "0.0.71.01-beta"
            )
        )
        self.assertTrue(
            version_valida(
                "1.0.0.0"
            )
        )
        self.assertTrue(
            version_valida(
                "1.0.0.1"
            )
        )

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
            with self.subTest(
                version=version
            ):
                self.assertFalse(
                    version_valida(
                        version
                    )
                )

    def test_constructor_v2_usa_forma_corta_sin_maintenance(self):
        self.assertEqual(
            "0.128.2.0-beta",
            construir_version_beta_revision_v2(
                128,
                2,
            ),
        )
        self.assertEqual(
            "0.129.2.1-beta",
            construir_version_beta_revision_v2(
                129,
                2,
                correction=1,
            ),
        )
        self.assertEqual(
            "0.234.7.12-beta",
            construir_version_beta_revision_v2(
                234,
                7,
                correction=12,
            ),
        )

    def test_constructor_v2_rechaza_limites_invalidos(self):
        casos = (
            (127, 1, 0),
            (128, 0, 0),
            (128, 100, 0),
            (128, 1, -1),
            (128, 1, 1000),
        )
        for caso in casos:
            with self.subTest(caso=caso):
                with self.assertRaises(ValueError):
                    construir_version_beta_revision_v2(*caso)

    def test_descomposicion_v2_recupera_componentes(self):
        self.assertEqual(
            (128, 2, 0),
            descomponer_version_beta_revision_v2(
                "0.128.2.0-beta"
            ),
        )
        self.assertEqual(
            (129, 2, 1),
            descomponer_version_beta_revision_v2(
                "0.129.2.1-beta"
            ),
        )

    def test_parser_generico_preserva_global_y_edition_para_v2(self):
        self.assertEqual(
            (128, 2),
            descomponer_version_beta_revision(
                "0.128.2.0-beta"
            ),
        )

    def test_familia_v2_es_valida_sin_invalidar_v1(self):
        validas = (
            "0.0.71.01-beta",
            "0.1.27.02-beta",
            "0.128.2.0-beta",
            "0.129.2.1-beta",
            "0.234.7.12-beta",
        )
        for version in validas:
            with self.subTest(version=version):
                self.assertTrue(version_valida(version))

    def test_familia_v2_rechaza_forma_larga_y_padding(self):
        invalidas = (
            "0.127.2.0-beta",
            "0.128.02.0-beta",
            "0.128.2.00-beta",
            "0.128.0.0-beta",
            "0.128.100.0-beta",
            "0.128.2.000.000-beta",
            "0.2.34.07.000.000-beta",
        )
        for version in invalidas:
            with self.subTest(version=version):
                self.assertFalse(version_valida(version))

    def test_release_contract_normaliza_v1_y_expone_v2(self):
        self.assertEqual(
            (127, 2),
            parse_revision_aware(
                "0.1.27.02-beta"
            ),
        )
        self.assertEqual(
            (127, 2, 0, 0, 1),
            parse_revision_aware_components(
                "0.1.27.02-beta"
            ),
        )
        self.assertEqual(
            (128, 2, 0, 0, 2),
            parse_revision_aware_components(
                "0.128.2.0-beta"
            ),
        )
        self.assertEqual(
            (129, 2, 1, 0, 2),
            parse_revision_aware_components(
                "0.129.2.1-beta"
            ),
        )
        self.assertEqual(
            (129, 2),
            parse_revision_aware(
                "0.129.2.1-beta"
            ),
        )

    def test_release_contract_rechaza_revision_aware_ambigua(self):
        invalidas = (
            "0.00.71.01-beta",
            "0.128.02.0-beta",
            "0.128.2.00-beta",
            "0.2.34.07.000.000-beta",
        )
        for version in invalidas:
            with self.subTest(version=version):
                with self.assertRaises(ValueError):
                    parse_revision_aware_components(version)

    def test_ledger_contiene_g001_a_g108_sin_huecos_ni_duplicados(self):
        texto = LEDGER.read_text(
            encoding="utf-8"
        )

        globales = [
            int(valor)
            for valor in re.findall(
                r"^\| G(\d{3}) \| `0\.",
                texto,
                flags=re.MULTILINE,
            )
        ]

        historicos = [
            value
            for value in globales
            if 1 <= value <= 108
        ]

        self.assertEqual(
            list(
                range(
                    1,
                    109,
                )
            ),
            historicos,
        )

        self.assertEqual(
            108,
            len(
                historicos
            ),
        )

        self.assertEqual(
            len(
                historicos
            ),
            len(
                set(
                    historicos
                )
            ),
        )

    def test_ids_del_ledger_codifican_su_global(self):
        texto = LEDGER.read_text(
            encoding="utf-8"
        )

        filas = re.findall(
            r"^\| G(\d{3}) \| `(0\.[^`]+-beta)` \|",
            texto,
            flags=re.MULTILINE,
        )

        aceptadas = filas[
            :108
        ]

        self.assertEqual(
            108,
            len(
                aceptadas
            ),
        )

        for global_texto, version in aceptadas:
            with self.subTest(
                global_texto=global_texto,
                version=version,
            ):
                descompuesta = (
                    descomponer_version_beta_revision(
                        version
                    )
                )

                self.assertIsNotNone(
                    descompuesta
                )

                self.assertEqual(
                    int(
                        global_texto
                    ),
                    descompuesta[
                        0
                    ],
                )

    def test_g071_historico_y_anomalia_de_promocion_quedan_documentados(
        self,
    ):
        ledger = LEDGER.read_text(
            encoding="utf-8"
        )

        auditoria = AUDITORIA.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "G071",
            ledger,
        )

        self.assertIn(
            "v0.0.71.01-beta",
            ledger,
        )

        self.assertIn(
            "VER.2",
            auditoria,
        )

        self.assertIn(
            "G087",
            ledger,
        )

        self.assertIn(
            "anomalía",
            ledger.lower(),
        )


if __name__ == "__main__":
    unittest.main()
