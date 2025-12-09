"""
Módulo de Métricas Financieras Avanzadas
Cálculos profesionales: VPN, TIR, Rentabilidad Real, Valor Presente
"""

import numpy as np
from scipy.optimize import newton
from typing import Dict, List, Tuple


def calcular_vpn(flujos: List[float], tasa_descuento: float) -> float:
    """
    Calcula el Valor Presente Neto de una serie de flujos de caja.

    Args:
        flujos: Lista de flujos de caja (cotizaciones netas por año)
        tasa_descuento: Tasa de descuento anual (ej: 0.05 para 5%)

    Returns:
        Valor presente neto
    """
    vpn = sum([flujo / (1 + tasa_descuento) ** t for t, flujo in enumerate(flujos, 1)])
    return vpn


def calcular_tir(flujos: List[float], inversion_inicial: float = 0) -> float:
    """
    Calcula la Tasa Interna de Retorno.

    Args:
        flujos: Lista de flujos de caja
        inversion_inicial: Inversión inicial (negativa)

    Returns:
        TIR como decimal (ej: 0.05 para 5%)
    """
    flujos_completos = [-inversion_inicial] + flujos if inversion_inicial > 0 else flujos

    def npv(tasa):
        return sum([flujo / (1 + tasa) ** t for t, flujo in enumerate(flujos_completos)])

    try:
        tir = newton(npv, x0=0.05, maxiter=100)
        return tir if abs(npv(tir)) < 1 else 0.0
    except:
        return 0.0


def calcular_rentabilidad_real(rentabilidad_nominal: float, inflacion: float) -> float:
    """
    Calcula la rentabilidad real ajustada por inflación usando la fórmula de Fisher.

    Args:
        rentabilidad_nominal: Tasa nominal anual (ej: 0.05 para 5%)
        inflacion: Tasa de inflación anual (ej: 0.03 para 3%)

    Returns:
        Rentabilidad real
    """
    return ((1 + rentabilidad_nominal) / (1 + inflacion)) - 1


def calcular_valor_presente_pension(pension_mensual: float, anos_pension: int,
                                    tasa_descuento: float, inflacion: float) -> float:
    """
    Calcula el valor presente de la pensión considerando inflación.

    Args:
        pension_mensual: Pensión mensual inicial
        anos_pension: Años de pensión
        tasa_descuento: Tasa de descuento anual
        inflacion: Inflación esperada

    Returns:
        Valor presente total de las pensiones
    """
    meses_totales = anos_pension * 12
    vp_total = 0

    for mes in range(1, meses_totales + 1):
        # Ajustar pensión por inflación
        pension_ajustada = pension_mensual * ((1 + inflacion) ** (mes / 12))
        # Descontar al presente
        vp_mes = pension_ajustada / ((1 + tasa_descuento) ** (mes / 12))
        vp_total += vp_mes

    return vp_total


def calcular_tasa_reemplazo_real(pension_mensual: float, sueldo_final: float,
                                  anos_hasta_jubilacion: int, inflacion: float) -> float:
    """
    Calcula la tasa de reemplazo real considerando el poder adquisitivo.

    Args:
        pension_mensual: Pensión mensual al jubilar
        sueldo_final: Sueldo al momento de jubilar
        anos_hasta_jubilacion: Años hasta jubilar
        inflacion: Inflación esperada anual

    Returns:
        Tasa de reemplazo real como porcentaje
    """
    # Ajustar ambos valores al mismo momento temporal (valor real)
    sueldo_real = sueldo_final / ((1 + inflacion) ** anos_hasta_jubilacion)
    pension_real = pension_mensual / ((1 + inflacion) ** anos_hasta_jubilacion)

    return (pension_real / sueldo_real) * 100


def calcular_brecha_previsional(pension_esperada: float, pension_deseada: float,
                                anos_faltantes: int, rentabilidad: float) -> Dict[str, float]:
    """
    Calcula cuánto más debe cotizar para alcanzar la pensión deseada.

    Args:
        pension_esperada: Pensión que se espera con cotizaciones actuales
        pension_deseada: Pensión objetivo
        anos_faltantes: Años que faltan para jubilar
        rentabilidad: Rentabilidad esperada anual

    Returns:
        Dict con brecha mensual y total necesaria
    """
    if pension_esperada >= pension_deseada:
        return {"brecha_mensual": 0, "ahorro_total_necesario": 0, "hay_brecha": False}

    # Calcular capital adicional necesario
    brecha_pension = pension_deseada - pension_esperada
    # Suponer 20 años de pensión (ajustable)
    capital_adicional = brecha_pension * 12 * 20

    # Calcular cotización mensual adicional necesaria
    meses_faltantes = anos_faltantes * 12
    if meses_faltantes > 0:
        # Fórmula de anualidad
        r_mensual = (1 + rentabilidad) ** (1/12) - 1
        if r_mensual > 0:
            cotizacion_mensual = (capital_adicional * r_mensual) / (((1 + r_mensual) ** meses_faltantes) - 1)
        else:
            cotizacion_mensual = capital_adicional / meses_faltantes
    else:
        cotizacion_mensual = 0

    return {
        "brecha_mensual": cotizacion_mensual,
        "ahorro_total_necesario": capital_adicional,
        "hay_brecha": True,
        "brecha_pension_mensual": brecha_pension
    }


def calcular_equivalente_uf(monto_clp: float, valor_uf: float) -> float:
    """
    Convierte un monto de CLP a UF.

    Args:
        monto_clp: Monto en pesos chilenos
        valor_uf: Valor actual de la UF

    Returns:
        Monto en UF
    """
    return monto_clp / valor_uf if valor_uf > 0 else 0
