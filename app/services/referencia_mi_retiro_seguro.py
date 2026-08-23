"""Extracción segura de referencias desde comprobantes PDF de Mi Retiro Seguro.

El servicio procesa el archivo en memoria y devuelve los datos que el Asegurado(a)
puede revisar antes de importarlos. No persiste el PDF y solo expone identificadores
opcionales cuando aparecen con una etiqueta inequívoca.
"""

from __future__ import annotations

from datetime import datetime
from io import BytesIO
import re

from pypdf import PdfReader

from app.models.simulacion import (
    RegistroReferenciaMiRetiroSeguro,
    ResumenReferenciaMiRetiroSeguro,
)


MARCADOR_DOCUMENTO = (
    "COMPROBANTE DE DECISIÓN DEL PROGRAMA DE INVALIDEZ, VEJEZ Y MUERTE"
)


def _buscar(patron: str, texto: str, flags: int = re.IGNORECASE) -> str | None:
    """Devuelve el primer grupo capturado por una búsqueda regular opcional."""

    coincidencia = re.search(patron, texto, flags)
    if not coincidencia:
        return None
    return coincidencia.group(1).strip()


def _texto_opcional(valor: str | None) -> str | None:
    """Normaliza espacios de un texto opcional extraído del documento."""

    if not valor:
        return None
    limpio = re.sub(r"\s+", " ", valor).strip(" :-\t")
    return limpio or None


def _descomponer_nombre_completo(
    nombre: str | None,
    sexo: str | None,
) -> dict[str, str | None]:
    """Descompone un nombre completo usando una regla conservadora y revisable.

    Para mujeres, la construcción ``... de APELLIDO`` al final se interpreta
    como apellido de casada. Del resto se reservan los dos últimos componentes
    como apellidos y el primer componente como primer nombre; cualquier término
    intermedio se conserva unido como segundo nombre. El resultado siempre pasa
    por la vista previa antes de incorporarse a la simulación.
    """

    limpio = _texto_opcional(nombre)
    resultado = {
        "primer_nombre": None,
        "segundo_nombre": None,
        "primer_apellido": None,
        "segundo_apellido": None,
        "apellido_casada": None,
    }
    if not limpio:
        return resultado

    base = limpio
    if sexo == "F":
        coincidencia_casada = re.match(
            r"^(.*?)\s+de\s+([^\n\r]+)$",
            base,
            re.IGNORECASE,
        )
        if coincidencia_casada:
            base = coincidencia_casada.group(1).strip()
            resultado["apellido_casada"] = _texto_opcional(
                coincidencia_casada.group(2)
            )

    partes = base.split()
    if not partes:
        return resultado

    if len(partes) == 1:
        resultado["primer_nombre"] = partes[0]
    elif len(partes) == 2:
        resultado["primer_nombre"] = partes[0]
        resultado["primer_apellido"] = partes[1]
    elif len(partes) == 3:
        resultado["primer_nombre"] = partes[0]
        resultado["primer_apellido"] = partes[1]
        resultado["segundo_apellido"] = partes[2]
    else:
        resultado["primer_nombre"] = partes[0]
        resultado["segundo_nombre"] = " ".join(partes[1:-2]) or None
        resultado["primer_apellido"] = partes[-2]
        resultado["segundo_apellido"] = partes[-1]

    return resultado


def _buscar_identificador(
    texto: str,
    patrones: tuple[str, ...],
) -> str | None:
    """Devuelve el primer identificador claramente etiquetado que se encuentre."""

    for patron in patrones:
        valor = _texto_opcional(_buscar(patron, texto))
        if valor:
            return valor
    return None


def _monto(valor: str | None) -> float | None:
    """Convierte un importe textual del comprobante en un valor numérico."""

    if not valor:
        return None
    return float(valor.replace(",", ""))


def _fecha_ddmmyyyy(valor: str | None):
    """Convierte una fecha DD/MM/YYYY válida o devuelve ``None``."""

    if not valor:
        return None
    try:
        return datetime.strptime(valor, "%d/%m/%Y").date()
    except ValueError:
        return None


def _normalizar_sistema(texto: str) -> tuple[str, str]:
    """Mapea el nombre textual del sistema a su código y etiqueta canónicos."""

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
    """Clasifica la prestación detectada como mensual, pago único o desconocida."""

    texto = (prestacion or "").upper()

    if "PENSIÓN" in texto or "PENSION" in texto:
        return "PENSION_MENSUAL"

    if "INDEMNIZ" in texto or "PAGO ÚNICO" in texto or "PAGO UNICO" in texto:
        return "PAGO_UNICO"

    return "NO_IDENTIFICADA"


