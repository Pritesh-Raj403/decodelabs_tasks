# Task 2 – Exploratory Data Analysis (EDA)

**Internship:** DecodeLabs Industrial Training Kit (Data Analytics Track)
**Week:** 2
**Author:** Pritesh Raj

## 📌 Goal
Analyze the e-commerce orders dataset to uncover hidden patterns, trends, distributions, and outliers — transforming raw numbers into actionable business intelligence.

## 📂 Files in this Folder
| File | Description |
|------|-------------|
| `Dataset_for_Data_Analytics.xlsx` | Raw e-commerce dataset (1200 rows, 14 columns) |
| `eda_analysis.py` | Main EDA script — generates all statistics and 8 charts |
| `generate_eda_report.py` | Script that builds the formatted PDF EDA report |
| `EDA_Report.pdf` | Full EDA report with charts, insights & recommendations |
| `charts/` | Folder containing all 8 generated chart images |

## 🔍 Key Findings

| # | Finding | Business Impact |
|---|---------|----------------|
| 1 | Chair & Printer are top revenue products (~₹195K each) | Focus inventory & promotions here |
| 2 | Cancelled + Returned orders = **41.4%** of all orders | Critical — investigate root cause urgently |
| 3 | Instagram is the #1 revenue channel (₹275K) | Increase Instagram marketing budget |
| 4 | Mean order value (₹1054) >> Median (₹824) — right skew | Use median for strategy; target mid-market |
| 5 | 8 outlier orders detected above ₹3,330 (IQR method) | Bulk/VIP buyers — create loyalty segment |
| 6 | UnitPrice is the strongest driver of TotalPrice (r=0.72) | Premium upselling = highest revenue impact |

## 📊 Charts Generated (8 total)
1. Descriptive Statistics Table
2. TotalPrice Distribution (Histogram)
3. Monthly Revenue Trend (2023–2025)
4. Revenue by Product Category
5. Order Status Distribution
6. Revenue by Referral Source
7. Outlier Detection (Boxplot – IQR Method)
8. Correlation Heatmap

## 🛠️ Techniques Used
- Descriptive Statistics (mean, median, std, quartiles)
- Distribution Analysis (histogram, skewness)
- Trend Analysis (monthly revenue)
- Outlier Detection (IQR Method: Q1 - 1.5×IQR, Q3 + 1.5×IQR)
- Correlation Analysis (Pearson r)

## ▶️ How to Run
```bash
pip install pandas matplotlib seaborn reportlab openpyxl Pillow
python eda_analysis.py
python generate_eda_report.py
```

## 🧰 Tools Used
Python, Pandas, NumPy, Matplotlib, ReportLab, Pillow
