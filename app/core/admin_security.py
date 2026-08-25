"""Controles de seguridad administrativa de Mi Retiro Proyectado.

Centraliza la protección de superficies internas o administrativas.
"""

from __future__ import annotations

import os
import secrets

ENV_ADMIN_TOKEN = "MRP_ADMIN_TOKEN"


def obtener_token_administrativo() -> str | None:
    """Obtiene el token administrativo desde variables de entorno."""

    token = os.getenv(ENV_ADMIN_TOKEN, "").strip()
    return token or None


def autenticacion_admin_habilitada() -> bool:
    """Indica si existe protección administrativa configurada."""

    return obtener_token_administrativo() is not None


def validar_token_administrativo(token_recibido: str | None) -> bool:
    """Valida un token sin realizar comparaciones inseguras."""

    token_real = obtener_token_administrativo()

    if not token_real or not token_recibido:
        return False

    return secrets.compare_digest(token_real, token_recibido)
