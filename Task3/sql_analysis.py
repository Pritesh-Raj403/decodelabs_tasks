"""
DecodeLabs Internship - Week 3, Task 3
Project: SQL Data Analysis
---------------------------------------------------
Goal: Use SQL queries to extract business insights
from the e-commerce orders dataset using SELECT,
WHERE, ORDER BY, GROUP BY, COUNT, SUM, AVG.

Author: Pritesh Raj

Approach: We load the Excel dataset into an in-memory
SQLite database and run real SQL queries on it.
This is the standard industry approach when working
with flat files before a proper DB is set up.
"""

import pandas as pd
import sqlite3

# ── STEP 1: Load dataset into SQLite ────────────────────
df = pd.read_excel('Dataset_for_Data_Analytics__1_.xlsx')
df['CouponCode'] = df['CouponCode'].fillna('No Coupon')
df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

conn = sqlite3.connect(':memory:')
df.to_sql('orders', conn, index=False, if_exists='replace')
print("✅ Dataset loaded into SQLite.")
print(f"   Table: orders | Rows: {len(df)} | Columns: {len(df.columns)}\n")
print("=" * 65)

def run_query(title, sql, show_rows=10):
    """Helper: run a SQL query, print results neatly."""
    print(f"\n{'─'*65}")
    print(f"📌 {title}")
    print(f"SQL:\n{sql.strip()}\n")
    result = pd.read_sql_query(sql, conn)
    print(result.head(show_rows).to_string(index=False))
    print(f"   ({len(result)} row(s) returned)")
    return result

# ════════════════════════════════════════════════════════
# QUERY 1 – SELECT: View first 5 orders
# ════════════════════════════════════════════════════════
run_query(
    "Q1: Basic SELECT – View top 5 orders",
    """
    SELECT OrderID, Date, CustomerID, Product,
           Quantity, UnitPrice, TotalPrice, OrderStatus
    FROM   orders
    LIMIT  5;
    """,
    show_rows=5
)

# ════════════════════════════════════════════════════════
# QUERY 2 – WHERE: Filter Delivered orders
# ════════════════════════════════════════════════════════
run_query(
    "Q2: WHERE – Only 'Delivered' orders",
    """
    SELECT OrderID, Date, Product, TotalPrice, OrderStatus
    FROM   orders
    WHERE  OrderStatus = 'Delivered'
    ORDER  BY TotalPrice DESC
    LIMIT  10;
    """
)

# ════════════════════════════════════════════════════════
# QUERY 3 – WHERE + comparison: High value orders > 2000
# ════════════════════════════════════════════════════════
run_query(
    "Q3: WHERE (Comparison) – Orders with TotalPrice > 2000",
    """
    SELECT OrderID, Product, Quantity, UnitPrice,
           TotalPrice, PaymentMethod
    FROM   orders
    WHERE  TotalPrice > 2000
    ORDER  BY TotalPrice DESC;
    """,
    show_rows=10
)

# ════════════════════════════════════════════════════════
# QUERY 4 – COUNT: Total number of orders per status
# ════════════════════════════════════════════════════════
run_query(
    "Q4: COUNT + GROUP BY – Orders count by Status",
    """
    SELECT OrderStatus,
           COUNT(*) AS Total_Orders
    FROM   orders
    GROUP  BY OrderStatus
    ORDER  BY Total_Orders DESC;
    """
)

# ════════════════════════════════════════════════════════
# QUERY 5 – SUM + GROUP BY: Revenue by Product
# ════════════════════════════════════════════════════════
run_query(
    "Q5: SUM + GROUP BY – Total Revenue by Product",
    """
    SELECT Product,
           COUNT(*)                    AS Total_Orders,
           SUM(TotalPrice)             AS Total_Revenue,
           ROUND(AVG(TotalPrice), 2)   AS Avg_Order_Value
    FROM   orders
    GROUP  BY Product
    ORDER  BY Total_Revenue DESC;
    """
)

