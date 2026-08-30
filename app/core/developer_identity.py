"""DEV.2 R6 — Identidad y autorización del Portal Developer."""

from __future__ import annotations

from enum import StrEnum
import re
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)


class RolDeveloper(StrEnum):
    """Roles predefinidos del Portal Developer."""

    PROPIETARIO = "owner"
    ADMINISTRADOR = "admin"
    OPERADOR = "operator"
    AUDITOR = "auditor"


class PermisoDeveloper(StrEnum):
    """Permisos atómicos utilizados por la autorización Developer."""

    PERFIL_LEER = "profile.read"
    PERFIL_EDITAR_PROPIO = "profile.edit.self"

    USUARIOS_LEER = "users.read"
    USUARIOS_CREAR = "users.create"
    USUARIOS_EDITAR = "users.edit"
    USUARIOS_DESACTIVAR = "users.disable"

    ROLES_ASIGNAR_BASICOS = "roles.assign.basic"
    ROLES_ASIGNAR_ADMIN = "roles.assign.admin"

    DIAGNOSTICO_LEER = "diagnostics.read"
    EVENTOS_LEER = "events.read"
    ARCHIVOS_LEER = "files.read"
    ARCHIVOS_DESCARGAR = "files.download"

    MANTENIMIENTO_LEER = "maintenance.read"
    MANTENIMIENTO_EJECUTAR = "maintenance.execute"
    MANTENIMIENTO_DESTRUCTIVO = "maintenance.destructive"

    PRIVACIDAD_LEER = "privacy.read"

    TOKENS_LEER = "tokens.read"
    TOKENS_GESTIONAR = "tokens.manage"

    SEGURIDAD_AUDITAR = "security.audit"
    PROPIETARIO_GESTIONAR = "owner.manage"


_PERMISOS_LECTURA = frozenset(
    {
        PermisoDeveloper.PERFIL_LEER,
        PermisoDeveloper.PERFIL_EDITAR_PROPIO,
        PermisoDeveloper.DIAGNOSTICO_LEER,
        PermisoDeveloper.EVENTOS_LEER,
        PermisoDeveloper.ARCHIVOS_LEER,
        PermisoDeveloper.PRIVACIDAD_LEER,
    }
)

_PERMISOS_OPERADOR = _PERMISOS_LECTURA | frozenset(
    {
        PermisoDeveloper.ARCHIVOS_DESCARGAR,
        PermisoDeveloper.MANTENIMIENTO_LEER,
        PermisoDeveloper.MANTENIMIENTO_EJECUTAR,
    }
)

_PERMISOS_ADMINISTRADOR = _PERMISOS_OPERADOR | frozenset(
    {
        PermisoDeveloper.USUARIOS_LEER,
        PermisoDeveloper.USUARIOS_CREAR,
        PermisoDeveloper.USUARIOS_EDITAR,
        PermisoDeveloper.USUARIOS_DESACTIVAR,
        PermisoDeveloper.ROLES_ASIGNAR_BASICOS,
        PermisoDeveloper.MANTENIMIENTO_DESTRUCTIVO,
        PermisoDeveloper.TOKENS_LEER,
        PermisoDeveloper.TOKENS_GESTIONAR,
        PermisoDeveloper.SEGURIDAD_AUDITAR,
    }
)

_PERMISOS_PROPIETARIO = frozenset(PermisoDeveloper)

PERMISOS_POR_ROL: dict[RolDeveloper, frozenset[PermisoDeveloper]] = {
    RolDeveloper.PROPIETARIO: _PERMISOS_PROPIETARIO,
    RolDeveloper.ADMINISTRADOR: _PERMISOS_ADMINISTRADOR,
    RolDeveloper.OPERADOR: _PERMISOS_OPERADOR,
    RolDeveloper.AUDITOR: _PERMISOS_LECTURA,
}


_USUARIO_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,63}$")
_LONGITUD_MINIMA_PASSWORD = 12
_LONGITUD_MAXIMA_PASSWORD = 256
_PREFIJO_RECUPERACION = "MRP-OWNER-RECOVERY-"

_PASSWORD_HASHER = PasswordHasher()


def normalizar_usuario(usuario: str) -> str:
    """Normaliza y valida un identificador de inicio de sesión."""

    normalizado = str(usuario).strip().casefold()

    if not _USUARIO_RE.fullmatch(normalizado):
        raise ValueError(
            "El usuario debe tener entre 3 y 64 caracteres y usar únicamente "
            "letras minúsculas, números, punto, guion o guion bajo."
        )

    return normalizado


