"""
Módulo de Visualizaciones Profesionales
Gráficos interactivos con Plotly para el simulador
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List


class PensionCharts:
    """Generador de gráficos profesionales para pensiones."""

    def __init__(self):
        """Inicializa con configuración de estilo profesional."""
        self.color_palette = {
            'primary': '#1E3A8A',      # Azul corporativo
            'secondary': '#3B82F6',    # Azul claro
            'success': '#10B981',      # Verde
            'warning': '#F59E0B',      # Amarillo
            'danger': '#EF4444',       # Rojo
            'info': '#06B6D4',         # Cyan
            'gray': '#6B7280',         # Gris
        }

        self.template = 'plotly_white'
        self.font_family = 'Arial, sans-serif'

    def grafico_evolucion_saldo(self, df_simulacion: pd.DataFrame, mostrar_real: bool = True) -> go.Figure:
        """
        Gráfico de evolución del saldo acumulado.

        Args:
            df_simulacion: DataFrame con la simulación anual
            mostrar_real: Si True, muestra saldo real ajustado por inflación

        Returns:
            Figura de Plotly
        """
        fig = go.Figure()

        # Saldo nominal
        fig.add_trace(go.Scatter(
            x=df_simulacion['edad'],
            y=df_simulacion['saldo_nominal'],
            name='Saldo Nominal',
            mode='lines+markers',
            line=dict(color=self.color_palette['primary'], width=3),
            marker=dict(size=6),
            hovertemplate='<b>Edad: %{x}</b><br>Saldo: $%{y:,.0f}<extra></extra>'
        ))

        # Saldo real (ajustado por inflación)
        if mostrar_real:
            fig.add_trace(go.Scatter(
                x=df_simulacion['edad'],
                y=df_simulacion['saldo_real'],
                name='Saldo Real (ajustado inflación)',
                mode='lines+markers',
                line=dict(color=self.color_palette['success'], width=3, dash='dot'),
                marker=dict(size=6),
                hovertemplate='<b>Edad: %{x}</b><br>Saldo Real: $%{y:,.0f}<extra></extra>'
            ))

        # Marcar períodos con lagunas
        lagunas = df_simulacion[df_simulacion['tiene_laguna'] == True]
        if not lagunas.empty:
            fig.add_trace(go.Scatter(
                x=lagunas['edad'],
                y=lagunas['saldo_nominal'],
                name='Años con Laguna',
                mode='markers',
                marker=dict(
                    size=12,
                    color=self.color_palette['danger'],
                    symbol='x',
                    line=dict(width=2)
                ),
                hovertemplate='<b>Laguna Previsional</b><br>Edad: %{x}<extra></extra>'
            ))

        fig.update_layout(
            title=dict(
                text='<b>Evolución del Ahorro Previsional</b>',
                font=dict(size=20, family=self.font_family)
            ),
            xaxis=dict(
                title='Edad',
                showgrid=True,
                gridcolor='#E5E7EB'
            ),
            yaxis=dict(
                title='Saldo Acumulado (CLP)',
                showgrid=True,
                gridcolor='#E5E7EB',
                tickformat='$,.0f'
            ),
            template=self.template,
            hovermode='x unified',
            font=dict(family=self.font_family),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            ),
            height=500
        )

        return fig

    def grafico_comparacion_modalidades(self, pension_rp: float, pension_rv: float,
                                       pension_pbs: float = 0) -> go.Figure:
        """
        Gráfico comparativo de modalidades de pensión.

        Args:
            pension_rp: Pensión Retiro Programado
            pension_rv: Pensión Renta Vitalicia
            pension_pbs: Pensión Básica Solidaria

        Returns:
            Figura de Plotly
        """
        modalidades = ['Retiro<br>Programado', 'Renta<br>Vitalicia']
        valores = [pension_rp, pension_rv]
        colores = [self.color_palette['primary'], self.color_palette['success']]

        if pension_pbs > 0:
            modalidades.append('Pensión Básica<br>Solidaria')
            valores.append(pension_pbs)
            colores.append(self.color_palette['warning'])

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=modalidades,
            y=valores,
            marker=dict(
                color=colores,
                line=dict(color='white', width=2)
            ),
            text=[f'${v:,.0f}' for v in valores],
            textposition='outside',
            textfont=dict(size=14, family=self.font_family, color='#1E293B'),
            hovertemplate='<b>%{x}</b><br>Pensión: $%{y:,.0f}<extra></extra>'
        ))

        fig.update_layout(
            title=dict(
                text='<b>Comparación de Modalidades de Pensión</b>',
                font=dict(size=20, family=self.font_family)
            ),
            yaxis=dict(
                title='Pensión Mensual (CLP)',
                showgrid=True,
                gridcolor='#E5E7EB',
                tickformat='$,.0f'
            ),
            template=self.template,
            font=dict(family=self.font_family),
            height=450,
            showlegend=False
        )

        return fig

    def grafico_composicion_saldo(self, df_simulacion: pd.DataFrame) -> go.Figure:
        """
        Gráfico de composición del saldo (cotizaciones vs rentabilidad).

        Args:
            df_simulacion: DataFrame con simulación

        Returns:
            Figura de Plotly
        """
        # Calcular totales
        total_cotizaciones = df_simulacion['cotizacion_neta_anual'].sum()
        total_comisiones = df_simulacion['comision_anual'].sum()
        total_rentabilidad = df_simulacion['rentabilidad_nominal_anual'].sum()
        saldo_final = df_simulacion['saldo_nominal'].iloc[-1]

        labels = ['Cotizaciones Netas', 'Rentabilidad Generada', 'Comisiones AFP']
        values = [total_cotizaciones, total_rentabilidad, total_comisiones]
        colors = [self.color_palette['primary'], self.color_palette['success'],
                 self.color_palette['danger']]

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            hole=0.4,
            textinfo='label+percent',
            textfont=dict(size=13, family=self.font_family),
            hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>'
        )])

        fig.update_layout(
            title=dict(
                text='<b>Composición del Saldo Final</b>',
                font=dict(size=20, family=self.font_family)
            ),
            annotations=[dict(
                text=f'<b>Total</b><br>${saldo_final:,.0f}',
                x=0.5, y=0.5,
                font=dict(size=16, family=self.font_family),
                showarrow=False
            )],
            template=self.template,
            font=dict(family=self.font_family),
            height=450
        )

        return fig

    def grafico_monte_carlo(self, resultados_mc: Dict) -> go.Figure:
        """
        Gráfico de distribución Monte Carlo.

        Args:
            resultados_mc: Resultados de simulación Monte Carlo

        Returns:
            Figura de Plotly
        """
        pension_dist = resultados_mc['distribucion_completa']['pension_rp']

        fig = go.Figure()

        # Histograma
        fig.add_trace(go.Histogram(
            x=pension_dist,
            nbinsx=50,
            name='Distribución',
            marker=dict(
                color=self.color_palette['primary'],
                line=dict(color='white', width=1)
            ),
            opacity=0.7,
            hovertemplate='Pensión: $%{x:,.0f}<br>Frecuencia: %{y}<extra></extra>'
        ))

        # Líneas de percentiles
        percentiles = [
            (resultados_mc['pension_rp']['percentil_10'], 'P10 (Pesimista)', self.color_palette['danger']),
            (resultados_mc['pension_rp']['mediana'], 'Mediana', self.color_palette['success']),
            (resultados_mc['pension_rp']['percentil_90'], 'P90 (Optimista)', self.color_palette['info'])
        ]

        for valor, nombre, color in percentiles:
            fig.add_vline(
                x=valor,
                line_dash='dash',
                line_color=color,
                line_width=2,
                annotation_text=f'{nombre}<br>${valor:,.0f}',
                annotation_position='top'
            )

        fig.update_layout(
            title=dict(
                text='<b>Análisis de Riesgo - Simulación Monte Carlo</b><br>'
                     f'<sub>{resultados_mc["n_simulaciones"]:,} simulaciones</sub>',
                font=dict(size=20, family=self.font_family)
            ),
            xaxis=dict(
                title='Pensión Mensual (CLP)',
                tickformat='$,.0f'
            ),
            yaxis=dict(
                title='Frecuencia'
            ),
            template=self.template,
            font=dict(family=self.font_family),
            height=500,
            showlegend=False
        )

        return fig

    def grafico_sensibilidad(self, df_sensibilidad: pd.DataFrame, parametro: str) -> go.Figure:
        """
        Gráfico de análisis de sensibilidad.

        Args:
            df_sensibilidad: DataFrame con resultados de sensibilidad
            parametro: Nombre del parámetro analizado

        Returns:
            Figura de Plotly
        """
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Impacto en Pensión', 'Impacto en Tasa de Reemplazo'),
            vertical_spacing=0.15
        )

        # Gráfico 1: Pensión
        fig.add_trace(
            go.Scatter(
                x=df_sensibilidad['valor_parametro'],
                y=df_sensibilidad['pension_rp'],
                mode='lines+markers',
                name='Retiro Programado',
                line=dict(color=self.color_palette['primary'], width=3),
                marker=dict(size=8),
                hovertemplate='%{x}<br>Pensión: $%{y:,.0f}<extra></extra>'
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df_sensibilidad['valor_parametro'],
                y=df_sensibilidad['pension_rv'],
                mode='lines+markers',
                name='Renta Vitalicia',
                line=dict(color=self.color_palette['success'], width=3),
                marker=dict(size=8),
                hovertemplate='%{x}<br>Pensión: $%{y:,.0f}<extra></extra>'
            ),
            row=1, col=1
        )

        # Gráfico 2: Tasa de Reemplazo
        fig.add_trace(
            go.Scatter(
                x=df_sensibilidad['valor_parametro'],
                y=df_sensibilidad['tasa_reemplazo'],
                mode='lines+markers',
                name='Tasa Reemplazo',
                line=dict(color=self.color_palette['info'], width=3),
                marker=dict(size=8),
                fill='tozeroy',
                fillcolor='rgba(6, 182, 212, 0.1)',
                hovertemplate='%{x}<br>Tasa: %{y:.1f}%<extra></extra>'
            ),
            row=2, col=1
        )

        fig.update_xaxes(title_text=parametro.replace('_', ' ').title(), row=2, col=1)
        fig.update_yaxes(title_text='Pensión (CLP)', tickformat='$,.0f', row=1, col=1)
        fig.update_yaxes(title_text='Tasa Reemplazo (%)', row=2, col=1)

        fig.update_layout(
            title=dict(
                text=f'<b>Análisis de Sensibilidad: {parametro.replace("_", " ").title()}</b>',
                font=dict(size=20, family=self.font_family)
            ),
            template=self.template,
            font=dict(family=self.font_family),
            height=700,
            hovermode='x unified'
        )

        return fig

    def grafico_comparador_escenarios(self, df_comparacion: pd.DataFrame) -> go.Figure:
        """
        Gráfico comparador de múltiples escenarios.

        Args:
            df_comparacion: DataFrame con comparación de escenarios

        Returns:
            Figura de Plotly
        """
        fig = go.Figure()

        # Pensión RP
        fig.add_trace(go.Bar(
            name='Retiro Programado',
            x=df_comparacion['escenario'],
            y=df_comparacion['pension_rp'],
            marker=dict(color=self.color_palette['primary']),
            text=[f'${v:,.0f}' for v in df_comparacion['pension_rp']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>RP: $%{y:,.0f}<extra></extra>'
        ))

        # Pensión RV
        fig.add_trace(go.Bar(
            name='Renta Vitalicia',
            x=df_comparacion['escenario'],
            y=df_comparacion['pension_rv'],
            marker=dict(color=self.color_palette['success']),
            text=[f'${v:,.0f}' for v in df_comparacion['pension_rv']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>RV: $%{y:,.0f}<extra></extra>'
        ))

        fig.update_layout(
            title=dict(
                text='<b>Comparación de Escenarios</b>',
                font=dict(size=20, family=self.font_family)
            ),
            xaxis=dict(title='Escenario'),
            yaxis=dict(
                title='Pensión Mensual (CLP)',
                tickformat='$,.0f'
            ),
            template=self.template,
            font=dict(family=self.font_family),
            barmode='group',
            height=500,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )

        return fig

    def grafico_flujo_caja(self, df_simulacion: pd.DataFrame) -> go.Figure:
        """
        Gráfico de flujo de caja año por año.

        Args:
            df_simulacion: DataFrame con simulación

        Returns:
            Figura de Plotly
        """
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=df_simulacion['edad'],
            y=df_simulacion['cotizacion_neta_anual'],
            name='Cotizaciones Netas',
            marker=dict(color=self.color_palette['success']),
            hovertemplate='Edad: %{x}<br>Cotización: $%{y:,.0f}<extra></extra>'
        ))

        fig.add_trace(go.Bar(
            x=df_simulacion['edad'],
            y=-df_simulacion['comision_anual'],
            name='Comisiones AFP',
            marker=dict(color=self.color_palette['danger']),
            hovertemplate='Edad: %{x}<br>Comisión: $%{y:,.0f}<extra></extra>'
        ))

        fig.add_trace(go.Scatter(
            x=df_simulacion['edad'],
            y=df_simulacion['rentabilidad_nominal_anual'],
            name='Rentabilidad',
            mode='lines+markers',
            line=dict(color=self.color_palette['primary'], width=3),
            marker=dict(size=6),
            yaxis='y2',
            hovertemplate='Edad: %{x}<br>Rentabilidad: $%{y:,.0f}<extra></extra>'
        ))

        fig.update_layout(
            title=dict(
                text='<b>Flujo de Caja Previsional Anual</b>',
                font=dict(size=20, family=self.font_family)
            ),
            xaxis=dict(title='Edad'),
            yaxis=dict(
                title='Cotizaciones y Comisiones (CLP)',
                tickformat='$,.0f'
            ),
            yaxis2=dict(
                title='Rentabilidad (CLP)',
                overlaying='y',
                side='right',
                tickformat='$,.0f'
            ),
            template=self.template,
            font=dict(family=self.font_family),
            barmode='relative',
            height=500,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )

        return fig
