"""DEV.2 R6 — Persistencia local de identidades del Portal Developer."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
import os
from pathlib import Path
import sqlite3
import uuid

from app.core.developer_identity import (
    RolDeveloper,
    normalizar_nombre_visible,
    normalizar_usuario,
    rol_puede_asignar,
)


_REPO_ROOT = Path(__file__).resolve().parents[2]
_RUTA_PREDETERMINADA = (
    _REPO_ROOT
    / "data"
    / "developer"
    / "portal.sqlite3"
)


@dataclass(frozen=True, slots=True)
class UsuarioDeveloper:
    """Representación interna de una cuenta Developer."""

    identificador: str
    usuario: str
    nombre_visible: str
    rol: RolDeveloper
    password_hash: str = field(repr=False)
    revision_seguridad: int = 1
    activo: bool = True
    debe_cambiar_password: bool = False
    es_propietario: bool = False
    recovery_code_hash: str | None = field(
        default=None,
        repr=False,
    )
    avatar_relativo: str | None = None
    creado_utc: str = ""
    actualizado_utc: str = ""
    ultimo_acceso_utc: str | None = None


def ruta_almacen_developer(
    ruta: str | Path | None = None,
) -> Path:
    """Resuelve la ubicación local de la base administrativa."""

    if ruta is not None:
        candidata = Path(ruta).expanduser()
    else:
        valor_entorno = os.getenv(
            "MRP_DEVELOPER_STORE_PATH",
            "",
        ).strip()

        candidata = (
            Path(valor_entorno).expanduser()
            if valor_entorno
            else _RUTA_PREDETERMINADA
        )

    if not candidata.is_absolute():
        candidata = _REPO_ROOT / candidata

    return candidata.resolve()


def _ahora_utc() -> str:
    """Genera una marca temporal UTC estable."""

    return datetime.now(timezone.utc).isoformat()


def _validar_hash_argon2id(valor: str, nombre: str) -> str:
    """Impide persistir secretos o hashes de formato inesperado."""

    if (
        not isinstance(valor, str)
        or not valor.startswith("$argon2id$")
    ):
        raise ValueError(
            f"{nombre} debe ser un hash Argon2id válido."
        )

    return valor


@contextmanager
def _conectar(
    ruta: str | Path | None = None,
) -> Iterator[sqlite3.Connection]:
    """Abre y cierra de forma segura la base administrativa."""

    destino = ruta_almacen_developer(ruta)
    destino.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    conexion = sqlite3.connect(
        destino,
        timeout=5,
    )
    conexion.row_factory = sqlite3.Row

    try:
        conexion.execute("PRAGMA foreign_keys = ON")
        conexion.execute("PRAGMA busy_timeout = 5000")

        yield conexion

        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()


_ESQUEMA = """
CREATE TABLE IF NOT EXISTS developer_users (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL COLLATE NOCASE UNIQUE,
    display_name TEXT NOT NULL,
    role TEXT NOT NULL
        CHECK (
            role IN (
                'owner',
                'admin',
                'operator',
                'auditor'
            )
        ),
    password_hash TEXT NOT NULL
        CHECK (password_hash LIKE '$argon2id$%'),
    recovery_code_hash TEXT
        CHECK (
            recovery_code_hash IS NULL
            OR recovery_code_hash LIKE '$argon2id$%'
        ),
    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),
    must_change_password INTEGER NOT NULL DEFAULT 0
        CHECK (must_change_password IN (0, 1)),
    security_version INTEGER NOT NULL DEFAULT 1
        CHECK (security_version >= 1),
    is_owner INTEGER NOT NULL DEFAULT 0
        CHECK (is_owner IN (0, 1)),
    avatar_path TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    last_login_at TEXT,

    CHECK (
        (
            is_owner = 1
            AND role = 'owner'
            AND recovery_code_hash IS NOT NULL
        )
        OR
        (
            is_owner = 0
            AND role <> 'owner'
            AND recovery_code_hash IS NULL
        )
    )
);

CREATE UNIQUE INDEX IF NOT EXISTS
    ux_developer_single_owner
ON developer_users(is_owner)
WHERE is_owner = 1;

CREATE TRIGGER IF NOT EXISTS
    trg_developer_owner_no_delete
