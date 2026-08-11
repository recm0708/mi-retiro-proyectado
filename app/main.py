from fastapi import FastAPI

app = FastAPI(
    title="Calculadora de Pensión CSS",
    description=(
        "Aplicación web para estimar y comparar pensiones de jubilación "
        "de la Caja de Seguro Social de Panamá."
    ),
    version="0.1.0",
)


@app.get("/")
def inicio():
    return {
        "aplicacion": "Calculadora de Pensión CSS",
        "version": "0.1.0",
        "estado": "Proyecto iniciado correctamente",
    }


@app.get("/salud")
def salud():
    return {
        "estado": "ok",
        "servicio": "Calculadora de Pensión CSS",
    }