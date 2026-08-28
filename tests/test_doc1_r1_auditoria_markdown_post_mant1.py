"""Regresión documental de DOC.1 R1 post-MANT.1."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

DOC1_EVIDENCE = [
    "docs/archive/governance/markdown-audit-post-mant1-doc1-r1.md",
    "docs/archive/governance/doc1-r1-markdown-decision-matrix.md",
    "docs/archive/governance/doc1-r1-markdown-update-context.md",
    "docs/archive/governance/doc1-r1-post-mant1-documentation-baseline.md",
    "docs/archive/governance/doc1-r1-applicability-only-review.md",
    "docs/archive/governance/doc1-r1-markdown-documentation-closeout.md",
]

DOCS_VIGENTES_REVISADOS = [
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "RELEASES.md",
    "SECURITY.md",
    "VERSIONING.md",
    "docs/architecture/system-architecture.md",
    "docs/decisions/README.md",
    "docs/architecture/development-center.md",
    "docs/product/functional-specification.md",
    "docs/standards/code-and-comments.md",
    "docs/README.md",
    "docs/governance/pre-1-0-revision-ledger.md",
    "docs/archive/governance/ver2-revision-decision-matrix.md",
    "docs/product/traceability-matrix.md",
    "docs/operations/observability-and-logs.md",
    "docs/governance/master-plan-to-1-0.md",
    "docs/security/privacy-policy.md",
    "docs/operations/release-process.md",
    "docs/governance/roadmap.md",
    "docs/product/transparency.md",
    "docs/operations/validation.md",
]

FRASES_DESACTUALIZADAS = [
    "Bloque transversal activo",
    "Siguiente bloque funcional",
    "pendiente de integración final",
    "todavía pendiente",
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def test_doc1_r1_evidence_files_exist():
    for rel in DOC1_EVIDENCE:
        assert (ROOT / rel).is_file(), rel


def test_linea_base_documental_post_mant1_define_estado_canonico():
    text = read("docs/archive/governance/doc1-r1-post-mant1-documentation-baseline.md")

    assert "`0.0.26-beta`" in text
    assert "`VERSION`" in text
    assert "MANT.1 R7" in text
    assert "#55" in text
    assert "`57078f2`" in text
    assert "`0.0.71.01-beta`" in text
    assert "candidato" in text
    assert "`939 passed`" in text
    assert "`928 tests OK`" in text


def test_estado_historico_doc1_r1_no_congela_version_actual():
    linea_base = read(
        "docs/archive/governance/"
        "doc1-r1-post-mant1-documentation-baseline.md"
    )
    cierre = read(
        "docs/archive/governance/"
        "doc1-r1-markdown-documentation-closeout.md"
    )
    assert "`0.0.71.01-beta`" in linea_base
    assert "`VERSION` permanece en `0.0.26-beta`" in cierre


def test_readme_expone_estado_vigente_y_doc1_preserva_su_cierre():
    readme = read("README.md")
    cierre = read("docs/archive/governance/doc1-r1-markdown-documentation-closeout.md")

    version = read("VERSION").strip()
    assert f"**Versión canónica vigente:** `{version}`" in readme
    assert "G071/E01 promovido en `VERSION`" in readme
    assert "VER.2 publicó `v0.0.71.01-beta`" in readme
    assert "**DOC.1 R1:** cerrado" in readme
    assert "**NOR.1:** cerrado" in readme
    assert "**NOR.2 R4:** cerrado" in readme
    assert "**NOR.2 R5:** cerrado" in readme
    assert "**NOR.2 R6:** cerrado" in readme
    assert "**NOR.2 R7:** cerrado" in readme
    assert "img.shields.io/badge/versi%C3%B3n-" in readme

    # Los detalles post-MANT.1 pertenecen a la evidencia histórica de DOC.1,
    # no al estado operativo actual de README.
    assert "MANT.1 queda cerrado operativamente" in cierre
    assert "DOC.1 R1 queda cerrado" in cierre
    assert "`0.0.71.01-beta` permanece como candidato VER.2" in cierre


def test_security_declara_estado_vigente_post_mant1_y_preserva_anclas():
    text = read("SECURITY.md")

    assert "## Estado de seguridad post-MANT.1" in text
    version = read("VERSION").strip()
    assert f"La versión canónica vigente es `{version}`" in text
    assert "`v0.0.71.01-beta`" in text
    assert "G071/E01" in text
    assert "Referencia legacy histórica preservada por pruebas de regresión" in text


def test_docs_vigentes_no_conservan_frases_de_estado_obsoleto():
    errores = []

    for rel in DOCS_VIGENTES_REVISADOS:
        text = read(rel)

        for numero, linea in enumerate(text.splitlines(), start=1):
            for frase in FRASES_DESACTUALIZADAS:
                if frase.lower() not in linea.lower():
                    continue

                # TRANSPARENCIA conserva una formulación explícitamente histórica.
                if rel == "docs/product/transparency.md" and "evidencia histórica" in linea.lower():
                    continue

                # README conserva anclas históricas exigidas por pruebas previas.
                if rel == "README.md" and "ancla histórica" in linea.lower():
                    continue

                # El Plan Maestro conserva una ancla exacta heredada de VER.2.
                if (
                    rel == "docs/governance/master-plan-to-1-0.md"
                    and "ancla histórica preservada" in linea.lower()
                ):
                    continue

                # CHANGELOG puede conservar redacciones históricas si están en pasado.
                if rel == "CHANGELOG.md" and "quedó documentado en ese momento" in linea.lower():
                    continue

                errores.append(f"{rel}:{numero}: {linea}")

    assert not errores, "\n".join(errores)


def test_indice_lista_evidencia_doc1_r1():
    text = read("docs/README.md")

    for rel in DOC1_EVIDENCE:
        nombre = Path(rel).name
        assert nombre in text

def test_cierre_doc1_r1_resume_alcance_limites_y_validacion():
    text = read("docs/archive/governance/doc1-r1-markdown-documentation-closeout.md")

    assert "Total Markdown evaluados: `106`" in text
    assert "Documentos marcados `ACTUALIZAR`: `15`" in text
    assert "Documentos marcados `REVISAR_MANUALMENTE`: `8`" in text
    assert "Documentos marcados `REVISAR_SOLO_SI_APLICA`: `7`" in text
    assert "`VERSION` permanece en `0.0.26-beta`" in text
    assert "`0.0.71.01-beta` permanece como candidato VER.2" in text
    assert "DOC.1 R1 queda cerrado" in text
    assert "fórmulas previsionales" in text
    assert "`regulations/`" in text
    assert "`data/`" in text
    assert "`_entregas/`" in text
