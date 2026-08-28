"""Compatibilidad controlada de los importadores con la versión vigente de pypdf."""

from io import BytesIO
from pathlib import Path
import unittest

import pypdf
from pypdf import PdfReader, PdfWriter

from app.services.ficha_digital import analizar_ficha_digital_pdf
from app.services.mi_retiro_seguro_reference import analizar_comprobante_pdf


ROOT = Path(__file__).resolve().parents[1]


class TestPypdfCompatibilidad(unittest.TestCase):
    """Protege el contrato PDF usado por los dos importadores vigentes."""

    @staticmethod
    def _pdf_en_blanco(paginas: int = 1) -> bytes:
        escritor = PdfWriter()
        for _ in range(paginas):
            escritor.add_blank_page(width=612, height=792)
        salida = BytesIO()
        escritor.write(salida)
        return salida.getvalue()

    def test_version_pypdf_instalada_coincide_con_pin_vigente(self):
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        pin = next(
            (
                linea.split("==", 1)[1].strip()
                for linea in requirements.splitlines()
                if linea.strip().casefold().startswith("pypdf==")
            ),
            None,
        )
        self.assertIsNotNone(pin, "requirements.txt debe fijar pypdf")
        self.assertEqual(pin, pypdf.__version__)

    def test_roundtrip_pdfreader_pdfwriter_sigue_operativo(self):
        contenido = self._pdf_en_blanco()
        lector = PdfReader(BytesIO(contenido))

        self.assertEqual(1, len(lector.pages))
        self.assertEqual("", lector.pages[0].extract_text() or "")

    def test_ambos_importadores_rechazan_pdf_digital_sin_texto_de_forma_controlada(self):
        contenido = self._pdf_en_blanco()

        for importador in (
            analizar_comprobante_pdf,
            analizar_ficha_digital_pdf,
        ):
            with self.subTest(importador=importador.__name__):
                with self.assertRaisesRegex(ValueError, "texto extraíble"):
                    importador(contenido)

    def test_limites_de_paginas_siguen_activos_con_pypdf_vigente(self):
        with self.assertRaisesRegex(ValueError, "más páginas"):
            analizar_comprobante_pdf(self._pdf_en_blanco(21))

        with self.assertRaisesRegex(ValueError, "demasiadas páginas"):
            analizar_ficha_digital_pdf(self._pdf_en_blanco(31))


if __name__ == "__main__":
    unittest.main()
