"""Regresiones del bloque unificado de información personal del Paso 1."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestUX46dRevision14Paso1InformacionPersonal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.simulacion = (ROOT / "app/templates/simulation.html").read_text(encoding="utf-8")
        cls.importacion_js = (ROOT / "app/static/js/official_data_import.js").read_text(encoding="utf-8")

    def test_paso_uno_unifica_identificacion_y_prevision_en_informacion_personal(self):
        panel = self.simulacion.split('data-panel="1"', 1)[1].split('data-panel="2"', 1)[0]
        self.assertIn('id="informacion-personal-titulo"', panel)
        self.assertIn('>Información personal</h3>', panel)
        self.assertNotIn('id="identificacion-personal-titulo"', panel)
        self.assertNotIn('id="informacion-previsional-titulo"', panel)
        self.assertNotIn('>Identificación personal</h3>', panel)
        self.assertNotIn('>Información previsional básica</h3>', panel)

    def test_sexo_esta_antes_del_apellido_de_casada_y_ambos_comparten_fila_logica(self):
        panel = self.simulacion.split('data-panel="1"', 1)[1].split('data-panel="2"', 1)[0]
        self.assertLess(panel.index('for="sexo"'), panel.index('id="apellido-casada-wrapper"'))
        zona = panel.split('for="sexo"', 1)[1].split('</div>\n\n                    <div class="row g-4 mb-1 mt-0">', 1)[0]
        self.assertIn('id="apellido-casada-wrapper" class="col-md-6 d-none"', zona)

    def test_apellido_de_casada_conserva_condicion_femenina_sin_cambiar_logica(self):
        self.assertIn('const mostrar = sexo === "F";', self.importacion_js)
        self.assertIn('document.getElementById("sexo")?.addEventListener("change", actualizarApellidoCasada);', self.importacion_js)
        self.assertIn('actualizarApellidoCasada();', self.importacion_js)


if __name__ == "__main__":
    unittest.main()
