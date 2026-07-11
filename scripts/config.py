"""
CareerLens - Phase 2 Configuration

Centralized configuration for file paths, logging, and project constants.

Author: CareerLens
Python Version: 3.14
"""

from pathlib import Path

# ==========================================================
# Project Root
# ==========================================================

PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent

# ==========================================================
# Directories
# ==========================================================

DATA_DIR: Path = PROJECT_ROOT / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"

REPORTS_DIR: Path = PROJECT_ROOT / "reports"
LOGS_DIR: Path = PROJECT_ROOT / "logs"
SQL_DIR: Path = PROJECT_ROOT / "sql"
VISUALIZATION_DIR: Path = PROJECT_ROOT / "visualizations"

SCRIPTS_DIR: Path = PROJECT_ROOT / "scripts"
NOTEBOOKS_DIR: Path = PROJECT_ROOT / "notebooks"

# ==========================================================
# Visualization Subdirectories
# ==========================================================

COMPANIES_VIS_DIR: Path = VISUALIZATION_DIR / "companies"
LOCATIONS_VIS_DIR: Path = VISUALIZATION_DIR / "locations"
INDUSTRIES_VIS_DIR: Path = VISUALIZATION_DIR / "industries"
SKILLS_VIS_DIR: Path = VISUALIZATION_DIR / "skills"
SALARY_VIS_DIR: Path = VISUALIZATION_DIR / "salary"
TRENDS_VIS_DIR: Path = VISUALIZATION_DIR / "trends"
REMOTE_VIS_DIR: Path = VISUALIZATION_DIR / "remote"
CORRELATION_VIS_DIR: Path = VISUALIZATION_DIR / "correlations"

# ==========================================================
# Input Dataset
# ==========================================================

INPUT_DATASET: Path = PROCESSED_DATA_DIR / "jobs_enriched.csv"

# ==========================================================
# Output Files
# ==========================================================

ANALYTICS_SUMMARY_FILE: Path = PROCESSED_DATA_DIR / "analytics_summary.csv"

POWERBI_DATASET_FILE: Path = PROCESSED_DATA_DIR / "powerbi_dataset.csv"

DATABASE_FILE: Path = PROCESSED_DATA_DIR / "analytics_database.db"

KPI_JSON_FILE: Path = PROCESSED_DATA_DIR / "kpi_summary.json"

TOP_ENTITIES_FILE: Path = PROCESSED_DATA_DIR / "top_entities.csv"

KPI_SUMMARY_FILE = PROCESSED_DATA_DIR / "kpi_summary.json"

# Star Schema

DIM_COMPANY_FILE: Path = PROCESSED_DATA_DIR / "dim_company.csv"

DIM_LOCATION_FILE: Path = PROCESSED_DATA_DIR / "dim_location.csv"

DIM_INDUSTRY_FILE: Path = PROCESSED_DATA_DIR / "dim_industry.csv"

DIM_SKILL_FILE: Path = PROCESSED_DATA_DIR / "dim_skill.csv"

FACT_JOBS_FILE: Path = PROCESSED_DATA_DIR / "fact_jobs.csv"

BRIDGE_JOB_SKILL_FILE: Path = PROCESSED_DATA_DIR / "bridge_job_skill.csv"

# ==========================================================
# Reports
# ==========================================================

EDA_REPORT: Path = REPORTS_DIR / "exploratory_analysis.md"

BUSINESS_REPORT: Path = REPORTS_DIR / "business_insights.md"

SQL_REPORT: Path = REPORTS_DIR / "sql_analysis.md"

CORRELATION_REPORT: Path = REPORTS_DIR / "correlation_analysis.md"

EXECUTIVE_REPORT: Path = REPORTS_DIR / "executive_summary.md"

DATA_DICTIONARY_REPORT: Path = REPORTS_DIR / "data_dictionary.md"

POWERBI_PLAN_REPORT: Path = REPORTS_DIR / "powerbi_dashboard_plan.md"

PHASE2_REPORT: Path = REPORTS_DIR / "phase2_summary.md"

# ==========================================================
# SQL
# ==========================================================

SQL_QUERIES_FILE: Path = SQL_DIR / "analytics_queries.sql"

# ==========================================================
# Logging
# ==========================================================

LOG_FILE: Path = LOGS_DIR / "careerlens_phase2.log"

LOG_LEVEL: str = "INFO"

# ==========================================================
# Plot Settings
# ==========================================================

DEFAULT_DPI: int = 300

DEFAULT_FIGURE_SIZE: tuple[int, int] = (12, 6)

PLOT_STYLE: str = "ggplot"

# ==========================================================
# General Constants
# ==========================================================

TOP_N: int = 10

RANDOM_STATE: int = 42

DATE_FORMAT: str = "%Y-%m-%d"

CSV_ENCODING: str = "utf-8"

# ==========================================================
# Create Required Directories
# ==========================================================

REQUIRED_DIRECTORIES = [
    REPORTS_DIR,
    LOGS_DIR,
    SQL_DIR,
    VISUALIZATION_DIR,
    COMPANIES_VIS_DIR,
    LOCATIONS_VIS_DIR,
    INDUSTRIES_VIS_DIR,
    SKILLS_VIS_DIR,
    SALARY_VIS_DIR,
    TRENDS_VIS_DIR,
    REMOTE_VIS_DIR,
    CORRELATION_VIS_DIR,
]

for directory in REQUIRED_DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)
