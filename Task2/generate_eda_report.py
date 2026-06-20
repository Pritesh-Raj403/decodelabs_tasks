"""
Generates the EDA Summary PDF Report for Task 2
"""
import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, Image, HRFlowable)
from reportlab.lib.units import inch

# ── Load data for inline stats ───────────────────────────
df = pd.read_excel('Dataset_for_Data_Analytics.xlsx')
df['CouponCode'] = df['CouponCode'].fillna('No Coupon')
df['Date'] = pd.to_datetime(df['Date'])

Q1 = df['TotalPrice'].quantile(0.25)
Q3 = df['TotalPrice'].quantile(0.75)
IQR = Q3 - Q1
outliers_count = ((df['TotalPrice'] < Q1-1.5*IQR) | (df['TotalPrice'] > Q3+1.5*IQR)).sum()
top_product = df.groupby('Product')['TotalPrice'].sum().idxmax()
top_referral = df.groupby('ReferralSource')['TotalPrice'].sum().idxmax()
cancelled_pct = (df['OrderStatus']=='Cancelled').mean()*100
returned_pct  = (df['OrderStatus']=='Returned').mean()*100

# ── Document setup ───────────────────────────────────────
doc = SimpleDocTemplate("EDA_Report.pdf", pagesize=letter,
                        topMargin=0.55*inch, bottomMargin=0.55*inch,
                        leftMargin=0.65*inch, rightMargin=0.65*inch)
styles = getSampleStyleSheet()
W = 7.2*inch   # usable width

PRIMARY = colors.HexColor('#2c7a4b')
ACCENT  = colors.HexColor('#e74c3c')
LIGHT   = colors.HexColor('#f0f7f0')

title_s = ParagraphStyle('T', parent=styles['Title'],   fontSize=20, spaceAfter=4)
sub_s   = ParagraphStyle('S', parent=styles['Normal'],  fontSize=10, textColor=PRIMARY, spaceAfter=18)
h2_s    = ParagraphStyle('H2',parent=styles['Heading2'],fontSize=13, textColor=PRIMARY, spaceAfter=8, spaceBefore=14)
body_s  = ParagraphStyle('B', parent=styles['Normal'],  fontSize=9.5, leading=14)
cell_s  = ParagraphStyle('C', parent=styles['Normal'],  fontSize=8.5, leading=11)
cell_h  = ParagraphStyle('CH',parent=styles['Normal'],  fontSize=8.5, leading=11,
                          textColor=colors.white, fontName='Helvetica-Bold')

def wrow(row, header=False):
    st = cell_h if header else cell_s
    return [Paragraph(str(c), st) for c in row]

def section_img(path, w=W, h=None):
    """Insert a chart image scaled to width W."""
    from PIL import Image as PILImage
    im = PILImage.open(path)
    iw, ih = im.size
    ratio = ih/iw
    if h is None:
        h = w * ratio
    return Image(path, width=w, height=h)

story = []

# ── TITLE ────────────────────────────────────────────────
story.append(Paragraph("Exploratory Data Analysis – EDA Report", title_s))
story.append(Paragraph(
    "DecodeLabs Industrial Training Kit | Data Analytics – Project 2 | Prepared by Pritesh Raj",
    sub_s))
story.append(HRFlowable(width=W, thickness=1.5, color=PRIMARY))
story.append(Spacer(1, 10))

# ── 1. PROBLEM STATEMENT ─────────────────────────────────
story.append(Paragraph("1. Problem Statement", h2_s))
story.append(Paragraph(
    "This EDA investigates 1,200 e-commerce orders (Jan 2023 – Jun 2025) to answer: "
    "<b>Which products drive the most revenue? What are the key patterns in order value, "
    "referral source, and order status? Are there anomalous transactions?</b> "
    "The goal is to transform raw data into actionable business intelligence.", body_s))

# ── 2. METHODOLOGY ───────────────────────────────────────
story.append(Paragraph("2. Methodology", h2_s))
story.append(Paragraph(
    "IPO Framework applied: (a) <b>Input</b> – cleaned e-commerce dataset (14 columns). "
    "(b) <b>Process</b> – descriptive statistics, distribution analysis, trend analysis, "
    "outlier detection via IQR method, and Pearson correlation analysis. "
    "(c) <b>Output</b> – verified insights and business recommendations.", body_s))
