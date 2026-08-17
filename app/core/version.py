"""Versión canónica de Mi Retiro Proyectado.

La fuente única es el archivo ``VERSION`` situado en la raíz del repositorio.
Este módulo valida y expone su contenido para que FastAPI, las plantillas y
otros componentes no mantengan copias independientes del número de versión.
"""

from pathlib import Path
import re


VERSION_FILE = Path(__file__).resolve().parents[2] / "VERSION"
_VERSION_PATTERN = re.compile(
    r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)


def leer_version() -> str:
    """Lee y valida la versión declarada en la raíz del proyecto."""

    try:
        version = VERSION_FILE.read_text(encoding="utf-8").strip()
    except OSError as error:
        raise RuntimeError(
            f"No se pudo leer la versión canónica en {VERSION_FILE}."
        ) from error

    if not _VERSION_PATTERN.fullmatch(version):
        raise RuntimeError(
            "El archivo VERSION no contiene un identificador de versión válido: "
            f"{version!r}."
        )

    return version


APP_VERSION = leer_version()
