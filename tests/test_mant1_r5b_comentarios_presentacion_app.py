"""Regresiones para comentarios funcionales en CSS y plantillas de aplicación."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "app" / "static" / "css" / "calculation-guide.css"
TEMPLATE = ROOT / "app" / "templates" / "calculation_guide.html"
DOCS = (
    ROOT / "CHANGELOG.md",
    ROOT / "docs" / "standards/code-and-comments.md",
    ROOT / "docs" / "operations/validation.md",
    ROOT / "docs" / "architecture/system-architecture.md",
    ROOT / "docs" / "governance/roadmap.md",
)


class TestMant1R5BComentariosPresentacionApp(unittest.TestCase):
    """Protege comentarios estructurales sin convertirlos en trazabilidad histórica."""

    def test_css_declara_responsabilidades_visuales_principales(self):
        texto = CSS.read_text(encoding="utf-8")
        esperados = (
            "Página pública de guía de cálculo",
            "Hero y estado normativo",
            "Navegación interna",
            "Contenedores de sección",
            "Tarjetas de flujo",
            "Fórmulas y ejemplos",
            "Variantes de accesibilidad",
            "Responsive intermedio",
            "Glosarios locales",
        )
        for esperado in esperados:
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_plantilla_declara_bloques_funcionales_sin_texto_visible_extra(self):
        texto = TEMPLATE.read_text(encoding="utf-8")
        esperados = (
            "La guía es informativa",
            "Navegación interna",
            "Recorrido general",
            "Bloque SEBD",
            "Bloque Mixto",
            "Bloque SUCGS",
            "Cierre de la guía",
        )
        for esperado in esperados:
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

        self.assertNotIn("<!--", texto)
        self.assertIn("{#", texto)

    def test_comentarios_de_presentacion_no_registran_trazabilidad_historica(self):
        patron_prohibido = re.compile(r"MANT\.\s*1|DEV\.2|UX\.4\.6|VER\.2|PR\s*#|pull request", re.IGNORECASE)
        for ruta in (CSS, TEMPLATE):
            texto = ruta.read_text(encoding="utf-8")
            comentarios = []
            if ruta.suffix == ".css":
                comentarios = re.findall(r"/\*.*?\*/", texto, flags=re.DOTALL)
            else:
                comentarios = re.findall(r"\{#.*?#\}", texto, flags=re.DOTALL)
            with self.subTest(ruta=ruta.as_posix()):
                self.assertGreaterEqual(len(comentarios), 5)
                self.assertFalse(
                    any(patron_prohibido.search(comentario) for comentario in comentarios),
                    "Los comentarios de app deben describir intención permanente, no trazabilidad histórica.",
                )

    def test_documentacion_transversal_registra_r5b_y_alcance_excluido(self):
        for ruta in DOCS:
            texto = ruta.read_text(encoding="utf-8")
            with self.subTest(ruta=ruta.as_posix()):
                self.assertIn("MANT.1 R5B", texto)
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertIn("no cambia `VERSION`", changelog)
        self.assertIn("`APP_VERSION`", changelog)
        self.assertIn("motores previsionales", changelog)
        self.assertIn("regulations", changelog)
        self.assertIn("SEC.2", changelog)


if __name__ == "__main__":
    unittest.main()
