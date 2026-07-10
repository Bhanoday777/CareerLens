from pathlib import Path

from numpy import rint
import pandas as pd

from utils import load_csv, save_csv

RAW_PATH = Path("data/raw/linkedin_job_postings")

PROCESSED_PATH = Path("data/processed")


def load_datasets():

    postings = load_csv(RAW_PATH / "postings.csv")

    job_skills = load_csv(RAW_PATH / "jobs/job_skills.csv")

    skills = load_csv(RAW_PATH / "mappings/skills.csv")

    job_industries = load_csv(RAW_PATH / "jobs/job_industries.csv")

    industries = load_csv(RAW_PATH / "mappings/industries.csv")

    salaries = load_csv(RAW_PATH / "jobs/salaries.csv")

    return (postings, job_skills, skills, job_industries, industries, salaries)


def build_skills_dataset(job_skills, skills):

    print("Building skills dataset...")

    skills_df = job_skills.merge(skills, on="skill_abr", how="left")

    skills_aggregated = (
        skills_df.groupby("job_id")["skill_name"]
        .apply(lambda x: ",".join(sorted(set(x.dropna()))))
        .reset_index()
    )

    skills_aggregated.rename(columns={"skill_name": "skills"}, inplace=True)

    print(f"Skills dataset shape: {skills_aggregated.shape}")

    return skills_aggregated


def build_industries_dataset(job_industries, industries):

    print("Building industries dataset...")

    industries_df = job_industries.merge(industries, on="industry_id", how="left")

    industries_aggregated = (
        industries_df.groupby("job_id")["industry_name"]
        .apply(lambda x: ",".join(sorted(set(x.dropna()))))
        .reset_index()
    )

    industries_aggregated.rename(columns={"industry_name": "industries"}, inplace=True)

    print(f"Industries dataset shape: {industries_aggregated.shape}")

    return industries_aggregated


def build_master_dataset(postings, skills_aggregated, industries_aggregated, salaries):

    print("Building master dataset...")

    master_df = postings.merge(skills_aggregated, on="job_id", how="left")

    master_df = master_df.merge(industries_aggregated, on="job_id", how="left")

    master_df = master_df.merge(
        salaries, on="job_id", how="left", suffixes=("", "_salary")
    )

    print(f"Master dataset shape: {master_df.shape}")

    return master_df


def main():

    print("Loading datasets...")

    postings, job_skills, skills, job_industries, industries, salaries = load_datasets()

    print("Datasets loaded successfully.")

    print(postings.shape)
    print(job_skills.shape)
    print(skills.shape)
    print(job_industries.shape)
    print(industries.shape)
    print(salaries.shape)

    skills_aggregated = build_skills_dataset(job_skills, skills)

    print(skills_aggregated.head())

    industries_aggregated = build_industries_dataset(job_industries, industries)
    print(industries_aggregated.head())

    master_df = build_master_dataset(
        postings, skills_aggregated, industries_aggregated, salaries
    )

    print(master_df.head())
    save_csv(master_df, "data/processed/master_jobs_raw.csv")
    print("\nMASTER DATASET COLUMNS:\n")
    print(master_df.columns.tolist())
    print("\nDuplicate job_id count:")
    print(master_df["job_id"].duplicated().sum())

    print("\nUnique job_ids:")
    print(master_df["job_id"].nunique())

    print("\nDataset shape:")
    print(master_df.shape)


if __name__ == "__main__":
    main()
