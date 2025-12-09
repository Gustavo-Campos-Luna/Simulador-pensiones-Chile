"""
Validadores de Inputs
Validación de parámetros de entrada para el simulador
"""

from typing import Tuple, Optional


def validar_edad(edad: int, minima: int = 18, maxima: int = 70) -> Tuple[bool, Optional[str]]:
    """
    Valida que la edad esté en un rango válido.

    Args:
        edad: Edad a validar
        minima: Edad mínima permitida
        maxima: Edad máxima permitida

    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if edad < minima:
        return False, f"La edad debe ser al menos {minima} años"
    if edad > maxima:
        return False, f"La edad no puede ser mayor a {maxima} años"
    return True, None


def validar_ingreso(ingreso: float, minimo: float = 350000, maximo: float = 100000000) -> Tuple[bool, Optional[str]]:
    """
    Valida que el ingreso esté en un rango razonable.

    Args:
        ingreso: Ingreso mensual
        minimo: Ingreso mínimo (aprox. sueldo mínimo Chile)
        maximo: Ingreso máximo razonable

    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if ingreso < minimo:
        return False, f"El ingreso debe ser al menos ${minimo:,.0f}".replace(",", ".")
    if ingreso > maximo:
        return False, f"El ingreso parece muy alto (máx ${maximo:,.0f})".replace(",", ".")
    return True, None


def validar_rango_jubilacion(edad_actual: int, edad_jubilacion: int,
                            esperanza_vida: int) -> Tuple[bool, Optional[str]]:
    """
    Valida que las edades de jubilación y esperanza de vida sean coherentes.

    Args:
        edad_actual: Edad actual
        edad_jubilacion: Edad de jubilación
        esperanza_vida: Esperanza de vida

    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if edad_jubilacion <= edad_actual:
        return False, "La edad de jubilación debe ser mayor a la edad actual"

    if esperanza_vida <= edad_jubilacion:
        return False, "La esperanza de vida debe ser mayor a la edad de jubilación"

    if edad_jubilacion - edad_actual > 50:
        return False, "El período hasta la jubilación parece muy largo (máx 50 años)"

    return True, None


def validar_porcentaje(valor: float, nombre: str = "Valor",
                       minimo: float = 0, maximo: float = 100) -> Tuple[bool, Optional[str]]:
    """
    Valida que un porcentaje esté en un rango válido.

    Args:
        valor: Valor del porcentaje
        nombre: Nombre del campo
        minimo: Porcentaje mínimo
        maximo: Porcentaje máximo

    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if valor < minimo:
        return False, f"{nombre} debe ser al menos {minimo}%"
    if valor > maximo:
        return False, f"{nombre} no puede ser mayor a {maximo}%"
    return True, None


def validar_cotizacion(cotizacion: float, voluntaria: float = 0) -> Tuple[bool, Optional[str]]:
    """
    Valida parámetros de cotización.

    Args:
        cotizacion: Cotización obligatoria
        voluntaria: Cotización voluntaria

    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if cotizacion < 10:
        return False, "La cotización obligatoria mínima es 10%"

    if cotizacion + voluntaria > 50:
        return False, "La cotización total no puede superar 50%"

    return True, None


def validar_rentabilidad(rentabilidad: float) -> Tuple[bool, Optional[str]]:
    """
    Valida que la rentabilidad esperada sea razonable.

    Args:
        rentabilidad: Rentabilidad anual esperada (%)

    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if rentabilidad < -5:
        return False, "La rentabilidad no puede ser menor a -5% (muy pesimista)"

    if rentabilidad > 15:
        return False, "La rentabilidad parece muy alta (máx 15% recomendado)"

    return True, None


def validar_lagunas(anos_lagunas: int, anos_cotizacion: int) -> Tuple[bool, Optional[str]]:
    """
    Valida que los años de lagunas sean razonables.

    Args:
        anos_lagunas: Años sin cotización
        anos_cotizacion: Total de años de cotización

    Returns:
        Tupla (es_valido, mensaje_error)
    """
    if anos_lagunas < 0:
        return False, "Los años de lagunas no pueden ser negativos"

    if anos_lagunas > anos_cotizacion:
        return False, "Los años de lagunas no pueden ser mayores a los años de cotización"

    if anos_lagunas > anos_cotizacion * 0.5:
        return False, f"Los años de lagunas parecen muy altos ({anos_lagunas} de {anos_cotizacion} años)"

    return True, None


def validar_simulacion_completa(parametros: dict) -> Tuple[bool, Optional[str]]:
    """
    Valida todos los parámetros de la simulación.

    Args:
        parametros: Diccionario con todos los parámetros

    Returns:
        Tupla (es_valido, mensaje_error)
    """
    # Validar edad actual
    valido, mensaje = validar_edad(parametros.get('edad_actual', 0))
    if not valido:
        return False, mensaje

    # Validar ingreso
    valido, mensaje = validar_ingreso(parametros.get('ingreso_mensual', 0))
    if not valido:
        return False, mensaje

    # Validar rango de edades
    valido, mensaje = validar_rango_jubilacion(
        parametros.get('edad_actual', 0),
        parametros.get('edad_jubilacion', 0),
        parametros.get('esperanza_vida', 0)
    )
    if not valido:
        return False, mensaje

    # Validar cotización
    valido, mensaje = validar_cotizacion(
        parametros.get('cotizacion_obligatoria', 0),
        parametros.get('cotizacion_voluntaria', 0)
    )
    if not valido:
        return False, mensaje

    # Validar rentabilidad
    valido, mensaje = validar_rentabilidad(parametros.get('rentabilidad_nominal', 0))
    if not valido:
        return False, mensaje

    # Validar lagunas
    anos_cotizacion = parametros.get('edad_jubilacion', 0) - parametros.get('edad_actual', 0)
    valido, mensaje = validar_lagunas(parametros.get('anos_lagunas', 0), anos_cotizacion)
    if not valido:
        return False, mensaje

    return True, None
