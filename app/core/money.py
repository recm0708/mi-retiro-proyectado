"""Utilidades monetarias de la aplicación.

Los cálculos monetarios utilizan :class:`decimal.Decimal` para evitar
artefactos binarios de ``float`` y para aplicar un criterio uniforme de
redondeo.

Criterio adoptado:
- conservar la mayor precisión posible durante los cálculos;
- redondear únicamente cuando un resultado monetario se materializa;
- usar ROUND_HALF_UP a dos decimales, salvo que una norma específica
  exija expresamente otro tratamiento.
"""

from decimal import Decimal, ROUND_HALF_UP

CENTAVO = Decimal("0.01")


def a_decimal(valor: int | float | str | Decimal) -> Decimal:
    """Convierte un valor numérico a ``Decimal`` de forma estable."""

    if isinstance(valor, Decimal):
        return valor

    return Decimal(str(valor))


def redondear_decimal(
    valor: int | float | str | Decimal,
) -> Decimal:
    """Redondea un importe a centavos con ``ROUND_HALF_UP``."""

    return a_decimal(valor).quantize(
        CENTAVO,
        rounding=ROUND_HALF_UP,
    )


def redondear_moneda(
    valor: int | float | str | Decimal,
) -> float:
    """Devuelve un importe monetario redondeado a dos decimales."""

    return float(
        redondear_decimal(valor)
    )


def tiene_maximo_dos_decimales(
    valor: int | float | str | Decimal,
) -> bool:
    """Indica si un valor puede representarse exactamente en centavos."""

    decimal = a_decimal(valor)

    return decimal == decimal.quantize(
        CENTAVO,
        rounding=ROUND_HALF_UP,
    )
