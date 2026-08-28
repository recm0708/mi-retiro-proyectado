"""Regresiones NOR.2 R5 — archivo y consolidación histórica."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/audits/repository/repository-normalization-migration-matrix-nor2-r2.md"


ARCHIVE_RENAMES = {'docs/archive/governance/AUDITORIA_GITHUB.md': 'docs/archive/governance/github-audit.md', 'docs/archive/governance/AUDITORIA_MARKDOWN_POST_MANT1_DOC1_R1.md': 'docs/archive/governance/markdown-audit-post-mant1-doc1-r1.md', 'docs/archive/governance/AUDITORIA_PLAN1_R4_2026-08-20.md': 'docs/archive/governance/plan1-r4-audit-2026-08-20.md', 'docs/archive/governance/AUDITORIA_REPOSITORIO_2026-08-18.md': 'docs/archive/governance/repository-audit-2026-08-18.md', 'docs/archive/governance/AUDITORIA_VER2_CONTEO_PROVISIONAL.md': 'docs/archive/governance/ver2-provisional-count-audit.md', 'docs/archive/governance/AUDITORIA_VER2_SEGUNDA_PASADA.md': 'docs/archive/governance/ver2-second-pass-audit.md', 'docs/archive/governance/AUDITORIA_VERSIONADO_PRE_1_0.md': 'docs/archive/governance/pre-1-0-versioning-audit.md', 'docs/archive/governance/CIERRE_DOCUMENTAL_MARKDOWN_DOC1_R1.md': 'docs/archive/governance/doc1-r1-markdown-documentation-closeout.md', 'docs/archive/governance/CIERRE_GOV1.md': 'docs/archive/governance/gov1-closeout.md', 'docs/archive/governance/CONTEXTO_ACTUALIZACION_MARKDOWN_DOC1_R1.md': 'docs/archive/governance/doc1-r1-markdown-update-context.md', 'docs/archive/governance/LINEA_BASE_DOCUMENTAL_POST_MANT1_DOC1_R1.md': 'docs/archive/governance/doc1-r1-post-mant1-documentation-baseline.md', 'docs/archive/governance/MATRIZ_DECISION_MARKDOWN_DOC1_R1.md': 'docs/archive/governance/doc1-r1-markdown-decision-matrix.md', 'docs/archive/governance/MATRIZ_DECISION_REVISIONES_VER2.md': 'docs/archive/governance/ver2-revision-decision-matrix.md', 'docs/archive/governance/MIGRACION_FIRMAS_GIT_2026-08-17.md': 'docs/archive/governance/git-signature-migration-2026-08-17.md', 'docs/archive/governance/REGISTRO_CAMBIOS_HISTORICO.md': 'docs/archive/governance/historical-change-registry.md', 'docs/archive/governance/REVISION_SOLO_SI_APLICA_DOC1_R1.md': 'docs/archive/governance/doc1-r1-applicability-only-review.md', 'docs/archive/governance/VER2_R1_AUDITORIA_RECONCILIACION_POST_DOC1.md': 'docs/archive/governance/ver2-r1-post-doc1-reconciliation-audit.md', 'docs/archive/governance/VER2_R1_DECISION_OPERATIVA_POST_DOC1.md': 'docs/archive/governance/ver2-r1-post-doc1-operational-decision.md', 'docs/archive/governance/VER2_R1_MATRIZ_DECISION_RECONCILIACION_POST_DOC1.md': 'docs/archive/governance/ver2-r1-post-doc1-reconciliation-decision-matrix.md', 'docs/archive/governance/VER2_R2_ANALISIS_CONTRADICCIONES_POST_R1.md': 'docs/archive/governance/ver2-r2-post-r1-contradiction-analysis.md', 'docs/archive/governance/VER2_R2_CIERRE_DOCUMENTACION_VIVA_POST_R1.md': 'docs/archive/governance/ver2-r2-post-r1-live-documentation-closeout.md', 'docs/archive/governance/VER2_R2_PROPUESTA_CORRECCION_DOCUMENTACION_VIVA.md': 'docs/archive/governance/ver2-r2-live-documentation-correction-proposal.md', 'docs/archive/governance/VER2_R3_DECISION_VERSION_CANDIDATA_POST_R2.md': 'docs/archive/governance/ver2-r3-post-r2-candidate-version-decision.md', 'docs/archive/governance/VER2_R4_PROMOCION_G071_E01.md': 'docs/archive/governance/ver2-r4-g071-e01-promotion.md', 'docs/archive/governance/VER2_R5_ESTABILIZACION_POST_RELEASE.md': 'docs/archive/governance/ver2-r5-post-release-stabilization.md', 'docs/archive/technical/AUDITORIA_ARCHIVOS_R5F.md': 'docs/archive/technical/files-audit-r5f.md', 'docs/archive/technical/AUDITORIA_CALCULOS.md': 'docs/archive/technical/calculation-audit.md', 'docs/archive/technical/AUDITORIA_CARPETAS_R5E.md': 'docs/archive/technical/folders-audit-r5e.md', 'docs/archive/technical/AUDITORIA_DOCUMENTACION_R5G.md': 'docs/archive/technical/documentation-audit-r5g.md', 'docs/archive/technical/AUDITORIA_ESTRUCTURA_ARCHIVOS_R5D.md': 'docs/archive/technical/file-structure-audit-r5d.md', 'docs/archive/technical/AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md': 'docs/archive/technical/functional-audit-post-renames-r6.md', 'docs/archive/technical/AUDITORIA_NOMBRES_RESTANTES_R5H.md': 'docs/archive/technical/remaining-names-audit-r5h.md', 'docs/archive/technical/CIERRE_OPERATIVO_POST_AUDITORIA_R7.md': 'docs/archive/technical/operational-closeout-post-audit-r7.md', 'docs/archive/ux/AUDITORIA_UX46E_R7_2026-08-18.md': 'docs/archive/ux/ux46e-r7-audit-2026-08-18.md', 'docs/archive/ux/UX46H_R1_AUDITORIA_RESULTADOS.md': 'docs/archive/ux/ux46h-r1-results-audit.md', 'docs/archive/ux/UX46I_R1_AUDITORIA_COMO_SE_CALCULA.md': 'docs/archive/ux/ux46i-r1-calculation-explanation-audit.md'}


def parse_moves():
    text = MATRIX.read_text(encoding="utf-8")
    rows = re.findall(
        r"\| `(docs/[^`]+\.md)` "
        r"\| \*\*ARCHIVAR\*\* "
        r"\| `(docs/archive/(governance|technical|ux)/)` "
        r"\| R5 \|",
        text,
    )
    moves = []
    for src, dest_dir, category in rows:
        historical_dest = dest_dir + Path(src).name
        canonical_dest = ARCHIVE_RENAMES.get(historical_dest, historical_dest)
        moves.append((src, canonical_dest, category))
    return moves


MOVES = parse_moves()


class TestNOR2R5HistoricalDocumentation(unittest.TestCase):

    def test_36_documentos_archivados(self):
        self.assertEqual(36, len(MOVES))
        counts = {
            category: sum(c == category for _, _, c in MOVES)
            for category in ("governance", "technical", "ux")
        }
        self.assertEqual(
            {"governance": 25, "technical": 8, "ux": 3},
            counts,
        )
        self.assertEqual(36, len(ARCHIVE_RENAMES))

        for old, new, _ in MOVES:
            with self.subTest(old=old, new=new):
                self.assertFalse((ROOT / old).exists(), old)
                self.assertTrue((ROOT / new).is_file(), new)

    def test_raiz_docs_queda_solo_con_indice_markdown(self):
        markdown = sorted(p.name for p in (ROOT / "docs").glob("*.md"))
        self.assertEqual(["README.md"], markdown)

    def test_no_hay_markdown_con_contenido_identico(self):
        import hashlib

        hashes = {}
        duplicates = []

        for path in sorted((ROOT / "docs").rglob("*.md")):
            content = path.read_text(encoding="utf-8-sig")
            normalized = (
                content
                .replace("\r\n", "\n")
                .replace("\r", "\n")
                .strip()
            )
            digest = hashlib.sha256(
                normalized.encode("utf-8")
            ).hexdigest()

            if digest in hashes:
                duplicates.append(
                    (
                        hashes[digest],
                        path.relative_to(ROOT).as_posix(),
                    )
                )
            else:
                hashes[digest] = path.relative_to(ROOT).as_posix()

        self.assertEqual([], duplicates)

    def test_indices_historicos_sin_rutas_obsoletas(self):
        for rel in (
            "docs/archive/README.md",
            "docs/archive/governance/README.md",
            "docs/archive/technical/README.md",
            "docs/archive/ux/README.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            with self.subTest(rel=rel):
                self.assertNotIn("docs/INDICE.md", text)
                self.assertNotIn("../INDICE.md", text)
                self.assertNotIn(
                    "se mantienen como archivos de compatibilidad",
                    text,
                )

    def test_estado_transversal_r5(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        docs = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        sec2 = (
            ROOT / "docs/audits/security/sec2-final-closure.md"
        ).read_text(encoding="utf-8")

        self.assertIn("**NOR.2 R4:** cerrado", readme)
        self.assertIn("**NOR.2 R5:** cerrado", readme)
        self.assertIn("**NOR.2 R6:** cerrado", readme)
        self.assertIn("**NOR.2 R7:** cerrado", readme)
        self.assertIn("NOR.2 R5", docs)
        self.assertIn("NOR.2 R6", docs)
        self.assertIn(
            "**SEC.2:** R1 cerrado; hardening CodeQL del informe "
            "imprimible y normalización técnica de GitHub Actions "
            "completados.",
            readme,
        )
        self.assertIn("**Estado:** SEC.2 cerrado", sec2)
        self.assertIn("**Alcance completado:** SEC.2 R1–R6", sec2)
        self.assertIn("SEC.2 permanece **cerrado en R1–R6**", sec2)

    def test_evidencia_r5_existe(self):
        path = ROOT / (
            "docs/audits/repository/"
            "repository-normalization-historical-docs-nor2-r5.md"
        )
        self.assertTrue(path.is_file())
        text = path.read_text(encoding="utf-8")
        self.assertIn("36 documentos cerrados", text)
        self.assertIn("NOR.2 R6", text)

    def test_version_y_estado_transversal(self):
        from app.core.version import APP_VERSION
        self.assertEqual(
            APP_VERSION,
            (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        )

    def test_aplicador_temporal_no_permanece(self):
        self.assertFalse((ROOT / "apply_nor2_r5.py").exists())


if __name__ == "__main__":
    unittest.main()
