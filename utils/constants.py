"""
CareerLens
-----------

Application-wide constants.

This module centralizes values that are reused across the project
to avoid hardcoding strings, colors, icons, and default settings.
"""

from pathlib import Path

# ============================================================================
# APPLICATION INFORMATION
# ============================================================================

APP_NAME = "CareerLens"

APP_VERSION = "1.0.0"

APP_DESCRIPTION = (
    "An interactive analytics platform for exploring job market trends, "
    "salary insights, hiring patterns, and career opportunities."
)

AUTHOR = "Bhanoday Kurma"

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

PAGE_TITLE = APP_NAME

PAGE_ICON = "📊"

LAYOUT = "wide"

INITIAL_SIDEBAR_STATE = "expanded"

# ============================================================================
# PROJECT DIRECTORIES
# ============================================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = ROOT_DIR / "assets"

DATA_DIR = ROOT_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"

PROCESSED_DATA_DIR = DATA_DIR / "processed"

ANALYTICS_DATA_DIR = DATA_DIR / "analytics"

EXPORTS_DIR = ROOT_DIR / "exports"

# ============================================================================
# THEME COLORS
# ============================================================================

PRIMARY_COLOR = "#2563EB"

SECONDARY_COLOR = "#0F172A"

SUCCESS_COLOR = "#22C55E"

WARNING_COLOR = "#F59E0B"

ERROR_COLOR = "#EF4444"

INFO_COLOR = "#3B82F6"

BACKGROUND_COLOR = "#F8FAFC"

CARD_COLOR = "#FFFFFF"

TEXT_COLOR = "#111827"

BORDER_COLOR = "#E5E7EB"

# ============================================================================
# DEFAULT CHART SETTINGS
# ============================================================================

DEFAULT_CHART_HEIGHT = 450

DEFAULT_CHART_WIDTH = None

PLOT_TEMPLATE = "plotly_white"

# ============================================================================
# KPI LABELS
# ============================================================================

KPI_TOTAL_JOBS = "Total Jobs"

KPI_TOTAL_COMPANIES = "Companies"

KPI_TOTAL_LOCATIONS = "Locations"

KPI_TOTAL_INDUSTRIES = "Industries"

KPI_AVERAGE_SALARY = "Average Salary"

KPI_MAXIMUM_SALARY = "Maximum Salary"

KPI_REMOTE_PERCENTAGE = "Remote Jobs"

KPI_AVERAGE_SKILLS = "Avg Skills / Job"

# ============================================================================
# SIDEBAR
# ============================================================================

SIDEBAR_TITLE = "CareerLens"

SIDEBAR_SUBTITLE = "Job Market Analytics"

# ============================================================================
# FOOTER
# ============================================================================

FOOTER_TEXT = "Built with Streamlit • Plotly • Pandas • SQLite"
