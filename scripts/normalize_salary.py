"""
CareerLens
-----------

Normalize salary values to annual USD.

Creates a new column:

    annual_salary_usd

without modifying the original
normalized_salary column.
"""

from pathlib import Path
import pandas as pd

# ==========================================================
# PATHS
# ==========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

MASTER_DATASET = ROOT_DIR / "data" / "processed" / "master_jobs.csv"

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_csv(MASTER_DATASET)

# ==========================================================
# CREATE NEW COLUMN
# ==========================================================

df["annual_salary_usd"] = pd.NA

# ==========================================================
# KEEP ONLY USD SALARIES
# ==========================================================

usd_mask = (
    df["currency"] == "USD"
) & (
    df["normalized_salary"].notna()
)

salary_df = df.loc[usd_mask].copy()

# ==========================================================
# CONVERT TO YEARLY SALARY
# ==========================================================

def convert_to_annual(row):

    salary = row["normalized_salary"]
    period = row["pay_period"]

    if period == "YEARLY":
        return salary

    elif period == "MONTHLY":
        return salary * 12

    elif period == "WEEKLY":
        return salary * 52

    elif period == "BIWEEKLY":
        return salary * 26

    elif period == "HOURLY":
        return salary * 2080

    return pd.NA


salary_df["annual_salary_usd"] = salary_df.apply(
    convert_to_annual,
    axis=1
)

# ==========================================================
# COPY BACK
# ==========================================================

df.loc[
    salary_df.index,
    "annual_salary_usd"
] = salary_df["annual_salary_usd"]

# ==========================================================
# SAVE
# ==========================================================

df.to_csv(
    MASTER_DATASET,
    index=False
)

# ==========================================================
# SUMMARY
# ==========================================================

print("=" * 60)

print("Salary normalization complete.")

print()

print(f"Rows             : {len(df):,}")

print(
    f"Annual Salaries  : {df['annual_salary_usd'].notna().sum():,}"
)

print(
    f"Missing Salaries : {df['annual_salary_usd'].isna().sum():,}"
)

print("=" * 60)