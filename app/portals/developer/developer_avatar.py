"""Validación y almacenamiento persistente de avatares Developer."""

from __future__ import annotations

import os
from pathlib import Path
import secrets

from app.portals.developer.developer_store import (
    ruta_almacen_developer,
)


_REPO_ROOT = Path(
    __file__
).resolve().parents[3]

_ENV_MEDIA_DIR = "MRP_DEVELOPER_MEDIA_DIR"

MAX_AVATAR_BYTES = (
    8
    * 1024
    * 1024
)


def detectar_extension_avatar(
    contenido: bytes,
) -> str:
    """Identifica formatos web seguros mediante su firma binaria."""

    if contenido.startswith(
        b"\x89PNG\r\n\x1a\n"
    ):
        return ".png"

    if contenido.startswith(
        b"\xff\xd8\xff"
    ):
        return ".jpg"

    if (
        len(contenido) >= 12
        and contenido[:4] == b"RIFF"
        and contenido[8:12] == b"WEBP"
    ):
        return ".webp"

    raise ValueError(
        "La foto debe ser PNG, JPEG o WebP."
    )


def ruta_media_developer(
    ruta_almacen: str | Path | None = None,
) -> Path:
    """Resuelve la raíz persistente de medios Developer."""

    configurada = os.getenv(
        _ENV_MEDIA_DIR,
        "",
    ).strip()

    if configurada:
        candidata = Path(
            configurada
        ).expanduser()

        if not candidata.is_absolute():
            candidata = (
                _REPO_ROOT
                / candidata
            )

        return candidata.resolve()

    return (
        ruta_almacen_developer(
            ruta_almacen
        ).parent
        / "media"
    ).resolve()


def directorio_avatares_developer(
    ruta_almacen: str | Path | None = None,
) -> Path:
    """Devuelve el directorio persistente de avatares."""

    return (
        ruta_media_developer(
            ruta_almacen
        )
        / "avatars"
    ).resolve()


def guardar_avatar_developer(
    *,
    identificador: str,
    contenido: bytes,
    ruta_almacen: str | Path | None = None,
) -> str:
    """Guarda una imagen validada y devuelve su referencia relativa."""

    if not contenido:
        raise ValueError(
            "La foto seleccionada está vacía."
        )

    if (
        len(contenido)
        > MAX_AVATAR_BYTES
    ):
        raise ValueError(
            "La foto no puede superar 8 MiB."
        )

    extension = detectar_extension_avatar(
        contenido
    )

    usuario = str(
        identificador
    ).strip()

    if (
        not usuario
        or any(
            not (
                caracter.isalnum()
                or caracter in "-_"
            )
            for caracter in usuario
        )
    ):
        raise ValueError(
            "Identificador de usuario inválido."
        )

    directorio = (
        directorio_avatares_developer(
            ruta_almacen
        )
    )

    directorio.mkdir(
        parents=True,
        exist_ok=True,
    )

    nombre = (
        f"{usuario}-"
        f"{secrets.token_hex(8)}"
        f"{extension}"
    )

    destino = (
        directorio
        / nombre
    ).resolve()

    if destino.parent != directorio:
        raise ValueError(
            "Ruta de avatar inválida."
        )

    destino.write_bytes(
        contenido
    )

    return (
        Path("avatars")
        / nombre
    ).as_posix()


def resolver_avatar_developer(
    referencia: str | None,
    ruta_almacen: str | Path | None = None,
) -> Path | None:
    """Resuelve una referencia persistida sin permitir path traversal."""

    valor = str(
        referencia or ""
    ).strip()

    if not valor:
        return None

    relativa = Path(
        valor
    )

    if (
        relativa.is_absolute()
        or ".." in relativa.parts
        or len(relativa.parts) != 2
        or relativa.parts[0] != "avatars"
    ):
        return None

    directorio = (
        directorio_avatares_developer(
            ruta_almacen
        )
    )

    destino = (
        ruta_media_developer(
            ruta_almacen
        )
        / relativa
    ).resolve()

    if destino.parent != directorio:
        return None

    return destino


def eliminar_avatar_developer(
    referencia: str | None,
    ruta_almacen: str | Path | None = None,
) -> None:
    """Elimina una imagen de perfil válida si todavía existe."""

    destino = resolver_avatar_developer(
        referencia,
        ruta_almacen,
    )

    if (
        destino is not None
        and destino.is_file()
    ):
        destino.unlink()
