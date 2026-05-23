"""
Utilidades de formateo numerico para el sistema previsional chileno.

Implementa las convenciones locales: separador de miles con punto,
separador decimal con coma, prefijo peso chileno y unidades UF.
"""

from typing import Union

Number = Union[int, float]


def formato_clp(valor: Number, decimales: int = 0) -> str:
    """Formatea un valor monetario en pesos chilenos.

    Args:
        valor: Monto numerico.
        decimales: Digitos decimales (default 0 para pesos enteros).

    Returns:
        Cadena con formato chileno, ej. "$1.234.567".
    """
    if valor is None:
        return "$0"
    try:
        if decimales == 0:
            return f"${int(round(valor)):,}".replace(",", ".")
        formatted = f"${valor:,.{decimales}f}"
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return "$0"


def formato_porcentaje(valor: Number, decimales: int = 1) -> str:
    """Formatea un valor como porcentaje con convencion chilena.

    Args:
        valor: Porcentaje en puntos (ej. 5.5 para 5,5 %).
        decimales: Digitos decimales.

    Returns:
        Cadena, ej. "5,5 %".
    """
    if valor is None:
        return "0,0 %"
    try:
        return f"{valor:.{decimales}f} %".replace(".", ",")
    except (TypeError, ValueError):
        return "0,0 %"


def formato_uf(valor: Number, decimales: int = 2) -> str:
    """Formatea un valor en Unidades de Fomento.

    Args:
        valor: Monto en UF.
        decimales: Digitos decimales.

    Returns:
        Cadena, ej. "UF 1.234,56".
    """
    if valor is None:
        return "UF 0,00"
    try:
        formatted = f"UF {valor:,.{decimales}f}"
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return "UF 0,00"


def formato_numero(valor: Number, decimales: int = 0) -> str:
    """Formatea un numero con separadores de miles chilenos.

    Args:
        valor: Numero a formatear.
        decimales: Digitos decimales.

    Returns:
        Cadena, ej. "1.234.567".
    """
    if valor is None:
        return "0"
    try:
        if decimales == 0:
            return f"{int(round(valor)):,}".replace(",", ".")
        formatted = f"{valor:,.{decimales}f}"
        return formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return "0"


def formato_abreviado(valor: Number) -> str:
    """Formatea valores grandes de forma abreviada (MM, M, K).

    Util para etiquetas de graficos donde el espacio es limitado.

    Args:
        valor: Monto numerico.

    Returns:
        Cadena abreviada, ej. "$1,2MM", "$350M".
    """
    if valor is None:
        return "$0"
    try:
        abs_v = abs(valor)
        if abs_v >= 1_000_000_000:
            return f"${valor / 1_000_000_000:.1f}MM".replace(".", ",")
        if abs_v >= 1_000_000:
            return f"${valor / 1_000_000:.1f}M".replace(".", ",")
        if abs_v >= 1_000:
            return f"${valor / 1_000:.0f}K"
        return formato_clp(valor)
    except (TypeError, ValueError):
        return "$0"


def formato_anos(anos: int) -> str:
    """Devuelve la representacion en texto del numero de años.

    Args:
        anos: Numero entero de anos.

    Returns:
        Cadena gramaticalmente correcta en espanol.
    """
    return "1 ano" if anos == 1 else f"{anos} anos"
