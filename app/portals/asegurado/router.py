"""Router HTTP del Portal Asegurado."""

from fastapi import APIRouter
from app.portals.asegurado.pdf_files import leer_pdf_subido
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
from app.services.regulatory_sources import construir_catalogo_metodologia
from app.services.calculation_guide import construir_guia_calculo

router = APIRouter()

templates = None

def configure_router(*, templates_value) -> None:
    """Inyecta dependencias compartidas desde el composition root."""
    global templates
    templates = templates_value

@router.get(
    "/",
    response_class=HTMLResponse,
)
async def inicio(
    request: Request,
):
    """Muestra la página principal."""

    return templates.TemplateResponse(
        request=request,
        name="asegurado/index.html",
        context={
            "pagina_activa": "inicio",
            "version": APP_VERSION,
        },
    )


@router.get(
    "/simulacion",
    response_class=HTMLResponse,
)
async def simulacion(
    request: Request,
):
    """Muestra el asistente de simulación."""

    return templates.TemplateResponse(
        request=request,
        name="asegurado/simulation.html",
        context={
            "pagina_activa": "simulacion",
            "version": APP_VERSION,
        },
    )


@router.get(
    "/comparar",
    response_class=HTMLResponse,
)
async def comparar(
    request: Request,
):
    """Muestra la página del comparador."""

    return templates.TemplateResponse(
        request=request,
        name="asegurado/comparison.html",
        context={
            "pagina_activa": "comparar",
            "version": APP_VERSION,
        },
    )


@router.get(
    "/metodologia",
    response_class=HTMLResponse,
)
async def metodologia(
    request: Request,
):
    """Muestra la metodología transversal y las fuentes oficiales."""

    return templates.TemplateResponse(
        request=request,
        name="asegurado/methodology.html",
        context={
            "pagina_activa": "metodologia",
            "version": APP_VERSION,
            "catalogo": construir_catalogo_metodologia(),
        },
    )


@router.get(
    "/como-se-calcula",
    response_class=HTMLResponse,
)
async def como_se_calcula(
    request: Request,
):
    """Explica públicamente el procedimiento implementado por los motores."""

    return templates.TemplateResponse(
        request=request,
        name="asegurado/calculation_guide.html",
        context={
            "pagina_activa": "como_se_calcula",
            "version": APP_VERSION,
            "catalogo": construir_catalogo_metodologia(),
            "guia": construir_guia_calculo(),
        },
    )


@router.post(
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


@router.post(
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


@router.post(
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


@router.post(
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


@router.post(
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


@router.get(
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


@router.post(
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


@router.post(
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


@router.post(
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


@router.post(
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


@router.post(
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


@router.post(
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


@router.post(
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


@router.post(
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


@router.post(
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


@router.post(
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


@router.post(
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


@router.post(
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


@router.post(
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
