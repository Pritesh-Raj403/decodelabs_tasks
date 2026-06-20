# Task 3 – SQL Data Analysis

**Internship:** DecodeLabs Industrial Training Kit (Data Analytics Track)
**Week:** 3
**Author:** Pritesh Raj

## 📌 Goal
Use SQL queries to extract business insights from the e-commerce orders dataset — demonstrating SELECT, WHERE, ORDER BY, GROUP BY, HAVING, COUNT, SUM, and AVG.

## 📂 Files in this Folder
| File | Description |
|------|-------------|
| `Dataset_for_Data_Analytics__1_.xlsx` | Raw e-commerce dataset (1200 rows, 14 columns) |
| `sql_analysis.py` | Main SQL script — loads data into SQLite and runs all 12 queries |
| `generate_sql_report.py` | Script that builds the formatted PDF SQL report |
| `SQL_Analysis_Report.pdf` | Full report with all queries, results & business insights |

## 🗄️ Approach
The dataset (Excel) is loaded into an **SQLite in-memory database** using Python. This is the standard industry approach for SQL analysis on flat files — all queries are written in pure standard SQL and executed directly on the database.

## 📊 Queries Written (12 total)

| # | SQL Concepts Used | Business Question |
|---|-------------------|-------------------|
| Q1  | SELECT, FROM, LIMIT | View sample orders |
| Q2  | WHERE (equality), ORDER BY | Top delivered orders by value |
| Q3  | WHERE (comparison >)  | High-value orders > ₹2,000 |
| Q4  | COUNT, GROUP BY | Orders count by status |
| Q5  | SUM, AVG, GROUP BY | Revenue by product category |
| Q6  | AVG, SUM, GROUP BY | Average spend by payment method |
| Q7  | GROUP BY, ORDER BY | Revenue by referral/marketing source |
| Q8  | HAVING | Products crossing ₹1,80,000 revenue |
| Q9  | WHERE, AND | Cancelled Laptop orders |
| Q10 | COUNT, SUM, GROUP BY | Coupon code performance |
| Q11 | WHERE LIKE, GROUP BY | Month-wise revenue for 2024 |
| Q12 | COUNT, SUM, AVG, MIN, MAX | Executive KPI dashboard |

## 🔍 Key SQL Findings
- **₹12,64,762** total revenue across 1,200 orders
- **Cancelled + Returned = 41.4%** of all orders — critical business risk
- **Chair & Printer** lead revenue (~₹1.95L each)
- **Instagram** is the #1 revenue channel (₹2.75L)
- **Credit Card** users have highest avg order value (₹1,128)
- **June 2024** was peak month (₹68,069 revenue)

## ▶️ How to Run
```bash
pip install pandas openpyxl reportlab
python sql_analysis.py          # runs all 12 queries, prints results
python generate_sql_report.py   # generates PDF report
```

## 🧰 Tools Used
Python 3, SQLite3, Pandas, ReportLab
