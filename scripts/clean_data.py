from utils import load_csv, save_csv
import pandas as pd


def main():

    print("Loading master dataset...")

    df = load_csv("data/processed/master_jobs_raw.csv")

    print(f"Initial Shape: {df.shape}")

    print("Cleaning started...")

    # ==================================================
    # Remove Duplicate Jobs
    # ==================================================

    initial_rows = len(df)

    df.drop_duplicates(subset=["job_id"], inplace=True)

    duplicates_removed = initial_rows - len(df)

    print(f"Duplicates Removed: {duplicates_removed}")

    # ==================================================
    # Fill Missing Values
    # ==================================================

    df["company_name"] = df["company_name"].fillna("Unknown Company")

    df["description"] = df["description"].fillna("No Description Available")

    df["skills"] = df["skills"].fillna("Not Specified")

    df["industries"] = df["industries"].fillna("Unknown Industry")

    df["views"] = df["views"].fillna(0)

    df["applies"] = df["applies"].fillna(0)

    df["formatted_experience_level"] = df["formatted_experience_level"].fillna(
        "Not Specified"
    )

    df["remote_allowed"] = df["remote_allowed"].fillna(False)

    # ==================================================
    # Salary Standardization
    # ==================================================

    df["salary_max"] = df["max_salary_salary"].fillna(df["max_salary"])

    df["salary_min"] = df["min_salary_salary"].fillna(df["min_salary"])

    df["salary_median"] = df["med_salary_salary"].fillna(df["med_salary"])

    # ==================================================
    # Unified Salary Field
    # ==================================================

    df["annual_salary_usd"] = (
        df["salary_median"].fillna(df["salary_max"]).fillna(df["salary_min"])
    )

    # ==================================================
    # Rename Columns
    # ==================================================

    df.rename(
        columns={
            "title": "job_title",
            "formatted_work_type": "work_type_standardized",
            "formatted_experience_level": "experience_level",
            "listed_time": "posting_time",
        },
        inplace=True,
    )

    # ==================================================
    # Date Conversion
    # ==================================================

    df["posting_time"] = pd.to_datetime(df["posting_time"], unit="ms", errors="coerce")

    df["original_listed_time"] = pd.to_datetime(
        df["original_listed_time"], unit="ms", errors="coerce"
    )

    # ==================================================
    # Drop Unnecessary Columns
    # ==================================================

    columns_to_drop = [
        "salary_id",
        "job_posting_url",
        "application_url",
        "posting_domain",
        "zip_code",
        "fips",
        "closed_time",
        "expiry",
        "max_salary",
        "min_salary",
        "med_salary",
        "max_salary_salary",
        "min_salary_salary",
        "med_salary_salary",
    ]

    df.drop(columns=columns_to_drop, inplace=True, errors="ignore")

    print("Cleaning completed.")

    # ==================================================
    # Save Clean Dataset
    # ==================================================

    save_csv(df, "data/processed/jobs_cleaned.csv")

    # ==================================================
    # Validation Output
    # ==================================================

    print("\nFinal Shape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nDuplicate job_ids:")
    print(df["job_id"].duplicated().sum())

    print("\nMissing Values (%):")

    missing_pct = df.isnull().sum() / len(df) * 100

    print(missing_pct.sort_values(ascending=False).head(15))
    print("\nPosting Time Sample:")
    print(df["posting_time"].head())

    print("\nOriginal Listed Time Sample:")
    print(df["original_listed_time"].head())


if __name__ == "__main__":
    main()
