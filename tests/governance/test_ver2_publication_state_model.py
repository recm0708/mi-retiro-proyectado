"""Regresiones del modelo snapshot/candidato/publicación de versionado."""

from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[2]

SCRIPTS = ROOT / "scripts"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(
        0,
        str(SCRIPTS),
    )

import release_publication  # noqa: E402
import release_readiness  # noqa: E402


LEDGER = (
    ROOT
    / "data"
    / "governance"
    / "pre-1-0-revision-ledger.json"
)

REGISTRY = (
    ROOT
    / "data"
    / "governance"
    / "work-block-registry.json"
)

MANIFEST = (
    ROOT
    / "data"
    / "governance"
    / "release-publication-manifest.json"
)


class TestVer2PublicationStateModel(
    unittest.TestCase
):
    @classmethod
    def setUpClass(
        cls,
    ):
        cls.ledger = json.loads(
            LEDGER.read_text(
                encoding="utf-8"
            )
        )

        cls.registry = json.loads(
            REGISTRY.read_text(
                encoding="utf-8"
            )
        )

        cls.manifest = json.loads(
            MANIFEST.read_text(
                encoding="utf-8"
            )
        )

    def test_ledger_no_contiene_workflow_state(
        self,
    ):
        self.assertEqual(
            2,
            self.ledger[
                "schema_version"
            ],
        )

        self.assertNotIn(
            "active_phase",
            self.ledger,
        )

        self.assertNotIn(
            "next_candidate_assignment",
            self.ledger,
        )

        self.assertEqual(
            129,
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

    def test_registry_es_dueno_del_estado_vivo(
        self,
    ):
        self.assertEqual(
            2,
            self.registry[
                "schema_version"
            ],
        )

        baseline = self.registry[
            "accepted_baseline"
        ]

        self.assertEqual(
            (
                128,
                2,
                "0.128.2.0-beta",
                "VER.2",
                "R6",
            ),
            (
                baseline[
                    "global_revision"
                ],
                baseline[
                    "edition"
                ],
                baseline[
                    "revision_aware"
                ],
                baseline[
                    "block"
                ],
                baseline[
                    "functional_revision"
                ],
            ),
        )

        active = self.registry[
            "active_phase"
        ]

        self.assertEqual(
            (
                "VER.2",
                "R6",
                164,
                "accepted_pending_integration",
            ),
            (
                active[
                    "block"
                ],
                active[
                    "revision"
                ],
                active[
                    "issue"
                ],
                active[
                    "state"
                ],
            ),
        )

        self.assertEqual(128, active["global_revision"])
        self.assertEqual("0.128.2.0-beta", active["revision_aware"])

        candidate = self.registry[
            "current_candidate"
        ]

        self.assertEqual(
            "accepted_pending_integration",
            candidate[
                "state"
            ],
        )

        self.assertEqual(
            129,
            candidate[
                "next_global_available"
            ],
        )

        self.assertEqual(128, candidate["global_revision"])
        self.assertEqual(2, candidate["edition"])

    def test_mantenimiento_cerrado_y_ver2_activo(
        self,
    ):
        ids = {
            item[
                "identifier"
            ]: item
            for item in self.registry[
                "identifiers"
            ]
        }

        self.assertEqual(
            "closed_r2",
            ids[
                "MANT.2"
            ][
                "status"
            ],
        )

        self.assertEqual(
            "accepted_r6_pending_integration",
            ids[
                "VER.2"
            ][
                "status"
            ],
        )

    def test_manifest_es_snapshot_release_input(
        self,
    ):
        manifest = self.manifest

        self.assertEqual(
            2,
            manifest[
                "schema_version"
            ],
        )

        self.assertEqual(
            "release-input",
            manifest[
                "snapshot_role"
            ],
        )

        self.assertEqual(
            "runtime",
            manifest[
                "publication_resolution"
            ],
        )

        self.assertEqual(
            128,
            manifest[
                "global_revision"
            ],
        )

        self.assertEqual(
            2,
            manifest[
                "edition"
            ],
        )

        self.assertEqual(
            2,
            manifest[
                "identifier_schema"
            ],
        )

        self.assertEqual(
            0,
            manifest[
                "correction_ordinal"
            ],
        )

        self.assertEqual(
            0,
            manifest[
                "maintenance_ordinal"
            ],
        )

        for forbidden in (
            "publication_state",
            "published_commit",
            "tag_object",
            "release_id",
            "published_at",
        ):
            with self.subTest(
                forbidden=forbidden
            ):
                self.assertNotIn(
                    forbidden,
                    manifest,
                )

    def test_manifest_valida_sin_usar_candidato_vivo(
        self,
    ):
        version = (
            ROOT / "VERSION"
        ).read_text(
            encoding="utf-8"
        ).strip()

        self.assertEqual(
            [],
            release_publication.validate_manifest(
                self.manifest,
                version,
                self.ledger,
            ),
        )

    def test_readiness_reporta_snapshot_y_estado_vivo_por_separado(
        self,
    ):
        report = (
            release_readiness.build_report()
        )

        self.assertEqual(
            "pass",
            report[
                "result"
            ],
            report[
                "errors"
            ],
        )

        self.assertEqual(
            "release-input",
            report[
                "manifest_snapshot_role"
            ],
        )

        self.assertEqual(
            129,
            report[
                "next_global"
            ],
        )

        self.assertIsNone(
            report[
                "next_candidate"
            ]
        )


if __name__ == "__main__":
    unittest.main()
