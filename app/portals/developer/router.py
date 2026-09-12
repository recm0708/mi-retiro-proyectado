"""Router HTTP del Portal Developer."""

from fastapi import APIRouter
from pathlib import Path
from app.core.observability import (
    clasificar_operacion_http,
    correlacion_actual,
    establecer_correlacion,
    modo_desarrollo_activo,
    registrar_evento,
    registrar_excepcion,
    restablecer_correlacion,
)
from app.core.config import (
    APP_AUTHOR,
    APP_DESCRIPTION,
    APP_NAME,
    APP_SUBTITLE,
    APP_VERSION,
    MI_CAJA_DIGITAL_URL,
    ADMIN_COOKIE_SECURE,
    ADMIN_COOKIE_SAMESITE,
    ADMIN_SESSION_MINUTES,
    ADMIN_SESSION_MAX_HOURS,
)
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    RedirectResponse,
    Response,
)
from app.portals.developer.development_center import construir_estado_centro_desarrollo
from app.portals.developer.developer_identity import (
    PermisoDeveloper,
    hashear_password,
    permisos_para_rol,
    rol_tiene_permiso,
)
from app.portals.developer.developer_store import cambiar_password_propio
from app.portals.developer.developer_web_security import (
    revalidar_password_usuario,
    token_csrf_para_sesion,
    validar_token_csrf_sesion,
)
from app.portals.developer.admin_session import (
    limpiar_sesiones_expiradas as limpiar_sesiones_developer_expiradas,
    obtener_sesiones_activas as obtener_sesiones_developer_activas,
    revocar_sesiones_usuario,
    revocar_todas_las_sesiones_admin,
)
from app.portals.developer.admin_security import (
    requerir_administrador,
    administracion_activa,
)
from app.portals.developer.admin_session import (
    crear_sesion_admin,
    obtener_sesion_admin,
    eliminar_sesion_admin,
)
from app.portals.developer.developer_provisioning import (
    autenticar_usuario_developer,
)
from app.portals.developer.developer_store import (
    UsuarioDeveloper,
    actualizar_avatar_usuario,
    actualizar_nombre_visible_usuario,
    obtener_usuario_por_id,
    registrar_acceso_usuario,
)
from app.portals.developer.developer_avatar import (
    MAX_AVATAR_BYTES,
    eliminar_avatar_developer,
    guardar_avatar_developer,
    resolver_avatar_developer,
)
from app.portals.developer.developer_identity import RolDeveloper
from app.portals.developer.developer_store import listar_usuarios_developer
from app.portals.developer.developer_user_audit import (
    listar_auditoria_usuarios_developer,
)
from app.portals.developer.developer_user_admin import (
    actualizar_nombre_usuario_administrado,
    cambiar_estado_usuario_administrado,
    cambiar_rol_usuario_administrado,
    consumir_credencial_temporal_para_sesion,
    crear_usuario_administrado,
    eliminar_usuario_administrado,
    guardar_credencial_temporal_para_sesion,
    restablecer_password_temporal_usuario,
    roles_asignables_por_actor,
)

router = APIRouter()

templates = None

def configure_router(*, templates_value) -> None:
    """Inyecta dependencias compartidas desde el composition root."""
    global templates
    templates = templates_value

@router.get(
    "/dev",
    response_class=HTMLResponse,
)
async def portal_developer(request: Request):
    """Entrada humana canónica del Portal Developer."""

    _verificar_superficie_administrativa()

    usuario = _obtener_usuario_sesion_web(
        request
    )

    if usuario is not None:
        if usuario.debe_cambiar_password:
            return RedirectResponse(
                url="/dev/perfil?cambio_password=obligatorio",
                status_code=303,
            )

        return _render_pagina_developer(
            request,
            usuario=usuario,
            plantilla="developer/dev_dashboard.html",
            pagina_activa="resumen",
        )

    return _render_login_developer(request)


@router.get(
    "/dev/diagnostico",
    response_class=HTMLResponse,
)
async def diagnostico_developer(request: Request):
    """Muestra el autodiagnóstico técnico del Portal Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="developer/dev_diagnostics.html",
        pagina_activa="diagnostico",
        permiso=PermisoDeveloper.DIAGNOSTICO_LEER,
    )


@router.get(
    "/dev/eventos",
    response_class=HTMLResponse,
)
async def eventos_developer(request: Request):
    """Muestra los eventos de observabilidad del Portal Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="developer/dev_events.html",
        pagina_activa="eventos",
        permiso=PermisoDeveloper.EVENTOS_LEER,
    )


@router.get(
    "/dev/archivos",
    response_class=HTMLResponse,
)
async def archivos_developer(request: Request):
    """Muestra el inventario técnico del Portal Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="developer/dev_files.html",
        pagina_activa="archivos",
        permiso=PermisoDeveloper.ARCHIVOS_LEER,
    )


@router.post(
    "/dev/archivos/exportar",
)
async def exportar_archivos_developer(
    request: Request,
    csrf_token: str = Form(...),
):
    """Descarga el ZIP diagnóstico sanitizado desde una sesión humana."""

    _requerir_permiso_developer(
        request,
        PermisoDeveloper.ARCHIVOS_DESCARGAR,
    )
    _validar_csrf_developer(
        request,
        csrf_token,
    )

    from fastapi.responses import FileResponse

    from app.portals.developer.development_center import (
        exportar_zip_diagnostico_sanitizado,
    )

    try:
        ruta_zip = exportar_zip_diagnostico_sanitizado()
    except PermissionError:
        return RedirectResponse(
            url="/dev/archivos?exportacion=bloqueada",
            status_code=303,
        )
    except FileNotFoundError:
        return RedirectResponse(
            url="/dev/archivos?exportacion=sin-archivos",
            status_code=303,
        )

    return FileResponse(
        path=ruta_zip,
        filename="mrp-diagnostics-export.zip",
        media_type="application/zip",
        headers={
            "Cache-Control": "no-store",
        },
    )


@router.get(
    "/dev/mantenimiento",
    response_class=HTMLResponse,
)
async def mantenimiento_developer(request: Request):
    """Muestra la superficie de mantenimiento del Portal Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="developer/dev_maintenance.html",
        pagina_activa="mantenimiento",
        permiso=PermisoDeveloper.MANTENIMIENTO_LEER,
    )


