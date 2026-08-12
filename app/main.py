"""Punto de entrada principal de la aplicación Calculadora de Pensión CSS.

Este módulo configura FastAPI, registra los recursos estáticos,
las plantillas HTML y los endpoints utilizados por la interfaz
y por los servicios de cálculo.
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.modelos.simulacion import (
    DatosCuotas,
    DatosHistorialSalarial,
    DatosProyeccionSalario,
    DatosSalario,
    ResumenCuotas,
    ResumenHistorialSalarial,
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
from app.servicios.linea_tiempo import (
    construir_linea_tiempo,
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


app = FastAPI(
    title="Calculadora de Pensión CSS",
    description=(
        "Aplicación web para estimar y comparar pensiones "
        "de jubilación de la Caja de Seguro Social de Panamá."
    ),
    version="0.1.0",
)


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
            "version": "0.1.0",
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
            "version": "0.1.0",
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
            "version": "0.1.0",
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
            "version": "0.1.0",
            "catalogo": construir_catalogo_metodologia(),
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
# API — Comparación transversal de escenarios (6F.1)
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
        "servicio": "Calculadora de Pensión CSS",
        "version": "0.1.0",
    }