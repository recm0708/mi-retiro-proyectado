"""Extracción segura de salarios recientes desde una Ficha Digital de Mi Caja Digital.

El archivo se procesa únicamente en memoria. El contrato de salida contiene los
registros del año más reciente detectado con mes, año y salario; no expone
identificadores del Asegurado(a). La vigencia se evalúa por separado contra una
fecha externa verificable.
"""

from __future__ import annotations

from io import BytesIO
import re
import unicodedata

from pypdf import PdfReader

from app.modelos.simulacion import RegistroFichaDigital, ResumenFichaDigital


MESES = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "setiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}


def _normalizar(texto: str) -> str:
    """Elimina marcas diacríticas para comparar texto extraído con estabilidad."""

    return "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caracter) != "Mn"
    )


def extraer_ficha_digital_desde_texto(
    texto: str,
    anio_actual: int | None = None,
) -> ResumenFichaDigital:
    """Extrae salarios del año más reciente presente en la Ficha Digital.

    ``anio_actual`` se conserva como argumento explícito para pruebas y llamadas
    controladas. En producción no se deriva del reloj local del equipo: si no se
    proporciona, se utiliza el año más reciente encontrado en el propio documento
    y la vigencia se evalúa después contra una fecha externa verificable.
    """

    texto_normalizado = _normalizar(texto)
    if "SALARIOS DEL ULTIMO ANO" not in texto_normalizado.upper():
        raise ValueError(
            "El archivo no parece contener la sección 'Salarios del último año' de la Ficha Digital."
        )

    patron = re.compile(
        r"(?P<anio>20\d{2})\s*[-–—]\s*"
        r"(?P<mes>Enero|Febrero|Marzo|Abril|Mayo|Junio|Julio|Agosto|Septiembre|Setiembre|Octubre|Noviembre|Diciembre)"
        r"\s+(?P<salario>[\d,]+(?:\.\d{2})?)",
        re.IGNORECASE,
    )

    coincidencias = list(patron.finditer(texto_normalizado))
    if not coincidencias:
        raise ValueError(
            "No fue posible detectar salarios mensuales en la Ficha Digital. "
            "Puedes continuar con captura manual."
        )

    anio_objetivo = (
        anio_actual
        if anio_actual is not None
        else max(int(coincidencia.group("anio")) for coincidencia in coincidencias)
    )

    por_periodo: dict[tuple[int, int], RegistroFichaDigital] = {}
    advertencias: list[str] = []

    for coincidencia in coincidencias:
        anio = int(coincidencia.group("anio"))
        if anio != anio_objetivo:
            continue

        mes_texto = coincidencia.group("mes").lower()
        mes = MESES[mes_texto]
        salario = float(coincidencia.group("salario").replace(",", ""))

        clave = (anio, mes)
        if clave in por_periodo:
            advertencias.append(
                f"Se detectó más de un valor para {anio}-{mes:02d}; se conservará el último encontrado."
            )

        por_periodo[clave] = RegistroFichaDigital(
            anio=anio,
            mes=mes,
            salario=salario,
            estado="COMPLETO",
        )

    if not por_periodo:
        raise ValueError(
            f"No fue posible detectar salarios del año {anio_objetivo} en la Ficha Digital. "
            "Puedes continuar con captura manual."
        )

    registros = sorted(
        por_periodo.values(),
        key=lambda registro: (registro.anio, registro.mes),
    )

    if len(registros) < 6:
        advertencias.append(
            f"Se detectaron pocos meses de {anio_objetivo}. Revisa la vista previa antes de confirmar la importación."
        )

    mas_reciente = registros[-1]

    return ResumenFichaDigital(
        registros=registros,
        anio_mas_reciente=mas_reciente.anio,
        mes_mas_reciente=mas_reciente.mes,
        advertencias=advertencias,
    )


def analizar_ficha_digital_pdf(contenido: bytes) -> ResumenFichaDigital:
    """Lee un PDF digital en memoria y extrae salarios recientes."""

    if not contenido:
        raise ValueError("El archivo PDF está vacío.")

    try:
        lector = PdfReader(BytesIO(contenido))
    except Exception as error:
        raise ValueError("No fue posible abrir la Ficha Digital en PDF.") from error

    if lector.is_encrypted:
        try:
            desbloqueado = lector.decrypt("")
        except Exception as error:
            raise ValueError(
                "La Ficha Digital está protegida y no puede analizarse automáticamente."
            ) from error
        if desbloqueado == 0:
            raise ValueError(
                "La Ficha Digital está protegida y no puede analizarse automáticamente."
            )

    if len(lector.pages) > 30:
        raise ValueError(
            "El documento contiene demasiadas páginas para este importador de Ficha Digital."
        )

    partes: list[str] = []
    total_caracteres = 0
    try:
        for pagina in lector.pages:
            texto_pagina = pagina.extract_text() or ""
            total_caracteres += len(texto_pagina)
            if total_caracteres > 2000000:
                raise ValueError(
                    "La Ficha Digital contiene demasiado texto para este importador."
                )
            partes.append(texto_pagina)
    except ValueError:
        raise
    except Exception as error:
        raise ValueError(
            "No fue posible extraer el texto de la Ficha Digital."
        ) from error

    texto = "\n".join(partes).strip()
    if not texto:
        raise ValueError(
            "El PDF no contiene texto extraíble. Si es una imagen escaneada, utiliza por ahora la captura manual."
        )

    return extraer_ficha_digital_desde_texto(texto)
