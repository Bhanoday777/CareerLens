import streamlit as st
import pandas as pd

from utils.data_loader import load_master_jobs
from utils.styling import apply_global_styles
from utils.filters import apply_filters
from components.sidebar import build_sidebar
from components.charts import (
    create_bar_chart,
    create_line_chart,
    create_pie_chart,
    create_histogram,
)
from utils.analytics import (
    get_top_locations,
    get_top_companies,
    get_top_industries,
    get_top_skills,
    get_experience_levels,
    get_work_types,
    get_salary_data,
)

apply_global_styles()
# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

df = load_master_jobs()

build_sidebar()

filtered_df = apply_filters(df)

salary_df = get_salary_data(filtered_df)

# ----------------------------------------------------
# PAGE TITLE
# ----------------------------------------------------

st.title("📊 Executive Overview")

st.markdown("""
A high-level executive dashboard summarizing the current job market
using key hiring, salary, company, location, and skill insights.
""")

st.divider()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Jobs", f"{len(filtered_df):,}")

with col2:
    st.metric("Companies", f"{filtered_df['company_name'].nunique():,}")

with col3:

    avg_salary = salary_df["normalized_salary"].mean() if not salary_df.empty else 0

    st.metric("Average Salary", f"${avg_salary:,.0f}")

with col4:

    if filtered_df.empty:
        remote_percent = 0
    else:
        remote_percent = filtered_df["remote_allowed"].fillna(False).mean() * 100

    st.metric("Remote %", f"{remote_percent:.1f}%")

st.divider()


# =====================================================
# ANALYTICS ROW 1
# =====================================================

left, right = st.columns(2)

with left:

    locations = (
        filtered_df["location"].fillna("Unknown").value_counts().head(10).reset_index()
    )

    locations.columns = ["Location", "Jobs"]

    location_fig = create_bar_chart(
        locations,
        x="Location",
        y="Jobs",
        title="Top Hiring Locations",
    )

    st.plotly_chart(
        location_fig,
        width="stretch",
        key="top_locations",
    )


with right:

    # Remove only the top 1% salary outliers
    upper_limit = salary_df["normalized_salary"].quantile(0.99)

    salary_plot = salary_df[salary_df["normalized_salary"].between(10000, upper_limit)]

    salary_fig = create_histogram(
        salary_plot, column="normalized_salary", title="Salary Distribution"
    )

    st.plotly_chart(salary_fig, width="stretch", key="salary_distribution")


# =====================================================
# ANALYTICS ROW 2
# =====================================================

st.divider()

left, right = st.columns(2)

# ----------------------------------------------------
# WORK TYPE DISTRIBUTION
# ----------------------------------------------------

with left:

    work_type = (
        filtered_df["formatted_work_type"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    work_type.columns = ["Work Type", "Jobs"]

    worktype_fig = create_pie_chart(
        work_type,
        names="Work Type",
        values="Jobs",
        title="Work Type Distribution",
    )

    st.plotly_chart(
        worktype_fig,
        width="stretch",
        key="work_type_distribution",
    )

# ----------------------------------------------------
# EXPERIENCE LEVELS
# ----------------------------------------------------

with right:

    experience = (
        filtered_df["formatted_experience_level"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    experience.columns = ["Experience", "Jobs"]

    experience_fig = create_bar_chart(
        experience,
        x="Experience",
        y="Jobs",
        title="Experience Level Distribution",
    )

    st.plotly_chart(
        experience_fig,
        width="stretch",
        key="experience_distribution",
    )


# =====================================================
# ANALYTICS ROW 3
# =====================================================

st.divider()

left, right = st.columns(2)

# ----------------------------------------------------
# TOP SKILLS
# ----------------------------------------------------

with left:

    skills = (
        filtered_df["skills"].dropna().astype(str).str.split(",").explode().str.strip()
    )

    skills = skills[skills != ""].value_counts().head(10).reset_index()

    skills.columns = ["Skill", "Jobs"]

    skills_fig = create_bar_chart(
        skills,
        x="Skill",
        y="Jobs",
        title="Top In-Demand Skills",
    )

    st.plotly_chart(
        skills_fig,
        width="stretch",
        key="top_skills",
    )

# ----------------------------------------------------
# TOP HIRING COMPANIES
# ----------------------------------------------------

with right:

    companies = (
        filtered_df[
            filtered_df["company_name"].notna()
            & (filtered_df["company_name"].str.strip() != "")
        ]["company_name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    companies.columns = ["Company", "Jobs"]

    company_fig = create_bar_chart(
        companies,
        x="Company",
        y="Jobs",
        title="Top Hiring Companies",
    )

    st.plotly_chart(
        company_fig,
        width="stretch",
        key="top_companies_overview",
    )
