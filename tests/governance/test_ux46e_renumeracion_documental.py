"""Regresiones UX.4.6e R6 para renumeración documental y metadata GitHub."""

import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


class TestUX46eRenumeracionDocumental(unittest.TestCase):
    """Protege la secuencia vigente sin borrar la evidencia histórica."""

    @classmethod
    def setUpClass(cls):
        cls.roadmap = (DOCS / "governance/roadmap.md").read_text(encoding="utf-8")
        cls.publicacion = (DOCS / "operations/github-public-repository.md").read_text(encoding="utf-8")
        cls.decisiones = (DOCS / "decisions/README.md").read_text(encoding="utf-8")
        cls.cierre = (DOCS / "archive/governance/gov1-closeout.md").read_text(encoding="utf-8")
        cls.transparencia = (DOCS / "product/transparency.md").read_text(encoding="utf-8")
        cls.auditoria_r7 = (
            DOCS / "archive/ux/ux46e-r7-audit-2026-08-18.md"
        ).read_text(encoding="utf-8")

    def test_secuencia_historica_ux46e_a_h_permanece_registrada(self):
        registry = json.loads(
            (
                ROOT
                / "data/governance/"
                "work-block-registry.json"
            ).read_text(encoding="utf-8")
        )

        ids = {
            item["identifier"]
            for item in registry["identifiers"]
        }

        for bloque in (
            "UX.4.6e",
            "UX.4.6f",
            "UX.4.6g",
            "UX.4.6h",
        ):
            with self.subTest(bloque=bloque):
                self.assertIn(
                    bloque,
                    ids,
                )

        self.assertIn(
            "UX.4.6f/UX.4.6g/UX.4.6h",
            self.cierre,
        )

        self.assertIn(
            "PLAN.2 R2",
            self.roadmap,
        )

    def test_r5_r6_r7_permanecen_en_ledger_historico(self):
        ledger = json.loads(
            (
                ROOT
                / "data/governance/"
                "pre-1-0-revision-ledger.json"
            ).read_text(encoding="utf-8")
        )

        entries = {
            item["global_revision"]: item
            for item in ledger["entries"]
        }

        self.assertEqual(
            "R5 — coherencia visible",
            entries[45]["state"],
        )
        self.assertIn(
            "576 pruebas",
            entries[45]["evidence"],
        )

        self.assertEqual(
            "R6 — renumeración/metadata",
            entries[46]["state"],
        )
        self.assertIn(
            "586 pruebas",
            entries[46]["evidence"],
        )

        self.assertEqual(
            "R7 — auditoría transversal",
            entries[47]["state"],
        )
        self.assertIn(
            "598 pruebas",
            entries[47]["evidence"],
        )

    def test_transparencia_usa_alcance_actual_e_a_h(self):
        self.assertIn("cierre de UX.4.6e y del alcance funcional UX.4.6f–h", self.transparencia)
        self.assertNotIn("cierre funcional de UX.4.6e–g", self.transparencia)

    def test_cierre_gov1_preserva_numeracion_original_con_nota_posterior(self):
        self.assertIn("cierre funcional/UX de UX.4.6e, UX.4.6f y UX.4.6g", self.cierre)
        self.assertIn("Nota posterior — UX.4.6e R6", self.cierre)
        self.assertIn("UX.4.6f/UX.4.6g/UX.4.6h", self.cierre)

    def test_snapshots_historicos_no_se_reescriben(self):
        historico = (DOCS / "archive/roadmap-pre-gov1-3.md").read_text(encoding="utf-8")
        self.assertIn("UX.4.6e — Paso 4 · Proyección salarial/laboral", historico)
        auditoria = (DOCS / "archive" / "governance" / "repository-audit-2026-08-18.md").read_text(encoding="utf-8")
        self.assertIn("UX.4.6e — Paso 4 · Proyección salarial/laboral", auditoria)

    def test_adr164_documenta_regla_de_no_reescritura(self):
        self.assertIn("## ADR-164 — La renumeración vigente no reescribe la historia UX anterior", self.decisiones)
        self.assertIn("documentos vigentes deben usar esta secuencia", self.decisiones)
        self.assertIn("conservan sus identificadores originales", self.decisiones)

    def test_adr164_permanece_y_admite_decisiones_posteriores_consecutivas(self):
        ids = [int(x) for x in re.findall(r"(?m)^## ADR-(\d{3})\s+—", self.decisiones)]
        self.assertGreaterEqual(max(ids), 164)
        self.assertEqual(list(range(1, max(ids) + 1)), ids)

    def test_topics_priorizan_espanol_y_reservan_tecnologias_canonicas(self):
        for topic in (
            "accesibilidad",
            "jubilacion",
            "retiro",
            "seguridad-social-panama",
            "estimacion-previsional",
            "privacidad",
            "simulador-pension",
            "python",
            "fastapi",
        ):
            with self.subTest(topic=topic):
                self.assertIn(
                    f"`{topic}`",
                    self.publicacion,
                )

        for legacy in (
            "prevision-social",
            "seguridad-social",
        ):
            with self.subTest(legacy=legacy):
                self.assertNotIn(
                    f"- `{legacy}`",
                    self.publicacion,
                )

    def test_topic_sebd_panama_es_el_valor_final_configurado(self):
        self.assertIn("`sebd-panama`", self.publicacion)
        self.assertIn("20/20 topics", self.publicacion)
        self.assertIn("no forma parte de la taxonomía final", self.publicacion)
        self.assertNotIn("- `sebd`\n", self.publicacion)

    def test_taxonomia_vigente_declara_28_labels_y_preserva_checkpoint_21(self):
        self.assertIn("28 labels", self.publicacion)
        self.assertIn("16 labels canónicos", self.publicacion)
        self.assertIn("12 labels suplementarios", self.publicacion)

        for label in (
            "duplicate",
            "good first issue",
            "help wanted",
            "invalid",
            "wontfix",
        ):
            self.assertIn(f"`{label}`", self.publicacion)

        self.assertIn("**21 labels** configuradas", self.auditoria_r7)


if __name__ == "__main__":
    unittest.main()