@router.post(
    "/dev/mantenimiento/limpiar-sesiones",
)
async def limpiar_sesiones_developer(
    request: Request,
    csrf_token: str = Form(...),
):
    """Elimina sesiones ya expiradas sin afectar sesiones vigentes."""

    usuario = _requerir_permiso_developer(
        request,
        PermisoDeveloper.MANTENIMIENTO_EJECUTAR,
    )
    _validar_csrf_developer(
        request,
        csrf_token,
    )

    antes = len(
        obtener_sesiones_developer_activas()
    )

    limpiar_sesiones_developer_expiradas()

    despues = len(
        obtener_sesiones_developer_activas()
    )

    registrar_evento(
        level="INFO",
        event="dev.maintenance.sessions.cleaned",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "maintenance.sessions.clean",
            "removed": max(0, antes - despues),
            "actor_role": usuario.rol.value,
        },
    )

    return RedirectResponse(
        url="/dev/mantenimiento?resultado=sesiones-limpiadas",
        status_code=303,
    )


@router.post(
    "/dev/mantenimiento/revocar-sesiones",
)
async def revocar_sesiones_developer(
    request: Request,
    csrf_token: str = Form(...),
    password_actual: str = Form(...),
    confirmacion: str = Form(...),
):
    """Revoca todas las sesiones tras RBAC, CSRF, revalidación y confirmación."""

    usuario = _requerir_permiso_developer(
        request,
        PermisoDeveloper.MANTENIMIENTO_DESTRUCTIVO,
    )
    _validar_csrf_developer(
        request,
        csrf_token,
    )
    _revalidar_operacion_developer(
        request,
        usuario,
        password_actual,
    )

    if confirmacion.strip() != "REVOCAR SESIONES":
        raise HTTPException(
            status_code=400,
            detail="La confirmación de la operación no coincide.",
        )

    registrar_evento(
        level="WARNING",
        event="dev.maintenance.sessions.revoke_all",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "maintenance.sessions.revoke_all",
            "actor_role": usuario.rol.value,
        },
    )

    revocar_todas_las_sesiones_admin()

    respuesta = RedirectResponse(
        url="/dev",
        status_code=303,
    )
    respuesta.delete_cookie(
        key="mrp_admin_session",
        path="/dev",
    )
    return respuesta


@router.get(
    "/dev/privacidad",
    response_class=HTMLResponse,
)
async def privacidad_developer(request: Request):
    """Muestra los controles de privacidad del Portal Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="developer/dev_privacy.html",
        pagina_activa="privacidad",
        permiso=PermisoDeveloper.PRIVACIDAD_LEER,
    )


@router.get(
    "/dev/perfil",
    response_class=HTMLResponse,
)
async def perfil_developer(request: Request):
    """Muestra la identidad y preferencias de la cuenta Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="developer/dev_profile.html",
        pagina_activa="perfil",
        permiso=PermisoDeveloper.PERFIL_LEER,
    )


@router.post(
    "/dev/perfil/datos",
)
async def actualizar_datos_perfil_developer(
    request: Request,
    csrf_token: str = Form(...),
    nombre_visible: str = Form(...),
):
    """Actualiza los datos personales editables de la cuenta autenticada."""

    usuario = _requerir_permiso_developer(
        request,
        PermisoDeveloper.PERFIL_EDITAR_PROPIO,
    )

    _validar_csrf_developer(
        request,
        csrf_token,
    )

    try:
        actualizar_nombre_visible_usuario(
            identificador=usuario.identificador,
            nombre_visible=nombre_visible,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    registrar_evento(
        level="INFO",
        event="dev.profile.updated",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "profile.update",
            "actor_role": usuario.rol.value,
        },
    )

    return RedirectResponse(
        url="/dev/perfil?perfil=actualizado",
        status_code=303,
    )


@router.post(
    "/dev/perfil/avatar",
)
async def actualizar_avatar_perfil_developer(
    request: Request,
    csrf_token: str = Form(...),
    avatar: UploadFile = File(...),
):
    """Valida y reemplaza la imagen de perfil de la cuenta autenticada."""

    usuario = _requerir_permiso_developer(
        request,
        PermisoDeveloper.PERFIL_EDITAR_PROPIO,
    )

    _validar_csrf_developer(
        request,
        csrf_token,
    )

    permitidos = {
        "image/jpeg",
        "image/png",
        "image/webp",
    }

    if (
        avatar.content_type
        and avatar.content_type.lower()
        not in permitidos
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "La foto debe ser PNG, JPEG o WebP."
            ),
        )

    try:
        contenido = await avatar.read(
            MAX_AVATAR_BYTES + 1
        )
    finally:
        await avatar.close()

    anterior = usuario.avatar_relativo
    nueva_referencia = None

    try:
        nueva_referencia = guardar_avatar_developer(
            identificador=usuario.identificador,
            contenido=contenido,
        )

        actualizar_avatar_usuario(
            identificador=usuario.identificador,
            avatar_relativo=nueva_referencia,
        )
    except ValueError as error:
        if nueva_referencia:
            eliminar_avatar_developer(
                nueva_referencia
            )

        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error
    except Exception:
        if nueva_referencia:
            eliminar_avatar_developer(
                nueva_referencia
            )

        raise

    if (
        anterior
        and anterior != nueva_referencia
    ):
        eliminar_avatar_developer(
            anterior
        )

    registrar_evento(
        level="INFO",
        event="dev.profile.avatar.updated",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "profile.avatar.update",
            "actor_role": usuario.rol.value,
        },
    )

    return RedirectResponse(
        url="/dev/perfil?avatar=actualizado",
        status_code=303,
    )


@router.post(
    "/dev/perfil/avatar/eliminar",
)
async def eliminar_avatar_perfil_developer(
    request: Request,
    csrf_token: str = Form(...),
):
    """Elimina la imagen personalizada de la cuenta autenticada."""

    usuario = _requerir_permiso_developer(
        request,
        PermisoDeveloper.PERFIL_EDITAR_PROPIO,
    )

    _validar_csrf_developer(
        request,
        csrf_token,
    )

    anterior = usuario.avatar_relativo

    actualizar_avatar_usuario(
        identificador=usuario.identificador,
        avatar_relativo=None,
    )

    eliminar_avatar_developer(
        anterior
    )

    registrar_evento(
        level="INFO",
        event="dev.profile.avatar.removed",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "profile.avatar.remove",
            "actor_role": usuario.rol.value,
        },
    )

    return RedirectResponse(
        url="/dev/perfil?avatar=eliminado",
        status_code=303,
    )


