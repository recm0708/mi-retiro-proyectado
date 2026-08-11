"""Motor de elegibilidad y clasificación de prestaciones por vejez SEBD.

La clasificación se realiza con fechas exactas y cuotas acreditadas o
estimadas al escenario de retiro. Se distingue entre las cuatro modalidades
de Pensión de Retiro por Vejez del artículo 181, la indemnización por vejez
del artículo 186 y los escenarios que todavía no cumplen una prestación.
"""

from calendar import monthrange
from datetime import date

from app.core.normativa import (
    cargar_parametros_sebd,
    obtener_edad_referencia,
)


def calcular_edad_cumplida(
    fecha_nacimiento: date,
    fecha_evaluacion: date,
) -> int:
    """Calcula la edad cumplida de una persona en una fecha."""

    edad = fecha_evaluacion.year - fecha_nacimiento.year

    if (
        (fecha_evaluacion.month, fecha_evaluacion.day)
        < (fecha_nacimiento.month, fecha_nacimiento.day)
    ):
        edad -= 1

    return edad


def _sumar_anios(fecha: date, cantidad: int) -> date:
    """Suma años preservando mes y día cuando sea posible."""

    anio = fecha.year + cantidad
    ultimo_dia = monthrange(anio, fecha.month)[1]

    return date(
        anio,
        fecha.month,
        min(fecha.day, ultimo_dia),
    )


def _meses_completos_entre(inicio: date, fin: date) -> int:
    """Devuelve meses calendario completos entre dos fechas."""

    if fin <= inicio:
        return 0

    meses = (
        (fin.year - inicio.year) * 12
        + fin.month
        - inicio.month
    )

    if fin.day < inicio.day:
        meses -= 1

    return max(meses, 0)


def fecha_edad_referencia(
    fecha_nacimiento: date,
    sexo: str,
) -> date:
    """Devuelve la fecha exacta en que se alcanza la edad de referencia."""

    return _sumar_anios(
        fecha_nacimiento,
        obtener_edad_referencia(sexo),
    )


def fecha_minima_retiro_anticipado(
    fecha_nacimiento: date,
    sexo: str,
) -> date:
    """Devuelve el límite inferior de la banda anticipada estándar."""

    referencia = fecha_edad_referencia(
        fecha_nacimiento,
        sexo,
    )

    maximo = int(
        cargar_parametros_sebd()["pension_vejez"]
        ["retiro_anticipado"]["maximo_anios_anticipacion"]
    )

    return _sumar_anios(referencia, -maximo)


def meses_desde_limite_anticipado(
    fecha_nacimiento: date,
    sexo: str,
    fecha_retiro: date,
) -> int:
    """Calcula meses completos transcurridos dentro de la banda anticipada."""

    inicio = fecha_minima_retiro_anticipado(
        fecha_nacimiento,
        sexo,
    )

    return _meses_completos_entre(
        inicio,
        fecha_retiro,
    )


