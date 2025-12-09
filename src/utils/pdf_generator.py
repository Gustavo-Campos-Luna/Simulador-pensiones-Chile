"""
Generador de Reportes PDF Profesionales
Crea reportes detallados de simulaciones de pensión
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime
from typing import Dict
import pandas as pd


class PDFReportGenerator:
    """Generador de reportes PDF profesionales."""

    def __init__(self):
        """Inicializa el generador con estilos."""
        self.styles = getSampleStyleSheet()
        self._crear_estilos_personalizados()

    def _crear_estilos_personalizados(self):
        """Crea estilos personalizados para el PDF."""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1E3A8A'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1E3A8A'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))

        # Texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))

        # Disclaimer
        self.styles.add(ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_JUSTIFY,
            leftIndent=20,
            rightIndent=20
        ))

    def generar_reporte(self, resultados: Dict, parametros: Dict) -> BytesIO:
        """
        Genera un reporte PDF completo.

        Args:
            resultados: Resultados de la simulación
            parametros: Parámetros usados en la simulación

        Returns:
            BytesIO con el PDF generado
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)

        # Contenido del reporte
        story = []

        # Encabezado
        story.extend(self._crear_encabezado())

        # Resumen ejecutivo
        story.extend(self._crear_resumen_ejecutivo(resultados, parametros))

        # Resultados principales
        story.extend(self._crear_resultados_principales(resultados))

        # Métricas financieras
        story.extend(self._crear_metricas_financieras(resultados))

        # Tabla de simulación (primeros y últimos años)
        story.extend(self._crear_tabla_simulacion(resultados))

        # Disclaimers y notas legales
        story.append(PageBreak())
        story.extend(self._crear_disclaimers())

        # Generar PDF
        doc.build(story)
        buffer.seek(0)
        return buffer

    def _crear_encabezado(self) -> list:
        """Crea el encabezado del reporte."""
        elementos = []

        # Título
        titulo = Paragraph(
            "<b>Reporte de Simulación de Pensión</b>",
            self.styles['CustomTitle']
        )
        elementos.append(titulo)

        # Fecha
        fecha = Paragraph(
            f"<i>Generado: {datetime.now().strftime('%d de %B de %Y, %H:%M')}</i>",
            self.styles['CustomBody']
        )
        elementos.append(fecha)
        elementos.append(Spacer(1, 20))

        return elementos

    def _crear_resumen_ejecutivo(self, resultados: Dict, parametros: Dict) -> list:
        """Crea el resumen ejecutivo."""
        elementos = []

        # Título de sección
        elementos.append(Paragraph("<b>Resumen Ejecutivo</b>", self.styles['CustomHeading']))

        # Datos del simulador
        datos = [
            ["<b>Parámetro</b>", "<b>Valor</b>"],
            ["Edad Actual", f"{parametros.get('edad_actual', 'N/A')} años"],
            ["Edad de Jubilación", f"{parametros.get('edad_jubilacion', 'N/A')} años"],
            ["Esperanza de Vida", f"{parametros.get('esperanza_vida', 'N/A')} años"],
            ["Años de Cotización", f"{resultados.get('anos_cotizacion', 'N/A')} años"],
            ["Ingreso Mensual", f"${parametros.get('ingreso_mensual', 0):,.0f}"],
            ["Rentabilidad Esperada", f"{parametros.get('rentabilidad_nominal', 0):.1f}%"],
            ["Inflación Esperada", f"{parametros.get('inflacion_esperada', 0):.1f}%"],
        ]

        tabla = Table(datos, colWidths=[3*inch, 2.5*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')])
        ]))

        elementos.append(tabla)
        elementos.append(Spacer(1, 20))

        return elementos

    def _crear_resultados_principales(self, resultados: Dict) -> list:
        """Crea la sección de resultados principales."""
        elementos = []

        elementos.append(Paragraph("<b>Resultados Principales</b>", self.styles['CustomHeading']))

        datos = [
            ["<b>Métrica</b>", "<b>Valor</b>"],
            ["Saldo Final Acumulado", f"${resultados.get('saldo_final_nominal', 0):,.0f}"],
            ["Pensión Retiro Programado", f"${resultados.get('pension_rp_nominal', 0):,.0f}/mes"],
            ["Pensión Renta Vitalicia", f"${resultados.get('pension_rv_nominal', 0):,.0f}/mes"],
            ["Tasa de Reemplazo (RP)", f"{resultados.get('tasa_reemplazo_rp', 0):.1f}%"],
            ["Tasa de Reemplazo (RV)", f"{resultados.get('tasa_reemplazo_rv', 0):.1f}%"],
            ["Último Sueldo", f"${resultados.get('ultimo_sueldo', 0):,.0f}/mes"],
        ]

        tabla = Table(datos, colWidths=[3.5*inch, 2*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0FDF4')])
        ]))

        elementos.append(tabla)
        elementos.append(Spacer(1, 20))

        # Interpretación
        tasa_reemplazo = resultados.get('tasa_reemplazo_rp', 0)
        if tasa_reemplazo >= 70:
            interpretacion = "✓ <b>Excelente:</b> Su pensión representa un alto porcentaje de su último sueldo."
        elif tasa_reemplazo >= 50:
            interpretacion = "⚠ <b>Aceptable:</b> Su pensión es moderada. Considere ahorros adicionales."
        else:
            interpretacion = "✗ <b>Baja:</b> Su pensión será significativamente menor a su sueldo. Se recomienda aumentar cotizaciones."

        elementos.append(Paragraph(interpretacion, self.styles['CustomBody']))
        elementos.append(Spacer(1, 20))

        return elementos

    def _crear_metricas_financieras(self, resultados: Dict) -> list:
        """Crea la sección de métricas financieras avanzadas."""
        elementos = []

        elementos.append(Paragraph("<b>Métricas Financieras Avanzadas</b>", self.styles['CustomHeading']))

        datos = [
            ["<b>Métrica</b>", "<b>Valor</b>"],
            ["Valor Presente Neto (VPN)", f"${resultados.get('vpn_cotizaciones', 0):,.0f}"],
            ["TIR de Cotizaciones", f"{resultados.get('tir_cotizaciones', 0):.2f}%"],
            ["Rentabilidad Real", f"{resultados.get('rentabilidad_real', 0):.2f}%"],
            ["Valor Presente Pensión", f"${resultados.get('vp_pension_total', 0):,.0f}"],
        ]

        tabla = Table(datos, colWidths=[3.5*inch, 2*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#EFF6FF')])
        ]))

        elementos.append(tabla)
        elementos.append(Spacer(1, 20))

        return elementos

    def _crear_tabla_simulacion(self, resultados: Dict) -> list:
        """Crea tabla con muestra de la simulación."""
        elementos = []

        elementos.append(Paragraph("<b>Detalle de Simulación (Muestra)</b>", self.styles['CustomHeading']))

        df = resultados.get('simulacion_anual')
        if df is not None and len(df) > 0:
            # Mostrar primeros 5 y últimos 5 años
            df_muestra = pd.concat([df.head(5), df.tail(5)])

            datos = [["Año", "Edad", "Ingreso", "Cotización", "Saldo"]]

            for _, row in df_muestra.iterrows():
                datos.append([
                    str(row['ano']),
                    str(row['edad']),
                    f"${row['ingreso_mensual']:,.0f}",
                    f"${row['cotizacion_anual']:,.0f}",
                    f"${row['saldo_nominal']:,.0f}"
                ])

            tabla = Table(datos, colWidths=[0.7*inch, 0.7*inch, 1.5*inch, 1.5*inch, 1.8*inch])
            tabla.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6B7280')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')])
            ]))

            elementos.append(tabla)

        return elementos

    def _crear_disclaimers(self) -> list:
        """Crea la sección de disclaimers legales."""
        elementos = []

        elementos.append(Paragraph("<b>Información Legal y Disclaimers</b>", self.styles['CustomHeading']))

        disclaimer_text = """
        <b>IMPORTANTE - LEA CUIDADOSAMENTE:</b><br/><br/>

        Este reporte es una <b>estimación</b> basada en los parámetros ingresados y <b>no constituye
        asesoría financiera profesional</b>. Los resultados son proyecciones que dependen de múltiples
        variables que pueden cambiar en el futuro.<br/><br/>

        <b>Consideraciones:</b><br/>
        • La rentabilidad futura no está garantizada y puede variar significativamente<br/>
        • No se consideran cambios en la legislación previsional<br/>
        • Los cálculos asumen condiciones de mercado estables<br/>
        • Las cifras no incluyen impuestos adicionales que puedan aplicar<br/>
        • Se recomienda consultar con un asesor financiero certificado antes de tomar decisiones<br/><br/>

        <b>Fuentes de datos:</b> Banco Central de Chile, Superintendencia de Pensiones, CMF.<br/><br/>

        Este simulador es una herramienta educativa para fines informativos.
        """

        elementos.append(Paragraph(disclaimer_text, self.styles['Disclaimer']))

        return elementos
