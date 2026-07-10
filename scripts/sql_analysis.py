"""
CareerLens - SQL Analytics

Phase 2

Creates the SQLite analytics database,
executes SQL analytics queries,
and generates SQL reports.

Author: CareerLens
Python Version: 3.14
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

from analytics_utils import (
    load_dataset,
    save_markdown,
    validate_dataframe,
)

from config import (
    DATABASE_FILE,
    INPUT_DATASET,
    SQL_QUERIES_FILE,
    SQL_REPORT,
)

from logger import get_logger

logger = get_logger(__name__)


class SQLAnalysis:
    """
    SQLite analytics engine.
    """

    def __init__(
        self,
        dataset_path: Path = INPUT_DATASET,
        database_path: Path = DATABASE_FILE,
    ) -> None:

        self.dataset_path = dataset_path
        self.database_path = database_path

        self.df: pd.DataFrame | None = None
        self.connection: sqlite3.Connection | None = None

    # =====================================================
    # DATASET
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
            "Dataset loaded."
        )

    # =====================================================
    # DATABASE
    # =====================================================

    def create_database(
        self,
    ) -> None:

        logger.info(
            "Creating SQLite database..."
        )

        self.connection = sqlite3.connect(
            self.database_path
        )

        logger.info(
            "Database created."
        )

    # =====================================================
    # IMPORT DATA
    # =====================================================

    def import_dataset(
        self,
    ) -> None:

        if self.connection is None:
            raise RuntimeError(
                "Database not initialized."
            )

        logger.info(
            "Importing dataset..."
        )

        self.df.to_sql(
            "jobs",
            self.connection,
            if_exists="replace",
            index=False,
        )

        logger.info(
            "Dataset imported."
        )

    # =====================================================
    # QUERY LIBRARY
    # =====================================================

    def query_library(
        self,
    ) -> dict[str, str]:

        return {

            "Total Jobs":
            """
            SELECT
                COUNT(*) AS total_jobs
            FROM jobs;
            """,

            "Top Hiring Companies":
            """
            SELECT
                company_name,
                COUNT(*) AS hiring_count
            FROM jobs
            GROUP BY company_name
            ORDER BY hiring_count DESC
            LIMIT 10;
            """,

            "Top Hiring Locations":
            """
            SELECT
                location,
                COUNT(*) AS hiring_count
            FROM jobs
            GROUP BY location
            ORDER BY hiring_count DESC
            LIMIT 10;
            """,

            "Top Industries":
            """
            SELECT
                industries,
                COUNT(*) AS hiring_count
            FROM jobs
            GROUP BY industries
            ORDER BY hiring_count DESC
            LIMIT 10;
            """,

            "Average Salary":
            """
            SELECT
                ROUND(
                    AVG(annual_salary_usd),
                    2
                ) AS average_salary
            FROM jobs
            WHERE annual_salary_usd
            IS NOT NULL;
            """,

            "Highest Paying Companies":
            """
            SELECT
                company_name,
                ROUND(
                    AVG(annual_salary_usd),
                    2
                ) AS average_salary
            FROM jobs
            WHERE annual_salary_usd
            IS NOT NULL
            GROUP BY company_name
            ORDER BY average_salary DESC
            LIMIT 10;
            """,

            "Experience Distribution":
            """
            SELECT
                experience_bucket,
                COUNT(*) AS jobs
            FROM jobs
            GROUP BY experience_bucket;
            """,

            "Remote Distribution":
            """
            SELECT
                remote_classification,
                COUNT(*) AS jobs
            FROM jobs
            GROUP BY remote_classification;
            """,

            "Monthly Hiring":
            """
            SELECT
                posting_month,
                COUNT(*) AS jobs
            FROM jobs
            GROUP BY posting_month
            ORDER BY posting_month;
            """,

            "Yearly Hiring":
            """
            SELECT
                posting_year,
                COUNT(*) AS jobs
            FROM jobs
            GROUP BY posting_year;
            """,
        }

    # =====================================================
    # EXECUTE QUERY
    # =====================================================

    def execute_query(
        self,
        query: str,
    ) -> pd.DataFrame:

        if self.connection is None:
            raise RuntimeError(
                "Database not connected."
            )

        return pd.read_sql_query(
            query,
            self.connection,
        )

    # =====================================================
    # EXECUTE ALL QUERIES
    # =====================================================

    def execute_all_queries(
        self,
    ) -> dict[str, pd.DataFrame]:

        logger.info(
            "Executing SQL queries..."
        )

        results = {}

        for (
            title,
            query,
        ) in self.query_library().items():

            results[title] = self.execute_query(
                query
            )

        logger.info(
            "SQL queries completed."
        )

        return results
    
    
    # =====================================================
# CLOSE DATABASE
# =====================================================

    def close_database(self) -> None:
        """
        Close SQLite connection safely.
        """

        if self.connection is not None:
            self.connection.close()
            self.connection = None

        logger.info(
            "Database connection closed."
        )
        

    # =====================================================
    # EXPORT SQL FILE
    # =====================================================

    def export_sql_queries(self) -> None:
        """
        Export all SQL queries to analytics_queries.sql
        """

        logger.info(
            "Exporting SQL query library..."
        )

        sql_text = []

        for title, query in self.query_library().items():

            sql_text.append(
                f"-- {title}\n"
            )

            sql_text.append(
                query.strip()
            )

            sql_text.append("\n\n")

        SQL_QUERIES_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            SQL_QUERIES_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            file.writelines(sql_text)

        logger.info(
            "SQL query library exported."
        )

    # =====================================================
    # GENERATE REPORT
    # =====================================================

    def generate_report(
        self,
        results: dict[str, pd.DataFrame],
    ) -> str:
        """
        Generate SQL analysis markdown report.
        """

        report = []

        report.append(
            "# SQL Analytics Report\n\n"
        )

        report.append(
            "This report contains the results "
            "of analytical SQL queries executed "
            "against the CareerLens SQLite database.\n\n"
        )

        for title, dataframe in results.items():

            report.append(
                f"## {title}\n\n"
            )

            report.append(
                dataframe.to_markdown(
                    index=False
                )
            )

            report.append("\n\n")

        return "".join(report)

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(self) -> None:
        """
        Execute complete SQL analytics pipeline.
        """

        logger.info("=" * 60)
        logger.info("Starting SQL Analytics")
        logger.info("=" * 60)

        try:

            self.load_dataset()

            self.create_database()

            self.import_dataset()

            results = self.execute_all_queries()

            self.export_sql_queries()

            report = self.generate_report(
                results
            )

            save_markdown(
                report,
                SQL_REPORT,
            )

            logger.info(
                "SQL report generated."
            )

        finally:

            self.close_database()

        logger.info("=" * 60)
        logger.info(
            "SQL Analytics Completed"
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

        analysis = SQLAnalysis()

        analysis.execute()

    except Exception:

        logger.exception(
            "SQL Analytics Failed."
        )

        raise


if __name__ == "__main__":
    main()