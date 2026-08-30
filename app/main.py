"""Punto de entrada principal de la aplicación Mi Retiro Proyectado.

Este módulo configura FastAPI, registra los recursos estáticos,
las plantillas HTML y los endpoints utilizados por la interfaz
y por los servicios de cálculo.
"""

from pathlib import Path
from time import monotonic

from app.core.pdf_files import leer_pdf_subido
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
)

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models.simulation import (
    DatosCuotas,
    DatosHistorialSalarial,
    DatosDetalleAnioActual,
    DatosProyeccionSalario,
    DatosSalario,
    ResumenCuotas,
    ResumenHistorialSalarial,
    ResumenDetalleAnioActual,
    ResumenReferenciaMiRetiroSeguro,
    ResumenFichaDigital,
    ResumenFechaReferencia,
    ResumenProyeccionSalario,
    ResumenSalario,
    DatosLineaTiempo,
    ResumenLineaTiempo,
    DatosRetiro,
    ResumenRetiro,
)
from app.services.salary_history import (
    analizar_historial_salarial,
)
from app.services.current_year_detail import (
    analizar_detalle_anio_actual,
)
from app.services.timeline import (
    construir_linea_tiempo,
)
from app.services.mi_retiro_seguro_reference import (
    analizar_comprobante_pdf,
)
from app.services.ficha_digital import (
    analizar_ficha_digital_pdf,
)
from app.services.reference_date import (
    obtener_fecha_referencia_confiable,
)
from app.services.contribution_projection import analizar_cuotas
from app.services.salary_projection import (
    normalizar_salario,
    proyectar_salario,
)
from app.services.retirement import (
    analizar_retiro,
)
from app.models.pension import (
    DatosCalculoSEBD,
    DatosCalculoSEBDNormal,
    DatosResultadoSEBD,
    DatosResultadoSEBDNormal,
    ResumenCalculoSEBD,
    ResumenCalculoSEBDNormal,
    ResumenResultadoSEBD,
    ResumenResultadoSEBDNormal,
    DatosCalculoMixto,
    DatosResultadoMixto,
    ResumenCalculoMixto,
    ResumenResultadoMixto,
    DatosCalculoSUCGS,
    DatosResultadoSUCGS,
    ResumenCalculoSUCGS,
    ResumenResultadoSUCGS,
)
from app.engines.sebd import (
    calcular_sebd_normal,
)
from app.engines.sebd_modalidades import (
    calcular_sebd,
)
from app.engines.mixto import (
    calcular_mixto,
)
from app.engines.sucgs import (
    calcular_sucgs,
)
from app.services.results import (
    calcular_resultado_sebd_normal,
)
from app.services.sebd_results import (
    calcular_resultado_sebd,
)
from app.services.mixto_results import (
    calcular_resultado_mixto,
)
from app.services.sucgs_results import (
    calcular_resultado_sucgs,
)
from app.models.comparacion import (
    DatosComparacionEscenarios,
    ResumenComparacionEscenarios,
)
from app.services.comparator import (
    comparar_escenarios,
)

# ============================================================
# Rutas internas de la aplicación
# ============================================================

# Directorio base del paquete "app".
BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# Configuración de FastAPI
# ============================================================
from app.services.regulatory_sources import construir_catalogo_metodologia
from app.services.calculation_guide import construir_guia_calculo
from app.services.development_center import construir_estado_centro_desarrollo
from app.core.admin_security import (
    requerir_administrador,
    administracion_activa,
)
from app.core.admin_session import (
    crear_sesion_admin,
    obtener_sesion_admin,
    eliminar_sesion_admin,
)
from app.core.developer_provisioning import (
    autenticar_usuario_developer,
)
from app.core.developer_store import (
    UsuarioDeveloper,
    obtener_usuario_por_id,
)


app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)


# ============================================================
# Developer Diagnostics — exclusivo de desarrollo
# ============================================================

