"""
CareerLens - Business Intelligence Analysis

Phase 2

Generates KPIs and business insights from the
processed jobs dataset.

Author: CareerLens
Python Version: 3.14
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from analytics_utils import (
    load_dataset,
    validate_dataframe,
)

from config import (
    ANALYTICS_SUMMARY_FILE,
    BUSINESS_REPORT,
    INPUT_DATASET,
    TOP_ENTITIES_FILE,
)

from logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# DATA CLASSES
# ==========================================================


@dataclass(slots=True)
class BusinessKPIs:
    """
    Overall Business KPIs.
    """

    total_jobs: int
    unique_companies: int
    unique_industries: int
    unique_locations: int
    unique_skills: int

    average_salary: float
    median_salary: float

    average_skill_count: float
    average_job_age: float

    remote_percentage: float
    hybrid_percentage: float
    onsite_percentage: float


@dataclass(slots=True)
class BusinessAnalysisResult:
    """
    Stores complete business analysis.
    """

    kpis: BusinessKPIs

    top_companies: pd.DataFrame
    top_locations: pd.DataFrame
    top_industries: pd.DataFrame
    top_job_titles: pd.DataFrame
    top_skills: pd.DataFrame

    salary_by_experience: pd.DataFrame
    salary_by_location: pd.DataFrame
    salary_by_industry: pd.DataFrame
    salary_by_remote: pd.DataFrame
    
    
    highest_paying_companies: pd.DataFrame
    highest_paying_industries: pd.DataFrame
    highest_paying_locations: pd.DataFrame
    

    experience_distribution: pd.DataFrame
    remote_distribution: pd.DataFrame
    salary_tier_distribution: pd.DataFrame

    hiring_monthly: pd.DataFrame
    hiring_yearly: pd.DataFrame


# ==========================================================
# BUSINESS ANALYSIS
# ==========================================================


class BusinessAnalysis:

    def __init__(
        self,
        dataset_path: Path = INPUT_DATASET,
    ) -> None:

        self.dataset_path = dataset_path
        self.df: pd.DataFrame | None = None

    # ------------------------------------------------------

    def load_dataset(self) -> None:

        logger.info("Loading dataset...")

        self.df = load_dataset(self.dataset_path)

        validate_dataframe(self.df)

        logger.info("Dataset loaded successfully.")

    # ------------------------------------------------------

    @staticmethod
    def percentage(
        count: int,
        total: int,
    ) -> float:

        if total == 0:
            return 0.0

        return round(
            (count / total) * 100,
            2,
        )

    # ------------------------------------------------------
    def salary_dataframe(self) -> pd.DataFrame:
        """
        Return only rows with valid salary information.
        """

        if self.df is None:
            raise RuntimeError("Dataset not loaded.")

        return self.df.dropna(
            subset=["annual_salary_usd"]
        )

    def calculate_kpis(
        self,
    ) -> BusinessKPIs:

        if self.df is None:
            raise RuntimeError("Dataset not loaded.")

        df = self.df

        total_jobs = len(df)

        unique_companies = df["company_name"].nunique()

        unique_industries = df["industries"].nunique()

        unique_locations = df["location"].nunique()

        unique_skills = (
            df["skills"]
            .fillna("")
            .str.split(",")
            .explode()
            .str.strip()
            .replace("", pd.NA)
            .dropna()
            .nunique()
        )

        average_salary = round(
            df["annual_salary_usd"].mean(),
            2,
        )

        median_salary = round(
            df["annual_salary_usd"].median(),
            2,
        )

        average_skill_count = round(
            df["skill_count"].mean(),
            2,
        )

        average_job_age = round(
            df["job_age_days"].mean(),
            2,
        )

        remote_distribution = df["remote_classification"].value_counts()

        remote_percentage = self.percentage(
            remote_distribution.get(
                "Remote",
                0,
            ),
            total_jobs,
        )

        hybrid_percentage = self.percentage(
            remote_distribution.get(
                "Hybrid",
                0,
            ),
            total_jobs,
        )

        onsite_percentage = self.percentage(
            remote_distribution.get(
                "Onsite",
                0,
            ),
            total_jobs,
        )

        logger.info("Business KPIs calculated.")

        return BusinessKPIs(
            total_jobs=total_jobs,
            unique_companies=unique_companies,
            unique_industries=unique_industries,
            unique_locations=unique_locations,
            unique_skills=unique_skills,
            average_salary=average_salary,
            median_salary=median_salary,
            average_skill_count=average_skill_count,
            average_job_age=average_job_age,
            remote_percentage=remote_percentage,
            hybrid_percentage=hybrid_percentage,
            onsite_percentage=onsite_percentage,
        )

        # ------------------------------------------------------

    # TOP HIRING COMPANIES
    # ------------------------------------------------------

    def top_hiring_companies(
        self,
        top_n: int = 10,
    ) -> pd.DataFrame:

        return (
            self.df["company_name"]
            .value_counts()
            .head(top_n)
            .rename_axis("Company")
            .reset_index(name="Hiring Count")
        )

    # ------------------------------------------------------
    # TOP HIRING LOCATIONS
    # ------------------------------------------------------

    def top_hiring_locations(
        self,
        top_n: int = 10,
    ) -> pd.DataFrame:

        return (
            self.df["location"]
            .value_counts()
            .head(top_n)
            .rename_axis("Location")
            .reset_index(name="Hiring Count")
        )

    # ------------------------------------------------------
    # TOP INDUSTRIES
    # ------------------------------------------------------

    def top_industries(
        self,
        top_n: int = 10,
    ) -> pd.DataFrame:

        return (
            self.df["industries"]
            .value_counts()
            .head(top_n)
            .rename_axis("Industry")
            .reset_index(name="Hiring Count")
        )

    # ------------------------------------------------------
    # TOP JOB TITLES
    # ------------------------------------------------------

    def top_job_titles(
        self,
        top_n: int = 10,
    ) -> pd.DataFrame:

        return (
            self.df["job_title"]
            .value_counts()
            .head(top_n)
            .rename_axis("Job Title")
            .reset_index(name="Count")
        )

    # ------------------------------------------------------
    # EXPERIENCE DISTRIBUTION
    # ------------------------------------------------------

    def experience_distribution(
        self,
    ) -> pd.DataFrame:

        return (
            self.df["experience_bucket"]
            .value_counts()
            .rename_axis("Experience")
            .reset_index(name="Count")
        )

    # ------------------------------------------------------
    # REMOTE DISTRIBUTION
    # ------------------------------------------------------

    def remote_distribution(
        self,
    ) -> pd.DataFrame:

        return (
            self.df["remote_classification"]
            .value_counts()
            .rename_axis("Remote Type")
            .reset_index(name="Count")
        )

    # ------------------------------------------------------
    # SALARY TIER DISTRIBUTION
    # ------------------------------------------------------

    def salary_tier_distribution(
        self,
    ) -> pd.DataFrame:

        return (
            self.df["salary_tier"]
            .value_counts()
            .rename_axis("Salary Tier")
            .reset_index(name="Count")
        )

    # ------------------------------------------------------
    # AVERAGE SALARY BY EXPERIENCE
    # ------------------------------------------------------

    def salary_by_experience(
        self,
    ) -> pd.DataFrame:

        salary_df = self.df.dropna(
        subset=["annual_salary_usd"]
        )

        return (
        salary_df.groupby(
        "experience_bucket"
    )["annual_salary_usd"]
    .mean()
    .round(2)
    .reset_index(name="Average Salary")
    .sort_values(
        by="Average Salary",
        ascending=False,
    )
)

    # ------------------------------------------------------
    # AVERAGE SALARY BY LOCATION
    # ------------------------------------------------------

    def salary_by_location(
    self,
    ) -> pd.DataFrame:

        salary_df = self.salary_dataframe()

        salary_df = self.df.dropna(
        subset=["annual_salary_usd"]
        )

        return (
        salary_df.groupby(
        "location"
    )["annual_salary_usd"]
    .mean()
    .round(2)
    .reset_index(name="Average Salary")
    .sort_values(
        by="Average Salary",
        ascending=False,
    )
)

    # ------------------------------------------------------
    # AVERAGE SALARY BY INDUSTRY
    # ------------------------------------------------------

    def salary_by_industry(
        self,
    ) -> pd.DataFrame:

        salary_df = self.df.dropna(
        subset=["annual_salary_usd"]
        )

        return (
    salary_df.groupby(
        "industries"
    )["annual_salary_usd"]
    .mean()
    .round(2)
    .reset_index(name="Average Salary")
    .sort_values(
        by="Average Salary",
        ascending=False,
    )
)

    # ------------------------------------------------------
    # AVERAGE SALARY BY REMOTE TYPE
    # ------------------------------------------------------

    def salary_by_remote(
        self,
    ) -> pd.DataFrame:
        
        salary_df = self.df.dropna(
        subset=["annual_salary_usd"]
    )

        return (
    salary_df.groupby(
        "remote_classification"
    )["annual_salary_usd"]
    .mean()
    .round(2)
    .reset_index(name="Average Salary")
    .sort_values(
        by="Average Salary",
        ascending=False,
    )
)

    # ------------------------------------------------------
    # HIGHEST PAYING COMPANIES
    # ------------------------------------------------------

    def highest_paying_companies(
        self,
        top_n: int = 10,
    ) -> pd.DataFrame:

        salary_df = self.df.dropna(
            subset=["annual_salary_usd"]
        )

        return (
            salary_df.groupby("company_name")["annual_salary_usd"]
            .mean()
            .round(2)
            .reset_index(name="Average Salary")
            .sort_values(
                by="Average Salary",
                ascending=False,
            )
            .head(top_n)
        )

    # ------------------------------------------------------
    # HIGHEST PAYING INDUSTRIES
    # ------------------------------------------------------

    def highest_paying_industries(
        self,
        top_n: int = 10,
    ) -> pd.DataFrame:

        return (
            self.df.groupby("industries")["annual_salary_usd"]
            .mean()
            .round(2)
            .reset_index(name="Average Salary")
            .sort_values(
                by="Average Salary",
                ascending=False,
            )
            .head(top_n)
        )

    # ------------------------------------------------------
    # HIGHEST PAYING LOCATIONS
    # ------------------------------------------------------

    def highest_paying_locations(
        self,
        top_n: int = 10,
    ) -> pd.DataFrame:

        return (
            self.df.groupby("location")["annual_salary_usd"]
            .mean()
            .round(2)
            .reset_index(name="Average Salary")
            .sort_values(
                by="Average Salary",
                ascending=False,
            )
            .head(top_n)
        )

    # ------------------------------------------------------
    # MONTHLY HIRING TREND
    # ------------------------------------------------------

    def monthly_hiring_trend(
        self,
    ) -> pd.DataFrame:

        return (
            self.df.groupby("posting_month")
            .size()
            .reset_index(name="Jobs")
            .sort_values(by="posting_month")
        )

    # ------------------------------------------------------
    # YEARLY HIRING TREND
    # ------------------------------------------------------

    def yearly_hiring_trend(
        self,
    ) -> pd.DataFrame:

        return (
            self.df.groupby("posting_year")
            .size()
            .reset_index(name="Jobs")
            .sort_values(by="posting_year")
        )

    # ------------------------------------------------------
    # MOST COMMON SKILLS
    # ------------------------------------------------------

    def top_skills(
        self,
        top_n: int = 20,
    ) -> pd.DataFrame:

        skills = self.df["skills"].fillna("").str.split(",").explode().str.strip()

        return (
            skills.value_counts()
            .head(top_n)
            .rename_axis("Skill")
            .reset_index(name="Frequency")
        )

    # ------------------------------------------------------
    # COMPLETE ANALYSIS
    # ------------------------------------------------------

    def analyze(
        self,
    ) -> BusinessAnalysisResult:

        logger.info("Running Business Intelligence analysis...")

        results = BusinessAnalysisResult(
            kpis=self.calculate_kpis(),
            top_companies=self.top_hiring_companies(),
            top_locations=self.top_hiring_locations(),
            top_industries=self.top_industries(),
            top_job_titles=self.top_job_titles(),
            top_skills=self.top_skills(),
            salary_by_experience=self.salary_by_experience(),
            salary_by_location=self.salary_by_location(),
            salary_by_industry=self.salary_by_industry(),
            salary_by_remote=self.salary_by_remote(),
            highest_paying_companies=self.highest_paying_companies(),
            highest_paying_industries=self.highest_paying_industries(),
            highest_paying_locations=self.highest_paying_locations(),
            experience_distribution=self.experience_distribution(),
            remote_distribution=self.remote_distribution(),
            salary_tier_distribution=self.salary_tier_distribution(),
            hiring_monthly=self.monthly_hiring_trend(),
            hiring_yearly=self.yearly_hiring_trend(),
        )

        logger.info("Business analysis completed successfully.")

        return results


        # ------------------------------------------------------
    # EXPORT ANALYTICS SUMMARY
    # ------------------------------------------------------

    def export_analytics_summary(
        self,
        results: BusinessAnalysisResult,
    ) -> None:

        summary = pd.DataFrame(
            {
                "Company": results.top_companies["Company"],
                "Hiring Count": results.top_companies["Hiring Count"],
            }
        )

        summary.to_csv(
            ANALYTICS_SUMMARY_FILE,
            index=False,
        )

        logger.info(
            "analytics_summary.csv exported."
        )

    # ------------------------------------------------------
    # EXPORT TOP ENTITIES
    # ------------------------------------------------------

    def export_top_entities(
        self,
        results: BusinessAnalysisResult,
    ) -> None:

        entities = []

        for _, row in results.top_companies.iterrows():
            entities.append(
                {
                    "Category": "Company",
                    "Entity": row["Company"],
                    "Count": row["Hiring Count"],
                }
            )

        for _, row in results.top_industries.iterrows():
            entities.append(
                {
                    "Category": "Industry",
                    "Entity": row["Industry"],
                    "Count": row["Hiring Count"],
                }
            )

        for _, row in results.top_locations.iterrows():
            entities.append(
                {
                    "Category": "Location",
                    "Entity": row["Location"],
                    "Count": row["Hiring Count"],
                }
            )

        for _, row in results.top_skills.iterrows():
            entities.append(
                {
                    "Category": "Skill",
                    "Entity": row["Skill"],
                    "Count": row["Frequency"],
                }
            )

        pd.DataFrame(
            entities
        ).to_csv(
            TOP_ENTITIES_FILE,
            index=False,
        )

        logger.info(
            "top_entities.csv exported."
        )

    # ------------------------------------------------------
    # GENERATE REPORT
    # ------------------------------------------------------

    def generate_report(
        self,
        results: BusinessAnalysisResult,
    ) -> str:

        report = []

        report.append(
            "# Business Intelligence Report\n"
        )

        report.append(
            "## Executive KPIs\n"
        )

        kpi = results.kpis

        report.extend(
            [
                f"- Total Jobs: {kpi.total_jobs}",
                f"- Unique Companies: {kpi.unique_companies}",
                f"- Unique Industries: {kpi.unique_industries}",
                f"- Unique Locations: {kpi.unique_locations}",
                f"- Average Salary: ${kpi.average_salary:,.2f}",
                f"- Median Salary: ${kpi.median_salary:,.2f}",
                f"- Remote Jobs: {kpi.remote_percentage}%",
                f"- Hybrid Jobs: {kpi.hybrid_percentage}%",
                f"- Onsite Jobs: {kpi.onsite_percentage}%",
                "",
            ]
        )

        report.append(
            "## Top Hiring Companies\n"
        )

        report.append(
            results.top_companies.to_markdown(
                index=False
            )
        )

        report.append("\n")

        report.append(
            "## Highest Paying Companies\n"
        )

        report.append(
            results.highest_paying_companies.to_markdown(
                index=False
            )
        )

        report.append("\n")

        report.append(
            "## Top Industries\n"
        )

        report.append(
            results.top_industries.to_markdown(
                index=False
            )
        )

        report.append("\n")

        report.append(
            "## Highest Paying Industries\n"
        )

        report.append(
            results.highest_paying_industries.to_markdown(
                index=False
            )
        )

        report.append("\n")

        report.append(
            "## Top Locations\n"
        )

        report.append(
            results.top_locations.to_markdown(
                index=False
            )
        )

        report.append("\n")

        report.append(
            "## Highest Paying Locations\n"
        )

        report.append(
            results.highest_paying_locations.to_markdown(
                index=False
            )
        )

        report.append("\n")

        report.append(
            "## Top Skills\n"
        )

        report.append(
            results.top_skills.to_markdown(
                index=False
            )
        )

        report.append("\n")

        report.append(
            "## Monthly Hiring Trend\n"
        )

        report.append(
            results.hiring_monthly.to_markdown(
                index=False
            )
        )

        return "\n".join(report)

    # ------------------------------------------------------
    # EXECUTE
    # ------------------------------------------------------

    def execute(self) -> None:

        logger.info("=" * 60)
        logger.info("Starting Business Analysis")
        logger.info("=" * 60)

        self.load_dataset()

        results = self.analyze()

        self.export_analytics_summary(
            results
        )

        self.export_top_entities(
            results
        )

        report = self.generate_report(
            results
        )

        with open(
            BUSINESS_REPORT,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(report)

        logger.info(
            "Business report generated."
        )

        logger.info("=" * 60)
        logger.info("Business Analysis Completed")
        logger.info("=" * 60)


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:

    try:

        analysis = BusinessAnalysis()

        analysis.execute()

    except Exception:

        logger.exception(
            "Business Analysis Failed."
        )

        raise


if __name__ == "__main__":
    main()