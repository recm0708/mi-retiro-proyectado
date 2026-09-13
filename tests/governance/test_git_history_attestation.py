"""Regresiones de la atestación histórica Git pre-UX.5."""

from __future__ import annotations

import unittest

from scripts import audit_git_history_attestation


class TestGitHistoryAttestation(
    unittest.TestCase
):
    @classmethod
    def setUpClass(cls):
        cls.data = (
            audit_git_history_attestation
            .load_manifest()
        )
        cls.entries = cls.data[
            "commits"
        ]

    def test_snapshot_contiene_195_identidades_continuas(
        self,
    ):
        self.assertEqual(
            195,
            len(self.entries),
        )
        self.assertEqual(
            [
                f"HIST-{index:04d}"
                for index in range(
                    1,
                    196,
                )
            ],
            [
                entry["hist_id"]
                for entry in self.entries
            ],
        )

    def test_frontera_de_firma_es_exacta_y_continua(
        self,
    ):
        unsigned = [
            entry
            for entry in self.entries
            if not entry[
                "signature_present"
            ]
        ]
        signed = [
            entry
            for entry in self.entries
            if entry[
                "signature_present"
            ]
        ]

        self.assertEqual(
            89,
            len(unsigned),
        )
        self.assertEqual(
            106,
            len(signed),
        )
        self.assertEqual(
            "HIST-0089",
            unsigned[-1]["hist_id"],
        )
        self.assertEqual(
            "HIST-0090",
            signed[0]["hist_id"],
        )

    def test_normalizaciones_de_idioma_estan_declaradas(
        self,
    ):
        expected = set(
            self.data[
                "language_attestation"
            ][
                "canonicalized_hist_ids"
            ]
        )
        actual = {
            entry["hist_id"]
            for entry in self.entries
            if entry[
                "canonicalization_category"
            ]
            != "preservado_es_o_tecnico"
        }

        self.assertEqual(
            19,
            len(expected),
        )
        self.assertEqual(
            expected,
            actual,
        )

        for entry in self.entries:
            if entry["hist_id"] in expected:
                self.assertTrue(
                    entry[
                        "subject_canonical_es"
                    ].strip()
                )

    def test_auditor_contrasta_snapshot_con_git_real(
        self,
    ):
        report = (
            audit_git_history_attestation
            .audit_history()
        )
        self.assertEqual(
            "pass",
            report["result"],
            report["errors"],
        )

    def test_identidad_actual_se_calcula_sin_modificar_commits(
        self,
    ):
        count = len(
            audit_git_history_attestation
            .history_shas(
                "HEAD"
            )
        )
        self.assertEqual(
            f"HIST-{count:04d}",
            audit_git_history_attestation
            .current_history_identity(
                "HEAD"
            ),
        )

    def test_presencia_de_firma_se_deriva_del_objeto_commit(
        self,
    ):
        self.assertFalse(
            audit_git_history_attestation
            .commit_has_signature(
                self.entries[88]["sha"]
            )
        )

        self.assertTrue(
            audit_git_history_attestation
            .commit_has_signature(
                self.entries[89]["sha"]
            )
        )


if __name__ == "__main__":
    unittest.main()
