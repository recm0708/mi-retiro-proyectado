"""Valida la coherencia documental incorporada en MANT.1 R5G."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


class TestMant1R5GDocumentacion(unittest.TestCase):
    def test_auditoria_r5g_existe_y_declara_alcance(self):
        ruta = DOCS / "archive" / "technical" / "documentation-audit-r5g.md"

        self.assertTrue(ruta.is_file())

        texto = ruta.read_text(encoding="utf-8")

        esperados = (
            "MANT.1 R5G",
            "coherencia documental",
            "referencias internas",
            "No modifica lógica funcional",
            "VERSION",
            "APP_VERSION",
            "SEC.2",
            "_entregas/",
        )

        for esperado in esperados:
            with self.subTest(esperado=esperado):
                self.assertIn(esperado, texto)

    def test_auditoria_r5g_documenta_excepciones_semanticas(self):
        texto = (DOCS / "archive" / "technical" / "documentation-audit-r5g.md").read_text(encoding="utf-8")

        expresiones = (
            "normativa/privacidad",
            "normativa/código",
            "normativa/jurídica",
            "no representan rutas obsoletas",
            "no carpetas del repositorio",
        )

        for expresion in expresiones:
            with self.subTest(expresion=expresion):
                self.assertIn(expresion, texto)

    def test_documentos_raiz_de_docs_estan_indexados(self):
        indice = (DOCS / "README.md").read_text(encoding="utf-8")

        faltantes = []

        for ruta in sorted(DOCS.glob("*.md")):
            if ruta.name == "README.md":
                continue

            if ruta.name not in indice:
                faltantes.append(f"docs/{ruta.name}")

        self.assertEqual([], faltantes)

    def test_indice_delega_documentos_relevantes_a_sus_autoridades(self):
        indice = (DOCS / "README.md").read_text(encoding="utf-8")
        decisiones = (DOCS / "decisions/README.md").read_text(
            encoding="utf-8"
        )
        estandares = (DOCS / "standards/README.md").read_text(
            encoding="utf-8"
        )
        archivo = (DOCS / "archive/README.md").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "architecture/development-center.md",
            indice,
        )
        self.assertIn(
            "[Índice de estándares](standards/README.md)",
            indice,
        )
        self.assertIn(
            "[Índice del archivo](archive/README.md)",
            indice,
        )

        self.assertIn(
            "adr-179-revision-aware-versioning.md",
            decisiones,
        )
        self.assertIn(
            "file-structure-by-extension.md",
            estandares,
        )
        self.assertIn(
            "[`technical/`](technical/)",
            archivo,
        )
        self.assertIn(
            "[`ux/`](ux/)",
            archivo,
        )

        historicos = (
            "archive/technical/file-structure-audit-r5d.md",
            "archive/technical/folders-audit-r5e.md",
            "archive/technical/files-audit-r5f.md",
            "archive/technical/documentation-audit-r5g.md",
            "archive/ux/ux46h-r1-results-audit.md",
            "archive/ux/ux46a-visual-redesign.md",
            "archive/ux/ux46b-step1-personal-data.md",
            "archive/ux/ux46c-step2-contributions.md",
            "archive/ux/ux46d-step3-history.md",
        )

        for relativo in historicos:
            with self.subTest(relativo=relativo):
                self.assertTrue(
                    (DOCS / relativo).is_file(),
                    relativo,
                )
                self.assertNotIn(
                    relativo,
                    indice,
                )
    def test_changelog_y_validacion_declaran_r5g(self):
        superficies = (
            ROOT / "CHANGELOG.md",
            DOCS / "operations/validation.md",
        )

        for ruta in superficies:
            with self.subTest(ruta=str(ruta.relative_to(ROOT))):
                texto = ruta.read_text(encoding="utf-8")
                self.assertIn("MANT.1 R5G", texto)

    def test_enlaces_markdown_locales_a_md_no_estan_rotos(self):
        patron = re.compile(r"\[[^\]]+\]\(([^)]+\.md(?:#[^)]+)?)\)")
        rotos = []

        for ruta in sorted(DOCS.rglob("*.md")):
            if "archive" in ruta.relative_to(DOCS).parts:
                continue

            texto = ruta.read_text(encoding="utf-8")

            for coincidencia in patron.finditer(texto):
                destino = coincidencia.group(1).split("#", 1)[0]

                if destino.startswith(("http://", "https://", "mailto:")):
                    continue

                destino_absoluto = (ruta.parent / destino).resolve()

                try:
                    destino_absoluto.relative_to(ROOT)
                except ValueError:
                    rotos.append((ruta.relative_to(ROOT).as_posix(), destino, "fuera_del_repo"))
                    continue

                if not destino_absoluto.exists():
                    rotos.append(
                        (
                            ruta.relative_to(ROOT).as_posix(),
                            destino,
                            destino_absoluto.relative_to(ROOT).as_posix(),
                        )
                    )

        self.assertEqual([], rotos)


if __name__ == "__main__":
    unittest.main()
