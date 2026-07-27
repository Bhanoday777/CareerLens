import streamlit as st

from utils.config import configure_page
from utils.session import initialize_session_state
from utils.styling import apply_global_styles

from utils.data_loader import load_master_jobs
from utils.filters import apply_filters

from components.sidebar import build_sidebar
from components.charts import (
    create_bar_chart,
    create_histogram,
    create_boxplot,
)

from utils.analytics import (
    get_average_salary_by_experience,
    get_average_salary_by_work_type,
    get_top_paying_industries,
    get_top_paying_locations,
    get_salary_data,
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

salary_df = get_salary_data(filtered_df)

# ----------------------------------------------------
# PAGE TITLE
# ----------------------------------------------------

st.title("💰 Salary Analytics")

st.markdown("""
Explore compensation trends across industries, experience levels,
work types, and locations.
""")

st.divider()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Average Salary", f"${salary_df['normalized_salary'].mean():,.0f}")

with col2:
    st.metric("Median Salary", f"${salary_df['normalized_salary'].median():,.0f}")

with col3:
    st.metric("Highest Salary", f"${salary_df['normalized_salary'].max():,.0f}")

with col4:
    st.metric("Salary Records", f"{len(salary_df):,}")

st.divider()


left, right = st.columns(2)

# ----------------------------------------------------
# EXPERIENCE
# ----------------------------------------------------

with left:

    exp = get_average_salary_by_experience(filtered_df)

    fig = create_bar_chart(
        exp,
        x="Experience",
        y="Average Salary",
        title="Average Salary by Experience",
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key="salary_exp",
    )

# ----------------------------------------------------
# WORK TYPE
# ----------------------------------------------------

with right:

    work = get_average_salary_by_work_type(filtered_df)

    fig = create_bar_chart(
        work,
        x="Work Type",
        y="Average Salary",
        title="Average Salary by Work Type",
    )

    st.plotly_chart(
        fig,
        width="stretch",
        key="salary_work",
    )