@app.middleware("http")
async def registrar_diagnostico_http(request: Request, call_next):
    """Observa una solicitud sin leer ni persistir su cuerpo."""

    if not modo_desarrollo_activo():
        return await call_next(request)

    operacion = clasificar_operacion_http(request.url.path)
    if operacion is None:
        return await call_next(request)

    token = establecer_correlacion()
    inicio = monotonic()
    try:
        try:
            respuesta = await call_next(request)
        except Exception as error:
            registrar_excepcion(
                event="http.request",
                component="fastapi",
                error=error,
                duration_ms=(monotonic() - inicio) * 1000,
                metadata={
                    "method": request.method,
                    "operation": operacion,
                },
            )
            raise

        status_code = int(respuesta.status_code)
        if status_code >= 500:
            level = "ERROR"
            outcome = "server_error"
        elif status_code >= 400:
            level = "WARNING"
            outcome = "client_error"
        else:
            level = "INFO"
            outcome = "success"

        registrar_evento(
            level=level,
            event="http.request",
            component="fastapi",
            outcome=outcome,
            duration_ms=(monotonic() - inicio) * 1000,
            metadata={
                "method": request.method,
                "operation": operacion,
                "status_code": status_code,
            },
        )

        correlation_id = correlacion_actual()
        if correlation_id is not None:
            respuesta.headers["X-Correlation-ID"] = correlation_id
        return respuesta
    finally:
        restablecer_correlacion(token)


# ============================================================
# Cabeceras defensivas para la aplicación local
# ============================================================

@app.middleware("http")
async def agregar_cabeceras_defensivas(request: Request, call_next):
    """Reduce exposición innecesaria del navegador sin alterar cálculos."""

    respuesta = await call_next(request)
    respuesta.headers.setdefault("X-Content-Type-Options", "nosniff")
    respuesta.headers.setdefault("X-Frame-Options", "DENY")
    respuesta.headers.setdefault("Referrer-Policy", "no-referrer")
    respuesta.headers.setdefault(
        "Permissions-Policy",
        "camera=(), microphone=(), geolocation=()",
    )
    respuesta.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data:; "
        "font-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'",
    )

    # Las respuestas del asistente pueden contener datos personales, salariales
    # o previsionales. Se evita su reutilización desde la caché HTTP.
    if (
        request.url.path.startswith("/api/simulacion/")
        or request.url.path == "/dev"
        or request.url.path.startswith("/dev/")
    ):
        respuesta.headers["Cache-Control"] = "no-store"

    return respuesta


# ============================================================
# Recursos estáticos y plantillas
# ============================================================

# Expone CSS, JavaScript, imágenes y otros recursos.
app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "static",
    ),
    name="static",
)

# Configura Jinja2 para renderizar páginas HTML.
templates = Jinja2Templates(
    directory=BASE_DIR / "templates",
)

templates.env.globals.update(
    app_name=APP_NAME,
    app_subtitle=APP_SUBTITLE,
    app_author=APP_AUTHOR,
    app_version=APP_VERSION,
    mi_caja_digital_url=MI_CAJA_DIGITAL_URL,
)


# ============================================================
# Recursos del navegador
# ============================================================

@app.get(
    "/favicon.ico",
    include_in_schema=False,
)
async def favicon_temporal():
    """Evita un 404 mientras se integra el favicon definitivo."""

    return Response(
        status_code=204,
        headers={
            "Cache-Control": "no-store",
        },
    )


# ============================================================
# Rutas de interfaz
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def inicio(
    request: Request,
):
    """Muestra la página principal."""

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "pagina_activa": "inicio",
            "version": APP_VERSION,
        },
    )


@app.get(
    "/simulacion",
    response_class=HTMLResponse,
)
async def simulacion(
    request: Request,
):
    """Muestra el asistente de simulación."""

    return templates.TemplateResponse(
        request=request,
        name="simulation.html",
        context={
            "pagina_activa": "simulacion",
            "version": APP_VERSION,
        },
    )


@app.get(
    "/comparar",
    response_class=HTMLResponse,
)
async def comparar(
    request: Request,
):
    """Muestra la página del comparador."""

    return templates.TemplateResponse(
        request=request,
        name="comparison.html",
        context={
            "pagina_activa": "comparar",
            "version": APP_VERSION,
        },
    )


@app.get(
    "/metodologia",
    response_class=HTMLResponse,
)
async def metodologia(
    request: Request,
):
    """Muestra la metodología transversal y las fuentes oficiales."""

    return templates.TemplateResponse(
        request=request,
        name="methodology.html",
        context={
            "pagina_activa": "metodologia",
            "version": APP_VERSION,
            "catalogo": construir_catalogo_metodologia(),
        },
    )


