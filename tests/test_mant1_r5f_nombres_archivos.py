"""Valida la normalización de nombres de archivos técnicos en MANT.1 R5F."""

from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TestMant1R5FNombresArchivos(unittest.TestCase):
    def test_archivos_antiguos_no_existen(self):
        antiguos = (
            "scripts/configurar_hooks_git.ps1",
            "scripts/validar_precommit.py",
            "data/ledger_revisiones_pre_1_0.json",
            "regulations/parametros_generales.json",
            "tests/test_comparador.py",
            "tests/test_fuentes_normativas.py",
            "tests/test_proyeccion_salarios.py",
            "tests/test_resultados.py",
            "tests/test_resultados_mixto.py",
            "tests/test_resultados_modalidades.py",
            "tests/test_resultados_sucgs.py",
            "tests/test_retiro.py",
            "tests/test_trazabilidad.py",
        )

        for ruta_relativa in antiguos:
            with self.subTest(ruta=ruta_relativa):
                self.assertFalse(
                    (ROOT / ruta_relativa).exists(),
                    f"No debe quedar archivo antiguo: {ruta_relativa}",
                )

    def test_archivos_nuevos_existen(self):
        nuevos = (
            "scripts/configure_git_hooks.ps1",
            "scripts/validate_precommit.py",
            "data/revision_ledger_pre_1_0.json",
            "regulations/general-parameters.json",
            "tests/test_comparator.py",
            "tests/test_regulatory_sources.py",
            "tests/test_salary_projection.py",
            "tests/test_results.py",
            "tests/test_mixto_results.py",
            "tests/test_modality_results.py",
            "tests/test_sucgs_results.py",
            "tests/test_retirement.py",
            "tests/test_traceability.py",
        )

        for ruta_relativa in nuevos:
            with self.subTest(ruta=ruta_relativa):
                self.assertTrue(
                    (ROOT / ruta_relativa).is_file(),
                    f"Debe existir el archivo nuevo: {ruta_relativa}",
                )

    def test_referencias_obsoletas_no_quedan_fuera_de_entregas(self):
        obsoletas = (
            "scripts/configurar_hooks_git.ps1",
            "scripts/validar_precommit.py",
            "data/ledger_revisiones_pre_1_0.json",
            "regulations/parametros_generales.json",
            "test_comparador.py",
            "test_fuentes_normativas.py",
            "test_proyeccion_salarios.py",
            "test_resultados.py",
            "test_resultados_mixto.py",
            "test_resultados_modalidades.py",
            "test_resultados_sucgs.py",
            "test_retiro.py",
            "test_trazabilidad.py",
        )

        extensiones = {".py", ".ps1", ".md", ".txt", ".yml", ".yaml", ".json", ".githook"}
        excluir = {
            "docs/archive/technical/AUDITORIA_ARCHIVOS_R5F.md",
            "tests/test_mant1_r5f_nombres_archivos.py",
        }

        resultado = subprocess.run(
            ["git", "ls-files"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

        for relativa in resultado.stdout.splitlines():
            if relativa.startswith("_entregas/"):
                continue

            if relativa in excluir:
                continue

            ruta = ROOT / relativa

            if not ruta.is_file():
                continue

            if ruta.suffix.lower() not in extensiones and ruta.name != "pre-commit":
                continue

            try:
                contenido = ruta.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            for referencia in obsoletas:
                with self.subTest(archivo=relativa, referencia=referencia):
                    self.assertNotIn(
                        referencia,
                        contenido,
                        f"Referencia obsoleta encontrada en {relativa}: {referencia}",
                    )

    def test_exclusiones_de_dominio_se_conservan(self):
        conservados = (
            "regulations/mixto.json",
            "regulations/sebd.json",
            "regulations/sucgs.json",
        )

        for ruta_relativa in conservados:
            with self.subTest(ruta=ruta_relativa):
                self.assertTrue(
                    (ROOT / ruta_relativa).is_file(),
                    f"Debe conservarse el nombre de dominio: {ruta_relativa}",
                )


if __name__ == "__main__":
    unittest.main()
