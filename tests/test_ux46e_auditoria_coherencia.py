"""Regresiones UX.4.6e R7 para auditoría transversal de coherencia."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app"
DOCS = ROOT / "docs"


class TestUX46eAuditoriaCoherencia(unittest.TestCase):
    """Protege el gate transversal y su evolución posterior sin reescribir R7."""

    def test_roadmap_preserva_r7_r8_r9_y_cierre_ux46e(self):
        texto = (DOCS / "ROADMAP.md").read_text(encoding="utf-8")
        self.assertIn("R6 — renumeración/metadata; 586 pruebas", texto)
        self.assertIn("R7 — auditoría transversal; 598 pruebas", texto)
        self.assertIn("R8 — validación funcional/procedencia editable", texto)
        self.assertIn("R9.2 — cierre formal mediante PR #21/#22", texto)
        self.assertIn("R9.1 se conserva como candidato local histórico", texto)
        self.assertIn("[x] **UX.4.6e — Estandarización técnica", texto)

    def test_readme_preserva_cierre_r8_r9_sin_congelar_bloque_activo(self):
        texto = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("**UX.4.6e:** cerrada en `0.0.25-beta`", texto)
        self.assertIn("PR #21 integrado por squash", texto)
        self.assertIn("21 labels y 20/20 topics", texto)
        self.assertNotIn("**Bloque activo:** UX.4.6e", texto)
        self.assertIn("**Bloque transversal activo:** VER.2", texto)

    def test_auditoria_r7_existe_y_declara_linea_base_y_objetivo(self):
        texto = (DOCS / "AUDITORIA_UX46E_R7_2026-08-18.md").read_text(encoding="utf-8")
        self.assertIn("Ran 586 tests", texto)
        self.assertIn("12 regresiones", texto)
        self.assertIn("598 pruebas", texto)
        self.assertIn("R8 — prueba funcional manual + automática", texto)

    def test_documentos_primarios_usan_secuencia_vigente_f_a_i(self):
        rutas = (
            ROOT / "README.md",
            DOCS / "ROADMAP.md",
            DOCS / "TRANSPARENCIA.md",
            DOCS / "VALIDACION.md",
            DOCS / "PREPARACION_PUBLICA_GITHUB.md",
            DOCS / "INDICE.md",
        )
        combinados = "\n".join(p.read_text(encoding="utf-8") for p in rutas)
        self.assertIn("UX.4.6f", combinados)
        self.assertIn("UX.4.6g", combinados)
        self.assertIn("UX.4.6h", combinados)
        self.assertIn("UX.4.6i", combinados)
        self.assertNotIn("UX.4.6e — Paso 4 · Proyección salarial/laboral", combinados)

    def test_auditoria_historica_preserva_texto_y_agrega_nota_posterior(self):
        texto = (DOCS / "AUDITORIA_REPOSITORIO_2026-08-18.md").read_text(encoding="utf-8")
        self.assertIn("UX.4.6e — Paso 4 · Proyección salarial/laboral", texto)
        self.assertIn("Nota posterior — UX.4.6e R7", texto)
        self.assertIn("UX.4.6f / UX.4.6g / UX.4.6h", texto)

    def test_runtime_no_contiene_identificadores_cronologicos_en_comentarios(self):
        patrones = re.compile(r"\b(?:UX|GOV)\.\d")
        candidatos = []
        for ruta in APP.rglob("*"):
            if not ruta.is_file() or ruta.suffix.lower() not in {".py", ".js", ".css", ".html"}:
                continue
            texto = ruta.read_text(encoding="utf-8")
            if ruta.suffix == ".py":
                lineas = [linea for linea in texto.splitlines() if linea.lstrip().startswith("#")]
            elif ruta.suffix == ".js":
                lineas = [linea for linea in texto.splitlines() if "//" in linea or "/*" in linea or "*" in linea]
            elif ruta.suffix == ".css":
                lineas = [linea for linea in texto.splitlines() if "/*" in linea or "*" in linea]
            else:
                lineas = re.findall(r"<!--(.*?)-->", texto, flags=re.S)
            if any(patrones.search(linea) for linea in lineas):
                candidatos.append(str(ruta.relative_to(ROOT)))
        self.assertEqual([], candidatos)

    def test_python_app_mantiene_docstrings_completos(self):
        faltantes = []
        for ruta in APP.rglob("*.py"):
            arbol = ast.parse(ruta.read_text(encoding="utf-8"))
            if ast.get_docstring(arbol) is None:
                faltantes.append(f"{ruta.relative_to(ROOT)}:<module>")
            for nodo in ast.walk(arbol):
                if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if ast.get_docstring(nodo) is None:
                        faltantes.append(f"{ruta.relative_to(ROOT)}:{nodo.lineno}:{nodo.name}")
        self.assertEqual([], faltantes)

    def test_namespace_web_storage_no_regresa_a_lectura_pre_beta(self):
        archivos = {
            ruta.name: ruta.read_text(encoding="utf-8")
            for ruta in (APP / "static/js").glob("*.js")
        }
        runtime = "\n".join(archivos.values())
        for clave in (
            "miRetiroProyectado.simulacion",
            "miRetiroProyectado.privacidadConsentimiento",
            "miRetiroProyectado.privacidadConsentimientoSesion",
            "miRetiroProyectado.tema",
        ):
            self.assertIn(clave, runtime)

        for nombre, contenido in archivos.items():
            if nombre in {"gestion_datos.js", "privacidad.js"}:
                continue
            with self.subTest(nombre=nombre):
                self.assertNotIn("calculadoraPensionCSS", contenido)
                self.assertNotIn("mi-retiro-proyectado-tema", contenido)

        self.assertIn("CLAVES_GESTION_LEGACY", archivos["gestion_datos.js"])
        self.assertIn("CLAVES_PRIVACIDAD_LEGACY", archivos["privacidad.js"])

    def test_interfaz_muestra_ayuda_y_no_expone_gobierno_interno(self):
        plantillas = "\n".join(
            ruta.read_text(encoding="utf-8")
            for ruta in (APP / "templates").rglob("*.html")
        )
        for visible in (
            "Ayuda y contacto",
            "Abrir repositorio del proyecto",
            "Privacidad",
            "Fuentes oficiales",
            "No sustituye la determinación oficial",
        ):
            self.assertIn(visible, plantillas)
        for interno in (
            "CODEOWNERS",
            "Dependabot",
            "ruleset",
            "allowed_signers",
            "Auditoría de gobernanza",
            "ADR-",
        ):
            self.assertNotIn(interno, plantillas)

    def test_enlaces_markdown_relativos_vigentes(self):
        rotos = []
        rutas = [
            ROOT / "README.md",
            ROOT / "CONTRIBUTING.md",
            ROOT / "GOVERNANCE.md",
            ROOT / "SECURITY.md",
            ROOT / "SUPPORT.md",
            *DOCS.glob("*.md"),
        ]
        for ruta in rutas:
            texto = ruta.read_text(encoding="utf-8")
            for objetivo in re.findall(r"\[[^\]]*\]\(([^)]+)\)", texto):
                objetivo = objetivo.strip()
                if not objetivo or objetivo.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                objetivo = objetivo.split("#", 1)[0]
                if objetivo and not (ruta.parent / objetivo).resolve().exists():
                    rotos.append(f"{ruta.relative_to(ROOT)} -> {objetivo}")
        self.assertEqual([], rotos)

    def test_higiene_textual_y_json_versionado(self):
        """Audita solo archivos versionables y la política canónica de EOL."""

        errores = []
        extensiones = {
            ".py", ".js", ".css", ".html", ".md", ".yml", ".yaml", ".json",
            ".txt", ".ps1",
        }
        nombres_sin_extension = {
            "VERSION", "LICENSE", ".gitignore", ".gitattributes", ".editorconfig",
            "pre-commit",
        }

        atributos = (ROOT / ".gitattributes").read_text(encoding="utf-8")
        self.assertIn("* text=auto eol=lf", atributos)

        resultado = subprocess.run(
            [
                "git",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "-z",
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
        )

        rutas_relativas = [
            Path(valor.decode("utf-8"))
            for valor in resultado.stdout.split(b"\0")
            if valor
        ]

        for relativa in rutas_relativas:
            ruta = ROOT / relativa
            if not ruta.is_file():
                continue
            if ruta.suffix.lower() not in extensiones and ruta.name not in nombres_sin_extension:
                continue

            contenido = ruta.read_bytes()
            if contenido.startswith(b"\xef\xbb\xbf"):
                errores.append(f"{relativa}:BOM")

            try:
                texto = contenido.decode("utf-8")
            except UnicodeDecodeError as error:
                errores.append(f"{relativa}:UTF8:{error}")
                continue

            for numero, linea in enumerate(texto.splitlines(), start=1):
                if linea.endswith((" ", "\t")):
                    errores.append(f"{relativa}:{numero}:whitespace")
                    break

            if ruta.suffix.lower() == ".json":
                try:
                    json.loads(texto)
                except json.JSONDecodeError as error:
                    errores.append(f"{relativa}:JSON:{error}")

        self.assertEqual([], errores)

    def test_adr165_historico_y_adr179_revision_aware_estan_trazados(self):
        texto = (DOCS / "DECISIONES.md").read_text(encoding="utf-8")
        self.assertIn("## ADR-165 — La auditoría transversal es un gate", texto)
        ids = [int(x) for x in re.findall(r"(?m)^## ADR-(\d{3})\s+—", texto)]
        self.assertGreaterEqual(max(ids), 178)
        self.assertEqual(list(range(1, max(ids) + 1)), ids)
        self.assertIn(
            f"**ADR indexadas:** {max(ids)} (`ADR-001` a `ADR-{max(ids):03d}`)",
            texto,
        )
        adr179 = (DOCS / "ADR_179_VERSIONADO_REVISION_AWARE.md").read_text(encoding="utf-8")
        self.assertIn("# ADR-179 —", adr179)
        self.assertIn("0.GG.RR.EE-beta", adr179)


if __name__ == "__main__":
    unittest.main()