@app.get(
    "/como-se-calcula",
    response_class=HTMLResponse,
)
async def como_se_calcula(
    request: Request,
):
    """Explica públicamente el procedimiento implementado por los motores."""

    return templates.TemplateResponse(
        request=request,
        name="calculation_guide.html",
        context={
            "pagina_activa": "como_se_calcula",
            "version": APP_VERSION,
            "catalogo": construir_catalogo_metodologia(),
            "guia": construir_guia_calculo(),
        },
    )


@app.get(
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
        return _render_pagina_developer(
            request,
            usuario=usuario,
            plantilla="dev_dashboard.html",
            pagina_activa="resumen",
        )

    return _render_login_developer(request)


@app.get(
    "/dev/diagnostico",
    response_class=HTMLResponse,
)
async def diagnostico_developer(request: Request):
    """Muestra el autodiagnóstico técnico del Portal Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="dev_diagnostics.html",
        pagina_activa="diagnostico",
    )


@app.get(
    "/dev/eventos",
    response_class=HTMLResponse,
)
async def eventos_developer(request: Request):
    """Muestra los eventos de observabilidad del Portal Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="dev_events.html",
        pagina_activa="eventos",
    )


@app.get(
    "/dev/archivos",
    response_class=HTMLResponse,
)
async def archivos_developer(request: Request):
    """Muestra el inventario técnico del Portal Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="dev_files.html",
        pagina_activa="archivos",
    )


@app.post(
    "/dev/archivos/exportar",
)
async def exportar_archivos_developer(request: Request):
    """Descarga el ZIP diagnóstico sanitizado desde una sesión humana."""

    _verificar_superficie_administrativa()

    usuario = _obtener_usuario_sesion_web(request)

    if usuario is None:
        return RedirectResponse(
            url="/dev",
            status_code=303,
        )

    from fastapi.responses import FileResponse

    from app.services.development_center import (
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


@app.get(
    "/dev/mantenimiento",
    response_class=HTMLResponse,
)
async def mantenimiento_developer(request: Request):
    """Muestra la superficie de mantenimiento del Portal Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="dev_maintenance.html",
        pagina_activa="mantenimiento",
    )


@app.get(
    "/dev/privacidad",
    response_class=HTMLResponse,
)
async def privacidad_developer(request: Request):
    """Muestra los controles de privacidad del Portal Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="dev_privacy.html",
        pagina_activa="privacidad",
    )


@app.get(
    "/dev/perfil",
    response_class=HTMLResponse,
)
async def perfil_developer(request: Request):
    """Muestra la identidad y preferencias de la cuenta Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="dev_profile.html",
        pagina_activa="perfil",
    )


@app.get(
    "/dev/acceso-tecnico",
    response_class=HTMLResponse,
)
async def acceso_tecnico_developer(request: Request):
    """Muestra la superficie humana de credenciales técnicas Developer."""

    return _render_pagina_developer_autenticada(
        request,
        plantilla="dev_technical_access.html",
        pagina_activa="acceso_tecnico",
    )


@app.get(
    "/dev/login",
    include_in_schema=False,
)
async def login_administrativo_legacy():
    """Conserva la URL histórica y dirige al acceso humano canónico."""

    return RedirectResponse(
        url="/dev",
        status_code=303,
    )


@app.post(
    "/dev",
)
@app.post(
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
        )

    sesion = crear_sesion_admin(
        usuario_id=cuenta.identificador,
        usuario=cuenta.usuario,
        rol=cuenta.rol,
        revision_seguridad=(
            cuenta.revision_seguridad
        ),
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
        url="/dev",
        status_code=303,
    )
    respuesta.set_cookie(
        key="mrp_admin_session",
        value=sesion,
        httponly=True,
        samesite=ADMIN_COOKIE_SAMESITE,
        secure=ADMIN_COOKIE_SECURE,
        max_age=ADMIN_SESSION_MINUTES * 60,
        path="/dev",
    )
    return respuesta


@app.post("/dev/logout")
async def logout_administrativo(request: Request):
    """Cierra la sesión web Developer activa."""

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


