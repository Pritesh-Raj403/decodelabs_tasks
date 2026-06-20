"""
DecodeLabs Internship - Week 2, Task 2
Project: Exploratory Data Analysis (EDA)
-------------------------------------------------
Goal: Analyze the e-commerce orders dataset to uncover
patterns, trends, distributions, and outliers.

Author: Pritesh Raj
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

# ── colour palette ──────────────────────────────────────
COLORS = ['#2ecc71','#3498db','#e74c3c','#f39c12','#9b59b6','#1abc9c','#e67e22']
PRIMARY = '#2c7a4b'
ACCENT  = '#e74c3c'

# ── 0. LOAD & PREP ──────────────────────────────────────
df = pd.read_excel('Dataset_for_Data_Analytics.xlsx')
df['CouponCode'] = df['CouponCode'].fillna('No Coupon')
df['Date']       = pd.to_datetime(df['Date'])
df['Month']      = df['Date'].dt.to_period('M')
df['Year']       = df['Date'].dt.year

print("Dataset loaded:", df.shape)
print("Date range:", df['Date'].min().date(), "to", df['Date'].max().date())

# ── helper ──────────────────────────────────────────────
def save(fig, name):
    path = f"charts/{name}"
    fig.savefig(path, dpi=130, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  saved → {path}")

# ════════════════════════════════════════════════════════
# CHART 1 – Descriptive Statistics Summary (table image)
# ════════════════════════════════════════════════════════
stats = df[['Quantity','UnitPrice','TotalPrice','ItemsInCart']].describe().round(2)
fig, ax = plt.subplots(figsize=(9, 3.5))
ax.axis('off')
tbl = ax.table(cellText=stats.values,
               rowLabels=stats.index,
               colLabels=stats.columns,
               cellLoc='center', loc='center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(10)
tbl.scale(1, 1.6)
for (r, c), cell in tbl.get_celld().items():
    if r == 0 or c == -1:
        cell.set_facecolor(PRIMARY)
        cell.set_text_props(color='white', fontweight='bold')
    else:
        cell.set_facecolor('#f0f7f0' if r % 2 == 0 else 'white')
plt.title('Descriptive Statistics – Numeric Columns', fontsize=13,
          fontweight='bold', color=PRIMARY, pad=12)
save(fig, 'chart1_descriptive_stats.png')

# ════════════════════════════════════════════════════════
# CHART 2 – TotalPrice Distribution (histogram)
# ════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(df['TotalPrice'], bins=35, color=PRIMARY, edgecolor='white', linewidth=0.5)
ax.axvline(df['TotalPrice'].mean(),   color=ACCENT,    lw=2, ls='--', label=f"Mean  ₹{df['TotalPrice'].mean():.0f}")
ax.axvline(df['TotalPrice'].median(), color='#f39c12', lw=2, ls='-',  label=f"Median ₹{df['TotalPrice'].median():.0f}")
ax.set_xlabel('Total Price (₹)', fontsize=11)
ax.set_ylabel('Number of Orders', fontsize=11)
ax.set_title('Distribution of Order Value (TotalPrice)', fontsize=13, fontweight='bold', color=PRIMARY)
ax.legend()
ax.spines[['top','right']].set_visible(False)
save(fig, 'chart2_totalprice_distribution.png')

# ════════════════════════════════════════════════════════
# CHART 3 – Monthly Revenue Trend
# ════════════════════════════════════════════════════════
monthly = df.groupby('Month')['TotalPrice'].sum()
fig, ax = plt.subplots(figsize=(13, 4))
ax.plot(monthly.index.astype(str), monthly.values, color=PRIMARY, lw=2, marker='o', ms=4)
ax.fill_between(monthly.index.astype(str), monthly.values, alpha=0.15, color=PRIMARY)
ax.set_title('Monthly Revenue Trend (2023–2025)', fontsize=13, fontweight='bold', color=PRIMARY)
ax.set_ylabel('Revenue (₹)', fontsize=11)
ax.set_xlabel('Month', fontsize=11)
# show only every 4th label to avoid clutter
labels = monthly.index.astype(str)
ax.set_xticks(range(len(labels)))
ax.set_xticklabels([l if i % 4 == 0 else '' for i, l in enumerate(labels)], rotation=45, ha='right')
ax.spines[['top','right']].set_visible(False)
save(fig, 'chart3_monthly_revenue.png')

# ════════════════════════════════════════════════════════
# CHART 4 – Revenue by Product (horizontal bar)
# ════════════════════════════════════════════════════════
prod_rev = df.groupby('Product')['TotalPrice'].sum().sort_values()
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.barh(prod_rev.index, prod_rev.values, color=COLORS[:len(prod_rev)])
ax.bar_label(bars, labels=[f'₹{v/1000:.0f}K' for v in prod_rev.values], padding=4, fontsize=9)
ax.set_xlabel('Total Revenue (₹)', fontsize=11)
ax.set_title('Total Revenue by Product Category', fontsize=13, fontweight='bold', color=PRIMARY)
ax.spines[['top','right']].set_visible(False)
ax.set_xlim(0, prod_rev.max() * 1.15)
save(fig, 'chart4_revenue_by_product.png')

# ════════════════════════════════════════════════════════
# CHART 5 – Order Status Distribution (bar)
# ════════════════════════════════════════════════════════
status_counts = df['OrderStatus'].value_counts()
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(status_counts.index, status_counts.values,
              color=[PRIMARY,'#3498db','#f39c12',ACCENT,'#9b59b6'])
ax.bar_label(bars, padding=3, fontsize=10)
ax.set_ylabel('Number of Orders', fontsize=11)
ax.set_title('Order Status Distribution', fontsize=13, fontweight='bold', color=PRIMARY)
ax.spines[['top','right']].set_visible(False)
# highlight Cancelled in red note
ax.set_ylim(0, status_counts.max() * 1.15)
save(fig, 'chart5_order_status.png')

# ════════════════════════════════════════════════════════
# CHART 6 – Referral Source vs Revenue (bar)
# ════════════════════════════════════════════════════════
ref_rev = df.groupby('ReferralSource')['TotalPrice'].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(ref_rev.index, ref_rev.values, color=COLORS[:len(ref_rev)])
ax.bar_label(bars, labels=[f'₹{v/1000:.0f}K' for v in ref_rev.values], padding=3, fontsize=9)
ax.set_ylabel('Total Revenue (₹)', fontsize=11)
ax.set_title('Revenue by Referral Source', fontsize=13, fontweight='bold', color=PRIMARY)
ax.spines[['top','right']].set_visible(False)
ax.set_ylim(0, ref_rev.max() * 1.15)
save(fig, 'chart6_referral_revenue.png')

# ════════════════════════════════════════════════════════
# CHART 7 – Outliers: TotalPrice Boxplot
# ════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(6, 4))
bp = ax.boxplot(df['TotalPrice'], vert=True, patch_artist=True,
                boxprops=dict(facecolor='#d5e8d4', color=PRIMARY),
                medianprops=dict(color=ACCENT, lw=2),
                whiskerprops=dict(color=PRIMARY),
                capprops=dict(color=PRIMARY),
                flierprops=dict(marker='o', color=ACCENT, markersize=5, alpha=0.7))
ax.set_ylabel('Total Price (₹)', fontsize=11)
ax.set_title('Boxplot – TotalPrice Outlier Detection\n(IQR Method)', fontsize=12,
             fontweight='bold', color=PRIMARY)
ax.spines[['top','right']].set_visible(False)
Q1 = df['TotalPrice'].quantile(0.25)
Q3 = df['TotalPrice'].quantile(0.75)
IQR = Q3 - Q1
ax.text(1.08, Q3+1.5*IQR, f'Upper fence\n₹{Q3+1.5*IQR:.0f}', fontsize=8, color=ACCENT)
save(fig, 'chart7_outlier_boxplot.png')

# ════════════════════════════════════════════════════════
# CHART 8 – Correlation Heatmap
# ════════════════════════════════════════════════════════
import matplotlib.colors as mcolors
corr = df[['Quantity','UnitPrice','TotalPrice','ItemsInCart']].corr().round(3)
fig, ax = plt.subplots(figsize=(6, 5))
cmap = plt.cm.RdYlGn
im = ax.imshow(corr.values, cmap=cmap, vmin=-1, vmax=1)
plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=30, ha='right')
ax.set_yticklabels(corr.columns)
for i in range(len(corr)):
    for j in range(len(corr.columns)):
        ax.text(j, i, f'{corr.values[i,j]:.2f}', ha='center', va='center',
                fontsize=11, fontweight='bold',
                color='white' if abs(corr.values[i,j]) > 0.5 else 'black')
ax.set_title('Correlation Heatmap – Numeric Features', fontsize=12,
             fontweight='bold', color=PRIMARY)
save(fig, 'chart8_correlation_heatmap.png')

print("\nAll 8 charts saved successfully!")

# ── Print key insights for report ───────────────────────
Q1_tp = df['TotalPrice'].quantile(0.25)
Q3_tp = df['TotalPrice'].quantile(0.75)
IQR_tp = Q3_tp - Q1_tp
outliers = df[(df['TotalPrice'] < Q1_tp-1.5*IQR_tp) | (df['TotalPrice'] > Q3_tp+1.5*IQR_tp)]
print("\n=== KEY INSIGHTS SUMMARY ===")
print(f"Total Orders: {len(df)}")
print(f"Total Revenue: ₹{df['TotalPrice'].sum():,.2f}")
print(f"Avg Order Value (Mean): ₹{df['TotalPrice'].mean():.2f}")
print(f"Avg Order Value (Median): ₹{df['TotalPrice'].median():.2f}")
print(f"Top Product by Revenue: {df.groupby('Product')['TotalPrice'].sum().idxmax()}")
print(f"Top Referral Source: {df.groupby('ReferralSource')['TotalPrice'].sum().idxmax()}")
print(f"Cancelled Orders: {(df['OrderStatus']=='Cancelled').sum()} ({(df['OrderStatus']=='Cancelled').mean()*100:.1f}%)")
print(f"Returned Orders: {(df['OrderStatus']=='Returned').sum()} ({(df['OrderStatus']=='Returned').mean()*100:.1f}%)")
print(f"Outliers (IQR method): {len(outliers)} orders above ₹{Q3_tp+1.5*IQR_tp:.0f}")
print(f"Correlation – Quantity & TotalPrice: {df['Quantity'].corr(df['TotalPrice']):.3f}")
print(f"Correlation – UnitPrice & TotalPrice: {df['UnitPrice'].corr(df['TotalPrice']):.3f}")
