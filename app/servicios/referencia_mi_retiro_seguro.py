"""Extracción segura de referencias desde comprobantes PDF de Mi Retiro Seguro.

El servicio procesa el archivo en memoria y devuelve solo los datos necesarios
para comparar una simulación actual con la referencia personal del Asegurado(a).
No persiste el PDF ni expone nombre, cédula o número de seguro social.
"""

from __future__ import annotations

from datetime import datetime
from io import BytesIO
import re

from pypdf import PdfReader

from app.modelos.simulacion import (
    RegistroReferenciaMiRetiroSeguro,
    ResumenReferenciaMiRetiroSeguro,
)


MARCADOR_DOCUMENTO = (
    "COMPROBANTE DE DECISIÓN DEL PROGRAMA DE INVALIDEZ, VEJEZ Y MUERTE"
)


def _buscar(patron: str, texto: str, flags: int = re.IGNORECASE) -> str | None:
    coincidencia = re.search(patron, texto, flags)
    if not coincidencia:
        return None
    return coincidencia.group(1).strip()


def _monto(valor: str | None) -> float | None:
    if not valor:
        return None
    return float(valor.replace(",", ""))


def _fecha_ddmmyyyy(valor: str | None):
    if not valor:
        return None
    try:
        return datetime.strptime(valor, "%d/%m/%Y").date()
    except ValueError:
        return None


def _normalizar_sistema(texto: str) -> tuple[str, str]:
    texto_mayus = texto.upper()

    if "SUBSISTEMA EXCLUSIVO DE BENEFICIO DEFINIDO" in texto_mayus or "SEBD" in texto_mayus:
        return "SEBD", "SEBD — Beneficio Definido"

    if "SUBSISTEMA MIXTO" in texto_mayus or "SISTEMA MIXTO" in texto_mayus:
        return "MIXTO", "Subsistema Mixto"

    if (
        "SISTEMA ÚNICO DE CAPITALIZACIÓN CON GARANTÍA SOLIDARIA" in texto_mayus
        or "SISTEMA UNICO DE CAPITALIZACION CON GARANTIA SOLIDARIA" in texto_mayus
        or "SUCGS" in texto_mayus
    ):
        return "SUCGS", "SUCGS — Capitalización con Garantía Solidaria"

    return "NO_IDENTIFICADO", "Sistema no identificado"


def _normalizar_naturaleza(prestacion: str | None) -> str:
    texto = (prestacion or "").upper()

    if "PENSIÓN" in texto or "PENSION" in texto:
        return "PENSION_MENSUAL"

    if "INDEMNIZ" in texto or "PAGO ÚNICO" in texto or "PAGO UNICO" in texto:
        return "PAGO_UNICO"

    return "NO_IDENTIFICADA"


def _extraer_registros(texto: str) -> list[RegistroReferenciaMiRetiroSeguro]:
    registros: list[RegistroReferenciaMiRetiroSeguro] = []

    patron = re.compile(
        r"^(\d{4})\s+"
        r"(\d{1,3})\s+"
        r"(Histórico(?:\s*\+\s*Proyectado)?|Proyectado)\s+"
        r"([\d,]+\.\d{2})\s+"
        r"(\d{1,2})\s*$",
        re.IGNORECASE,
    )

    for linea in texto.splitlines():
        coincidencia = patron.match(linea.strip())
        if not coincidencia:
            continue

        tipo_original = coincidencia.group(3)
        tipo_mayus = tipo_original.upper()
        if "+" in tipo_original:
            tipo = "HISTORICO_PROYECTADO"
        elif "PROYECTADO" in tipo_mayus:
            tipo = "PROYECTADO"
        else:
            tipo = "HISTORICO"

        registros.append(
            RegistroReferenciaMiRetiroSeguro(
                anio=int(coincidencia.group(1)),
                edad=int(coincidencia.group(2)),
                tipo=tipo,
                salario_anual=float(coincidencia.group(4).replace(",", "")),
                cuotas=int(coincidencia.group(5)),
            )
        )

    return registros