@app.get(
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


def _contexto_developer(
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
):
    """Renderiza el acceso humano sin persistir credenciales."""

    contexto = _contexto_developer(
        autenticado=False
    )
    contexto["error"] = error

    return templates.TemplateResponse(
        request=request,
        name="dev_login.html",
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
        autenticado=usuario is not None,
        usuario=usuario,
    )
    contexto["estado_dev"] = (
        construir_estado_centro_desarrollo()
    )

    return templates.TemplateResponse(
        request=request,
        name="dev_development_center.html",
        context=contexto,
    )


# ============================================================
# API — Cuotas
# ============================================================

@app.post(
    "/api/simulacion/cuotas",
    response_model=ResumenCuotas,
)
async def calcular_resumen_cuotas(
    datos: DatosCuotas,
):
    """Analiza cuotas acreditadas y proyectadas."""

    try:
        return analizar_cuotas(
            datos,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# API — Historial salarial
# ============================================================

@app.post(
    "/api/simulacion/historial-salarial",
    response_model=ResumenHistorialSalarial,
)
async def calcular_resumen_historial_salarial(
    datos: DatosHistorialSalarial,
):
    """Valida y resume el historial salarial anual."""

    try:
        return analizar_historial_salarial(
            datos,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# API — Detalle salarial del año actual
# ============================================================

@app.post(
    "/api/simulacion/detalle-anio-actual",
    response_model=ResumenDetalleAnioActual,
)
async def calcular_detalle_anio_actual(
    datos: DatosDetalleAnioActual,
):
    """Valida salarios mensuales/quincenales del año actual."""

    try:
        return analizar_detalle_anio_actual(
            datos,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# API — Referencia personal de Mi Retiro Seguro
# ============================================================

@app.post(
    "/api/simulacion/referencia-mi-retiro-seguro",
    response_model=ResumenReferenciaMiRetiroSeguro,
)
async def analizar_referencia_mi_retiro_seguro(
    archivo: UploadFile = File(...),
):
    """Extrae una referencia variable desde un comprobante PDF personal.

    El archivo se procesa en memoria y no se persiste. La respuesta puede
    incluir identificadores opcionales cuando el PDF los etiqueta de forma
    inequívoca; el navegador solo los conserva durante la simulación actual.
    """

    contenido = await leer_pdf_subido(
        archivo,
        limite_bytes=8 * 1024 * 1024,
        etiqueta="el comprobante",
    )

    try:
        return analizar_comprobante_pdf(contenido)
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# API — Ficha Digital de Mi Caja Digital
# ============================================================

@app.post(
    "/api/simulacion/ficha-digital",
    response_model=ResumenFichaDigital,
)
async def analizar_ficha_digital(
    archivo: UploadFile = File(...),
):
    """Extrae salarios del año calendario actual desde una Ficha Digital.

    El archivo se procesa en memoria y no se persiste. La respuesta no
    contiene nombre, cédula ni número de seguro social ni períodos de
    años anteriores.
    """

    contenido = await leer_pdf_subido(
        archivo,
        limite_bytes=12 * 1024 * 1024,
        etiqueta="la Ficha Digital",
    )

    try:
        resumen = analizar_ficha_digital_pdf(contenido)
    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    referencia = obtener_fecha_referencia_confiable()
    resumen.fecha_referencia = referencia.fecha
    resumen.fecha_referencia_confiable = referencia.confiable
    resumen.fuente_fecha_referencia = referencia.fuente
    return resumen


@app.get(
    "/api/sistema/fecha-referencia",
    response_model=ResumenFechaReferencia,
)
def consultar_fecha_referencia():
    """Devuelve la fecha externa usada para controles de vigencia documental."""

    referencia = obtener_fecha_referencia_confiable()
    return ResumenFechaReferencia(
        fecha=referencia.fecha,
        confiable=referencia.confiable,
        fuente=referencia.fuente,
    )


# ============================================================
# API — Salario actual
# ============================================================

@app.post(
    "/api/simulacion/salario",
    response_model=ResumenSalario,
)
async def calcular_resumen_salario(
    datos: DatosSalario,
):
    """Normaliza el salario actual."""

    try:
        return normalizar_salario(
            datos,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# API — Proyección salarial
# ============================================================

@app.post(
    "/api/simulacion/proyeccion-salario",
    response_model=ResumenProyeccionSalario,
)
async def calcular_proyeccion_salario(
    datos: DatosProyeccionSalario,
):
    """Construye uno o varios escenarios salariales futuros."""

    try:
        return proyectar_salario(
            datos,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# API — Línea temporal
# ============================================================

@app.post(
    "/api/simulacion/linea-tiempo",
    response_model=ResumenLineaTiempo,
)
async def calcular_linea_tiempo(
    datos: DatosLineaTiempo,
):
    """Une información histórica y proyectada por año."""

    try:
        return construir_linea_tiempo(
            datos,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

# ============================================================
# API — Retiro
# ============================================================

@app.post(
    "/api/simulacion/retiro",
    response_model=ResumenRetiro,
)
async def calcular_retiro(
    datos: DatosRetiro,
):
    """Construye fechas y escenarios preliminares de retiro."""

    try:
        return analizar_retiro(
            datos,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

# ============================================================
# API — SEBD: Pensión de Vejez Normal
# ============================================================

@app.post(
    "/api/simulacion/sebd/normal",
    response_model=ResumenCalculoSEBDNormal,
)
async def calcular_pension_sebd_normal(
    datos: DatosCalculoSEBDNormal,
):
    """Calcula el desglose de la Pensión de Vejez Normal del SEBD."""

    try:
        return calcular_sebd_normal(
            datos,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# API — Resultados integrados SEBD
# ============================================================

@app.post(
    "/api/simulacion/resultados/sebd-normal",
    response_model=ResumenResultadoSEBDNormal,
)
async def calcular_resultado_integrado_sebd_normal(
    datos: DatosResultadoSEBDNormal,
):
    """Calcula SEBD normal a partir de los Pasos 1–5."""

    try:
        return calcular_resultado_sebd_normal(
            datos,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# API — SEBD: clasificación y modalidades generales
# ============================================================

@app.post(
    "/api/simulacion/sebd",
    response_model=ResumenCalculoSEBD,
)
async def calcular_pension_sebd(
    datos: DatosCalculoSEBD,
):
    """Clasifica y calcula la modalidad SEBD aplicable."""

    try:
        return calcular_sebd(datos)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


@app.post(
    "/api/simulacion/resultados/sebd",
    response_model=ResumenResultadoSEBD,
)
async def calcular_resultado_integrado_sebd(
    datos: DatosResultadoSEBD,
):
    """Clasifica y calcula SEBD a partir de los Pasos 1–5."""

    try:
        return calcular_resultado_sebd(datos)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# API — Subsistema Mixto: evaluación preliminar
# ============================================================

@app.post(
    "/api/simulacion/mixto",
    response_model=ResumenCalculoMixto,
)
async def calcular_pension_mixto(
    datos: DatosCalculoMixto,
):
    """Evalúa transición y componentes de retiro por vejez del Mixto."""

    try:
        return calcular_mixto(datos)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


@app.post(
    "/api/simulacion/resultados/mixto",
    response_model=ResumenResultadoMixto,
)
async def calcular_resultado_integrado_mixto(
    datos: DatosResultadoMixto,
):
    """Calcula el Mixto a partir de los Pasos 1–5 y datos explícitos CAP."""

    try:
        return calcular_resultado_mixto(datos)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# API — SUCGS: cálculo por capas hasta el artículo 197
# ============================================================

@app.post(
    "/api/simulacion/sucgs",
    response_model=ResumenCalculoSUCGS,
)
async def calcular_pension_sucgs(
    datos: DatosCalculoSUCGS,
):
    """Calcula SUCGS por capas hasta la garantía del artículo 197."""

    try:
        return calcular_sucgs(datos)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


@app.post(
    "/api/simulacion/resultados/sucgs",
    response_model=ResumenResultadoSUCGS,
)
async def calcular_resultado_integrado_sucgs(
    datos: DatosResultadoSUCGS,
):
    """Calcula SUCGS hasta el artículo 197 con el escenario del asistente."""

    try:
        return calcular_resultado_sucgs(datos)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# API — Comparación transversal de escenarios
# ============================================================

@app.post(
    "/api/simulacion/comparar-escenarios",
    response_model=ResumenComparacionEscenarios,
)
async def calcular_comparacion_escenarios(
    datos: DatosComparacionEscenarios,
):
    """Compara escenarios de retiro y salario sin duplicar fórmulas legales."""

    try:
        return comparar_escenarios(datos)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# Estado del servicio
# ============================================================

@app.get("/salud")
async def salud():
    """Permite verificar que el servicio está funcionando."""

    return {
        "estado": "ok",
        "servicio": "Mi Retiro Proyectado",
        "version": APP_VERSION,
    }