def clasificar_modalidad_sebd(
    fecha_nacimiento: date,
    sexo: str,
    fecha_retiro: date,
    cuotas_totales: int,
) -> dict:
    """Determina la prestación SEBD aplicable al escenario indicado.

    La clasificación no sustituye la revisión individual de la CSS. Se limita
    a las reglas generales de edad y cuotas de los artículos 178, 179, 181 y
    186. Los regímenes especiales se mantienen fuera de esta primera capa.
    """

    parametros = cargar_parametros_sebd()["pension_vejez"]
    cuotas_referencia = int(parametros["cuotas_referencia"])
    cuotas_minimas = int(parametros["cuotas_minimas_proporcional"])

    referencia = fecha_edad_referencia(
        fecha_nacimiento,
        sexo,
    )
    minima_anticipada = fecha_minima_retiro_anticipado(
        fecha_nacimiento,
        sexo,
    )
    edad = calcular_edad_cumplida(
        fecha_nacimiento,
        fecha_retiro,
    )

    base = {
        "fecha_referencia": referencia,
        "fecha_minima_anticipada": minima_anticipada,
        "edad_retiro_anios": edad,
        "edad_referencia": obtener_edad_referencia(sexo),
        "cuotas_totales": cuotas_totales,
        "cuotas_referencia": cuotas_referencia,
        "cuotas_minimas_proporcional": cuotas_minimas,
        "motivos": [],
        "advertencias": [],
    }

    if fecha_retiro < minima_anticipada:
        return {
            **base,
            "modalidad": "NO_ELEGIBLE",
            "modalidad_nombre": "Aún no cumple la banda de edad para retiro por vejez",
            "tipo_prestacion": "NINGUNA",
            "elegible": False,
            "motivos": [
                "La fecha elegida es anterior al límite de dos años previo a la edad de referencia."
            ],
        }

    if fecha_retiro < referencia:
        if cuotas_totales >= cuotas_referencia:
            return {
                **base,
                "modalidad": "ANTICIPADA",
                "modalidad_nombre": "Pensión de Retiro por Vejez Anticipada",
                "tipo_prestacion": "PENSION",
                "elegible": True,
            }

        if cuotas_totales >= cuotas_minimas:
            return {
                **base,
                "modalidad": "PROPORCIONAL_ANTICIPADA",
                "modalidad_nombre": "Pensión de Retiro por Vejez Proporcional Anticipada",
                "tipo_prestacion": "PENSION",
                "elegible": True,
            }

        return {
            **base,
            "modalidad": "NO_ELEGIBLE",
            "modalidad_nombre": "Aún no cumple las condiciones de pensión por vejez",
            "tipo_prestacion": "NINGUNA",
            "elegible": False,
            "motivos": [
                "Dentro de la banda anticipada se requieren al menos 180 cuotas para una pensión proporcional anticipada."
            ],
        }

    if cuotas_totales >= cuotas_referencia:
        return {
            **base,
            "modalidad": "NORMAL",
            "modalidad_nombre": "Pensión de Retiro por Vejez Normal",
            "tipo_prestacion": "PENSION",
            "elegible": True,
        }

    if cuotas_totales >= cuotas_minimas:
        return {
            **base,
            "modalidad": "PROPORCIONAL",
            "modalidad_nombre": "Pensión de Retiro por Vejez Proporcional",
            "tipo_prestacion": "PENSION",
            "elegible": True,
        }

    transicion = date(2036, 3, 1)

    if fecha_retiro < transicion:
        return {
            **base,
            "modalidad": "INDEMNIZACION",
            "modalidad_nombre": "Indemnización por Vejez",
            "tipo_prestacion": "INDEMNIZACION",
            "elegible": True,
            "advertencias": [
                "La aplicación identifica la posible indemnización por vejez, pero su monto todavía no se calcula en esta fase."
            ],
        }

    return {
        **base,
        "modalidad": "NO_ELEGIBLE",
        "modalidad_nombre": "Evaluación requerida bajo el SUCGS",
        "tipo_prestacion": "TRANSICION_SUCGS",
        "elegible": False,
        "motivos": [
            "Desde el 1 de marzo de 2036 la Ley dispone que ya no se conceda indemnización por vejez y que el cálculo proceda conforme al SUCGS."
        ],
    }


def evaluar_elegibilidad_sebd_normal(
    fecha_nacimiento: date,
    sexo: str,
    fecha_retiro: date,
    cuotas_totales: int,
) -> tuple[bool, list[str]]:
    """Conserva la API previa de elegibilidad para pensión normal."""

    clasificacion = clasificar_modalidad_sebd(
        fecha_nacimiento,
        sexo,
        fecha_retiro,
        cuotas_totales,
    )

    if clasificacion["modalidad"] == "NORMAL":
        return True, []

    motivos = list(clasificacion.get("motivos", []))

    if not motivos:
        motivos.append(
            "El escenario corresponde a una modalidad distinta de la Pensión de Retiro por Vejez Normal."
        )

    return False, motivos
