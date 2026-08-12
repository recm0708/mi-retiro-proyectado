"""Regresiones de UX.4.4 para mostrar edad por año en la línea temporal."""

import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


ROOT = Path(__file__).resolve().parents[1]


class TestUX44EdadLineaTiempo(unittest.TestCase):
    """Protege la columna Edad en historial real y proyección futura."""

    @classmethod
    def setUpClass(cls):
        cls.cliente = TestClient(app)
        cls.linea_tiempo = (ROOT / "app/static/js/linea_tiempo.js").read_text(
            encoding="utf-8"
        )
        cls.css = (ROOT / "app/static/css/style.css").read_text(encoding="utf-8")

    def test_linea_tiempo_define_calculo_de_edad_por_anio(self):
        self.assertIn("function obtenerEdadEnAnio(anio)", self.linea_tiempo)
        self.assertIn("simulacion.persona?.fecha_nacimiento", self.linea_tiempo)
        self.assertIn("return anioFila - anioNacimiento", self.linea_tiempo)

    def test_historial_real_incluye_columna_edad(self):
        bloque = self.linea_tiempo.split("function crearTablaHistorialLineaTiempo", 1)[1]
        bloque = bloque.split("function crearResumenAnioActual", 1)[0]
        self.assertIn('"Año",\n    "Edad",\n    "Cuotas"', bloque)
        self.assertIn("obtenerEdadEnAnio(registro.anio)", bloque)

    def test_proyeccion_futura_incluye_columna_edad(self):
        bloque = self.linea_tiempo.split("function crearTablaProyeccionLineaTiempo", 1)[1]
        bloque = bloque.split("function mostrarProyeccionConHistorialLimitado", 1)[0]
        self.assertIn('"Año",\n    "Edad",\n    "Cuotas proyectadas"', bloque)
        self.assertIn("obtenerEdadEnAnio(registro.anio)", bloque)

    def test_tabla_temporal_conserva_ancho_legible_y_simulacion_responde(self):
        self.assertIn(".timeline-table {\n  min-width: 900px;", self.css)
        respuesta = self.cliente.get("/simulacion")
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn("linea_tiempo.js", respuesta.text)


if __name__ == "__main__":
    unittest.main()
