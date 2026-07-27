"""
CareerLens
-----------

Session State Manager

Centralizes all Streamlit session state initialization and management.
"""

from __future__ import annotations

import streamlit as st


DEFAULT_SESSION_STATE = {
    # ==========================
    # Data
    # ==========================
    "raw_df": None,
    "filtered_df": None,
    "current_dataset": None,

    # ==========================
    # Global Filters
    # ==========================
    "selected_location": "All",
    "selected_company": "All",
    "selected_industry": "All",
    "selected_experience": "All",
    "selected_remote": "All",
    "selected_salary_range": "All",
    "selected_work_type": "All",

    # ==========================
    # Search
    # ==========================
    "search_query": "",
    "selected_columns": [],

    # ==========================
    # UI
    # ==========================
    "theme": "light",
    "sidebar_expanded": True,

    # ==========================
    # Downloads
    # ==========================
    "last_export": None,

    # ==========================
    # Misc
    # ==========================
    "page_loaded": False,
}


def initialize_session_state() -> None:
    """
    Initialize all session state variables.
    Safe to call multiple times.
    """

    for key, value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_filters() -> None:
    """
    Reset only filter-related session state.
    """

    st.session_state.selected_location = "All"
    st.session_state.selected_company = "All"
    st.session_state.selected_industry = "All"
    st.session_state.selected_experience = "All"
    st.session_state.selected_remote = "All"
    st.session_state.selected_work_type = "All"
    st.session_state.selected_salary_range = "All"
    st.session_state.search_query = ""


def clear_loaded_data() -> None:
    """
    Clear cached dataframe references from session state.
    """

    st.session_state.raw_df = None
    st.session_state.filtered_df = None
    st.session_state.current_dataset = None