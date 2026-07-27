import streamlit as st

from utils.data_loader import load_master_jobs
from utils.filters import apply_filters
from utils.config import configure_page
from utils.session import initialize_session_state
from utils.styling import apply_global_styles

from components.sidebar import build_sidebar
from components.charts import (
    create_bar_chart,
    create_pie_chart,
)

from utils.analytics import (
    get_top_locations,
    get_top_companies,
    get_top_industries,
    get_top_skills,
    get_experience_levels,
    get_work_types,
    get_top_job_titles,
)

configure_page()
initialize_session_state()
apply_global_styles()
# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------

df = load_master_jobs()

build_sidebar()

filtered_df = apply_filters(df)

# ----------------------------------------------------
# PAGE TITLE
# ----------------------------------------------------

st.title("📈 Hiring Trends")

st.markdown("""
Analyze hiring demand across locations, industries, companies,
work types, experience levels, and required skills.
""")

st.divider()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Active Jobs", f"{len(filtered_df):,}")

with col2:
    st.metric("Hiring Companies", f"{filtered_df['company_name'].nunique():,}")

with col3:
    st.metric("Locations", f"{filtered_df['location'].nunique():,}")

with col4:
    st.metric("Industries", f"{filtered_df['industries'].nunique():,}")

st.divider()


left, right = st.columns(2)

with left:

    locations = get_top_locations(filtered_df)

    fig = create_bar_chart(
        locations, x="Location", y="Jobs", title="Top Hiring Locations"
    )

    st.plotly_chart(fig, width="stretch", key="trend_locations")

with right:

    companies = get_top_companies(filtered_df)

    fig = create_bar_chart(
        companies, x="Company", y="Jobs", title="Top Hiring Companies"
    )

    st.plotly_chart(fig, width="stretch", key="trend_companies")


st.divider()

left, right = st.columns(2)

# ----------------------------------------------------
# TOP INDUSTRIES
# ----------------------------------------------------

with left:

    industries = get_top_industries(filtered_df)

    fig = create_bar_chart(
        industries,
        x="Industry",
        y="Jobs",
        title="Top Hiring Industries",
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key="trend_industries",
    )

with right:

    experience = get_experience_levels(filtered_df)

    fig = create_bar_chart(
        experience,
        x="Experience",
        y="Jobs",
        title=" Experience Level Demand",
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key="trend_experience",
    )


# =====================================================
# ANALYTICS ROW 3
# =====================================================

st.divider()

left, right = st.columns(2)

# =====================================================
# JOB TITLES
# =====================================================


with left:

    titles = get_top_job_titles(filtered_df)

    fig = create_bar_chart(
        titles,
        x="Job Title",
        y="Jobs",
        title="Top Hiring Roles",
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key="trend_job_titles",
    )


# ----------------------------------------------------
# REMOTE VS ONSITE
# ----------------------------------------------------

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
        remote,
        names="Type",
        values="Jobs",
        title="Remote vs Onsite Hiring",
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key="trend_remote",
    )


st.divider()

st.subheader("Hiring Insights")

st.success(f"""
### Market Highlights

• **{len(filtered_df):,}** active job postings across **{filtered_df['company_name'].nunique():,}** companies.

• Hiring demand is concentrated in major metropolitan regions, with the United States and large cities accounting for the highest number of openings.

• Full-time roles continue to dominate hiring activity, while remote opportunities represent approximately **{filtered_df['remote_allowed'].fillna(False).mean() * 100:.1f}%** of postings.

• Healthcare, IT Services, Retail, and Financial Services remain among the strongest hiring industries.

• Employers continue to prioritize **Mid-Senior** and **Entry-Level** talent, reflecting demand for experienced professionals alongside early-career hiring.
""")
