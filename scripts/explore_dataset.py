"""
CareerLens - Dataset Exploration Script

Purpose:
- Inspect all raw datasets
- Display shape, columns, data types
- Calculate missing values
- Generate initial data dictionary

Author: CareerLens
"""

from pathlib import Path
import pandas as pd

RAW_DATA_PATH = Path("data/raw/linkedin_job_postings")


FILES = [
    "postings.csv",
    "companies/companies.csv",
    "jobs/job_skills.csv",
    "jobs/job_industries.csv",
    "jobs/salaries.csv",
    "mappings/skills.csv",
    "mappings/industries.csv",
]


def inspect_dataset(file_path: Path) -> None:
    """Inspect a dataset and print useful metadata."""

    print("\n" + "=" * 80)
    print(f"FILE: {file_path.name}")
    print("=" * 80)

    try:
        df = pd.read_csv(file_path)

        print(f"\nShape: {df.shape}")

        print("\nColumns:")
        for col in df.columns:
            print(f" - {col}")

        print("\nData Types:")
        print(df.dtypes)

        print("\nMissing Values:")
        missing = df.isnull().sum()

        for col, count in missing.items():
            percentage = (count / len(df)) * 100

            if count > 0:
                print(f"{col}: {count:,} missing " f"({percentage:.2f}%)")

        print("\nFirst 5 Rows:")
        print(df.head())

    except Exception as e:
        print(f"Error reading {file_path}")
        print(f"Reason: {e}")


def main():

    print("\nCareerLens Dataset Exploration\n")

    for file in FILES:
        file_path = RAW_DATA_PATH / file

        if file_path.exists():
            inspect_dataset(file_path)
        else:
            print(f"\nFile not found: {file_path}")


if __name__ == "__main__":
    main()