# ════════════════════════════════════════════════════════
# QUERY 6 – AVG + GROUP BY: Avg order value by Payment
# ════════════════════════════════════════════════════════
run_query(
    "Q6: AVG + GROUP BY – Average Order Value by Payment Method",
    """
    SELECT PaymentMethod,
           COUNT(*)                    AS Total_Orders,
           ROUND(AVG(TotalPrice), 2)   AS Avg_Order_Value,
           ROUND(SUM(TotalPrice), 2)   AS Total_Revenue
    FROM   orders
    GROUP  BY PaymentMethod
    ORDER  BY Avg_Order_Value DESC;
    """
)

# ════════════════════════════════════════════════════════
# QUERY 7 – GROUP BY + ORDER BY: Top Referral Sources
# ════════════════════════════════════════════════════════
run_query(
    "Q7: GROUP BY + ORDER BY – Revenue by Referral Source",
    """
    SELECT ReferralSource,
           COUNT(*)                    AS Total_Orders,
           ROUND(SUM(TotalPrice), 2)   AS Total_Revenue,
           ROUND(AVG(TotalPrice), 2)   AS Avg_Order_Value
    FROM   orders
    GROUP  BY ReferralSource
    ORDER  BY Total_Revenue DESC;
    """
)

# ════════════════════════════════════════════════════════
# QUERY 8 – HAVING: Products with revenue > 180,000
# ════════════════════════════════════════════════════════
run_query(
    "Q8: HAVING – Products with Total Revenue > 180,000",
    """
    SELECT Product,
           ROUND(SUM(TotalPrice), 2) AS Total_Revenue
    FROM   orders
    GROUP  BY Product
    HAVING Total_Revenue > 180000
    ORDER  BY Total_Revenue DESC;
    """
)

# ════════════════════════════════════════════════════════
# QUERY 9 – WHERE + AND: Cancelled Laptop orders
# ════════════════════════════════════════════════════════
run_query(
    "Q9: WHERE + AND – Cancelled Laptop orders",
    """
    SELECT OrderID, Date, CustomerID,
           Product, TotalPrice, OrderStatus
    FROM   orders
    WHERE  OrderStatus = 'Cancelled'
      AND  Product = 'Laptop'
    ORDER  BY TotalPrice DESC
    LIMIT  10;
    """
)

# ════════════════════════════════════════════════════════
# QUERY 10 – Coupon Usage Analysis
# ════════════════════════════════════════════════════════
run_query(
    "Q10: COUNT + SUM – Coupon Code Usage & Revenue",
    """
    SELECT CouponCode,
           COUNT(*)                    AS Times_Used,
           ROUND(SUM(TotalPrice), 2)   AS Total_Revenue,
           ROUND(AVG(TotalPrice), 2)   AS Avg_Order_Value
    FROM   orders
    GROUP  BY CouponCode
    ORDER  BY Times_Used DESC;
    """
)

# ════════════════════════════════════════════════════════
# QUERY 11 – Monthly Revenue Trend (WHERE year filter)
# ════════════════════════════════════════════════════════
run_query(
    "Q11: WHERE + GROUP BY – Monthly Revenue for Year 2024",
    """
    SELECT SUBSTR(Date, 1, 7)          AS Month,
           COUNT(*)                    AS Total_Orders,
           ROUND(SUM(TotalPrice), 2)   AS Monthly_Revenue
    FROM   orders
    WHERE  Date LIKE '2024%'
    GROUP  BY Month
    ORDER  BY Month;
    """
)

# ════════════════════════════════════════════════════════
# QUERY 12 – Business KPI Summary (Executive Dashboard)
# ════════════════════════════════════════════════════════
run_query(
    "Q12: Business KPI Summary – Overall Performance",
    """
    SELECT COUNT(*)                             AS Total_Orders,
           ROUND(SUM(TotalPrice), 2)            AS Total_Revenue,
           ROUND(AVG(TotalPrice), 2)            AS Avg_Order_Value,
           ROUND(MIN(TotalPrice), 2)            AS Min_Order_Value,
           ROUND(MAX(TotalPrice), 2)            AS Max_Order_Value,
           COUNT(DISTINCT CustomerID)           AS Unique_Customers,
           COUNT(DISTINCT Product)              AS Product_Categories
    FROM   orders;
    """
)

print("\n" + "=" * 65)
print("✅ All 12 SQL queries executed successfully!")
conn.close()