@router.get(
    "/dev/perfil/avatar/{identificador}",
    include_in_schema=False,
)
async def obtener_avatar_perfil_developer(
    request: Request,
    identificador: str,
):
    """Entrega un avatar únicamente dentro de una sesión Developer válida."""

    solicitante = _obtener_usuario_sesion_web(
        request
    )

    if solicitante is None:
        raise HTTPException(
            status_code=401,
            detail="Sesión Developer requerida.",
        )

    objetivo = obtener_usuario_por_id(
        identificador
    )

    if objetivo is None:
        raise HTTPException(
            status_code=404,
            detail="La cuenta Developer no existe.",
        )

    puede_ver_otros = rol_tiene_permiso(
        solicitante.rol,
        PermisoDeveloper.USUARIOS_LEER,
    )

    if (
        objetivo.identificador
        != solicitante.identificador
        and not puede_ver_otros
    ):
        raise HTTPException(
            status_code=403,
            detail="La cuenta no puede consultar este perfil.",
        )

    ruta = resolver_avatar_developer(
        objetivo.avatar_relativo
    )

    if (
        ruta is None
        or not ruta.is_file()
    ):
        raise HTTPException(
            status_code=404,
            detail="La cuenta no tiene foto de perfil.",
        )

    media_type = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".webp": "image/webp",
    }.get(
        ruta.suffix.lower(),
        "application/octet-stream",
    )

    return FileResponse(
        path=ruta,
        media_type=media_type,
        headers={
            "Cache-Control": "no-store",
        },
    )


@router.post(
    "/dev/perfil/password",
)
async def cambiar_password_perfil_developer(
    request: Request,
    csrf_token: str = Form(...),
    password_actual: str = Form(...),
    nueva_password: str = Form(...),
    confirmar_password: str = Form(...),
):
    """Cambia la contraseña propia y revoca las sesiones anteriores."""

    usuario = _requerir_permiso_developer(
        request,
        PermisoDeveloper.PERFIL_EDITAR_PROPIO,
    )
    _validar_csrf_developer(
        request,
        csrf_token,
    )
    _revalidar_operacion_developer(
        request,
        usuario,
        password_actual,
    )

    if nueva_password != confirmar_password:
        raise HTTPException(
            status_code=400,
            detail="Las contraseñas nuevas no coinciden.",
        )

    actualizado = cambiar_password_propio(
        identificador=usuario.identificador,
        password_hash=hashear_password(
            nueva_password
        ),
    )

    revocar_sesiones_usuario(
        actualizado.identificador
    )

    registrar_evento(
        level="INFO",
        event="dev.profile.password.changed",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "profile.password.change",
            "actor_role": actualizado.rol.value,
        },
    )

    respuesta = RedirectResponse(
        url="/dev",
        status_code=303,
    )
    respuesta.delete_cookie(
        key="mrp_admin_session",
        path="/dev",
    )
    return respuesta


@router.get(
    "/dev/usuarios",
    response_class=HTMLResponse,
)
async def usuarios_developer(request: Request):
    """Muestra el directorio humano de cuentas según RBAC y jerarquía."""

    _verificar_superficie_administrativa()

    actor = _obtener_usuario_sesion_web(
        request
    )

    if actor is None:
        return RedirectResponse(
            url="/dev",
            status_code=303,
        )

    if actor.debe_cambiar_password:
        return RedirectResponse(
            url="/dev/perfil?cambio_password=obligatorio",
            status_code=303,
        )

    if not rol_tiene_permiso(
        actor.rol,
        PermisoDeveloper.USUARIOS_LEER,
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "La cuenta Developer no tiene permiso "
                "para acceder a esta sección."
            ),
        )

    contexto = _contexto_developer(
        request,
        autenticado=True,
        usuario=actor,
        pagina_activa="usuarios",
    )

    contexto["estado_dev"] = (
        construir_estado_centro_desarrollo()
    )

    contexto["dev_usuarios"] = (
        _filas_gestion_usuarios_developer(
            actor
        )
    )

    contexto["dev_roles_creables"] = [
        _opcion_rol_developer(
            rol
        )
        for rol in roles_asignables_por_actor(
            actor
        )
    ]

    contexto["dev_auditoria_usuarios"] = (
        listar_auditoria_usuarios_developer(
            limite=200,
        )
        if rol_tiene_permiso(
            actor.rol,
            PermisoDeveloper.SEGURIDAD_AUDITAR,
        )
        else []
    )

    contexto["dev_credencial_temporal"] = (
        consumir_credencial_temporal_para_sesion(
            _identificador_sesion_developer(
                request
            )
        )
    )

    contexto["dev_resultado_mensaje"] = (
        _mensaje_resultado_usuarios(
            request.query_params.get(
                "resultado"
            )
        )
    )

    return templates.TemplateResponse(
        request=request,
        name="developer/dev_users.html",
        context=contexto,
    )


@router.post(
    "/dev/usuarios/crear",
)
async def crear_usuario_developer_web(
    request: Request,
    csrf_token: str = Form(...),
    usuario_nuevo: str = Form(...),
    nombre_visible: str = Form(...),
    rol: str = Form(...),
    password_actual: str = Form(...),
):
    """Crea una cuenta con credencial temporal tras autorización reforzada."""

    actor = _requerir_permiso_developer(
        request,
        PermisoDeveloper.USUARIOS_CREAR,
    )

    _validar_csrf_developer(
        request,
        csrf_token,
    )

    permiso_rol = (
        PermisoDeveloper.ROLES_ASIGNAR_ADMIN
        if rol == RolDeveloper.ADMINISTRADOR.value
        else PermisoDeveloper.ROLES_ASIGNAR_BASICOS
    )

    _requerir_permiso_developer(
        request,
        permiso_rol,
    )

    if not revalidar_password_usuario(
        actor,
        password_actual,
    ):
        return RedirectResponse(
            url="/dev/usuarios?resultado=revalidacion-invalida",
            status_code=303,
        )

    try:
        creado, password_temporal = (
            crear_usuario_administrado(
                actor=actor,
                usuario=usuario_nuevo,
                nombre_visible=nombre_visible,
                rol=rol,
            )
        )
    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error),
        ) from error
    except ValueError:
        return RedirectResponse(
            url="/dev/usuarios?resultado=crear-invalido",
            status_code=303,
        )

    guardar_credencial_temporal_para_sesion(
        sesion=_identificador_sesion_developer(
            request
        ),
        usuario=creado.usuario,
        password=password_temporal,
        operacion="crear",
    )

    registrar_evento(
        level="INFO",
        event="dev.users.created",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "users.create",
            "actor_role": actor.rol.value,
            "target_role": creado.rol.value,
        },
    )

    return RedirectResponse(
        url="/dev/usuarios?resultado=creado",
        status_code=303,
    )


