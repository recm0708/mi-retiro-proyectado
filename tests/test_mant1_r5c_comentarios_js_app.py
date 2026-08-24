"""Regresiones de comentarios funcionales para JavaScript de aplicación."""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]

JS_COMENTARIOS_ESPERADOS = {
    "app/static/js/comparator.js": (
        "no replica reglas de elegibilidad ni fórmulas de pensión",
        "obligatorias ya fijadas por el estado de la simulación",
        "advertencias globales y por combinación se deduplican",
    ),
    "app/static/js/simulation.js": (
        "fuente persistida del",
        "silenciar mensajes y reportes nativos de formulario",
        "Paso 3 consolida decisiones de historial",
    ),
    "app/static/js/results.js": (
        "comparación acreditado/proyectado usa el mismo endpoint",
        "campos vacíos viajan como null",
        "Cambiar el escenario salarial invalida únicamente salidas dependientes",
    ),
    "app/static/js/results_orchestration.js": (
        "contenedores dependen del último cálculo válido",
        "transición Mixto -> SUCGS reutiliza datos",
        "interfaz se crea de forma idempotente",
    ),
    "app/static/js/data_management.js": (
        "laterales normales",
        "Paso 6 es siempre descendiente",
        "borrado integral se limita a claves propias",
    ),
    "app/static/js/privacy.js": (
        "consentimiento persistente solo es válido",
        "alcanza el final del contenido",
        "mismo modal funciona para lectura informativa",
    ),
    "app/static/js/attachment_processing.js": (
        "token conserva el estado original",
        "devuelve accesibilidad visual",
    ),
    "app/static/js/official_data_import.js": (
        "vigencia compara el período más reciente",
        "borrador revisable",
        "campos detectados se bloquean",
    ),
}

MARCAS_HISTORICAS_NO_OPERATIVAS = (
    "MANT.1",
    "DEV.2",
    "UX.4.6",
    "PR #",
    "pull request",
)

CLAVES_STORAGE_ESPERADAS = (
    "miRetiroProyectado.simulacion",
    "miRetiroProyectado.privacidadConsentimiento",
    "miRetiroProyectado.privacidadConsentimientoSesion",
    "miRetiroProyectado.tema",
)


class TestMant1R5CComentariosJSApp(unittest.TestCase):
    """Protege comentarios de intención en JavaScript sin cambiar contratos."""

    @staticmethod
    def _leer(ruta: str) -> str:
        return (ROOT / ruta).read_text(encoding="utf-8")

    def test_js_revisados_contienen_comentarios_funcionales(self):
        for ruta, fragmentos in JS_COMENTARIOS_ESPERADOS.items():
            texto = self._leer(ruta)
            with self.subTest(ruta=ruta):
                self.assertIn("use strict", texto)
                for fragmento in fragmentos:
                    self.assertIn(fragmento, texto)

    def test_js_revisados_no_declaran_trazabilidad_historica_en_codigo(self):
        for ruta in JS_COMENTARIOS_ESPERADOS:
            texto = self._leer(ruta)
            with self.subTest(ruta=ruta):
                for marca in MARCAS_HISTORICAS_NO_OPERATIVAS:
                    self.assertNotIn(marca, texto)

    def test_claves_de_almacenamiento_publicas_siguen_estables(self):
        contenido = "\n".join(
            self._leer(ruta)
            for ruta in JS_COMENTARIOS_ESPERADOS
        )

        for clave in CLAVES_STORAGE_ESPERADAS:
            with self.subTest(clave=clave):
                self.assertIn(clave, contenido)

        gestion = self._leer("app/static/js/data_management.js")
        privacidad = self._leer("app/static/js/privacy.js")
        self.assertIn("CLAVES_GESTION_LEGACY_SESION", gestion)
        self.assertIn("CLAVES_GESTION_LEGACY_LOCAL", gestion)
        self.assertIn("CLAVES_PRIVACIDAD_LEGACY_SESION", privacidad)
        self.assertNotIn("getItem(CLAVES_GESTION_LEGACY", gestion)
        self.assertNotIn("setItem(CLAVES_GESTION_LEGACY", gestion)
        self.assertNotIn("getItem(CLAVES_PRIVACIDAD_LEGACY", privacidad)
        self.assertNotIn("setItem(CLAVES_PRIVACIDAD_LEGACY", privacidad)

    def test_documentacion_transversal_registra_r5c_sin_promover_version(self):
        documentos = (
            "CHANGELOG.md",
            "docs/standards/code-and-comments.md",
            "docs/operations/validation.md",
            "docs/architecture/system-architecture.md",
            "docs/governance/roadmap.md",
        )

        for ruta in documentos:
            texto = self._leer(ruta)
            with self.subTest(ruta=ruta):
                self.assertIn("MANT.1 R5C", texto)
                self.assertIn("JavaScript", texto)

        changelog = self._leer("CHANGELOG.md")
        self.assertIn("no cambia `VERSION`, `APP_VERSION`", changelog)
        self.assertIn("sin cambiar claves de storage", changelog)


if __name__ == "__main__":
    unittest.main()
