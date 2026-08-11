from app.modelos.simulacion import (
    DatosSalario,
    ResumenSalario,
)

def normalizar_salario(
    datos: DatosSalario,
) -> ResumenSalario:
    monto = datos.monto

    if datos.periodicidad == "SEMANAL":
        salario_anual = monto * 52

    elif datos.periodicidad == "QUINCENAL":
        salario_anual = monto * 24

    elif datos.periodicidad == "MENSUAL":
        salario_anual = monto * 12

    elif datos.periodicidad == "ANUAL":
        salario_anual = monto

    else:
        raise ValueError(
            "La periodicidad salarial indicada no es válida."
        )

    salario_mensual = salario_anual / 12
    salario_quincenal = salario_anual / 24
    salario_semanal = salario_anual / 52

    return ResumenSalario(
        monto_original=round(monto, 2),
        periodicidad_original=datos.periodicidad,
        salario_semanal=round(salario_semanal, 2),
        salario_quincenal=round(salario_quincenal, 2),
        salario_mensual=round(salario_mensual, 2),
        salario_anual=round(salario_anual, 2),
    )