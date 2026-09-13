"""Composition root de Mi Retiro Proyectado.

Configura FastAPI, middleware, recursos compartidos y registra
los routers HTTP de Asegurado y Developer sin concentrar sus
handlers dentro de este módulo.
"""

from pathlib import Path
from time import monotonic, time_ns

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
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# ============================================================
# Rutas internas de la aplicación
# ============================================================

# Directorio base del paquete "app".
BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# Configuración de FastAPI
# ============================================================


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

    # En desarrollo, el navegador debe consumir siempre el HTML, CSS y
    # JavaScript correspondientes al árbol de trabajo actual. Esto evita
    # combinar una plantilla nueva con recursos estáticos almacenados de
    # una revisión anterior.
    if modo_desarrollo_activo():
        content_type = respuesta.headers.get(
            "content-type",
            "",
        )

        if (
            request.url.path.startswith("/static/")
            or content_type.startswith("text/html")
        ):
            respuesta.headers["Cache-Control"] = (
                "no-store, no-cache, must-revalidate, max-age=0"
            )
            respuesta.headers["Pragma"] = "no-cache"
            respuesta.headers["Expires"] = "0"

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

# Los recursos locales reciben una revisión de URL.
# En desarrollo cambia con cada proceso para evitar combinar
# HTML actual con CSS o JavaScript almacenados anteriormente.
# Fuera de desarrollo utiliza la versión publicada.
STATIC_REVISION = (
    str(time_ns())
    if modo_desarrollo_activo()
    else APP_VERSION
)

templates.env.globals.update(
    static_revision=STATIC_REVISION,
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
async def favicon_aplicacion():
    """Entrega el favicon oficial de la aplicación."""

    return FileResponse(
        path=(
            BASE_DIR
            / "static"
            / "shared"
            / "img"
            / "brand"
            / "favicon.ico"
        ),
        media_type="image/x-icon",
        headers={
            "Cache-Control": "public, max-age=86400",
        },
    )


# ============================================================
# Rutas de interfaz
# ============================================================


# ============================================================
# API — Cuotas
# ============================================================


# ============================================================
# API — Historial salarial
# ============================================================


# ============================================================
# API — Detalle salarial del año actual
# ============================================================


# ============================================================
# API — Referencia personal de Mi Retiro Seguro
# ============================================================


# ============================================================
# API — Ficha Digital de Mi Caja Digital
# ============================================================


# ============================================================
# API — Salario actual
# ============================================================


# ============================================================
# API — Proyección salarial
# ============================================================


# ============================================================
# API — Línea temporal
# ============================================================


# ============================================================
# API — Retiro
# ============================================================


# ============================================================
# API — SEBD: Pensión de Vejez Normal
# ============================================================


# ============================================================
# API — Resultados integrados SEBD
# ============================================================


# ============================================================
# API — SEBD: clasificación y modalidades generales
# ============================================================


# ============================================================
# API — Subsistema Mixto: evaluación preliminar
# ============================================================


# ============================================================
# API — SUCGS: cálculo por capas hasta el artículo 197
# ============================================================


# ============================================================
# API — Comparación transversal de escenarios
# ============================================================


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

# ============================================================
# Registro final de routers por portal
# ============================================================
# Los imports se difieren hasta que FastAPI, templates y globals
# compartidos han terminado de inicializarse.
from app.portals.asegurado.router import (
    configure_router as configure_asegurado_router,
    router as asegurado_router,
)
from app.portals.developer.router import (
    configure_router as configure_developer_router,
    router as developer_router,
)

configure_asegurado_router(
    templates_value=templates,
)

configure_developer_router(
    templates_value=templates,
)

if len(asegurado_router.routes) != 24:
    raise RuntimeError(
        'Router Asegurado incompleto: '
        + str(len(asegurado_router.routes))
    )

if len(developer_router.routes) != 29:
    raise RuntimeError(
        'Router Developer incompleto: '
        + str(len(developer_router.routes))
    )

app.include_router(asegurado_router)
app.include_router(developer_router)
