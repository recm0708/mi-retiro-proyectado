"""DEV.2 R6 — Provisión y recuperación de cuentas Developer."""

from __future__ import annotations

from pathlib import Path

from app.core.developer_identity import (
    RolDeveloper,
    generar_codigo_recuperacion_propietario,
    hashear_codigo_recuperacion,
    hashear_password,
    verificar_codigo_recuperacion,
    verificar_password,
)
from app.core.developer_store import (
    UsuarioDeveloper,
    actualizar_password_usuario,
    crear_propietario,
    obtener_propietario,
    obtener_usuario_por_login,
    rotar_credenciales_propietario,
)


def autenticar_usuario_developer(
    usuario: str,
    password: str,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper | None:
    """Autentica una cuenta activa sin revelar por qué falló."""

    cuenta = obtener_usuario_por_login(
        usuario,
        ruta,
    )

    if cuenta is None or not cuenta.activo:
        return None

    if not verificar_password(
        password,
        cuenta.password_hash,
    ):
        return None

    return cuenta


def bootstrap_propietario(
    *,
    usuario: str,
    nombre_visible: str,
    password: str,
    ruta: str | Path | None = None,
) -> tuple[UsuarioDeveloper, str]:
    """Crea la cuenta Propietario inicial y entrega su recuperación una vez."""

    if obtener_propietario(ruta) is not None:
        raise ValueError(
            "Ya existe una cuenta Propietario."
        )

    codigo = generar_codigo_recuperacion_propietario()

    propietario = crear_propietario(
        usuario=usuario,
        nombre_visible=nombre_visible,
        password_hash=hashear_password(password),
        recovery_code_hash=(
            hashear_codigo_recuperacion(codigo)
        ),
        ruta=ruta,
    )

    return propietario, codigo


def restablecer_password_developer(
    *,
    actor: UsuarioDeveloper,
    usuario_objetivo: str,
    nueva_password: str,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper:
    """Restablece contraseñas ordinarias respetando jerarquía y protección Owner."""

    if not actor.activo:
        raise PermissionError(
            "La cuenta que ejecuta la operación no está activa."
        )

    if actor.rol not in {
        RolDeveloper.PROPIETARIO,
        RolDeveloper.ADMINISTRADOR,
    }:
        raise PermissionError(
            "La cuenta no tiene privilegios para restablecer contraseñas."
        )

    objetivo = obtener_usuario_por_login(
        usuario_objetivo,
        ruta,
    )

    if objetivo is None:
        raise LookupError(
            "La cuenta objetivo no existe."
        )

    if objetivo.es_propietario:
        raise PermissionError(
            "La cuenta Propietario solo puede recuperarse mediante "
            "el procedimiento protegido."
        )

    if (
        objetivo.rol is RolDeveloper.ADMINISTRADOR
        and actor.rol is not RolDeveloper.PROPIETARIO
    ):
        raise PermissionError(
            "Solo el Propietario puede restablecer "
            "la contraseña de un Administrador."
        )

    return actualizar_password_usuario(
        identificador=objetivo.identificador,
        password_hash=hashear_password(
            nueva_password
        ),
        debe_cambiar_password=True,
        ruta=ruta,
    )


def recuperar_propietario(
    *,
    codigo_recuperacion: str,
    nueva_password: str,
    ruta: str | Path | None = None,
) -> tuple[UsuarioDeveloper, str]:
    """Recupera Owner consumiendo y rotando el código anterior."""

    propietario = obtener_propietario(ruta)

    if (
        propietario is None
        or propietario.recovery_code_hash is None
        or not verificar_codigo_recuperacion(
            codigo_recuperacion,
            propietario.recovery_code_hash,
        )
    ):
        raise PermissionError(
            "El código de recuperación no es válido."
        )

    nuevo_codigo = (
        generar_codigo_recuperacion_propietario()
    )

    actualizado = rotar_credenciales_propietario(
        identificador=propietario.identificador,
        recovery_hash_esperado=(
            propietario.recovery_code_hash
        ),
        nuevo_password_hash=hashear_password(
            nueva_password
        ),
        nuevo_recovery_hash=(
            hashear_codigo_recuperacion(
                nuevo_codigo
            )
        ),
        ruta=ruta,
    )

    return actualizado, nuevo_codigo
