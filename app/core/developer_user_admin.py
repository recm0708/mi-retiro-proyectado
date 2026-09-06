"""Administración humana de cuentas del Portal Developer."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import secrets

from app.core.developer_identity import (
    RolDeveloper,
    hashear_password,
    rol_puede_asignar,
    validar_password,
)
from app.core.developer_provisioning import (
    restablecer_password_developer,
)
from app.core.developer_user_audit import (
    etiqueta_rol_auditoria,
    registrar_auditoria_usuario_developer,
)
from app.core.developer_store import (
    UsuarioDeveloper,
    actualizar_nombre_visible_usuario,
    cambiar_estado_usuario,
    cambiar_rol_usuario,
    crear_usuario_developer,
    eliminar_usuario_developer,
    obtener_usuario_por_id,
)


@dataclass(frozen=True)
class CredencialTemporalDeveloper:
    """Credencial efímera mostrable exactamente una vez tras una operación."""

    usuario: str
    password: str
    operacion: str


_credenciales_temporales: dict[
    str,
    CredencialTemporalDeveloper,
] = {}


def generar_password_temporal_developer() -> str:
    """Genera una contraseña temporal aleatoria que cumple la política vigente."""

    password = (
        "Tmp!"
        + secrets.token_urlsafe(24)
        + "A"
    )

    return validar_password(
        password
    )


def roles_asignables_por_actor(
    actor: UsuarioDeveloper,
) -> tuple[RolDeveloper, ...]:
    """Devuelve únicamente roles que el actor puede asignar por jerarquía."""

    if not actor.activo:
        return ()

    candidatos = (
        RolDeveloper.ADMINISTRADOR,
        RolDeveloper.OPERADOR,
        RolDeveloper.AUDITOR,
    )

    return tuple(
        rol
        for rol in candidatos
        if rol_puede_asignar(
            actor.rol,
            rol,
        )
    )


def _requerir_actor_gestor(
    actor: UsuarioDeveloper,
) -> None:
    """Exige una identidad activa con facultades reales de gestión de usuarios."""

    if not actor.activo:
        raise PermissionError(
            "La cuenta que ejecuta la operación no está activa."
        )

    if actor.rol not in {
        RolDeveloper.PROPIETARIO,
        RolDeveloper.ADMINISTRADOR,
    }:
        raise PermissionError(
            "La cuenta no puede administrar usuarios Developer."
        )


def _obtener_objetivo_gestionable(
    *,
    actor: UsuarioDeveloper,
    identificador: str,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper:
    """Resuelve un objetivo administrable sin permitir Owner ni autogestión."""

    _requerir_actor_gestor(
        actor
    )

    objetivo = obtener_usuario_por_id(
        identificador,
        ruta,
    )

    if objetivo is None:
        raise LookupError(
            "La cuenta Developer no existe."
        )

    if objetivo.es_propietario:
        raise PermissionError(
            "La cuenta Propietario está protegida."
        )

    if (
        objetivo.identificador
        == actor.identificador
    ):
        raise PermissionError(
            "La cuenta propia se administra desde Mi perfil."
        )

    if (
        objetivo.rol
        is RolDeveloper.ADMINISTRADOR
        and actor.rol
        is not RolDeveloper.PROPIETARIO
    ):
        raise PermissionError(
            "Solo el Propietario puede administrar a un Administrador."
        )

    return objetivo


def crear_usuario_administrado(
    *,
    actor: UsuarioDeveloper,
    usuario: str,
    nombre_visible: str,
    rol: RolDeveloper | str,
    ruta: str | Path | None = None,
) -> tuple[UsuarioDeveloper, str]:
    """Crea una cuenta con credencial temporal y cambio obligatorio."""

    _requerir_actor_gestor(
        actor
    )

    rol_destino = RolDeveloper(
        rol
    )

    if not rol_puede_asignar(
        actor.rol,
        rol_destino,
    ):
        raise PermissionError(
            "El actor no puede asignar el rol solicitado."
        )

    password_temporal = (
        generar_password_temporal_developer()
    )

    creado = crear_usuario_developer(
        actor_rol=actor.rol,
        usuario=usuario,
        nombre_visible=nombre_visible,
        rol=rol_destino,
        password_hash=hashear_password(
            password_temporal
        ),
        debe_cambiar_password=True,
        ruta=ruta,
    )

    registrar_auditoria_usuario_developer(
        actor=actor,
        objetivo=creado,
        accion="user.created",
        resumen=(
            "Cuenta creada con rol "
            + etiqueta_rol_auditoria(creado.rol)
            + "."
        ),
        ruta=ruta,
    )

    return creado, password_temporal


def actualizar_nombre_usuario_administrado(
    *,
    actor: UsuarioDeveloper,
    identificador: str,
    nombre_visible: str,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper:
    """Actualiza solo el nombre visible de una cuenta administrable."""

    objetivo = _obtener_objetivo_gestionable(
        actor=actor,
        identificador=identificador,
        ruta=ruta,
    )

    actualizado = actualizar_nombre_visible_usuario(
        identificador=objetivo.identificador,
        nombre_visible=nombre_visible,
        ruta=ruta,
    )

    registrar_auditoria_usuario_developer(
        actor=actor,
        objetivo=actualizado,
        accion="user.display_name.updated",
        resumen="Nombre visible actualizado.",
        ruta=ruta,
    )

    return actualizado


def cambiar_rol_usuario_administrado(
    *,
    actor: UsuarioDeveloper,
    identificador: str,
    nuevo_rol: RolDeveloper | str,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper:
    """Cambia un rol respetando jerarquía, Owner y autogestión."""

    objetivo = _obtener_objetivo_gestionable(
        actor=actor,
        identificador=identificador,
        ruta=ruta,
    )

    destino = RolDeveloper(
        nuevo_rol
    )

    if destino is objetivo.rol:
        return objetivo

    actualizado = cambiar_rol_usuario(
        actor_rol=actor.rol,
        identificador=objetivo.identificador,
        nuevo_rol=destino,
        ruta=ruta,
    )

    registrar_auditoria_usuario_developer(
        actor=actor,
        objetivo=actualizado,
        accion="user.role.changed",
        resumen=(
            "Rol cambiado de "
            + etiqueta_rol_auditoria(objetivo.rol)
            + " a "
            + etiqueta_rol_auditoria(actualizado.rol)
            + "."
        ),
        ruta=ruta,
    )

    return actualizado


def cambiar_estado_usuario_administrado(
    *,
    actor: UsuarioDeveloper,
    identificador: str,
    activo: bool,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper:
    """Activa o desactiva una cuenta sin permitir autodesactivación."""

    objetivo = _obtener_objetivo_gestionable(
        actor=actor,
        identificador=identificador,
        ruta=ruta,
    )

    nuevo_estado = bool(
        activo
    )

    if objetivo.activo is nuevo_estado:
        return objetivo

    actualizado = cambiar_estado_usuario(
        actor_rol=actor.rol,
        identificador=objetivo.identificador,
        activo=nuevo_estado,
        ruta=ruta,
    )

    registrar_auditoria_usuario_developer(
        actor=actor,
        objetivo=actualizado,
        accion=(
            "user.reactivated"
            if actualizado.activo
            else "user.disabled"
        ),
        resumen=(
            "Cuenta reactivada."
            if actualizado.activo
            else "Cuenta desactivada."
        ),
        ruta=ruta,
    )

    return actualizado


def restablecer_password_temporal_usuario(
    *,
    actor: UsuarioDeveloper,
    identificador: str,
    ruta: str | Path | None = None,
) -> tuple[UsuarioDeveloper, str]:
    """Rota una contraseña ordinaria y obliga a sustituirla al iniciar sesión."""

    objetivo = _obtener_objetivo_gestionable(
        actor=actor,
        identificador=identificador,
        ruta=ruta,
    )

    password_temporal = (
        generar_password_temporal_developer()
    )

    actualizado = restablecer_password_developer(
        actor=actor,
        usuario_objetivo=objetivo.usuario,
        nueva_password=password_temporal,
        ruta=ruta,
    )

    registrar_auditoria_usuario_developer(
        actor=actor,
        objetivo=actualizado,
        accion="user.password.reset",
        resumen=(
            "Credencial restablecida; "
            "cambio obligatorio activado."
        ),
        ruta=ruta,
    )

    return actualizado, password_temporal


def guardar_credencial_temporal_para_sesion(
    *,
    sesion: str,
    usuario: str,
    password: str,
    operacion: str,
) -> None:
    """Conserva en memoria una credencial hasta el siguiente GET de la sesión."""

    identificador = str(
        sesion
    ).strip()

    if not identificador:
        raise ValueError(
            "La sesión Developer es obligatoria."
        )

    login = str(
        usuario
    ).strip()

    if not login:
        raise ValueError(
            "El usuario de la credencial temporal es obligatorio."
        )

    accion = str(
        operacion
    ).strip()

    if not accion:
        raise ValueError(
            "La operación de la credencial temporal es obligatoria."
        )

    validar_password(
        password
    )

    _credenciales_temporales[
        identificador
    ] = CredencialTemporalDeveloper(
        usuario=login,
        password=password,
        operacion=accion,
    )


def consumir_credencial_temporal_para_sesion(
    sesion: str,
) -> CredencialTemporalDeveloper | None:
    """Consume una credencial efímera para impedir una segunda visualización."""

    identificador = str(
        sesion
    ).strip()

    if not identificador:
        return None

    return _credenciales_temporales.pop(
        identificador,
        None,
    )


def eliminar_usuario_administrado(
    *,
    actor: UsuarioDeveloper,
    identificador: str,
    ruta: str | Path | None = None,
) -> UsuarioDeveloper:
    # El borrado irreversible queda reservado al Propietario.
    """Elimina una cuenta administrable aplicando jerarquía y auditoría."""
    _requerir_actor_gestor(actor)

    if actor.rol is not RolDeveloper.PROPIETARIO:
        raise PermissionError(
            "Solo el Propietario puede eliminar usuarios."
        )

    objetivo = _obtener_objetivo_gestionable(
        actor=actor,
        identificador=identificador,
        ruta=ruta,
    )

    eliminado = eliminar_usuario_developer(
        objetivo.identificador,
        ruta,
    )

    registrar_auditoria_usuario_developer(
        actor=actor,
        objetivo=eliminado,
        accion="user.deleted",
        resumen="Cuenta eliminada definitivamente.",
        ruta=ruta,
    )

    return eliminado
