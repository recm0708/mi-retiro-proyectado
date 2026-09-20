"""Versión canónica de Mi Retiro Proyectado.

La fuente única es el archivo ``VERSION`` situado en la raíz del repositorio.
Este módulo valida y expone su contenido para que FastAPI, las plantillas y
otros componentes no mantengan copias independientes del número de versión.

Se preservan las familias históricas ``0.0.N-beta`` y
``0.<G_HI>.<G_LO>.<EE>-beta``.

La política de versionado introduce prospectivamente la familia revision-aware v2:

``0.<G_HI>.<G_LO>.<EE>.<CCC>.<DDD>-beta``

donde ``CCC`` representa la corrección material y ``DDD`` el ciclo material
de mantenimiento de dependencias. La línea estable conserva cuatro componentes
``MAYOR.MENOR.PARCHE.REVISIÓN`` sin sufijo. El Build es independiente.
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
    r"^0\.(0|[1-9][0-9]*)"
    r"\.([0-9]{2})"
    r"\.([0-9]{2})"
    r"\.([0-9]{3})"
    r"\.([0-9]{3})-beta$"
)

_VERSION_OFICIAL_PATTERN = re.compile(
    r"^[1-9][0-9]*\.[0-9]+\.[0-9]+\.[0-9]+$"
)


def _global_desde_fragmentos(
    grupo: str,
    resto: str,
) -> int:
    """Reconstruye el contador Global desde ``G_HI`` y ``G_LO``."""

    return int(grupo) * 100 + int(resto)


def descomponer_version_beta_revision_v2(
    version: str,
) -> tuple[int, int, int, int] | None:
    """Devuelve ``(Global, Edition, CCC, DDD)`` para revision-aware v2.

    ``None`` indica que el identificador no pertenece a la familia v2 o
    intenta representar Global/Edition cero.
    """

    coincidencia = _VERSION_BETA_REVISION_V2_PATTERN.fullmatch(
        version
    )

    if coincidencia is None:
        return None

    revision_global = _global_desde_fragmentos(
        coincidencia.group(1),
        coincidencia.group(2),
    )

    edition = int(
        coincidencia.group(3)
    )

    correction = int(
        coincidencia.group(4)
    )

    maintenance = int(
        coincidencia.group(5)
    )

    if revision_global <= 0 or edition <= 0:
        return None

    return (
        revision_global,
        edition,
        correction,
        maintenance,
    )


def descomponer_version_beta_revision(
    version: str,
) -> tuple[int, int] | None:
    """Devuelve ``(Global, Edition)`` para cualquier revision-aware.

    Mantiene el contrato histórico de dos valores. Para recuperar además
    ``CCC`` y ``DDD`` debe usarse
    :func:`descomponer_version_beta_revision_v2`.
    """

    coincidencia = _VERSION_BETA_REVISION_V1_PATTERN.fullmatch(
        version
    )

    if coincidencia is not None:
        revision_global = _global_desde_fragmentos(
            coincidencia.group(1),
            coincidencia.group(2),
        )

        edition = int(
            coincidencia.group(3)
        )

        if revision_global <= 0 or edition <= 0:
            return None

        return (
            revision_global,
            edition,
        )

    detalles_v2 = descomponer_version_beta_revision_v2(
        version
    )

    if detalles_v2 is None:
        return None

    return (
        detalles_v2[0],
        detalles_v2[1],
    )


def construir_version_beta_revision(
    revision_global: int,
    revision_bloque: int,
) -> str:
    """Construye una versión revision-aware v1 histórica/canónica."""

    if revision_global <= 0:
        raise ValueError(
            "La revisión global debe ser mayor que cero."
        )

    if not 1 <= revision_bloque <= 99:
        raise ValueError(
            "La revisión del bloque debe estar entre 1 y 99."
        )

    grupo, resto = divmod(
        revision_global,
        100,
    )

    return (
        f"0.{grupo}.{resto:02d}."
        f"{revision_bloque:02d}-beta"
    )


def construir_version_beta_revision_v2(
    revision_global: int,
    edition: int,
    correction: int = 0,
    maintenance: int = 0,
) -> str:
    """Construye una versión revision-aware v2.

    ``CCC`` y ``DDD`` son ordinales de tres dígitos y admiten ``000``.
    La semántica material de esos ordinales pertenece a la política de versionado;
    esta función valida únicamente su representación estructural.
    """

    if revision_global <= 0:
        raise ValueError(
            "La revisión global debe ser mayor que cero."
        )

    if not 1 <= edition <= 99:
        raise ValueError(
            "La Edition debe estar entre 1 y 99."
        )

    if not 0 <= correction <= 999:
        raise ValueError(
            "La corrección material debe estar entre 0 y 999."
        )

    if not 0 <= maintenance <= 999:
        raise ValueError(
            "El ordinal de mantenimiento debe estar entre 0 y 999."
        )

    grupo, resto = divmod(
        revision_global,
        100,
    )

    return (
        f"0.{grupo}.{resto:02d}."
        f"{edition:02d}."
        f"{correction:03d}."
        f"{maintenance:03d}-beta"
    )


def version_valida(
    version: str,
) -> bool:
    """Indica si el identificador pertenece a una familia admitida."""

    return bool(
        _VERSION_BETA_LEGACY_PATTERN.fullmatch(
            version
        )
        or descomponer_version_beta_revision(
            version
        )
        is not None
        or _VERSION_OFICIAL_PATTERN.fullmatch(
            version
        )
    )


def leer_version() -> str:
    """Lee y valida la versión declarada en la raíz del proyecto."""

    try:
        version = VERSION_FILE.read_text(
            encoding="utf-8"
        ).strip()
    except OSError as error:
        raise RuntimeError(
            "No se pudo leer la versión canónica en "
            f"{VERSION_FILE}."
        ) from error

    if not version_valida(
        version
    ):
        raise RuntimeError(
            "El archivo VERSION no contiene un "
            "identificador de versión válido: "
            f"{version!r}."
        )

    return version


APP_VERSION = leer_version()