def _extraer_registros(texto: str) -> list[RegistroReferenciaMiRetiroSeguro]:
    """Extrae filas anuales preservando su clasificación histórica/proyectada."""

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

    fecha_ingreso_css = _fecha_ddmmyyyy(
        _buscar(r"Fecha de Ingreso CSS:\s*(\d{2}/\d{2}/\d{4})", texto)
    )

    historicos = [registro for registro in registros if registro.tipo == "HISTORICO"]
    if fecha_ingreso_css and historicos:
        anio_historico_inicial = min(registro.anio for registro in historicos)
        if anio_historico_inicial < fecha_ingreso_css.year:
            advertencias.append(
                "El comprobante contiene historial desde "
                f"{anio_historico_inicial}, anterior a la fecha de ingreso CSS "
                f"indicada ({fecha_ingreso_css.strftime('%d/%m/%Y')}). "
                "Los registros se conservarán porque aparecen en el documento; "
                "revisa esta diferencia antes de continuar si necesitas confirmarla."
            )

    # Se priorizan componentes etiquetados explícitamente. Si el comprobante
    # solo ofrece un nombre completo, se aplica una descomposición conservadora
    # que el Asegurado(a) puede revisar antes de importar.
    primer_nombre = _texto_opcional(_buscar(r"Primer\s+Nombre:\s*([^\n\r]+)", texto))
    segundo_nombre = _texto_opcional(_buscar(r"Segundo\s+Nombre:\s*([^\n\r]+)", texto))
    primer_apellido = _texto_opcional(_buscar(r"Primer\s+Apellido:\s*([^\n\r]+)", texto))
    segundo_apellido = _texto_opcional(_buscar(r"Segundo\s+Apellido:\s*([^\n\r]+)", texto))
    apellido_casada = _texto_opcional(_buscar(r"Apellido\s+de\s+Casada:\s*([^\n\r]+)", texto))
    nombre_completo = _texto_opcional(
        _buscar(r"(?:Nombre\s+Completo|Nombre):\s*([^\n\r]+)", texto)
    )

    if nombre_completo and not any(
        (primer_nombre, segundo_nombre, primer_apellido, segundo_apellido)
    ):
        componentes = _descomponer_nombre_completo(nombre_completo, sexo_codigo)
        primer_nombre = componentes["primer_nombre"]
        segundo_nombre = componentes["segundo_nombre"]
        primer_apellido = componentes["primer_apellido"]
        segundo_apellido = componentes["segundo_apellido"]
        apellido_casada = apellido_casada or componentes["apellido_casada"]

    cedula = _buscar_identificador(
        texto,
        (
            r"C[eé]dula(?:\s+de\s+Identidad\s+Personal)?\s*[:#-]\s*([^\n\r]+)",
            r"(?:No\.?|Nro\.?|N[°º])\s*(?:de\s+)?C[eé]dula\s*[:#-]?\s*([A-Z0-9-]+)",
        ),
    )
    numero_seguro_social = _buscar_identificador(
        texto,
        (
            r"N[uú]mero\s+(?:de\s+)?Seguro\s+Social\s*[:#-]\s*([A-Z0-9-]+)",
            r"(?:No\.?|Nro\.?|N[°º])\s*(?:de\s+)?Seguro\s+Social\s*[:#-]?\s*([A-Z0-9-]+)",
            r"NSS\s*[:#-]\s*([A-Z0-9-]+)",
            r"Seguro\s+Social\s*:\s*([A-Z0-9-]+)",
        ),
    )

    return ResumenReferenciaMiRetiroSeguro(
        primer_nombre=primer_nombre,
        segundo_nombre=segundo_nombre,
        primer_apellido=primer_apellido,
        segundo_apellido=segundo_apellido,
        apellido_casada=apellido_casada,
        nombre_completo_detectado=nombre_completo,
        cedula=cedula,
        numero_seguro_social=numero_seguro_social,
        fecha_comprobante=_fecha_ddmmyyyy(
            _buscar(r"Fecha de Comprobante:\s*(\d{2}/\d{2}/\d{4})", texto)
        ),
        fecha_decision_texto=_buscar(r"Fecha de decisión:\s*([^\n\r]+)", texto),
        fecha_nacimiento=_fecha_ddmmyyyy(
            _buscar(r"Fecha de Nacimiento:\s*(\d{2}/\d{2}/\d{4})", texto)
        ),
        sexo=sexo_codigo,
        fecha_ingreso_css=fecha_ingreso_css,
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

    total_caracteres = 0
    try:
        for pagina in lector.pages:
            texto_pagina = pagina.extract_text() or ""
            total_caracteres += len(texto_pagina)
            if total_caracteres > 1500000:
                raise ValueError(
                    "El comprobante contiene demasiado texto para este importador."
                )
            partes.append(texto_pagina)
    except ValueError:
        raise
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
