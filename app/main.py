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

# ============================================================
# Rutas internas de la aplicación
# ============================================================

# Directorio base del paquete "app".
BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# Configuración de FastAPI
# ============================================================

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