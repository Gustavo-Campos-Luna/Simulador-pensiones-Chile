"""
Metodologia y transparencia — Documentacion tecnica del simulador.

Describe las formulas implementadas, los supuestos del modelo, las
fuentes de datos utilizadas y los avisos legales correspondientes.
"""

import streamlit as st

st.set_page_config(
    page_title="Metodologia",
    page_icon=None,
    layout="wide",
)

st.title("Metodologia")
st.caption("Descripcion tecnica de formulas, supuestos y fuentes de datos")

tab_sistema, tab_formulas, tab_datos, tab_legal = st.tabs([
    "Sistema AFP", "Formulas", "Datos y supuestos", "Aviso legal",
])

# ---------------------------------------------------------------------------
# Tab 1: Sistema AFP
# ---------------------------------------------------------------------------
with tab_sistema:
    st.subheader("Sistema de capitalizacion individual — AFP Chile")

    with st.expander("Estructura del sistema previsional"):
        st.markdown("""
        El sistema previsional chileno, establecido por el Decreto Ley 3.500 de 1980,
        opera bajo el principio de **capitalizacion individual**: cada trabajador
        acumula sus propios ahorros en una cuenta gestionada por una
        Administradora de Fondos de Pensiones (AFP).

        **Flujo de aportes:**
        1. El trabajador cotiza el 10 % de su remuneracion imponible mensualmente.
        2. La AFP administra el fondo e invierte en renta fija y variable segun el tipo de fondo.
        3. La AFP cobra una comision sobre la remuneracion imponible (entre 0,49 % y 1,45 %).
        4. El saldo acumula rendimientos compuestos durante el periodo de acumulacion.
        5. Al jubilar, el saldo se utiliza para financiar la pension bajo una modalidad elegida.

        **Tipos de fondo:**

        | Fondo | Perfil | Renta variable max | Rentabilidad historica (10 anos) |
        |---|---|---|---|
        | A | Agresivo | 80 % | 6,8 % aprox. |
        | B | Alto riesgo | 60 % | 6,2 % aprox. |
        | C | Balanceado | 40 % | 5,5 % aprox. |
        | D | Conservador | 15 % | 4,8 % aprox. |
        | E | Muy conservador | 0 % | 3,2 % aprox. |

        Fuente: Superintendencia de Pensiones (datos promedio historico 2014-2024).
        """)

    with st.expander("Modalidades de pension al jubilarse"):
        st.markdown("""
        Al alcanzar la edad legal (65 anos hombres / 60 anos mujeres), el cotizante
        puede elegir entre:

        **Retiro Programado (RP)**
        - El saldo permanece en la AFP y se retira mensualmente.
        - La pension se recalcula periodicamente segun saldo remanente y tablas de mortalidad.
        - El titular conserva el remanente como herencia.
        - Riesgo de longevidad asumido por el cotizante.

        **Renta Vitalicia (RV)**
        - Se transfiere el saldo a una compania de seguros a cambio de una renta mensual fija.
        - La aseguradora garantiza el pago de por vida, independientemente de cuanto se viva.
        - Se pierde el capital residual (no hay herencia del saldo transferido).
        - Riesgo de longevidad asumido por la aseguradora.

        **Pension Basica Solidaria (PBS) — Pilar solidario estatal**
        - Si la pension calculada es inferior a la PBS (CLP 214.296 en 2024), el Estado
          puede complementar hasta dicho monto segun la Ley 20.255 (Reforma Previsional 2008).
        """)

    with st.expander("Ahorro Previsional Voluntario (APV)"):
        st.markdown("""
        El APV permite ahorrar adicionalmente con beneficio tributario. Existen dos regimenes:

        **Regimen A — Subsidio directo**
        - El Fisco deposita el 15 % del aporte directamente en la cuenta, con tope de 6 UTM anuales.
        - Los retiros tributan con una tasa unica del 43 %.
        - Conveniente para cotizantes con tasa marginal inferior al 15 %.

        **Regimen B — Deduccion de base imponible**
        - Los aportes se descuentan de la base imponible del Impuesto Global Complementario.
        - El ahorro tributario equivale a: monto x tasa marginal del cotizante.
        - Los retiros tributan como renta ordinaria.
        - Conveniente para cotizantes con tasa marginal superior al 15 %.

        El tope anual en ambos regimenes es 600 UF (articulo 20 de la Ley 19.728).
        """)