def extraer_referencia_desde_texto(texto: str) -> ResumenReferenciaMiRetiroSeguro:
    """Extrae la referencia variable desde el texto de un comprobante."""

    if MARCADOR_DOCUMENTO not in texto.upper():
        raise ValueError(
            "El archivo no parece ser un comprobante de Mi Retiro Seguro compatible."
        )

    monto = _monto(
        _buscar(
            r"Monto estimado de prestación:\s*B/\.\s*([\d,]+\.\d{2})",
            texto,
        )
    )

    if monto is None:
        raise ValueError(
            "No fue posible localizar el monto estimado de prestación en el comprobante."
        )

    prestacion = _buscar(r"Prestación esperada:\s*([^\n\r]+)", texto)

    sistema_texto = _buscar(r"Sistema elegido:\s*([^\n\r]+)", texto) or ""
    if not sistema_texto:
        sistema_texto = _buscar(
            r"Sistema actual:\s*([\s\S]{0,100}?)(?:\nINFORMACIÓN DEL SISTEMA|\nINFORMACION DEL SISTEMA)",
            texto,
        ) or ""

    sistema, nombre_sistema = _normalizar_sistema(sistema_texto)

    registros = _extraer_registros(texto)
    advertencias: list[str] = []

    if sistema == "NO_IDENTIFICADO":
        advertencias.append(
            "No se pudo identificar con certeza el sistema elegido en el comprobante."
        )

    if not registros:
        advertencias.append(
            "No se pudieron extraer filas del historial anual; la referencia monetaria sí está disponible."
        )

    edad_retiro_texto = _buscar(r"Edad de retiro elegida:\s*(\d+)\s*años", texto)
    cuotas_historicas_texto = _buscar(
        r"Total cuotas históricas\s+aportadas a la fecha:\s*(\d+)",
        texto,
    )
    total_cuotas_texto = _buscar(
        r"Total de cuotas acumuladas:\s*(\d+)\s*cuotas",
        texto,
    )

    sexo = _buscar(r"Sexo:\s*(Femenino|Masculino)", texto)
    sexo_codigo = None
    if sexo:
        sexo_codigo = "F" if sexo.lower().startswith("f") else "M"

    return ResumenReferenciaMiRetiroSeguro(
        fecha_comprobante=_fecha_ddmmyyyy(
            _buscar(r"Fecha de Comprobante:\s*(\d{2}/\d{2}/\d{4})", texto)
        ),
        fecha_decision_texto=_buscar(r"Fecha de decisión:\s*([^\n\r]+)", texto),
        fecha_nacimiento=_fecha_ddmmyyyy(
            _buscar(r"Fecha de Nacimiento:\s*(\d{2}/\d{2}/\d{4})", texto)
        ),
        sexo=sexo_codigo,
        fecha_ingreso_css=_fecha_ddmmyyyy(
            _buscar(r"Fecha de Ingreso CSS:\s*(\d{2}/\d{2}/\d{4})", texto)
        ),
        sistema_elegido=sistema,
        sistema_elegido_nombre=nombre_sistema,
        edad_retiro_elegida=(
            int(edad_retiro_texto) if edad_retiro_texto else None
        ),
        cuotas_historicas=(
            int(cuotas_historicas_texto) if cuotas_historicas_texto else None
        ),
        prestacion_esperada=prestacion,
        naturaleza_prestacion=_normalizar_naturaleza(prestacion),
        monto_estimado_prestacion=monto,
        total_cuotas_acumuladas=(
            int(total_cuotas_texto) if total_cuotas_texto else None
        ),
        registros=registros,
        advertencias=advertencias,
    )


def analizar_comprobante_pdf(contenido: bytes) -> ResumenReferenciaMiRetiroSeguro:
    """Extrae texto de un PDF en memoria y analiza su referencia personal."""

    if not contenido:
        raise ValueError("El archivo PDF está vacío.")

    try:
        lector = PdfReader(BytesIO(contenido))
    except Exception as error:
        raise ValueError("No fue posible abrir el archivo PDF.") from error

    if lector.is_encrypted:
        try:
            desbloqueado = lector.decrypt("")
        except Exception as error:
            raise ValueError(
                "El PDF está protegido y no puede analizarse automáticamente."
            ) from error
        if desbloqueado == 0:
            raise ValueError(
                "El PDF está protegido y no puede analizarse automáticamente."
            )

    if len(lector.pages) > 20:
        raise ValueError(
            "El comprobante contiene más páginas de las esperadas para este importador."
        )

    partes: list[str] = []

    try:
        for pagina in lector.pages:
            partes.append(pagina.extract_text() or "")
    except Exception as error:
        raise ValueError(
            "No fue posible extraer el texto del comprobante PDF."
        ) from error

    texto = "\n".join(partes).strip()

    if not texto:
        raise ValueError(
            "El PDF no contiene texto extraíble. Por ahora se requiere un comprobante digital, no una imagen escaneada."
        )

    return extraer_referencia_desde_texto(texto)
