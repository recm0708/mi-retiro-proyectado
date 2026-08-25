"""SEC.2 R2 - Seguridad administrativa."""

from __future__ import annotations

import os
import secrets
from typing import Optional

from fastapi import HTTPException, Request


def obtener_secreto_admin() -> str:
    """Obtiene el secreto configurado para autenticación administrativa.

    Prioriza la variable de entorno MRP_ADMIN_SECRET y mantiene
    compatibilidad con MRP_ADMIN_TOKEN.
    """
    return (
        os.getenv("MRP_ADMIN_SECRET", "").strip()
        or os.getenv("MRP_ADMIN_TOKEN", "").strip()
    )


def autenticacion_admin_habilitada() -> bool:
    """Determina si existe un secreto administrativo configurado.

    Retorna True cuando la aplicación dispone de un secreto válido
    para realizar autenticación administrativa.
    """
    return bool(obtener_secreto_admin())


def administracion_activa() -> bool:
    """Verifica si la superficie administrativa está habilitada.

    La activación depende de la variable de entorno MRP_ADMIN_ENABLED.
    """
    return os.getenv("MRP_ADMIN_ENABLED", "").strip() == "1"


def validar_token_administrativo(token: Optional[str] = None):
    """
    Compatible con:
    - pruebas unitarias: validar_token_administrativo("abc123") -> True/False
    - endpoint FastAPI actual: recibe token extraído del header -> True/False
    """

    secreto = obtener_secreto_admin()

    if not secreto:
        return False

    if token is None:
        return False

    return secrets.compare_digest(str(token), secreto)


def validar_request_administrativo(request: Request) -> None:
    """
    Validador basado en Request para usos futuros con FastAPI.
    """
    if not administracion_activa():
        return

    authorization = request.headers.get("Authorization", "")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Credenciales administrativas requeridas.")

    token = authorization.replace("Bearer ", "", 1).strip()

    if not validar_token_administrativo(token):
        raise HTTPException(status_code=401, detail="Credenciales administrativas inválidas.")


# Compatibilidad
validar_token_admin = validar_token_administrativo
