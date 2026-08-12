"""Construcción de escenarios preliminares de retiro.

Este servicio calcula fechas exactas de referencia y fechas
alternativas de retiro. También produce una estimación de cuotas
futuras a partir de los datos definidos en el Paso 2.

La fecha de evaluación y la fecha de corte de las cuotas se
mantienen separadas porque un reporte de la CSS puede contener
información acreditada hasta una fecha anterior al día en que
se realiza la simulación.

La edad de referencia no implica por sí sola elegibilidad para
una pensión. La verificación legal completa corresponderá al
motor de elegibilidad.
"""

from calendar import monthrange
from datetime import date

from app.core.normativa import (
    obtener_edad_referencia,
)
from app.modelos.simulacion import (
    DatosRetiro,
    EscenarioRetiro,
    ResumenRetiro,
)


# ============================================================
# Funciones de fecha
# ============================================================

def _sumar_anios(
    fecha: date,
    cantidad: int,
) -> date:
    """Suma años conservando mes y día cuando sea posible.

    Para personas nacidas el 29 de febrero, un año no bisiesto
    utiliza el 28 de febrero.
    """

    nuevo_anio = (
        fecha.year
        + cantidad
    )

    ultimo_dia_mes = monthrange(
        nuevo_anio,
        fecha.month,
    )[1]

    nuevo_dia = min(
        fecha.day,
        ultimo_dia_mes,
    )

    return date(
        nuevo_anio,
        fecha.month,
        nuevo_dia,
    )


def _meses_completos_entre(
    inicio: date,
    fin: date,
) -> int:
    """Calcula meses calendario completos entre dos fechas."""

    if fin <= inicio:
        return 0

    meses = (
        (fin.year - inicio.year)
        * 12
        + (fin.month - inicio.month)
    )

    if fin.day < inicio.day:
        meses -= 1

    return max(
        meses,
        0,
    )


def _calcular_edad(
    fecha_nacimiento: date,
    fecha_evaluacion: date,
) -> int:
    """Calcula la edad cumplida en una fecha determinada."""

    edad = (
        fecha_evaluacion.year
        - fecha_nacimiento.year
    )

    if (
        (
            fecha_evaluacion.month,
            fecha_evaluacion.day,
        )
        <
        (
            fecha_nacimiento.month,
            fecha_nacimiento.day,
        )
    ):
        edad -= 1

    return edad


def _fecha_corte_desde_ultimo_mes(
    ultimo_mes: str,
    fecha_evaluacion: date,
) -> date:
    """Convierte YYYY-MM en una fecha de corte mensual coherente.

    El último mes acreditado no puede ser posterior al mes en que se
    realiza la evaluación. Para meses anteriores se utiliza el último día
    del mes; si coincide con el mes de evaluación, la fecha se limita al
    propio día de evaluación para no crear una fecha futura artificial.
    """

    anio_texto, mes_texto = ultimo_mes.split("-", maxsplit=1)
    anio = int(anio_texto)
    mes = int(mes_texto)

    if (anio, mes) > (fecha_evaluacion.year, fecha_evaluacion.month):
        raise ValueError(
            "El último mes con cuotas acreditadas no puede "
            "ser posterior al mes de la fecha de evaluación."
        )

    ultimo_dia = monthrange(anio, mes)[1]
    fecha_mes = date(anio, mes, ultimo_dia)

    if (anio, mes) == (fecha_evaluacion.year, fecha_evaluacion.month):
        return min(fecha_mes, fecha_evaluacion)

    return fecha_mes


# ============================================================
# Estimación de cuotas
# ============================================================

def _estimar_cuotas_por_meses(
    meses: int,
    cuotas_por_anio: int,
) -> int:
    """Convierte meses completos en cuotas según densidad anual."""

    if (
        meses <= 0
        or cuotas_por_anio <= 0
    ):
        return 0

    return int(
        meses
        * cuotas_por_anio
        / 12
    )


