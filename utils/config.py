"""
CareerLens
-----------

Application configuration.

Responsible for:
- Streamlit page configuration
- Project paths
- Dataset discovery
- Export directories
"""

from pathlib import Path
import streamlit as st

from utils.constants import (
    DATA_DIR,
    PAGE_TITLE,
    PAGE_ICON,
    LAYOUT,
    INITIAL_SIDEBAR_STATE,
    ROOT_DIR,
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    ANALYTICS_DATA_DIR,
    EXPORTS_DIR,
)

# ============================================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================================

def configure_page() -> None:
    """
    Configure the Streamlit application.

    Call this once at the top of every page.
    """
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout=LAYOUT,
        initial_sidebar_state=INITIAL_SIDEBAR_STATE,
    )


# ============================================================================
# CREATE REQUIRED DIRECTORIES
# ============================================================================

def create_project_directories() -> None:
    """
    Ensure all required project directories exist.
    """

    directories = [
        DATA_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        ANALYTICS_DATA_DIR,
        EXPORTS_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


# ============================================================================
# DATASET DISCOVERY
# ============================================================================

def list_csv_files(folder: Path) -> list[Path]:
    """
    Return every CSV file inside a folder.

    Parameters
    ----------
    folder : Path

    Returns
    -------
    list[Path]
    """

    if not folder.exists():
        return []

    return sorted(folder.glob("*.csv"))


# ============================================================================
# DATASET LOCATIONS
# ============================================================================

RAW_DATA = list_csv_files(RAW_DATA_DIR)

PROCESSED_DATA = list_csv_files(PROCESSED_DATA_DIR)

ANALYTICS_DATA = list_csv_files(ANALYTICS_DATA_DIR)


# ============================================================================
# STARTUP INITIALIZATION
# ============================================================================

create_project_directories()