from pathlib import Path

from fastapi import FastAPI, Request
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.modelos.simulacion import DatosCuotas, ResumenCuotas
from app.servicios.proyeccion_cuotas import analizar_cuotas

BASE_DIR = Path(__file__).resolve().parent


app = FastAPI(
    title="Calculadora de Pensión CSS",
    description=(
        "Aplicación web para estimar y comparar pensiones "
        "de jubilación de la Caja de Seguro Social de Panamá."
    ),
    version="0.1.0",
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)


templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
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
    return templates.TemplateResponse(
        request=request,
        name="comparar.html",
        context={
            "pagina_activa": "comparar",
            "version": "0.1.0",
        },
    )

@app.post(
    "/api/simulacion/cuotas",
    response_model=ResumenCuotas,
)
async def calcular_resumen_cuotas(
    datos: DatosCuotas,
):
    try:
        return analizar_cuotas(datos)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

@app.get("/salud")
async def salud():
    return {
        "estado": "ok",
        "servicio": "Calculadora de Pensión CSS",
        "version": "0.1.0",
    }