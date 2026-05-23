# Simulador de Pensiones Chile

Herramienta de analisis previsional para el sistema AFP chileno. Proyecta el
saldo acumulado y la pension estimada mediante metodos actuariales estandar,
incorpora metricas financieras avanzadas y ofrece analisis de riesgo mediante
simulacion Monte Carlo vectorizada.

---

## Descripcion

El simulador implementa un motor de calculo basado en capitalizacion individual
año a año, coherente con la estructura del sistema AFP establecido por el
Decreto Ley 3.500. Los resultados incluyen indicadores de uso habitual en
gestion de patrimonio y planificacion previsional: VPN, TIR, duracion de
Macaulay del pasivo, DV01, brecha previsional y comparacion de regimenes APV.

El modulo de analisis de riesgo ejecuta hasta 20.000 escenarios Monte Carlo
mediante operaciones vectoriales numpy, sin bucles Python por escenario,
con tiempos de respuesta inferiores a 2 segundos.

---

## Funcionalidades principales

### Proyeccion actuarial
- Acumulacion año a año con capitalizacion compuesta nominal
- Saldo real deflactado a pesos constantes del año de calculo
- Tope imponible dinamico (84,7 UF segun Ley 19.728)
- Modelado de lagunas previsionales por patron de carrera
- Aumento salarial configurable con tope imponible

### Calculo de pension
- Formula de anualidad actuarial para Retiro Programado:
  `PMT = PV x r / (1 - (1+r)^-n)`
- Comparacion Retiro Programado vs. Renta Vitalicia
- Piso de Pension Basica Solidaria (PBS)
- Ajuste por tasa de descuento durante el periodo de retiro

### Metricas financieras
- Valor Presente Neto (VPN) de cotizaciones
- Tasa Interna de Retorno (TIR) — metodo Brent con fallback Newton-Raphson
- Rentabilidad real mediante ecuacion de Fisher exacta
- Valor presente de la corriente de pensiones futuras
- Duracion de Macaulay del pasivo previsional (ALM)
- DV01 por punto base de variacion en la tasa de descuento
- Brecha previsional respecto al objetivo OCDE (70 % de reemplazo)

### APV — Beneficio tributario
- Regimen A: subsidio estatal directo del 15 % (tope 600 UF/año)
- Regimen B: deduccion de base imponible segun tasa marginal
- Recomendacion automatica segun tasa marginal del cotizante
- Proyeccion del capital adicional acumulado por beneficio tributario

### Analisis de riesgo (Monte Carlo)
- Rentabilidad nominal: variable aleatoria normal truncada
- Inflacion: variable aleatoria normal con piso en cero
- Cesantia: proceso de Bernoulli por año
- Implementacion vectorizada (numpy): 50-100x mas rapido que bucle Python
- Estadisticas por percentil: P5, P10, P25, P50, P75, P90, P95
- Coeficiente de variacion y amplitud intercuantil
- Probabilidad de alcanzar pension objetivo configurable
- Analisis de sensibilidad parametrica determinista

### Visualizaciones
- Evolucion del saldo nominal y real
- Composicion del saldo (cotizaciones, rentabilidad, comisiones)
- Flujo de caja previsional anual con eje doble
- Comparacion de modalidades de pension
- Histograma de distribucion Monte Carlo con lineas de percentil
- Fan chart de rangos de confianza
- Analisis de sensibilidad parametrica (2 subplots)
- Comparacion de impacto APV por regimen

### Exportacion
- Reporte PDF con resumen ejecutivo y aviso legal (ReportLab)
- Tabla año a año en Excel (openpyxl)
- Parametros y resumen en JSON (reutilizable entre sesiones)

---

## Estructura del proyecto

```
Simulador-pensiones-Chile/
|
|-- Home.py                          # Pagina de inicio con indicadores macroeconomicos
|
|-- pages/
|   |-- 1_Simulador.py              # Proyeccion individual con metricas avanzadas
|   |-- 2_Analisis_de_Riesgo.py     # Monte Carlo y analisis de sensibilidad
|   |-- 3_Metodologia.py            # Documentacion tecnica y aviso legal
|
|-- src/
|   |-- calculators/
|   |   |-- pension_engine.py       # Motor de calculo (PensionCalculator)
|   |   |-- financial_metrics.py    # VPN, TIR, Fisher, APV, duracion, DV01
|   |   |-- monte_carlo.py          # Monte Carlo vectorizado (MonteCarloSimulator)
|   |
|   |-- visualizations/
|   |   |-- charts.py               # Graficos Plotly (PensionCharts)
|   |
|   |-- utils/
|   |   |-- formatters.py           # Formateo CLP, UF, porcentajes
|   |   |-- validators.py           # Validacion de parametros de entrada
|   |   |-- pdf_generator.py        # Generacion de reportes PDF (ReportLab)
|   |
|   |-- api/
|       |-- data_sources.py         # Cliente APIs publicas (UF, AFP, inflacion)
|
|-- .streamlit/
|   |-- config.toml                 # Tema y configuracion del servidor
|
|-- requirements.txt                # Dependencias Python con versiones fijadas
|-- .python-version                 # Version de Python (3.11)
|-- .gitignore
|-- README.md
```

