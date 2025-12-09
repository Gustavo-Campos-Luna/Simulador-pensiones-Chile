# 💰 Simulador Profesional de Pensiones Chile

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-production--ready-success.svg)

**Simulador de pensiones con análisis financiero avanzado y datos en tiempo real**

[Demo en Vivo](#) • [Documentación](#características) • [Instalación](#instalación)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Tecnologías](#tecnologías)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Metodología](#metodología)
- [Deploy](#deploy)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Contacto](#contacto)

---

## 📖 Descripción

Simulador profesional de pensiones para el sistema previsional chileno (AFP) que permite proyectar el saldo acumulado y la pensión futura considerando múltiples variables financieras y económicas.

### ✨ Características Principales

#### 🧮 **Cálculos Financieros Avanzados**
- ✅ **Valor Presente Neto (VPN)** de cotizaciones
- ✅ **Tasa Interna de Retorno (TIR)** de la inversión previsional
- ✅ **Rentabilidad Real** ajustada por inflación (Fórmula de Fisher)
- ✅ **Proyección año por año** con capitalización compuesta
- ✅ **Análisis de brecha previsional**
- ✅ **Tasa de reemplazo** real y nominal

#### 🎲 **Análisis de Riesgo**
- ✅ **Simulación Monte Carlo** (10,000+ escenarios)
- ✅ **Distribución probabilística** de resultados
- ✅ **Percentiles** (P5, P10, P25, P50, P75, P90, P95)
- ✅ **Análisis de sensibilidad** paramétrica
- ✅ **Escenarios** optimista/base/pesimista
- ✅ **Rangos de confianza** para planificación

#### 📊 **Datos Actualizados en Tiempo Real**
- ✅ **UF del día** (API Banco Central vía mindicador.cl)
- ✅ **Comisiones AFP** reales por administradora
- ✅ **Inflación histórica** (INE)
- ✅ **Rentabilidades** por tipo de fondo (A, B, C, D, E)
- ✅ **Pensión Básica Solidaria** actualizada
- ✅ **Tope imponible** vigente (84.7 UF)

#### 📈 **Visualizaciones Interactivas**
- ✅ Gráficos **Plotly** profesionales e interactivos
- ✅ Evolución del ahorro en el tiempo
- ✅ Comparación Retiro Programado vs Renta Vitalicia
- ✅ Composición del saldo (cotizaciones vs rentabilidad)
- ✅ Flujo de caja anual
- ✅ Distribuciones de probabilidad
- ✅ Impacto de lagunas previsionales

#### 💾 **Exportación y Reportes**
- ✅ **Reportes PDF** profesionales con branding
- ✅ **Excel** con simulación año por año
- ✅ **JSON** para guardar/cargar escenarios
- ✅ Gráficos descargables en alta resolución

---

## 🛠️ Tecnologías

### **Backend / Cálculos**
| Tecnología | Versión | Uso |
|-----------|---------|-----|
| **Python** | 3.9+ | Lenguaje principal |
| **NumPy** | 1.24+ | Cálculos numéricos y arrays |
| **Pandas** | 2.0+ | Manipulación de datos y tablas |
| **SciPy** | 1.11+ | Optimización (TIR) y estadística |

### **Frontend / Visualización**
| Tecnología | Versión | Uso |
|-----------|---------|-----|
| **Streamlit** | 1.28+ | Framework web interactivo |
| **Plotly** | 5.17+ | Gráficos interactivos profesionales |

### **Utilidades**
| Tecnología | Versión | Uso |
|-----------|---------|-----|
| **ReportLab** | 4.0+ | Generación de reportes PDF |
| **Requests** | 2.31+ | APIs externas (UF, inflación) |
| **OpenPyXL** | 3.1+ | Exportación a Excel |
| **Pillow** | 10.0+ | Procesamiento de imágenes |

---

## 📦 Requisitos

### **Requisitos del Sistema**
- **Python:** 3.9 o superior
- **pip:** Gestor de paquetes de Python
- **Navegador:** Chrome, Firefox, Safari o Edge (moderno)
- **Conexión a Internet:** Para APIs de datos en tiempo real

### **Dependencias Python**
```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.11.0
plotly>=5.17.0
reportlab>=4.0.0
requests>=2.31.0
pillow>=10.0.0
openpyxl>=3.1.0
python-dateutil>=2.8.0
```

---

## 🚀 Instalación

### **Método 1: Instalación Local**

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU-USUARIO/SimuladorPensionesChile.git
cd SimuladorPensionesChile

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar la aplicación
streamlit run Home.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

### **Método 2: Docker** (Próximamente)

```bash
docker pull simulador-pensiones:latest
docker run -p 8501:8501 simulador-pensiones
```

---

## 💡 Uso

### **Inicio Rápido**

1. **Ejecutar la aplicación:**
   ```bash
   streamlit run Home.py
   ```

2. **Navegar a la sección "Simulador"** en el menú lateral

3. **Configurar parámetros:**
   - Edad actual y de jubilación
   - Ingreso mensual
   - Cotizaciones y comisiones
   - Rentabilidad esperada
   - Lagunas previsionales (opcional)

4. **Click en "Calcular Pensión"**

5. **Explorar resultados:**
   - Saldo acumulado proyectado
   - Pensión mensual estimada
   - Gráficos interactivos
   - Métricas financieras avanzadas

### **Análisis de Riesgo (Monte Carlo)**

1. Ejecutar primero una simulación base
2. Ir a la sección "Análisis de Riesgo"
3. Configurar volatilidad y probabilidades
4. Ejecutar simulación Monte Carlo
5. Analizar distribución de resultados

### **Exportar Resultados**

- **PDF:** Click en "Generar PDF" → Descarga reporte profesional
- **Excel:** Click en "Descargar Excel" → Obtén datos año por año
- **JSON:** Guarda tus simulaciones para cargarlas después

---

## 📂 Estructura del Proyecto

```
SimuladorPensionesChile/
│
├── Home.py                          # Página principal (landing)
│
├── pages/                           # Páginas de la aplicación
│   ├── 1_📊_Simulador.py           # Simulador principal
│   ├── 2_🎲_Análisis_de_Riesgo.py  # Monte Carlo y análisis de riesgo
│   └── 3_📚_Metodología.py         # Documentación y metodología
│
├── src/                             # Código fuente
│   ├── calculators/                 # Motores de cálculo
│   │   ├── __init__.py
│   │   ├── pension_engine.py       # Motor principal de cálculo
│   │   ├── financial_metrics.py    # VPN, TIR, inflación, etc.
│   │   └── monte_carlo.py          # Simulación Monte Carlo
│   │
│   ├── visualizations/              # Visualizaciones
│   │   ├── __init__.py
│   │   └── charts.py               # Gráficos Plotly profesionales
│   │
│   ├── utils/                       # Utilidades
│   │   ├── __init__.py
│   │   ├── formatters.py           # Formato CLP, UF, porcentajes
│   │   ├── validators.py           # Validación de inputs
│   │   └── pdf_generator.py        # Generación de reportes PDF
│   │
│   └── api/                         # Integración con APIs externas
│       ├── __init__.py
│       └── data_sources.py         # APIs: UF, inflación, comisiones AFP
│
├── .streamlit/                      # Configuración de Streamlit
│   └── config.toml                 # Tema corporativo y settings
│
├── requirements.txt                 # Dependencias Python
├── .python-version                  # Versión de Python (3.9)
├── packages.txt                     # Dependencias del sistema (si aplica)
├── .gitignore                       # Archivos excluidos de Git
└── README.md                        # Este archivo
```

---

## 🧮 Metodología

### **Cálculo del Saldo Acumulado**

```python
Para cada año t desde edad_actual hasta edad_jubilacion:

    # 1. Calcular ingreso con aumento anual
    Ingreso_t = Ingreso_(t-1) × (1 + aumento_anual%)

    # 2. Aplicar tope imponible
    Ingreso_imponible = min(Ingreso_t, 84.7 UF)

    # 3. Calcular cotizaciones (si no hay laguna)
    Cotización_t = Ingreso_imponible × (10% + Voluntaria% + Empleador%)
    Comisión_t = Ingreso_imponible × Comisión_AFP%

    # 4. Rentabilidad del saldo anterior
    Rentabilidad_t = Saldo_(t-1) × Rentabilidad_anual%

    # 5. Actualizar saldo
    Saldo_t = Saldo_(t-1) + Rentabilidad_t + Cotización_t - Comisión_t
```

### **Cálculo de Pensión**

**Retiro Programado:**
```python
Pension_RP = Saldo_Final / (Esperanza_Vida - Edad_Jubilacion) / 12
```

**Renta Vitalicia:**
```python
Pension_RV = Pension_RP × Factor_RV
# Factor_RV típicamente 0.92 (92%), configurable
```

### **Métricas Avanzadas**

**Valor Presente Neto:**
```python
VPN = Σ [Cotización_t / (1 + tasa_descuento)^t]
```

**Rentabilidad Real (Fórmula de Fisher):**
```python
Rentabilidad_Real = (1 + Rent_Nominal) / (1 + Inflación) - 1
```

**TIR (Tasa Interna de Retorno):**
```python
Encuentra TIR donde:
0 = Σ [Cotización_t / (1 + TIR)^t] - Saldo_Final
# Resuelto numéricamente con método Newton-Raphson
```

---

## 🌐 Deploy en Streamlit Cloud

### **Deploy Gratuito (Recomendado)**

1. **Subir código a GitHub** (repositorio público)

2. **Ir a Streamlit Cloud:**
   ```
   https://share.streamlit.io
   ```

3. **Crear nueva app:**
   - Repository: `TU-USUARIO/SimuladorPensionesChile`
   - Branch: `main`
   - Main file path: `Home.py`

4. **Deploy!**

**Resultado:** Tu app estará disponible 24/7 en:
```
https://tu-app.streamlit.app
```

### **Configuración Requerida**

- ✅ Repositorio público en GitHub
- ✅ Archivo `requirements.txt` en la raíz
- ✅ Archivo `Home.py` en la raíz
- ✅ Python 3.9+ (especificado en `.python-version`)

**Costo:** $0 USD/mes (plan gratuito ilimitado) ✅

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaFuncionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/NuevaFuncionalidad`)
5. Abre un Pull Request

### **Guías de Contribución**

- Seguir PEP 8 para código Python
- Documentar funciones con docstrings
- Agregar tests para nuevas funcionalidades
- Actualizar README si es necesario

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 👤 Autor

**Gustavo Felipe Campos Luna**

- 📧 Email: [felipecamposluna2001@gmail.com](mailto:felipecamposluna2001@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/gustavo-campos-luna](https://www.linkedin.com/in/gustavo-campos-luna)
- 🌐 GitHub: [@Gustavo-Campos-Luna](https://github.com/Gustavo-Campos-Luna)

---

## 🙏 Agradecimientos

- **Banco Central de Chile** - API pública de indicadores económicos
- **mindicador.cl** - API de UF e indicadores
- **Superintendencia de Pensiones** - Datos públicos de AFPs
- **INE Chile** - Datos de inflación y estadísticas
- **Streamlit Community** - Framework web open source

---

## ⚠️ Disclaimer

**IMPORTANTE:** Este simulador es una herramienta **educativa e informativa**. Los resultados son estimaciones basadas en supuestos y **NO constituyen asesoría financiera profesional**.

- ❌ La rentabilidad futura no está garantizada
- ❌ No se consideran cambios en la legislación previsional
- ❌ Los cálculos son aproximaciones simplificadas
- ✅ Se recomienda consultar con un asesor previsional certificado

**Fuentes de datos:** Banco Central de Chile, Superintendencia de Pensiones, CMF, INE.

---

## 📊 Estadísticas del Proyecto

- **Líneas de código:** ~3,500
- **Archivos Python:** 17
- **Funciones implementadas:** 50+
- **Tests unitarios:** En desarrollo
- **Cobertura:** En desarrollo

---

## 🗺️ Roadmap

### **v1.0 (Actual)**
- ✅ Simulador básico completo
- ✅ Análisis Monte Carlo
- ✅ Exportación PDF/Excel
- ✅ APIs de datos reales

### **v1.1 (Próximo)**
- [ ] Calculadora APV con beneficios tributarios
- [ ] Comparador de AFPs
- [ ] Tests unitarios completos
- [ ] Documentación API

### **v2.0 (Futuro)**
- [ ] Modo multi-usuario con autenticación
- [ ] Dashboard administrativo
- [ ] API REST pública
- [ ] Integración con datos personales (mediante autorización)
- [ ] Análisis comparativo internacional

---

## 📞 Soporte

¿Encontraste un bug? ¿Tienes una sugerencia?

- **Issues:** [GitHub Issues](https://github.com/TU-USUARIO/SimuladorPensionesChile/issues)
- **Discusiones:** [GitHub Discussions](https://github.com/TU-USUARIO/SimuladorPensionesChile/discussions)
- **Email:** felipecamposluna2001@gmail.com

---

<div align="center">

**Hecho con ❤️ en Chile**

⭐ Si este proyecto te resultó útil, ¡dale una estrella!

[⬆ Volver arriba](#-simulador-profesional-de-pensiones-chile)

</div>
