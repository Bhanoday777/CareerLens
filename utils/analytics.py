import pandas as pd


def get_salary_data(df):
    """
    Returns cleaned salary records for analytics.
    """

    salary = df.copy()

    salary = salary[salary["normalized_salary"].notna()]

    salary = salary[salary["normalized_salary"].between(20000, 300000)]

    return salary


# =====================================================
# LOCATIONS
# =====================================================


def get_top_locations(df, n=10):

    locations = df["location"].fillna("Unknown").value_counts().head(n).reset_index()

    locations.columns = ["Location", "Jobs"]

    return locations


# =====================================================
# COMPANIES
# =====================================================


def get_top_companies(df, n=10):

    companies = (
        df[df["company_name"].notna() & (df["company_name"].str.strip() != "")][
            "company_name"
        ]
        .value_counts()
        .head(n)
        .reset_index()
    )

    companies.columns = ["Company", "Jobs"]

    return companies


# =====================================================
# INDUSTRIES
# =====================================================


def get_top_industries(df, n=10):

    industries = (
        df["industries"]
        .dropna()
        .astype(str)
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(n)
        .reset_index()
    )

    industries.columns = ["Industry", "Jobs"]

    return industries


# =====================================================
# SKILLS
# =====================================================


def get_top_skills(df, n=10):

    skills = df["skills"].dropna().astype(str).str.split(",").explode().str.strip()

    skills = (
        skills[(skills != "") & (skills != "nan")].value_counts().head(n).reset_index()
    )

    skills.columns = ["Skill", "Jobs"]

    return skills


# =====================================================
# EXPERIENCE
# =====================================================


def get_experience_levels(df):

    experience = (
        df["formatted_experience_level"].fillna("Unknown").value_counts().reset_index()
    )

    experience.columns = ["Experience", "Jobs"]

    return experience


# =====================================================
# WORK TYPES
# =====================================================


def get_work_types(df):

    work = df["formatted_work_type"].fillna("Unknown").value_counts().reset_index()

    work.columns = ["Work Type", "Jobs"]

    return work


# =====================================================
# JOB TITLES
# =====================================================


def get_top_job_titles(df, n=10):

    jobs = df["title"].dropna().value_counts().head(n).reset_index()

    jobs.columns = ["Job Title", "Jobs"]

    return jobs


# =====================================================
# AVERAGE SALARY BY EXPERIENCE
# =====================================================


def get_average_salary_by_experience(df):

    salary = get_salary_data(df)

    counts = salary.groupby("formatted_experience_level").size()

    valid = counts[counts >= 30].index

    salary = salary[salary["formatted_experience_level"].isin(valid)]

    result = (
        salary.groupby("formatted_experience_level")["normalized_salary"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    result.columns = ["Experience", "Average Salary"]

    return result


# =====================================================
# AVERAGE SALARY BY WORK TYPE
# =====================================================


def get_average_salary_by_work_type(df):

    salary = get_salary_data(df)

    counts = salary.groupby("formatted_work_type").size()

    valid = counts[counts >= 30].index

    salary = salary[salary["formatted_work_type"].isin(valid)]

    result = (
        salary.groupby("formatted_work_type")["normalized_salary"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )

    result.columns = ["Work Type", "Average Salary"]

    return result


# =====================================================
# TOP PAYING INDUSTRIES
# =====================================================


def get_top_paying_industries(df, n=10):

    salary = get_salary_data(df)
    salary = salary[salary["industries"].notna()].copy()

    salary["industries"] = salary["industries"].str.split(",")

    salary = salary.explode("industries")

    salary["industries"] = salary["industries"].str.strip()

    result = (
        salary.groupby("industries")["normalized_salary"]
        .mean()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )

    result.columns = ["Industry", "Average Salary"]

    return result


# =====================================================
# TOP PAYING LOCATIONS
# =====================================================


def get_top_paying_locations(df, n=10):

    salary = get_salary_data(df)
    salary = salary[salary["location"].notna()].copy()

    result = (
        salary.groupby("location")["normalized_salary"]
        .mean()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )

    result.columns = ["Location", "Average Salary"]

    return result
