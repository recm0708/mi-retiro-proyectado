"""MANT.1 R5E — regresión de nombres de carpetas técnicas."""

from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestMant1R5ENombresCarpetas(unittest.TestCase):
    """Protege que las carpetas técnicas queden en inglés y referenciadas."""

    def test_carpetas_vigentes_existen(self):
        esperadas = (
            "app/models",
            "app/engines",
            "app/services",
            "regulations",
            "tests/validation_cases",
            "docs/archive",
            "docs/archive/governance",
            "docs/archive/regulatory-privacy",
            "docs/archive/technical",
            "docs/archive/ux",
        )

        for ruta_relativa in esperadas:
            with self.subTest(ruta=ruta_relativa):
                self.assertTrue(
                    (ROOT / ruta_relativa).is_dir(),
                    f"Falta carpeta vigente: {ruta_relativa}",
                )

    def test_carpetas_tecnicas_antiguas_no_existen(self):
        antiguas = (
            "app/modelos",
            "app/motores",
            "app/servicios",
            "normativa",
            "tests/casos_validacion",
            "docs/historico",
        )

        for ruta_relativa in antiguas:
            with self.subTest(ruta=ruta_relativa):
                self.assertFalse(
                    (ROOT / ruta_relativa).exists(),
                    f"No debe quedar carpeta antigua: {ruta_relativa}",
                )

    def test_referencias_tecnicas_antiguas_no_quedan_en_texto(self):
        patrones_antiguos = (
            "app/modelos",
            "app\\modelos",
            "app.modelos",
            "app/motores",
            "app\\motores",
            "app.motores",
            "app/servicios",
            "app\\servicios",
            "app.servicios",
            "docs/historico",
            "docs\\historico",
            "tests/casos_validacion",
            "tests\\casos_validacion",
            "casos_validacion",
            "normativa/*.json",
            "normativa/general-parameters.json",
            "normativa/sebd.json",
            "normativa/mixto.json",
            "normativa/sucgs.json",
            "/normativa/ @recm0708",
        )

        hallazgos: list[str] = []

        for ruta in ROOT.rglob("*"):
            if not ruta.is_file():
                continue

            relativa = ruta.relative_to(ROOT).as_posix()

            if (
                relativa.startswith(".git/")
                or relativa.startswith(".venv/")
                or relativa.startswith("_entregas/")
                or relativa.startswith("_deliverables/")
                or "__pycache__/" in relativa
                or relativa in {
                    "docs/archive/technical/AUDITORIA_CARPETAS_R5E.md",
                    "tests/test_mant1_r5e_nombres_carpetas.py",
                }
                or relativa.endswith((".png", ".ico", ".pdf", ".zip"))
            ):
                continue

            try:
                texto = ruta.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            for patron in patrones_antiguos:
                if patron in texto:
                    hallazgos.append(f"{relativa}: {patron}")

        self.assertEqual([], hallazgos)

    def test_documentacion_de_auditoria_declara_alcance_y_exclusiones(self):
        auditoria = ROOT / "docs" / "archive/technical/AUDITORIA_CARPETAS_R5E.md"
        politica = ROOT / "docs" / "standards/file-structure-by-extension.md"
        indice = ROOT / "docs" / "README.md"

        for ruta in (auditoria, politica, indice):
            with self.subTest(ruta=ruta.as_posix()):
                self.assertTrue(ruta.exists())

        texto = auditoria.read_text(encoding="utf-8")
        self.assertIn("app/models/", texto)
        self.assertIn("app/engines/", texto)
        self.assertIn("app/services/", texto)
        self.assertIn("regulations/", texto)
        self.assertIn("docs/archive/", texto)
        self.assertIn("_entregas/", texto)
        self.assertIn("No se renombran archivos", texto)

        self.assertIn(
            "archive/technical/AUDITORIA_CARPETAS_R5E.md",
            indice.read_text(encoding="utf-8"),
        )
        self.assertIn(
            "nombres de carpetas",
            politica.read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
