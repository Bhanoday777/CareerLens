"""
CareerLens
-----------

Global Sidebar Component

Responsible for:
- Branding
- Global Filters
- Dataset Summary
- Quick Statistics
"""

from __future__ import annotations

import streamlit as st

from utils.data_loader import load_master_jobs
from utils.filters import get_unique_values
from utils.session import reset_filters


def build_sidebar():
    """
    Build the global application sidebar.
    """

    df = load_master_jobs()

    with st.sidebar:

        # ========================================================
        # Branding
        # ========================================================

        st.title("📊 CareerLens")
        st.caption("Job Market Intelligence Platform")

        st.divider()

        # ========================================================
        # Dataset
        # ========================================================

        st.subheader("📁 Dataset")
        st.success("master_jobs.csv")

        st.divider()

        # ========================================================
        # Filters
        # ========================================================

        st.subheader("🔍 Global Filters")

        # --------------------------------------------------------
        # Search
        # --------------------------------------------------------

        st.session_state.search_query = st.text_input(
            "Search Jobs",
            value=st.session_state.search_query,
            placeholder="Software Engineer, Data Scientist...",
        )

        # --------------------------------------------------------
        # Company
        # --------------------------------------------------------

        st.session_state.selected_company = st.selectbox(
            "🏢 Company",
            get_unique_values(df, "company_name"),
        )

        # --------------------------------------------------------
        # Experience
        # --------------------------------------------------------

        st.session_state.selected_experience = st.selectbox(
            "💼 Experience",
            get_unique_values(df, "formatted_experience_level"),
        )

        # --------------------------------------------------------
        # Work Type
        # --------------------------------------------------------

        st.session_state.selected_work_type = st.selectbox(
            "💼 Work Type",
            get_unique_values(df, "formatted_work_type"),
        )

        # --------------------------------------------------------
        # Location
        # --------------------------------------------------------

        st.session_state.selected_location = st.selectbox(
            "🏢 Location",
            get_unique_values(df, "location"),
        )

        # --------------------------------------------------------
        # Industry
        # --------------------------------------------------------

        st.session_state.selected_industry = st.selectbox(
            "🏢 Industry",
            get_unique_values(df, "industries"),
        )

        # --------------------------------------------------------
        # Remote
        # --------------------------------------------------------

        st.session_state.selected_remote = st.selectbox(
            "💼 Work Arrangement",
            [
                "All",
                "Remote",
                "On-site",
            ],
        )

        # --------------------------------------------------------
        # Salary
        # --------------------------------------------------------

        st.session_state.selected_salary_range = st.selectbox(
            "💰 Salary Range",
            [
                "All",
                "< $50K",
                "$50K – $100K",
                "$100K – $150K",
                "> $150K",
            ],
        )

        st.divider()

        # ========================================================
        # Quick Statistics
        # ========================================================

        st.subheader("📈 Quick Statistics")

        st.metric(
            "Jobs",
            f"{len(df):,}",
        )

        st.metric(
            "🏢 Companies",
            f"{df['company_name'].nunique():,}",
        )

        st.metric(
            "📍 Location",
            f"{df['location'].nunique():,}",
        )

        st.metric(
            "🏢 Industries",
            f"{df['industries'].nunique():,}",
        )

        st.divider()

        # ========================================================
        # Reset Filters
        # ========================================================

        if st.button(
            "🔄 Reset Filters",
            use_container_width=True,
        ):
            reset_filters()
            st.rerun()

        st.divider()

        st.caption("CareerLens v1.0")
