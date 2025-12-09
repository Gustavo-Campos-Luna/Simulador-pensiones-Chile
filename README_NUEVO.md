# 💰 Simulador Profesional de Pensiones Chile

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

Simulador avanzado de pensiones para Chile con análisis financiero profesional, simulación Monte Carlo, y datos actualizados en tiempo real.

## 🌟 Características Profesionales

### 📊 Cálculos Avanzados
- ✅ **Valor Presente Neto (VPN)** de cotizaciones
- ✅ **Tasa Interna de Retorno (TIR)** de inversión previsional
- ✅ **Rentabilidad Real** ajustada por inflación
- ✅ **Proyección año por año** con lagunas previsionales
- ✅ **Análisis de brecha previsional**
- ✅ **Comparación** Retiro Programado vs Renta Vitalicia

### 🎲 Análisis de Riesgo
- ✅ **Simulación Monte Carlo** (10,000+ escenarios)
- ✅ **Distribución probabilística** de resultados
- ✅ **Percentiles** (P10, P50, P90) para planificación
- ✅ **Análisis de sensibilidad** paramétrica
- ✅ **Escenarios** optimista/base/pesimista

### 📈 Datos Reales Actualizados
- ✅ **UF del día** (API Banco Central)
- ✅ **Comisiones AFP** reales por administradora
- ✅ **Inflación histórica** (INE)
- ✅ **Rentabilidades** por tipo de fondo
- ✅ **Pensión Básica Solidaria** actualizada
- ✅ **Tope imponible** vigente

### 🎨 Visualizaciones Interactivas
- ✅ Gráficos **Plotly** profesionales
- ✅ Evolución del ahorro en el tiempo
- ✅ Composición del saldo (cotizaciones vs rentabilidad)
- ✅ Flujo de caja año por año
- ✅ Distribuciones de probabilidad Monte Carlo

### 💾 Exportación
- ✅ **Reportes PDF** profesionales con branding
- ✅ **Excel** con simulación completa
- ✅ **JSON** para guardar/cargar escenarios
- ✅ Gráficos descargables

## 🚀 Demo en Vivo

**Pruébalo aquí:** [simulador-pensiones-chile.streamlit.app](#) *(próximamente)*

## 📦 Instalación Local

### Requisitos
- Python 3.9+
- pip

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/SimuladorPensionesChile.git
cd SimuladorPensionesChile

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run Home.py
```

La aplicación se abrirá en `http://localhost:8501`

## 📚 Estructura del Proyecto

```
SimuladorPensionesChile/
├── Home.py                          # Página principal
├── pages/
│   ├── 1_📊_Simulador.py           # Simulador principal
│   ├── 2_🎲_Análisis_de_Riesgo.py  # Monte Carlo
│   └── 3_📚_Metodología.py         # Documentación
├── src/
│   ├── calculators/
│   │   ├── pension_engine.py       # Motor de cálculo principal
│   │   ├── financial_metrics.py    # VPN, TIR, etc.
│   │   └── monte_carlo.py          # Simulación Monte Carlo
│   ├── visualizations/
│   │   └── charts.py               # Gráficos Plotly
│   ├── utils/
│   │   ├── formatters.py           # Formato CLP, UF, %
│   │   ├── validators.py           # Validación inputs
│   │   └── pdf_generator.py        # Generador PDF
│   └── api/
│       └── data_sources.py         # APIs externas
├── .streamlit/
│   └── config.toml                 # Configuración tema
├── requirements.txt
└── README.md
```

## 🧮 Metodología

### Cálculo del Saldo

```python
Para cada año t:
  Cotización_t = Sueldo_t × (10% + Voluntaria% + Empleador%)
  Comisión_t = Sueldo_t × Comisión_AFP%
  Rentabilidad_t = Saldo_(t-1) × Rentabilidad_Anual
  Saldo_t = Saldo_(t-1) + Rentabilidad_t + Cotización_t - Comisión_t
```

### Pensión Mensual

**Retiro Programado:**
```python
Pensión_RP = Saldo_Final / (Esperanza_Vida - Edad_Jubilación) / 12
```

**Renta Vitalicia:**
```python
Pensión_RV = Pensión_RP × 0.92  # Factor típico
```

### Análisis Avanzado

**Valor Presente Neto:**
```python
VPN = Σ [Cotización_t / (1 + tasa_descuento)^t]
```

**Rentabilidad Real:**
```python
Rentabilidad_Real = (1 + Rent_Nominal) / (1 + Inflación) - 1
```

## 📊 Fuentes de Datos

| Indicador | Fuente | Actualización |
|-----------|--------|---------------|
| **UF** | [Banco Central](https://www.bcentral.cl) / [mindicador.cl](https://mindicador.cl) | Diaria |
| **Inflación** | [INE](https://www.ine.cl) | Mensual |
| **Comisiones AFP** | [SP Pensiones](https://www.spensiones.cl) | Mensual |
| **Rentabilidades** | SP Pensiones | Mensual |
| **PBS** | [IPS](https://www.ips.gob.cl) | Anual |

## ⚠️ Disclaimer Legal

**IMPORTANTE:** Este simulador es una herramienta **educativa e informativa**.

- ❌ NO constituye asesoría financiera profesional
- ❌ NO garantiza resultados futuros
- ❌ NO considera cambios legislativos
- ✅ Los resultados son **estimaciones** basadas en supuestos

**Recomendación:** Consulta con un asesor previsional certificado antes de tomar decisiones importantes.

## 🛠️ Tecnologías

- **[Streamlit](https://streamlit.io)** - Framework web
- **[Plotly](https://plotly.com/python/)** - Visualizaciones interactivas
- **[NumPy](https://numpy.org)** - Cálculos numéricos
- **[Pandas](https://pandas.pydata.org)** - Manipulación de datos
- **[SciPy](https://scipy.org)** - Optimización (TIR, Monte Carlo)
- **[ReportLab](https://www.reportlab.com)** - Generación PDF
- **[Requests](https://requests.readthedocs.io)** - APIs externas

## 📈 Roadmap

- [ ] Calculadora de APV con beneficios tributarios
- [ ] Comparador de AFPs
- [ ] Simulador de retiro 10%
- [ ] Integración con datos personales (API AFP)
- [ ] Modo multi-usuario con autenticación
- [ ] Análisis comparativo internacional
- [ ] Bot de Telegram/WhatsApp

## 🤝 Contribuciones

Las contribuciones son bienvenidas!

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📧 Contacto

**Desarrollador:** Gustavo Felipe Campos Luna
**Email:** felipecamposluna2001@gmail.com
**LinkedIn:** [linkedin.com/in/gustavo-campos-luna](https://www.linkedin.com/in/gustavo-campos-luna)

## 📄 Licencia

Este proyecto es de código abierto bajo la licencia MIT.

## ⭐ Agradecimientos

- Banco Central de Chile por APIs públicas
- Superintendencia de Pensiones por datos abiertos
- Comunidad de Streamlit

---

**💡 ¿Te resultó útil? ¡Dale una ⭐ al proyecto!**

Hecho con ❤️ para ayudar a los chilenos a planificar su futuro previsional
