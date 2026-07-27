"""
CareerLens
-----------

Global Styling

Injects the application's CSS.
All reusable UI components should live in utils/ui.py.
"""

from __future__ import annotations
from turtle import color

import streamlit as st

from utils.theme import (
    PRIMARY_COLOR,
    BACKGROUND_COLOR,
    CARD_COLOR,
    TEXT_COLOR,
    BORDER_COLOR,
    SUCCESS_COLOR,
    TEXT_SECONDARY,
    WARNING_COLOR,
    ERROR_COLOR,
    FONT_FAMILY,
    CARD_RADIUS,
    SHADOW,
    TRANSITION,
)


def apply_global_styles() -> None:
    """
    Inject the global CSS used throughout the application.
    Call once at the top of every page.
    """

    st.markdown(
        f"""
<style>

/* ============================================================
   GOOGLE FONT
============================================================ */

@import url('https://fonts.googleapis.com/css2?family={FONT_FAMILY.replace(" ", "+")}:wght@300;400;500;600;700&display=swap');

/* ============================================================
   GLOBAL
============================================================ */

html,
body,
[class*="css"] {{
    font-family: '{FONT_FAMILY}', sans-serif;
}}

.stApp {{
    background-color: {BACKGROUND_COLOR};
    color: {TEXT_COLOR};
}}

/* ============================================================
   MAIN CONTAINER
============================================================ */

.block-container {{
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
    max-width: 1600px;
}}

/* ============================================================
   SIDEBAR
============================================================ */

[data-testid="stSidebar"] {{
    background-color: {CARD_COLOR};
    border-right: 1px solid {BORDER_COLOR};
}}

[data-testid="stSidebar"] * {{
    color: {TEXT_COLOR};
}}

h1{{
    font-size:2.3rem;
    font-weight:700;
    letter-spacing:-0.03em;
    margin-bottom:0.25rem;
}}

h2{{
    font-size:1.7rem;
    font-weight:650;
    margin-top:1.8rem;
}}

h3{{
    font-size:1.25rem;
    font-weight:600;
}}

/* ============================================================
   BUTTONS
============================================================ */

.stButton > button {{

    width: 100%;

    border-radius: {CARD_RADIUS};

    border: none;

    background: {PRIMARY_COLOR};

    color: white;

    font-weight: 600;

    transition: {TRANSITION};

    padding: 0.65rem 1rem;
}}

.stButton > button:hover {{

    transform: translateY(-2px);

    filter: brightness(1.05);

    box-shadow: {SHADOW};
}}

/* ============================================================
   METRIC
============================================================ */

[data-testid="stMetric"] {{
    background: {CARD_COLOR};
    border: 1px solid {BORDER_COLOR};
    border-radius: {CARD_RADIUS};
    padding: 1rem;
    box-shadow: {SHADOW};
    transition: {TRANSITION};
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-3px);
}}

[data-testid="stMetricLabel"] {{
    color: {TEXT_SECONDARY} !important;
    font-size: 0.9rem;
    font-weight: 500;
}}

[data-testid="stMetricValue"] {{
    color: {TEXT_COLOR} !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}}
/* ============================================================
   INPUTS
============================================================ */

.stTextInput input,
.stNumberInput input{{
    background:#1E293B !important;

    color:#F8FAFC !important;
    
    -webkit-text-fill-color: #F8FAFC !important;

    border:1px solid #475569 !important;

    border-radius:12px;
}}
.stSelectbox div[data-baseweb="select"] {{
    background:#1E293B !important;

    color:#F8FAFC !important;
    
    border-radius: 12px;
}}

.stTextInput input::placeholder{{
    color:#94A3B8 !important;
    opacity: 1 !important;
}}

/* -----------------------------
   Select Boxes
------------------------------*/

div[data-baseweb="select"] {{
    background: #1E293B !important;
    color: #F8FAFC !important;
    border-radius: 12px;
}}

div[data-baseweb="select"] * {{
    color: #F8FAFC !important;
}}

/* -----------------------------
   Dropdown Menu
------------------------------*/

ul[role="listbox"] {{
    background: #1E293B !important;
}}

ul[role="listbox"] li {{
    color: #F8FAFC !important;
}}

/* ============================================================
   STREAMLIT 1.60+ SELECTBOX
============================================================ */

input[data-rac]{{
    background:#1E293B !important;

    color:#F8FAFC !important;

    -webkit-text-fill-color:#F8FAFC !important;

    caret-color:#F8FAFC !important;
}}

input[data-rac]::placeholder{{
    color:#94A3B8 !important;
}}

div[role="listbox"]{{
    background:#1E293B !important;
}}

div[role="option"]{{
    background:#1E293B !important;
    color:#F8FAFC !important;
}}


/* ============================================================
   TABLES
============================================================ */

[data-testid="stDataFrame"] {{

    border-radius: 16px;

    border: 1px solid {BORDER_COLOR};

    overflow: hidden;
    
     background: {CARD_COLOR};

    box-shadow: {SHADOW};
    
    padding:8px
}}

/* ============================================================
   PLOTS
============================================================ */

.js-plotly-plot {{
    border-radius:{CARD_RADIUS};
    
    overflow:hidden;
    background:{CARD_COLOR};
    padding:12px;
    border:1px solid {BORDER_COLOR};
    box-shadow:{SHADOW};
    transition:.25s ease;
}}
.js-plotly-plot:hover{{

    transform:translateY(-4px);

    box-shadow:0 16px 40px rgba(0,0,0,.40);
}}

/* ============================================================
   TABS
============================================================ */

button[data-baseweb="tab"] {{

    border-radius: 10px;

    padding: .5rem 1rem;

    font-weight: 600;
}}

button[data-baseweb="tab"][aria-selected="true"] {{

    background: {PRIMARY_COLOR};

    color: white;
}}

/* ============================================================
   ALERT COLORS
============================================================ */

.success {{
    color: {SUCCESS_COLOR};
}}

.warning {{
    color: {WARNING_COLOR};
}}

.error {{
    color: {ERROR_COLOR};
}}

details {{
    border-radius: 12px;
}}

.streamlit-expanderHeader {{
    font-weight: 600;
}}
[data-testid="stSidebar"] hr{{
    margin:18px 0;
}}


/* ============================================================
   SCROLLBAR
============================================================ */

::-webkit-scrollbar {{
    width: 8px;
}}

::-webkit-scrollbar-track {{
    background: #F1F5F9;
}}

::-webkit-scrollbar-thumb {{
    background: #CBD5E1;
    border-radius: 20px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: #94A3B8;
}}

</style>
""",
        unsafe_allow_html=True,
    )