@router.post(
    "/dev/usuarios/{identificador}/editar",
)
async def editar_usuario_developer_web(
    identificador: str,
    request: Request,
    csrf_token: str = Form(...),
    nombre_visible: str = Form(""),
    nuevo_rol: str = Form(""),
    estado: str = Form(""),
    password_actual: str = Form(...),
):
    """Aplica en una sola revalidación los cambios solicitados."""

    actor = _requerir_permiso_developer(
        request,
        PermisoDeveloper.USUARIOS_EDITAR,
    )

    _validar_csrf_developer(
        request,
        csrf_token,
    )

    if not revalidar_password_usuario(
        actor,
        password_actual,
    ):
        return RedirectResponse(
            url="/dev/usuarios?resultado=revalidacion-invalida",
            status_code=303,
        )

    objetivo = next(
        (
            usuario
            for usuario
            in listar_usuarios_developer()
            if usuario.identificador == identificador
        ),
        None,
    )

    if objetivo is None:
        raise HTTPException(
            status_code=404,
            detail="La cuenta Developer no existe.",
        )

    cambios = 0
    seguridad_cambiada = False

    nombre_solicitado = nombre_visible.strip()

    if (
        nombre_solicitado
        and nombre_solicitado != objetivo.nombre_visible
    ):
        objetivo = actualizar_nombre_usuario_administrado(
            actor=actor,
            identificador=objetivo.identificador,
            nombre_visible=nombre_solicitado,
        )
        cambios += 1

    rol_solicitado = nuevo_rol.strip()

    if rol_solicitado:
        try:
            destino = RolDeveloper(
                rol_solicitado
            )
        except ValueError:
            return RedirectResponse(
                url="/dev/usuarios?resultado=editar-invalido",
                status_code=303,
            )

        if destino is not objetivo.rol:
            objetivo = cambiar_rol_usuario_administrado(
                actor=actor,
                identificador=objetivo.identificador,
                nuevo_rol=destino,
            )
            cambios += 1
            seguridad_cambiada = True

    estado_solicitado = estado.strip()

    if estado_solicitado:
        if estado_solicitado not in {
            "activa",
            "desactivada",
        }:
            return RedirectResponse(
                url="/dev/usuarios?resultado=editar-invalido",
                status_code=303,
            )

        activo_solicitado = (
            estado_solicitado == "activa"
        )

        if activo_solicitado != objetivo.activo:
            objetivo = cambiar_estado_usuario_administrado(
                actor=actor,
                identificador=objetivo.identificador,
                activo=activo_solicitado,
            )
            cambios += 1
            seguridad_cambiada = True

    if seguridad_cambiada:
        revocar_sesiones_usuario(
            objetivo.identificador
        )

    if cambios == 0:
        return RedirectResponse(
            url="/dev/usuarios?resultado=sin-cambios",
            status_code=303,
        )

    registrar_evento(
        level="INFO",
        event="dev.users.updated",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "users.edit",
            "changes": cambios,
            "security_changed": seguridad_cambiada,
        },
    )

    return RedirectResponse(
        url="/dev/usuarios?resultado=cuenta-actualizada",
        status_code=303,
    )


@router.post(
    "/dev/usuarios/{identificador}/datos",
)
async def actualizar_usuario_developer_web(
    identificador: str,
    request: Request,
    csrf_token: str = Form(...),
    nombre_visible: str = Form(...),
):
    """Actualiza el nombre visible de una cuenta administrable."""

    actor = _requerir_permiso_developer(
        request,
        PermisoDeveloper.USUARIOS_EDITAR,
    )

    _validar_csrf_developer(
        request,
        csrf_token,
    )

    try:
        actualizar_nombre_usuario_administrado(
            actor=actor,
            identificador=identificador,
            nombre_visible=nombre_visible,
        )
    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error),
        ) from error
    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error
    except ValueError:
        return RedirectResponse(
            url="/dev/usuarios?resultado=datos-invalidos",
            status_code=303,
        )

    registrar_evento(
        level="INFO",
        event="dev.users.profile.updated",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "users.profile.update",
            "actor_role": actor.rol.value,
        },
    )

    return RedirectResponse(
        url="/dev/usuarios?resultado=datos-actualizados",
        status_code=303,
    )


@router.post(
    "/dev/usuarios/{identificador}/rol",
)
async def cambiar_rol_usuario_developer_web(
    identificador: str,
    request: Request,
    csrf_token: str = Form(...),
    nuevo_rol: str = Form(...),
    password_actual: str = Form(...),
):
    """Cambia el rol de una cuenta con permiso específico y revalidación."""

    actor = _requerir_permiso_developer(
        request,
        PermisoDeveloper.USUARIOS_EDITAR,
    )

    _validar_csrf_developer(
        request,
        csrf_token,
    )

    permiso_rol = (
        PermisoDeveloper.ROLES_ASIGNAR_ADMIN
        if nuevo_rol == RolDeveloper.ADMINISTRADOR.value
        else PermisoDeveloper.ROLES_ASIGNAR_BASICOS
    )

    _requerir_permiso_developer(
        request,
        permiso_rol,
    )

    if not revalidar_password_usuario(
        actor,
        password_actual,
    ):
        return RedirectResponse(
            url="/dev/usuarios?resultado=revalidacion-invalida",
            status_code=303,
        )

    try:
        actualizado = (
            cambiar_rol_usuario_administrado(
                actor=actor,
                identificador=identificador,
                nuevo_rol=nuevo_rol,
            )
        )
    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error),
        ) from error
    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error
    except ValueError:
        return RedirectResponse(
            url="/dev/usuarios?resultado=rol-invalido",
            status_code=303,
        )

    revocar_sesiones_usuario(
        actualizado.identificador
    )

    registrar_evento(
        level="WARNING",
        event="dev.users.role.changed",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "users.role.change",
            "actor_role": actor.rol.value,
            "target_role": actualizado.rol.value,
        },
    )

    return RedirectResponse(
        url="/dev/usuarios?resultado=rol-actualizado",
        status_code=303,
    )


