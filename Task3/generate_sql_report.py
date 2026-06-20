"""
Generates the SQL Analysis PDF Report for Task 3
"""
import pandas as pd
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.units import inch

# ── Load data ────────────────────────────────────────────
df = pd.read_excel('Dataset_for_Data_Analytics__1_.xlsx')
df['CouponCode'] = df['CouponCode'].fillna('No Coupon')
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')
conn = sqlite3.connect(':memory:')
df.to_sql('orders', conn, index=False, if_exists='replace')

def q(sql):
    return pd.read_sql_query(sql, conn)

# ── Styles ───────────────────────────────────────────────
doc = SimpleDocTemplate("SQL_Analysis_Report.pdf", pagesize=letter,
                        topMargin=0.55*inch, bottomMargin=0.55*inch,
                        leftMargin=0.65*inch, rightMargin=0.65*inch)
styles = getSampleStyleSheet()
W = 7.2*inch
PRIMARY = colors.HexColor('#1a3a5c')
ACCENT  = colors.HexColor('#e07b00')
LIGHT   = colors.HexColor('#eef3f8')
CODE_BG = colors.HexColor('#1e1e2e')
CODE_FG = colors.HexColor('#cdd6f4')

title_s = ParagraphStyle('T',  parent=styles['Title'],   fontSize=20, spaceAfter=4)
sub_s   = ParagraphStyle('S',  parent=styles['Normal'],  fontSize=10, textColor=PRIMARY, spaceAfter=16)
h2_s    = ParagraphStyle('H2', parent=styles['Heading2'],fontSize=12, textColor=PRIMARY, spaceAfter=6, spaceBefore=12)
body_s  = ParagraphStyle('B',  parent=styles['Normal'],  fontSize=9.5, leading=14)
code_s  = ParagraphStyle('C',  parent=styles['Code'],    fontSize=8.5, leading=13,
                          backColor=CODE_BG, textColor=CODE_FG,
                          leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4)
insight_s = ParagraphStyle('I', parent=styles['Normal'], fontSize=9, leading=13,
                             textColor=colors.HexColor('#555555'), leftIndent=10)
cell_s  = ParagraphStyle('CS', parent=styles['Normal'],  fontSize=8, leading=10)
cell_h  = ParagraphStyle('CH', parent=styles['Normal'],  fontSize=8, leading=10,
                          textColor=colors.white, fontName='Helvetica-Bold')

def wrow(row, header=False):
    st = cell_h if header else cell_s
    return [Paragraph(str(c), st) for c in row]

