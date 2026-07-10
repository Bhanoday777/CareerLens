"""
CareerLens - Analytics Utility Functions

Common reusable utility functions used throughout
Phase 2 Analytics & Business Intelligence.

Author: CareerLens
Python Version: 3.14
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from config import CSV_ENCODING
from logger import get_logger

logger = get_logger(__name__)


# ==========================================================
# DIRECTORY UTILITIES
# ==========================================================


def ensure_directory(directory: Path) -> None:
    """
    Create a directory if it does not exist.

    Parameters
    ----------
    directory : Path
        Directory to create.
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info("Verified directory: %s", directory)

    except Exception as exc:
        logger.exception("Unable to create directory: %s", directory)
        raise RuntimeError(f"Failed creating directory: {directory}") from exc


# ==========================================================
# FILE VALIDATION
# ==========================================================


def validate_file_exists(file_path: Path) -> None:
    """
    Ensure a file exists.

    Raises
    ------
    FileNotFoundError
    """
    if not file_path.exists():
        logger.error("File not found: %s", file_path)
        raise FileNotFoundError(file_path)

    logger.info("Found file: %s", file_path)


# ==========================================================
# DATASET LOADING
# ==========================================================


def load_dataset(file_path: Path) -> pd.DataFrame:
    """
    Load a CSV dataset.

    Parameters
    ----------
    file_path : Path

    Returns
    -------
    pd.DataFrame
    """
    validate_file_exists(file_path)

    try:
        dataframe = pd.read_csv(
            file_path,
            encoding=CSV_ENCODING,
        )

        logger.info(
            "Dataset loaded successfully (%d rows, %d columns)",
            len(dataframe),
            len(dataframe.columns),
        )

        return dataframe

    except Exception as exc:
        logger.exception("Failed loading dataset.")
        raise RuntimeError(f"Unable to load dataset: {file_path}") from exc


# ==========================================================
# DATASET SAVING
# ==========================================================


def save_csv(
    dataframe: pd.DataFrame,
    output_file: Path,
    *,
    index: bool = False,
) -> None:
    """
    Save DataFrame to CSV.

    Parameters
    ----------
    dataframe : pd.DataFrame
    output_file : Path
    index : bool
    """
    ensure_directory(output_file.parent)

    try:
        dataframe.to_csv(
            output_file,
            index=index,
            encoding=CSV_ENCODING,
        )

        logger.info("CSV exported: %s", output_file)

    except Exception as exc:
        logger.exception("CSV export failed.")
        raise RuntimeError(f"Unable to export CSV: {output_file}") from exc


# ==========================================================
# JSON EXPORT
# ==========================================================


def save_json(
    data: dict[str, Any],
    output_file: Path,
) -> None:
    """
    Save dictionary as JSON.

    Parameters
    ----------
    data : dict
    output_file : Path
    """
    ensure_directory(output_file.parent)

    try:
        with output_file.open(
            "w",
            encoding="utf-8",
        ) as json_file:
            json.dump(
                data,
                json_file,
                indent=4,
                ensure_ascii=False,
            )

        logger.info("JSON exported: %s", output_file)

    except Exception as exc:
        logger.exception("JSON export failed.")
        raise RuntimeError(f"Unable to export JSON: {output_file}") from exc


# ==========================================================
# MARKDOWN EXPORT
# ==========================================================


def save_markdown(
    content: str,
    output_file: Path,
) -> None:
    """
    Save markdown report.

    Parameters
    ----------
    content : str
    output_file : Path
    """
    ensure_directory(output_file.parent)

    try:
        output_file.write_text(
            content,
            encoding="utf-8",
        )

        logger.info("Markdown report saved: %s", output_file)

    except Exception as exc:
        logger.exception("Markdown export failed.")
        raise RuntimeError(f"Unable to save markdown: {output_file}") from exc


# ==========================================================
# DATAFRAME VALIDATION
# ==========================================================


def validate_dataframe(
    dataframe: pd.DataFrame,
) -> None:
    """
    Validate DataFrame.

    Raises
    ------
    ValueError
        If DataFrame is empty.
    """
    if dataframe.empty:
        logger.error("DataFrame is empty.")
        raise ValueError("DataFrame is empty.")

    logger.info(
        "Validated DataFrame (%d rows)",
        len(dataframe),
    )


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str],
) -> None:
    """
    Ensure required columns exist.

    Parameters
    ----------
    dataframe : pd.DataFrame
    required_columns : list[str]
    """
    missing = [column for column in required_columns if column not in dataframe.columns]

    if missing:
        logger.error(
            "Missing columns: %s",
            ", ".join(missing),
        )
        raise ValueError(f"Missing required columns: {missing}")

    logger.info("All required columns are present.")


