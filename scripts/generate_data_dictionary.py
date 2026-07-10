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


all_metadata = []

for file in FILES:

    file_path = RAW_DATA_PATH / file

    if not file_path.exists():
        continue

    df = pd.read_csv(file_path)

    for col in df.columns:

        all_metadata.append(
            {
                "dataset": file,
                "column_name": col,
                "data_type": str(df[col].dtype),
                "null_count": int(df[col].isnull().sum()),
                "null_percentage": round((df[col].isnull().sum() / len(df)) * 100, 2),
            }
        )

dictionary_df = pd.DataFrame(all_metadata)

output_path = Path("reports/data_dictionary.csv")

output_path.parent.mkdir(parents=True, exist_ok=True)

dictionary_df.to_csv(output_path, index=False)

print(f"Data dictionary saved to: {output_path}")
