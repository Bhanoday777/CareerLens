from pathlib import Path

import pandas as pd

from utils import load_csv

EXPECTED_COLUMNS = [
    "job_id",
    "company_name",
    "job_title",
    "description",
    "location",
    "posting_time",
    "experience_level",
    "experience_bucket",
    "skills",
    "skill_count",
    "industries",
    "annual_salary_usd",
    "salary_tier",
    "remote_classification",
]


def validate_duplicates(df):
    return df["job_id"].duplicated().sum()


def validate_expected_columns(df):
    missing = []

    for column in EXPECTED_COLUMNS:
        if column not in df.columns:
            missing.append(column)

    return missing


def validate_salary(df):

    salary = df["annual_salary_usd"].dropna()

    if salary.empty:
        return "No salary information available."

    return {
        "minimum": salary.min(),
        "maximum": salary.max(),
        "average": round(salary.mean(), 2),
    }


def validate_dates(df):

    invalid_dates = df["posting_time"].isna().sum()

    return invalid_dates


def validate_skill_count(df):

    invalid = (df["skill_count"] < 0).sum()

    return invalid


def validate_experience(df):

    return df["experience_bucket"].value_counts()


def generate_report(df):

    duplicate_count = validate_duplicates(df)

    missing_columns = validate_expected_columns(df)

    salary_stats = validate_salary(df)

    invalid_dates = validate_dates(df)

    invalid_skill_counts = validate_skill_count(df)

    experience_counts = validate_experience(df)

    report = []

    report.append("# CareerLens Data Quality Report\n")

    report.append(f"Total Records: {len(df)}\n")

    report.append(f"Total Columns: {len(df.columns)}\n")

    report.append(f"Duplicate Job IDs: {duplicate_count}\n")

    report.append("\n---\n")

    report.append("## Missing Values (%)\n")

    missing_pct = (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)

    for column, value in missing_pct.items():
        report.append(f"- {column}: {value:.2f}%")

    report.append("\n---\n")

    report.append("## Expected Columns\n")

    if missing_columns:
        report.append(str(missing_columns))
    else:
        report.append("All expected columns exist.")

    report.append("\n---\n")

    report.append("## Salary Statistics\n")

    report.append(str(salary_stats))

    report.append("\n---\n")

    report.append("## Invalid Posting Dates\n")

    report.append(str(invalid_dates))

    report.append("\n---\n")

    report.append("## Invalid Skill Counts\n")

    report.append(str(invalid_skill_counts))

    report.append("\n---\n")

    report.append("## Experience Bucket Distribution\n")

    report.append(experience_counts.to_string())

    report.append("\n---\n")

    report.append("## Recommendations\n")

    report.append("- Continue using salary only where available.")
    report.append("- Consider extracting technologies from descriptions in Phase 2.")
    report.append("- Missing salary values are expected in job-posting datasets.")
    report.append("- Dataset is suitable for Power BI and SQL analytics.")

    return "\n".join(report)


def main():

    print("Loading enriched dataset...")

    df = load_csv("data/processed/jobs_enriched.csv")

    print(f"Dataset Shape: {df.shape}")

    report = generate_report(df)

    report_path = Path("reports/data_quality_report.md")

    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print("\nValidation Complete.")

    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