# ==========================================================
# BASIC DATASET INFORMATION
# ==========================================================


def dataset_shape(
    dataframe: pd.DataFrame,
) -> tuple[int, int]:
    """
    Return dataset shape.

    Returns
    -------
    tuple[int, int]
    """
    return dataframe.shape


def column_names(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Return column names.
    """
    return dataframe.columns.tolist()


def dataframe_memory_usage(
    dataframe: pd.DataFrame,
) -> float:
    """
    Calculate memory usage in MB.
    """
    memory = dataframe.memory_usage(deep=True).sum()

    return round(memory / 1024**2, 2)


# ==========================================================
# DUPLICATE ANALYSIS
# ==========================================================


def duplicate_count(
    dataframe: pd.DataFrame,
) -> int:
    """
    Count duplicate rows.
    """
    return int(dataframe.duplicated().sum())


def duplicate_percentage(
    dataframe: pd.DataFrame,
) -> float:
    """
    Duplicate percentage.
    """
    total = len(dataframe)

    if total == 0:
        return 0.0

    duplicates = duplicate_count(dataframe)

    return round((duplicates / total) * 100, 2)


# ==========================================================
# MISSING VALUE ANALYSIS
# ==========================================================


def missing_value_summary(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate a summary of missing values for each column.

    Returns
    -------
    pd.DataFrame
        Columns:
            - Column
            - Missing Values
            - Missing Percentage
    """
    missing_count = dataframe.isna().sum()
    missing_percent = (missing_count / len(dataframe)).round(4) * 100

    summary = pd.DataFrame(
        {
            "Column": dataframe.columns,
            "Missing Values": missing_count.values,
            "Missing Percentage": missing_percent.values,
        }
    )

    summary = summary.sort_values(
        by="Missing Values",
        ascending=False,
    )

    return summary.reset_index(drop=True)


# ==========================================================
# COLUMN INFORMATION
# ==========================================================


def column_information(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate metadata for each column.

    Returns
    -------
    pd.DataFrame
    """
    info = pd.DataFrame(
        {
            "Column": dataframe.columns,
            "Data Type": dataframe.dtypes.astype(str).values,
            "Non-Null Count": dataframe.count().values,
            "Null Count": dataframe.isna().sum().values,
            "Unique Values": dataframe.nunique().values,
        }
    )

    return info


# ==========================================================
# DATA TYPE SUMMARY
# ==========================================================


def datatype_summary(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Count columns by datatype.
    """
    summary = (
        dataframe.dtypes.astype(str)
        .value_counts()
        .rename_axis("Data Type")
        .reset_index(name="Count")
    )

    return summary


# ==========================================================
# NUMERICAL COLUMNS
# ==========================================================


def numerical_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Return numerical columns.
    """
    return dataframe.select_dtypes(include="number").columns.tolist()


# ==========================================================
# CATEGORICAL COLUMNS
# ==========================================================


def categorical_columns(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Return categorical columns.
    """
    return dataframe.select_dtypes(include=["object", "category"]).columns.tolist()


# ==========================================================
# NUMERICAL SUMMARY
# ==========================================================


def numerical_summary(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate descriptive statistics
    for all numerical columns.
    """
    numeric_df = dataframe[numerical_columns(dataframe)]

    summary = pd.DataFrame(index=numeric_df.columns)

    summary["Count"] = numeric_df.count()
    summary["Missing"] = numeric_df.isna().sum()
    summary["Mean"] = numeric_df.mean(numeric_only=True)
    summary["Median"] = numeric_df.median(numeric_only=True)
    summary["Std"] = numeric_df.std(numeric_only=True)
    summary["Variance"] = numeric_df.var(numeric_only=True)
    summary["Minimum"] = numeric_df.min(numeric_only=True)
    summary["25%"] = numeric_df.quantile(0.25)
    summary["75%"] = numeric_df.quantile(0.75)
    summary["Maximum"] = numeric_df.max(numeric_only=True)

    summary["IQR"] = summary["75%"] - summary["25%"]

    return summary.round(2).reset_index(names="Column")


# ==========================================================
# CATEGORICAL SUMMARY
# ==========================================================


def categorical_summary(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate summary statistics
    for categorical columns.
    """
    rows = []

    for column in categorical_columns(dataframe):

        mode = dataframe[column].mode(dropna=True)

        rows.append(
            {
                "Column": column,
                "Unique Values": dataframe[column].nunique(),
                "Missing": dataframe[column].isna().sum(),
                "Top Value": mode.iloc[0] if not mode.empty else None,
                "Top Frequency": dataframe[column].value_counts(dropna=True).max(),
            }
        )

    return pd.DataFrame(rows)


# ==========================================================
# DATASET PROFILE
# ==========================================================


def dataset_profile(
    dataframe: pd.DataFrame,
) -> dict[str, object]:
    """
    Generate a complete dataset profile.
    """
    profile = {
        "Rows": len(dataframe),
        "Columns": len(dataframe.columns),
        "Memory Usage (MB)": dataframe_memory_usage(dataframe),
        "Duplicate Rows": duplicate_count(dataframe),
        "Duplicate Percentage": duplicate_percentage(dataframe),
        "Missing Cells": int(dataframe.isna().sum().sum()),
        "Numerical Columns": len(numerical_columns(dataframe)),
        "Categorical Columns": len(categorical_columns(dataframe)),
    }

    return profile


# ==========================================================
# MARKDOWN TABLE
# ==========================================================


def dataframe_to_markdown(
    dataframe: pd.DataFrame,
) -> str:
    """
    Convert DataFrame to markdown table.
    """
    return dataframe.to_markdown(
        index=False,
        tablefmt="github",
    )


# ==========================================================
# MARKDOWN SECTION
# ==========================================================


def markdown_heading(
    title: str,
    level: int = 1,
) -> str:
    """
    Generate markdown heading.
    """
    return f"{'#' * level} {title}\n\n"


def markdown_text(
    text: str,
) -> str:
    """
    Format markdown paragraph.
    """
    return f"{text}\n\n"


# ==========================================================
# REPORT BUILDERS
# ==========================================================


def markdown_key_value_table(
    data: dict[str, object],
) -> str:
    """
    Convert a dictionary into a markdown key-value table.

    Parameters
    ----------
    data : dict[str, object]

    Returns
    -------
    str
    """
    lines = [
        "| Metric | Value |",
        "|--------|-------|",
    ]

    for key, value in data.items():
        lines.append(f"| {key} | {value} |")

    return "\n".join(lines) + "\n"


def markdown_dataframe_section(
    title: str,
    dataframe: pd.DataFrame,
    level: int = 2,
) -> str:
    """
    Create a markdown section containing
    a heading and DataFrame.

    Parameters
    ----------
    title : str
    dataframe : pd.DataFrame
    level : int

    Returns
    -------
    str
    """
    return markdown_heading(title, level) + dataframe_to_markdown(dataframe) + "\n\n"


# ==========================================================
# DATAFRAME HELPERS
# ==========================================================


def safe_copy(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Return a deep copy of a DataFrame.
    """
    return dataframe.copy(deep=True)


def sort_dataframe(
    dataframe: pd.DataFrame,
    by: str,
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Return a sorted DataFrame.
    """
    return dataframe.sort_values(
        by=by,
        ascending=ascending,
    ).reset_index(drop=True)


def top_n(
    dataframe: pd.DataFrame,
    by: str,
    n: int = 10,
) -> pd.DataFrame:
    """
    Return the top N rows sorted by a column.
    """
    return (
        dataframe.sort_values(
            by=by,
            ascending=False,
        )
        .head(n)
        .reset_index(drop=True)
    )


# ==========================================================
# COLUMN UTILITIES
# ==========================================================


def rename_columns_lowercase(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Return a DataFrame with normalized column names.
    """
    df = dataframe.copy()

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    return df


def percentage(
    value: float,
    total: float,
) -> float:
    """
    Calculate percentage safely.
    """
    if total == 0:
        return 0.0

    return round((value / total) * 100, 2)


# ==========================================================
# VALUE COUNT HELPERS
# ==========================================================


def frequency_table(
    dataframe: pd.DataFrame,
    column: str,
) -> pd.DataFrame:
    """
    Return frequency table for a categorical column.
    """
    counts = dataframe[column].value_counts(dropna=False).rename("Count").reset_index()

    counts.columns = [column, "Count"]

    counts["Percentage"] = (counts["Count"] / len(dataframe) * 100).round(2)

    return counts


# ==========================================================
# GROUPING HELPERS
# ==========================================================


def grouped_average(
    dataframe: pd.DataFrame,
    group_column: str,
    value_column: str,
) -> pd.DataFrame:
    """
    Calculate average of a numeric column
    grouped by another column.
    """
    return (
        dataframe.groupby(group_column)[value_column]
        .mean()
        .round(2)
        .reset_index()
        .rename(columns={value_column: f"Average {value_column}"})
    )


def grouped_median(
    dataframe: pd.DataFrame,
    group_column: str,
    value_column: str,
) -> pd.DataFrame:
    """
    Calculate median grouped by a column.
    """
    return (
        dataframe.groupby(group_column)[value_column]
        .median()
        .round(2)
        .reset_index()
        .rename(columns={value_column: f"Median {value_column}"})
    )


# ==========================================================
# TIMESTAMP
# ==========================================================

from datetime import datetime


def generation_timestamp() -> str:
    """
    Return current timestamp.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
