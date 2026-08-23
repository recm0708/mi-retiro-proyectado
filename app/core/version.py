"""Versión canónica de Mi Retiro Proyectado.

La fuente única es el archivo ``VERSION`` situado en la raíz del repositorio.
Este módulo valida y expone su contenido para que FastAPI, las plantillas y
otros componentes no mantengan copias independientes del número de versión.

La historia conserva la familia legacy ``0.0.N-beta``. VER.2 incorpora una
familia beta revision-aware ``0.GG.RR.EE-beta`` para estados nuevos, donde
``GG``/``RR`` codifican el contador global y ``EE`` el ordinal aceptado dentro
del bloque. La línea oficial futura conserva cuatro componentes
``MAYOR.MENOR.PARCHE.REVISIÓN`` sin sufijo. El Build es independiente.
"""

from pathlib import Path
import re


VERSION_FILE = Path(__file__).resolve().parents[2] / "VERSION"

_VERSION_BETA_LEGACY_PATTERN = re.compile(r"^0\.0\.[1-9][0-9]*-beta$")
_VERSION_BETA_REVISION_PATTERN = re.compile(
    r"^0\.(0|[1-9][0-9]*)\.([0-9]{2})\.([0-9]{2})-beta$"
)
_VERSION_OFICIAL_PATTERN = re.compile(
    r"^[1-9][0-9]*\.[0-9]+\.[0-9]+\.[0-9]+$"
)


def descomponer_version_beta_revision(version: str) -> tuple[int, int] | None:
    """Devuelve ``(revision_global, revision_bloque)`` para la beta nueva.

    ``None`` indica que ``version`` no pertenece a la familia revision-aware o
    que intenta representar la revisión global/local cero, que se reservan
    como origen conceptual y no como estados publicables.
    """

    coincidencia = _VERSION_BETA_REVISION_PATTERN.fullmatch(version)
    if coincidencia is None:
        return None

    grupo = int(coincidencia.group(1))
    resto = int(coincidencia.group(2))
    revision_bloque = int(coincidencia.group(3))
    revision_global = grupo * 100 + resto

    if revision_global <= 0 or revision_bloque <= 0:
        return None

    return revision_global, revision_bloque


def construir_version_beta_revision(
    revision_global: int,
    revision_bloque: int,
) -> str:
    """Construye una versión beta revision-aware canónica.

    El ordinal local se limita a dos dígitos. Si un bloque llegara a necesitar
    más de 99 estados aceptados, la política de versionado debe revisarse antes
    de continuar en lugar de emitir un identificador ambiguo.
    """

    if revision_global <= 0:
        raise ValueError("La revisión global debe ser mayor que cero.")
    if not 1 <= revision_bloque <= 99:
        raise ValueError("La revisión del bloque debe estar entre 1 y 99.")

    grupo, resto = divmod(revision_global, 100)
    return f"0.{grupo}.{resto:02d}.{revision_bloque:02d}-beta"


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
            f"No se pudo leer la versión canónica en {VERSION_FILE}."
        ) from error

    if not version_valida(version):
        raise RuntimeError(
            "El archivo VERSION no contiene un identificador de versión válido: "
            f"{version!r}."
        )

    return version


APP_VERSION = leer_version()
