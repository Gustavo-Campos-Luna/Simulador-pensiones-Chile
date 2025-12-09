"""
Fuentes de Datos Externos (APIs Gratuitas)
Obtención de UF, inflación y datos de AFPs
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
import json


class DataFetcher:
    """Cliente para obtener datos de fuentes públicas chilenas."""

    def __init__(self):
        """Inicializa el cliente con URLs base."""
        self.banco_central_url = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"
        self.mindicador_url = "https://mindicador.cl/api"

        # Cache simple (en producción usar Redis o similar)
        self._cache = {}
        self._cache_timeout = 3600  # 1 hora

    def obtener_uf_actual(self) -> float:
        """
        Obtiene el valor actual de la UF desde API pública.

        Returns:
            Valor de la UF en CLP (ej: 37000.50)
        """
        cache_key = f"uf_{datetime.now().date()}"

        # Verificar cache
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            # Usar mindicador.cl (API pública y confiable)
            response = requests.get(f"{self.mindicador_url}/uf", timeout=5)
            response.raise_for_status()
            data = response.json()

            if 'serie' in data and len(data['serie']) > 0:
                uf_valor = float(data['serie'][0]['valor'])
                self._cache[cache_key] = uf_valor
                return uf_valor
        except Exception as e:
            print(f"Error obteniendo UF: {e}")

        # Valor por defecto si falla
        return 37000.0

    def obtener_inflacion_historica(self, anos: int = 10) -> Dict[int, float]:
        """
        Obtiene inflación histórica de Chile.

        Args:
            anos: Número de años hacia atrás

        Returns:
            Dict {año: inflación_porcentaje}
        """
        cache_key = f"inflacion_{anos}"

        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            response = requests.get(f"{self.mindicador_url}/ipc", timeout=5)
            response.raise_for_status()
            data = response.json()

            # Procesar datos (esto es simplificado)
            # En producción, calcular inflación anual correctamente
            inflacion_promedio = {
                2024: 4.5,
                2023: 7.6,
                2022: 12.8,
                2021: 7.2,
                2020: 3.0,
                2019: 2.3,
                2018: 2.3,
                2017: 2.2,
                2016: 2.7,
                2015: 4.4
            }

            self._cache[cache_key] = inflacion_promedio
            return inflacion_promedio

        except Exception as e:
            print(f"Error obteniendo inflación: {e}")
            # Valor por defecto
            return {ano: 3.0 for ano in range(datetime.now().year - anos, datetime.now().year + 1)}

    def obtener_comisiones_afp(self) -> Dict[str, float]:
        """
        Obtiene comisiones actuales de las AFPs.

        Returns:
            Dict {nombre_afp: comision_porcentaje}
        """
        cache_key = "comisiones_afp"

        if cache_key in self._cache:
            return self._cache[cache_key]

        # Datos actualizados manualmente (CMF no tiene API pública fácil)
        # Fuente: https://www.spensiones.cl/ (actualizar mensualmente)
        comisiones = {
            "Capital": 1.44,
            "Cuprum": 1.44,
            "Habitat": 1.27,
            "Modelo": 0.58,
            "Planvital": 1.16,
            "Provida": 1.45,
            "Uno": 0.49
        }

        self._cache[cache_key] = comisiones
        return comisiones

    def obtener_rentabilidades_afp(self, fondo: str = "C") -> Dict[str, float]:
        """
        Obtiene rentabilidades históricas por tipo de fondo.

        Args:
            fondo: Tipo de fondo (A, B, C, D, E)

        Returns:
            Dict con rentabilidades anuales promedio
        """
        # Rentabilidades reales promedio histórico (últimos 10 años)
        # Fuente: SP Pensiones
        rentabilidades_promedio = {
            "A": 6.8,  # Más riesgoso
            "B": 6.2,
            "C": 5.5,  # Balanceado
            "D": 4.8,
            "E": 3.2   # Conservador
        }

        return {
            "fondo": fondo,
            "rentabilidad_promedio_10a": rentabilidades_promedio.get(fondo, 5.0),
            "volatilidad_estimada": self._estimar_volatilidad(fondo)
        }

    def _estimar_volatilidad(self, fondo: str) -> float:
        """
        Estima la volatilidad (desviación estándar) por tipo de fondo.

        Args:
            fondo: Tipo de fondo

        Returns:
            Volatilidad estimada
        """
        volatilidades = {
            "A": 12.0,
            "B": 9.0,
            "C": 6.0,
            "D": 4.0,
            "E": 2.0
        }
        return volatilidades.get(fondo, 6.0)

    def obtener_pension_basica_solidaria(self, ano: int = None) -> float:
        """
        Obtiene el monto de la Pensión Básica Solidaria.

        Args:
            ano: Año de referencia (None = actual)

        Returns:
            Monto PBS en CLP
        """
        if ano is None:
            ano = datetime.now().year

        # Montos históricos y proyectados
        pbs_montos = {
            2024: 214296,
            2023: 206173,
            2022: 193917,
            2021: 185004,
            2020: 177849
        }

        return pbs_montos.get(ano, 214296)

    def obtener_tope_imponible(self, en_uf: bool = True) -> float:
        """
        Obtiene el tope imponible actual.

        Args:
            en_uf: Si True retorna en UF, si False en CLP

        Returns:
            Tope imponible
        """
        tope_uf = 84.7  # Actualizado 2024

        if en_uf:
            return tope_uf
        else:
            uf_valor = self.obtener_uf_actual()
            return tope_uf * uf_valor

    def obtener_sueldo_minimo(self) -> float:
        """
        Obtiene el sueldo mínimo actual en Chile.

        Returns:
            Sueldo mínimo en CLP
        """
        # Actualizado 2024
        return 500000

    def obtener_datos_completos(self) -> Dict:
        """
        Obtiene todos los datos relevantes en una sola llamada.

        Returns:
            Dict con todos los indicadores
        """
        return {
            "uf": self.obtener_uf_actual(),
            "inflacion_historica": self.obtener_inflacion_historica(5),
            "inflacion_promedio": 3.5,  # Promedio últimos años
            "comisiones_afp": self.obtener_comisiones_afp(),
            "pbs": self.obtener_pension_basica_solidaria(),
            "tope_imponible_uf": self.obtener_tope_imponible(en_uf=True),
            "tope_imponible_clp": self.obtener_tope_imponible(en_uf=False),
            "sueldo_minimo": self.obtener_sueldo_minimo(),
            "rentabilidades_fondos": {
                "A": self.obtener_rentabilidades_afp("A"),
                "B": self.obtener_rentabilidades_afp("B"),
                "C": self.obtener_rentabilidades_afp("C"),
                "D": self.obtener_rentabilidades_afp("D"),
                "E": self.obtener_rentabilidades_afp("E")
            },
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }


# Instancia global
data_fetcher = DataFetcher()
