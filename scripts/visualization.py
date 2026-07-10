"""
CareerLens

Visualization Engine

Phase 2

Generates professional visualizations for
Business Intelligence and Power BI.

Author: CareerLens
Python Version: 3.14
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud

from analytics_utils import (
    load_dataset,
    validate_dataframe,
)

from config import (
    INPUT_DATASET,
    COMPANIES_VIS_DIR,
    LOCATIONS_VIS_DIR,
    INDUSTRIES_VIS_DIR,
    SKILLS_VIS_DIR,
    SALARY_VIS_DIR,
    TRENDS_VIS_DIR,
    REMOTE_VIS_DIR,
    CORRELATION_VIS_DIR,
)

from logger import get_logger

logger = get_logger(__name__)


class VisualizationGenerator:
    """
    Generates all project visualizations.
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

        logger.info(
            "Dataset loaded successfully."
        )

    # =====================================================
    # SAVE FIGURE
    # =====================================================

    @staticmethod
    def save_figure(
        output_path: Path,
    ) -> None:

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=300,
            bbox_inches="tight",
        )

        plt.close()

        logger.info(
            "Saved: %s",
            output_path.name,
        )

    # =====================================================
    # TOP N HELPER
    # =====================================================

    @staticmethod
    def top_n(
        series: pd.Series,
        n: int = 10,
    ) -> pd.Series:

        return (
            series
            .value_counts()
            .head(n)
        )
        
        
        # =====================================================
    # TOP COMPANIES
    # =====================================================

    def plot_top_companies(self) -> None:

        data = self.top_n(
            self.df["company_name"]
        )

        plt.figure(figsize=(12, 6))
        data.plot(kind="bar")

        plt.title("Top Hiring Companies")
        plt.xlabel("Company")
        plt.ylabel("Job Count")

        self.save_figure(
            COMPANIES_VIS_DIR / "top_companies.png"
        )

    # =====================================================
    # TOP INDUSTRIES
    # =====================================================

    def plot_top_industries(self) -> None:

        data = self.top_n(
            self.df["industries"]
        )

        plt.figure(figsize=(12, 6))
        data.plot(kind="bar")

        plt.title("Top Industries")
        plt.xlabel("Industry")
        plt.ylabel("Job Count")

        self.save_figure(
            INDUSTRIES_VIS_DIR / "top_industries.png"
        )

    # =====================================================
    # TOP LOCATIONS
    # =====================================================

    def plot_top_locations(self) -> None:

        data = self.top_n(
            self.df["location"]
        )

        plt.figure(figsize=(12, 6))
        data.plot(kind="bar")

        plt.title("Top Hiring Locations")
        plt.xlabel("Location")
        plt.ylabel("Job Count")

        self.save_figure(
            LOCATIONS_VIS_DIR / "top_locations.png"
        )

    # =====================================================
    # TOP SKILLS
    # =====================================================

    def plot_top_skills(self) -> None:

        skills = (
            self.df["skills"]
            .fillna("")
            .str.split(",")
            .explode()
            .str.strip()
        )

        data = skills.value_counts().head(20)

        plt.figure(figsize=(12, 7))
        data.plot(kind="bar")

        plt.title("Top Skills")
        plt.xlabel("Skill")
        plt.ylabel("Frequency")

        self.save_figure(
            SKILLS_VIS_DIR / "top_skills.png"
        )

    # =====================================================
    # EXPERIENCE DISTRIBUTION
    # =====================================================

    def plot_experience_distribution(self) -> None:

        data = (
            self.df["experience_bucket"]
            .value_counts()
        )

        plt.figure(figsize=(8, 6))
        data.plot(kind="bar")

        plt.title("Experience Distribution")
        plt.xlabel("Experience")
        plt.ylabel("Jobs")

        self.save_figure(
            TRENDS_VIS_DIR /
            "experience_distribution.png"
        )

    # =====================================================
    # REMOTE DISTRIBUTION
    # =====================================================

    def plot_remote_distribution(self) -> None:

        data = (
            self.df["remote_classification"]
            .value_counts()
        )

        plt.figure(figsize=(7, 7))

        plt.pie(
            data,
            labels=data.index,
            autopct="%1.1f%%",
        )

        plt.title("Remote Classification")

        self.save_figure(
            REMOTE_VIS_DIR /
            "remote_distribution.png"
        )

    # =====================================================
    # SALARY TIER
    # =====================================================

    def plot_salary_tier(self) -> None:

        data = (
            self.df["salary_tier"]
            .value_counts()
        )

        plt.figure(figsize=(7, 7))

        plt.pie(
            data,
            labels=data.index,
            autopct="%1.1f%%",
        )

        plt.title("Salary Tier")

        self.save_figure(
            SALARY_VIS_DIR /
            "salary_tier.png"
        )

    # =====================================================
    # MONTHLY HIRING
    # =====================================================

    def plot_monthly_hiring(self) -> None:

        data = (
            self.df["posting_month"]
            .value_counts()
            .sort_index()
        )

        plt.figure(figsize=(10, 5))

        data.plot(marker="o")

        plt.title("Monthly Hiring Trend")
        plt.xlabel("Month")
        plt.ylabel("Jobs")

        self.save_figure(
            TRENDS_VIS_DIR /
            "monthly_hiring.png"
        )

    # =====================================================
    # YEARLY HIRING
    # =====================================================

    def plot_yearly_hiring(self) -> None:

        data = (
            self.df["posting_year"]
            .value_counts()
            .sort_index()
        )

        plt.figure(figsize=(8, 5))

        data.plot(marker="o")

        plt.title("Yearly Hiring Trend")
        plt.xlabel("Year")
        plt.ylabel("Jobs")

        self.save_figure(
            TRENDS_VIS_DIR /
            "yearly_hiring.png"
        )

    # =====================================================
    # SALARY HISTOGRAM
    # =====================================================

    def plot_salary_distribution(self) -> None:

        plt.figure(figsize=(10, 6))

        plt.hist(
            self.df["annual_salary_usd"].dropna(),
            bins=40,
        )

        plt.title("Salary Distribution")
        plt.xlabel("Annual Salary")
        plt.ylabel("Frequency")

        self.save_figure(
            SALARY_VIS_DIR /
            "salary_distribution.png"
        )
        
        # =====================================================
    # SKILL COUNT HISTOGRAM
    # =====================================================

    def plot_skill_count_distribution(self) -> None:

        plt.figure(figsize=(10, 6))

        plt.hist(
            self.df["skill_count"],
            bins=20,
        )

        plt.title("Skill Count Distribution")
        plt.xlabel("Skill Count")
        plt.ylabel("Frequency")

        self.save_figure(
            SKILLS_VIS_DIR /
            "skill_count_distribution.png"
        )

    # =====================================================
    # SALARY VS SKILL COUNT
    # =====================================================

    def plot_salary_vs_skill_count(self) -> None:

        dataframe = self.df.dropna(
            subset=[
                "annual_salary_usd",
                "skill_count",
            ]
        )

        plt.figure(figsize=(10, 6))

        plt.scatter(
            dataframe["skill_count"],
            dataframe["annual_salary_usd"],
            alpha=0.4,
        )

        plt.title("Salary vs Skill Count")
        plt.xlabel("Skill Count")
        plt.ylabel("Annual Salary (USD)")

        self.save_figure(
            CORRELATION_VIS_DIR /
            "salary_vs_skill_count.png"
        )

    # =====================================================
    # SALARY VS EXPERIENCE
    # =====================================================

    def plot_salary_vs_experience(self) -> None:

        dataframe = self.df.dropna(
            subset=["annual_salary_usd"]
        )

        plt.figure(figsize=(10, 6))

        dataframe.boxplot(
            column="annual_salary_usd",
            by="experience_bucket",
            rot=45,
        )

        plt.title("Salary by Experience")

        plt.suptitle("")

        plt.xlabel("Experience")

        plt.ylabel("Annual Salary")

        self.save_figure(
            SALARY_VIS_DIR /
            "salary_vs_experience.png"
        )

    # =====================================================
    # SALARY VS REMOTE
    # =====================================================

    def plot_salary_vs_remote(self) -> None:

        dataframe = self.df.dropna(
            subset=["annual_salary_usd"]
        )

        plt.figure(figsize=(10, 6))

        dataframe.boxplot(
            column="annual_salary_usd",
            by="remote_classification",
        )

        plt.title("Salary by Remote Classification")

        plt.suptitle("")

        plt.xlabel("Remote Classification")

        plt.ylabel("Annual Salary")

        self.save_figure(
            REMOTE_VIS_DIR /
            "salary_vs_remote.png"
        )

    # =====================================================
    # CORRELATION HEATMAP
    # =====================================================

    def plot_correlation_heatmap(self) -> None:

        dataframe = self.df[
            [
                "annual_salary_usd",
                "salary_min",
                "salary_max",
                "salary_median",
                "skill_count",
                "job_age_days",
            ]
        ].dropna()

        correlation = dataframe.corr(
            numeric_only=True,
        )

        plt.figure(figsize=(8, 6))

        plt.imshow(
            correlation,
            aspect="auto",
        )

        plt.xticks(
            range(len(correlation.columns)),
            correlation.columns,
            rotation=45,
        )

        plt.yticks(
            range(len(correlation.columns)),
            correlation.columns,
        )

        plt.colorbar()

        plt.title("Correlation Heatmap")

        self.save_figure(
            CORRELATION_VIS_DIR /
            "correlation_heatmap.png"
        )
        
        # =====================================================
    # WORD CLOUD
    # =====================================================

    def plot_wordcloud(self) -> None:

        text = " ".join(
            self.df["skills"]
            .fillna("")
            .astype(str)
        )

        wordcloud = WordCloud(
            width=1600,
            height=800,
            background_color="white",
        ).generate(text)

        plt.figure(figsize=(14, 8))

        plt.imshow(
            wordcloud,
            interpolation="bilinear",
        )

        plt.axis("off")

        plt.title("Top Skills Word Cloud")

        self.save_figure(
            SKILLS_VIS_DIR /
            "skills_wordcloud.png"
        )

    # =====================================================
    # TREEMAP
    # =====================================================

         # =====================================================
    # INDUSTRY TREEMAP
    # =====================================================

    def plot_industry_treemap(self) -> None:

        data = (
            self.df["industries"]
            .value_counts()
            .head(20)
            .reset_index()
        )

        data.columns = [
            "Industry",
            "Count",
        ]

        figure = px.treemap(
            data,
            path=["Industry"],
            values="Count",
            title="Top Industries Treemap",
        )

        output_file = (
            INDUSTRIES_VIS_DIR /
            "industry_treemap.png"
        )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        figure.write_image(
            output_file,
            width=1400,
            height=800,
            scale=2,
        )

        logger.info(
            "Saved: %s",
            output_file.name,
        )
    # =====================================================
    # GENERATE ALL VISUALIZATIONS
    # =====================================================

    def generate_all_visualizations(
        self,
    ) -> None:

        logger.info(
            "Generating visualizations..."
        )

        self.plot_top_companies()

        self.plot_top_industries()

        self.plot_top_locations()

        self.plot_top_skills()

        self.plot_experience_distribution()

        self.plot_remote_distribution()

        self.plot_salary_tier()

        self.plot_monthly_hiring()

        self.plot_yearly_hiring()

        self.plot_salary_distribution()

        self.plot_skill_count_distribution()

        self.plot_salary_vs_skill_count()

        self.plot_salary_vs_experience()

        self.plot_salary_vs_remote()

        self.plot_correlation_heatmap()

        self.plot_wordcloud()

        self.plot_industry_treemap()

        logger.info(
            "All visualizations generated successfully."
        )

    # =====================================================
    # EXECUTE
    # =====================================================

    def execute(
        self,
    ) -> None:

        logger.info("=" * 60)
        logger.info(
            "Starting Visualization Engine"
        )
        logger.info("=" * 60)

        self.load_dataset()

        self.generate_all_visualizations()

        logger.info("=" * 60)
        logger.info(
            "Visualization Engine Completed"
        )
        logger.info("=" * 60)


# =====================================================
# MAIN
# =====================================================


def main() -> None:

    try:

        visualization = VisualizationGenerator()

        visualization.execute()

    except Exception:

        logger.exception(
            "Visualization generation failed."
        )

        raise


if __name__ == "__main__":
    main()