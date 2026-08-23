"""Pruebas de identidad, terminología y contenido visible de la interfaz."""

import unittest

from fastapi.testclient import TestClient

from app.core.config import APP_NAME
from app.main import app


class TestIdentidadInterfaz(unittest.TestCase):
    """Evita regresiones de marca y exposición de etiquetas internas."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(app)

    def test_nombre_publico_se_centraliza_en_configuracion(self):
        self.assertEqual(APP_NAME, "Mi Retiro Proyectado")
        self.assertEqual(app.title, APP_NAME)

    def test_paginas_principales_no_exponen_nombre_anterior_ni_subfases(self):
        for ruta in ["/", "/simulacion", "/comparar", "/metodologia"]:
            with self.subTest(ruta=ruta):
                respuesta = self.cliente.get(ruta)
                self.assertEqual(respuesta.status_code, 200)
                self.assertIn(APP_NAME, respuesta.text)
                self.assertNotIn("Calculadora de Pensión CSS", respuesta.text)
                self.assertNotIn("Paso 6F.", respuesta.text)
                self.assertNotIn("Metodología 6F.", respuesta.text)
                self.assertNotIn("Cierre funcional 6F.", respuesta.text)

    def test_metodologia_usa_terminologia_publica_y_no_rutas_tecnicas(self):
        respuesta = self.cliente.get("/metodologia")

        self.assertIn("Asegurados(as)", respuesta.text)
        self.assertIn("Herramienta independiente de la CSS", respuesta.text)
        self.assertNotIn("Estimador independiente", respuesta.text)
        self.assertNotIn("Documentación técnica del proyecto", respuesta.text)
        self.assertNotIn("docs/FUENTES_NORMATIVAS.md", respuesta.text)
        self.assertNotIn("regulations/*.json", respuesta.text)

    def test_footer_identifica_independencia_sin_duplicar_mi_caja_digital(self):
        respuesta = self.cliente.get("/")

        self.assertIn("Todos los derechos reservados", respuesta.text)
        self.assertIn("Herramienta independiente de estimación previsional", respuesta.text)
        self.assertIn("No sustituye la determinación oficial", respuesta.text)
        self.assertIn("Fuentes oficiales", respuesta.text)
        self.assertNotIn("Abrir Mi Caja Digital", respuesta.text)


if __name__ == "__main__":
    unittest.main()