# ---------------------------------------------------------------------------
# Tab 2: Formulas
# ---------------------------------------------------------------------------
with tab_formulas:
    st.subheader("Formulas implementadas")

    with st.expander("Acumulacion del saldo"):
        st.markdown("""
        La evolucion del saldo se calcula año a año mediante capitalizacion compuesta:

        ```
        Saldo_t = Saldo_{t-1} x (1 + r_nominal) + Cotizacion_neta_t

        Cotizacion_neta_t = Ingreso_imponible_t x (cot_obligatoria + cot_voluntaria + emp_contrib - comision) x 12

        Ingreso_imponible_t = min(Ingreso_t, Tope_imponible)

        Ingreso_t = Ingreso_0 x (1 + aumento_salarial)^t
        ```

        Si el ano t tiene laguna previsional, Cotizacion_neta_t = 0.

        **Saldo real (pesos constantes del año 0):**
        ```
        Saldo_real_t = Saldo_nominal_t / (1 + inflacion)^t
        ```
        Este enfoque deflacta el saldo nominal en lugar de aplicar
        rentabilidad real sobre flujos nominales, lo cual es conceptualmente correcto.
        """)

    with st.expander("Pension bajo Retiro Programado — Formula de anualidad"):
        st.markdown("""
        La pension mensual se calcula con la formula estandar de anualidad de valor presente:

        ```
        PMT = PV x r_m / (1 - (1 + r_m)^(-n))
        ```

        Donde:
        - PV = saldo acumulado al momento de jubilar
        - r_m = tasa mensual equivalente de la tasa de retiro (3 % anual por defecto)
        - n = meses de pension = (esperanza_vida - edad_jubilacion) x 12

        Esta formula es mas precisa que la division simple (que equivale a r_m = 0),
        ya que incorpora el valor temporal del dinero durante el periodo de retiro.

        **Renta Vitalicia:**
        ```
        Pension_RV = Pension_RP x Factor_RV
        Factor_RV = 0,92 (estimacion; depende de edad, genero y aseguradora)
        ```
        """)

    with st.expander("Rentabilidad real — Ecuacion de Fisher"):
        st.markdown("""
        ```
        r_real = (1 + r_nominal) / (1 + inflacion) - 1
        ```

        La ecuacion de Fisher es la expresion exacta de la relacion entre
        tasas reales y nominales. La aproximacion lineal (r_real = r_nom - inflacion)
        subestima la tasa real para valores altos.
        """)

    with st.expander("Valor Presente Neto (VPN) de cotizaciones"):
        st.markdown("""
        ```
        VPN = sum_{t=1}^{T} [Cotizacion_neta_t / (1 + r_real)^t]
        ```

        Representa el valor actual de todos los aportes futuros descontados
        a la tasa de rentabilidad real esperada del fondo.
        """)

    with st.expander("Tasa Interna de Retorno (TIR)"):
        st.markdown("""
        La TIR resuelve numericamente la ecuacion:

        ```
        0 = sum_{t=1}^{T} [Cotizacion_neta_t / (1 + TIR)^t] - Saldo_Final
        ```

        Se implementa con el metodo de Brent (convergencia garantizada en el intervalo
        [-50 %, 500 %]), con fallback a Newton-Raphson si no converge.
        La TIR representa la tasa de retorno efectiva de la inversion previsional.
        """)

    with st.expander("Duracion de Macaulay del pasivo previsional"):
        st.markdown("""
        ```
        D_Mac = sum_{m=1}^{n} [m x v(m)] / sum_{m=1}^{n} [v(m)]

        v(m) = 1 / (1 + r_m)^m
        ```

        La duracion de Macaulay mide el vencimiento promedio ponderado de
        los flujos de pension, expresado en anos. Es un indicador central de
        ALM (Asset-Liability Management): mide la sensibilidad del valor
        presente del pasivo a cambios en la tasa de descuento.
        """)

    with st.expander("DV01 del pasivo previsional"):
        st.markdown("""
        ```
        DV01 = |VP(r + 1bp) - VP(r)|
        ```

        El DV01 (Dollar Value of 1 basis point) indica el cambio en el valor
        presente de la corriente de pensiones ante un movimiento de 1 punto
        base (0,01 %) en la tasa de descuento. Expresado en CLP.
        """)

    with st.expander("Valor presente de la corriente de pensiones"):
        st.markdown("""
        ```
        VP_pension = sum_{m=1}^{n*12} [Pension_m x (1 + inflacion)^(m/12)] / (1 + r_real)^(m/12)
        ```

        Calcula el valor actual de todos los pagos de pension futuros, ajustados
        por inflacion y descontados a la tasa real de retiro.
        """)

    with st.expander("Simulacion Monte Carlo — metodologia"):
        st.markdown("""
        La implementacion vectorizada genera matrices de dimension (n_sim x n_anos):

        **Variables estocasticas por año:**
        - Rentabilidad nominal ~ N(mu_r, sigma_r^2), truncada en -20 %
        - Inflacion ~ N(mu_i, sigma_i^2), truncada en 0 %
        - Cesantia ~ Bernoulli(p_desempleo) por año

        **Calculo vectorizado del saldo final:**
        ```
        G_t = prod_{s=0}^{t} (1 + r_s)       (factor de crecimiento acumulado)
        B_n = G_n x sum_{t=0}^{n-1} [C_t / G_t]
        ```

        Esta formulacion evita el bucle Python por escenario, reduciendo el
        tiempo de computo de O(n_sim x n_anos x overhead_Python) a
        operaciones vectoriales numpy de O(n_sim x n_anos).
        """)

