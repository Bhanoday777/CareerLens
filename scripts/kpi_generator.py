"""
CareerLens - KPI Generator

Phase 2

Generates key business KPIs from the processed dataset
and exports them as a JSON file.

Author: CareerLens
Python Version: 3.14
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from analytics_utils import (
    load_dataset,
    validate_dataframe,
)

from config import (
    INPUT_DATASET,
    KPI_SUMMARY_FILE,
)

from logger import get_logger

logger = get_logger(__name__)


class KPIGenerator:
    """
    Generates business KPIs.
    """

    def __init__(
        self,
        dataset_path: Path = INPUT_DATASET,
    ) -> None:

        self.dataset_path = dataset_path
        self.df: pd.DataFrame | None = None

    # =====================================================
    # LOAD DATASET
    # =====================================================

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

    # =====================================================
    # HELPER
    # =====================================================

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

    # =====================================================
    # GENERATE KPI DICTIONARY
    # =====================================================

    def generate_kpis(
        self,
    ) -> dict:

        if self.df is None:
            raise RuntimeError(
                "Dataset not loaded."
            )

        df = self.df

        total_jobs = len(df)

        remote_distribution = (
            df["remote_classification"]
            .value_counts()
        )

        top_company = (
            df["company_name"]
            .value_counts()
            .idxmax()
        )

        top_industry = (
            df["industries"]
            .value_counts()
            .idxmax()
        )

        top_location = (
            df["location"]
            .value_counts()
            .idxmax()
        )

        skills = (
            df["skills"]
            .fillna("")
            .str.split(",")
            .explode()
            .str.strip()
        )

        top_skill = (
            skills.value_counts()
            .idxmax()
        )

        return {

            "total_jobs": total_jobs,

            "average_salary": round(
                df["annual_salary_usd"].mean(),
                2,
            ),

            "median_salary": round(
                df["annual_salary_usd"].median(),
                2,
            ),

            "remote_percentage": self.percentage(
                remote_distribution.get(
                    "Remote",
                    0,
                ),
                total_jobs,
            ),

            "hybrid_percentage": self.percentage(
                remote_distribution.get(
                    "Hybrid",
                    0,
                ),
                total_jobs,
            ),

            "onsite_percentage": self.percentage(
                remote_distribution.get(
                    "Onsite",
                    0,
                ),
                total_jobs,
            ),

            "unique_companies":
                df["company_name"].nunique(),

            "unique_industries":
                df["industries"].nunique(),

            "top_company":
                top_company,

            "top_industry":
                top_industry,

            "top_skill":
                top_skill,

            "top_location":
                top_location,
        }
        
        
        # =====================================================
    # EXPORT KPI JSON
    # =====================================================

    def export_kpis(
        self,
        kpis: dict,
    ) -> None:
        """
        Export KPI summary as JSON.
        """

        logger.info(
            "Exporting KPI summary..."
        )

        KPI_SUMMARY_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            KPI_SUMMARY_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                kpis,
                file,
                indent=4,
            )

        logger.info(
            "KPI summary exported successfully."
        )

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(self) -> None:
        """
        Execute KPI generation pipeline.
        """

        logger.info("=" * 60)
        logger.info("Starting KPI Generation")
        logger.info("=" * 60)

        self.load_dataset()

        kpis = self.generate_kpis()

        self.export_kpis(
            kpis
        )

        logger.info("=" * 60)
        logger.info("KPI Generation Completed")
        logger.info("=" * 60)


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:
    """
    Application entry point.
    """

    try:

        generator = KPIGenerator()

        generator.execute()

    except Exception:

        logger.exception(
            "KPI Generation Failed."
        )

        raise


if __name__ == "__main__":
    main()