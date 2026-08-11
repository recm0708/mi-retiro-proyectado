"""Servicios para normalizar y posteriormente proyectar salarios.

Actualmente este módulo convierte un salario ingresado en cualquiera
de las periodicidades admitidas a equivalentes semanal, quincenal,
mensual y anual.
"""

from app.modelos.simulacion import (
    DatosSalario,
    ResumenSalario,
)


# ============================================================
# Normalización salarial
# ============================================================

def normalizar_salario(
    datos: DatosSalario,
) -> ResumenSalario:
    """Convierte un salario a todas las periodicidades soportadas.

    Primero se obtiene un salario anual equivalente. A partir de
    ese valor común se calculan las demás periodicidades para evitar
    conversiones encadenadas y diferencias innecesarias de redondeo.
    """

    monto = datos.monto

    # Normaliza el dato original a un equivalente anual.
    if datos.periodicidad == "SEMANAL":
        salario_anual = monto * 52

    elif datos.periodicidad == "QUINCENAL":
        salario_anual = monto * 24

    elif datos.periodicidad == "MENSUAL":
        salario_anual = monto * 12

    elif datos.periodicidad == "ANUAL":
        salario_anual = monto

    else:
        # Esta validación normalmente será interceptada primero
        # por Pydantic, pero se conserva como protección del servicio.
        raise ValueError(
            "La periodicidad salarial indicada no es válida."
        )

    # Todas las demás equivalencias se derivan del valor anual.
    salario_mensual = salario_anual / 12
    salario_quincenal = salario_anual / 24
    salario_semanal = salario_anual / 52

    # Los valores mostrados y enviados a la interfaz se expresan
    # con dos decimales monetarios.
    return ResumenSalario(
        monto_original=round(monto, 2),
        periodicidad_original=datos.periodicidad,
        salario_semanal=round(salario_semanal, 2),
        salario_quincenal=round(salario_quincenal, 2),
        salario_mensual=round(salario_mensual, 2),
        salario_anual=round(salario_anual, 2),
    )