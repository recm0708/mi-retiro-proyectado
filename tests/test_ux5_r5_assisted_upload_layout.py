"""Contratos visuales del centro documental UX.5 R5."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]

ASSISTED = (
    ROOT
    / "app/templates/partials/assisted_preparation.html"
)

MRS = (
    ROOT
    / "app/templates/partials/official_data_import.html"
)

FICHA = (
    ROOT
    / "app/templates/partials/ficha_digital_import.html"
)

STYLE = (
    ROOT
    / "app/static/css/style.css"
)


class TestUX5R5AssistedUploadLayout(
    unittest.TestCase
):

    def test_centro_asistido_contiene_ambas_fuentes(self):
        text = ASSISTED.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'partials/official_data_import.html',
            text,
        )

        self.assertIn(
            'partials/ficha_digital_import.html',
            text,
        )

        self.assertIn(
            'id="assisted-mrs-status"',
            text,
        )

        self.assertIn(
            'id="assisted-ficha-status"',
            text,
        )


    def test_mi_retiro_seguro_no_nace_oculto(self):
        text = MRS.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'id="seccion-importacion-comprobante"',
            text,
        )

        root = text.split(
            "\n",
            5,
        )[4]

        self.assertNotIn(
            "d-none",
            root,
        )


    def test_ficha_no_conserva_margenes_del_paso_3(self):
        text = FICHA.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'id="seccion-importacion-ficha" '
            'class="official-import-section"',
            text,
        )

        first = text.splitlines()[3]

        self.assertNotIn(
            "mt-4",
            first,
        )

        self.assertNotIn(
            "mb-4",
            first,
        )


    def test_importadores_embebidos_no_anidan_otra_tarjeta_visual(self):
        css = STYLE.read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "Centro documental Asistido — importadores embebidos",
            css,
        )

        self.assertIn(
            ".assisted-source-card .official-import-card",
            css,
        )

        self.assertIn(
            "grid-template-columns: minmax(0, 1fr);",
            css,
        )

    def test_mrs_no_tiene_segundo_propietario_de_visibilidad(self):
        html = MRS.read_text(
            encoding="utf-8"
        )

        js = (
            ROOT
            / "app/static/js/official_data_import.js"
        ).read_text(
            encoding="utf-8"
        )

        design = (
            ROOT
            / "app/static/css/design-system.css"
        ).read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'id="seccion-importacion-comprobante"',
            html,
        )

        self.assertNotIn(
            "personal-import-panel",
            html,
        )

        self.assertNotIn(
            "seccion-importacion-comprobante",
            js,
        )

        self.assertNotIn(
            ".personal-import-panel",
            design,
        )


if __name__ == "__main__":
    unittest.main()
