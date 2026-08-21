"""Punto de entrada principal de la aplicación Mi Retiro Proyectado.

Este módulo configura FastAPI, registra los recursos estáticos,
las plantillas HTML y los endpoints utilizados por la interfaz
y por los servicios de cálculo.
"""

from pathlib import Path
from time import monotonic

from app.core.archivos_pdf import leer_pdf_subido
from app.core.observabilidad import (
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
)

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.modelos.simulacion import (
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
from app.servicios.historial_salarios import (
    analizar_historial_salarial,
)
from app.servicios.detalle_anio_actual import (
    analizar_detalle_anio_actual,
)
from app.servicios.linea_tiempo import (
    construir_linea_tiempo,
)
from app.servicios.referencia_mi_retiro_seguro import (
    analizar_comprobante_pdf,
)
from app.servicios.ficha_digital import (
    analizar_ficha_digital_pdf,
)
from app.servicios.fecha_referencia import (
    obtener_fecha_referencia_confiable,
)
from app.servicios.proyeccion_cuotas import analizar_cuotas
from app.servicios.proyeccion_salarios import (
    normalizar_salario,
    proyectar_salario,
)
from app.servicios.retiro import (
    analizar_retiro,
)
from app.modelos.pension import (
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
from app.motores.sebd import (
    calcular_sebd_normal,
)
from app.motores.sebd_modalidades import (
    calcular_sebd,
)
from app.motores.mixto import (
    calcular_mixto,
)
from app.motores.sucgs import (
    calcular_sucgs,
)
from app.servicios.resultados import (
    calcular_resultado_sebd_normal,
)
from app.servicios.resultados_sebd import (
    calcular_resultado_sebd,
)
from app.servicios.resultados_mixto import (
    calcular_resultado_mixto,
)
from app.servicios.resultados_sucgs import (
    calcular_resultado_sucgs,
)
from app.modelos.comparacion import (
    DatosComparacionEscenarios,
    ResumenComparacionEscenarios,
)
from app.servicios.comparador import (
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
from app.servicios.fuentes_normativas import construir_catalogo_metodologia
from app.servicios.como_se_calcula import construir_guia_calculo


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
    if request.url.path.startswith("/api/simulacion/"):
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
        name="simulacion.html",
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
        name="comparar.html",
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
        name="metodologia.html",
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
        name="como_se_calcula.html",
        context={
            "pagina_activa": "como_se_calcula",
            "version": APP_VERSION,
            "catalogo": construir_catalogo_metodologia(),
            "guia": construir_guia_calculo(),
        },
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
