"""Cierre funcional UX.4.6e R8: procedencia editable y coherencia documental."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


class TestUx46eR8CierreFuncional(unittest.TestCase):
    """Protege el contrato aceptado tras la validación manual de Pasos 1–3."""

    def test_adr_167_es_consecutiva_y_esta_indexada(self):
        texto = (DOCS / "DECISIONES.md").read_text(encoding="utf-8")
        ids = [int(x) for x in re.findall(r"(?m)^## ADR-(\d{3})\s+—", texto)]
        indice = [int(x) for x in re.findall(r"(?m)^\| ADR-(\d{3}) \|", texto)]
        # ADR-001..ADR-167 son la evidencia histórica del cierre R8.
        # Las decisiones posteriores pueden crecer sin invalidar ese hito,
        # siempre que la numeración total siga siendo estrictamente consecutiva.
        self.assertGreaterEqual(len(ids), 167)
        self.assertEqual(list(range(1, max(ids) + 1)), ids)
        self.assertEqual(ids, indice)
        self.assertEqual(list(range(1, 168)), ids[:167])
        self.assertIn(
            "## ADR-167 — Los datos documentales confirmados son editables",
            texto,
        )

    def test_adr_167_sustituye_bloqueo_sin_anular_no_reduccion_silenciosa(self):
        texto = (DOCS / "DECISIONES.md").read_text(encoding="utf-8")
        self.assertIn("## ADR-167 — Los datos documentales confirmados son editables", texto)
        self.assertIn("ADR-088, ADR-103, ADR-105 y ADR-106", texto)
        self.assertIn("ADR-156 continúa vigente", texto)
        self.assertIn("no reduce silenciosamente", texto)

    def test_especificacion_permite_editar_excluir_y_reincluir(self):
        texto = (DOCS / "ESPECIFICACION_FUNCIONAL.md").read_text(encoding="utf-8")
        self.assertIn("la fotografía original permanecen separadas", texto)
        self.assertIn("excluir o reincluir explícitamente un período detectado", texto)
        self.assertIn("Excluido por ti", texto)

    def test_gestion_datos_preserva_original_y_copia_de_trabajo(self):
        texto = (DOCS / "GESTION_DATOS_SIMULACION.md").read_text(encoding="utf-8")
        self.assertIn("Procedencia editable y referencias documentales", texto)
        self.assertIn("fotografía original", texto)
        self.assertIn("copia de trabajo", texto)
        self.assertIn("Excluido por ti", texto)

    def test_modelo_documenta_metadata_frontend_sin_cambiar_pydantic(self):
        texto = (DOCS / "MODELO_DE_DATOS.md").read_text(encoding="utf-8")
        for esperado in (
            "referencia_mi_retiro_seguro_original",
            "ficha_digital_importada_original",
            "periodos_excluidos_importacion_ficha",
            "no cambian el documento fuente ni los modelos Pydantic",
        ):
            self.assertIn(esperado, texto)

    def test_changelog_registra_evidencia_funcional_r8(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        for esperado in (
            "R8.2 cerró funcionalmente con **644 pruebas en `OK`**",
            "282/6",
            "281/5",
            "B/.7,321.13",
            "B/.8,883.50",
            "ADR-167",
        ):
            self.assertIn(esperado, texto)

    def test_roadmap_y_readme_marcan_r8_cerrada_y_r9_en_cierre(self):
        texto = (DOCS / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("- [x] R8 — prueba funcional", texto)
        self.assertIn("- [x] R9 — cierre técnico y publicación del hito;", texto)
        self.assertIn(
            "[x] R9.1 — candidato local `0.0.25-beta` validado con 660 pruebas en `OK`",
            texto,
        )
        self.assertIn(
            "[x] R9.2 — PR #21 integrado por squash",
            texto,
        )
        self.assertIn("procedencia editable", texto)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("UX.4.6e:** cerrada en `0.0.25-beta`", readme)
        self.assertIn("660 pruebas en `OK`", readme)
        self.assertIn("PR #21 integrado por squash", readme)
        self.assertIn("**Bloque activo:** UX.4.6f", readme)

    def test_validacion_define_gate_documental_652_y_preserva_base_r8(self):
        texto = (DOCS / "VALIDACION.md").read_text(encoding="utf-8")
        self.assertIn("**644 pruebas en `OK`**", texto)
        self.assertIn("**8 regresiones adicionales**", texto)
        self.assertIn("**652 pruebas en `OK`**", texto)
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn(
            "`VERSION` permanece en `0.0.24-beta` hasta R9",
            changelog,
        )


if __name__ == "__main__":
    unittest.main()
