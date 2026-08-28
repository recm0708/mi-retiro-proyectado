"""MANT.1 R5D — política, plantillas y uniformidad por extensión."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import unittest


RAIZ = Path(__file__).resolve().parents[1]
PLANTILLAS = RAIZ / "docs" / "templates" / "file-structure"


class TestMant1R5DPoliticaExtensiones(unittest.TestCase):
    """Protege política, plantillas y encabezados uniformes por extensión."""

    def test_documentacion_base_existe_y_declara_alcance(self):
        politica = RAIZ / "docs" / "standards/file-structure-by-extension.md"
        auditoria = RAIZ / "docs" / "archive/technical/file-structure-audit-r5d.md"
        estandar = RAIZ / "docs" / "standards/code-and-comments.md"

        for ruta in (politica, auditoria, estandar):
            with self.subTest(ruta=ruta.as_posix()):
                self.assertTrue(ruta.exists(), f"Falta documento: {ruta}")

        texto_politica = politica.read_text(encoding="utf-8")
        self.assertIn("Política por extensión", texto_politica)
        self.assertIn("docs/templates/file-structure/", texto_politica)
        self.assertIn("La trazabilidad de revisiones", texto_politica)

        for extension in (
            ".md",
            ".py",
            ".js",
            ".css",
            ".html",
            ".yml",
            ".json",
            ".ps1",
            ".githook",
            ".gitignore",
            ".gitattributes",
            ".editorconfig",
            ".png",
            ".ico",
        ):
            with self.subTest(extension=extension):
                self.assertIn(extension, texto_politica)

    def test_plantillas_oficiales_por_extension(self):
        esperadas = (
            "README.md",
            "template.md",
            "template.py",
            "template.js",
            "template.css",
            "template.html",
            "template.yml",
            "template.yaml",
            "template.json",
            "template.ps1",
            "template.githook",
            "template.txt",
            "template.gitignore",
            "template.gitattributes",
            "template.editorconfig",
            "template_without_extension",
            "template.png",
            "template.ico",
        )

        for nombre in esperadas:
            ruta = PLANTILLAS / nombre
            with self.subTest(nombre=nombre):
                self.assertTrue(ruta.exists(), f"Falta plantilla: {nombre}")
                self.assertGreater(ruta.stat().st_size, 0, f"Plantilla vacía: {nombre}")

        ast.parse((PLANTILLAS / "template.py").read_text(encoding="utf-8"))
        json.loads((PLANTILLAS / "template.json").read_text(encoding="utf-8"))

        for nombre in (
            "template.js",
            "template.css",
            "template.html",
            "template.yml",
            "template.ps1",
            "template.githook",
        ):
            with self.subTest(nombre=nombre):
                texto = (PLANTILLAS / nombre).read_text(encoding="utf-8")
                self.assertNotRegex(texto, r"\b(?:MANT\.1|DEV\.2|UX\.4\.6|PR\s*#)")
                self.assertIn("Propósito", texto)

    def test_encabezados_js_operativos_son_uniformes(self):
        patron_revision = re.compile(r"\b(?:MANT\.1|DEV\.2|UX\.4\.6|PR\s*#)")
        archivos = sorted((RAIZ / "app" / "static" / "js").glob("*.js"))

        self.assertGreaterEqual(len(archivos), 1)

        for ruta in archivos:
            texto = ruta.read_text(encoding="utf-8")
            primeras_lineas = "\n".join(texto.splitlines()[:12])
            with self.subTest(ruta=ruta.as_posix()):
                self.assertTrue(texto.startswith('"use strict";\n\n/*'))
                self.assertIn("Mi Retiro Proyectado —", primeras_lineas)
                self.assertIn("Propósito:", primeras_lineas)
                self.assertIn("Alcance:", primeras_lineas)
                self.assertNotRegex(primeras_lineas, patron_revision)

    def test_encabezados_css_operativos_son_uniformes(self):
        patron_revision = re.compile(r"\b(?:MANT\.1|DEV\.2|UX\.4\.6|PR\s*#)")
        archivos = sorted((RAIZ / "app" / "static" / "css").glob("*.css"))

        self.assertGreaterEqual(len(archivos), 1)

        for ruta in archivos:
            texto = ruta.read_text(encoding="utf-8")
            primeras_lineas = "\n".join(texto.splitlines()[:10])
            with self.subTest(ruta=ruta.as_posix()):
                self.assertTrue(texto.startswith("/*"))
                self.assertIn("Mi Retiro Proyectado —", primeras_lineas)
                self.assertIn("Propósito:", primeras_lineas)
                self.assertIn("Alcance:", primeras_lineas)
                self.assertNotRegex(primeras_lineas, patron_revision)


if __name__ == "__main__":
    unittest.main()
