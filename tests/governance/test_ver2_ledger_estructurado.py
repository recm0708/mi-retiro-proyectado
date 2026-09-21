"""Regresiones del ledger estructurado revision-aware."""

from copy import deepcopy
import json
from pathlib import Path
import unittest

from app.core.version_ledger import (
    LEDGER_FILE,
    LedgerRevisionError,
    cargar_ledger,
    validar_ledger,
)


ROOT = Path(__file__).resolve().parents[2]

LEDGER_MD = (
    ROOT
    / "docs"
    / "governance"
    / "pre-1-0-revision-ledger.md"
)

MATRIZ = (
    ROOT
    / "docs"
    / "archive"
    / "governance"
    / "ver2-revision-decision-matrix.md"
)


class TestVer2LedgerEstructurado(
    unittest.TestCase
):
    """Protege continuidad, schema y compatibilidad histórica."""

    @classmethod
    def setUpClass(
        cls,
    ):
        cls.ledger = cargar_ledger()

    def test_schema_v2_y_siguiente_global_canonico(
        self,
    ):
        self.assertTrue(
            LEDGER_FILE.is_file()
        )

        self.assertEqual(
            2,
            self.ledger[
                "schema_version"
            ],
        )

        accepted = self.ledger[
            "accepted_count"
        ]

        self.assertEqual(
            accepted,
            len(
                self.ledger[
                    "entries"
                ]
            ),
        )

        self.assertEqual(
            accepted + 1,
            self.ledger[
                "next_global"
            ],
        )

        self.assertNotIn(
            "next_global_if_ver2_accepted",
            self.ledger,
        )

    def test_globales_son_contiguos_y_version_actual_coincide(
        self,
    ):
        entries = self.ledger[
            "entries"
        ]

        globales = [
            entry[
                "global_revision"
            ]
            for entry in entries
        ]

        accepted = self.ledger[
            "accepted_count"
        ]

        self.assertEqual(
            list(
                range(
                    1,
                    accepted + 1,
                )
            ),
            globales,
        )

        version = (
            ROOT / "VERSION"
        ).read_text(
            encoding="utf-8"
        ).strip()

        self.assertEqual(
            version,
            entries[-1][
                "revision_aware"
            ],
        )

    def test_entradas_historicas_declaran_metadata_v2(
        self,
    ):
        for entry in self.ledger[
            "entries"
        ]:
            with self.subTest(
                global_revision=entry[
                    "global_revision"
                ]
            ):
                self.assertEqual(
                    1,
                    entry[
                        "identifier_schema"
                    ],
                )

                self.assertEqual(
                    "revision-aware-v1",
                    entry[
                        "version_format"
                    ],
                )

                self.assertEqual(
                    entry[
                        "ordinal"
                    ],
                    entry[
                        "edition"
                    ],
                )

                self.assertIn(
                    "functional_revision",
                    entry,
                )

                self.assertIsNone(
                    entry[
                        "correction_ordinal"
                    ]
                )

                self.assertIsInstance(
                    entry[
                        "maintenance_ordinal"
                    ],
                    int,
                )

    def test_mantenimiento_historico_tiene_ordinal_explicito(
        self,
    ):
        entries = {
            entry[
                "global_revision"
            ]: entry
            for entry in self.ledger[
                "entries"
            ]
        }

        self.assertEqual(
            1,
            entries[123][
                "maintenance_ordinal"
            ],
        )

        self.assertEqual(
            2,
            entries[127][
                "maintenance_ordinal"
            ],
        )

        for global_revision, entry in entries.items():
            if global_revision in (
                123,
                127,
            ):
                continue

            self.assertEqual(
                0,
                entry[
                    "maintenance_ordinal"
                ],
            )

    def test_candidato_permanece_sin_asignar(
        self,
    ):
        self.assertEqual(
            128,
            self.ledger[
                "next_global"
            ],
        )

        self.assertIsNone(
            self.ledger[
                "next_candidate"
            ]
        )

        self.assertIsNone(
            self.ledger[
                "next_candidate_block"
            ]
        )

    def test_validador_rechaza_hueco_global(
        self,
    ):
        altered = deepcopy(
            self.ledger
        )

        altered[
            "entries"
        ][9][
            "global_revision"
        ] = 99

        with self.assertRaises(
            LedgerRevisionError
        ):
            validar_ledger(
                altered
            )

    def test_validador_rechaza_edition_y_ordinal_divergentes(
        self,
    ):
        altered = deepcopy(
            self.ledger
        )

        altered[
            "entries"
        ][-1][
            "edition"
        ] = 99

        with self.assertRaises(
            LedgerRevisionError
        ):
            validar_ledger(
                altered
            )

    def test_validador_rechaza_formato_incoherente(
        self,
    ):
        altered = deepcopy(
            self.ledger
        )

        altered[
            "entries"
        ][-1][
            "version_format"
        ] = "revision-aware-v2"

        with self.assertRaises(
            LedgerRevisionError
        ):
            validar_ledger(
                altered
            )

    def test_validador_rechaza_siguiente_global_incorrecto(
        self,
    ):
        altered = deepcopy(
            self.ledger
        )

        altered[
            "next_global"
        ] = 999

        with self.assertRaises(
            LedgerRevisionError
        ):
            validar_ledger(
                altered
            )

    def test_validador_rechaza_clave_acoplada_obsoleta(
        self,
    ):
        altered = deepcopy(
            self.ledger
        )

        altered[
            "next_global_if_ver2_accepted"
        ] = altered[
            "next_global"
        ]

        with self.assertRaises(
            LedgerRevisionError
        ):
            validar_ledger(
                altered
            )

    def test_validador_acepta_entrada_revision_aware_v2_sintetica(
        self,
    ):
        altered = deepcopy(
            self.ledger
        )

        altered[
            "entries"
        ].append(
            {
                "global_revision": 128,
                "block": "SYNTHETIC",
                "ordinal": 1,
                "edition": 1,
                "functional_revision": "R1",
                "identifier_schema": 2,
                "version_format": "revision-aware-v2",
                "correction_ordinal": 0,
                "maintenance_ordinal": 0,
                "revision_aware": "0.128.1.0-beta",
                "state": "estado sintético de validación",
                "anchor": "test-only",
                "evidence": "test-only",
            }
        )

        altered[
            "accepted_count"
        ] = 128

        altered[
            "next_global"
        ] = 129

        validar_ledger(
            altered
        )

    def test_markdown_preserva_historia_reconciliada(
        self,
    ):
        ledger_md = LEDGER_MD.read_text(
            encoding="utf-8"
        )

        matriz = MATRIZ.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "**G070**",
            ledger_md,
        )

        self.assertIn(
            "G070 | `0.0.70.02-beta`",
            ledger_md,
        )

        self.assertIn(
            "**Total aceptado antes de VER.2** | **70**",
            matriz,
        )

        for value in (
            "G071–G108",
            "G109",
            "G110 | `0.1.10.01-beta`",
            "G111 | `0.1.11.01-beta`",
            "G112 | `0.1.12.07-beta`",
            "G113 | `0.1.13.03-beta`",
            "G114 | `0.1.14.01-beta`",
            "G115 | `0.1.15.04-beta`",
            "G116 | `0.1.16.05-beta`",
            "`0.0.71.01-beta`",
        ):
            with self.subTest(
                value=value
            ):
                self.assertIn(
                    value,
                    ledger_md,
                )

    def test_archivo_json_no_tiene_bom_y_parsea_directamente(
        self,
    ):
        raw = LEDGER_FILE.read_bytes()

        self.assertFalse(
            raw.startswith(bytes((0xEF, 0xBB, 0xBF)))
        )

        self.assertIsInstance(
            json.loads(
                raw.decode(
                    "utf-8"
                )
            ),
            dict,
        )


if __name__ == "__main__":
    unittest.main()
