"""Extracción segura de salarios recientes desde una Ficha Digital de Mi Caja Digital.

El archivo se procesa únicamente en memoria. El contrato de salida contiene solo
registros del año calendario actual con mes, año y salario; no conserva períodos
de años anteriores ni expone identificadores del Asegurado(a).
"""

from __future__ import annotations

from datetime import date
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
    return "".join(
        caracter
        for caracter in unicodedata.normalize("NFD", texto)
        if unicodedata.category(caracter) != "Mn"
    )


def extraer_ficha_digital_desde_texto(
    texto: str,
    anio_actual: int | None = None,
) -> ResumenFichaDigital:
    """Extrae únicamente los salarios mensuales del año calendario actual."""

    anio_objetivo = anio_actual if anio_actual is not None else date.today().year

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

    por_periodo: dict[tuple[int, int], RegistroFichaDigital] = {}
    advertencias: list[str] = []

    for coincidencia in patron.finditer(texto_normalizado):
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
            f"No fue posible detectar salarios del año actual {anio_objetivo} en la Ficha Digital. "
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
    try:
        for pagina in lector.pages:
            partes.append(pagina.extract_text() or "")
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
