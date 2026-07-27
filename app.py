import streamlit as st
import pandas as pd

from utils.config import configure_page
from utils.session import initialize_session_state
from utils.styling import apply_global_styles

from utils.data_loader import load_master_jobs
from utils.filters import apply_filters

from components.sidebar import build_sidebar
from components.charts import (
    create_bar_chart,
    create_pie_chart,
)

# ----------------------------------------------------
# INITIALIZATION
# ----------------------------------------------------

configure_page()

initialize_session_state()

apply_global_styles()

# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

df = load_master_jobs()

build_sidebar()

filtered_df = apply_filters(df)

salary_df = filtered_df[filtered_df["normalized_salary"].notna()]

# =====================================================
# HERO
# =====================================================

st.title("CareerLens")

st.markdown("""
### Job Market Intelligence Platform

Analyze hiring trends, salary insights, company demand, remote opportunities,
and workforce analytics through an interactive dashboard.

---
""")

# =====================================================
# KPI CARDS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Jobs", f"{len(filtered_df):,}")

with col2:
    st.metric("Companies", f"{filtered_df['company_name'].nunique():,}")

with col3:
    avg_salary = salary_df["normalized_salary"].mean() if not salary_df.empty else 0

    st.metric("Average Salary", f"${avg_salary:,.0f}")

with col4:
    remote_jobs = filtered_df["remote_allowed"].fillna(False).sum()

    st.metric("Remote Jobs", f"{int(remote_jobs):,}")

st.divider()


# =====================================================
# ANALYTICS ROW 1
# =====================================================

left, right = st.columns([2, 1])

with left:

    top_companies = filtered_df["company_name"].value_counts().head(10).reset_index()

    top_companies.columns = ["Company", "Jobs"]

    fig = create_bar_chart(
        top_companies, x="Company", y="Jobs", title="Top Hiring Companies"
    )

    st.plotly_chart(fig, width="stretch", key="top_hiring_companies")

with right:

    remote = (
        filtered_df["remote_allowed"]
        .fillna(False)
        .replace({True: "Remote", False: "Onsite"})
        .value_counts()
        .reset_index()
    )

    remote.columns = ["Type", "Jobs"]

    fig = create_pie_chart(
        remote, names="Type", values="Jobs", title="Remote Distribution"
    )

    st.plotly_chart(fig, width="stretch", key="remote_distribution")


# =====================================================
# ANALYTICS ROW 2
# =====================================================

left, right = st.columns(2)

with left:

    industries = (
        filtered_df["industries"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
        .reset_index()
    )

    industries.columns = ["Industry", "Jobs"]

    fig = create_bar_chart(industries, x="Industry", y="Jobs", title="Top Industries")

    st.plotly_chart(fig, width="stretch", key="top_industries")

with right:

    exp = (
        filtered_df["formatted_experience_level"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )

    exp.columns = ["Experience", "Jobs"]

    fig = create_bar_chart(exp, x="Experience", y="Jobs", title="Experience Levels")

    st.plotly_chart(fig, width="stretch", key="experience_levels")

st.divider()

st.subheader("Key Insights")

insight1 = len(filtered_df)
insight2 = filtered_df["company_name"].nunique()
insight3 = salary_df["normalized_salary"].mean()
insight4 = int(remote_jobs)

st.info(f"""
**Current Market Snapshot**

• **{insight1:,}** active job postings

• **{insight2:,}** companies hiring

• Average salary of **${insight3:,.0f}**

• **{insight4:,}** remote opportunities available

Use the sidebar filters to drill into industries, locations, companies, experience levels, and work types.
""")


st.divider()

st.subheader("About CareerLens")

st.markdown("""
CareerLens is an interactive Job Market Intelligence Platform built using:

- Python
- Streamlit
- Pandas
- Plotly

The platform analyzes over **108,000+ LinkedIn job postings** to uncover
hiring trends, salary insights, company demand, remote opportunities,
and workforce analytics.

Use the navigation menu on the left to explore specialized dashboards.
""")
