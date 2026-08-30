"""Seguridad de operaciones humanas del Portal Developer."""

from __future__ import annotations

import hashlib
import hmac
import secrets

from app.core.developer_identity import verificar_password
from app.core.developer_store import UsuarioDeveloper


_CSRF_SECRET = secrets.token_bytes(32)


def token_csrf_para_sesion(
    identificador_sesion: str,
) -> str:
    """Genera un token CSRF ligado a una sesión que ya vive solo en memoria."""

    sesion = str(identificador_sesion or "").strip()

    if not sesion:
        return ""

    return hmac.new(
        _CSRF_SECRET,
        sesion.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def validar_token_csrf_sesion(
    identificador_sesion: str,
    token_recibido: str | None,
) -> bool:
    """Valida un token CSRF sin comparaciones temporales inseguras."""

    esperado = token_csrf_para_sesion(
        identificador_sesion,
    )

    recibido = str(token_recibido or "").strip()

    if not esperado or not recibido:
        return False

    return hmac.compare_digest(
        esperado,
        recibido,
    )


def revalidar_password_usuario(
    usuario: UsuarioDeveloper,
    password: str | None,
) -> bool:
    """Revalida la contraseña humana de una identidad activa."""

    if not usuario.activo:
        return False

    if not password:
        return False

    return verificar_password(
        password,
        usuario.password_hash,
    )
