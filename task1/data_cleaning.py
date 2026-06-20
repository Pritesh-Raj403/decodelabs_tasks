"""
DecodeLabs Internship - Week 1, Task 1
Project: Data Cleaning & Preparation
-----------------------------------------------
Goal: Clean a raw e-commerce orders dataset by handling
missing values, duplicates, and incorrect data formats.

Author: Pritesh Raj
"""

import pandas as pd

# -----------------------------------------------------
# STEP 0: LOAD THE RAW DATASET
# -----------------------------------------------------
RAW_FILE = "Dataset_for_Data_Analytics_task1.xlsx"
df = pd.read_excel(RAW_FILE)

print("Original dataset shape:", df.shape)
print("\nMissing values per column (BEFORE cleaning):")
print(df.isnull().sum())

change_log = []  # to record every change made (for the PDF/markdown change log)

# -----------------------------------------------------
# PHASE 1: STRATEGIC IMPUTATION (Handle missing values)
# -----------------------------------------------------
# CouponCode has 309 missing values. A missing coupon code simply
# means "no coupon was applied" on that order, so instead of
# deleting these rows (which would lose 25% of the data), we
# impute them with a clear category label: "No Coupon".
missing_coupon_count = df["CouponCode"].isnull().sum()
df["CouponCode"] = df["CouponCode"].fillna("No Coupon")
change_log.append({
    "Change ID": "CR001",
    "Description": "Imputed missing 'CouponCode' values with 'No Coupon'",
    "Impact": f"Preserved {missing_coupon_count} records (no rows deleted)",
    "Status": "Resolved"
})

# -----------------------------------------------------
# PHASE 2: THE INTEGRITY AUDIT (Remove duplicates)
# -----------------------------------------------------
# Check for fully duplicated rows
full_dupes = df.duplicated().sum()
df = df.drop_duplicates()
change_log.append({
    "Change ID": "CR002",
    "Description": "Checked and removed fully duplicated rows",
    "Impact": f"Removed {full_dupes} duplicate row(s)",
    "Status": "Resolved"
})

# Check for duplicate OrderID (each order must be unique - "One Truth, One Record")
dup_orderid = df["OrderID"].duplicated().sum()
df = df.drop_duplicates(subset="OrderID", keep="first")
change_log.append({
    "Change ID": "CR003",
    "Description": "Verified OrderID column for duplicate unique identifiers",
    "Impact": f"Removed {dup_orderid} duplicate OrderID record(s)",
    "Status": "Resolved"
})

# -----------------------------------------------------
# PHASE 3: SPEAK ONE LANGUAGE (Correct data formats)
# -----------------------------------------------------

# 3a. Trim whitespace and standardize text case for all text columns
text_cols = ["OrderID", "CustomerID", "Product", "ShippingAddress",
             "PaymentMethod", "OrderStatus", "TrackingNumber",
             "CouponCode", "ReferralSource"]

for col in text_cols:
    before_sample = df[col].copy()
    df[col] = df[col].astype(str).str.strip()
    changed = (before_sample.astype(str) != df[col]).sum()
    if changed > 0:
        change_log.append({
            "Change ID": f"CR-WS-{col}",
            "Description": f"Trimmed leading/trailing whitespace in '{col}'",
            "Impact": f"Fixed {changed} record(s)",
            "Status": "Resolved"
        })

# 3b. Standardize Date column to ISO 8601 format (YYYY-MM-DD)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
change_log.append({
    "Change ID": "CR004",
    "Description": "Standardized 'Date' column to ISO 8601 format (YYYY-MM-DD)",
    "Impact": f"Reformatted {len(df)} record(s)",
    "Status": "Resolved"
})

# 3c. Standardize numeric precision to 2 decimal places
# (UnitPrice and TotalPrice had inconsistent decimal places: 180.5 vs 180.50)
df["UnitPrice"] = df["UnitPrice"].round(2)
df["TotalPrice"] = df["TotalPrice"].round(2)
change_log.append({
    "Change ID": "CR005",
    "Description": "Standardized 'UnitPrice' and 'TotalPrice' to 2 decimal precision",
    "Impact": f"Reformatted {len(df)} record(s)",
    "Status": "Resolved"
})

# 3d. Validate calculated field consistency: Quantity * UnitPrice should equal TotalPrice
calc_total = (df["Quantity"] * df["UnitPrice"]).round(2)
mismatch_count = (calc_total - df["TotalPrice"]).abs().gt(0.01).sum()
change_log.append({
    "Change ID": "CR006",
    "Description": "Validated TotalPrice = Quantity x UnitPrice for all records",
    "Impact": f"Found {mismatch_count} mismatch(es) after rounding correction",
    "Status": "Resolved" if mismatch_count == 0 else "Reviewed"
})

# -----------------------------------------------------
# FINAL VERIFICATION GATE (per task requirements)
# -----------------------------------------------------
final_dup_orderid = df["OrderID"].duplicated().sum()
bad_dates = (~df["Date"].astype(str).str.match(r"^\d{4}-\d{2}-\d{2}$")).sum()

print("\n================ VERIFICATION GATE ================")
print(f"Duplicate OrderIDs remaining : {final_dup_orderid}  (target: 0)")
print(f"Incorrectly formatted dates  : {bad_dates}  (target: 0)")
print(f"Remaining missing values     :\n{df.isnull().sum().sum()} total nulls")
print("=====================================================")

# -----------------------------------------------------
# SAVE CLEANED DATASET
# -----------------------------------------------------
OUTPUT_FILE = "cleaned_dataset.xlsx"
df.to_excel(OUTPUT_FILE, index=False)
print(f"\nCleaned dataset saved as: {OUTPUT_FILE}")
print("Final dataset shape:", df.shape)

# -----------------------------------------------------
# SAVE CHANGE LOG
# -----------------------------------------------------
log_df = pd.DataFrame(change_log)
log_df.to_csv("change_log.csv", index=False)
print("Change log saved as: change_log.csv")
print("\nChange Log Summary:")
print(log_df.to_string(index=False))
