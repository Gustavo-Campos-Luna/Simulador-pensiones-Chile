"""
Motor Principal de Cálculo de Pensiones
Simulador profesional con inflación, valor presente, y análisis avanzado
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from .financial_metrics import (
    calcular_vpn, calcular_tir, calcular_rentabilidad_real,
    calcular_valor_presente_pension, calcular_brecha_previsional
)


class PensionCalculator:
    """Calculadora profesional de pensiones con métricas avanzadas."""

    def __init__(self):
        """Inicializa la calculadora con parámetros por defecto."""
        self.TOPE_IMPONIBLE = 84.7  # UF (actualizable)
        self.PENSION_BASICA_SOLIDARIA = 214_296  # CLP (2024)
        self.APORTE_PREVISIONAL_SOLIDARIO_MAX = 214_296

    def calcular_pension_completa(
        self,
        edad_actual: int,
        edad_jubilacion: int,
        esperanza_vida: int,
        ingreso_mensual: float,
        aumento_salarial_anual: float,
        cotizacion_obligatoria: float,
        comision_afp: float,
        aporte_empleador: float,
        cotizacion_voluntaria: float,
        rentabilidad_nominal: float,
        inflacion_esperada: float,
        anos_lagunas: int,
        distribucion_lagunas: str,
        valor_uf: float = 37000,
    ) -> Dict:
        """
        Calcula la pensión con todas las métricas profesionales.

        Args:
            edad_actual: Edad actual del cotizante
            edad_jubilacion: Edad de jubilación
            esperanza_vida: Esperanza de vida
            ingreso_mensual: Ingreso mensual imponible (CLP)
            aumento_salarial_anual: Aumento anual del sueldo (%)
            cotizacion_obligatoria: Cotización obligatoria (%)
            comision_afp: Comisión AFP (%)
            aporte_empleador: Aporte del empleador (%)
            cotizacion_voluntaria: Cotización voluntaria adicional (%)
            rentabilidad_nominal: Rentabilidad esperada anual (%)
            inflacion_esperada: Inflación esperada anual (%)
            anos_lagunas: Años sin cotización
            distribucion_lagunas: Distribución de lagunas
            valor_uf: Valor actual de la UF

        Returns:
            Dict con todos los resultados y métricas
        """
        # Convertir porcentajes a decimales
        aumento_salarial = aumento_salarial_anual / 100
        cotizacion_total = (cotizacion_obligatoria + cotizacion_voluntaria) / 100
        comision = comision_afp / 100
        aporte_emp = aporte_empleador / 100
        rent_nominal = rentabilidad_nominal / 100
        inflacion = inflacion_esperada / 100

        # Calcular rentabilidad real
        rentabilidad_real = calcular_rentabilidad_real(rent_nominal, inflacion)

        # Años de cotización
        anos_cotizacion = edad_jubilacion - edad_actual
        if anos_cotizacion <= 0:
            return self._resultado_error("Edad de jubilación debe ser mayor a edad actual")

        # Generar simulación año por año
        simulacion = self._generar_simulacion_anual(
            anos_cotizacion=anos_cotizacion,
            edad_inicial=edad_actual,
            ingreso_inicial=ingreso_mensual,
            aumento_salarial=aumento_salarial,
            cotizacion_total=cotizacion_total,
            comision=comision,
            aporte_empleador=aporte_emp,
            rentabilidad_nominal=rent_nominal,
            rentabilidad_real=rentabilidad_real,
            anos_lagunas=anos_lagunas,
            distribucion_lagunas=distribucion_lagunas,
            tope_imponible_clp=self.TOPE_IMPONIBLE * valor_uf
        )

        # Calcular pensiones
        saldo_final_nominal = simulacion['saldo_nominal'].iloc[-1]
        saldo_final_real = simulacion['saldo_real'].iloc[-1]
        ultimo_sueldo = simulacion['ingreso_mensual'].iloc[-1]

        anos_pension = esperanza_vida - edad_jubilacion
        if anos_pension <= 0:
            return self._resultado_error("Esperanza de vida debe ser mayor a edad de jubilación")

        # Pensión en Retiro Programado
        pension_rp_nominal = saldo_final_nominal / (anos_pension * 12)
        pension_rp_real = saldo_final_real / (anos_pension * 12)

        # Pensión en Renta Vitalicia (92% del RP típicamente)
        factor_rv = 0.92
        pension_rv_nominal = pension_rp_nominal * factor_rv
        pension_rv_real = pension_rp_real * factor_rv

        # Tasas de reemplazo
        tasa_reemplazo_rp_nominal = (pension_rp_nominal / ultimo_sueldo) * 100
        tasa_reemplazo_rv_nominal = (pension_rv_nominal / ultimo_sueldo) * 100

        # Calcular tasa de reemplazo REAL (ajustada por inflación)
        sueldo_real_inicio = ingreso_mensual
        sueldo_real_final = ultimo_sueldo / ((1 + inflacion) ** anos_cotizacion)
        pension_real_jubilacion = pension_rp_real

        tasa_reemplazo_real = (pension_real_jubilacion / sueldo_real_final) * 100

        # Métricas financieras avanzadas
        flujos_cotizaciones = simulacion['cotizacion_neta_anual'].tolist()
        vpn_cotizaciones = calcular_vpn(flujos_cotizaciones, rentabilidad_real)
        tir_cotizaciones = calcular_tir(flujos_cotizaciones)

        # Valor presente de la pensión
        vp_pension_rp = calcular_valor_presente_pension(
            pension_rp_nominal, anos_pension, rentabilidad_real, inflacion
        )

        # Calcular brecha previsional (objetivo 70% del sueldo)
        pension_objetivo = ultimo_sueldo * 0.70
        brecha = calcular_brecha_previsional(
            pension_rp_nominal,
            pension_objetivo,
            max(anos_cotizacion, 1),
            rent_nominal
        )

        # Pensión Básica Solidaria (PBS) si aplica
        pension_final_rp = max(pension_rp_nominal, self.PENSION_BASICA_SOLIDARIA)
        pension_final_rv = max(pension_rv_nominal, self.PENSION_BASICA_SOLIDARIA)

        return {
            # Resultados principales
            'saldo_final_nominal': saldo_final_nominal,
            'saldo_final_real': saldo_final_real,
            'pension_rp_nominal': pension_rp_nominal,
            'pension_rp_real': pension_rp_real,
            'pension_rv_nominal': pension_rv_nominal,
            'pension_rv_real': pension_rv_real,
            'pension_rp_con_pbs': pension_final_rp,
            'pension_rv_con_pbs': pension_final_rv,

            # Tasas de reemplazo
            'tasa_reemplazo_rp': tasa_reemplazo_rp_nominal,
            'tasa_reemplazo_rv': tasa_reemplazo_rv_nominal,
            'tasa_reemplazo_real': tasa_reemplazo_real,

            # Información del cotizante
            'ultimo_sueldo': ultimo_sueldo,
            'anos_cotizacion': anos_cotizacion,
            'anos_pension': anos_pension,
            'anos_lagunas_efectivos': anos_lagunas,

            # Métricas financieras
            'vpn_cotizaciones': vpn_cotizaciones,
            'tir_cotizaciones': tir_cotizaciones * 100,  # Como porcentaje
            'rentabilidad_real': rentabilidad_real * 100,
            'rentabilidad_nominal': rent_nominal * 100,
            'vp_pension_total': vp_pension_rp,

            # Brecha previsional
            'brecha_previsional': brecha,

            # DataFrame de simulación
            'simulacion_anual': simulacion,

            # Metadata
            'factor_renta_vitalicia': factor_rv,
            'inflacion_esperada': inflacion * 100,
            'valor_uf_usado': valor_uf,
        }

    def _generar_simulacion_anual(
        self,
        anos_cotizacion: int,
        edad_inicial: int,
        ingreso_inicial: float,
        aumento_salarial: float,
        cotizacion_total: float,
        comision: float,
        aporte_empleador: float,
        rentabilidad_nominal: float,
        rentabilidad_real: float,
        anos_lagunas: int,
        distribucion_lagunas: str,
        tope_imponible_clp: float
    ) -> pd.DataFrame:
        """Genera la simulación año por año."""

        # Inicializar DataFrame
        df = pd.DataFrame({
            'ano': range(1, anos_cotizacion + 1),
            'edad': range(edad_inicial, edad_inicial + anos_cotizacion),
            'ingreso_mensual': 0.0,
            'ingreso_imponible': 0.0,
            'cotizacion_anual': 0.0,
            'aporte_empleador_anual': 0.0,
            'comision_anual': 0.0,
            'cotizacion_neta_anual': 0.0,
            'rentabilidad_nominal_anual': 0.0,
            'rentabilidad_real_anual': 0.0,
            'saldo_nominal': 0.0,
            'saldo_real': 0.0,
            'tiene_laguna': False
        })

        # Determinar años con lagunas
        lagunas_indices = self._calcular_lagunas(anos_cotizacion, anos_lagunas, distribucion_lagunas)
        df.loc[lagunas_indices, 'tiene_laguna'] = True

        # Calcular evolución año por año
        saldo_nominal = 0.0
        saldo_real = 0.0

        for i in range(anos_cotizacion):
            # Calcular ingreso con aumento anual
            if i == 0:
                ingreso = ingreso_inicial
            else:
                ingreso = df.loc[i-1, 'ingreso_mensual'] * (1 + aumento_salarial)

            # Aplicar tope imponible
            ingreso_imponible = min(ingreso, tope_imponible_clp)

            df.loc[i, 'ingreso_mensual'] = ingreso
            df.loc[i, 'ingreso_imponible'] = ingreso_imponible

            # Si hay laguna, no hay cotización
            if df.loc[i, 'tiene_laguna']:
                cotizacion_anual = 0
                aporte_empleador_anual = 0
                comision_anual = 0
            else:
                cotizacion_mensual = ingreso_imponible * cotizacion_total
                aporte_emp_mensual = ingreso_imponible * aporte_empleador
                comision_mensual = ingreso_imponible * comision

                cotizacion_anual = cotizacion_mensual * 12
                aporte_empleador_anual = aporte_emp_mensual * 12
                comision_anual = comision_mensual * 12

            cotizacion_neta = cotizacion_anual + aporte_empleador_anual - comision_anual

            df.loc[i, 'cotizacion_anual'] = cotizacion_anual
            df.loc[i, 'aporte_empleador_anual'] = aporte_empleador_anual
            df.loc[i, 'comision_anual'] = comision_anual
            df.loc[i, 'cotizacion_neta_anual'] = cotizacion_neta

            # Actualizar saldo con rentabilidad
            rentabilidad_nominal_anual = saldo_nominal * rentabilidad_nominal
            rentabilidad_real_anual = saldo_real * rentabilidad_real

            saldo_nominal = saldo_nominal + rentabilidad_nominal_anual + cotizacion_neta
            saldo_real = saldo_real + rentabilidad_real_anual + cotizacion_neta

            df.loc[i, 'rentabilidad_nominal_anual'] = rentabilidad_nominal_anual
            df.loc[i, 'rentabilidad_real_anual'] = rentabilidad_real_anual
            df.loc[i, 'saldo_nominal'] = saldo_nominal
            df.loc[i, 'saldo_real'] = saldo_real

        return df

    def _calcular_lagunas(self, anos_totales: int, anos_lagunas: int, distribucion: str) -> List[int]:
        """Calcula qué años tienen lagunas previsionales."""
        if anos_lagunas <= 0 or anos_lagunas > anos_totales:
            return []

        if distribucion == "Aleatorio":
            return np.random.choice(anos_totales, anos_lagunas, replace=False).tolist()
        elif distribucion == "Inicio de carrera":
            return list(range(min(anos_lagunas, anos_totales)))
        elif distribucion == "Mitad de carrera":
            inicio = max(0, (anos_totales // 2) - (anos_lagunas // 2))
            fin = min(anos_totales, inicio + anos_lagunas)
            return list(range(inicio, fin))
        elif distribucion == "Final de carrera":
            inicio = max(0, anos_totales - anos_lagunas)
            return list(range(inicio, anos_totales))
        else:
            return []

    def _resultado_error(self, mensaje: str) -> Dict:
        """Retorna un diccionario de error."""
        return {
            'error': True,
            'mensaje': mensaje,
            'saldo_final_nominal': 0,
            'pension_rp_nominal': 0
        }
