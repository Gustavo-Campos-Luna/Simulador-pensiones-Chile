"""
Simulador Principal de Pensiones
Calculadora completa con visualizaciones profesionales
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from calculators.pension_engine import PensionCalculator
from visualizations.charts import PensionCharts
from utils.formatters import formato_clp, formato_porcentaje, formato_uf
from utils.validators import validar_simulacion_completa
from api.data_sources import data_fetcher
from utils.pdf_generator import PDFReportGenerator

# Configuración de la página
st.set_page_config(
    page_title="Simulador de Pensiones",
    page_icon="📊",
    layout="wide"
)

# Inicializar calculadora y gráficos
calculator = PensionCalculator()
charts = PensionCharts()
pdf_generator = PDFReportGenerator()

# CSS personalizado
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Simulador de Pensiones")
st.markdown("Calcula tu pensión estimada con análisis financiero profesional")

# Obtener datos actualizados
with st.spinner("Cargando datos actualizados..."):
    datos_actualizados = data_fetcher.obtener_datos_completos()

# Sidebar - Parámetros
st.sidebar.header("⚙️ Parámetros de Simulación")

# Sección 1: Datos Personales
st.sidebar.subheader("👤 Datos Personales")

edad_actual = st.sidebar.number_input(
    "Edad Actual",
    min_value=18,
    max_value=70,
    value=30,
    step=1,
    help="Tu edad actual en años"
)

genero = st.sidebar.selectbox(
    "Género",
    options=["Hombre", "Mujer"],
    help="Afecta la edad legal de jubilación"
)

edad_jubilacion_default = 65 if genero == "Hombre" else 60

edad_jubilacion = st.sidebar.number_input(
    "Edad de Jubilación",
    min_value=edad_actual + 1,
    max_value=75,
    value=edad_jubilacion_default,
    step=1,
    help="Edad a la que planeas jubilarte"
)

esperanza_vida_default = 83 if genero == "Hombre" else 89

esperanza_vida = st.sidebar.number_input(
    "Esperanza de Vida",
    min_value=edad_jubilacion + 1,
    max_value=110,
    value=esperanza_vida_default,
    step=1,
    help="Esperanza de vida estimada"
)

# Sección 2: Ingresos
st.sidebar.subheader("💵 Ingresos")

ingreso_mensual = st.sidebar.number_input(
    "Ingreso Mensual Imponible (CLP)",
    min_value=int(datos_actualizados['sueldo_minimo']),
    max_value=50000000,
    value=800000,
    step=50000,
    help="Tu sueldo bruto mensual imponible"
)

aumento_salarial = st.sidebar.slider(
    "Aumento Salarial Anual (%)",
    min_value=0.0,
    max_value=10.0,
    value=2.0,
    step=0.5,
    help="Incremento anual esperado de tu sueldo"
)

# Sección 3: Cotizaciones
st.sidebar.subheader("💳 Cotizaciones")

cotizacion_obligatoria = st.sidebar.number_input(
    "Cotización Obligatoria (%)",
    min_value=10.0,
    max_value=20.0,
    value=10.0,
    step=0.5,
    help="Por ley es 10% en Chile"
)

afps_disponibles = datos_actualizados['comisiones_afp']
afp_seleccionada = st.sidebar.selectbox(
    "AFP",
    options=list(afps_disponibles.keys()),
    index=list(afps_disponibles.keys()).index("Modelo") if "Modelo" in afps_disponibles else 0,
    help="Tu AFP actual o la que consideras"
)

comision_afp = afps_disponibles[afp_seleccionada]
st.sidebar.caption(f"Comisión {afp_seleccionada}: {comision_afp}%")

cotizacion_voluntaria = st.sidebar.slider(
    "Cotización Voluntaria Adicional (%)",
    min_value=0.0,
    max_value=20.0,
    value=0.0,
    step=0.5,
    help="APV u otro ahorro previsional voluntario"
)

aporte_empleador = st.sidebar.slider(
    "Aporte del Empleador (%)",
    min_value=0.0,
    max_value=10.0,
    value=0.0,
    step=0.5,
    help="Si tu empleador aporta adicional"
)

# Sección 4: Rentabilidad e Inflación
st.sidebar.subheader("📈 Rentabilidad e Inflación")

tipo_fondo = st.sidebar.select_slider(
    "Tipo de Fondo",
    options=["E", "D", "C", "B", "A"],
    value="C",
    help="A=Mayor riesgo/retorno, E=Conservador"
)

rentabilidad_fondo = datos_actualizados['rentabilidades_fondos'][tipo_fondo]
rentabilidad_sugerida = rentabilidad_fondo['rentabilidad_promedio_10a']

rentabilidad_nominal = st.sidebar.slider(
    "Rentabilidad Esperada Anual (%)",
    min_value=0.0,
    max_value=12.0,
    value=rentabilidad_sugerida,
    step=0.5,
    help=f"Fondo {tipo_fondo}: promedio histórico {rentabilidad_sugerida}%"
)

inflacion_esperada = st.sidebar.slider(
    "Inflación Esperada Anual (%)",
    min_value=0.0,
    max_value=10.0,
    value=float(datos_actualizados['inflacion_promedio']),
    step=0.5,
    help="Inflación promedio esperada"
)

# Sección 5: Lagunas Previsionales
st.sidebar.subheader("⚠️ Lagunas Previsionales")

anos_cotizacion_total = edad_jubilacion - edad_actual

anos_lagunas = st.sidebar.slider(
    "Años sin Cotización",
    min_value=0,
    max_value=min(20, anos_cotizacion_total),
    value=0,
    step=1,
    help="Períodos sin cotizar (desempleo, etc.)"
)

distribucion_lagunas = st.sidebar.selectbox(
    "Distribución de Lagunas",
    options=["Aleatorio", "Inicio de carrera", "Mitad de carrera", "Final de carrera"],
    help="Cuándo ocurrirán las lagunas"
)

# Botón de simulación
st.sidebar.divider()
simular_btn = st.sidebar.button("🚀 Calcular Pensión", type="primary", use_container_width=True)

# Main content
if simular_btn or 'resultados' in st.session_state:

    # Preparar parámetros
    parametros = {
        'edad_actual': edad_actual,
        'edad_jubilacion': edad_jubilacion,
        'esperanza_vida': esperanza_vida,
        'ingreso_mensual': ingreso_mensual,
        'aumento_salarial_anual': aumento_salarial,
        'cotizacion_obligatoria': cotizacion_obligatoria,
        'comision_afp': comision_afp,
        'aporte_empleador': aporte_empleador,
        'cotizacion_voluntaria': cotizacion_voluntaria,
        'rentabilidad_nominal': rentabilidad_nominal,
        'inflacion_esperada': inflacion_esperada,
        'anos_lagunas': anos_lagunas,
        'distribucion_lagunas': distribucion_lagunas,
        'valor_uf': datos_actualizados['uf']
    }

    # Validar parámetros
    valido, mensaje_error = validar_simulacion_completa(parametros)

    if not valido:
        st.error(f"❌ Error en los parámetros: {mensaje_error}")
    else:
        # Calcular con spinner
        with st.spinner("🔄 Calculando tu pensión..."):
            resultados = calculator.calcular_pension_completa(**parametros)

            # Guardar en session state
            st.session_state['resultados'] = resultados
            st.session_state['parametros'] = parametros

        # Mostrar resultados
        st.success("✅ Simulación completada")

        # Métricas principales
        st.subheader("📊 Resultados Principales")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Saldo Final</div>
                <div class="metric-value">{formato_clp(resultados['saldo_final_nominal'])}</div>
                <div class="metric-label">{formato_uf(resultados['saldo_final_nominal'] / datos_actualizados['uf'])}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Pensión Mensual (RP)</div>
                <div class="metric-value">{formato_clp(resultados['pension_rp_nominal'])}</div>
                <div class="metric-label">Retiro Programado</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Tasa de Reemplazo</div>
                <div class="metric-value">{formato_porcentaje(resultados['tasa_reemplazo_rp'])}</div>
                <div class="metric-label">Del último sueldo</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">TIR Cotizaciones</div>
                <div class="metric-value">{formato_porcentaje(resultados['tir_cotizaciones'])}</div>
                <div class="metric-label">Retorno Inversión</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Tabs con información detallada
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Gráficos", "💰 Modalidades", "📊 Métricas Avanzadas",
            "📋 Detalle Anual", "💾 Exportar"
        ])

        with tab1:
            st.subheader("Evolución del Ahorro")
            fig_evolucion = charts.grafico_evolucion_saldo(resultados['simulacion_anual'], mostrar_real=True)
            st.plotly_chart(fig_evolucion, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Composición del Saldo")
                fig_composicion = charts.grafico_composicion_saldo(resultados['simulacion_anual'])
                st.plotly_chart(fig_composicion, use_container_width=True)

            with col2:
                st.subheader("Flujo de Caja Anual")
                fig_flujo = charts.grafico_flujo_caja(resultados['simulacion_anual'])
                st.plotly_chart(fig_flujo, use_container_width=True)

        with tab2:
            st.subheader("Comparación de Modalidades de Pensión")

            col1, col2 = st.columns(2)

            with col1:
                fig_comparacion = charts.grafico_comparacion_modalidades(
                    resultados['pension_rp_nominal'],
                    resultados['pension_rv_nominal'],
                    datos_actualizados['pbs']
                )
                st.plotly_chart(fig_comparacion, use_container_width=True)

            with col2:
                st.markdown("### 📋 Detalle por Modalidad")

                st.info(f"""
                **Retiro Programado**
                - Pensión Mensual: {formato_clp(resultados['pension_rp_nominal'])}
                - Pensión Real (ajustada): {formato_clp(resultados['pension_rp_real'])}
                - Tasa Reemplazo: {formato_porcentaje(resultados['tasa_reemplazo_rp'])}
                - Flexibilidad: Alta
                - Riesgo: Tú asumes variabilidad
                """)

                st.success(f"""
                **Renta Vitalicia**
                - Pensión Mensual: {formato_clp(resultados['pension_rv_nominal'])}
                - Pensión Real (ajustada): {formato_clp(resultados['pension_rv_real'])}
                - Tasa Reemplazo: {formato_porcentaje(resultados['tasa_reemplazo_rv'])}
                - Flexibilidad: Baja (fija de por vida)
                - Riesgo: Aseguradora asume riesgo
                """)

                if resultados['pension_rp_nominal'] < datos_actualizados['pbs']:
                    st.warning(f"""
                    ⚠️ **Pensión Básica Solidaria**

                    Tu pensión estimada es menor a la PBS ({formato_clp(datos_actualizados['pbs'])}).
                    El Estado complementará hasta ese monto.
                    """)

        with tab3:
            st.subheader("Métricas Financieras Avanzadas")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Valor Presente Neto (VPN)",
                    formato_clp(resultados['vpn_cotizaciones']),
                    help="Valor presente de todas las cotizaciones"
                )

                st.metric(
                    "Tasa Interna de Retorno (TIR)",
                    formato_porcentaje(resultados['tir_cotizaciones']),
                    help="Rentabilidad efectiva de tus cotizaciones"
                )

                st.metric(
                    "Rentabilidad Real",
                    formato_porcentaje(resultados['rentabilidad_real']),
                    help="Rentabilidad ajustada por inflación"
                )

            with col2:
                st.metric(
                    "Valor Presente Total Pensión",
                    formato_clp(resultados['vp_pension_total']),
                    help="Valor actual de todas tus pensiones futuras"
                )

                st.metric(
                    "Último Sueldo Proyectado",
                    formato_clp(resultados['ultimo_sueldo']),
                    help="Tu sueldo al momento de jubilar"
                )

                st.metric(
                    "Años de Cotización Efectivos",
                    f"{resultados['anos_cotizacion'] - resultados['anos_lagunas_efectivos']} años",
                    f"-{resultados['anos_lagunas_efectivos']} lagunas" if resultados['anos_lagunas_efectivos'] > 0 else "Sin lagunas"
                )

            # Brecha previsional
            st.divider()
            st.subheader("📉 Análisis de Brecha Previsional")

            brecha = resultados['brecha_previsional']
            if brecha['hay_brecha']:
                st.warning(f"""
                ⚠️ **Existe una brecha previsional**

                Tu pensión estimada ({formato_clp(resultados['pension_rp_nominal'])}) es menor
                al objetivo del 70% del sueldo ({formato_clp(resultados['ultimo_sueldo'] * 0.7)}).

                **Para cerrar la brecha necesitas:**
                - Cotizar {formato_clp(brecha['brecha_mensual'])} adicional por mes
                - O acumular {formato_clp(brecha['ahorro_total_necesario'])} adicional
                """)
            else:
                st.success("""
                ✅ **¡Felicitaciones!**

                Tu pensión estimada alcanza o supera el objetivo del 70% del sueldo.
                """)

        with tab4:
            st.subheader("Simulación Año por Año")

            df_display = resultados['simulacion_anual'].copy()
            df_display['Año'] = df_display['ano']
            df_display['Edad'] = df_display['edad']
            df_display['Ingreso Mensual'] = df_display['ingreso_mensual'].apply(lambda x: formato_clp(x))
            df_display['Cotización Anual'] = df_display['cotizacion_anual'].apply(lambda x: formato_clp(x))
            df_display['Comisión AFP'] = df_display['comision_anual'].apply(lambda x: formato_clp(x))
            df_display['Rentabilidad'] = df_display['rentabilidad_nominal_anual'].apply(lambda x: formato_clp(x))
            df_display['Saldo Acumulado'] = df_display['saldo_nominal'].apply(lambda x: formato_clp(x))
            df_display['Laguna'] = df_display['tiene_laguna'].apply(lambda x: '❌' if x else '✅')

            st.dataframe(
                df_display[['Año', 'Edad', 'Ingreso Mensual', 'Cotización Anual',
                           'Comisión AFP', 'Rentabilidad', 'Saldo Acumulado', 'Laguna']],
                use_container_width=True,
                height=400
            )

            # Descargar como Excel
            @st.cache_data
            def convert_df_to_excel(df):
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False, sheet_name='Simulación')
                return output.getvalue()

            excel_data = convert_df_to_excel(resultados['simulacion_anual'])
            st.download_button(
                label="📥 Descargar Excel",
                data=excel_data,
                file_name=f"simulacion_pension_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        with tab5:
            st.subheader("💾 Exportar Resultados")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 📄 Reporte PDF")
                st.info("""
                Descarga un reporte profesional con:
                - Resumen ejecutivo
                - Gráficos y métricas
                - Análisis detallado
                - Disclaimers legales
                """)

                if st.button("Generar PDF", type="primary"):
                    with st.spinner("Generando reporte PDF..."):
                        pdf_buffer = pdf_generator.generar_reporte(resultados, parametros)
                        st.download_button(
                            label="📥 Descargar PDF",
                            data=pdf_buffer,
                            file_name=f"reporte_pension_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf"
                        )

            with col2:
                st.markdown("### 💾 Guardar Simulación")
                st.info("""
                Guarda tus parámetros y resultados
                en formato JSON para cargarlos después.
                """)

                simulacion_data = {
                    'parametros': parametros,
                    'fecha': datetime.now().isoformat(),
                    'resumen': {
                        'saldo_final': resultados['saldo_final_nominal'],
                        'pension_rp': resultados['pension_rp_nominal'],
                        'tasa_reemplazo': resultados['tasa_reemplazo_rp']
                    }
                }

                json_data = json.dumps(simulacion_data, indent=2, default=str)
                st.download_button(
                    label="📥 Descargar JSON",
                    data=json_data,
                    file_name=f"simulacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

else:
    # Mensaje inicial
    st.info("""
    👈 **Configura los parámetros** en el panel lateral y presiona **"Calcular Pensión"**
    para ver tu proyección de pensión detallada.

    💡 Los valores por defecto están basados en datos reales actualizados de Chile.
    """)

    # Mostrar ejemplo de qué esperar
    st.markdown("### 📋 ¿Qué obtendrás?")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **Cálculos Detallados:**
        - Saldo final acumulado
        - Pensión mensual estimada
        - Tasa de reemplazo
        - TIR de inversión
        """)

    with col2:
        st.markdown("""
        **Visualizaciones:**
        - Evolución del ahorro
        - Comparación modalidades
        - Composición del saldo
        - Flujo de caja anual
        """)

    with col3:
        st.markdown("""
        **Análisis Avanzado:**
        - Valor presente neto
        - Rentabilidad real
        - Brecha previsional
        - Reportes exportables
        """)
