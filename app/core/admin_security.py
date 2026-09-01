"""Seguridad administrativa centralizada y auditable."""

from __future__ import annotations

import os
import secrets
from typing import Optional

from fastapi import HTTPException, Request
from app.core.observability import registrar_evento


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


def validar_token_administrativo(token: Optional[str] = None) -> bool:
    """Valida un token administrativo contra el secreto configurado.

    Utiliza comparación segura para evitar ataques de comparación
    temporal.
    """

    secreto = obtener_secreto_admin()

    if not secreto:
        return False

    if token is None:
        return False

    return secrets.compare_digest(str(token), secreto)


def extraer_token_bearer(request: Request) -> Optional[str]:
    """Extrae el token Bearer enviado en la cabecera Authorization.

    Retorna None cuando la solicitud no contiene una credencial
    administrativa con formato válido.
    """

    authorization = request.headers.get("Authorization", "")

    if not authorization.startswith("Bearer "):
        return None

    return authorization.removeprefix("Bearer ").strip()


def requerir_administrador(request: Request) -> None:
    """Exige autenticación administrativa válida y audita el acceso.

    Registra intentos administrativos permitidos o bloqueados sin almacenar
    credenciales, tokens ni información sensible.
    """

    endpoint = request.url.path

    if not administracion_activa():
        registrar_evento(
            level="WARNING",
            event="admin.access.blocked",
            component="security.admin",
            outcome="blocked",
            metadata={
                "reason": "administration_disabled",
                "endpoint": endpoint,
            },
        )

        raise HTTPException(
            status_code=403,
            detail="Superficie administrativa no disponible.",
        )

    if not autenticacion_admin_habilitada():
        registrar_evento(
            level="WARNING",
            event="admin.access.blocked",
            component="security.admin",
            outcome="blocked",
            metadata={
                "reason": "authentication_not_configured",
                "endpoint": endpoint,
            },
        )

        raise HTTPException(
            status_code=403,
            detail="Autenticación administrativa no configurada.",
        )

    token = extraer_token_bearer(request)

    if not validar_token_administrativo(token):
        registrar_evento(
            level="WARNING",
            event="admin.access.denied",
            component="security.admin",
            outcome="denied",
            metadata={
                "reason": (
                    "missing_token"
                    if token is None
                    else "invalid_token"
                ),
                "endpoint": endpoint,
            },
        )

        raise HTTPException(
            status_code=401 if token is None else 403,
            detail="Autenticación administrativa requerida.",
        )

    registrar_evento(
        level="INFO",
        event="admin.access.granted",
        component="security.admin",
        outcome="allowed",
        metadata={
            "endpoint": endpoint,
        },
    )


# Compatibilidad con versiones anteriores
validar_token_admin = validar_token_administrativo
validar_request_administrativo = requerir_administrador
