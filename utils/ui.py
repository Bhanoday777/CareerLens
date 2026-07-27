"""
CareerLens
-----------

Reusable UI components.

These functions provide consistent UI elements across the application.
"""

from __future__ import annotations

import streamlit as st


# ============================================================
# PAGE HEADER
# ============================================================

def page_header(title: str, subtitle: str | None = None) -> None:
    """
    Display a consistent page header.
    """

    st.title(title)

    if subtitle:
        st.caption(subtitle)

    st.divider()


# ============================================================
# SECTION HEADER
# ============================================================

def section_header(title: str, subtitle: str | None = None) -> None:
    """
    Display a section heading.
    """

    st.subheader(title)

    if subtitle:
        st.caption(subtitle)


# ============================================================
# METRIC CARD
# ============================================================

def metric_card(
    title: str,
    value,
    delta: str | None = None,
    help_text: str | None = None,
):
    """
    Wrapper around st.metric.
    """

    st.metric(
        label=title,
        value=value,
        delta=delta,
        help=help_text,
        border=True,
    )


# ============================================================
# INFO CARD
# ============================================================

def info_card(
    title: str,
    content: str,
):
    """
    Display information inside a styled container.
    """

    with st.container(border=True):
        st.markdown(f"### {title}")
        st.write(content)


# ============================================================
# STATUS BADGE
# ============================================================

def status_badge(status: str) -> None:
    """
    Display a colored badge using Streamlit status styles.
    """

    status_lower = status.lower()

    if status_lower == "remote":
        st.success(status)

    elif status_lower == "hybrid":
        st.warning(status)

    elif status_lower == "onsite":
        st.info(status)

    else:
        st.caption(status)


# ============================================================
# EMPTY STATE
# ============================================================

def empty_state(message: str = "No data available.") -> None:
    """
    Display a standard empty state.
    """

    st.info(message)


# ============================================================
# COMING SOON
# ============================================================

def coming_soon(feature_name: str) -> None:
    """
    Placeholder for unfinished sections.
    """

    st.warning(f"🚧 {feature_name} is coming soon.")


# ============================================================
# SUCCESS MESSAGE
# ============================================================

def success_message(message: str) -> None:
    st.success(message)


# ============================================================
# ERROR MESSAGE
# ============================================================

def error_message(message: str) -> None:
    st.error(message)


# ============================================================
# WARNING MESSAGE
# ============================================================

def warning_message(message: str) -> None:
    st.warning(message)


# ============================================================
# INFO MESSAGE
# ============================================================

def info_message(message: str) -> None:
    st.info(message)


# ============================================================
# HORIZONTAL DIVIDER
# ============================================================

def divider() -> None:
    st.divider()


# ============================================================
# SPACING
# ============================================================

def vertical_space(lines: int = 1) -> None:
    """
    Insert vertical spacing.
    """

    for _ in range(lines):
        st.write("")