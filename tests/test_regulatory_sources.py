"""Pruebas de la página transversal de metodología y fuentes."""

import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.services.regulatory_sources import construir_catalogo_metodologia


class TestFuentesNormativas(unittest.TestCase):
    """Valida catálogo, enlaces oficiales y renderizado de la página."""

    def test_catalogo_incluye_los_tres_sistemas(self):
        catalogo = construir_catalogo_metodologia()
        ids = [grupo["id"] for grupo in catalogo["grupos"]]

        self.assertEqual(ids, ["sebd", "mixto", "sucgs"])
        self.assertEqual(catalogo["version"], "1.0")

    def test_fuentes_tienen_etiquetas_humanas_y_https(self):
        catalogo = construir_catalogo_metodologia()
        fuentes = list(catalogo["fuentes_generales"])
        for grupo in catalogo["grupos"]:
            fuentes.extend(grupo["fuentes"])

        self.assertTrue(fuentes)
        self.assertTrue(all("_" not in fuente["titulo"] for fuente in fuentes))
        self.assertTrue(all(fuente["url"].startswith("https://") for fuente in fuentes))
        self.assertTrue(any("Ley 462" in fuente["titulo"] for fuente in fuentes))

    def test_pagina_metodologia_responde_y_muestra_fuentes(self):
        cliente = TestClient(app)
        respuesta = cliente.get("/metodologia")

        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("Metodología y fuentes oficiales", respuesta.text)
        self.assertIn("Texto Único de la Ley 51 de 2005", respuesta.text)
        self.assertIn("Resolución 57,805-2025-J.D.", respuesta.text)
        self.assertIn("Mi Caja Digital", respuesta.text)
        self.assertNotIn("Mi Retiro Seguro — CSS", respuesta.text)
        catalogo = construir_catalogo_metodologia()
        self.assertEqual(len(catalogo["recursos"]), 2)


if __name__ == "__main__":
    unittest.main()