---

## Instalacion

### Requisitos del sistema
- Python 3.9 o superior
- pip
- Conexion a internet (para APIs de datos en tiempo real)

### Instalacion local

```bash
# Clonar el repositorio
git clone https://github.com/gustavo-campos-luna/simulador-pensiones-chile.git
cd simulador-pensiones-chile

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicacion
streamlit run Home.py
```

La aplicacion estara disponible en `http://localhost:8501`.

### Despliegue en Streamlit Cloud

1. Subir el repositorio a GitHub (publico o privado con acceso).
2. Acceder a [share.streamlit.io](https://share.streamlit.io).
3. Configurar: repositorio, rama `main`, archivo principal `Home.py`.
4. Streamlit Cloud detecta `requirements.txt` automaticamente.

---

## Dependencias

| Libreria | Version minima | Uso |
|---|---|---|
| streamlit | 1.28 | Framework web interactivo |
| numpy | 1.24 | Calculo vectorizado y Monte Carlo |
| pandas | 2.0 | Manipulacion de datos tabulares |
| scipy | 1.11 | Optimizacion numerica (TIR via Brent) |
| plotly | 5.17 | Visualizaciones interactivas |
| reportlab | 4.0 | Generacion de reportes PDF |
| requests | 2.31 | Consumo de APIs externas |
| openpyxl | 3.1 | Exportacion a Excel |
| pillow | 10.0 | Procesamiento de imagenes (PDF) |

---

## Fuentes de datos

| Indicador | Fuente | Frecuencia |
|---|---|---|
| Valor UF | Banco Central via mindicador.cl | Diaria |
| Comisiones AFP | Superintendencia de Pensiones | Mensual (manual) |
| Rentabilidades AFP | Superintendencia de Pensiones | Mensual (manual) |
| Inflacion historica | INE via mindicador.cl | Mensual |
| Pension Basica Solidaria | Decreto Supremo | Anual (manual) |
| Tope imponible | Ley 19.728 | Anual (manual) |

---

## Metodologia resumida

### Acumulacion

```
Saldo_t = Saldo_{t-1} x (1 + r_nominal) + Cotizacion_neta_t
Saldo_real_t = Saldo_nominal_t / (1 + inflacion)^t
```

### Pension — Formula de anualidad

```
PMT = PV x r_m / (1 - (1 + r_m)^-n)
r_m = (1 + r_anual)^(1/12) - 1
```

### Rentabilidad real (Fisher)

```
r_real = (1 + r_nominal) / (1 + inflacion) - 1
```

### TIR (metodo Brent)

```
0 = sum_{t=1}^{T} [C_t / (1 + TIR)^t] - Saldo_Final
```

### Monte Carlo vectorizado

```
G_t = prod_{s=0}^{t} (1 + r_s)
Saldo_Final = G_n x sum_{t=0}^{n-1} [C_t / G_t]
```

---

## Normativa de referencia

- Decreto Ley 3.500 (1980) — Sistema de capitalizacion individual AFP
- Ley 19.728 (2001) — Seguro de Cesantia
- Ley 20.255 (2008) — Reforma Previsional (PBS y APS)
- Ley 21.563 (2024) — Pension Garantizada Universal (PGU)
- Circular SP N° 1.723 — Comisiones AFP vigentes

---

## Aviso legal

Esta herramienta tiene caracter estrictamente educativo e informativo.
Los resultados son estimaciones basadas en supuestos simplificadores y
no constituyen asesoria financiera ni recomendacion de inversion.
La rentabilidad pasada no garantiza rentabilidad futura.
Se recomienda complementar el analisis con un asesor previsional certificado.

---

## Autor

Gustavo Felipe Campos Luna

- LinkedIn: [linkedin.com/in/gustavo-campos-luna](https://www.linkedin.com/in/gustavo-campos-luna)
- GitHub: [github.com/gustavo-campos-luna](https://github.com/gustavo-campos-luna)
- Contacto: camposluna@uc.cl
