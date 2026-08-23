"""Regresiones UX.4.6e R8 para borrado integral y reconsentimiento."""

from pathlib import Path
import json
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
JS = ROOT / "app" / "static" / "js"
DOCS = ROOT / "docs"


class TestUX46eR8ReconsentimientoBorrado(unittest.TestCase):
    """Protege el borrado local y la reapertura obligatoria de términos."""

    @classmethod
    def setUpClass(cls):
        cls.gestion = (JS / "data_management.js").read_text(encoding="utf-8")
        cls.privacidad = (JS / "privacy.js").read_text(encoding="utf-8")
        cls.terminos = (
            ROOT / "app/templates/partials/privacy_consent.html"
        ).read_text(encoding="utf-8")
        cls.decisiones = (DOCS / "DECISIONES.md").read_text(encoding="utf-8")

    def test_borrado_integral_fuerza_presentacion_desde_inicio(self):
        self.assertIn('window.location.replace("/?privacidad=1")', self.gestion)
        self.assertIn("debeForzarVistaPrivacidad()", self.privacidad)
        self.assertIn('esRutaSimulacion() ? "simulacion" : "inicio"', self.privacidad)

    def test_borrado_purga_namespace_vigente_y_residuos_pre_beta(self):
        for esperado in (
            "CLAVE_GESTION_SIMULACION",
            "CLAVE_GESTION_PRIVACIDAD",
            "CLAVE_GESTION_PRIVACIDAD_SESION",
            "CLAVE_GESTION_TEMA",
            "calculadoraPensionCSS.simulacion",
            "calculadoraPensionCSS.privacidadConsentimiento",
            "calculadoraPensionCSS.privacidadConsentimientoSesion",
            "mi-retiro-proyectado-tema",
        ):
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, self.gestion)
        self.assertNotIn("localStorage.clear", self.gestion)
        self.assertNotIn("sessionStorage.clear", self.gestion)

    def test_legacy_es_solo_destructivo_sin_fallback(self):
        self.assertNotIn('getItem("calculadoraPensionCSS', self.gestion)
        self.assertNotIn('setItem("calculadoraPensionCSS', self.gestion)
        self.assertNotIn('getItem("calculadoraPensionCSS', self.privacidad)
        self.assertNotIn('setItem("calculadoraPensionCSS', self.privacidad)
        self.assertIn("## ADR-166 —", self.decisiones)
        self.assertIn("no existe compatibilidad, fallback ni migración", self.decisiones)

    def test_texto_visible_explica_reconsentimiento(self):
        self.assertIn("Después del borrado vuelve a Inicio", self.terminos)
        self.assertIn("entras a Simular sin una aceptación vigente", self.terminos)
        self.assertIn("volverá a solicitarlas", self.terminos)

    def test_documentacion_tecnica_refleja_el_flujo(self):
        gestion_doc = (DOCS / "GESTION_DATOS_SIMULACION.md").read_text(encoding="utf-8")
        politica = (DOCS / "POLITICA_PRIVACIDAD.md").read_text(encoding="utf-8")
        especificacion = (DOCS / "ESPECIFICACION_FUNCIONAL.md").read_text(encoding="utf-8")
        seguridad = (DOCS / "SEGURIDAD_PRIVACIDAD.md").read_text(encoding="utf-8")
        self.assertIn("purga identificadores pre-beta", gestion_doc)
        self.assertIn("no se leen, restauran ni migran", gestion_doc)
        self.assertIn("vuelve a presentar las condiciones desde Inicio", politica)
        self.assertIn("nueva presentación de las condiciones", especificacion)
        self.assertIn("identificadores pre-beta conocidos exclusivamente para purgarlos", seguridad)

    def test_ejecucion_js_borra_claves_y_conserva_almacenamiento_ajeno(self):
        ruta = json.dumps(str(JS / "data_management.js"))
        script = rf'''
const fs = require("fs");
const vm = require("vm");
function storage(inicial) {{
  const datos = new Map(Object.entries(inicial));
  return {{
    getItem: (k) => datos.has(k) ? datos.get(k) : null,
    setItem: (k, v) => datos.set(k, String(v)),
    removeItem: (k) => datos.delete(k),
    has: (k) => datos.has(k),
  }};
}}
const sessionStorage = storage({{
  "miRetiroProyectado.simulacion": "actual",
  "miRetiroProyectado.privacidadConsentimientoSesion": "actual",
  "calculadoraPensionCSS.simulacion": "legacy",
  "calculadoraPensionCSS.privacidadConsentimientoSesion": "legacy",
  "otraAplicacion.sesion": "preservar",
}});
const localStorage = storage({{
  "miRetiroProyectado.privacidadConsentimiento": "actual",
  "miRetiroProyectado.tema": "dark",
  "calculadoraPensionCSS.privacidadConsentimiento": "legacy",
  "mi-retiro-proyectado-tema": "legacy",
  "otraAplicacion.local": "preservar",
}});
let destino = null;
const context = {{
  console,
  window: {{
    sessionStorage,
    localStorage,
    location: {{ replace: (url) => {{ destino = url; }}, reload: () => {{}} }},
  }},
  document: {{
    addEventListener: () => {{}},
    querySelectorAll: () => [],
    getElementById: () => null,
  }},
}};
vm.createContext(context);
vm.runInContext(fs.readFileSync({ruta}, "utf8"), context);
vm.runInContext('accionGestionDatosPendiente = "browser"; ejecutarGestionDatosConfirmada();', context);
const eliminadas = [
  "miRetiroProyectado.simulacion",
  "miRetiroProyectado.privacidadConsentimientoSesion",
  "calculadoraPensionCSS.simulacion",
  "calculadoraPensionCSS.privacidadConsentimientoSesion",
].every((k) => !sessionStorage.has(k)) && [
  "miRetiroProyectado.privacidadConsentimiento",
  "miRetiroProyectado.tema",
  "calculadoraPensionCSS.privacidadConsentimiento",
  "mi-retiro-proyectado-tema",
].every((k) => !localStorage.has(k));
if (!eliminadas) process.exit(21);
if (!sessionStorage.has("otraAplicacion.sesion")) process.exit(22);
if (!localStorage.has("otraAplicacion.local")) process.exit(23);
if (destino !== "/?privacidad=1") process.exit(24);
'''
        resultado = subprocess.run(
            ["node", "-e", script],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, resultado.returncode, resultado.stderr or resultado.stdout)


if __name__ == "__main__":
    unittest.main()
