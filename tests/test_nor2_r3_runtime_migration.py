"""Regresiones de NOR.2 R3 — migración técnica de runtime y configuración."""

from importlib import import_module
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]

MOVES = {
    "app/services/centro_desarrollo.py": "app/services/development_center.py",
    "app/services/como_se_calcula.py": "app/services/calculation_guide.py",
    "app/services/detalle_anio_actual.py": "app/services/current_year_detail.py",
    "app/services/referencia_mi_retiro_seguro.py": "app/services/mi_retiro_seguro_reference.py",
    "app/static/css/como-se-calcula.css": "app/static/css/calculation-guide.css",
    "app/static/css/procedencia-editable.css": "app/static/css/editable-provenance.css",
    "app/static/js/detalle_anio_actual.js": "app/static/js/current_year_detail.js",
    "app/static/js/procedencia_editable.js": "app/static/js/editable_provenance.js",
    "app/static/js/referencia_mi_retiro_seguro.js": "app/static/js/mi_retiro_seguro_reference.js",
    "app/static/js/tema.js": "app/static/js/theme.js",
    "app/templates/como_se_calcula.html": "app/templates/calculation_guide.html",
    "app/templates/comparar.html": "app/templates/comparison.html",
    "app/templates/dev_centro_desarrollo.html": "app/templates/dev_development_center.html",
    "app/templates/metodologia.html": "app/templates/methodology.html",
    "app/templates/partials/detalle_anio_actual.html": "app/templates/partials/current_year_detail.html",
    "app/templates/partials/importacion_ficha_digital.html": "app/templates/partials/ficha_digital_import.html",
    "app/templates/partials/referencia_mi_retiro_seguro.html": "app/templates/partials/mi_retiro_seguro_reference.html",
    "tests/test_dev2_centro_desarrollo.py": "tests/test_dev2_development_center.py",
    "tests/test_ux44_detalle_anio_actual.py": "tests/test_ux44_current_year_detail.py",
    "tests/test_ux44_referencia_pdf.py": "tests/test_ux44_pdf_reference.py",
    "tests/test_ux46d_revision18_procedencia_persistencia.py": "tests/test_ux46d_revision18_provenance_persistence.py",
    "tests/test_ux46d_revision19_sincronizacion_actual.py": "tests/test_ux46d_revision19_current_sync.py",
    "tests/test_ux46d_revision23_ficha_actualiza_cuotas.py": "tests/test_ux46d_revision23_ficha_updates_contributions.py",
    "tests/test_ux46e_r81_procedencia_editable.py": "tests/test_ux46e_r81_editable_provenance.py",
    "tests/test_ux46f_r1_consistencia_procedencia_adjuntos.py": "tests/test_ux46f_r1_attachment_provenance_consistency.py",
    "tests/test_ux46g_r1_escenarios_retiro.py": "tests/test_ux46g_r1_retirement_scenarios.py",
    "tests/test_ux46i_r1_como_se_calcula.py": "tests/test_ux46i_r1_calculation_guide.py",
    "regulations/general_parameters.json": "regulations/general-parameters.json",
}


class TestNOR2R3RuntimeMigration(unittest.TestCase):

    def test_28_movimientos_materializados(self):
        self.assertEqual(28, len(MOVES))
        for old, new in MOVES.items():
            with self.subTest(old=old, new=new):
                self.assertFalse((ROOT / old).exists(), old)
                self.assertTrue((ROOT / new).is_file(), new)

    def test_modulos_python_migrados_importan(self):
        for module in (
            "app.services.development_center",
            "app.services.calculation_guide",
            "app.services.current_year_detail",
            "app.services.mi_retiro_seguro_reference",
        ):
            with self.subTest(module=module):
                import_module(module)

    def test_ficha_digital_permanece_excepcion_de_dominio(self):
        self.assertTrue((ROOT / "app/services/ficha_digital.py").is_file())

    def test_runtime_app_no_referencia_nombres_tecnicos_antiguos(self):
        old_tokens = [
            "centro_desarrollo.py",
            "como_se_calcula.py",
            "detalle_anio_actual.py",
            "referencia_mi_retiro_seguro.py",
            "como-se-calcula.css",
            "procedencia-editable.css",
            "detalle_anio_actual.js",
            "procedencia_editable.js",
            "referencia_mi_retiro_seguro.js",
            "tema.js",
            "como_se_calcula.html",
            "comparar.html",
            "dev_centro_desarrollo.html",
            "metodologia.html",
            "partials/detalle_anio_actual.html",
            "partials/importacion_ficha_digital.html",
            "partials/referencia_mi_retiro_seguro.html",
            "app.services.centro_desarrollo",
            "app.services.como_se_calcula",
            "app.services.detalle_anio_actual",
            "app.services.referencia_mi_retiro_seguro",
            "general_parameters.json",
        ]
        errores = []
        for path in (ROOT / "app").rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {
                ".py", ".html", ".js", ".css", ".json", ".md"
            }:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for token in old_tokens:
                if token in text:
                    errores.append(f"{path.relative_to(ROOT).as_posix()}: {token}")
        self.assertEqual([], errores)

    def test_urls_publicas_en_espanol_no_cambian(self):
        main = (ROOT / "app/main.py").read_text(encoding="utf-8")
        for route in (
            "/como-se-calcula",
            "/comparar",
            "/metodologia",
            "/dev/centro-desarrollo",
        ):
            self.assertIn(route, main)

    def test_documentacion_transversal_declara_nor2_r3(self):
        evidencia = (
            ROOT
            / "docs"
            / "audits"
            / "repository"
            / "repository-normalization-runtime-migration-nor2-r3.md"
        ).read_text(encoding="utf-8")

        self.assertIn("NOR.2 R3", evidencia)

        for rel in (
            "CHANGELOG.md",
            "README.md",
            "docs/README.md",
            "docs/governance/roadmap.md",
            "docs/operations/validation.md",
            "docs/governance/master-plan-to-1-0.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("NOR.2 R4", text, rel)

    def test_evidencia_r3_existe(self):
        report = (
            ROOT
            / "docs"
            / "audits"
            / "repository"
            / "repository-normalization-runtime-migration-nor2-r3.md"
        )
        self.assertTrue(report.is_file())
        text = report.read_text(encoding="utf-8")
        self.assertIn("28", text)
        self.assertIn("URL públicas", text)
        self.assertIn("Ficha Digital", text)
        self.assertIn("R4", text)

    def test_version_no_cambia(self):
        self.assertEqual(
            "0.1.09.01-beta",
            (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        )

    def test_aplicador_temporal_no_queda_en_arbol(self):
        self.assertFalse((ROOT / "apply_nor2_r3.py").exists())


if __name__ == "__main__":
    unittest.main()