BEFORE DELETE ON developer_users
FOR EACH ROW
WHEN OLD.is_owner = 1
BEGIN
    SELECT RAISE(
        ABORT,
        'owner_protected'
    );
END;

CREATE TRIGGER IF NOT EXISTS
    trg_developer_owner_identity_protected
BEFORE UPDATE OF
    id,
    role,
    is_active,
    is_owner
ON developer_users
FOR EACH ROW
WHEN
    OLD.is_owner = 1
    AND (
        NEW.id <> OLD.id
        OR NEW.role <> 'owner'
        OR NEW.is_active <> 1
        OR NEW.is_owner <> 1
    )
BEGIN
    SELECT RAISE(
        ABORT,
        'owner_protected'
    );
END;

CREATE TRIGGER IF NOT EXISTS
    trg_developer_no_owner_promotion
BEFORE UPDATE OF
    role,
    is_owner
ON developer_users
FOR EACH ROW
WHEN
    OLD.is_owner = 0
    AND (
        NEW.is_owner = 1
        OR NEW.role = 'owner'
    )
BEGIN
    SELECT RAISE(
        ABORT,
        'owner_promotion_forbidden'
    );
END;
"""


def _migrar_esquema_developer(
    conexion: sqlite3.Connection,
) -> None:
    """Migra de forma aditiva bases Developer creadas por revisiones previas."""

    columnas = {
        fila["name"]
        for fila in conexion.execute(
            "PRAGMA table_info(developer_users)"
        ).fetchall()
    }

    if "security_version" not in columnas:
        conexion.execute(
            """
            ALTER TABLE developer_users
            ADD COLUMN security_version INTEGER NOT NULL
            DEFAULT 1 CHECK (security_version >= 1)
            """
        )


def inicializar_almacen_developer(
    ruta: str | Path | None = None,
) -> Path:
    """Crea idempotentemente el esquema administrativo."""

    destino = ruta_almacen_developer(ruta)

    with _conectar(destino) as conexion:
        conexion.executescript(_ESQUEMA)
        _migrar_esquema_developer(conexion)

    return destino


def _fila_a_usuario(
    fila: sqlite3.Row,
) -> UsuarioDeveloper:
    """Convierte una fila SQLite en un modelo interno."""

    return UsuarioDeveloper(
        identificador=fila["id"],
        usuario=fila["username"],
        nombre_visible=fila["display_name"],
        rol=RolDeveloper(fila["role"]),
        password_hash=fila["password_hash"],
        revision_seguridad=int(fila["security_version"]),
        recovery_code_hash=fila["recovery_code_hash"],
        activo=bool(fila["is_active"]),
        debe_cambiar_password=bool(
            fila["must_change_password"]
        ),
        es_propietario=bool(fila["is_owner"]),
        avatar_relativo=fila["avatar_path"],
        creado_utc=fila["created_at"],
        actualizado_utc=fila["updated_at"],
        ultimo_acceso_utc=fila["last_login_at"],
    )


def contar_propietarios(
    ruta: str | Path | None = None,
) -> int:
    """Cuenta las cuentas Propietario persistidas."""

    inicializar_almacen_developer(ruta)

    with _conectar(ruta) as conexion:
        fila = conexion.execute(
            """
            SELECT COUNT(*) AS total
            FROM developer_users
            WHERE is_owner = 1
            """
        ).fetchone()

    return int(fila["total"])


def obtener_usuario_por_id(
    identificador: str,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper | None:
    """Busca una cuenta por su identificador estable."""

    inicializar_almacen_developer(ruta)

    with _conectar(ruta) as conexion:
        fila = conexion.execute(
            """
            SELECT *
            FROM developer_users
            WHERE id = ?
            """,
            (identificador,),
        ).fetchone()

    return (
        _fila_a_usuario(fila)
        if fila is not None
        else None
    )


def obtener_usuario_por_login(
    usuario: str,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper | None:
    """Busca una cuenta usando el identificador de login normalizado."""

    try:
        login = normalizar_usuario(usuario)
    except ValueError:
        return None

    inicializar_almacen_developer(ruta)

    with _conectar(ruta) as conexion:
        fila = conexion.execute(
            """
            SELECT *
            FROM developer_users
            WHERE username = ?
            """,
            (login,),
        ).fetchone()

    return (
        _fila_a_usuario(fila)
        if fila is not None
        else None
    )


def crear_propietario(
    *,
    usuario: str,
    nombre_visible: str,
    password_hash: str,
    recovery_code_hash: str,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper:
    """Crea la única cuenta Propietario permitida."""

    inicializar_almacen_developer(ruta)

    if contar_propietarios(ruta) != 0:
        raise ValueError(
            "Ya existe una cuenta Propietario."
        )

    login = normalizar_usuario(usuario)
    nombre = normalizar_nombre_visible(
        nombre_visible
    )
    password_hash = _validar_hash_argon2id(
        password_hash,
        "password_hash",
    )
    recovery_code_hash = _validar_hash_argon2id(
        recovery_code_hash,
        "recovery_code_hash",
    )

    identificador = uuid.uuid4().hex
    ahora = _ahora_utc()

    try:
        with _conectar(ruta) as conexion:
            conexion.execute(
                """
                INSERT INTO developer_users (
                    id,
                    username,
                    display_name,
                    role,
                    password_hash,
                    recovery_code_hash,
                    is_active,
                    must_change_password,
                    is_owner,
                    avatar_path,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, 1, 0, 1, NULL, ?, ?)
                """,
                (
                    identificador,
                    login,
                    nombre,
                    RolDeveloper.PROPIETARIO.value,
                    password_hash,
                    recovery_code_hash,
                    ahora,
                    ahora,
                ),
            )
    except sqlite3.IntegrityError as error:
        raise ValueError(
            "No fue posible crear la cuenta Propietario."
        ) from error

    propietario = obtener_usuario_por_id(
        identificador,
        ruta,
    )

    if propietario is None:
        raise RuntimeError(
            "La cuenta Propietario no pudo recuperarse."
        )

    return propietario


def crear_usuario_developer(
    *,
    actor_rol: RolDeveloper | str,
    usuario: str,
    nombre_visible: str,
    rol: RolDeveloper | str,
    password_hash: str,
    debe_cambiar_password: bool = True,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper:
    """Crea una cuenta respetando la jerarquía de roles."""

    rol_destino = RolDeveloper(rol)

    if not rol_puede_asignar(
        actor_rol,
        rol_destino,
    ):
        raise PermissionError(
            "El actor no puede asignar el rol solicitado."
        )

    if rol_destino is RolDeveloper.PROPIETARIO:
        raise PermissionError(
            "La cuenta Propietario solo puede crearse mediante bootstrap."
        )

    login = normalizar_usuario(usuario)
    nombre = normalizar_nombre_visible(
        nombre_visible
    )
    password_hash = _validar_hash_argon2id(
        password_hash,
        "password_hash",
    )

    inicializar_almacen_developer(ruta)

    identificador = uuid.uuid4().hex
    ahora = _ahora_utc()

    try:
        with _conectar(ruta) as conexion:
            conexion.execute(
                """
                INSERT INTO developer_users (
                    id,
                    username,
                    display_name,
                    role,
                    password_hash,
                    recovery_code_hash,
                    is_active,
                    must_change_password,
                    is_owner,
                    avatar_path,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, NULL, 1, ?, 0, NULL, ?, ?)
                """,
                (
                    identificador,
                    login,
                    nombre,
                    rol_destino.value,
                    password_hash,
                    int(bool(debe_cambiar_password)),
                    ahora,
                    ahora,
                ),
            )
    except sqlite3.IntegrityError as error:
        raise ValueError(
            "No fue posible crear la cuenta Developer."
        ) from error

    creado = obtener_usuario_por_id(
        identificador,
        ruta,
    )

    if creado is None:
        raise RuntimeError(
            "La cuenta Developer no pudo recuperarse."
        )

    return creado


def cambiar_rol_usuario(
    *,
    actor_rol: RolDeveloper | str,
    identificador: str,
    nuevo_rol: RolDeveloper | str,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper:
    """Cambia un rol sin permitir escaladas o alteración del Propietario."""

    actor = RolDeveloper(actor_rol)
    destino = RolDeveloper(nuevo_rol)

    usuario = obtener_usuario_por_id(
        identificador,
        ruta,
    )

    if usuario is None:
        raise LookupError(
            "La cuenta Developer no existe."
        )

    if usuario.es_propietario:
        raise PermissionError(
            "La cuenta Propietario está protegida."
        )

    if (
        usuario.rol is RolDeveloper.ADMINISTRADOR
        and actor is not RolDeveloper.PROPIETARIO
    ):
        raise PermissionError(
            "Solo el Propietario puede modificar a un Administrador."
        )

    if not rol_puede_asignar(
        actor,
        destino,
    ):
        raise PermissionError(
            "El actor no puede asignar el rol solicitado."
        )

    ahora = _ahora_utc()

    with _conectar(ruta) as conexion:
        conexion.execute(
            """
            UPDATE developer_users
            SET
                role = ?,
                security_version = security_version + 1,
                updated_at = ?
            WHERE id = ?
            """,
            (
                destino.value,
                ahora,
                identificador,
            ),
        )

    actualizado = obtener_usuario_por_id(
        identificador,
        ruta,
    )

    if actualizado is None:
        raise RuntimeError(
            "La cuenta actualizada no pudo recuperarse."
        )

    return actualizado



def obtener_propietario(
    ruta: str | Path | None = None,
) -> UsuarioDeveloper | None:
    """Obtiene la única cuenta Propietario, si existe."""

    inicializar_almacen_developer(ruta)

    with _conectar(ruta) as conexion:
        fila = conexion.execute(
            """
            SELECT *
            FROM developer_users
            WHERE is_owner = 1
            """
        ).fetchone()

    return (
        _fila_a_usuario(fila)
        if fila is not None
        else None
    )


def actualizar_password_usuario(
    *,
    identificador: str,
    password_hash: str,
    debe_cambiar_password: bool,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper:
    """Actualiza una contraseña ordinaria; nunca la del Propietario."""

    usuario = obtener_usuario_por_id(
        identificador,
        ruta,
    )

    if usuario is None:
        raise LookupError(
            "La cuenta Developer no existe."
        )

    if usuario.es_propietario:
        raise PermissionError(
            "La contraseña del Propietario no puede restablecerse "
            "por el procedimiento ordinario."
        )

    password_hash = _validar_hash_argon2id(
        password_hash,
        "password_hash",
    )
    ahora = _ahora_utc()

    with _conectar(ruta) as conexion:
        conexion.execute(
            """
            UPDATE developer_users
            SET
                password_hash = ?,
                must_change_password = ?,
                security_version = security_version + 1,
                updated_at = ?
            WHERE id = ?
            """,
            (
                password_hash,
                int(bool(debe_cambiar_password)),
                ahora,
                identificador,
            ),
        )

    actualizado = obtener_usuario_por_id(
        identificador,
        ruta,
    )

    if actualizado is None:
        raise RuntimeError(
            "La cuenta actualizada no pudo recuperarse."
        )

    return actualizado


def rotar_credenciales_propietario(
    *,
    identificador: str,
    recovery_hash_esperado: str,
    nuevo_password_hash: str,
    nuevo_recovery_hash: str,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper:
    """Rota atómicamente contraseña y recuperación del Propietario."""

    nuevo_password_hash = _validar_hash_argon2id(
        nuevo_password_hash,
        "nuevo_password_hash",
    )
    nuevo_recovery_hash = _validar_hash_argon2id(
        nuevo_recovery_hash,
        "nuevo_recovery_hash",
    )
    recovery_hash_esperado = _validar_hash_argon2id(
        recovery_hash_esperado,
        "recovery_hash_esperado",
    )

    ahora = _ahora_utc()

    with _conectar(ruta) as conexion:
        cursor = conexion.execute(
            """
            UPDATE developer_users
            SET
                password_hash = ?,
                recovery_code_hash = ?,
                must_change_password = 0,
                security_version = security_version + 1,
                updated_at = ?
            WHERE
                id = ?
                AND is_owner = 1
                AND recovery_code_hash = ?
            """,
            (
                nuevo_password_hash,
                nuevo_recovery_hash,
                ahora,
                identificador,
                recovery_hash_esperado,
            ),
        )

        if cursor.rowcount != 1:
            raise PermissionError(
                "La recuperación del Propietario no pudo completarse."
            )

    actualizado = obtener_usuario_por_id(
        identificador,
        ruta,
    )

    if actualizado is None:
        raise RuntimeError(
            "La cuenta Propietario no pudo recuperarse."
        )

    return actualizado
