"""
Simulador Profesional de Pensiones Chile
Página Principal - Landing Page
"""

import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Configuración de la página
st.set_page_config(
    page_title="Simulador de Pensiones Chile",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-card {
        background: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1E3A8A;
        margin: 1rem 0;
    }
    .cta-button {
        background: #1E3A8A;
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
        font-size: 1.2rem;
        margin: 2rem 0;
    }
    .footer {
        text-align: center;
        color: #6B7280;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<div class="main-header">💰 Simulador Profesional de Pensiones Chile</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Proyecta tu futuro previsional con análisis financiero avanzado</div>', unsafe_allow_html=True)

# Introducción
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    ### 🎯 ¿Por qué usar este simulador?

    Este simulador profesional te ayuda a estimar tu **pensión futura** considerando
    **inflación, rentabilidad real, y análisis de riesgo**, ofreciendo una visión
    realista de tu jubilación.
    """)

st.divider()

# Características principales
st.markdown("### ✨ Características Profesionales")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h4>📊 Cálculos Avanzados</h4>
        <ul>
            <li>Valor Presente Neto (VPN)</li>
            <li>Tasa Interna de Retorno (TIR)</li>
            <li>Rentabilidad Real vs Nominal</li>
            <li>Ajuste por inflación</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h4>🎲 Análisis de Riesgo</h4>
        <ul>
            <li>Simulación Monte Carlo</li>
            <li>Escenarios optimista/pesimista</li>
            <li>Análisis de sensibilidad</li>
            <li>Distribución probabilística</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h4>📈 Datos Reales</h4>
        <ul>
            <li>UF actualizada diariamente</li>
            <li>Comisiones AFP reales</li>
            <li>Inflación histórica</li>
            <li>Rentabilidades por fondo</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Funcionalidades
st.markdown("### 🚀 Funcionalidades")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🧮 Simulador Básico
    - Proyección de saldo acumulado
    - Comparación Retiro Programado vs Renta Vitalicia
    - Análisis de lagunas previsionales
    - Tasa de reemplazo real y nominal
    - Impacto de cotizaciones voluntarias
    """)

    st.markdown("""
    #### 📊 Análisis de Riesgo
    - Simulación Monte Carlo (10,000 escenarios)
    - Rangos de confianza (P10, P50, P90)
    - Análisis de sensibilidad
    - Evaluación de incertidumbre
    """)

with col2:
    st.markdown("""
    #### 🔄 Comparador de Escenarios
    - Comparar múltiples estrategias
    - Evaluar diferentes aportes
    - Análisis "qué pasa si..."
    - Optimización de cotizaciones
    """)

    st.markdown("""
    #### 📄 Exportación
    - Reporte PDF profesional
    - Exportar datos a Excel
    - Guardar/cargar simulaciones
    - Compartir resultados
    """)

st.divider()

# Datos actualizados
from api.data_sources import data_fetcher

with st.spinner("Obteniendo datos actualizados..."):
    try:
        datos = data_fetcher.obtener_datos_completos()

        st.markdown("### 📊 Datos Actualizados")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="UF Actual",
                value=f"${datos['uf']:,.2f}",
                help="Valor de la UF actualizado"
            )

        with col2:
            st.metric(
                label="Inflación Promedio",
                value=f"{datos['inflacion_promedio']}%",
                help="Promedio últimos años"
            )

        with col3:
            st.metric(
                label="Pensión Básica",
                value=f"${datos['pbs']:,}",
                help="Pensión Básica Solidaria"
            )

        with col4:
            st.metric(
                label="Tope Imponible",
                value=f"{datos['tope_imponible_uf']:.1f} UF",
                help=f"${datos['tope_imponible_clp']:,.0f}"
            )

        st.caption(f"Última actualización: {datos['fecha_actualizacion']}")
    except:
        st.info("💡 Los datos se actualizan automáticamente desde fuentes oficiales")

st.divider()

# Call to Action
st.markdown("### 🎯 Comienza tu Simulación")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.info("""
    **👉 Usa el menú lateral** para navegar entre las diferentes herramientas:

    1. **📊 Simulador** - Calcula tu pensión estimada
    2. **🎲 Análisis de Riesgo** - Evalúa escenarios probabilísticos
    3. **🔄 Comparador** - Compara diferentes estrategias
    4. **📚 Metodología** - Conoce cómo funcionan los cálculos
    """)

# Disclaimer
st.divider()
st.warning("""
⚠️ **Disclaimer Legal:**

Este simulador es una herramienta **educativa e informativa**. Los resultados son estimaciones
basadas en los parámetros ingresados y **no constituyen asesoría financiera profesional**.

- La rentabilidad futura no está garantizada
- No se consideran cambios en la legislación
- Se recomienda consultar con un asesor certificado
- Los cálculos son aproximaciones simplificadas

**Fuentes:** Banco Central, Superintendencia de Pensiones, CMF
""")

# Footer
st.markdown("""
<div class="footer">
    <p><b>Simulador Profesional de Pensiones Chile</b></p>
    <p>Desarrollado con Streamlit • Python • Datos Actualizados en Tiempo Real</p>
    <p>© 2024 • Herramienta Gratuita y Open Source</p>
</div>
""", unsafe_allow_html=True)
