"""
Análisis de Riesgo - Simulación Monte Carlo
Evaluación probabilística de escenarios
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from calculators.monte_carlo import MonteCarloSimulator
from visualizations.charts import PensionCharts
from utils.formatters import formato_clp, formato_porcentaje

st.set_page_config(
    page_title="Análisis de Riesgo",
    page_icon="🎲",
    layout="wide"
)

st.title("🎲 Análisis de Riesgo - Monte Carlo")
st.markdown("Evalúa tu pensión bajo diferentes escenarios probabilísticos")

# Verificar si hay resultados previos
if 'parametros' not in st.session_state:
    st.warning("⚠️ Primero debes ejecutar una simulación en la página **Simulador**")
    st.stop()

parametros_base = st.session_state['parametros']

st.info(f"""
**Parámetros base de la simulación:**
- Edad: {parametros_base['edad_actual']} → {parametros_base['edad_jubilacion']} años
- Ingreso: {formato_clp(parametros_base['ingreso_mensual'])}
- Rentabilidad: {formato_porcentaje(parametros_base['rentabilidad_nominal'])}
""")

# Configuración Monte Carlo
st.sidebar.header("⚙️ Configuración Monte Carlo")

n_simulaciones = st.sidebar.select_slider(
    "Número de Simulaciones",
    options=[1000, 5000, 10000, 20000],
    value=10000,
    help="Más simulaciones = mayor precisión pero más tiempo"
)

volatilidad_rent = st.sidebar.slider(
    "Volatilidad Rentabilidad (%)",
    min_value=0.5,
    max_value=5.0,
    value=2.0,
    step=0.5,
    help="Desviación estándar de la rentabilidad"
)

volatilidad_inf = st.sidebar.slider(
    "Volatilidad Inflación (%)",
    min_value=0.2,
    max_value=3.0,
    value=1.0,
    step=0.2,
    help="Desviación estándar de la inflación"
)

prob_desempleo = st.sidebar.slider(
    "Probabilidad Desempleo Anual (%)",
    min_value=0.0,
    max_value=20.0,
    value=5.0,
    step=1.0,
    help="Probabilidad de estar desempleado cada año"
) / 100

ejecutar_mc = st.sidebar.button("🎲 Ejecutar Simulación Monte Carlo", type="primary", use_container_width=True)

if ejecutar_mc or 'mc_resultados' in st.session_state:

    if ejecutar_mc:
        with st.spinner(f"⏳ Ejecutando {n_simulaciones:,} simulaciones..."):
            simulator = MonteCarloSimulator(n_simulaciones=n_simulaciones)

            resultados_mc = simulator.simular_escenarios(
                parametros_base=parametros_base,
                volatilidad_rentabilidad=volatilidad_rent / 100,
                volatilidad_inflacion=volatilidad_inf / 100,
                prob_desempleo_anual=prob_desempleo
            )

            st.session_state['mc_resultados'] = resultados_mc

        st.success(f"✅ {resultados_mc['n_simulaciones']:,} simulaciones completadas")

    resultados_mc = st.session_state['mc_resultados']

    # Métricas principales
    st.subheader("📊 Resultados Probabilísticos")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Escenario Pesimista (P10)",
            formato_clp(resultados_mc['pension_rp']['percentil_10']),
            help="10% de probabilidad de obtener menos"
        )

    with col2:
        st.metric(
            "Escenario Base (Mediana)",
            formato_clp(resultados_mc['pension_rp']['mediana']),
            help="50% de probabilidad a cada lado"
        )

    with col3:
        st.metric(
            "Escenario Optimista (P90)",
            formato_clp(resultados_mc['pension_rp']['percentil_90']),
            help="90% de probabilidad de obtener menos"
        )

    with col4:
        st.metric(
            "Promedio",
            formato_clp(resultados_mc['pension_rp']['promedio']),
            f"±{formato_clp(resultados_mc['pension_rp']['desviacion_std'])}"
        )

    st.divider()

    # Gráfico de distribución
    charts = PensionCharts()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Distribución de Resultados")
        fig_mc = charts.grafico_monte_carlo(resultados_mc)
        st.plotly_chart(fig_mc, use_container_width=True)

    with col2:
        st.subheader("Percentiles Clave")

        percentiles_data = {
            "Percentil": ["P5", "P10", "P25", "P50", "P75", "P90", "P95"],
            "Pensión": [
                formato_clp(resultados_mc['pension_rp']['percentil_5']),
                formato_clp(resultados_mc['pension_rp']['percentil_10']),
                formato_clp(resultados_mc['pension_rp']['percentil_25']),
                formato_clp(resultados_mc['pension_rp']['mediana']),
                formato_clp(resultados_mc['pension_rp']['percentil_75']),
                formato_clp(resultados_mc['pension_rp']['percentil_90']),
                formato_clp(resultados_mc['pension_rp']['percentil_95']),
            ]
        }

        st.table(percentiles_data)

    # Interpretación
    st.divider()
    st.subheader("📖 Interpretación")

    p10 = resultados_mc['pension_rp']['percentil_10']
    p50 = resultados_mc['pension_rp']['mediana']
    p90 = resultados_mc['pension_rp']['percentil_90']

    rango = p90 - p10
    rango_pct = (rango / p50) * 100

    st.info(f"""
    **Análisis de Incertidumbre:**

    - Tu pensión tiene un **rango de variación del {rango_pct:.1f}%** entre escenarios pesimistas y optimistas
    - El **80% de los escenarios** cae entre {formato_clp(p10)} y {formato_clp(p90)}
    - En el **peor escenario** (P5): {formato_clp(resultados_mc['pension_rp']['percentil_5'])}
    - En el **mejor escenario** (P95): {formato_clp(resultados_mc['pension_rp']['percentil_95'])}

    **Recomendación:** Planifica con el escenario pesimista (P10-P25) para estar preparado.
    """)

    # Probabilidad de alcanzar objetivo
    st.divider()
    st.subheader("🎯 Probabilidad de Alcanzar Objetivos")

    objetivo = st.slider(
        "Define tu pensión objetivo mensual (CLP)",
        min_value=100000,
        max_value=3000000,
        value=500000,
        step=50000
    )

    pension_dist = resultados_mc['distribucion_completa']['pension_rp']
    prob_alcanzar = (sum(1 for p in pension_dist if p >= objetivo) / len(pension_dist)) * 100

    if prob_alcanzar >= 75:
        st.success(f"✅ **{prob_alcanzar:.1f}% de probabilidad** de alcanzar o superar {formato_clp(objetivo)}")
    elif prob_alcanzar >= 50:
        st.warning(f"⚠️ **{prob_alcanzar:.1f}% de probabilidad** de alcanzar o superar {formato_clp(objetivo)}")
    else:
        st.error(f"❌ **Solo {prob_alcanzar:.1f}% de probabilidad** de alcanzar {formato_clp(objetivo)}")

else:
    st.info("👈 Configura los parámetros y ejecuta la simulación Monte Carlo")
