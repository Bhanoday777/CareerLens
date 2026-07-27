import streamlit as st
import pandas as pd

from utils.session import initialize_session_state
from utils.data_loader import load_master_jobs
from utils.filters import apply_filters
from utils.styling import apply_global_styles
from components.sidebar import build_sidebar

apply_global_styles()
initialize_session_state()

df = load_master_jobs()

build_sidebar()

filtered_df = apply_filters(df)

st.title("📂 Dataset Explorer")

st.markdown("""
Explore the complete filtered dataset, inspect records,
select columns, and export data for further analysis.
""")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Records", f"{len(filtered_df):,}")

with col2:
    st.metric("Columns", len(filtered_df.columns))

with col3:
    st.metric("Missing Values", f"{filtered_df.isna().sum().sum():,}")

with col4:
    memory = filtered_df.memory_usage(deep=True).sum() / 1024 / 1024

    st.metric("Memory Usage", f"{memory:.2f} MB")

st.divider()

st.subheader("Select Columns")

default_columns = [
    "title",
    "company_name",
    "location",
    "formatted_experience_level",
    "formatted_work_type",
    "normalized_salary",
    "industries",
]

selected_columns = st.multiselect(
    "Choose columns to display",
    options=filtered_df.columns.tolist(),
    default=default_columns,
)

search = st.text_input("Search within displayed data")

display_df = filtered_df.copy()

display_df = display_df.fillna("Not Specified")

display_df["company_name"] = display_df["company_name"].replace(
    "None", "Unknown Company"
)

if search:

    mask = display_df.astype(str).apply(
        lambda row: row.str.contains(search, case=False, na=False).any(), axis=1
    )

    display_df = display_df[mask]

display_df = display_df[selected_columns]

st.subheader("Dataset Preview")

rows_to_show = st.slider(
    "Rows to display",
    min_value=10,
    max_value=500,
    value=100,
    step=10,
)

st.caption(
    f"Showing first {min(rows_to_show, len(display_df)):,} "
    f"of {len(display_df):,} filtered job postings"
)

st.dataframe(
    display_df.head(rows_to_show),
    width="stretch",
    height=650,
)

csv = display_df.to_csv(index=False)

st.download_button(
    "⬇ Download Filtered Dataset",
    csv,
    file_name="careerlens_filtered_data.csv",
    mime="text/csv",
)
