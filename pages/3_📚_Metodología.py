"""
Metodología y Documentación
Explicación transparente de los cálculos
"""

import streamlit as st

st.set_page_config(
    page_title="Metodología",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Metodología y Transparencia")
st.markdown("Conoce cómo funcionan los cálculos de este simulador")

# Introducción
st.info("""
Este simulador utiliza **métodos financieros profesionales** para estimar tu pensión futura.
Todos los cálculos son transparentes y están basados en fórmulas estándar de finanzas.
""")

# Tabs de contenido
tab1, tab2, tab3, tab4 = st.tabs(["💡 Conceptos Básicos", "🧮 Fórmulas", "📊 Datos Utilizados", "⚖️ Legal"])

with tab1:
    st.subheader("Conceptos Básicos del Sistema de Pensiones Chileno")

    with st.expander("🏦 ¿Cómo funciona el sistema de AFP?"):
        st.markdown("""
        El sistema de **pensiones chileno** es de **capitalización individual**:

        1. **Cotizas el 10%** de tu sueldo mensualmente (obligatorio)
        2. La **AFP administra** tu dinero e invierte en fondos
        3. Se cobra una **comisión** mensual (varía por AFP, ~0.5% a 1.5%)
        4. Tu dinero genera **rentabilidad** según el tipo de fondo
        5. Al jubilar, usas el **saldo acumulado** para financiar tu pensión

        **Tipos de Fondo:**
        - **Fondo A**: Mayor riesgo/retorno (hasta 80% acciones)
        - **Fondo B**: Alto riesgo (45-80% acciones)
        - **Fondo C**: Balanceado (15-45% acciones)
        - **Fondo D**: Conservador (0-20% acciones)
        - **Fondo E**: Muy conservador (sin acciones)
        """)

    with st.expander("💰 Modalidades de Pensión"):
        st.markdown("""
        Al jubilar puedes elegir:

        **1. Retiro Programado (RP)**
        - Calculas: Saldo ÷ (Años de vida × 12 meses)
        - El dinero sigue en tu cuenta
        - Pensión variable (depende de rentabilidad)
        - Flexibilidad alta
        - Riesgo: lo asumes tú

        **2. Renta Vitalicia (RV)**
        - Transfieres tu saldo a una aseguradora
        - Recibes pensión fija de por vida
        - Típicamente ~92% del RP inicial
        - Sin flexibilidad
        - Riesgo: lo asume la aseguradora

        **3. Pensión Básica Solidaria (PBS)**
        - Si tu pensión < PBS (~$214.000 en 2024)
        - El Estado complementa hasta ese monto
        - Para personas con bajo saldo acumulado
        """)

    with st.expander("📈 Rentabilidad e Inflación"):
        st.markdown("""
        **Rentabilidad Nominal vs Real:**

        - **Nominal**: Lo que ves en los estados de cuenta (ej: 6% anual)
        - **Real**: Ajustada por inflación (poder adquisitivo real)

        **Fórmula Fisher:**
        ```
        Rentabilidad Real = (1 + Rent. Nominal) / (1 + Inflación) - 1
        ```

        **Ejemplo:**
        - Rentabilidad nominal: 6%
        - Inflación: 3%
        - Rentabilidad real: (1.06 / 1.03) - 1 = 2.9%

        **Importancia:** El poder adquisitivo es lo que realmente importa.
        """)

with tab2:
    st.subheader("🧮 Fórmulas Utilizadas")

    with st.expander("1️⃣ Cálculo del Saldo Acumulado"):
        st.markdown("""
        El saldo se calcula **año por año**:

        ```
        Para cada año t:
        1. Cotización_t = Sueldo_t × 10% (+ voluntaria + empleador)
        2. Comisión_t = Sueldo_t × Comisión_AFP
        3. Cotización_Neta_t = Cotización_t - Comisión_t
        4. Rentabilidad_t = Saldo_(t-1) × Rentabilidad_Anual
        5. Saldo_t = Saldo_(t-1) + Rentabilidad_t + Cotización_Neta_t
        ```

        **Consideraciones:**
        - Si hay laguna en año t, Cotización_t = 0
        - El sueldo aumenta cada año según % configurado
        - Se aplica tope imponible (84.7 UF)
        """)

    with st.expander("2️⃣ Valor Presente Neto (VPN)"):
        st.markdown("""
        Calcula el valor actual de las cotizaciones futuras:

        ```
        VPN = Σ [Cotización_t / (1 + tasa_descuento)^t]
        ```

        - Tasa de descuento = Rentabilidad real
        - Permite comparar flujos en diferentes momentos
        - Útil para evaluar si "vale la pena" cotizar más
        """)

    with st.expander("3️⃣ Tasa Interna de Retorno (TIR)"):
        st.markdown("""
        Rentabilidad efectiva de tus cotizaciones:

        ```
        Encuentra TIR donde:
        0 = Σ [Cotización_t / (1 + TIR)^t] - Saldo_Final
        ```

        - Se resuelve numéricamente (método Newton-Raphson)
        - Compara con rentabilidades de inversiones alternativas
        - TIR > Rentabilidad AFP = estás ganando por interés compuesto
        """)

    with st.expander("4️⃣ Pensión Mensual"):
        st.markdown("""
        **Retiro Programado:**
        ```
        Pensión_RP = Saldo_Final / (Años_Pensión × 12)
        ```

        **Renta Vitalicia:**
        ```
        Pensión_RV = Pensión_RP × Factor_RV
        ```
        - Factor_RV típicamente 0.92 (92%)
        - Depende de edad, género, aseguradora
        """)

    with st.expander("5️⃣ Tasa de Reemplazo"):
        st.markdown("""
        Porcentaje del último sueldo que recibirás:

        **Nominal:**
        ```
        Tasa_Reemplazo = (Pensión_Mensual / Último_Sueldo) × 100
        ```

        **Real (ajustada por inflación):**
        ```
        Tasa_Reemplazo_Real = (Pensión_Real / Sueldo_Real) × 100
        ```

        - Meta OCDE: 70% del último sueldo
        - Chile promedio: 30-40%
        """)

with tab3:
    st.subheader("📊 Fuentes de Datos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **🏦 Banco Central de Chile**
        - Valor UF actualizado
        - Indicadores económicos
        - API: mindicador.cl

        **📈 Superintendencia de Pensiones**
        - Rentabilidades históricas AFPs
        - Comisiones por fondo
        - Estadísticas del sistema

        **📊 Comisión para el Mercado Financiero (CMF)**
        - Datos de AFPs
        - Regulaciones
        - Información pública
        """)

    with col2:
        st.markdown("""
        **📉 Instituto Nacional de Estadísticas (INE)**
        - Inflación histórica y proyectada
        - IPC (Índice de Precios al Consumidor)
        - Salarios promedio

        **💼 Datos Internos**
        - Parámetros configurables
        - Valores por defecto basados en promedios
        - Actualizaciones periódicas
        """)

    st.info("""
    **Frecuencia de Actualización:**
    - UF: Diaria (vía API)
    - Comisiones AFP: Mensual (actualización manual)
    - Inflación: Mensual (INE)
    - Rentabilidades: Mensual (SP Pensiones)
    """)

with tab4:
    st.subheader("⚖️ Avisos Legales y Limitaciones")

    st.warning("""
    ### ⚠️ DISCLAIMER LEGAL - LEER CUIDADOSAMENTE

    **Este simulador NO constituye:**
    - Asesoría financiera profesional
    - Recomendación de inversión
    - Garantía de resultados futuros
    - Producto regulado por la CMF

    **Es una herramienta educativa** para fines informativos.
    """)

    with st.expander("🔒 Limitaciones del Modelo"):
        st.markdown("""
        **Este simulador NO considera:**

        1. **Cambios legislativos** futuros en el sistema de pensiones
        2. **Crisis económicas** o eventos extremos
        3. **Cambios en comisiones** AFP durante el período
        4. **Impuestos** sobre retiros o pensiones
        5. **Bonos gubernamentales** específicos
        6. **Herencias** o traspasos de saldo
        7. **Pensiones de sobrevivencia**
        8. **APV con beneficios tributarios** (simplificado)
        9. **Multifondos** dinámicos (asume fondo fijo)
        10. **Seguros de invalidez** o sobrevivencia

        **Supuestos Simplificadores:**
        - Rentabilidad constante (en realidad varía año a año)
        - Inflación constante (en realidad fluctúa)
        - Aumentos salariales lineales
        - No considera cambios de AFP
        - No considera retiros del 10%/PGU
        """)

    with st.expander("📜 Términos de Uso"):
        st.markdown("""
        **Al usar este simulador aceptas:**

        1. Los resultados son **estimaciones** y **no garantías**
        2. La rentabilidad pasada **no garantiza** rentabilidad futura
        3. Debes **validar** los resultados con un profesional certificado
        4. El desarrollador **no se hace responsable** de decisiones tomadas basadas en este simulador
        5. Los datos se obtienen de fuentes públicas pero pueden contener errores
        6. Este es un proyecto **educativo** y **gratuito**

        **Recomendaciones:**
        - Consulta con un **asesor previsional** certificado
        - Revisa tu **estado de cuenta AFP** real
        - Considera escenarios **pesimistas** al planificar
        - Diversifica tus **ahorros** para la vejez
        - Mantente informado sobre **reformas** al sistema
        """)

    with st.expander("🔐 Privacidad de Datos"):
        st.markdown("""
        **Política de Privacidad:**

        - **No se almacenan** datos personales en servidores
        - Todo se ejecuta en tu navegador (**client-side**)
        - **No hay tracking** de información sensible
        - Los datos que ingreses son **privados**
        - Al exportar, los datos quedan en **tu dispositivo**

        **Opcional:**
        - Si guardas simulaciones en JSON, son solo tuyas
        - No se comparten con terceros
        - No hay base de datos centralizada
        """)

    st.success("""
    ✅ **Uso Responsable:**

    Este simulador está diseñado para **educarte** sobre el sistema de pensiones
    y ayudarte a tomar **decisiones informadas**. Úsalo como punto de partida,
    no como única fuente de información.
    """)

# Footer
st.divider()
st.markdown("""
### 📧 Contacto y Contribuciones

¿Encontraste un error? ¿Tienes sugerencias?

Este es un proyecto open source. Las contribuciones son bienvenidas.

**Desarrollado con:** Python • Streamlit • NumPy • Pandas • SciPy • Plotly • ReportLab
""")