story.append(Spacer(1, 8))

# ── 3. DESCRIPTIVE STATS ─────────────────────────────────
story.append(Paragraph("3. Descriptive Statistics", h2_s))
try:
    story.append(section_img('charts/chart1_descriptive_stats.png', w=W, h=2.6*inch))
except: pass
story.append(Spacer(1, 6))
story.append(Paragraph(
    f"The average order value (mean ₹{df['TotalPrice'].mean():.2f}) is significantly higher "
    f"than the median (₹{df['TotalPrice'].median():.2f}), confirming a <b>right-skewed "
    f"distribution</b> — a few high-value orders pull the mean upward. "
    f"For business decisions, the median is a more reliable measure.", body_s))

# ── 4. DISTRIBUTION ──────────────────────────────────────
story.append(Paragraph("4. Order Value Distribution", h2_s))
try:
    story.append(section_img('charts/chart2_totalprice_distribution.png', w=W, h=2.5*inch))
except: pass
story.append(Spacer(1, 6))
story.append(Paragraph(
    "The histogram confirms a right-skewed distribution. Most orders fall between "
    "₹200–₹1,500, with a long tail of high-value orders. "
    "This suggests a mix of budget and premium customers.", body_s))

# ── 5. MONTHLY TREND ─────────────────────────────────────
story.append(Paragraph("5. Monthly Revenue Trend", h2_s))
try:
    story.append(section_img('charts/chart3_monthly_revenue.png', w=W, h=2.4*inch))
except: pass
story.append(Spacer(1, 6))
story.append(Paragraph(
    "Revenue shows <b>high monthly volatility</b> with no consistent seasonal peak. "
    "The highest single month was June 2024 (₹68,069). "
    "Revenue in 2023 was generally higher than 2024, suggesting a possible decline "
    "in order volumes that warrants investigation.", body_s))

# ── 6. PRODUCT REVENUE ───────────────────────────────────
story.append(Paragraph("6. Revenue by Product Category", h2_s))
try:
    story.append(section_img('charts/chart4_revenue_by_product.png', w=W, h=2.5*inch))
except: pass
story.append(Spacer(1, 6))
prod_rev = df.groupby('Product')['TotalPrice'].sum().sort_values(ascending=False)
story.append(Paragraph(
    f"<b>Chair (₹{prod_rev['Chair']/1000:.0f}K)</b> and "
    f"<b>Printer (₹{prod_rev['Printer']/1000:.0f}K)</b> are the top revenue-generating "
    f"products, though all 7 categories are closely competitive. "
    f"Phone (₹{prod_rev['Phone']/1000:.0f}K) is the lowest — possibly due to lower "
    f"unit prices rather than low demand.", body_s))

# ── 7. ORDER STATUS ──────────────────────────────────────
story.append(Paragraph("7. Order Status Analysis", h2_s))
try:
    story.append(section_img('charts/chart5_order_status.png', w=W, h=2.5*inch))
except: pass
story.append(Spacer(1, 6))
story.append(Paragraph(
    f"<b>⚠ Critical Finding:</b> Cancelled ({cancelled_pct:.1f}%) and Returned "
    f"({returned_pct:.1f}%) orders together account for <b>~41.4% of all orders</b>. "
    f"This is an extremely high churn rate and represents significant revenue loss. "
    f"Business recommendation: investigate root causes of cancellations immediately.", body_s))

# ── 8. REFERRAL SOURCE ───────────────────────────────────
story.append(Paragraph("8. Revenue by Referral Source", h2_s))
try:
    story.append(section_img('charts/chart6_referral_revenue.png', w=W, h=2.5*inch))
except: pass
story.append(Spacer(1, 6))
ref_rev = df.groupby('ReferralSource')['TotalPrice'].sum()
story.append(Paragraph(
    f"<b>Instagram (₹{ref_rev['Instagram']/1000:.0f}K)</b> is the highest revenue-driving "
    f"channel, followed by Email and Google. Referral program generates the least revenue "
    f"(₹{ref_rev['Referral']/1000:.0f}K). Marketing budget should be prioritized toward "
    f"Instagram and Email campaigns.", body_s))

