"""Regresiones de DOC.2 R1 — reconstrucción histórica del CHANGELOG."""

from __future__ import annotations

import json
import re
from pathlib import Path
import unittest

from app.core.version_ledger import cargar_ledger

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "data/doc2-legacy-changelog-evidence.json"


class TestDOC2R1ChangelogReconstruction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        cls.changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    def test_evidencia_tiene_21_estados_y_80_commits(self):
        self.assertEqual(1, self.data["schema_version"])
        self.assertEqual("DOC.2 R1", self.data["doc2_revision"])
        self.assertEqual(21, self.data["state_count"])
        self.assertEqual(80, self.data["commit_count"])
        self.assertEqual(21, len(self.data["states"]))

    def test_versiones_rangos_y_conteos_son_los_reconstruidos(self):
        expected = [
            (1, "a0a9e09", "13ce028", 6),
            (2, "ae45943", "eafe54d", 3),
            (3, "a7e1ed4", "78e5188", 4),
            (4, "563d6c4", "2d4dfd0", 7),
            (5, "d41682c", "8a7e381", 3),
            (6, "fa5348f", "e087d6e", 4),
            (7, "c442ec2", "e956ea9", 4),
            (8, "6d4c2d8", "d599ee2", 3),
            (9, "376a967", "e6b02dc", 4),
            (10, "3f2f5d7", "8feb682", 6),
            (11, "c2da494", "1f350f6", 3),
            (12, "5607cc1", "6e6b33b", 3),
            (13, "b671c9a", "9f849d0", 2),
            (14, "5ca39ac", "f4a0d45", 6),
            (15, "88a1d14", "3430f2e", 3),
            (16, "338db37", "6f138da", 4),
            (17, "488aff5", "e55190b", 3),
            (18, "429201a", "11aefca", 3),
            (19, "e6c2310", "83a67ed", 3),
            (20, "e80d15e", "2a69fb8", 3),
            (21, "05232df", "7941f58", 3),
        ]
        for state, (number, start, end, count) in zip(self.data["states"], expected):
            self.assertEqual(number, state["global_revision"])
            self.assertEqual(f"0.0.{number}-beta", state["legacy_version"])
            self.assertTrue(state["range_start"].startswith(start))
            self.assertTrue(state["range_end"].startswith(end))
            self.assertEqual(count, state["commit_count"])

    def test_los_80_commits_son_unicos_y_respetan_extremos(self):
        shas = []
        for state in self.data["states"]:
            commits = state["commits"]
            self.assertEqual(state["commit_count"], len(commits))
            self.assertEqual(state["range_start"], commits[0]["sha"])
            self.assertEqual(state["range_end"], commits[-1]["sha"])
            shas.extend(item["sha"] for item in commits)
        self.assertEqual(80, len(shas))
        self.assertEqual(80, len(set(shas)))

    def test_changelog_contiene_detalle_de_cada_estado_y_commit(self):
        headings = re.findall(r"(?m)^### \[0\.0\.(\d+)-beta\]", self.changelog)
        legacy = [int(value) for value in headings if 1 <= int(value) <= 21]
        self.assertEqual(set(range(1, 22)), set(legacy))
        for state in self.data["states"]:
            self.assertIn(
                f"`{state['range_start'][:7]}` → `{state['range_end'][:7]}`",
                self.changelog,
            )
            self.assertIn(f"**{state['commit_count']} commits**", self.changelog)
            for commit in state["commits"]:
                self.assertIn(
                    f"`{commit['short_sha']}` — {commit['subject']}",
                    self.changelog,
                )

    def test_anomalia_del_commit_raiz_se_preserva(self):
        first = self.data["states"][0]["commits"][0]
        self.assertTrue(first["sha"].startswith("a0a9e09"))
        self.assertEqual("tipo: descripción del cambio", first["subject"])
        self.assertIn("anomalía histórica", self.changelog)

    def test_doc2_preserva_g111_sin_fijar_estado_actual(self):
        ledger = cargar_ledger()
        entry = next(e for e in ledger["entries"] if e["global_revision"] == 111)
        self.assertEqual("DOC.2", entry["block"])
        self.assertEqual("0.1.11.01-beta", entry["revision_aware"])
        self.assertTrue(self.data["reserved_candidate"]["consumed"])
        self.assertEqual(87, self.data["accepted_state"]["pull_request"])

    def test_doc2_preserva_contexto_g110_y_29_releases(self):
        audit = (
            ROOT
            / "docs/audits/documentation/changelog-reconstruction-doc2-r1.md"
        ).read_text(encoding="utf-8")
        self.assertIn("0.1.10.01-beta", audit)
        self.assertIn("G110/E01", audit)
        self.assertIn("29 tags formales", audit)
        self.assertIn("29 GitHub Releases", audit)

    def test_documentacion_preserva_g111_y_32_releases(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        releases = (ROOT / "RELEASES.md").read_text(encoding="utf-8")

        self.assertIn("G111/E01", readme)
        self.assertIn("G111/E01", releases)
        self.assertIn("v0.1.11.01-beta", releases)
        self.assertIn("32 tags formales reales", readme)
        self.assertIn("32 GitHub Releases", readme)

    def test_auditoria_doc2_existe_y_esta_indexada(self):
        audit_rel = "audits/documentation/changelog-reconstruction-doc2-r1.md"
        audit = ROOT / "docs" / audit_rel
        self.assertTrue(audit.is_file())
        text = audit.read_text(encoding="utf-8")
        self.assertIn("80 commits únicos", text)
        self.assertIn("G111/E01", text)
        index = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        self.assertIn(audit_rel, index)


if __name__ == "__main__":
    unittest.main()