def _estimar_cuotas_hasta_fecha(
    datos: DatosRetiro,
    fecha_corte_cuotas: date,
    fecha_objetivo: date,
) -> int:
    """Estima cuotas nuevas respetando el cierre del año actual.

    El año de evaluación utiliza primero
    ``cuotas_esperadas_cierre_anio``. A partir del siguiente año
    se aplica ``cuotas_esperadas_por_anio``.

    Esto evita que una densidad futura de 12 cuotas por año agregue
    cuotas al año actual cuando el Asegurado(a) ya indicó, por ejemplo,
    que ese año cerrará con la misma cantidad que ya tiene acreditada.
    """

    if (
        not datos.continua_cotizando
        or fecha_objetivo <= fecha_corte_cuotas
    ):
        return 0

    anio_actual = fecha_corte_cuotas.year

    cuotas_restantes_anio_actual = max(
        datos.cuotas_esperadas_cierre_anio
        - datos.cuotas_anio_actual,
        0,
    )

    # Si el objetivo todavía está dentro del mismo año, la cantidad
    # estimada no puede exceder ni los meses transcurridos ni el cierre
    # anual que el Asegurado(a) definió en el Paso 2.
    if fecha_objetivo.year == anio_actual:
        meses_disponibles = (
            _meses_completos_entre(
                fecha_corte_cuotas,
                fecha_objetivo,
            )
        )

        cuotas_por_meses = (
            _estimar_cuotas_por_meses(
                meses_disponibles,
                datos.cuotas_esperadas_por_anio,
            )
        )

        return min(
            cuotas_restantes_anio_actual,
            cuotas_por_meses,
        )

    cuotas_adicionales = (
        cuotas_restantes_anio_actual
    )

    # Años completos posteriores al año actual y anteriores al año
    # de la fecha objetivo.
    for anio in range(
        anio_actual + 1,
        fecha_objetivo.year,
    ):
        cuotas_adicionales += (
            datos.cuotas_esperadas_por_anio
        )

    # Parte transcurrida del año objetivo. Se cuentan meses completos
    # desde el 1 de enero hasta la fecha evaluada.
    inicio_anio_objetivo = date(
        fecha_objetivo.year,
        1,
        1,
    )

    meses_anio_objetivo = (
        _meses_completos_entre(
            inicio_anio_objetivo,
            fecha_objetivo,
        )
    )

    cuotas_adicionales += (
        _estimar_cuotas_por_meses(
            meses_anio_objetivo,
            datos.cuotas_esperadas_por_anio,
        )
    )

    return cuotas_adicionales


# ============================================================
# Construcción de escenarios
# ============================================================

def _crear_escenario(
    *,
    datos: DatosRetiro,
    fecha_corte: date,
    fecha_corte_cuotas: date,
    fecha_retiro: date,
    tipo: str,
    nombre: str,
    edad_retiro: int,
) -> EscenarioRetiro:
    """Construye un escenario individual de retiro."""

    meses_desde_corte_cuotas = (
        _meses_completos_entre(
            fecha_corte_cuotas,
            fecha_retiro,
        )
    )

    cuotas_adicionales = (
        _estimar_cuotas_hasta_fecha(
            datos,
            fecha_corte_cuotas,
            fecha_retiro,
        )
    )

    return EscenarioRetiro(
        tipo=tipo,
        nombre=nombre,
        fecha_retiro=fecha_retiro,
        edad_retiro_anios=edad_retiro,
        meses_desde_corte_cuotas=(
            meses_desde_corte_cuotas
        ),
        cuotas_estimadas_adicionales=(
            cuotas_adicionales
        ),
        cuotas_estimadas_totales=(
            datos.cuotas_reales
            + cuotas_adicionales
        ),
        fecha_ya_transcurrida=(
            fecha_retiro
            < fecha_corte
        ),
    )


