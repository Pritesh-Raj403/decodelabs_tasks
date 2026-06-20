# Task 1 – Data Cleaning & Preparation

**Internship:** DecodeLabs Industrial Training Kit (Data Analytics Track)
**Week:** 1
**Author:** Pritesh Raj

## 📌 Goal
Clean a raw e-commerce orders dataset by handling missing values, duplicates, and incorrect data formats, while documenting every change made.

## 📂 Files in this Folder
| File | Description |
|------|--------------|
| `Dataset_for_Data_Analytics_task1.xlsx` | Original raw dataset provided (1200 rows, 14 columns) |
| `data_cleaning.py` | Python script that performs the full cleaning pipeline |
| `generate_change_log_pdf.py` | Script that converts the change log into a formatted PDF report |
| `cleaned_dataset.xlsx` | Final cleaned dataset (output) |
| `change_log.csv` | Raw change log data (output) |
| `Change_Log_Report.pdf` | Formatted PDF report of all changes made (output) |

## 🔍 Issues Identified in the Raw Dataset
1. **Missing values** – 309 records (25.75%) had a blank `CouponCode`.
2. **Inconsistent date format** – `Date` column needed standardization to ISO 8601 (`YYYY-MM-DD`).
3. **Inconsistent numeric precision** – `UnitPrice` and `TotalPrice` had varying decimal places (e.g. `180.5` instead of `180.50`).
4. **Duplicate check** – Verified the dataset for fully duplicated rows and duplicate `OrderID` values (none were found, confirming data integrity at the identifier level).

## 🛠️ Cleaning Approach
The cleaning was performed in 3 phases, following industry best practice:

1. **Strategic Imputation** – Missing `CouponCode` values were filled with `"No Coupon"` instead of being deleted, preserving all 309 records (avoiding the loss of statistical power that listwise deletion would cause).
2. **Integrity Audit** – Checked for duplicate rows and duplicate `OrderID`s to ensure "One Truth, One Record".
3. **Standardization** – Trimmed whitespace, standardized dates to ISO 8601, and rounded all monetary fields to 2 decimal places. Also validated that `Quantity × UnitPrice = TotalPrice` for every record.

## ✅ Verification Gate Results
| Metric | Result |
|--------|--------|
| Duplicate Unique Identifiers (OrderID) | 0 |
| Incorrectly Formatted Dates | 0 |
| Remaining Missing/Null Values | 0 |
| Records Before Cleaning | 1200 |
| Records After Cleaning | 1200 |

## ▶️ How to Run
```bash
pip install pandas openpyxl reportlab
python data_cleaning.py
python generate_change_log_pdf.py
```

## 🧰 Tools Used
Python, Pandas, OpenPyXL, ReportLab
