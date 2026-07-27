"""
CareerLens
-----------

Data Loader

Responsible for:
- Loading CSV datasets
- Loading JSON files
- Loading SQLite database
- Dataset validation
- Cached data loading
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.constants import (
    PROCESSED_DATA_DIR,
)

# ============================================================
# DATASET PATHS
# ============================================================

MASTER_JOBS = PROCESSED_DATA_DIR / "master_jobs.csv"

FACT_JOBS = PROCESSED_DATA_DIR / "fact_jobs.csv"

COMPANIES = PROCESSED_DATA_DIR / "dim_company.csv"

INDUSTRIES = PROCESSED_DATA_DIR / "dim_industry.csv"

LOCATIONS = PROCESSED_DATA_DIR / "dim_location.csv"

SKILLS = PROCESSED_DATA_DIR / "dim_skill.csv"

BRIDGE = PROCESSED_DATA_DIR / "bridge_job_skill.csv"

POWERBI = PROCESSED_DATA_DIR / "powerbi_dataset.csv"

SUMMARY = PROCESSED_DATA_DIR / "analytics_summary.csv"

TOP_ENTITIES = PROCESSED_DATA_DIR / "top_entities.csv"

KPI_JSON = PROCESSED_DATA_DIR / "kpi_summary.json"

DATABASE = PROCESSED_DATA_DIR / "analytics_database.db"


# ============================================================
# GENERIC CSV LOADER
# ============================================================


@st.cache_data(show_spinner=False)
def load_csv(path: Path) -> pd.DataFrame:
    """
    Load a CSV file.
    """

    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    df = pd.read_csv(path)

    # ----------------------------------------------------
    # DATE CLEANUP (only if the column exists)
    # ----------------------------------------------------

    if "listed_time" in df.columns:

        df["listed_time"] = pd.to_datetime(
            df["listed_time"],
            unit="ms",
            errors="coerce",
        )

        df["posting_month"] = df["listed_time"].dt.to_period("M").astype(str)

        df["posting_year"] = df["listed_time"].dt.year

    return df


# ============================================================
# JSON LOADER
# ============================================================


@st.cache_data(show_spinner=False)
def load_json(path: Path):
    """
    Load a JSON file.
    """

    if not path.exists():
        raise FileNotFoundError(path)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# SQLITE LOADER
# ============================================================


@st.cache_resource
def get_database_connection():

    if not DATABASE.exists():
        raise FileNotFoundError(DATABASE)

    return sqlite3.connect(DATABASE)


# ============================================================
# INDIVIDUAL DATASETS
# ============================================================


def load_master_jobs():
    return load_csv(MASTER_JOBS)


def load_fact_jobs():
    return load_csv(FACT_JOBS)


def load_companies():
    return load_csv(COMPANIES)


def load_industries():
    return load_csv(INDUSTRIES)


def load_locations():
    return load_csv(LOCATIONS)


def load_skills():
    return load_csv(SKILLS)


def load_bridge():
    return load_csv(BRIDGE)


def load_powerbi_dataset():
    return load_csv(POWERBI)


def load_summary():
    return load_csv(SUMMARY)


def load_top_entities():
    return load_csv(TOP_ENTITIES)


def load_kpi_summary():
    return load_json(KPI_JSON)


# ============================================================
# LOAD EVERYTHING
# ============================================================


@st.cache_data(show_spinner=False)
def load_all_data():
    """
    Load every dataset required by the application.
    """

    return {
        "master_jobs": load_master_jobs(),
        "fact_jobs": load_fact_jobs(),
        "companies": load_companies(),
        "industries": load_industries(),
        "locations": load_locations(),
        "skills": load_skills(),
        "bridge": load_bridge(),
        "powerbi": load_powerbi_dataset(),
        "summary": load_summary(),
        "top_entities": load_top_entities(),
        "kpi": load_kpi_summary(),
    }


# ============================================================
# DATA VALIDATION
# ============================================================


def validate_dataframe(df: pd.DataFrame) -> bool:
    """
    Validate a dataframe.
    """

    return not df.empty


# ============================================================
# DATABASE TABLES
# ============================================================


def get_database_tables():

    conn = get_database_connection()

    query = """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    """

    tables = pd.read_sql(query, conn)

    return tables["name"].tolist()
