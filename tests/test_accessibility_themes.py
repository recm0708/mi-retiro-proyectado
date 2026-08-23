"""Pruebas de temas visuales, accesibilidad básica y pie de página."""

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


ROOT = Path(__file__).resolve().parents[1]


class TestAccesibilidadTemas(unittest.TestCase):
    """Protege las decisiones visibles de temas y navegación global."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(app)

    def test_menu_de_apariencia_conserva_cuatro_modos(self):
        respuesta = self.cliente.get("/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('id="menu-apariencia"', respuesta.text)
        self.assertIn('data-theme-choice="system"', respuesta.text)
        self.assertIn('data-theme-choice="light"', respuesta.text)
        self.assertIn('data-theme-choice="dark"', respuesta.text)
        self.assertIn('data-theme-choice="contrast"', respuesta.text)
        self.assertIn("Accesibilidad", respuesta.text)
        self.assertIn('/static/js/tema.js', respuesta.text)

    def test_navegacion_incluye_salto_al_contenido_y_aria_current(self):
        respuesta = self.cliente.get("/metodologia")

        self.assertIn('class="skip-link"', respuesta.text)
        self.assertIn('href="#contenido-principal"', respuesta.text)
        self.assertIn('id="contenido-principal"', respuesta.text)
        self.assertIn('aria-current="page"', respuesta.text)

    def test_footer_es_compacto_y_mantiene_aviso_legal(self):
        respuesta = self.cliente.get("/")

        self.assertIn('class="container footer-modern"', respuesta.text)
        self.assertIn("Mi Retiro Proyectado", respuesta.text)
        self.assertIn("Todos los derechos reservados", respuesta.text)
        self.assertIn("Herramienta independiente de estimación previsional", respuesta.text)
        self.assertIn("No sustituye la determinación oficial", respuesta.text)
        self.assertIn("Fuentes oficiales", respuesta.text)
        self.assertIn("Ayuda y contacto", respuesta.text)
        self.assertIn('href="/metodologia#ayuda-contacto"', respuesta.text)
        self.assertNotIn("Abrir Mi Caja Digital", respuesta.text)

    def test_tema_persiste_en_localstorage_y_sigue_preferencia_del_sistema(self):
        contenido = (ROOT / "app/static/js/tema.js").read_text(encoding="utf-8")

        self.assertIn("miRetiroProyectado.tema", contenido)
        self.assertIn("localStorage", contenido)
        self.assertIn("prefers-color-scheme: dark", contenido)
        self.assertIn('data-bs-theme', contenido)
        self.assertIn('data-app-theme', contenido)
        self.assertIn("data-theme-choice", contenido)

    def test_css_incluye_foco_movimiento_reducido_y_objetivos_tactiles(self):
        contenido = (ROOT / "app/static/css/style.css").read_text(encoding="utf-8")

        self.assertIn(":focus-visible", contenido)
        self.assertIn("prefers-reduced-motion: reduce", contenido)
        self.assertIn("min-height: 44px", contenido)
        self.assertIn('html[data-bs-theme="dark"]', contenido)
        self.assertIn('html[data-app-theme="contrast"]', contenido)


if __name__ == "__main__":
    unittest.main()
