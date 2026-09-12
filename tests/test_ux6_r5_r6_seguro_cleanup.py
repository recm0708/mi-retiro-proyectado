"""Regresiones de importación oficial segura y limpieza técnica."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestSeguroCleanup(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.official = (
            ROOT / "app/templates/asegurado/partials/official_data_import.html"
        ).read_text(encoding="utf-8")
        cls.ficha = (
            ROOT / "app/templates/asegurado/partials/ficha_digital_import.html"
        ).read_text(encoding="utf-8")
        cls.import_js = (
            ROOT / "app/static/js/official_data_import.js"
        ).read_text(encoding="utf-8")
        cls.reference_service = (
            ROOT / "app/services/mi_retiro_seguro_reference.py"
        ).read_text(encoding="utf-8")
        cls.style = (
            ROOT / "app/static/css/style.css"
        ).read_text(encoding="utf-8")
        cls.dev_css = (
            ROOT / "app/static/css/developer-portal.css"
        ).read_text(encoding="utf-8")
        cls.motion = (
            ROOT / "app/static/css/motion.css"
        ).read_text(encoding="utf-8")

    def test_ambos_documentos_explican_revision_y_confirmacion_sin_jerga_tecnica(self):
        for template in (
            self.official,
            self.ficha,
        ):
            with self.subTest():
                self.assertIn(
                    "vista previa",
                    template,
                )
                self.assertIn(
                    "Importar datos",
                    template,
                )
                self.assertIn(
                    'accept=".pdf,application/pdf"',
                    template,
                )
                self.assertIn(
                    "/metodologia#privacidad-datos",
                    template,
                )
                self.assertNotIn(
                    "archivo original no se guarda",
                    template,
                )

    def test_inputs_pdf_tienen_ayuda_y_controles_relacionados(self):
        self.assertIn(
            'aria-describedby="ayuda-import-comprobante-pdf"',
            self.official,
        )
        self.assertIn(
            'aria-describedby="ayuda-import-ficha-digital-pdf"',
            self.ficha,
        )
        self.assertIn(
            'aria-controls="estado-comprobante-importacion modal-import-comprobante"',
            self.official,
        )
        self.assertIn(
            "modal-vigencia-ficha-digital modal-import-ficha-digital",
            self.ficha,
        )

    def test_importacion_sigue_requiriendo_confirmacion_explicita(self):
        self.assertIn("btn-confirmar-import-comprobante", self.import_js)
        self.assertIn("confirmarComprobanteImportacion", self.import_js)
        self.assertIn("confirmarFichaDigitalImportacion", self.import_js)
        self.assertIn("borradorImportacionComprobante", self.import_js)
        self.assertIn("borradorImportacionFichaDigital", self.import_js)

    def test_servicio_mi_retiro_seguro_procesa_en_memoria(self):
        self.assertIn("BytesIO", self.reference_service)
        self.assertNotIn("write_bytes(", self.reference_service)
        self.assertNotIn("NamedTemporaryFile", self.reference_service)

    def test_motion_es_unico_propietario_de_entradas_generales(self):
        self.assertNotIn("aparecer-suave", self.style)
        self.assertNotIn("dev-page-enter", self.dev_css)
        self.assertIn("@keyframes app-surface-enter", self.motion)
        self.assertIn(".resultado-cuotas,", self.motion)
        self.assertIn(".dev-main > section", self.motion)

    def test_feedback_importacion_consume_movimiento_compartido(self):
        self.assertIn(
            ".official-import-status:not(.d-none)",
            self.motion,
        )
        self.assertIn(".dev-open-app", self.motion)
        self.assertIn(".dev-user-trigger", self.motion)


if __name__ == "__main__":
    unittest.main()
