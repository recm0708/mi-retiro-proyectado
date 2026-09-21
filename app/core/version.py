"""Versión canónica de Mi Retiro Proyectado.

La fuente única es el archivo ``VERSION`` situado en la raíz del repositorio.
Este módulo valida y expone su contenido para que FastAPI, las plantillas y
otros componentes no mantengan copias independientes del número de versión.

Se preservan las familias históricas ``0.0.N-beta`` y
``0.<G_HI>.<G_LO>.<EE>-beta``.

La política de versionado introduce prospectivamente desde G128 la familia
revision-aware v2 simplificada:

``0.<GLOBAL>.<EDITION>.<CORRECTION>-beta``

La revisión funcional y el ordinal de mantenimiento permanecen como metadata
de gobierno y no forman parte de la versión visible. La línea estable conserva
cuatro componentes ``MAYOR.MENOR.PARCHE.REVISIÓN`` sin sufijo. El Build es
independiente de VERSION.
"""

from pathlib import Path
import re


VERSION_FILE = Path(__file__).resolve().parents[2] / "VERSION"

_VERSION_BETA_LEGACY_PATTERN = re.compile(
    r"^0\.0\.[1-9][0-9]*-beta$"
)

_VERSION_BETA_REVISION_V1_PATTERN = re.compile(
    r"^0\.(0|[1-9][0-9]*)\.([0-9]{2})\.([0-9]{2})-beta$"
)

_VERSION_BETA_REVISION_V2_PATTERN = re.compile(
    r"^0\.([1-9][0-9]*)"
    r"\.([1-9][0-9]*)"
    r"\.(0|[1-9][0-9]*)-beta$"
)

_VERSION_OFICIAL_PATTERN = re.compile(
    r"^[1-9][0-9]*\.[0-9]+\.[0-9]+\.[0-9]+$"
)


def _global_desde_fragmentos(
    grupo: str,
    resto: str,
) -> int:
    """Reconstruye el contador Global de la familia revision-aware v1."""

    return int(grupo) * 100 + int(resto)


def descomponer_version_beta_revision_v2(
    version: str,
) -> tuple[int, int, int] | None:
    """Devuelve ``(Global, Edition, Correction)`` para v2.

    La familia v2 comienza prospectivamente en G128. Edition admite 1..99
    y Correction admite 0..999. Los componentes usan su forma decimal
    canónica, sin padding.
    """

    coincidencia = _VERSION_BETA_REVISION_V2_PATTERN.fullmatch(version)
    if coincidencia is None:
        return None

    revision_global = int(coincidencia.group(1))
    edition = int(coincidencia.group(2))
    correction = int(coincidencia.group(3))

    if revision_global < 128:
        return None
    if not 1 <= edition <= 99:
        return None
    if not 0 <= correction <= 999:
        return None

    return revision_global, edition, correction


def descomponer_version_beta_revision(
    version: str,
) -> tuple[int, int] | None:
    """Devuelve ``(Global, Edition)`` para revision-aware v1 o v2."""

    detalles_v2 = descomponer_version_beta_revision_v2(version)
    if detalles_v2 is not None:
        return detalles_v2[0], detalles_v2[1]

    coincidencia = _VERSION_BETA_REVISION_V1_PATTERN.fullmatch(version)
    if coincidencia is None:
        return None

    revision_global = _global_desde_fragmentos(
        coincidencia.group(1),
        coincidencia.group(2),
    )
    edition = int(coincidencia.group(3))

    if revision_global <= 0 or edition <= 0:
        return None

    return revision_global, edition


def construir_version_beta_revision(
    revision_global: int,
    revision_bloque: int,
) -> str:
    """Construye una versión revision-aware v1 histórica/canónica."""

    if revision_global <= 0:
        raise ValueError("La revisión global debe ser mayor que cero.")
    if not 1 <= revision_bloque <= 99:
        raise ValueError("La revisión del bloque debe estar entre 1 y 99.")

    grupo, resto = divmod(revision_global, 100)
    return f"0.{grupo}.{resto:02d}.{revision_bloque:02d}-beta"


def construir_version_beta_revision_v2(
    revision_global: int,
    edition: int,
    correction: int = 0,
) -> str:
    """Construye ``0.<GLOBAL>.<EDITION>.<CORRECTION>-beta``.

    La familia v2 comienza en G128. El ordinal de mantenimiento de dependencias y la
    revisión funcional no se codifican en VERSION: permanecen como metadata.
    """

    if revision_global < 128:
        raise ValueError("La familia revision-aware v2 comienza en G128.")
    if not 1 <= edition <= 99:
        raise ValueError("La Edition debe estar entre 1 y 99.")
    if not 0 <= correction <= 999:
        raise ValueError("La corrección material debe estar entre 0 y 999.")

    return f"0.{revision_global}.{edition}.{correction}-beta"


def version_valida(version: str) -> bool:
    """Indica si el identificador pertenece a una familia admitida."""

    return bool(
        _VERSION_BETA_LEGACY_PATTERN.fullmatch(version)
        or descomponer_version_beta_revision(version) is not None
        or _VERSION_OFICIAL_PATTERN.fullmatch(version)
    )


def leer_version() -> str:
    """Lee y valida la versión declarada en la raíz del proyecto."""

    try:
        version = VERSION_FILE.read_text(encoding="utf-8").strip()
    except OSError as error:
        raise RuntimeError(
            "No se pudo leer la versión canónica en " + str(VERSION_FILE) + "."
        ) from error

    if not version_valida(version):
        raise RuntimeError(
            "El archivo VERSION no contiene un identificador de versión válido: "
            + repr(version)
            + "."
        )

    return version


APP_VERSION = leer_version()
