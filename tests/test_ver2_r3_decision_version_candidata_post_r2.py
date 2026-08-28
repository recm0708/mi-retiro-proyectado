"""Regresión documental de VER.2 R3 sobre versión candidata post-R2."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECISION = (
    ROOT
    / "docs"
    / "archive"
    / "governance"
    / "ver2-r3-post-r2-candidate-version-decision.md"
)
INDICE = ROOT / "docs" / "README.md"


def leer(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ver2_r3_decision_existe_e_indexada():
    assert DECISION.exists()
    assert "ver2-r3-post-r2-candidate-version-decision.md" in leer(INDICE)


def test_ver2_r3_mantiene_candidato_g071_e01():
    texto = leer(DECISION)

    assert "El candidato se mantiene en `0.0.71.01-beta` como VER.2 G071/E01." in texto
    assert "No consumen G072" in texto
    assert "no incrementan EE" in texto


def test_ver2_r3_no_publica_ni_taguea_candidato():
    texto = leer(DECISION)

    assert "`v0.0.71.01-beta` no existe todavía." in texto
    assert "`0.0.71.01-beta` permanece como candidato VER.2 G071/E01, no como versión publicada." in texto
    assert "R3 no crea tags." in texto
    assert "R3 no publica `0.0.71.01-beta`." in texto


def test_ver2_r3_preserva_version_historica_de_la_decision():
    texto = leer(DECISION)

    assert "`VERSION` permanece en `0.0.26-beta`." in texto
    assert "`v0.0.26-beta` permanece como último tag formal." in texto


def test_ver2_r3_declara_punto_futuro_de_promocion():
    texto = leer(DECISION)

    assert "La modificación de `VERSION` corresponde a una fase posterior de promoción controlada del candidato" in texto
    assert "después de cerrar R3" in texto
    assert "crear el tag firmado `v0.0.71.01-beta`, si corresponde" in texto