def analizar_retiro(
    datos: DatosRetiro,
) -> ResumenRetiro:
    """Construye fechas de retiro y cuotas estimadas."""

    fecha_corte = (
        datos.fecha_corte
        or date.today()
    )

    if datos.ultimo_mes_cuotas:
        fecha_corte_cuotas = _fecha_corte_desde_ultimo_mes(
            datos.ultimo_mes_cuotas,
            fecha_corte,
        )

        if (
            datos.fecha_corte_cuotas is not None
            and datos.fecha_corte_cuotas != fecha_corte_cuotas
        ):
            raise ValueError(
                "El último mes acreditado y la fecha de corte de cuotas "
                "deben representar el mismo cierre."
            )
    else:
        fecha_corte_cuotas = (
            datos.fecha_corte_cuotas
            or fecha_corte
        )

    if datos.fecha_nacimiento > fecha_corte:
        raise ValueError(
            "La fecha de nacimiento no puede "
            "ser posterior a la fecha de evaluación."
        )

    if fecha_corte_cuotas > fecha_corte:
        raise ValueError(
            "La fecha de corte de las cuotas no puede "
            "ser posterior a la fecha de evaluación."
        )

    if fecha_corte_cuotas < datos.fecha_nacimiento:
        raise ValueError(
            "La fecha de corte de las cuotas no puede "
            "ser anterior a la fecha de nacimiento."
        )

    if (
        datos.cuotas_esperadas_cierre_anio
        < datos.cuotas_anio_actual
    ):
        raise ValueError(
            "Las cuotas esperadas al cierre del año no pueden "
            "ser menores que las cuotas ya acreditadas ese año."
        )

    edad_actual = _calcular_edad(
        datos.fecha_nacimiento,
        fecha_corte,
    )

    edad_referencia = (
        obtener_edad_referencia(
            datos.sexo,
        )
    )

    fecha_referencia = (
        _sumar_anios(
            datos.fecha_nacimiento,
            edad_referencia,
        )
    )

    alcanzo_referencia = (
        fecha_corte
        >= fecha_referencia
    )

    dias_hasta_referencia = (
        fecha_referencia
        - fecha_corte
    ).days

    escenarios: list[
        EscenarioRetiro
    ] = []

    adicionales = sorted(
        set(
            datos.anios_adicionales
        )
    )

    for adicional in adicionales:
        if adicional < -2:
            raise ValueError(
                "Los escenarios anticipados estándar no pueden superar "
                "dos años antes de la edad de referencia."
            )

        fecha_retiro = (
            _sumar_anios(
                fecha_referencia,
                adicional,
            )
        )

        if adicional < 0:
            tipo = "ANTICIPADO"
            cantidad = abs(adicional)
            nombre = (
                f"Edad de referencia - "
                f"{cantidad} "
                f"{'año' if cantidad == 1 else 'años'}"
            )

        elif adicional == 0:
            tipo = "REFERENCIA"
            nombre = "Edad de referencia"

        else:
            tipo = "ADICIONAL"
            nombre = (
                f"Edad de referencia + "
                f"{adicional} "
                f"{'año' if adicional == 1 else 'años'}"
            )

        escenarios.append(
            _crear_escenario(
                datos=datos,
                fecha_corte=fecha_corte,
                fecha_corte_cuotas=fecha_corte_cuotas,
                fecha_retiro=fecha_retiro,
                tipo=tipo,
                nombre=nombre,
                edad_retiro=(
                    edad_referencia
                    + adicional
                ),
            )
        )

    if (
        datos.fecha_retiro_personalizada
        is not None
    ):
        fecha_personalizada = (
            datos.fecha_retiro_personalizada
        )

        if (
            fecha_personalizada
            < datos.fecha_nacimiento
        ):
            raise ValueError(
                "La fecha personalizada de retiro "
                "no puede ser anterior al nacimiento."
            )

        escenarios.append(
            _crear_escenario(
                datos=datos,
                fecha_corte=fecha_corte,
                fecha_corte_cuotas=fecha_corte_cuotas,
                fecha_retiro=fecha_personalizada,
                tipo="PERSONALIZADO",
                nombre="Fecha personalizada",
                edad_retiro=_calcular_edad(
                    datos.fecha_nacimiento,
                    fecha_personalizada,
                ),
            )
        )

    advertencias: list[str] = []

    escenarios_futuros = [
        escenario
        for escenario in escenarios
        if not escenario.fecha_ya_transcurrida
    ]

    anio_maximo_escenarios = max(
        (
            escenario.fecha_retiro.year
            for escenario in escenarios_futuros
        ),
        default=fecha_corte.year,
    )

    if (
        datos.anio_fin_proyeccion_salarial
        is None
    ):
        proyeccion_cubre = False

        if escenarios_futuros:
            advertencias.append(
                "No se pudo verificar hasta qué año está cubierta "
                "la proyección salarial del Paso 4."
            )

    else:
        proyeccion_cubre = (
            datos.anio_fin_proyeccion_salarial
            >= anio_maximo_escenarios
        )

        if not proyeccion_cubre:
            advertencias.append(
                "La proyección salarial del Paso 4 llega hasta "
                f"{datos.anio_fin_proyeccion_salarial}, pero los "
                f"escenarios de retiro seleccionados llegan hasta "
                f"{anio_maximo_escenarios}. Antes de calcular una "
                "pensión para esos escenarios deberá ampliarse "
                "la proyección salarial."
            )

    return ResumenRetiro(
        fecha_corte=fecha_corte,
        fecha_corte_cuotas=(
            fecha_corte_cuotas
        ),
        edad_actual_anios=edad_actual,
        edad_referencia=edad_referencia,
        fecha_referencia=fecha_referencia,
        alcanzo_edad_referencia=(
            alcanzo_referencia
        ),
        dias_hasta_referencia=(
            dias_hasta_referencia
        ),
        escenarios=escenarios,
        anio_fin_proyeccion_salarial=(
            datos.anio_fin_proyeccion_salarial
        ),
        proyeccion_salarial_cubre_escenarios=(
            proyeccion_cubre
        ),
        advertencias=advertencias,
        metodo_estimacion_cuotas=(
            (
                "El último mes con cuotas acreditadas define el cierre "
                "del historial real. "
            )
            if datos.ultimo_mes_cuotas
            else ""
        )
        + (
            "El año actual respeta las cuotas esperadas al cierre "
            "definidas en el Paso 2. Desde el año siguiente se usa "
            "la densidad anual esperada. Las cuotas dentro de un "
            "año futuro se estiman por meses calendario completos. "
            "No sustituye el historial mensual oficial de la CSS."
        ),
    )
