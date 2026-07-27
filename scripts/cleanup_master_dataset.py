from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent

MASTER_DATASET = ROOT_DIR / "data" / "processed" / "master_jobs.csv"

df = pd.read_csv(MASTER_DATASET)

duplicate_columns = [
        "pay_period_salary",
    "currency_salary",
    "compensation_type_salary",
    "min_salary_salary",
    "med_salary_salary",
    "max_salary_salary",
    "work_type",

]

existing_columns = [
    col for col in duplicate_columns
    if col in df.columns
]

df.drop(columns=existing_columns, inplace=True)

df.to_csv(MASTER_DATASET, index=False)

print("=" * 60)
print("Dataset cleaned successfully.")
print(f"Removed {len(existing_columns)} duplicate columns.")
print(f"Remaining columns: {len(df.columns)}")
print("=" * 60)