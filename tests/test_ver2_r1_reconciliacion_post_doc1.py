"""Regresión documental de VER.2 R1 post-DOC.1.

Protege que VER.2 R1 sea una fase de auditoría y decisión sin consumir versión,
sin crear tags y sin modificar archivos protegidos.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ARCHIVE = ROOT / "docs" / "archive" / "governance"
AUDITORIA = ARCHIVE / "ver2-r1-post-doc1-reconciliation-audit.md"
MATRIZ = ARCHIVE / "ver2-r1-post-doc1-reconciliation-decision-matrix.md"
DECISION = ARCHIVE / "ver2-r1-post-doc1-operational-decision.md"


def leer(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_ver2_r1_documentos_base_existen():
    assert AUDITORIA.exists()
    assert MATRIZ.exists()
    assert DECISION.exists()


def test_ver2_r1_preserva_estado_historico_y_candidato():
    decision = leer(DECISION)

    assert "`VERSION` permanece en `0.0.26-beta`" in decision
    assert "`v0.0.26-beta` permanece como último tag formal" in decision
    assert "`0.0.71.01-beta` permanece como candidato VER.2 G071/E01" in decision


def test_ver2_r1_no_declara_publicacion_ni_consumo_candidato():
    decision = leer(DECISION)

    assert "No se crea tag." in decision
    assert "No se declara `0.0.71.01-beta` como versión publicada." in decision
    assert "No se consume el candidato VER.2." in decision
    assert "No modificar `VERSION` durante VER.2 R1." in leer(MATRIZ)


def test_ver2_r1_protege_archivos_y_directorios_sensibles():
    decision = leer(DECISION)
    matriz = leer(MATRIZ)
    auditoria = leer(AUDITORIA)

    for esperado in [
        "`app/core/version.py`",
        "`app/core/config.py`",
        "`regulations/`, `data/` ni `_entregas/`",
    ]:
        assert esperado in decision
        assert esperado in matriz
        assert esperado in auditoria


def test_ver2_r1_matriz_clasifica_alcance_y_contradicciones():
    matriz = leer(MATRIZ)
    decision = leer(DECISION)

    assert "Total de coincidencias clasificadas: `1601`" in matriz
    assert "| `PROTEGIDO_NO_MODIFICAR` | 24 |" in matriz
    assert "| `PRESERVAR_EVIDENCIA_CERRADA` | 448 |" in matriz
    assert "| `PRESERVAR_PRUEBA_REGRESION` | 80 |" in matriz
    assert "| `REVISAR_POSIBLE_CONTRADICCION` | 11 |" in matriz

    assert "Las siguientes filas se trasladan a VER.2 R2 como prioridad alta:" in decision
    assert "| `REVISAR_POSIBLE_CONTRADICCION` | 11 |" not in decision


def test_ver2_r1_define_salida_hacia_r2_sin_cambios_de_versionado():
    decision = leer(DECISION)

    assert "Abrir VER.2 R2" in decision
    assert "documentación viva priorizada" in decision
    assert "sin modificar todavía `VERSION`, `data/`, `regulations/` ni tags" in decision
