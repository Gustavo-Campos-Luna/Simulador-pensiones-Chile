"""
Utilidades de Formateo
Formateo de números, monedas y texto para Chile
"""

from typing import Union


def formato_clp(valor: Union[int, float], decimales: int = 0) -> str:
    """
    Formatea un valor como moneda chilena.

    Args:
        valor: Valor numérico
        decimales: Número de decimales (default 0)

    Returns:
        String formateado (ej: "$1.234.567")
    """
    if valor is None:
        return "$0"

    try:
        if decimales == 0:
            return f"${int(valor):,}".replace(",", ".")
        else:
            # Formatear con decimales
            formatted = f"${valor:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return formatted
    except:
        return "$0"


def formato_porcentaje(valor: Union[int, float], decimales: int = 1) -> str:
    """
    Formatea un valor como porcentaje.

    Args:
        valor: Valor numérico (ej: 5.5 para 5.5%)
        decimales: Número de decimales

    Returns:
        String formateado (ej: "5,5%")
    """
    if valor is None:
        return "0%"

    try:
        formatted = f"{valor:.{decimales}f}%".replace(".", ",")
        return formatted
    except:
        return "0%"


def formato_uf(valor: Union[int, float], decimales: int = 2) -> str:
    """
    Formatea un valor en UF.

    Args:
        valor: Valor numérico
        decimales: Número de decimales

    Returns:
        String formateado (ej: "UF 1.234,56")
    """
    if valor is None:
        return "UF 0,00"

    try:
        formatted = f"UF {valor:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return formatted
    except:
        return "UF 0,00"


def formato_numero(valor: Union[int, float], decimales: int = 0) -> str:
    """
    Formatea un número con separadores de miles chilenos.

    Args:
        valor: Valor numérico
        decimales: Número de decimales

    Returns:
        String formateado (ej: "1.234.567")
    """
    if valor is None:
        return "0"

    try:
        if decimales == 0:
            return f"{int(valor):,}".replace(",", ".")
        else:
            formatted = f"{valor:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")
            return formatted
    except:
        return "0"


def formato_abreviado(valor: Union[int, float]) -> str:
    """
    Formatea números grandes de forma abreviada.

    Args:
        valor: Valor numérico

    Returns:
        String formateado (ej: "1,2M", "350K")
    """
    if valor is None:
        return "0"

    try:
        abs_valor = abs(valor)

        if abs_valor >= 1_000_000_000:
            return f"${valor / 1_000_000_000:.1f}B".replace(".", ",")
        elif abs_valor >= 1_000_000:
            return f"${valor / 1_000_000:.1f}M".replace(".", ",")
        elif abs_valor >= 1_000:
            return f"${valor / 1_000:.0f}K".replace(".", ",")
        else:
            return formato_clp(valor)
    except:
        return "$0"


def pluralizar(cantidad: int, singular: str, plural: str = None) -> str:
    """
    Retorna la forma singular o plural según la cantidad.

    Args:
        cantidad: Número de elementos
        singular: Forma singular
        plural: Forma plural (si no se proporciona, añade 's')

    Returns:
        String con la forma correcta
    """
    if plural is None:
        plural = singular + "s"

    return singular if cantidad == 1 else plural


def tiempo_transcurrido(anos: int) -> str:
    """
    Formatea años en texto legible.

    Args:
        anos: Número de años

    Returns:
        String formateado (ej: "1 año", "25 años")
    """
    if anos == 1:
        return "1 año"
    else:
        return f"{anos} años"
