from io import BytesIO
from decimal import Decimal
from datetime import datetime
import locale
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, Flowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

# Opcional: si quieres usar una fuente TTF personalizada, registra aquí
# pdfmetrics.registerFont(TTFont('Inter', '/path/to/Inter-Regular.ttf'))

def _header_footer(canvas: Canvas, doc):
    """Dibuja cabecera y pie de página en cada página."""
    width, height = letter
    # Cabecera: barra superior con color y título pequeño
    header_height = 40
    canvas.saveState()
    canvas.setFillColor(colors.HexColor('#22577A'))
    canvas.rect(0, height - header_height, width, header_height, fill=1, stroke=0)
    canvas.setFillColor(colors.whitesmoke)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(inch * 0.6, height - header_height + 12, "CashFlow — Informe de Transacciones")
    # Pie: número de página y fecha de generación
    canvas.setFillColor(colors.HexColor('#38A3A5'))
    canvas.setFont("Helvetica", 9)
    footer_y = 0.5 * inch
    canvas.drawString(inch * 0.6, footer_y, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    canvas.drawRightString(width - inch * 0.6, footer_y, f"Página {doc.page}")
    canvas.restoreState()

def _fmt_currency(value):
    """Formatea Decimal/float a $X.XXX,XX (sin depender del locale del sistema)."""
    try:
        v = Decimal(value)
    except Exception:
        v = Decimal('0')
    # separador de miles con coma y punto decimal
    s = f"${v:,.2f}"
    return s

def _make_pie_by_category(transactions):
    """Devuelve BytesIO con un pie chart por categoría (por importe absoluto)."""
    # Agrupar por categoría
    cat_map = {}
    for tx in transactions:
        name = tx.category.name if getattr(tx, 'category', None) else "Sin categoría"
        amt = Decimal(tx.amount)
        amt = abs(amt)
        cat_map[name] = cat_map.get(name, Decimal('0')) + amt
    if not cat_map:
        return None
    labels = list(cat_map.keys())
    sizes = [float(v) for v in cat_map.values()]
    # Colores basados en la paleta
    palette = ['#22577A', '#38A3A5', '#57CC99', '#80ED99', '#C7F9CC']
    fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        autopct=lambda pct: f"{pct:.1f}%",
        textprops=dict(fontsize=8),
        colors=[palette[i % len(palette)] for i in range(len(labels))],
        startangle=90
    )
    ax.axis('equal')
    plt.tight_layout()
    bio = BytesIO()
    fig.savefig(bio, format='png', bbox_inches='tight', dpi=150)
    plt.close(fig)
    bio.seek(0)
    return bio

def _make_monthly_trend(transactions, start_date=None, end_date=None):
    """Gráfico de barras: ingresos vs gastos por mes."""
    import calendar
    from collections import defaultdict
    monthly = defaultdict(lambda: {'income': Decimal('0'), 'expense': Decimal('0')})
    for tx in transactions:
        dt = tx.created_at
        key = f"{dt.year}-{dt.month:02d}"
        if tx.type == 'income':
            monthly[key]['income'] += Decimal(tx.amount)
        else:
            monthly[key]['expense'] += Decimal(tx.amount)
    if not monthly:
        return None
    # ordenar por fecha
    keys = sorted(monthly.keys())
    incomes = [float(monthly[k]['income']) for k in keys]
    expenses = [float(monthly[k]['expense']) for k in keys]
    x = range(len(keys))
    palette = ['#38A3A5', '#22577A']
    fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
    width = 0.35
    ax.bar([i - width/2 for i in x], incomes, width, label='Ingresos', color=palette[0])
    ax.bar([i + width/2 for i in x], expenses, width, label='Gastos', color=palette[1])
    ax.set_xticks(x)
    # etiquetas más amigables: "2025-03" -> "Mar 2025"
    xticks = []
    for k in keys:
        y, m = k.split('-')
        xticks.append(f"{calendar.month_abbr[int(m)]} {y}")
    ax.set_xticklabels(xticks, rotation=45, ha='right', fontsize=8)
    ax.legend(fontsize=8)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    bio = BytesIO()
    fig.savefig(bio, format='png', bbox_inches='tight', dpi=150)
    plt.close(fig)
    bio.seek(0)
    return bio

