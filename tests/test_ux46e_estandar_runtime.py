"""Regresiones de comentarios permanentes y cobertura documental del runtime."""

from __future__ import annotations

import ast
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
TESTS = ROOT / "tests"
DOCS = ROOT / "docs"
FASE_RE = re.compile(r"\b(?:UX|GOV)\.\d", re.IGNORECASE)


class TestUX46eEstandarRuntime(unittest.TestCase):
    """Protege el patrón de comentarios/docstrings adoptado para mantenimiento."""

    def test_python_runtime_no_conserva_identificadores_cronologicos(self):
        for ruta in APP.rglob("*.py"):
            with self.subTest(ruta=ruta.relative_to(ROOT)):
                texto = ruta.read_text(encoding="utf-8")
                self.assertIsNone(FASE_RE.search(texto))

    def test_todas_las_funciones_y_clases_de_app_tienen_docstring(self):
        faltantes = []
        for ruta in APP.rglob("*.py"):
            arbol = ast.parse(ruta.read_text(encoding="utf-8"))
            for nodo in ast.walk(arbol):
                if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if ast.get_docstring(nodo) is None:
                        faltantes.append(
                            f"{ruta.relative_to(ROOT)}:{nodo.lineno}:{nodo.name}"
                        )
        self.assertEqual([], faltantes)

    def test_todos_los_modulos_de_pruebas_tienen_docstring(self):
        faltantes = []
        for ruta in TESTS.glob("test_*.py"):
            arbol = ast.parse(ruta.read_text(encoding="utf-8"))
            if ast.get_docstring(arbol) is None:
                faltantes.append(str(ruta.relative_to(ROOT)))
        self.assertEqual([], faltantes)

    def test_jinja_vigente_no_conserva_identificadores_cronologicos(self):
        for ruta in (APP / "templates").rglob("*.html"):
            with self.subTest(ruta=ruta.relative_to(ROOT)):
                self.assertIsNone(FASE_RE.search(ruta.read_text(encoding="utf-8")))

    def test_css_vigente_no_conserva_identificadores_cronologicos(self):
        for ruta in (APP / "static" / "css").glob("*.css"):
            with self.subTest(ruta=ruta.relative_to(ROOT)):
                self.assertIsNone(FASE_RE.search(ruta.read_text(encoding="utf-8")))

    def test_estandar_separa_historia_de_documentacion_permanente(self):
        texto = (DOCS / "standards/code-and-comments.md").read_text(encoding="utf-8")
        self.assertIn("Historia frente a documentación permanente", texto)
        self.assertIn("El código de runtime usa comentarios semánticos", texto)
        self.assertIn("La revisión transversal actual deja documentadas todas", texto)

    def test_adr162_registra_decision_sin_reescribir_historia(self):
        texto = (DOCS / "decisions/README.md").read_text(encoding="utf-8")
        self.assertIn("## ADR-162 — Los comentarios de runtime son semánticos", texto)
        self.assertRegex(texto, r"las pruebas pueden\s+conservar identificadores históricos")
        ids = [int(x) for x in re.findall(r"(?m)^## ADR-(\d{3})\s+—", texto)]
        self.assertEqual(list(range(1, max(ids) + 1)), ids)
        self.assertGreaterEqual(max(ids), 162)
        self.assertIn(
            f"**ADR indexadas:** {max(ids)} (`ADR-001` a `ADR-{max(ids):03d}`)",
            texto,
        )

    def test_r4_preserva_0_0_24_como_evidencia_del_checkpoint(self):
        texto = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn(
            "iniciada R4 de normalización permanente del runtime",
            texto,
        )
        self.assertIn(
            "`VERSION` permanece en `0.0.24-beta` hasta el cierre integral de UX.4.6e",
            texto,
        )


if __name__ == "__main__":
    unittest.main()
