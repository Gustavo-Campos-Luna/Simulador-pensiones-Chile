"""
Simulación Monte Carlo para Análisis de Riesgo
Permite evaluar la incertidumbre en las proyecciones de pensión
"""

import numpy as np
import pandas as pd
from typing import Dict, List
from .pension_engine import PensionCalculator


class MonteCarloSimulator:
    """Simulador Monte Carlo para análisis de riesgo en pensiones."""

    def __init__(self, n_simulaciones: int = 10000):
        """
        Inicializa el simulador.

        Args:
            n_simulaciones: Número de simulaciones a ejecutar
        """
        self.n_simulaciones = n_simulaciones
        self.calculator = PensionCalculator()

    def simular_escenarios(
        self,
        parametros_base: Dict,
        volatilidad_rentabilidad: float = 0.02,
        volatilidad_inflacion: float = 0.01,
        prob_desempleo_anual: float = 0.05,
        seed: int = 42
    ) -> Dict:
        """
        Ejecuta simulación Monte Carlo con parámetros variables.

        Args:
            parametros_base: Parámetros base de la simulación
            volatilidad_rentabilidad: Desviación estándar de rentabilidad (ej: 0.02 = 2%)
            volatilidad_inflacion: Desviación estándar de inflación
            prob_desempleo_anual: Probabilidad de desempleo por año
            seed: Semilla para reproducibilidad

        Returns:
            Dict con estadísticas de los escenarios
        """
        np.random.seed(seed)

        resultados_pension_rp = []
        resultados_pension_rv = []
        resultados_saldo = []
        resultados_tasa_reemplazo = []

        rent_base = parametros_base['rentabilidad_nominal']
        inflacion_base = parametros_base['inflacion_esperada']
        anos_cotizacion = parametros_base['edad_jubilacion'] - parametros_base['edad_actual']

        for i in range(self.n_simulaciones):
            # Variar rentabilidad (distribución normal)
            rentabilidad_sim = np.random.normal(rent_base, volatilidad_rentabilidad * 100)
            rentabilidad_sim = max(0, rentabilidad_sim)  # No permitir rentabilidad negativa extrema

            # Variar inflación
            inflacion_sim = np.random.normal(inflacion_base, volatilidad_inflacion * 100)
            inflacion_sim = max(0, inflacion_sim)

            # Simular lagunas aleatorias por desempleo
            anos_lagunas_sim = np.random.binomial(anos_cotizacion, prob_desempleo_anual)

            # Crear parámetros modificados
            params_sim = parametros_base.copy()
            params_sim['rentabilidad_nominal'] = rentabilidad_sim
            params_sim['inflacion_esperada'] = inflacion_sim
            params_sim['anos_lagunas'] = anos_lagunas_sim
            params_sim['distribucion_lagunas'] = 'Aleatorio'

            # Calcular pensión para este escenario
            resultado = self.calculator.calcular_pension_completa(**params_sim)

            if 'error' not in resultado:
                resultados_pension_rp.append(resultado['pension_rp_nominal'])
                resultados_pension_rv.append(resultado['pension_rv_nominal'])
                resultados_saldo.append(resultado['saldo_final_nominal'])
                resultados_tasa_reemplazo.append(resultado['tasa_reemplazo_rp'])

        # Calcular estadísticas
        return {
            'pension_rp': {
                'percentil_5': np.percentile(resultados_pension_rp, 5),
                'percentil_10': np.percentile(resultados_pension_rp, 10),
                'percentil_25': np.percentile(resultados_pension_rp, 25),
                'mediana': np.percentile(resultados_pension_rp, 50),
                'percentil_75': np.percentile(resultados_pension_rp, 75),
                'percentil_90': np.percentile(resultados_pension_rp, 90),
                'percentil_95': np.percentile(resultados_pension_rp, 95),
                'promedio': np.mean(resultados_pension_rp),
                'desviacion_std': np.std(resultados_pension_rp),
                'minimo': np.min(resultados_pension_rp),
                'maximo': np.max(resultados_pension_rp),
            },
            'pension_rv': {
                'percentil_5': np.percentile(resultados_pension_rv, 5),
                'percentil_10': np.percentile(resultados_pension_rv, 10),
                'mediana': np.percentile(resultados_pension_rv, 50),
                'percentil_90': np.percentile(resultados_pension_rv, 90),
                'percentil_95': np.percentile(resultados_pension_rv, 95),
                'promedio': np.mean(resultados_pension_rv),
            },
            'saldo_final': {
                'percentil_10': np.percentile(resultados_saldo, 10),
                'mediana': np.percentile(resultados_saldo, 50),
                'percentil_90': np.percentile(resultados_saldo, 90),
                'promedio': np.mean(resultados_saldo),
            },
            'tasa_reemplazo': {
                'percentil_10': np.percentile(resultados_tasa_reemplazo, 10),
                'mediana': np.percentile(resultados_tasa_reemplazo, 50),
                'percentil_90': np.percentile(resultados_tasa_reemplazo, 90),
                'promedio': np.mean(resultados_tasa_reemplazo),
            },
            'distribucion_completa': {
                'pension_rp': resultados_pension_rp,
                'saldo': resultados_saldo,
                'tasa_reemplazo': resultados_tasa_reemplazo
            },
            'n_simulaciones': len(resultados_pension_rp)
        }

    def analizar_sensibilidad(
        self,
        parametros_base: Dict,
        parametro_variable: str,
        rango_valores: List[float]
    ) -> pd.DataFrame:
        """
        Analiza sensibilidad de un parámetro específico.

        Args:
            parametros_base: Parámetros base
            parametro_variable: Nombre del parámetro a variar
            rango_valores: Lista de valores a probar

        Returns:
            DataFrame con resultados de sensibilidad
        """
        resultados = []

        for valor in rango_valores:
            params = parametros_base.copy()
            params[parametro_variable] = valor

            resultado = self.calculator.calcular_pension_completa(**params)

            if 'error' not in resultado:
                resultados.append({
                    'valor_parametro': valor,
                    'parametro': parametro_variable,
                    'pension_rp': resultado['pension_rp_nominal'],
                    'pension_rv': resultado['pension_rv_nominal'],
                    'saldo_final': resultado['saldo_final_nominal'],
                    'tasa_reemplazo': resultado['tasa_reemplazo_rp']
                })

        return pd.DataFrame(resultados)

    def comparar_escenarios(
        self,
        escenario_base: Dict,
        escenarios_alternativos: List[Dict]
    ) -> pd.DataFrame:
        """
        Compara múltiples escenarios diferentes.

        Args:
            escenario_base: Escenario base
            escenarios_alternativos: Lista de escenarios a comparar

        Returns:
            DataFrame comparativo
        """
        resultados = []

        # Calcular escenario base
        res_base = self.calculator.calcular_pension_completa(**escenario_base)
        if 'error' not in res_base:
            resultados.append({
                'escenario': 'Base',
                'pension_rp': res_base['pension_rp_nominal'],
                'pension_rv': res_base['pension_rv_nominal'],
                'saldo_final': res_base['saldo_final_nominal'],
                'tasa_reemplazo': res_base['tasa_reemplazo_rp'],
                'tir': res_base['tir_cotizaciones']
            })

        # Calcular escenarios alternativos
        for i, escenario in enumerate(escenarios_alternativos, 1):
            params = escenario_base.copy()
            params.update(escenario['parametros'])

            resultado = self.calculator.calcular_pension_completa(**params)

            if 'error' not in resultado:
                resultados.append({
                    'escenario': escenario.get('nombre', f'Alternativa {i}'),
                    'pension_rp': resultado['pension_rp_nominal'],
                    'pension_rv': resultado['pension_rv_nominal'],
                    'saldo_final': resultado['saldo_final_nominal'],
                    'tasa_reemplazo': resultado['tasa_reemplazo_rp'],
                    'tir': resultado['tir_cotizaciones']
                })

        return pd.DataFrame(resultados)