@router.post(
    "/dev/usuarios/{identificador}/estado",
)
async def cambiar_estado_usuario_developer_web(
    identificador: str,
    request: Request,
    csrf_token: str = Form(...),
    activo: str = Form(...),
    password_actual: str = Form(...),
):
    """Activa o desactiva una cuenta tras revalidación de identidad."""

    actor = _requerir_permiso_developer(
        request,
        PermisoDeveloper.USUARIOS_DESACTIVAR,
    )

    _validar_csrf_developer(
        request,
        csrf_token,
    )

    if not revalidar_password_usuario(
        actor,
        password_actual,
    ):
        return RedirectResponse(
            url="/dev/usuarios?resultado=revalidacion-invalida",
            status_code=303,
        )

    if activo not in {
        "0",
        "1",
    }:
        raise HTTPException(
            status_code=400,
            detail="Estado de cuenta inválido.",
        )

    try:
        actualizado = (
            cambiar_estado_usuario_administrado(
                actor=actor,
                identificador=identificador,
                activo=(activo == "1"),
            )
        )
    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error),
        ) from error
    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    revocar_sesiones_usuario(
        actualizado.identificador
    )

    registrar_evento(
        level="WARNING",
        event="dev.users.state.changed",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "users.state.change",
            "actor_role": actor.rol.value,
            "active": actualizado.activo,
        },
    )

    return RedirectResponse(
        url="/dev/usuarios?resultado=estado-actualizado",
        status_code=303,
    )


@router.post(
    "/dev/usuarios/{identificador}/password-temporal",
)
async def restablecer_password_usuario_developer_web(
    identificador: str,
    request: Request,
    csrf_token: str = Form(...),
    password_actual: str = Form(...),
):
    """Genera una credencial temporal y revoca las sesiones del objetivo."""

    actor = _requerir_permiso_developer(
        request,
        PermisoDeveloper.USUARIOS_EDITAR,
    )

    _validar_csrf_developer(
        request,
        csrf_token,
    )

    if not revalidar_password_usuario(
        actor,
        password_actual,
    ):
        return RedirectResponse(
            url="/dev/usuarios?resultado=revalidacion-invalida",
            status_code=303,
        )

    try:
        actualizado, password_temporal = (
            restablecer_password_temporal_usuario(
                actor=actor,
                identificador=identificador,
            )
        )
    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error),
        ) from error
    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    revocar_sesiones_usuario(
        actualizado.identificador
    )

    guardar_credencial_temporal_para_sesion(
        sesion=_identificador_sesion_developer(
            request
        ),
        usuario=actualizado.usuario,
        password=password_temporal,
        operacion="restablecer",
    )

    registrar_evento(
        level="WARNING",
        event="dev.users.password.reset",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "users.password.reset",
            "actor_role": actor.rol.value,
            "target_role": actualizado.rol.value,
        },
    )

    return RedirectResponse(
        url="/dev/usuarios?resultado=password-temporal",
        status_code=303,
    )


@router.post(
    "/dev/usuarios/{identificador}/eliminar",
)
async def eliminar_usuario_developer_web(
    identificador: str,
    request: Request,
    csrf_token: str = Form(...),
    password_actual: str = Form(...),
    confirmacion: str = Form(...),
):
    """Elimina una cuenta ordinaria desde la superficie web protegida."""
    actor = _requerir_permiso_developer(
        request,
        PermisoDeveloper.USUARIOS_ELIMINAR,
    )

    _validar_csrf_developer(
        request,
        csrf_token,
    )

    if not revalidar_password_usuario(
        actor,
        password_actual,
    ):
        return RedirectResponse(
            url="/dev/usuarios?resultado=revalidacion-invalida",
            status_code=303,
        )

    if confirmacion.strip() != "ELIMINAR USUARIO":
        return RedirectResponse(
            url="/dev/usuarios?resultado=eliminar-confirmacion",
            status_code=303,
        )

    try:
        eliminado = eliminar_usuario_administrado(
            actor=actor,
            identificador=identificador,
        )
    except PermissionError as error:
        raise HTTPException(
            status_code=403,
            detail=str(error),
        ) from error
    except LookupError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    revocar_sesiones_usuario(
        eliminado.identificador
    )

    if eliminado.avatar_relativo:
        eliminar_avatar_developer(
            eliminado.avatar_relativo
        )

    registrar_evento(
        level="WARNING",
        event="dev.users.deleted",
        component="security.developer",
        outcome="success",
        metadata={
            "operation": "users.delete",
            "actor_role": actor.rol.value,
            "target_role": eliminado.rol.value,
        },
    )

    return RedirectResponse(
        url="/dev/usuarios?resultado=usuario-eliminado",
        status_code=303,
    )


