"""
CareerLens
-----------

Reusable Plotly Chart Library

Every dashboard page should use these functions
instead of writing Plotly code repeatedly.
"""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ==========================================================
# GLOBAL THEME
# ==========================================================

from utils.theme import (
    PRIMARY_COLOR,
    CARD_COLOR,
    TEXT_COLOR,
    BORDER_COLOR,
    FONT_FAMILY,
    DEFAULT_CHART_HEIGHT,
    PLOT_TEMPLATE,
)

COLOR_SEQUENCE = [
    PRIMARY_COLOR,
    "#10B981",
    "#F59E0B",
    "#EF4444",
    "#8B5CF6",
    "#14B8A6",
]

FONT = dict(
    family=FONT_FAMILY,
    size=14,
    color=TEXT_COLOR,
)

# ==========================================================
# APPLY COMMON LAYOUT
# ==========================================================


def apply_layout(fig):

    fig.update_layout(
        template=PLOT_TEMPLATE,
        height=DEFAULT_CHART_HEIGHT,
        font=FONT,
        paper_bgcolor=CARD_COLOR,
        plot_bgcolor=CARD_COLOR,
        title=dict(
            x=0.02,
            xanchor="left",
            font=dict(size=22, color=TEXT_COLOR),
        ),
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.20,
            xanchor="center",
            x=0.5,
        ),
        hovermode="x unified",
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        showline=False,
        gridcolor=BORDER_COLOR,
        color=TEXT_COLOR,
    )

    fig.update_yaxes(
        gridcolor=BORDER_COLOR,
        zeroline=False,
        showline=False,
        color=TEXT_COLOR,
    )

    return fig


# ==========================================================
# BAR CHART
# ==========================================================


def create_bar_chart(
    data,
    x,
    y,
    title,
):

    fig = px.bar(
        data,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=[PRIMARY_COLOR],
    )
    fig.update_traces(
        marker_line_width=0,
    )

    return apply_layout(fig)


# ==========================================================
# LINE CHART
# ==========================================================


def create_line_chart(
    data,
    x,
    y,
    title,
):

    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        markers=True,
    )

    fig.update_traces(
        line_width=3,
        marker_size=8,
    )

    return apply_layout(fig)


# ==========================================================
# PIE CHART
# ==========================================================


def create_pie_chart(
    data,
    names,
    values,
    title,
):

    fig = px.pie(
        data,
        names=names,
        values=values,
        title=title,
        color_discrete_sequence=COLOR_SEQUENCE,
        hole=0.45,
    )
    fig.update_traces(
        textinfo="percent+label",
        pull=[0.02] * len(data),
    )

    return apply_layout(fig)


# ==========================================================
# HISTOGRAM
# ==========================================================


def create_histogram(
    data,
    column,
    title,
):

    fig = px.histogram(
        data,
        x=column,
        title=title,
        nbins=40,
        color_discrete_sequence=[PRIMARY_COLOR],
    )
    fig.update_traces(
        marker_line_width=0,
    )

    return apply_layout(fig)


# ==========================================================
# BOX PLOT
# ==========================================================


def create_boxplot(
    data,
    x,
    y,
    title,
):

    fig = px.box(
        data,
        x=x,
        y=y,
        title=title,
        color=x,
        color_discrete_sequence=COLOR_SEQUENCE,
    )

    return apply_layout(fig)


# ==========================================================
# SCATTER
# ==========================================================


def create_scatter(
    data,
    x,
    y,
    title,
):

    fig = px.scatter(
        data,
        x=x,
        y=y,
        title=title,
        color_discrete_sequence=[PRIMARY_COLOR],
    )

    return apply_layout(fig)


# ==========================================================
# KPI CARD
# ==========================================================


def create_kpi_card(
    title: str,
    value,
    delta=None,
):

    return {
        "title": title,
        "value": value,
        "delta": delta,
    }
