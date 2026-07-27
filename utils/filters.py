"""
CareerLens
-----------

Filtering utilities.

Contains reusable dataframe filtering logic shared across the application.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

# ============================================================
# FILTER OPTIONS
# ============================================================


def get_unique_values(df: pd.DataFrame, column: str) -> list:
    """
    Return sorted unique values from a column.
    """

    if column not in df.columns:
        return ["All"]

    values = df[column].dropna().astype(str).sort_values().unique().tolist()

    return ["All"] + values


# ============================================================
# EXPERIENCE FILTER
# ============================================================


def filter_experience(df: pd.DataFrame) -> pd.DataFrame:

    value = st.session_state.selected_experience

    if value != "All" and "formatted_experience_level" in df.columns:
        df = df[df["formatted_experience_level"] == value]

    return df


# ============================================================
# INDUSTRY FILTER
# ============================================================


def filter_industry(df: pd.DataFrame) -> pd.DataFrame:

    value = st.session_state.selected_industry

    if value == "All":
        return df

    if "industries" not in df.columns:
        return df

    return df[df["industries"].fillna("").str.contains(value, case=False, na=False)]


# ============================================================
# LOCATION FILTER
# ============================================================


def filter_location(df: pd.DataFrame) -> pd.DataFrame:

    value = st.session_state.selected_location

    if value != "All" and "location" in df.columns:
        df = df[df["location"] == value]

    return df


# ============================================================
# COMPANY FILTER
# ============================================================


def filter_company(df: pd.DataFrame) -> pd.DataFrame:

    value = st.session_state.selected_company

    if value != "All" and "company_name" in df.columns:
        df = df[df["company_name"] == value]

    return df


# ============================================================
# REMOTE FILTER
# ============================================================


def filter_remote(df: pd.DataFrame) -> pd.DataFrame:

    value = st.session_state.selected_remote

    if value == "No Preference":
        return df

    if "remote_allowed" not in df.columns:
        return df

    if value == "Remote":
        return df[df["remote_allowed"] == True]

    if value == "Onsite":
        return df[df["remote_allowed"] == False]

    return df


# ============================================================
# SALARY FILTER
# ============================================================


def filter_salary(df: pd.DataFrame) -> pd.DataFrame:

    value = st.session_state.selected_salary_range

    if value == "All":
        return df

    if "normalized_salary" not in df.columns:
        return df

    salary = df["normalized_salary"]

    if value == "< $50K":
        return df[salary < 50_000]

    elif value == "$50K – $100K":
        return df[(salary >= 50_000) & (salary < 100_000)]

    elif value == "$100K – $150K":
        return df[(salary >= 100_000) & (salary < 150_000)]

    elif value == "> $150K":
        return df[salary >= 150_000]

    return df


def filter_work_type(df: pd.DataFrame) -> pd.DataFrame:

    value = st.session_state.selected_work_type

    if value != "All" and "formatted_work_type" in df.columns:
        df = df[df["formatted_work_type"] == value]

    return df


# ============================================================
# SEARCH FILTER
# ============================================================


def filter_search(df: pd.DataFrame) -> pd.DataFrame:

    query = st.session_state.search_query.strip()

    if not query:
        return df

    query = query.lower()

    searchable_columns = [
        col
        for col in [
            "title",
            "company_name",
            "industries",
            "location",
        ]
        if col in df.columns
    ]

    if not searchable_columns:
        return df

    mask = False

    for column in searchable_columns:
        mask = mask | df[column].astype(str).str.lower().str.contains(query, na=False)

    return df[mask]


# ============================================================
# APPLY ALL FILTERS
# ============================================================


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply every global filter.
    """

    df = filter_experience(df)
    df = filter_work_type(df)
    df = filter_industry(df)
    df = filter_location(df)
    df = filter_company(df)
    df = filter_remote(df)
    df = filter_salary(df)
    df = filter_search(df)

    return df.reset_index(drop=True)
