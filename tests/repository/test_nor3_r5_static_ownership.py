"""Contrato NOR.3 R5: ownership físico de assets estáticos."""

from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "app" / "static"

CSS_SHARED = {"accessibility.css", "brand.css", "design-system.css", "motion.css"}
CSS_ASEGURADO = {"style.css", "calculation-guide.css", "editable-provenance.css", "results.css"}
CSS_DEVELOPER = {"developer-portal.css"}
JS_SHARED = {"accessibility.js", "datetime_ui.js", "interaction_ui.js", "shell_state_boot.js", "shell_ui.js", "theme.js"}
JS_DEVELOPER = {"developer_forms.js", "developer_portal.js"}
JS_ASEGURADO = {
    "app_shell.js", "assisted_flow.js", "attachment_processing.js", "comparator.js",
    "currency.js", "current_year_detail.js", "data_management.js", "editable_provenance.js",
    "mi_retiro_seguro_reference.js", "official_data_import.js", "privacy.js", "results.js",
    "results_orchestration.js", "retirement.js", "salary_history.js", "simulation.js",
    "simulation_mode.js", "timeline.js", "wizard_navigation.js",
}
BRAND = {
    "app-icon-192.png", "app-icon-512.png", "apple-touch-icon.png",
    "favicon-16x16.png", "favicon-32x32.png", "favicon-48x48.png",
    "favicon.ico", "logo-mark-128.png",
}

class TestNOR3R5StaticOwnership(unittest.TestCase):
    def test_css_por_owner_es_exacto(self):
        self.assertEqual(CSS_SHARED, {p.name for p in (STATIC / "shared" / "css").glob("*.css")})
        self.assertEqual(CSS_ASEGURADO, {p.name for p in (STATIC / "asegurado" / "css").glob("*.css")})
        self.assertEqual(CSS_DEVELOPER, {p.name for p in (STATIC / "developer" / "css").glob("*.css")})

    def test_js_por_owner_es_exacto(self):
        self.assertEqual(JS_SHARED, {p.name for p in (STATIC / "shared" / "js").glob("*.js")})
        self.assertEqual(JS_ASEGURADO, {p.name for p in (STATIC / "asegurado" / "js").glob("*.js")})
        self.assertEqual(JS_DEVELOPER, {p.name for p in (STATIC / "developer" / "js").glob("*.js")})

    def test_brand_shared_es_exacto(self):
        self.assertEqual(BRAND, {p.name for p in (STATIC / "shared" / "img" / "brand").iterdir() if p.is_file()})
        self.assertFalse((STATIC / "shared" / "img" / "favicon.svg").exists())

    def test_raices_legacy_desaparecen(self):
        for name in ("css", "js", "img"):
            self.assertFalse((STATIC / name).exists())

    def test_shells_declaran_ownership_correcto(self):
        asegurado = (ROOT / "app" / "templates" / "asegurado" / "base.html").read_text(encoding="utf-8")
        developer = (ROOT / "app" / "templates" / "developer" / "dev_base.html").read_text(encoding="utf-8")
        self.assertIn("/asegurado/css/style.css", asegurado)
        self.assertNotIn("/asegurado/css/style.css", developer)
        self.assertIn("/developer/css/developer-portal.css", developer)
        for shared in (
            "/shared/css/design-system.css", "/shared/css/accessibility.css",
            "/shared/css/brand.css", "/shared/css/motion.css",
            "/shared/js/theme.js", "/shared/js/shell_state_boot.js",
        ):
            self.assertIn(shared, asegurado)
            self.assertIn(shared, developer)

    def test_style_es_asegurado_y_design_system_es_shared(self):
        style = (STATIC / "asegurado" / "css" / "style.css").read_text(encoding="utf-8")
        design = (STATIC / "shared" / "css" / "design-system.css").read_text(encoding="utf-8")
        self.assertIn("Estilos funcionales de App Asegurado", style)
        self.assertIn(".hero-section {", style)
        self.assertNotIn("font-family: var(--app-font-family);", style)
        self.assertIn("font-family: var(--app-font-family);", design)
        self.assertIn("body {", design)
        self.assertIn(".footer {", design)
        self.assertIn(".form-control,", design)

    def test_policy_activa_namespaces_static(self):
        policy = json.loads((ROOT / "data" / "governance" / "repository-structure-policy.json").read_text(encoding="utf-8"))
        ownership = policy["future_ownership_contract"]
        self.assertTrue(ownership["enforced"])
        self.assertEqual("NOR.3 R5", ownership["activated_in"])
        self.assertEqual(
            {"shared": "app/static/shared", "asegurado": "app/static/asegurado", "developer": "app/static/developer"},
            ownership["static_namespaces"],
        )

if __name__ == "__main__":
    unittest.main()
