"""Regresiones UX.4.6e R3 para Web Storage y comentarios JavaScript."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "app" / "static" / "js"
DOCS = ROOT / "docs"


class TestUX46eAlmacenamientoComentariosJS(unittest.TestCase):
    """Protege el namespace local y el estándar documental de runtime."""

    def test_namespace_storage_es_mi_retiro_proyectado(self):
        esperadas = {
            "miRetiroProyectado.simulacion",
            "miRetiroProyectado.privacidadConsentimiento",
            "miRetiroProyectado.privacidadConsentimientoSesion",
            "miRetiroProyectado.tema",
        }
        contenido = "\n".join(
            p.read_text(encoding="utf-8")
            for p in JS.glob("*.js")
        )
        for clave in esperadas:
            with self.subTest(clave=clave):
                self.assertIn(clave, contenido)

    def test_claves_pre_beta_solo_aparecen_en_borrado_defensivo(self):
        archivos = {
            p.name: p.read_text(encoding="utf-8")
            for p in JS.glob("*.js")
        }
        for nombre, contenido in archivos.items():
            if nombre in {"gestion_datos.js", "privacidad.js"}:
                continue
            with self.subTest(nombre=nombre):
                self.assertNotIn("calculadoraPensionCSS.", contenido)
                self.assertNotIn("mi-retiro-proyectado-tema", contenido)

        gestion = archivos["gestion_datos.js"]
        privacidad = archivos["privacidad.js"]
        self.assertIn("CLAVES_GESTION_LEGACY_SESION", gestion)
        self.assertIn("CLAVES_GESTION_LEGACY_LOCAL", gestion)
        self.assertIn("CLAVES_PRIVACIDAD_LEGACY_SESION", privacidad)
        self.assertNotIn("getItem(CLAVES_GESTION_LEGACY", gestion)
        self.assertNotIn("setItem(CLAVES_GESTION_LEGACY", gestion)
        self.assertNotIn("getItem(CLAVES_PRIVACIDAD_LEGACY", privacidad)
        self.assertNotIn("setItem(CLAVES_PRIVACIDAD_LEGACY", privacidad)

    def test_tema_y_borrado_integral_comparten_clave(self):
        tema = (JS / "tema.js").read_text(encoding="utf-8")
        gestion = (JS / "gestion_datos.js").read_text(encoding="utf-8")
        self.assertIn('const STORAGE_KEY = "miRetiroProyectado.tema";', tema)
        self.assertIn('const CLAVE_GESTION_TEMA = "miRetiroProyectado.tema";', gestion)

    def test_simulacion_comparador_privacidad_y_gestion_comparten_namespace(self):
        archivos = {
            nombre: (JS / nombre).read_text(encoding="utf-8")
            for nombre in (
                "simulacion.js",
                "comparador.js",
                "privacidad.js",
                "gestion_datos.js",
            )
        }
        for nombre, contenido in archivos.items():
            with self.subTest(nombre=nombre):
                self.assertIn("miRetiroProyectado.", contenido)
        self.assertIn("miRetiroProyectado.simulacion", archivos["simulacion.js"])
        self.assertIn("miRetiroProyectado.simulacion", archivos["comparador.js"])
        self.assertIn("miRetiroProyectado.simulacion", archivos["privacidad.js"])
        self.assertIn("miRetiroProyectado.simulacion", archivos["gestion_datos.js"])

    def test_javascript_runtime_no_usa_identificadores_cronologicos_en_comentarios(self):
        patron = re.compile(r"(?:UX\.\d|GOV\.\d)")
        hallazgos = []
        for ruta in JS.glob("*.js"):
            for numero, linea in enumerate(
                ruta.read_text(encoding="utf-8").splitlines(),
                start=1,
            ):
                if patron.search(linea):
                    hallazgos.append(f"{ruta.name}:{numero}:{linea.strip()}")
        self.assertEqual([], hallazgos)

    def test_estandar_documental_define_patron_por_tecnologia(self):
        ruta = DOCS / "ESTANDAR_CODIGO_Y_COMENTARIOS.md"
        self.assertTrue(ruta.is_file())
        texto = ruta.read_text(encoding="utf-8")
        for esperado in (
            "## 3. Python",
            "## 4. JavaScript",
            "## 5. HTML / Jinja",
            "## 6. CSS",
            "## 7. Pruebas",
            "## 8. JSON y normativa",
            "## 9. YAML y configuración",
            "miRetiroProyectado.*",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_indice_y_contributing_enlazan_estandar(self):
        indice = (DOCS / "INDICE.md").read_text(encoding="utf-8")
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        self.assertIn("ESTANDAR_CODIGO_Y_COMENTARIOS.md", indice)
        self.assertIn("docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md", contributing)

    def test_adr161_documenta_ruptura_pre_beta_sin_fallback(self):
        decisiones = (DOCS / "DECISIONES.md").read_text(encoding="utf-8")
        gestion = (DOCS / "GESTION_DATOS_SIMULACION.md").read_text(encoding="utf-8")
        self.assertIn("## ADR-161 —", decisiones)
        self.assertIn("sin fallback ni migración", decisiones)
        self.assertIn("miRetiroProyectado.simulacion", gestion)
        self.assertIn("miRetiroProyectado.tema", gestion)
        self.assertIn("sin fallback ni migración", decisiones)
        self.assertIn("identificadores pre-beta conocidos", gestion)
        self.assertIn("no se leen, restauran ni migran", gestion)


if __name__ == "__main__":
    unittest.main()