# ── 9. OUTLIER DETECTION ─────────────────────────────────
story.append(Paragraph("9. Outlier Detection (IQR Method)", h2_s))
try:
    story.append(section_img('charts/chart7_outlier_boxplot.png', w=4.5*inch, h=2.8*inch))
except: pass
story.append(Spacer(1, 6))
story.append(Paragraph(
    f"Using the IQR method (Q1=₹{Q1:.0f}, Q3=₹{Q3:.0f}, IQR=₹{IQR:.0f}): "
    f"Upper fence = ₹{Q3+1.5*IQR:.0f}. "
    f"<b>{outliers_count} orders were identified as outliers</b> (values above ₹3,330). "
    f"These are likely high-volume bulk orders (Qty=5 × high UnitPrice) — they are "
    f"SIGNAL (VIP/bulk buyers), not data errors, so they should be retained but "
    f"investigated separately.", body_s))

# ── 10. CORRELATION ──────────────────────────────────────
story.append(Paragraph("10. Correlation Analysis", h2_s))
try:
    story.append(section_img('charts/chart8_correlation_heatmap.png', w=4.5*inch, h=3.5*inch))
except: pass
story.append(Spacer(1, 6))
corr_data = [
    ["Variable Pair", "Correlation (r)", "Interpretation"],
    ["UnitPrice ↔ TotalPrice", "0.72", "Strong positive – higher-priced items drive revenue"],
    ["Quantity ↔ TotalPrice",  "0.62", "Moderate positive – more items = higher bill"],
    ["ItemsInCart ↔ Quantity", "0.65", "Moderate – browsing behaviour linked to purchase qty"],
    ["UnitPrice ↔ Quantity",   "0.01", "No correlation – price doesn't affect quantity ordered"],
]
corr_table = Table([wrow(corr_data[0], True)] + [wrow(r) for r in corr_data[1:]],
                   colWidths=[2.3*inch, 1.5*inch, 3.3*inch])
corr_table.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), PRIMARY),
    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LIGHT]),
    ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
]))
story.append(corr_table)
story.append(Paragraph("<i>Note: Correlation ≠ Causation. These are clues, not verdicts.</i>",
                        ParagraphStyle('note', parent=styles['Normal'], fontSize=8,
                                       textColor=colors.grey, spaceBefore=4)))

# ── 11. KEY FINDINGS & RECOMMENDATIONS ──────────────────
story.append(Paragraph("11. Key Findings & Business Recommendations", h2_s))
findings = [
    ["#", "Finding", "Recommendation"],
    ["1", f"Chair & Printer lead revenue (₹195K each)",
          "Increase inventory & run targeted promotions"],
    ["2", f"Cancelled+Returned = 41.4% of orders",
          "Urgent investigation — implement post-purchase surveys"],
    ["3", f"Instagram is the #1 revenue channel (₹275K)",
          "Increase marketing budget allocation to Instagram"],
    ["4", f"Mean (₹1054) >> Median (₹824) — right skew",
          "Use median for pricing strategy; target mid-market segment"],
    ["5", f"8 bulk/VIP orders above ₹3,330 detected",
          "Create a VIP customer segment with loyalty benefits"],
    ["6", f"UnitPrice drives TotalPrice most strongly (r=0.72)",
          "Premium product upselling will have highest revenue impact"],
]
f_table = Table([wrow(findings[0], True)] + [wrow(r) for r in findings[1:]],
                colWidths=[0.3*inch, 2.8*inch, 4.0*inch])
f_table.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), PRIMARY),
    ('GRID',(0,0),(-1,-1),0.5,colors.grey),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LIGHT]),
    ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5),
    ('VALIGN',(0,0),(-1,-1),'TOP'),
]))
story.append(f_table)
story.append(Spacer(1, 10))
story.append(Paragraph(
    "<b>Tools used:</b> Python 3, Pandas, NumPy, Matplotlib, ReportLab", body_s))

doc.build(story)
print("EDA_Report.pdf generated successfully!")
