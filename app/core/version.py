"""Versión canónica de Mi Retiro Proyectado.

La fuente única es el archivo ``VERSION`` situado en la raíz del repositorio.
Este módulo valida y expone su contenido para que FastAPI, las plantillas y
otros componentes no mantengan copias independientes del número de versión.

Durante la etapa beta se acepta ``0.0.N-beta``. La línea oficial futura usa
cuatro componentes ``MAYOR.MENOR.PARCHE.REVISIÓN``. El identificador de Build
es independiente y no forma parte de ``VERSION``.
"""

from pathlib import Path
import re


VERSION_FILE = Path(__file__).resolve().parents[2] / "VERSION"

_VERSION_BETA_PATTERN = re.compile(r"^0\.0\.[1-9][0-9]*-beta$")
_VERSION_OFICIAL_PATTERN = re.compile(
    r"^[1-9][0-9]*\.[0-9]+\.[0-9]+\.[0-9]+$"
)


def version_valida(version: str) -> bool:
    """Indica si el identificador pertenece a una familia admitida."""

    return bool(
        _VERSION_BETA_PATTERN.fullmatch(version)
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
