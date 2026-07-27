import streamlit as st

from utils.session import initialize_session_state
from utils.data_loader import load_master_jobs
from utils.styling import apply_global_styles

from components.sidebar import build_sidebar

apply_global_styles()
initialize_session_state()

df = load_master_jobs()

build_sidebar()

st.title("ℹ️ About CareerLens")

st.markdown("""
CareerLens is an AI-powered Job Market Intelligence Platform that transforms
large-scale job posting data into actionable insights for job seekers,
recruiters, analysts, and organizations.

Instead of manually exploring thousands of job listings,
CareerLens provides interactive dashboards, salary analytics,
hiring trends, and skill demand visualizations through an intuitive interface.
""")

st.divider()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Job Listings", f"{len(df):,}")

with col2:
    st.metric("Companies", f"{df['company_name'].nunique():,}")

with col3:
    st.metric("Locations", f"{df['location'].nunique():,}")

with col4:
    st.metric("Industries", f"{df['industries'].nunique():,}")

st.divider()

st.header("✨ Key Features")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
### 📊 Interactive Analytics

- Executive Dashboard
- Hiring Trends
- Salary Analytics
- Job Search
- Dataset Explorer

### 🔍 Smart Filtering

- Company
- Experience
- Industry
- Work Type
- Location
- Work Arrangement
- Salary Range
""")

with col2:

    st.markdown("""
### 📈 Business Intelligence

- Hiring Insights
- Salary Trends
- Company Analysis
- Industry Analysis
- Skill Demand
- Workforce Distribution

### 📥 Export

- Download filtered datasets
- Interactive exploration
- Dynamic visualizations
""")

st.divider()

st.header("🛠 Technology Stack")

tech1, tech2, tech3, tech4 = st.columns(4)

with tech1:

    st.markdown("""
### 🐍 Backend

- Python
- Pandas
- NumPy
""")

with tech2:

    st.markdown("""
### 🎨 Frontend

- Streamlit
- HTML
- CSS
""")

with tech3:

    st.markdown("""
### 📈 Visualization

- Plotly
- Interactive Charts
- KPI Cards
""")

with tech4:

    st.markdown("""
### ⚙ Data Engineering

- CSV
- Feature Engineering
- Analytics Pipeline
""")

st.divider()

st.divider()

st.header("⚙ Project Workflow")

st.markdown("""
### 📥 Data Collection

⬇️

### 🧹 Data Cleaning

⬇️

### ⚙ Feature Engineering

⬇️

### 📊 Analytics Processing

⬇️

### 📈 Interactive Dashboards

⬇️

### 💡 Business Insights
""")

st.divider()

st.header("👨‍💻 Developer")

st.markdown("""
**Bhanoday Kurma**

CareerLens is an end-to-end Job Market Intelligence Platform built to demonstrate
Data Analytics, Business Intelligence, Data Engineering, and Interactive Dashboard
development using Python, Streamlit, and Plotly.

---

### 🔗 Connect

**GitHub:** https://github.com/Bhanoday777/CareerLens

**LinkedIn:** https://www.linkedin.com/in/YOUR-LINKEDIN/

---

© 2026 CareerLens
""")
