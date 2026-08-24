"""Regresión MANT.1 R7: cierre operativo posterior a auditorías R5H/R6."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TESTS = ROOT / "tests"

DOCUMENTO_R7 = DOCS / "CIERRE_OPERATIVO_POST_AUDITORIA_R7.md"
INDICE = DOCS / "INDICE.md"


def _leer(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8", errors="replace")


def test_r7_documento_de_cierre_existe_y_declara_alcance_operativo():
    """El cierre R7 debe quedar documentado sin abrir alcance funcional."""

    texto = _leer(DOCUMENTO_R7)

    tokens = [
        "MANT.1 R7",
        "Cierre operativo post-auditoría",
        "R7 no introduce cambios funcionales",
        "No existen ramas locales no mergeadas contra `main`",
        "Las pruebas focalizadas R5H + R6 pasan correctamente",
        "R7 no modifica",
        "`VERSION`",
        "`app/core/version.py`",
        "`app/core/config.py`",
        "`regulations/`",
        "`data/`",
        "`_entregas/`",
    ]

    for token in tokens:
        assert token in texto


def test_r7_indice_documental_referencia_cierre_operativo():
    """Todo documento nuevo en docs raíz debe estar referenciado en el índice."""

    indice = _leer(INDICE)

    assert "CIERRE_OPERATIVO_POST_AUDITORIA_R7.md" in indice
    assert "MANT.1 R7" in indice


def test_r7_evidencias_r5h_y_r6_permanecen_disponibles():
    """El cierre operativo depende de que R5H y R6 sigan materializados."""

    evidencias = [
        DOCS / "AUDITORIA_NOMBRES_RESTANTES_R5H.md",
        DOCS / "AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md",
        TESTS / "test_mant1_r5h_auditoria_nombres_restantes.py",
        TESTS / "test_mant1_r6_auditoria_funcional_post_renombres.py",
    ]

    for ruta in evidencias:
        assert ruta.exists(), ruta


def test_r7_indice_conserva_referencias_r5h_r6_y_r7():
    """El índice debe reflejar la secuencia documental de cierre MANT.1."""

    indice = _leer(INDICE)

    for token in [
        "AUDITORIA_NOMBRES_RESTANTES_R5H.md",
        "AUDITORIA_FUNCIONAL_POST_RENOMBRES_R6.md",
        "CIERRE_OPERATIVO_POST_AUDITORIA_R7.md",
    ]:
        assert token in indice
