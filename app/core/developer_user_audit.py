"""Auditoría persistente de la gestión de cuentas del Portal Developer."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
import uuid

from app.core.developer_identity import RolDeveloper
from app.core.developer_store import (
    UsuarioDeveloper,
    inicializar_almacen_developer,
    ruta_almacen_developer,
)


@dataclass(frozen=True, slots=True)
class EventoAuditoriaUsuario:
    """Representa un evento persistente e inmutable de auditoría administrativa."""
    identificador: str
    timestamp_utc: str
    accion: str
    accion_etiqueta: str
    actor_id: str
    actor_usuario: str
    actor_rol: str
    objetivo_id: str
    objetivo_usuario: str
    objetivo_rol: str
    resumen: str


_SCHEMA = """
CREATE TABLE IF NOT EXISTS developer_user_audit (
    id TEXT PRIMARY KEY,
    timestamp_utc TEXT NOT NULL,
    action TEXT NOT NULL,
    actor_id TEXT NOT NULL,
    actor_username TEXT NOT NULL,
    actor_role TEXT NOT NULL,
    target_id TEXT NOT NULL,
    target_username TEXT NOT NULL,
    target_role TEXT NOT NULL,
    summary TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS
    ix_developer_user_audit_timestamp
ON developer_user_audit(timestamp_utc DESC);

CREATE INDEX IF NOT EXISTS
    ix_developer_user_audit_target
ON developer_user_audit(target_id, timestamp_utc DESC);

CREATE TRIGGER IF NOT EXISTS
    trg_developer_user_audit_no_update
BEFORE UPDATE ON developer_user_audit
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'developer_user_audit_append_only');
END;

CREATE TRIGGER IF NOT EXISTS
    trg_developer_user_audit_no_delete
BEFORE DELETE ON developer_user_audit
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'developer_user_audit_append_only');
END;
"""

_ETIQUETAS_ACCION = {
    "user.created": "Usuario creado",
    "user.display_name.updated": "Nombre actualizado",
    "user.role.changed": "Rol modificado",
    "user.disabled": "Usuario desactivado",
    "user.reactivated": "Usuario reactivado",
    "user.password.reset": "Contraseña restablecida",
    "user.deleted": "Usuario eliminado",
}

_ETIQUETAS_ROL = {
    RolDeveloper.PROPIETARIO: "Propietario",
    RolDeveloper.ADMINISTRADOR: "Administrador",
    RolDeveloper.OPERADOR: "Operador",
    RolDeveloper.AUDITOR: "Auditor",
}


def etiqueta_rol_auditoria(
    rol: RolDeveloper | str,
) -> str:
    """Devuelve la etiqueta legible de un rol almacenado en auditoría."""
    return _ETIQUETAS_ROL[
        RolDeveloper(rol)
    ]


def _conectar_auditoria(
    ruta: str | Path | None = None,
) -> sqlite3.Connection:
    """Abre y prepara la conexión SQLite usada por el ledger de auditoría."""
    inicializar_almacen_developer(ruta)

    conexion = sqlite3.connect(
        ruta_almacen_developer(ruta),
        timeout=5,
    )
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    conexion.execute("PRAGMA busy_timeout = 5000")
    conexion.executescript(_SCHEMA)
    return conexion


def registrar_auditoria_usuario_developer(
    *,
    actor: UsuarioDeveloper,
    objetivo: UsuarioDeveloper,
    accion: str,
    resumen: str,
    ruta: str | Path | None = None,
) -> EventoAuditoriaUsuario:
    """Registra un evento administrativo append-only sin incluir secretos."""
    accion_normalizada = str(accion).strip()

    if accion_normalizada not in _ETIQUETAS_ACCION:
        raise ValueError(
            "Acción de auditoría Developer no reconocida."
        )

    resumen_normalizado = " ".join(
        str(resumen).strip().split()
    )

    if not resumen_normalizado:
        raise ValueError(
            "El resumen de auditoría es obligatorio."
        )

    if len(resumen_normalizado) > 240:
        raise ValueError(
            "El resumen de auditoría excede 240 caracteres."
        )

    evento = EventoAuditoriaUsuario(
        identificador=uuid.uuid4().hex,
        timestamp_utc=datetime.now(
            timezone.utc
        ).isoformat(timespec="milliseconds"),
        accion=accion_normalizada,
        accion_etiqueta=_ETIQUETAS_ACCION[
            accion_normalizada
        ],
        actor_id=actor.identificador,
        actor_usuario=actor.usuario,
        actor_rol=actor.rol.value,
        objetivo_id=objetivo.identificador,
        objetivo_usuario=objetivo.usuario,
        objetivo_rol=objetivo.rol.value,
        resumen=resumen_normalizado,
    )

    conexion = _conectar_auditoria(ruta)

    try:
        conexion.execute(
            """
            INSERT INTO developer_user_audit (
                id,
                timestamp_utc,
                action,
                actor_id,
                actor_username,
                actor_role,
                target_id,
                target_username,
                target_role,
                summary
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                evento.identificador,
                evento.timestamp_utc,
                evento.accion,
                evento.actor_id,
                evento.actor_usuario,
                evento.actor_rol,
                evento.objetivo_id,
                evento.objetivo_usuario,
                evento.objetivo_rol,
                evento.resumen,
            ),
        )
        conexion.commit()
    finally:
        conexion.close()

    return evento


def listar_auditoria_usuarios_developer(
    *,
    limite: int = 200,
    ruta: str | Path | None = None,
) -> list[EventoAuditoriaUsuario]:
    """Lista los eventos persistentes de auditoría de usuarios en orden reciente."""
    limite_normalizado = max(
        1,
        min(int(limite), 500),
    )

    conexion = _conectar_auditoria(ruta)

    try:
        filas = conexion.execute(
            """
            SELECT
                id,
                timestamp_utc,
                action,
                actor_id,
                actor_username,
                actor_role,
                target_id,
                target_username,
                target_role,
                summary
            FROM developer_user_audit
            ORDER BY timestamp_utc DESC, id DESC
            LIMIT ?
            """,
            (limite_normalizado,),
        ).fetchall()
    finally:
        conexion.close()

    return [
        EventoAuditoriaUsuario(
            identificador=fila["id"],
            timestamp_utc=fila["timestamp_utc"],
            accion=fila["action"],
            accion_etiqueta=_ETIQUETAS_ACCION.get(
                fila["action"],
                fila["action"],
            ),
            actor_id=fila["actor_id"],
            actor_usuario=fila["actor_username"],
            actor_rol=fila["actor_role"],
            objetivo_id=fila["target_id"],
            objetivo_usuario=fila["target_username"],
            objetivo_rol=fila["target_role"],
            resumen=fila["summary"],
        )
        for fila in filas
    ]
