"""Regresión MANT.1 R5H para nombres técnicos restantes."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


EXPECTED_PATHS = [
    "app/portals/asegurado/pdf_files.py",
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
    "app/static/shared/css/accessibility.css",
    "app/static/asegurado/css/results.css",
    "app/static/shared/js/accessibility.js",
    "app/static/asegurado/js/attachment_processing.js",
    "app/static/asegurado/js/comparator.js",
    "app/static/asegurado/js/currency.js",
    "app/static/asegurado/js/data_management.js",
    "app/static/asegurado/js/official_data_import.js",
    "app/static/asegurado/js/privacy.js",
    "app/static/asegurado/js/results.js",
    "app/static/asegurado/js/results_orchestration.js",
    "app/static/asegurado/js/retirement.js",
    "app/static/asegurado/js/salary_history.js",
    "app/static/asegurado/js/simulation.js",
    "app/static/asegurado/js/timeline.js",
    "app/static/asegurado/js/wizard_navigation.js",
    "app/templates/asegurado/partials/data_management.html",
    "app/templates/asegurado/partials/official_data_import.html",
    "app/templates/asegurado/partials/privacy_consent.html",
    "app/templates/asegurado/partials/results.html",
    "app/templates/asegurado/partials/retirement.html",
    "app/templates/asegurado/partials/salary_history.html",
    "app/templates/asegurado/simulation.html",
    "tests/shared/test_accessibility_themes.py",
    "tests/shared/test_accessibility_ux4.py",
    "tests/domain/test_money.py",
    "tests/domain/test_timeline.py",
    "tests/domain/test_unified_result.py",
    "tests/shared/test_visual_identity_pre_r8.py",
    "tests/shared/test_visual_stabilization.py",
]


PRESERVED_PATHS = [
    "app/core/normativa.py",
    "app/portals/developer/development_center.py",
    "app/services/mi_retiro_seguro_reference.py",
    "app/templates/developer/dev_development_center.html",
    "app/templates/asegurado/partials/mi_retiro_seguro_reference.html",
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
        audit = ROOT / "docs" / "archive/technical/remaining-names-audit-r5h.md"
        index = ROOT / "docs" / "README.md"

        self.assertTrue(audit.is_file())
        self.assertIn(
            "archive/technical/remaining-names-audit-r5h.md",
            index.read_text(encoding="utf-8"),
        )

    def test_validacion_documenta_gate_r5h(self):
        validation = (ROOT / "docs" / "operations/validation.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("MANT.1 R5H", validation)
        self.assertIn("924 passed", validation)
        self.assertIn("git diff --check: OK", validation)


if __name__ == "__main__":
    unittest.main()
