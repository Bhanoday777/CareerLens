"""
CareerLens - Exploratory Data Analysis

Phase 2

Loads the processed dataset and performs
exploratory data analysis.

Outputs
-------
reports/exploratory_analysis.md
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from analytics_utils import (
    categorical_summary,
    column_information,
    dataframe_to_markdown,
    dataset_profile,
    generation_timestamp,
    load_dataset,
    markdown_key_value_table,
    missing_value_summary,
    numerical_summary,
    save_markdown,
    validate_dataframe,
)

from config import (
    EDA_REPORT,
    INPUT_DATASET,
)

from logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# DATA CLASS
# ==========================================================


@dataclass(slots=True)
class EDAResults:
    """
    Stores all exploratory analysis outputs.
    """

    profile: dict
    column_info: pd.DataFrame
    missing_values: pd.DataFrame
    numerical_summary: pd.DataFrame
    categorical_summary: pd.DataFrame


# ==========================================================
# EXPLORATORY ANALYSIS
# ==========================================================


class ExploratoryAnalysis:
    """
    Performs exploratory analysis on the processed dataset.
    """

    def __init__(
        self,
        dataset_path: Path = INPUT_DATASET,
    ) -> None:

        self.dataset_path = dataset_path

        self.df: pd.DataFrame | None = None

    # ======================================================
    # LOAD DATASET
    # ======================================================

    def load_dataset(self) -> None:
        """
        Load and validate dataset.
        """

        logger.info("Loading processed dataset...")

        self.df = load_dataset(self.dataset_path)

        validate_dataframe(self.df)

        logger.info("Dataset loaded successfully.")

    # ======================================================
    # DATASET PROFILE
    # ======================================================

    def generate_dataset_profile(self) -> dict:

        logger.info("Generating dataset profile...")

        return dataset_profile(self.df)

    # ======================================================
    # COLUMN INFORMATION
    # ======================================================

    def generate_column_information(self) -> pd.DataFrame:

        logger.info("Generating column information...")

        return column_information(self.df)

    # ======================================================
    # MISSING VALUE SUMMARY
    # ======================================================

    def generate_missing_values(
        self,
    ) -> pd.DataFrame:

        logger.info("Generating missing value summary...")

        return missing_value_summary(self.df)

    # ======================================================
    # NUMERICAL SUMMARY
    # ======================================================

    def generate_numerical_summary(
        self,
    ) -> pd.DataFrame:

        logger.info("Generating numerical summary...")

        return numerical_summary(self.df)

    # ======================================================
    # CATEGORICAL SUMMARY
    # ======================================================

    def categorical_summary(
        self,
    ) -> pd.DataFrame:

        logger.info("Generating categorical summary...")

        return categorical_summary(self.df)

    # ======================================================
    # RUN COMPLETE EDA
    # ======================================================

    def analyze(
        self,
    ) -> EDAResults:
        """
        Execute exploratory analysis.
        """

        if self.df is None:
            raise RuntimeError("Dataset has not been loaded.")

        logger.info("Running exploratory analysis...")

        results = EDAResults(
            profile=self.generate_dataset_profile(),
            column_info=self.generate_column_information(),
            missing_values=self.generate_missing_values(),
            numerical_summary=self.generate_numerical_summary(),
            categorical_summary=self.categorical_summary(),
        )

        logger.info("Exploratory analysis completed.")

        return results

    # ======================================================
    # REPORT GENERATION
    # ======================================================

    def build_report(
        self,
        results: EDAResults,
    ) -> str:
        """
        Build the exploratory analysis markdown report.
        """

        report: list[str] = []

        report.append("# CareerLens Exploratory Analysis Report\n")

        report.append(
            "This report presents an exploratory analysis "
            "of the processed job dataset.\n"
        )

        report.append(f"Report Generated: {generation_timestamp()}\n")

        # --------------------------------------------------

        report.append("## Dataset Profile\n")

        report.append(markdown_key_value_table(results.profile))

        # --------------------------------------------------

        report.append("## Column Information\n")

        report.append(dataframe_to_markdown(results.column_info))

        report.append("\n")

        # --------------------------------------------------

        report.append("## Missing Value Analysis\n")

        report.append(dataframe_to_markdown(results.missing_values))

        report.append("\n")

        # --------------------------------------------------

        report.append("## Numerical Summary\n")

        report.append(dataframe_to_markdown(results.numerical_summary))

        report.append("\n")

        # --------------------------------------------------

        report.append("## Categorical Summary\n")

        report.append(dataframe_to_markdown(results.categorical_summary))

        report.append("\n")

        report.append("## Conclusion\n")

        report.append(
            "The dataset has been successfully profiled "
            "and is ready for Business Intelligence analysis.\n"
        )

        return "\n".join(report)

    # ======================================================
    # EXPORT REPORT
    # ======================================================

    def export_report(
        self,
        report: str,
    ) -> None:
        """
        Export markdown report.
        """

        logger.info("Saving report...")

        save_markdown(
            report,
            EDA_REPORT,
        )

        logger.info("Report exported successfully.")

    # ======================================================
    # COMPLETE PIPELINE
    # ======================================================

    def execute(self) -> None:
        """
        Execute complete exploratory analysis.
        """

        logger.info("=" * 60)
        logger.info("Starting Exploratory Analysis")
        logger.info("=" * 60)

        self.load_dataset()

        results = self.analyze()

        report = self.build_report(results)

        self.export_report(report)

        logger.info("=" * 60)
        logger.info("Exploratory Analysis Completed")
        logger.info("=" * 60)


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:
    """
    Main entry point.
    """

    try:

        analysis = ExploratoryAnalysis()

        analysis.execute()

    except Exception:

        logger.exception("Exploratory Analysis Failed.")

        raise


if __name__ == "__main__":
    main()
