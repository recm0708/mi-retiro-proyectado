"""Regresión de VER.2 R4 para la promoción controlada G071/E01."""

from pathlib import Path

from app.core.config import APP_VERSION
from app.core.version import descomponer_version_beta_revision, version_valida


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "VER2_R4_PROMOCION_G071_E01.md"


def leer(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_version_promovida_a_g071_e01():
    version = leer(ROOT / "VERSION").strip()

    assert version == "0.0.71.01-beta"
    assert APP_VERSION == version
    assert version_valida(version)
    assert descomponer_version_beta_revision(version) == (71, 1)


def test_documento_r4_existe_e_indexado():
    indice = leer(ROOT / "docs" / "README.md")

    assert DOC.exists()
    assert "VER2_R4_PROMOCION_G071_E01.md" in indice


def test_r4_no_crea_tag_dentro_del_pr():
    texto = leer(DOC)

    assert "Tag formal pendiente post-merge: `v0.0.71.01-beta`" in texto
    assert "`v0.0.71.01-beta` no se crea dentro de esta rama." in texto
    assert "`v0.0.26-beta` permanece como último tag formal legacy" in texto


def test_r4_preserva_historia_y_protegidos_de_dominio():
    texto = leer(DOC)

    assert "Mantiene referencias históricas a `0.0.26-beta`" in texto
    assert "No mueve ni recrea `v0.0.26-beta`." in texto
    assert "No crea tags revision-aware retrospectivos para G001–G070." in texto
    assert "No modifica motores previsionales, normativa, datos protegidos ni `_entregas/`." in texto
