"""
CareerLens

Power BI Dataset Export

Phase 2

Creates a Power BI ready dataset together with
a dimensional star schema.

Author: CareerLens
Python Version: 3.14
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from analytics_utils import (
    load_dataset,
    save_csv,
    validate_dataframe,
)

from config import (
    INPUT_DATASET,
    POWERBI_DATASET_FILE,
    DIM_COMPANY_FILE,
    DIM_LOCATION_FILE,
    DIM_INDUSTRY_FILE,
    DIM_SKILL_FILE,
    FACT_JOBS_FILE,
    BRIDGE_JOB_SKILL_FILE,
)

from logger import get_logger

logger = get_logger(__name__)


class PowerBIExporter:
    """
    Generates Power BI datasets.
    """

    def __init__(
        self,
        dataset_path: Path = INPUT_DATASET,
    ) -> None:

        self.dataset_path = dataset_path

        self.df: pd.DataFrame | None = None

    # ==========================================================
    # LOAD DATASET
    # ==========================================================

    def load_dataset(self) -> None:

        logger.info(
            "Loading dataset..."
        )

        self.df = load_dataset(
            self.dataset_path
        )

        validate_dataframe(
            self.df
        )

        logger.info(
            "Dataset loaded successfully."
        )

        save_csv(self.df, POWERBI_DATASET_FILE)

    # ==========================================================
    # UNIQUE ID
    # ==========================================================

    @staticmethod
    def create_dimension(
        dataframe: pd.DataFrame,
        column: str,
        id_name: str,
    ) -> pd.DataFrame:
        """
        Create a dimension table.
        """

        dimension = (
            dataframe[[column]]
            .drop_duplicates()
            .sort_values(column)
            .reset_index(drop=True)
        )

        dimension.insert(
            0,
            id_name,
            range(
                1,
                len(dimension) + 1,
            ),
        )

        return dimension
    
        # ==========================================================
    # COMPANY DIMENSION
    # ==========================================================

    def create_company_dimension(
        self,
    ) -> pd.DataFrame:

        return self.create_dimension(
            self.df,
            "company_name",
            "company_id",
        )

    # ==========================================================
    # LOCATION DIMENSION
    # ==========================================================

    def create_location_dimension(
        self,
    ) -> pd.DataFrame:

        return self.create_dimension(
            self.df,
            "location",
            "location_id",
        )

    # ==========================================================
    # INDUSTRY DIMENSION
    # ==========================================================

    def create_industry_dimension(
        self,
    ) -> pd.DataFrame:

        return self.create_dimension(
            self.df,
            "industries",
            "industry_id",
        )

    # ==========================================================
    # SKILL DIMENSION
    # ==========================================================

    def create_skill_dimension(
        self,
    ) -> pd.DataFrame:

        skills = (
            self.df["skills"]
            .fillna("")
            .str.split(",")
            .explode()
            .str.strip()
        )

        skills = (
            skills[skills != ""]
            .drop_duplicates()
            .sort_values()
            .reset_index(drop=True)
        )

        dimension = pd.DataFrame(
            {
                "skill_id": range(
                    1,
                    len(skills) + 1,
                ),
                "skill": skills,
            }
        )

        return dimension
    
    
    # ==========================================================
# BRIDGE JOB SKILL
# ==========================================================

    def create_bridge_job_skill(
        self,
        skill_dim: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Create bridge table between jobs and skills.
        """

        skill_lookup = dict(
        zip(
            skill_dim["skill"],
            skill_dim["skill_id"],
        )
        )

        records = []

        for _, row in self.df.iterrows():

            job_id = row["job_id"]

            skills = str(
                row["skills"]
            ).split(",")

            for skill in skills:

                skill = skill.strip()

                if skill == "" or skill.lower() == "nan":
                    continue

                records.append(
                    {
                    "job_id": job_id,
                    "skill_id": skill_lookup[skill],
                    }
            )

        bridge = (
            pd.DataFrame(records)
            .drop_duplicates()
            .reset_index(drop=True)
            )

        return bridge

    # ==========================================================
    # FACT TABLE
    # ==========================================================

    def create_fact_table(
        self,
        company_dim: pd.DataFrame,
        location_dim: pd.DataFrame,
        industry_dim: pd.DataFrame,
    ) -> pd.DataFrame:

        fact = self.df.copy()

        company_lookup = dict(
            zip(
                company_dim["company_name"],
                company_dim["company_id"],
            )
        )

        location_lookup = dict(
            zip(
                location_dim["location"],
                location_dim["location_id"],
            )
        )

        industry_lookup = dict(
            zip(
                industry_dim["industries"],
                industry_dim["industry_id"],
            )
        )

        fact["company_id"] = (
            fact["company_name"]
            .map(company_lookup)
        )

        fact["location_id"] = (
            fact["location"]
            .map(location_lookup)
        )

        fact["industry_id"] = (
            fact["industries"]
            .map(industry_lookup)
        )

        fact = fact[
            [
                "job_id",
                "company_id",
                "location_id",
                "industry_id",
                "job_title",
                "annual_salary_usd",
                "salary_min",
                "salary_max",
                "salary_median",
                "views",
                "applies",
                "skill_count",
                "experience_bucket",
                "remote_classification",
                "salary_tier",
                "posting_year",
                "posting_month",
                "job_age_days",
            ]
        ]

        return fact

    # ==========================================================
    # POWER BI DATASET
    # ==========================================================

    def create_powerbi_dataset(
        self,
    ) -> pd.DataFrame:

        dataset = self.df.copy()

        dataset = dataset.loc[
            :,
            ~dataset.columns.duplicated(),
        ]

        return dataset
    
    
        # ==========================================================
    # EXPORT ALL DATASETS
    # ==========================================================

    def export_datasets(
        self,
    ) -> None:
        """
        Generate and export all Power BI datasets.
        """

        logger.info(
            "Generating Power BI datasets..."
        )

        company_dim = self.create_company_dimension()

        location_dim = self.create_location_dimension()

        industry_dim = self.create_industry_dimension()

        skill_dim = self.create_skill_dimension()
        
        bridge_job_skill = self.create_bridge_job_skill(
        skill_dim
        )

        fact_jobs = self.create_fact_table(
            company_dim,
            location_dim,
            industry_dim,
        )

        powerbi_dataset = (
            self.create_powerbi_dataset()
        )

        save_csv(
            company_dim,
            DIM_COMPANY_FILE,
        )

        save_csv(
            location_dim,
            DIM_LOCATION_FILE,
        )

        save_csv(
            industry_dim,
            DIM_INDUSTRY_FILE,
        )

        save_csv(
            skill_dim,
            DIM_SKILL_FILE,
        )
        
        save_csv(
            bridge_job_skill,
            BRIDGE_JOB_SKILL_FILE,
        )

        save_csv(
            fact_jobs,
            FACT_JOBS_FILE,
        )

        save_csv(
            powerbi_dataset,
            POWERBI_DATASET_FILE,
        )

        logger.info(
            "All Power BI datasets exported successfully."
        )

    # ==========================================================
    # EXECUTE
    # ==========================================================

    def execute(
        self,
    ) -> None:
        """
        Execute complete Power BI export pipeline.
        """

        logger.info("=" * 60)
        logger.info(
            "Starting Power BI Export"
        )
        logger.info("=" * 60)

        self.load_dataset()

        self.export_datasets()

        logger.info("=" * 60)
        logger.info(
            "Power BI Export Completed"
        )
        logger.info("=" * 60)


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:
    """
    Application entry point.
    """

    try:

        exporter = PowerBIExporter()

        exporter.execute()

    except Exception:

        logger.exception(
            "Power BI Export Failed."
        )

        raise


if __name__ == "__main__":
    main()
    