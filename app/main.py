"""Punto de entrada principal de la aplicación Calculadora de Pensión CSS.

Este módulo configura FastAPI, registra los recursos estáticos,
las plantillas HTML y los endpoints utilizados actualmente por
la interfaz y por los servicios de cálculo.
"""

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.modelos.simulacion import (
    DatosCuotas,
    DatosSalario,
    ResumenCuotas,
    ResumenSalario,
)
from app.servicios.proyeccion_cuotas import analizar_cuotas
from app.servicios.proyeccion_salarios import normalizar_salario


# ============================================================
# Rutas internas de la aplicación
# ============================================================

# Directorio base del paquete "app". Se utiliza para construir
# rutas absolutas independientes del directorio desde el cual
# se ejecute Uvicorn.
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

# Expone CSS, JavaScript, imágenes y otros recursos bajo /static.
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

# Configura Jinja2 para renderizar las páginas HTML.
templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# ============================================================
# Rutas de interfaz
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    """Muestra la página principal de la aplicación."""

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "pagina_activa": "inicio",
            "version": "0.1.0",
        },
    )


@app.get("/simulacion", response_class=HTMLResponse)
async def simulacion(request: Request):
    """Muestra el asistente para crear una nueva simulación."""

    return templates.TemplateResponse(
        request=request,
        name="simulacion.html",
        context={
            "pagina_activa": "simulacion",
            "version": "0.1.0",
        },
    )


@app.get("/comparar", response_class=HTMLResponse)
async def comparar(request: Request):
    """Muestra la página destinada al comparador de sistemas."""

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
    """Analiza las cuotas reales y las cuotas proyectadas.

    La lógica se mantiene fuera del endpoint y se delega al
    servicio ``analizar_cuotas`` para conservar la separación
    entre la API y el motor de cálculo.
    """

    try:
        return analizar_cuotas(datos)

    except ValueError as error:
        # Los errores de reglas de negocio se devuelven como
        # respuestas 422 para que la interfaz pueda mostrarlos.
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# API — Salario
# ============================================================

@app.post(
    "/api/simulacion/salario",
    response_model=ResumenSalario,
)
async def calcular_resumen_salario(
    datos: DatosSalario,
):
    """Normaliza un salario a diferentes periodicidades."""

    try:
        return normalizar_salario(datos)

    except ValueError as error:
        # Mantiene un formato de error consistente con el
        # endpoint utilizado para analizar cuotas.
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error


# ============================================================
# Estado del servicio
# ============================================================

@app.get("/salud")
async def salud():
    """Devuelve información mínima para verificar que la API funciona."""

    return {
        "estado": "ok",
        "servicio": "Calculadora de Pensión CSS",
        "version": "0.1.0",
    }