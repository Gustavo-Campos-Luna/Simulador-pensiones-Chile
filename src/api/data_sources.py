"""
Cliente de datos macroeconomicos para el simulador de pensiones.

Consume APIs publicas chilenas (mindicador.cl) para obtener la UF,
el IPC mensual y el sueldo minimo en tiempo real. Los datos de AFP
(comisiones, rentabilidades) no tienen API publica confiable y se
mantienen como constantes auditadas con su fuente documentada.

Cache:
    Los resultados se cachean en memoria por sesion para evitar
    llamadas repetidas a la API durante la misma ejecucion.
    En produccion con multiples usuarios se recomienda Redis o
    un cache persistente externo.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constantes reguladas sin API publica disponible
#
# La Superintendencia de Pensiones (SP) publica estos datos en su sitio web
# pero no expone un endpoint JSON de consumo publico y gratuito.
# Fuente oficial para actualizacion manual:
#   Comisiones:      https://www.spensiones.cl/apps/loadEstadisticas/genEstadAFP.php
#   Rentabilidades:  https://www.spensiones.cl/apps/rentabilidad/getRentabilidad.php
#   PBS:             https://www.bcn.cl/leychile (Decretos Supremos anuales)
#
# Estos valores DEBEN revisarse y actualizarse cuando cambie la regulacion.
# Ultima revision: mayo 2025.
# ---------------------------------------------------------------------------

_COMISIONES_AFP: Dict[str, float] = {
    "Capital":   1.44,  # % sobre remuneracion imponible
    "Cuprum":    1.44,
    "Habitat":   1.27,
    "Modelo":    0.58,
    "Planvital": 1.16,
    "Provida":   1.45,
    "Uno":       0.49,
}

# Rentabilidad nominal promedio 10 anos por tipo de fondo
# Fuente: SP Pensiones — serie historica 2014-2024
_RENTABILIDADES_FONDO: Dict[str, float] = {
    "A": 6.8,
    "B": 6.2,
    "C": 5.5,
    "D": 4.8,
    "E": 3.2,
}

# Volatilidad anual estimada (desviacion estandar) por tipo de fondo
# Fuente: calculo propio sobre serie historica SP Pensiones
_VOLATILIDAD_FONDO: Dict[str, float] = {
    "A": 12.0,
    "B": 9.0,
    "C": 6.0,
    "D": 4.0,
    "E": 2.0,
}

# Pension Basica Solidaria por ano
# Fuente: Decretos Supremos MIDESO / Ley 21.563 (PGU)
_PBS_HISTORICA: Dict[int, int] = {
    2025: 225_975,
    2024: 214_296,
    2023: 206_173,
    2022: 193_917,
    2021: 185_004,
    2020: 177_849,
}

# Tope imponible (Art. 16 DL 3.500 — reajustado anualmente)
_TOPE_IMPONIBLE_UF: float = 84.7

# Fallback sueldo minimo si la API no responde
_SUELDO_MINIMO_FALLBACK: int = 500_000

# Fallback inflacion anual INE si la API de IPC no responde
# Fuente: INE — Indice de Precios al Consumidor, variacion anual
_INFLACION_FALLBACK: Dict[int, float] = {
    2024: 4.5,
    2023: 7.6,
    2022: 12.8,
    2021: 7.2,
    2020: 3.0,
    2019: 2.3,
    2018: 2.3,
    2017: 2.2,
    2016: 2.7,
    2015: 4.4,
}


class DataFetcher:
    """Cliente de datos macroeconomicos desde fuentes publicas chilenas.

    Metodos publicos principales:
        obtener_datos_completos() -> Dict   (punto de entrada unico para la UI)
        obtener_uf_actual()       -> float
        obtener_inflacion_anual() -> Dict[int, float]
        obtener_inflacion_promedio(anos) -> float
    """

    _URL_BASE = "https://mindicador.cl/api"
    _TIMEOUT = 6  # segundos

    def __init__(self):
        self._cache: Dict[str, object] = {}

    # ------------------------------------------------------------------
    # API publica — mindicador.cl
    # ------------------------------------------------------------------

    def obtener_uf_actual(self) -> float:
        """Valor de la UF del dia desde mindicador.cl.

        Returns:
            UF en CLP. Fallback: 37.500 si la API no responde.
        """
        clave = f"uf_{datetime.now().date()}"
        if clave in self._cache:
            return self._cache[clave]

        try:
            data = self._get("uf")
            valor = float(data["serie"][0]["valor"])
            self._cache[clave] = valor
            return valor
        except Exception as exc:
            logger.warning("No se pudo obtener la UF: %s", exc)
            return 37_500.0

    def obtener_inflacion_anual(self, anos: int = 10) -> Dict[int, float]:
        """Inflacion anual calculada a partir del IPC mensual de la API.

        Descarga la serie mensual del IPC (variacion porcentual mensual)
        y computa la inflacion anual compuesta para cada año:
            inf_anual = prod(1 + ipc_m/100 for m in year) - 1

        Args:
            anos: Numero de anos hacia atras a incluir.

        Returns:
            Dict {año: inflacion_anual_porcentaje}.
            Fallback historico si la API no responde.
        """
        clave = f"inflacion_anual_{anos}"
        if clave in self._cache:
            return self._cache[clave]

        try:
            data = self._get("ipc")
            serie = data.get("serie", [])
            if not serie:
                raise ValueError("Serie IPC vacia.")

            # Agrupar variaciones mensuales por ano
            variaciones_por_ano: Dict[int, List[float]] = {}
            for entrada in serie:
                fecha_str = entrada.get("fecha", "")
                valor = float(entrada.get("valor", 0))
                ano = int(fecha_str[:4])
                variaciones_por_ano.setdefault(ano, []).append(valor)

            # Inflacion anual compuesta para cada ano con al menos 12 meses
            ano_actual = datetime.now().year
            resultado: Dict[int, float] = {}
            for ano in range(ano_actual - anos, ano_actual + 1):
                meses = variaciones_por_ano.get(ano, [])
                if len(meses) >= 12:
                    factor = 1.0
                    for m in meses:
                        factor *= 1.0 + m / 100.0
                    resultado[ano] = round((factor - 1.0) * 100.0, 2)
                elif meses:
                    # Ano en curso: anualizar los meses disponibles
                    factor = 1.0
                    for m in meses:
                        factor *= 1.0 + m / 100.0
                    n_meses = len(meses)
                    anualizado = ((factor ** (12.0 / n_meses)) - 1.0) * 100.0
                    resultado[ano] = round(anualizado, 2)

            if resultado:
                self._cache[clave] = resultado
                return resultado

        except Exception as exc:
            logger.warning("No se pudo calcular inflacion desde API: %s", exc)

        # Fallback: valores historicos INE conocidos
        return self._inflacion_fallback(anos)

    def obtener_inflacion_promedio(self, anos: int = 5) -> float:
        """Media aritmetica de la inflacion anual de los ultimos N anos.

        Args:
            anos: Ventana de calculo (default 5 anos).

        Returns:
            Promedio en puntos porcentuales, redondeado a 1 decimal.
        """
        historico = self.obtener_inflacion_anual(anos)
        if not historico:
            return 3.5

        ano_actual = datetime.now().year
        valores = [
            v for a, v in historico.items()
            if ano_actual - anos <= a < ano_actual
        ]
        if not valores:
            return 3.5

        return round(sum(valores) / len(valores), 1)

    def obtener_sueldo_minimo(self) -> float:
        """Sueldo minimo vigente desde mindicador.cl.

        Returns:
            Sueldo minimo en CLP. Fallback: 500.000 si la API falla.
        """
        clave = "sueldo_minimo"
        if clave in self._cache:
            return self._cache[clave]

        try:
            data = self._get("sueldo_minimo")
            valor = float(data["serie"][0]["valor"])
            self._cache[clave] = valor
            return valor
        except Exception as exc:
            logger.warning("No se pudo obtener sueldo minimo: %s", exc)
            return _SUELDO_MINIMO_FALLBACK

    # ------------------------------------------------------------------
    # Datos regulados (constantes auditadas)
    # ------------------------------------------------------------------

    def obtener_comisiones_afp(self) -> Dict[str, float]:
        """Comisiones AFP vigentes (SP Pensiones).

        Returns:
            Dict {nombre_afp: comision_sobre_remuneracion_porcentaje}.
        """
        return dict(_COMISIONES_AFP)

    def obtener_rentabilidades_afp(self, fondo: str = "C") -> Dict[str, float]:
        """Rentabilidad y volatilidad historica por tipo de fondo.

        Args:
            fondo: Letra del fondo (A–E).

        Returns:
            Dict con rentabilidad_promedio_10a y volatilidad_estimada.
        """
        return {
            "fondo": fondo,
            "rentabilidad_promedio_10a": _RENTABILIDADES_FONDO.get(fondo, 5.0),
            "volatilidad_estimada": _VOLATILIDAD_FONDO.get(fondo, 6.0),
        }

    def obtener_pension_basica_solidaria(self) -> int:
        """PBS vigente segun Decreto Supremo mas reciente.

        Returns:
            PBS en CLP.
        """
        ano = datetime.now().year
        return _PBS_HISTORICA.get(ano, max(_PBS_HISTORICA.values()))

    def obtener_tope_imponible(self, en_uf: bool = True) -> float:
        """Tope imponible (Art. 16 DL 3.500).

        Args:
            en_uf: True retorna en UF, False en CLP.

        Returns:
            Tope imponible en la unidad solicitada.
        """
        if en_uf:
            return _TOPE_IMPONIBLE_UF
        return _TOPE_IMPONIBLE_UF * self.obtener_uf_actual()

    # ------------------------------------------------------------------
    # Punto de entrada unico para la interfaz
    # ------------------------------------------------------------------

    def obtener_datos_completos(self) -> Dict:
        """Agrega todos los indicadores necesarios para la UI.

        Returns:
            Dict con uf, inflacion_anual, inflacion_promedio, comisiones_afp,
            rentabilidades_fondos, pbs, tope_imponible_uf, tope_imponible_clp,
            sueldo_minimo y fecha_actualizacion.
        """
        return {
            "uf": self.obtener_uf_actual(),
            "inflacion_anual": self.obtener_inflacion_anual(10),
            "inflacion_promedio": self.obtener_inflacion_promedio(5),
            "comisiones_afp": self.obtener_comisiones_afp(),
            "rentabilidades_fondos": {
                f: self.obtener_rentabilidades_afp(f) for f in ("A", "B", "C", "D", "E")
            },
            "pbs": self.obtener_pension_basica_solidaria(),
            "tope_imponible_uf": self.obtener_tope_imponible(en_uf=True),
            "tope_imponible_clp": self.obtener_tope_imponible(en_uf=False),
            "sueldo_minimo": self.obtener_sueldo_minimo(),
            "fecha_actualizacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------

    def _get(self, indicador: str) -> Dict:
        """GET a mindicador.cl/<indicador> con timeout.

        Args:
            indicador: Codigo del indicador (uf, ipc, sueldo_minimo, etc.).

        Returns:
            JSON deserializado como dict.

        Raises:
            requests.HTTPError: Si el servidor responde con error HTTP.
            ValueError: Si la respuesta no contiene datos utiles.
        """
        url = f"{self._URL_BASE}/{indicador}"
        response = requests.get(url, timeout=self._TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if "serie" not in data or not data["serie"]:
            raise ValueError(f"Respuesta sin datos para '{indicador}'.")
        return data

    @staticmethod
    def _inflacion_fallback(anos: int) -> Dict[int, float]:
        """Inflacion anual INE usada si la API de IPC no responde."""
        ano_actual = datetime.now().year
        return {a: v for a, v in _INFLACION_FALLBACK.items() if a >= ano_actual - anos}


# Instancia global compartida por todos los modulos
data_fetcher = DataFetcher()