# ---------------------------------------------------------------------------
# Tab 3: Datos
# ---------------------------------------------------------------------------
with tab_datos:
    st.subheader("Fuentes de datos y supuestos")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Banco Central de Chile**
        - Valor diario de la UF (via API mindicador.cl)
        - Series de inflacion historica

        **Superintendencia de Pensiones**
        - Rentabilidades historicas por tipo de fondo
        - Comisiones vigentes de las AFP
        - Estadisticas del sistema previsional

        **Comision para el Mercado Financiero (CMF)**
        - Datos regulatorios de AFP e industria aseguradora
        """)
    with col2:
        st.markdown("""
        **Instituto Nacional de Estadisticas (INE)**
        - IPC mensual y anual
        - Indices de remuneraciones

        **Tablas de mortalidad**
        - RV-2014 (SP Pensiones) para calculo de esperanza de vida referencial

        **Parametros fijos (actualizacion manual)**
        - PBS vigente (Decreto Supremo)
        - Tope imponible (84,7 UF segun Ley 19.728)
        - Sueldo minimo
        """)

    st.divider()
    st.markdown("#### Supuestos del modelo")
    st.markdown("""
    | Supuesto | Descripcion |
    |---|---|
    | Rentabilidad constante | Se asume la misma tasa nominal cada año (correctable via Monte Carlo) |
    | Inflacion constante | Se asume la misma tasa de inflacion cada año |
    | Fondo unico | No se modela el cambio de fondo durante la vida laboral |
    | Factor RV fijo | La conversion RP/RV se estima en 92 %; en la practica depende de tablas actuariales |
    | Tasa de retiro | Se usa 3 % anual como tasa de descuento durante el periodo de pension |
    | Sin retiros excepcionales | No se modelan los retiros del 10 % autorizados en 2020-2021 |
    | Sin impuestos | No se consideran impuestos sobre pensiones o retiros (excepto APV) |
    | Sin herencia | No se modela la transferencia del saldo residual |
    | Sin seguros | No se consideran seguros de invalidez ni sobrevivencia |
    | Aumentos salariales lineales | El crecimiento salarial es constante cada año |
    """)

# ---------------------------------------------------------------------------
# Tab 4: Legal
# ---------------------------------------------------------------------------
with tab_legal:
    st.subheader("Aviso legal y terminos de uso")

    st.warning(
        "**Esta herramienta tiene caracter exclusivamente educativo e informativo.**\n\n"
        "Los resultados son estimaciones basadas en supuestos simplificadores y "
        "no constituyen asesoria financiera, previsional ni recomendacion de inversion. "
        "Esta herramienta no se encuentra registrada ni regulada por la CMF."
    )

    with st.expander("Limitaciones del modelo"):
        st.markdown("""
        El simulador **no considera**:

        1. Cambios legislativos futuros en el sistema de pensiones
        2. Rentabilidades variables año a año (excepto en el modulo Monte Carlo)
        3. Crisis economicas, eventos de tail risk o ciclos de mercado
        4. Cambios de AFP o de tipo de fondo durante la vida laboral
        5. Retiros excepcionales autorizados por legislacion extraordinaria
        6. Impuesto a las herencias sobre saldo residual
        7. Pensiones de sobrevivencia o invalidez
        8. Efectos de la reforma previsional en tramite legislativo (2024)
        9. Multifondos dinamicos o estrategias de ciclo de vida
        10. Comisiones fijas distintas de la comision porcentual sobre remuneracion
        """)

    with st.expander("Terminos de uso"):
        st.markdown("""
        Al utilizar esta herramienta, el usuario acepta que:

        - Los resultados son proyecciones, no garantias.
        - La rentabilidad pasada no garantiza rentabilidad futura.
        - Se recomienda complementar el analisis con un asesor previsional certificado.
        - El desarrollador no asume responsabilidad por decisiones financieras
          tomadas con base en los resultados de este simulador.
        - Los datos obtenidos de APIs publicas pueden contener errores o retrasos.
        """)

    with st.expander("Privacidad de datos"):
        st.markdown("""
        - No se almacenan datos personales en servidores externos.
        - La aplicacion se ejecuta completamente en el entorno del servidor Streamlit.
        - Los datos ingresados no se comparten con terceros.
        - Las exportaciones (PDF, Excel, JSON) se generan localmente y quedan en el dispositivo del usuario.
        """)

    st.divider()
    st.markdown("""
    **Desarrollado con:** Python 3.11, Streamlit, NumPy, SciPy, Pandas, Plotly, ReportLab

    **Fuentes normativas:** Decreto Ley 3.500 (1980), Ley 19.728 (2001),
    Ley 20.255 (2008 — Reforma Previsional), Ley 21.563 (2024 — PGU).
    """)
