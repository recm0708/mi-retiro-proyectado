"""Mi Retiro Proyectado — nombre del módulo.

Propósito:
    Explicar la responsabilidad permanente del módulo.

Alcance:
    Indicar qué contrato cubre y qué queda fuera de este archivo.
"""

from __future__ import annotations


def funcion_de_ejemplo(valor: str) -> str:
    """Normaliza un valor de ejemplo sin aplicar lógica de negocio real."""
    # Validación defensiva: evita propagar valores vacíos cuando el contrato exige texto.
    if not valor:
        return "valor-pendiente"

    return valor.strip()