@router.get(
    "/dev/acceso-tecnico",
    response_class=HTMLResponse,
)
async def acceso_tecnico_developer(request: Request):
    """Muestra la superficie humana de credenciales técnicas Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="developer/dev_technical_access.html",
        pagina_activa="acceso_tecnico",
        permiso=PermisoDeveloper.TOKENS_LEER,
    )


@router.get(
    "/dev/login",
    include_in_schema=False,
)
async def login_administrativo_legacy():
    """Conserva la URL histórica y dirige al acceso humano canónico."""

    return RedirectResponse(
        url="/dev",
        status_code=303,
    )


@router.post(
    "/dev",
)
@router.post(
    "/dev/login",
    include_in_schema=False,
)
async def procesar_login_administrativo(
    request: Request,
    usuario: str | None = Form(None),
    password: str | None = Form(None),
):
    """Autentica una identidad Developer y crea su sesión web."""

    _verificar_superficie_administrativa()

    if usuario is None or password is None:
        raise HTTPException(
            status_code=422,
            detail="Usuario y contraseña requeridos.",
        )

    cuenta = autenticar_usuario_developer(
        usuario,
        password,
    )

    if cuenta is None:
        registrar_evento(
            level="WARNING",
            event="admin.login.denied",
            component="security.admin",
            outcome="denied",
            metadata={
                "endpoint": "/dev",
                "reason": "invalid_credentials",
            },
        )

        return _render_login_developer(
            request,
            error="Usuario o contraseña incorrectos.",
            status_code=401,
            usuario_recordado=usuario.strip(),
        )

    cuenta = registrar_acceso_usuario(
        identificador=cuenta.identificador,
    )

    sesion = crear_sesion_admin(
        usuario_id=cuenta.identificador,
        usuario=cuenta.usuario,
        rol=cuenta.rol,
        revision_seguridad=(
            cuenta.revision_seguridad
        ),
    )

    sesion_info = obtener_sesion_admin(
        sesion,
        actualizar_actividad=False,
    )

    limite_sesiones_aplicado = bool(
        sesion_info is not None
        and sesion_info.sesiones_cerradas_por_limite > 0
    )

    registrar_evento(
        level="INFO",
        event="admin.login.granted",
        component="security.admin",
        outcome="allowed",
        metadata={
            "endpoint": "/dev",
            "user_id": cuenta.identificador,
            "role": cuenta.rol.value,
        },
    )

    respuesta = RedirectResponse(
        url=(
            "/dev?sesion=limite"
            if limite_sesiones_aplicado
            else "/dev"
        ),
        status_code=303,
    )
    respuesta.set_cookie(
        key="mrp_admin_session",
        value=sesion,
        httponly=True,
        samesite=ADMIN_COOKIE_SAMESITE,
        secure=ADMIN_COOKIE_SECURE,
        max_age=ADMIN_SESSION_MAX_HOURS * 60 * 60,
        path="/dev",
    )
    return respuesta


@router.post("/dev/logout")
async def logout_administrativo(
    request: Request,
    csrf_token: str | None = Form(None),
):
    """Cierra la sesión web Developer activa."""

    usuario = _obtener_usuario_sesion_web(
        request
    )

    if usuario is not None:
        _validar_csrf_developer(
            request,
            csrf_token,
        )

    sesion = request.cookies.get(
        "mrp_admin_session"
    )

    if sesion:
        eliminar_sesion_admin(
            sesion
        )
        registrar_evento(
            level="INFO",
            event="admin.session.revoked",
            component="security.admin",
            outcome="success",
            metadata={
                "endpoint": request.url.path,
            },
        )

    respuesta = RedirectResponse(
        url="/dev",
        status_code=303,
    )
    respuesta.delete_cookie(
        key="mrp_admin_session",
        path="/dev",
    )
    return respuesta


@router.get(
    "/dev/centro-desarrollo",
    response_class=HTMLResponse,
)
async def centro_desarrollo(request: Request):
    """Conserva Bearer técnico y redirige sesiones humanas a /dev."""

    _verificar_superficie_administrativa()

    authorization = request.headers.get(
        "Authorization",
        "",
    )

    if authorization:
        requerir_administrador(
            request
        )
        return _render_centro_desarrollo(
            request
        )

    usuario = _obtener_usuario_sesion_web(
        request
    )

    if usuario is not None:
        return RedirectResponse(
            url="/dev",
            status_code=303,
        )

    acepta_html = (
        "text/html"
        in request.headers.get(
            "accept",
            "",
        ).lower()
    )

    if acepta_html:
        return RedirectResponse(
            url="/dev",
            status_code=303,
        )

    # Compatibilidad programática R5: sin sesión web ni
    # Bearer se conserva una respuesta administrativa 401.
    requerir_administrador(
        request
    )
    raise AssertionError(
        "requerir_administrador debe interrumpir la solicitud"
    )


def _verificar_superficie_administrativa() -> None:
    """Aplica el kill switch común del Portal Developer."""

    if not administracion_activa():
        raise HTTPException(
            status_code=403,
            detail=(
                "Superficie administrativa "
                "no disponible."
            ),
        )


def _obtener_usuario_sesion_web(
    request: Request,
) -> UsuarioDeveloper | None:
    """Resuelve y revalida la identidad persistente de la sesión web."""

    identificador = request.cookies.get(
        "mrp_admin_session"
    )

    if not identificador:
        return None

    sesion = obtener_sesion_admin(
        identificador
    )

    if (
        sesion is None
        or not sesion.tiene_identidad
        or sesion.usuario_id is None
    ):
        if sesion is not None:
            eliminar_sesion_admin(
                identificador
            )
        return None

    cuenta = obtener_usuario_por_id(
        sesion.usuario_id
    )

    if (
        cuenta is None
        or not cuenta.activo
        or cuenta.usuario != sesion.usuario
        or cuenta.rol != sesion.rol
        or cuenta.revision_seguridad
        != sesion.revision_seguridad
    ):
        eliminar_sesion_admin(
            identificador
        )
        return None

    return cuenta


def _sesion_web_admin_valida(
    request: Request,
) -> bool:
    """Mantiene el helper histórico sobre la validación R6."""

    return (
        _obtener_usuario_sesion_web(
            request
        )
        is not None
    )


def _nombre_presentacion_developer(
    nombre_visible: str,
) -> str:
    """Normaliza el nombre únicamente para presentación visual."""

    limpio = " ".join(
        nombre_visible.strip().split()
    )

    if not limpio:
        return ""

    if limpio == limpio.casefold():
        return " ".join(
            parte[:1].upper() + parte[1:]
            for parte in limpio.split()
        )

    return limpio


def _iniciales_nombre_developer(
    nombre_visible: str,
) -> str:
    """Obtiene hasta dos iniciales seguras para la identidad visual."""

    partes = [
        parte
        for parte in nombre_visible.strip().split()
        if parte
    ]

    if not partes:
        return "?"

    if len(partes) == 1:
        return partes[0][0].upper()

    return (
        partes[0][0]
        + partes[-1][0]
    ).upper()


def _revision_assets_developer() -> str:
    """Genera una revisión local a partir de los assets Developer."""

    rutas = (
        Path("app/static/css/developer-portal.css"),
        Path("app/static/js/developer_portal.js"),
        Path("app/static/js/developer_forms.js"),
    )

    revisiones = []

    for ruta_asset in rutas:
        try:
            revisiones.append(
                str(ruta_asset.stat().st_mtime_ns)
            )
        except OSError:
            revisiones.append("0")

    return "-".join(revisiones)


def _identificador_sesion_developer(
    request: Request,
) -> str:
    """Obtiene la cookie de sesión sin exponerla."""

    return (
        request.cookies.get(
            "mrp_admin_session",
            "",
        ).strip()
    )


def _token_csrf_developer(
    request: Request,
) -> str:
    """Genera el CSRF correspondiente a la sesión humana actual."""

    return token_csrf_para_sesion(
        _identificador_sesion_developer(
            request
        )
    )


def _validar_csrf_developer(
    request: Request,
    token: str | None,
) -> None:
    """Exige CSRF válido para operaciones humanas POST."""

    sesion = _identificador_sesion_developer(
        request
    )

    if not validar_token_csrf_sesion(
        sesion,
        token,
    ):
        registrar_evento(
            level="WARNING",
            event="dev.csrf.denied",
            component="security.developer",
            outcome="denied",
            metadata={
                "endpoint": request.url.path,
            },
        )

        raise HTTPException(
            status_code=403,
            detail="Validación de seguridad requerida.",
        )


def _requerir_permiso_developer(
    request: Request,
    permiso: PermisoDeveloper,
):
    """Autoriza una operación humana mediante RBAC server-side."""

    _verificar_superficie_administrativa()

    usuario = _obtener_usuario_sesion_web(
        request
    )

    if usuario is None:
        raise HTTPException(
            status_code=401,
            detail="Sesión Developer requerida.",
        )

    if (
        usuario.debe_cambiar_password
        and request.url.path
        != "/dev/perfil/password"
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "Debes cambiar la contraseña temporal "
                "antes de continuar."
            ),
        )

    if not rol_tiene_permiso(
        usuario.rol,
        permiso,
    ):
        registrar_evento(
            level="WARNING",
            event="dev.authorization.denied",
            component="security.developer",
            outcome="denied",
            metadata={
                "endpoint": request.url.path,
                "permission": permiso.value,
            },
        )

        raise HTTPException(
            status_code=403,
            detail="La cuenta no tiene permiso para esta operación.",
        )

    return usuario


def _revalidar_operacion_developer(
    request: Request,
    usuario,
    password: str | None,
) -> None:
    """Exige nuevamente la contraseña humana en operaciones sensibles."""

    if not revalidar_password_usuario(
        usuario,
        password,
    ):
        registrar_evento(
            level="WARNING",
            event="dev.revalidation.denied",
            component="security.developer",
            outcome="denied",
            metadata={
                "endpoint": request.url.path,
            },
        )

        raise HTTPException(
            status_code=403,
            detail="Revalidación de identidad incorrecta.",
        )


def _etiqueta_rol_gestion_developer(
    rol: RolDeveloper,
) -> str:
    """Devuelve la etiqueta humana utilizada en la gestión de usuarios."""

    return {
        RolDeveloper.PROPIETARIO: "Propietario",
        RolDeveloper.ADMINISTRADOR: "Administrador",
        RolDeveloper.OPERADOR: "Operador",
        RolDeveloper.AUDITOR: "Auditor",
    }[rol]


def _opcion_rol_developer(
    rol: RolDeveloper,
) -> dict[str, str]:
    """Convierte un rol asignable en una opción segura para la interfaz."""

    return {
        "value": rol.value,
        "label": _etiqueta_rol_gestion_developer(
            rol
        ),
    }


def _usuario_gestionable_por_actor(
    actor: UsuarioDeveloper,
    objetivo: UsuarioDeveloper,
) -> bool:
    """Replica solo la visibilidad de acciones; el dominio revalida la operación."""

    if (
        objetivo.es_propietario
        or objetivo.identificador
        == actor.identificador
    ):
        return False

    if actor.rol is RolDeveloper.PROPIETARIO:
        return True

    if actor.rol is not RolDeveloper.ADMINISTRADOR:
        return False

    return (
        objetivo.rol
        is not RolDeveloper.ADMINISTRADOR
    )


def _filas_gestion_usuarios_developer(
    actor: UsuarioDeveloper,
) -> list[dict[str, object]]:
    """Prepara el directorio de usuarios sin exponer hashes ni secretos."""

    roles_actor = roles_asignables_por_actor(
        actor
    )

    filas: list[dict[str, object]] = []

    for usuario in listar_usuarios_developer():
        gestionable = (
            _usuario_gestionable_por_actor(
                actor,
                usuario,
            )
        )

        roles_cambio = [
            _opcion_rol_developer(
                rol
            )
            for rol in roles_actor
            if (
                gestionable
                and rol is not usuario.rol
            )
        ]

        filas.append(
            {
                "usuario": usuario,
                "nombre": _nombre_presentacion_developer(
                    usuario.nombre_visible
                ),
                "iniciales": _iniciales_nombre_developer(
                    usuario.nombre_visible
                ),
                "rol_label": _etiqueta_rol_gestion_developer(
                    usuario.rol
                ),
                "avatar_url": (
                    (
                        "/dev/perfil/avatar/"
                        + usuario.identificador
                    )
                    if usuario.avatar_relativo
                    else None
                ),
                "es_actual": (
                    usuario.identificador
                    == actor.identificador
                ),
                "gestionable": gestionable,
                "roles_cambio": roles_cambio,
            }
        )

    return filas


def _mensaje_resultado_usuarios(
    codigo: str | None,
) -> dict[str, str] | None:
    """Traduce códigos no sensibles de redirección a mensajes de interfaz."""

    mensajes = {
        "creado": {
            "tipo": "success",
            "texto": (
                "La cuenta fue creada. Copia la "
                "contraseña temporal antes de salir de esta página."
            ),
        },
        "revalidacion-invalida": {
            "tipo": "danger",
            "texto": (
                "La contraseña actual no coincide. "
                "No se realizó ningún cambio."
            ),
        },
        "crear-invalido": {
            "tipo": "danger",
            "texto": (
                "No fue posible crear la cuenta. Revisa "
                "el usuario, nombre y rol seleccionados."
            ),
        },
        "datos-invalidos": {
            "tipo": "danger",
            "texto": (
                "El nombre visible no cumple los requisitos."
            ),
        },
        "cuenta-actualizada": {
            "tipo": "success",
            "texto": "Los cambios de la cuenta fueron guardados.",
        },
        "sin-cambios": {
            "tipo": "secondary",
            "texto": "No se solicitaron cambios para esta cuenta.",
        },
        "editar-invalido": {
            "tipo": "danger",
            "texto": "No fue posible aplicar los cambios solicitados.",
        },
        "datos-actualizados": {
            "tipo": "success",
            "texto": "El nombre visible fue actualizado.",
        },
        "rol-invalido": {
            "tipo": "danger",
            "texto": "El rol seleccionado no es válido.",
        },
        "rol-actualizado": {
            "tipo": "success",
            "texto": (
                "El rol fue actualizado y las sesiones "
                "anteriores de la cuenta fueron revocadas."
            ),
        },
        "estado-actualizado": {
            "tipo": "success",
            "texto": (
                "El estado de la cuenta fue actualizado y "
                "sus sesiones anteriores fueron revocadas."
            ),
        },
        "eliminar-confirmacion": {
            "tipo": "danger",
            "texto": (
                "La confirmación no coincide. "
                "La cuenta no fue eliminada."
            ),
        },
        "usuario-eliminado": {
            "tipo": "success",
            "texto": (
                "La cuenta fue eliminada definitivamente."
            ),
        },
        "password-temporal": {
            "tipo": "warning",
            "texto": (
                "La contraseña fue restablecida. Copia la "
                "nueva credencial temporal antes de salir de esta página."
            ),
        },
    }

    return mensajes.get(
        str(codigo or "")
    )


def _contexto_developer(
    request: Request,
    *,
    autenticado: bool,
    usuario: UsuarioDeveloper | None = None,
    pagina_activa: str = "resumen",
) -> dict[str, object]:
    """Construye el contexto visual común del shell Developer."""

    etiquetas_rol = {
        "owner": "Propietario",
        "admin": "Administrador",
        "operator": "Operador",
        "auditor": "Auditor",
    }

    return {
        "pagina_activa": pagina_activa,
        "version": APP_VERSION,
        "app_author": APP_AUTHOR,
        "dev_assets_revision": _revision_assets_developer(),
        "dev_autenticado": autenticado,
        "dev_csrf_token": (
            _token_csrf_developer(request)
            if autenticado
            else ""
        ),
        "dev_permisos": (
            sorted(
                permiso.value
                for permiso in permisos_para_rol(
                    usuario.rol
                )
            )
            if usuario is not None
            else []
        ),
        "dev_sesiones_activas": (
            len(
                obtener_sesiones_developer_activas()
            )
            if autenticado
            else 0
        ),
        "dev_usuario": usuario,
        "dev_nombre_presentacion": (
            _nombre_presentacion_developer(
                usuario.nombre_visible
            )
            if usuario is not None
            else None
        ),
        "dev_iniciales": (
            _iniciales_nombre_developer(
                usuario.nombre_visible
            )
            if usuario is not None
            else None
        ),
        "dev_avatar_url": (
            (
                "/dev/perfil/avatar/"
                + usuario.identificador
            )
            if (
                usuario is not None
                and usuario.avatar_relativo
            )
            else None
        ),
        "dev_rol_etiqueta": (
            etiquetas_rol.get(
                usuario.rol.value,
                usuario.rol.value,
            )
            if usuario is not None
            else None
        ),
    }


def _render_pagina_developer(
    request: Request,
    *,
    usuario: UsuarioDeveloper,
    plantilla: str,
    pagina_activa: str,
):
    """Renderiza una página humana autenticada del Portal Developer."""

    contexto = _contexto_developer(
        request,
        autenticado=True,
        usuario=usuario,
        pagina_activa=pagina_activa,
    )
    contexto["estado_dev"] = (
        construir_estado_centro_desarrollo()
    )

    return templates.TemplateResponse(
        request=request,
        name=plantilla,
        context=contexto,
    )


def _render_pagina_developer_autenticada(
    request: Request,
    *,
    plantilla: str,
    pagina_activa: str,
    permiso: PermisoDeveloper | None = None,
):
    """Exige sesión humana antes de renderizar una página Developer."""

    _verificar_superficie_administrativa()

    usuario = _obtener_usuario_sesion_web(
        request
    )

    if usuario is None:
        return RedirectResponse(
            url="/dev",
            status_code=303,
        )

    if (
        usuario.debe_cambiar_password
        and pagina_activa != "perfil"
    ):
        return RedirectResponse(
            url="/dev/perfil?cambio_password=obligatorio",
            status_code=303,
        )

    if (
        permiso is not None
        and not rol_tiene_permiso(
            usuario.rol,
            permiso,
        )
    ):
        raise HTTPException(
            status_code=403,
            detail=(
                "La cuenta Developer no tiene permiso "
                "para acceder a esta sección."
            ),
        )

    return _render_pagina_developer(
        request,
        usuario=usuario,
        plantilla=plantilla,
        pagina_activa=pagina_activa,
    )


def _render_login_developer(
    request: Request,
    *,
    error: str | None = None,
    status_code: int = 200,
    usuario_recordado: str = "",
):
    """Renderiza el acceso humano sin persistir credenciales."""

    contexto = _contexto_developer(
        request,
        autenticado=False
    )
    contexto["error"] = error
    contexto["usuario_recordado"] = usuario_recordado

    return templates.TemplateResponse(
        request=request,
        name="developer/dev_login.html",
        context=contexto,
        status_code=status_code,
    )


def _render_centro_desarrollo(
    request: Request,
    *,
    usuario: UsuarioDeveloper | None = None,
):
    """Renderiza el Centro Developer para sesión humana o Bearer legado."""

    contexto = _contexto_developer(
        request,
        autenticado=usuario is not None,
        usuario=usuario,
    )
    contexto["estado_dev"] = (
        construir_estado_centro_desarrollo()
    )

    return templates.TemplateResponse(
        request=request,
        name="developer/dev_development_center.html",
        context=contexto,
    )
