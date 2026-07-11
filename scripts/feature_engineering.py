import pandas as pd

from utils import load_csv, save_csv


def create_skill_count(df):
    """
    Count number of skills per job posting.
    """

    df["skill_count"] = df["skills"].apply(
        lambda x: len(str(x).split(",")) if pd.notna(x) and x != "Not Specified" else 0
    )

    return df


def create_posting_features(df):
    """
    Create posting year and month.
    """

    df["posting_year"] = df["posting_time"].dt.year

    df["posting_month"] = df["posting_time"].dt.strftime("%Y-%m")

    return df


def create_experience_bucket(df):
    """
    Convert experience levels into buckets.
    """

    experience_map = {
        "Internship": "Entry Level",
        "Entry level": "Entry Level",
        "Associate": "Mid Level",
        "Mid-Senior level": "Senior Level",
        "Director": "Lead Level",
        "Executive": "Lead Level",
        "Not Specified": "Unknown",
    }

    df["experience_bucket"] = df["experience_level"].map(experience_map).fillna("Other")

    return df


def create_remote_classification(df):
    """
    Classify jobs as Remote, Hybrid, or Onsite.
    """

    def classify(row):

        remote = str(row["remote_allowed"]).strip().lower()

        if remote in ["1", "1.0", "true", "yes"]:
            return "Remote"

        work_type = str(row["work_type"]).lower()

        if "hybrid" in work_type:
            return "Hybrid"

        return "Onsite"

    df["remote_classification"] = df.apply(classify, axis=1)

    return df


def create_salary_tier(df):
    """
    Create salary tiers using quartiles.
    """

    salary_series = df["annual_salary_usd"].dropna()

    if len(salary_series) == 0:

        df["salary_tier"] = "Unknown"

        return df

    q1 = salary_series.quantile(0.25)
    q2 = salary_series.quantile(0.50)
    q3 = salary_series.quantile(0.75)

    def classify_salary(value):

        if pd.isna(value):
            return "Unknown"

        if value <= q1:
            return "Low"

        if value <= q2:
            return "Medium"

        if value <= q3:
            return "High"

        return "Premium"

    df["salary_tier"] = df["annual_salary_usd"].apply(classify_salary)

    return df


def create_job_age(df):
    """
    Calculate age of job posting in days.
    """

    reference_date = df["posting_time"].max()

    df["job_age_days"] = (reference_date - df["posting_time"]).dt.days

    return df


def main():

    print("Loading cleaned dataset...")

    df = load_csv("data/processed/jobs_cleaned.csv")

    print(f"Initial Shape: {df.shape}")

    # -----------------------------------
    # Ensure datetime columns
    # -----------------------------------

    df["posting_time"] = pd.to_datetime(df["posting_time"], errors="coerce")

    # -----------------------------------
    # Feature Engineering
    # -----------------------------------

    df = create_skill_count(df)

    df = create_posting_features(df)

    df = create_experience_bucket(df)

    df = create_remote_classification(df)

    df = create_salary_tier(df)

    df = create_job_age(df)

    print("Feature engineering completed.")

    save_csv(df, "data/processed/jobs_enriched.csv")

    print("\nFinal Shape:")
    print(df.shape)

    print("\nNew Columns Created:")

    engineered_columns = [
        "skill_count",
        "posting_year",
        "posting_month",
        "experience_bucket",
        "remote_classification",
        "salary_tier",
        "job_age_days",
    ]

    print(engineered_columns)

    print("\nSample Output:")

    print(df[engineered_columns].head())


if __name__ == "__main__":
    main()
