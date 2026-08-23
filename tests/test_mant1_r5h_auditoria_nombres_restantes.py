"""Regresión MANT.1 R5H para nombres técnicos restantes."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


EXPECTED_PATHS = [
    ".github/workflows/governance-audit.yml",
    "app/core/pdf_files.py",
    "app/core/money.py",
    "app/core/observability.py",
    "app/models/simulation.py",
    "app/models/traceability.py",
    "app/models/unified_result.py",
    "app/services/comparator.py",
    "app/services/contribution_projection.py",
    "app/services/mixto_results.py",
    "app/services/reference_date.py",
    "app/services/regulatory_sources.py",
    "app/services/results.py",
    "app/services/retirement.py",
    "app/services/salary_history.py",
    "app/services/salary_projection.py",
    "app/services/sebd_results.py",
    "app/services/sucgs_results.py",
    "app/services/timeline.py",
    "app/services/traceability.py",
    "app/services/unified_result.py",
    "app/static/css/accessibility.css",
    "app/static/css/results.css",
    "app/static/js/accessibility.js",
    "app/static/js/attachment_processing.js",
    "app/static/js/comparator.js",
    "app/static/js/currency.js",
    "app/static/js/data_management.js",
    "app/static/js/official_data_import.js",
    "app/static/js/privacy.js",
    "app/static/js/results.js",
    "app/static/js/results_orchestration.js",
    "app/static/js/retirement.js",
    "app/static/js/salary_history.js",
    "app/static/js/simulation.js",
    "app/static/js/timeline.js",
    "app/static/js/wizard_navigation.js",
    "app/templates/partials/data_management.html",
    "app/templates/partials/official_data_import.html",
    "app/templates/partials/privacy_consent.html",
    "app/templates/partials/results.html",
    "app/templates/partials/retirement.html",
    "app/templates/partials/salary_history.html",
    "app/templates/simulation.html",
    "tests/test_accessibility_themes.py",
    "tests/test_accessibility_ux4.py",
    "tests/test_money.py",
    "tests/test_timeline.py",
    "tests/test_unified_result.py",
    "tests/test_visual_identity_pre_r8.py",
    "tests/test_visual_stabilization.py",
]


PRESERVED_PATHS = [
    "app/core/normativa.py",
    "app/services/centro_desarrollo.py",
    "app/services/referencia_mi_retiro_seguro.py",
    "app/templates/dev_centro_desarrollo.html",
    "app/templates/partials/referencia_mi_retiro_seguro.html",
    "regulations/mixto.json",
    "regulations/sebd.json",
    "regulations/sucgs.json",
]


class TestMant1R5HAuditoriaNombresRestantes(unittest.TestCase):
    def test_destinos_tecnicos_normalizados_existen(self):
        for path in EXPECTED_PATHS:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file(), path)

    def test_excepciones_de_dominio_y_trazabilidad_se_conservan(self):
        for path in PRESERVED_PATHS:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).exists(), path)

    def test_auditoria_r5h_queda_documentada_e_indexada(self):
        audit = ROOT / "docs" / "AUDITORIA_NOMBRES_RESTANTES_R5H.md"
        index = ROOT / "docs" / "INDICE.md"

        self.assertTrue(audit.is_file())
        self.assertIn(
            "AUDITORIA_NOMBRES_RESTANTES_R5H.md",
            index.read_text(encoding="utf-8"),
        )

    def test_validacion_documenta_gate_r5h(self):
        validation = (ROOT / "docs" / "VALIDACION.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("MANT.1 R5H", validation)
        self.assertIn("924 passed", validation)
        self.assertIn("git diff --check: OK", validation)


if __name__ == "__main__":
    unittest.main()
