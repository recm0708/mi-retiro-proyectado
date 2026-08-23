"""Regresiones de comentarios internos para servicios Python de aplicación."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


SERVICIOS_R5A = {
    "app/servicios/trazabilidad.py": (
        "resultado ya calculado",
        "pasos se agregan",
        "advertencias del motor",
    ),
    "app/servicios/comparador.py": (
        "no mutar",
        "matriz retiro × salario",
        "filas completas",
    ),
    "app/servicios/como_se_calcula.py": (
        "JSON versionados",
        "plantilla",
        "no se calculan pensiones",
    ),
    "app/servicios/fuentes_normativas.py": (
        "parámetros versionados",
        "sistemas",
        "contenido metodológico",
    ),
    "app/servicios/detalle_anio_actual.py": (
        "cuotas todavía no confirmadas",
        "contrato de salida",
        "meses completos",
    ),
    "app/servicios/ficha_digital.py": (
        "Ficha Digital esperada",
        "datos personales",
        "no se fuerza",
    ),
}

PATRON_TRAZABILIDAD_MAL_UBICADA = re.compile(
    r"MANT\.\s*1|DEV\.2|UX\.4\.6|PR\s*#\d+|pull request",
    re.IGNORECASE,
)


class TestMant1R5AComentariosServiciosApp(unittest.TestCase):
    """Protege comentarios útiles sin convertir el código en bitácora histórica."""

    def _leer(self, ruta: str) -> str:
        return (ROOT / ruta).read_text(encoding="utf-8")

    def _comentarios_internos(self, texto: str) -> list[str]:
        return [
            linea.strip()
            for linea in texto.splitlines()
            if linea.lstrip().startswith("#")
        ]

    def test_servicios_revisados_tienen_comentarios_internos_de_intencion(self):
        for ruta, patrones in SERVICIOS_R5A.items():
            texto = self._leer(ruta)
            comentarios = "\n".join(self._comentarios_internos(texto))
            with self.subTest(ruta=ruta):
                self.assertGreaterEqual(
                    len(self._comentarios_internos(texto)),
                    4,
                    f"{ruta} debe conservar comentarios internos de intención.",
                )
                for patron in patrones:
                    self.assertIn(patron, comentarios)

    def test_comentarios_de_app_no_registran_revisiones_o_pr(self):
        for ruta in SERVICIOS_R5A:
            texto = self._leer(ruta)
            comentarios = self._comentarios_internos(texto)
            hallazgos = [
                f"{ruta}:{indice}:{linea}"
                for indice, linea in enumerate(comentarios, start=1)
                if PATRON_TRAZABILIDAD_MAL_UBICADA.search(linea)
            ]
            with self.subTest(ruta=ruta):
                self.assertEqual([], hallazgos)

    def test_documentacion_transversal_registra_mant1_r5a(self):
        for ruta in (
            "CHANGELOG.md",
            "docs/ESTANDAR_CODIGO_Y_COMENTARIOS.md",
            "docs/VALIDACION.md",
            "docs/ARQUITECTURA.md",
            "docs/ROADMAP.md",
        ):
            texto = self._leer(ruta)
            with self.subTest(ruta=ruta):
                self.assertIn("MANT.1 R5A", texto)
                self.assertIn("comentarios internos", texto)

    def test_r5a_no_promueve_version_ni_sec2(self):
        version = self._leer("VERSION").strip()
        self.assertEqual("0.0.26-beta", version)

        changelog = self._leer("CHANGELOG.md")
        seccion = changelog.split("### MANT.1 R5A", 1)[1].split("### MANT.1 R4", 1)[0]
        self.assertIn("no cambia `VERSION`, `APP_VERSION`", seccion)
        self.assertIn("ni SEC.2", seccion)
        self.assertNotIn("SEC.2 — Hardening integral iniciado", seccion)


if __name__ == "__main__":
    unittest.main()