def make_table(df_result, col_widths=None):
    data = [wrow(list(df_result.columns), header=True)]
    for _, row in df_result.iterrows():
        data.append(wrow([str(v) for v in row]))
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,0), PRIMARY),
        ('GRID',(0,0),(-1,-1),0.4,colors.grey),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, LIGHT]),
        ('TOPPADDING',(0,0),(-1,-1),4), ('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ]))
    return t

story = []

# ── TITLE ────────────────────────────────────────────────
story.append(Paragraph("SQL Data Analysis Report", title_s))
story.append(Paragraph(
    "DecodeLabs Industrial Training Kit | Data Analytics – Project 3 | Prepared by Pritesh Raj",
    sub_s))
story.append(HRFlowable(width=W, thickness=2, color=PRIMARY))
story.append(Spacer(1, 8))

# ── INTRO ────────────────────────────────────────────────
story.append(Paragraph("Project Overview", h2_s))
story.append(Paragraph(
    "This project demonstrates SQL Data Analysis on 1,200 e-commerce orders using an "
    "SQLite in-memory database. All queries are written in standard SQL and cover "
    "SELECT, WHERE, ORDER BY, GROUP BY, HAVING, COUNT, SUM, and AVG — "
    "extracting actionable business intelligence from raw data.", body_s))
story.append(Spacer(1, 6))

# ── Database Schema ───────────────────────────────────────
story.append(Paragraph("Database Schema: orders table", h2_s))
schema_data = [
    ["Column", "Data Type", "Description"],
    ["OrderID","TEXT","Unique order identifier (ORD######)"],
    ["Date","TEXT","Order date (YYYY-MM-DD)"],
    ["CustomerID","TEXT","Unique customer identifier"],
    ["Product","TEXT","Product category (Chair, Laptop, etc.)"],
    ["Quantity","INTEGER","Units ordered (1–5)"],
    ["UnitPrice","REAL","Price per unit (₹)"],
    ["ShippingAddress","TEXT","Delivery address"],
    ["PaymentMethod","TEXT","Payment type (Cash, Credit Card, etc.)"],
    ["OrderStatus","TEXT","Status: Delivered/Shipped/Pending/Cancelled/Returned"],
    ["TrackingNumber","TEXT","Shipment tracking number"],
    ["ItemsInCart","INTEGER","Items browsed before purchase"],
    ["CouponCode","TEXT","Discount coupon applied"],
    ["ReferralSource","TEXT","Marketing channel (Instagram, Google, etc.)"],
    ["TotalPrice","REAL","Total order value = Quantity × UnitPrice"],
]
story.append(make_table(pd.DataFrame(schema_data[1:], columns=schema_data[0]),
                        col_widths=[1.3*inch, 0.9*inch, 5.0*inch]))
story.append(Spacer(1, 10))

# ── Helper to add a query block ──────────────────────────
def add_query(qnum, title, sql, result_df, insight, col_widths=None):
    story.append(Paragraph(f"Query {qnum}: {title}", h2_s))
    story.append(Paragraph(sql.strip(), code_s))
    story.append(make_table(result_df.head(8), col_widths=col_widths))
    story.append(Paragraph(f"💡 Insight: {insight}", insight_s))
    story.append(Spacer(1, 8))

# ── Q1 ───────────────────────────────────────────────────
sql1 = "SELECT OrderID, Date, Product, Quantity, UnitPrice, TotalPrice, OrderStatus\nFROM   orders  LIMIT 5;"
add_query(1, "Basic SELECT – View Sample Orders", sql1,
    q(sql1),
    "Quick snapshot of the data structure. Each order has a unique ID, date, product, and financial details.",
    col_widths=[0.9*inch,0.85*inch,0.7*inch,0.65*inch,0.75*inch,0.85*inch,0.85*inch])

# ── Q2 ───────────────────────────────────────────────────
sql2 = "SELECT OrderID, Date, Product, TotalPrice, OrderStatus\nFROM   orders  WHERE OrderStatus = 'Delivered'\nORDER  BY TotalPrice DESC  LIMIT 8;"
add_query(2, "WHERE – Top Delivered Orders by Value", sql2,
    q(sql2),
    "The highest-value delivered order was ₹3,456.40 (Tablet). WHERE filters row-by-row before any aggregation.",
    col_widths=[0.9*inch,0.85*inch,0.8*inch,0.85*inch,0.85*inch])

# ── Q3 ───────────────────────────────────────────────────
sql3 = "SELECT OrderID, Product, Quantity, TotalPrice, PaymentMethod\nFROM   orders  WHERE TotalPrice > 2000\nORDER  BY TotalPrice DESC  LIMIT 8;"
add_query(3, "WHERE (Comparison) – High-Value Orders > ₹2,000", sql3,
    q(sql3),
    "180 orders exceed ₹2,000. All are Qty=5 × high UnitPrice — these are bulk/VIP purchases.",
    col_widths=[0.9*inch,0.75*inch,0.7*inch,0.9*inch,1.05*inch])

# ── Q4 ───────────────────────────────────────────────────
sql4 = "SELECT OrderStatus, COUNT(*) AS Total_Orders\nFROM   orders  GROUP BY OrderStatus\nORDER  BY Total_Orders DESC;"
add_query(4, "COUNT + GROUP BY – Orders by Status", sql4,
    q(sql4),
    "⚠ CRITICAL: Cancelled (250) + Returned (247) = 497 orders = 41.4% of all orders. Severe revenue risk.",
    col_widths=[2.5*inch, 2.0*inch])

# ── Q5 ───────────────────────────────────────────────────
sql5 = "SELECT Product, COUNT(*) AS Orders, ROUND(SUM(TotalPrice),2) AS Revenue,\n       ROUND(AVG(TotalPrice),2) AS Avg_Value\nFROM   orders  GROUP BY Product  ORDER BY Revenue DESC;"
add_query(5, "SUM + AVG + GROUP BY – Revenue by Product", sql5,
    q(sql5),
    "Chair (₹195,620) and Printer (₹195,613) lead revenue. Laptop has the highest avg order value (₹1,111).",
    col_widths=[1.0*inch,0.9*inch,1.4*inch,1.2*inch])

# ── Q6 ───────────────────────────────────────────────────
sql6 = "SELECT PaymentMethod, COUNT(*) AS Orders,\n       ROUND(AVG(TotalPrice),2) AS Avg_Value,\n       ROUND(SUM(TotalPrice),2) AS Revenue\nFROM   orders  GROUP BY PaymentMethod  ORDER BY Avg_Value DESC;"
add_query(6, "AVG + GROUP BY – Revenue by Payment Method", sql6,
    q(sql6),
    "Credit Card customers spend the most on average (₹1,128/order). Consider CC-exclusive promotions.",
    col_widths=[1.2*inch,0.9*inch,1.2*inch,1.3*inch])

# ── Q7 ───────────────────────────────────────────────────
sql7 = "SELECT ReferralSource, COUNT(*) AS Orders,\n       ROUND(SUM(TotalPrice),2) AS Revenue\nFROM   orders  GROUP BY ReferralSource  ORDER BY Revenue DESC;"
add_query(7, "GROUP BY + ORDER BY – Revenue by Referral Source", sql7,
    q(sql7),
    "Instagram drives the most revenue (₹275,285). Referral programs generate the least (₹226,816).",
    col_widths=[1.5*inch,1.0*inch,1.4*inch])

# ── Q8 ───────────────────────────────────────────────────
sql8 = "SELECT Product, ROUND(SUM(TotalPrice),2) AS Revenue\nFROM   orders  GROUP BY Product\nHAVING Revenue > 180000  ORDER BY Revenue DESC;"
add_query(8, "HAVING – Products with Revenue > ₹1,80,000", sql8,
    q(sql8),
    "HAVING filters AFTER grouping (unlike WHERE which filters rows). 4 of 7 products exceed ₹1,80,000.",
    col_widths=[1.5*inch,1.5*inch])

# ── Q9 ───────────────────────────────────────────────────
sql9 = "SELECT OrderID, Date, Product, TotalPrice, OrderStatus\nFROM   orders\nWHERE  OrderStatus = 'Cancelled' AND Product = 'Laptop'\nORDER  BY TotalPrice DESC  LIMIT 8;"
add_query(9, "WHERE + AND – Cancelled Laptop Orders", sql9,
    q(sql9),
    "WHERE + AND narrows to a specific segment. Cancelled Laptop orders are high-value — investigating these could recover significant revenue.",
    col_widths=[0.9*inch,0.85*inch,0.75*inch,0.9*inch,0.9*inch])

# ── Q10 ──────────────────────────────────────────────────
sql10 = "SELECT CouponCode, COUNT(*) AS Used, ROUND(SUM(TotalPrice),2) AS Revenue,\n        ROUND(AVG(TotalPrice),2) AS Avg_Value\nFROM   orders  GROUP BY CouponCode  ORDER BY Used DESC;"
add_query(10, "COUNT + SUM – Coupon Code Performance", sql10,
    q(sql10),
    "FREESHIP is the most-used coupon (313 times, ₹3.35L revenue). Customers without coupons also spend similarly.",
    col_widths=[1.1*inch,0.8*inch,1.3*inch,1.2*inch])

# ── Q11 ──────────────────────────────────────────────────
sql11 = "SELECT SUBSTR(Date,1,7) AS Month, COUNT(*) AS Orders,\n        ROUND(SUM(TotalPrice),2) AS Revenue\nFROM   orders  WHERE Date LIKE '2024%'\nGROUP  BY Month  ORDER BY Month;"
add_query(11, "WHERE + GROUP BY – Monthly Revenue (2024)", sql11,
    q(sql11),
    "June 2024 was the peak month (₹68,069, 53 orders). May 2024 was the lowest (₹27,909, 34 orders).",
    col_widths=[1.2*inch,1.0*inch,1.4*inch])

# ── Q12 KPI ──────────────────────────────────────────────
sql12 = """SELECT COUNT(*) AS Total_Orders,
       ROUND(SUM(TotalPrice),2) AS Total_Revenue,
       ROUND(AVG(TotalPrice),2) AS Avg_Order_Value,
       ROUND(MIN(TotalPrice),2) AS Min_Order,
       ROUND(MAX(TotalPrice),2) AS Max_Order,
       COUNT(DISTINCT CustomerID) AS Unique_Customers
FROM   orders;"""
add_query(12, "Executive KPI Dashboard – Overall Business Summary", sql12,
    q(sql12),
    "Total revenue = ₹12,64,762 across 1,200 orders from 1,189 unique customers. Avg order = ₹1,054.",
    col_widths=[0.9*inch,1.1*inch,1.0*inch,0.8*inch,0.8*inch,1.1*inch])

# ── SUMMARY TABLE ────────────────────────────────────────
story.append(Paragraph("SQL Concepts Demonstrated", h2_s))
summary = [
    ["Query","SQL Concept Used","Business Question Answered"],
    ["Q1","SELECT, FROM, LIMIT","What does the raw data look like?"],
    ["Q2","WHERE (equality), ORDER BY","Which delivered orders had highest value?"],
    ["Q3","WHERE (comparison >)","Which orders exceeded ₹2,000?"],
    ["Q4","COUNT, GROUP BY","How many orders per status?"],
    ["Q5","SUM, AVG, GROUP BY","Which product generates most revenue?"],
    ["Q6","AVG, SUM, GROUP BY","Which payment method has highest avg spend?"],
    ["Q7","GROUP BY, ORDER BY","Which marketing channel drives most revenue?"],
    ["Q8","HAVING","Which products cross ₹1.8L revenue?"],
    ["Q9","WHERE, AND","How many Laptops were cancelled?"],
    ["Q10","COUNT, SUM, GROUP BY","Which coupon is most effective?"],
    ["Q11","WHERE LIKE, GROUP BY","What is month-wise revenue for 2024?"],
    ["Q12","COUNT, SUM, AVG, MIN, MAX","What are the overall business KPIs?"],
]
story.append(make_table(pd.DataFrame(summary[1:], columns=summary[0]),
                        col_widths=[0.55*inch, 2.1*inch, 4.55*inch]))
story.append(Spacer(1,10))
story.append(Paragraph("<b>Tools Used:</b> Python 3, SQLite3, Pandas, ReportLab", body_s))

conn.close()
doc.build(story)
print("SQL_Analysis_Report.pdf generated successfully!")
