"""Validación defensiva de archivos PDF recibidos por la API.

Este módulo centraliza límites, extensión, tipo MIME y firma PDF antes de
entregar bytes a los importadores específicos. Los archivos permanecen en
memoria y siempre se cierran al terminar la lectura.
"""

from __future__ import annotations

from fastapi import HTTPException, UploadFile


TIPOS_MIME_PDF_PERMITIDOS = {
    "application/pdf",
    "application/octet-stream",
    "",
}


async def leer_pdf_subido(
    archivo: UploadFile,
    *,
    limite_bytes: int,
    etiqueta: str,
) -> bytes:
    """Lee un PDF con límite de tamaño y validaciones básicas de contenido."""

    nombre = (archivo.filename or "").strip()
    tipo = (archivo.content_type or "").lower().strip()

    if not nombre.lower().endswith(".pdf"):
        await archivo.close()
        raise HTTPException(
            status_code=415,
            detail=f"Selecciona {etiqueta} en formato PDF.",
        )

    if tipo not in TIPOS_MIME_PDF_PERMITIDOS:
        await archivo.close()
        raise HTTPException(
            status_code=415,
            detail=f"El tipo de archivo recibido para {etiqueta} no corresponde a un PDF.",
        )

    try:
        contenido = await archivo.read(limite_bytes + 1)
    finally:
        await archivo.close()

    if not contenido:
        raise HTTPException(
            status_code=422,
            detail=f"{etiqueta.capitalize()} está vacío.",
        )

    if len(contenido) > limite_bytes:
        limite_mb = limite_bytes // (1024 * 1024)
        raise HTTPException(
            status_code=413,
            detail=f"{etiqueta.capitalize()} supera el límite de {limite_mb} MB permitido.",
        )

    # La cabecera PDF suele estar al inicio. Se admite hasta 1 KiB de prólogo
    # para tolerar archivos válidos generados por herramientas heterogéneas.
    if b"%PDF-" not in contenido[:1024]:
        raise HTTPException(
            status_code=415,
            detail=f"{etiqueta.capitalize()} no contiene una cabecera PDF válida.",
        )

    return contenido
