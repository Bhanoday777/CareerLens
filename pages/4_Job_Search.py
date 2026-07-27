import streamlit as st
import pandas as pd

from utils.session import initialize_session_state
from utils.data_loader import load_master_jobs
from utils.filters import apply_filters
from utils.analytics import get_salary_data
from utils.styling import apply_global_styles

from components.sidebar import build_sidebar

apply_global_styles()
initialize_session_state()

df = load_master_jobs()

build_sidebar()

filtered_df = apply_filters(df)

salary_df = get_salary_data(filtered_df)

st.title("🔍 Job Search")

st.markdown("""
Search and explore thousands of job postings using the filters in the sidebar.
""")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Jobs Found", f"{len(filtered_df):,}")

with col2:
    st.metric("Companies", f"{filtered_df['company_name'].nunique():,}")

with col3:
    st.metric("Average Salary", f"${salary_df['normalized_salary'].mean():,.0f}")

with col4:

    remote = filtered_df["remote_allowed"].fillna(False).mean() * 100

    st.metric("Remote %", f"{remote:.1f}%")

st.divider()

st.subheader("Search Results")

results = filtered_df[
    filtered_df["company_name"].notna()
    & (filtered_df["company_name"].str.strip() != "")
].head(25)

st.caption(f"Showing first {len(results)} of {len(filtered_df):,} matching jobs")

for _, job in results.iterrows():

    title = job.get("title", "Unknown")

    company = (
        job["company_name"] if pd.notna(job["company_name"]) else "Unknown Company"
    )

    with st.expander(f"💼 {title} | {company}"):

        col1, col2 = st.columns(2)

    with col1:

        st.write(f"🏢 **Company:** {company}")

        location = job["location"] if pd.notna(job["location"]) else "Not Specified"

        st.write(f"📍 **Location:** {location}")

        if pd.notna(job["normalized_salary"]):

            st.write(f"💰 **Salary:** ${job['normalized_salary']:,.0f}")

    with col2:

        experience = (
            job["formatted_experience_level"]
            if pd.notna(job["formatted_experience_level"])
            else "Not Specified"
        )

        st.write(f"🎓 **Experience:** {experience}")

        st.write(f"💼 **Work Type:** {job['formatted_work_type']}")

        st.write(f"🌍 **Remote:** {'Yes' if job['remote_allowed'] else 'No'}")

        industry = job["industries"] if pd.notna(job["industries"]) else "Not Specified"

        st.write(f"🏭 **Industry:** {industry}")

        if pd.notna(job["job_posting_url"]):

            st.link_button(
                "🔗 View Job Posting",
                job["job_posting_url"],
            )