def generate_pdf(user, transactions, start_date=None, end_date=None):
    """
    Genera un PDF estilizado con:
    - Cabecera / Pie con paginación
    - Tabla de transacciones
    - Resumen financiero
    - Gráficos: tendencia mensual y distribución por categoría
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            leftMargin=inch*0.6, rightMargin=inch*0.6,
                            topMargin=inch, bottomMargin=inch)
    elements = []
    styles = getSampleStyleSheet()

    # Paleta
    primary = colors.HexColor('#22577A')
    secondary = colors.HexColor('#38A3A5')
    accent1 = colors.HexColor('#57CC99')
    accent2 = colors.HexColor('#80ED99')
    pale = colors.HexColor('#C7F9CC')

    # TITLE
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        alignment=TA_CENTER,
        textColor=primary,
        spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        textColor=secondary,
        spaceAfter=12
    )

    elements.append(Paragraph("CashFlow", title_style))
    elements.append(Paragraph("Informe de Transacciones", subtitle_style))

    # Información del periodo y usuario
    period_text = f"{start_date.strftime('%Y-%m-%d') if start_date else 'Inicio'} — {end_date.strftime('%Y-%m-%d') if end_date else 'Hoy'}"
    meta_style = ParagraphStyle('meta', parent=styles['Normal'], fontSize=9, textColor=colors.black)
    elements.append(Paragraph(f"<b>Usuario:</b> {getattr(user, 'get_full_name', lambda: getattr(user,'username',str(user)))() if callable(getattr(user, 'get_full_name', None)) else getattr(user,'username',str(user))}", meta_style))
    elements.append(Paragraph(f"<b>Período:</b> {period_text}", meta_style))
    elements.append(Paragraph(f"<b>Generado:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", meta_style))
    elements.append(Spacer(1, 0.15*inch))

    # Prepara lista de transacciones
    tx_list = list(transactions) if hasattr(transactions, '__iter__') else []
    # Tabla de transacciones
    data = [['Fecha', 'Tipo', 'Monto', 'Categoría', 'Descripción']]
    for tx in tx_list:
        date_s = tx.created_at.strftime('%Y-%m-%d %H:%M')
        tipo = 'Ingreso' if tx.type == 'income' else 'Gasto'
        monto = _fmt_currency(tx.amount)
        cat = tx.category.name if getattr(tx, 'category', None) else '—'
        desc = (tx.description or '')[:60] + ('...' if (tx.description and len(tx.description) > 60) else '')
        data.append([date_s, tipo, monto, cat, desc])

    if not tx_list:
        data.append(['—', '—', '—', '—', 'Sin transacciones en el período'])

    col_widths = [1.25*inch, 0.8*inch, 1*inch, 1.2*inch, 2.25*inch]
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e6eef2')),
        ('ALIGN', (2, 1), (2, -1), 'RIGHT'),  # monto a la derecha
        ('ALIGN', (0, 1), (1, -1), 'CENTER'),
        ('ALIGN', (3, 1), (3, -1), 'LEFT'),
        ('ALIGN', (4, 1), (4, -1), 'LEFT'),
        # Espaciado de filas
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    # Row backgrounds alternados usando la paleta
    row_bg = []
    for i in range(1, len(data)):
        color = colors.whitesmoke if i % 2 == 1 else pale
        row_bg.append(('BACKGROUND', (0, i), (-1, i), color))
    for rg in row_bg:
        table_style.add(*rg)
    table.setStyle(table_style)

    elements.append(table)
    elements.append(Spacer(1, 0.25*inch))

    # RESUMEN financiero
    # Usamos agregaciones seguras
    total_income = sum([Decimal(tx.amount) for tx in tx_list if tx.type == 'income'], Decimal('0'))
    total_expense = sum([Decimal(tx.amount) for tx in tx_list if tx.type == 'expense'], Decimal('0'))
    balance = total_income - total_expense

    summary_data = [
        ['RESUMEN FINANCIERO', ''],
        ['Ingresos totales:', _fmt_currency(total_income)],
        ['Gastos totales:', _fmt_currency(total_expense)],
        ['Balance:', _fmt_currency(balance)],
    ]
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), secondary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e6eef2')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f7fffb'), colors.HexColor('#eefef4')]),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.25*inch))

    # GRÁFICOS
    pie_bio = _make_pie_by_category(tx_list)
    trend_bio = _make_monthly_trend(tx_list, start_date, end_date)

    if trend_bio:
        elements.append(Paragraph("Tendencia mensual (Ingresos vs Gastos)", ParagraphStyle('h', parent=styles['Heading3'], fontSize=12, textColor=primary)))
        img = Image(trend_bio, width=6*inch, height=2.8*inch)
        elements.append(img)
        elements.append(Spacer(1, 0.2*inch))

    if pie_bio:
        elements.append(Paragraph("Distribución por categoría (valores absolutos)", ParagraphStyle('h', parent=styles['Heading3'], fontSize=12, textColor=primary)))
        img2 = Image(pie_bio, width=3.8*inch, height=3.8*inch)
        elements.append(img2)
        elements.append(Spacer(1, 0.2*inch))

    # Pie de página / Notas
    note_style = ParagraphStyle('note', parent=styles['Normal'], fontSize=8, textColor=colors.grey)
    elements.append(Spacer(1, 0.15*inch))
    elements.append(Paragraph("Nota: Los montos están en la moneda registrada en la cuenta. Revisa las transacciones para detalles.", note_style))

    # Construir documento con header/footer
    doc.build(elements, onFirstPage=_header_footer, onLaterPages=_header_footer)

    buffer.seek(0)
    from django.http import HttpResponse
    filename = f"informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