def normalizar_nombre_visible(nombre: str) -> str:
    """Normaliza el nombre presentado en la interfaz."""

    normalizado = " ".join(str(nombre).strip().split())

    if not normalizado:
        raise ValueError("El nombre visible es obligatorio.")

    if len(normalizado) > 120:
        raise ValueError("El nombre visible no puede exceder 120 caracteres.")

    return normalizado


REGLAS_CREDENCIAL = (
    "al menos 12 caracteres",
    "al menos una letra mayúscula",
    "al menos un carácter especial",
    "máximo 256 caracteres",
)


def validar_password(password: str) -> str:
    """Aplica la política vigente a contraseñas nuevas o modificadas."""

    if not isinstance(password, str):
        raise TypeError("La contraseña debe ser texto.")

    errores: list[str] = []
    longitud = len(password)

    if longitud < _LONGITUD_MINIMA_PASSWORD:
        errores.append(
            f"debe tener al menos {_LONGITUD_MINIMA_PASSWORD} caracteres"
        )

    if longitud > _LONGITUD_MAXIMA_PASSWORD:
        errores.append(
            f"no puede exceder {_LONGITUD_MAXIMA_PASSWORD} caracteres"
        )

    if not any(caracter.isupper() for caracter in password):
        errores.append(
            "debe contener al menos una letra mayúscula"
        )

    if not any(
        not caracter.isalnum()
        and not caracter.isspace()
        for caracter in password
    ):
        errores.append(
            "debe contener al menos un carácter especial"
        )

    if errores:
        raise ValueError(
            "La contraseña no cumple la política: "
            + "; ".join(errores)
            + "."
        )

    return password


def hashear_password(password: str) -> str:
    """Genera un hash Argon2id de una contraseña válida."""

    return _PASSWORD_HASHER.hash(validar_password(password))


def verificar_password(password: str, password_hash: str) -> bool:
    """Verifica una contraseña sin revelar ni recuperar su valor original."""

    try:
        return bool(_PASSWORD_HASHER.verify(password_hash, password))
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def password_necesita_rehash(password_hash: str) -> bool:
    """Indica si un hash debe actualizarse a parámetros criptográficos vigentes."""

    try:
        return _PASSWORD_HASHER.check_needs_rehash(password_hash)
    except InvalidHashError:
        return True


def generar_codigo_recuperacion_propietario() -> str:
    """Genera un código aleatorio de recuperación para la cuenta Propietario."""

    return f"{_PREFIJO_RECUPERACION}{secrets.token_urlsafe(32)}"


def hashear_codigo_recuperacion(codigo: str) -> str:
    """Hash irreversible del código de recuperación del Propietario."""

    if not isinstance(codigo, str) or not codigo.startswith(_PREFIJO_RECUPERACION):
        raise ValueError("Código de recuperación inválido.")

    return _PASSWORD_HASHER.hash(codigo)


def verificar_codigo_recuperacion(codigo: str, codigo_hash: str) -> bool:
    """Valida un código de recuperación contra su hash almacenado."""

    if not isinstance(codigo, str):
        return False

    try:
        return bool(_PASSWORD_HASHER.verify(codigo_hash, codigo))
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def permisos_para_rol(
    rol: RolDeveloper | str,
) -> frozenset[PermisoDeveloper]:
    """Devuelve los permisos predefinidos de un rol."""

    rol_normalizado = RolDeveloper(rol)
    return PERMISOS_POR_ROL[rol_normalizado]


def rol_tiene_permiso(
    rol: RolDeveloper | str,
    permiso: PermisoDeveloper | str,
) -> bool:
    """Evalúa un permiso concreto usando denegación por defecto."""

    try:
        permiso_normalizado = PermisoDeveloper(permiso)
        rol_normalizado = RolDeveloper(rol)
    except ValueError:
        return False

    return permiso_normalizado in permisos_para_rol(rol_normalizado)


def rol_puede_asignar(
    actor: RolDeveloper | str,
    destino: RolDeveloper | str,
) -> bool:
    """Impide que roles inferiores otorguen privilegios equivalentes o mayores."""

    try:
        actor_normalizado = RolDeveloper(actor)
        destino_normalizado = RolDeveloper(destino)
    except ValueError:
        return False

    if destino_normalizado is RolDeveloper.PROPIETARIO:
        return False

    if destino_normalizado is RolDeveloper.ADMINISTRADOR:
        return actor_normalizado is RolDeveloper.PROPIETARIO

    return actor_normalizado in {
        RolDeveloper.PROPIETARIO,
        RolDeveloper.ADMINISTRADOR,
    }
