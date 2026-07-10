"""
CareerLens

Report Generator

Phase 2

Generates professional business reports
for CareerLens.

Author: CareerLens
Python Version: 3.14
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from analytics_utils import (
    load_dataset,
    save_markdown,
    validate_dataframe,
)

from config import (
    INPUT_DATASET,
    EXECUTIVE_REPORT,
    CORRELATION_REPORT,
    DATA_DICTIONARY_REPORT,
    POWERBI_PLAN_REPORT,
    PHASE2_REPORT,
)

from logger import get_logger

logger = get_logger(__name__)


class ReportGenerator:
    """
    Generates all Phase 2 reports.
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

    def load_dataset(
        self,
    ) -> None:

        logger.info(
            "Loading dataset..."
        )

        self.df = load_dataset(
            self.dataset_path
        )

        validate_dataframe(
            self.df
        )

    # =====================================================
    # CORRELATION
    # =====================================================

    def correlation_analysis(
        self,
    ) -> dict[str, float]:

        dataframe = self.df[
            [
                "annual_salary_usd",
                "skill_count",
                "job_age_days",
            ]
        ].dropna()

        return {

            "pearson_salary_skill":
                dataframe[
                    "annual_salary_usd"
                ].corr(
                    dataframe[
                        "skill_count"
                    ],
                    method="pearson",
                ),

            "pearson_salary_job_age":
                dataframe[
                    "annual_salary_usd"
                ].corr(
                    dataframe[
                        "job_age_days"
                    ],
                    method="pearson",
                ),

            "spearman_salary_skill":
                dataframe[
                    "annual_salary_usd"
                ].corr(
                    dataframe[
                        "skill_count"
                    ],
                    method="spearman",
                ),

            "spearman_salary_job_age":
                dataframe[
                    "annual_salary_usd"
                ].corr(
                    dataframe[
                        "job_age_days"
                    ],
                    method="spearman",
                ),
        }

    # =====================================================
    # DATA DICTIONARY
    # =====================================================

    def data_dictionary(
        self,
    ) -> pd.DataFrame:

        dataframe = self.df

        return pd.DataFrame(
            {
                "Field": dataframe.columns,
                "Data Type": dataframe.dtypes.astype(str),
                "Missing Values": dataframe.isna().sum().values,
            }
        )
        
        # =====================================================
    # EXECUTIVE SUMMARY
    # =====================================================

    def executive_summary(
        self,
    ) -> str:

        dataframe = self.df

        total_jobs = len(dataframe)

        avg_salary = dataframe[
            "annual_salary_usd"
        ].mean()

        median_salary = dataframe[
            "annual_salary_usd"
        ].median()

        top_company = (
            dataframe["company_name"]
            .value_counts()
            .idxmax()
        )

        top_location = (
            dataframe["location"]
            .value_counts()
            .idxmax()
        )

        top_industry = (
            dataframe["industries"]
            .value_counts()
            .idxmax()
        )

        return f"""
# Executive Summary

## Executive KPIs

- Total Jobs: {total_jobs:,}
- Average Salary: ${avg_salary:,.2f}
- Median Salary: ${median_salary:,.2f}
- Unique Companies: {dataframe['company_name'].nunique()}
- Unique Industries: {dataframe['industries'].nunique()}
- Unique Locations: {dataframe['location'].nunique()}

## Key Findings

- Highest hiring company: {top_company}
- Most active industry: {top_industry}
- Most active location: {top_location}

## Recommendations

- Continue monitoring hiring trends.
- Focus on high-paying industries.
- Build skill development around the most demanded technologies.

## Future Scope

- Live dashboards
- Automated ETL pipeline
- Predictive analytics
- ML salary prediction
"""

    # =====================================================
    # CORRELATION REPORT
    # =====================================================

    def correlation_report(
        self,
    ) -> str:

        corr = self.correlation_analysis()

        report = []

        report.append("# Correlation Analysis\n\n")

        for key, value in corr.items():

            report.append(
                f"- **{key}** : {value:.4f}\n"
            )

        return "".join(report)

    # =====================================================
    # DATA DICTIONARY REPORT
    # =====================================================

    def data_dictionary_report(
        self,
    ) -> str:

        dictionary = self.data_dictionary()

        return (
            "# Data Dictionary\n\n"
            + dictionary.to_markdown(
                index=False
            )
        )

    # =====================================================
    # POWER BI DASHBOARD PLAN
    # =====================================================

    def powerbi_dashboard_plan(
        self,
    ) -> str:

        return """
# Power BI Dashboard Plan

## Dashboard 1
Executive Overview

KPIs
- Total Jobs
- Average Salary
- Companies
- Industries

---

## Dashboard 2
Hiring Trends

Charts

- Monthly Hiring
- Yearly Hiring
- Top Companies

---

## Dashboard 3
Salary Intelligence

Charts

- Salary Distribution
- Salary by Industry
- Salary by Experience

---

## Dashboard 4
Skills Dashboard

Charts

- Top Skills
- Skill Distribution
- Skill Count

---

## Dashboard 5
Industry Dashboard

Charts

- Top Industries
- Highest Paying Industries

---

## Dashboard 6
Location Dashboard

Charts

- Top Locations
- Highest Paying Locations

Filters

- Company
- Industry
- Experience
- Salary Tier
- Remote Classification
"""

    # =====================================================
    # PHASE 2 SUMMARY
    # =====================================================

    def phase2_summary(
        self,
    ) -> str:

        return """
# Phase 2 Summary

## Objectives

- Perform Exploratory Data Analysis
- Generate Business Intelligence reports
- Create SQL Analytics layer
- Generate KPIs
- Prepare Power BI datasets
- Build Star Schema
- Generate Business Reports

---

## Deliverables

✓ Exploratory Analysis

✓ Business Analysis

✓ SQL Analytics

✓ KPI Generation

✓ Power BI Dataset

✓ Star Schema

✓ Executive Reports

✓ Correlation Analysis

✓ Data Dictionary

✓ Dashboard Planning

---

## Future Scope

- Interactive Power BI Dashboard
- Machine Learning Salary Prediction
- Live Data Pipeline
- Real-Time Job Analytics
"""

    # =====================================================
    # EXPORT REPORTS
    # =====================================================

    def export_reports(
        self,
    ) -> None:

        logger.info(
            "Generating reports..."
        )

        save_markdown(
            self.executive_summary(),
            EXECUTIVE_REPORT,
        )

        save_markdown(
            self.correlation_report(),
            CORRELATION_REPORT,
        )

        save_markdown(
            self.data_dictionary_report(),
            DATA_DICTIONARY_REPORT,
        )

        save_markdown(
            self.powerbi_dashboard_plan(),
            POWERBI_PLAN_REPORT,
        )

        save_markdown(
            self.phase2_summary(),
            PHASE2_REPORT,
        )

        logger.info(
            "Reports generated successfully."
        )

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(
        self,
    ) -> None:

        logger.info("=" * 60)
        logger.info(
            "Starting Report Generation"
        )
        logger.info("=" * 60)

        self.load_dataset()

        self.export_reports()

        logger.info("=" * 60)
        logger.info(
            "Report Generation Completed"
        )
        logger.info("=" * 60)


# ==========================================================
# MAIN
# ==========================================================


def main() -> None:

    try:

        generator = ReportGenerator()

        generator.execute()

    except Exception:

        logger.exception(
            "Report generation failed."
        )

        raise


if __name__ == "__main__":
    main()