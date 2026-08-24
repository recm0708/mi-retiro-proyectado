"""Regresión documental de VER.2 R2 post-R1.

Protege que la documentación viva se aclare sin consumir el candidato VER.2,
sin publicar versión nueva y sin modificar archivos protegidos.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

ARQUITECTURA = ROOT / "docs" / "ARQUITECTURA.md"
RELEASES = ROOT / "RELEASES.md"
README = ROOT / "README.md"
INDICE = ROOT / "docs" / "INDICE.md"
ANALISIS = ROOT / "docs" / "VER2_R2_ANALISIS_CONTRADICCIONES_POST_R1.md"
PROPUESTA = ROOT / "docs" / "VER2_R2_PROPUESTA_CORRECCION_DOCUMENTACION_VIVA.md"
CIERRE = ROOT / "docs" / "VER2_R2_CIERRE_DOCUMENTACION_VIVA_POST_R1.md"


def leer(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ver2_r2_documentos_existen_e_indexan_cierre():
    indice = leer(INDICE)

    assert ANALISIS.exists()
    assert PROPUESTA.exists()
    assert CIERRE.exists()
    assert "VER2_R2_ANALISIS_CONTRADICCIONES_POST_R1.md" in indice
    assert "VER2_R2_PROPUESTA_CORRECCION_DOCUMENTACION_VIVA.md" in indice
    assert "VER2_R2_CIERRE_DOCUMENTACION_VIVA_POST_R1.md" in indice


def test_ver2_r2_aclara_version_visible_sin_consumir_candidato():
    arquitectura = leer(ARQUITECTURA)

    assert "`0.0.26-beta` como versión visible/canónica legacy" in arquitectura
    assert "no la trata como candidato VER.2" in arquitectura


def test_ver2_r2_preserva_readme_como_explicacion_historica():
    readme = leer(README)

    assert "Después de `v0.0.26-beta`" in readme
    assert "G070/E02" in readme
    assert "no se crean tags revision-aware retrospectivos para G001–G070" in readme


def test_ver2_r2_aclara_candidato_no_publicado_en_releases():
    releases = leer(RELEASES)

    assert "candidato VER.2 no publicado" in releases
    assert "`0.0.71.01-beta` permanece como candidato VER.2 G071/E01 no publicado" in releases
    assert "no sustituye `VERSION = 0.0.26-beta`" in releases
    assert "no crea un tag formal" in releases


def test_ver2_r2_preserva_versionado_real():
    cierre = leer(CIERRE)
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()

    assert version == "0.0.26-beta"
    assert "`VERSION` permanece en `0.0.26-beta`" in cierre
    assert "`v0.0.26-beta` permanece como último tag formal" in cierre
    assert "`0.0.71.01-beta` permanece como candidato VER.2 G071/E01 no publicado" in cierre


def test_ver2_r2_declara_archivos_protegidos_sin_cambios():
    cierre = leer(CIERRE)

    for esperado in [
        "No se modifica `VERSION`.",
        "No se modifica `app/core/version.py`.",
        "No se modifica `app/core/config.py`.",
        "No se modifica `regulations/`, `data/` ni `_entregas/`.",
        "No se crean tags.",
        "No se publica `0.0.71.01-beta`.",
    ]:
        assert esperado in cierre
