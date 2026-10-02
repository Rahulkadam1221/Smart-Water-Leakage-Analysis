"""
Smart Water Leakage Detection Dashboard
========================================
A professional analytics dashboard for monitoring smart city water infrastructure.
Built with Streamlit + Plotly for interactive data exploration.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import os
import joblib
import base64
import textwrap

warnings.filterwarnings("ignore")

def get_bg_base64(image_path: str) -> str:
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

# ──────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Water Leakage Detection",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# CUSTOM CSS — Premium White / Light Theme
# ──────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
    /* ── Hide Streamlit Branding ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    [data-testid="stDecoration"] {display: none;}

    /* ── Animations ── */
    @keyframes shimmer {
        0%   { background-position: -200% 0; }
        100% { background-position:  200% 0; }
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.45; }
    }
    @keyframes headerGlow {
        0%, 100% { box-shadow: 0 4px 30px rgba(37,99,235,0.08), 0 1px 0 rgba(255,255,255,0.9) inset; }
        50%       { box-shadow: 0 4px 40px rgba(37,99,235,0.15), 0 1px 0 rgba(255,255,255,0.9) inset; }
    }

    /* ── Global ── */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: #f0f4f9 !important;
        color: #1e293b !important;
        font-family: 'Inter', 'Segoe UI', sans-serif !important;
    }
    [data-testid="stMain"], .main {
        background: #f0f4f9 !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1480px !important;
        animation: fadeInUp 0.4s ease;
    }

    /* ── Premium White Sidebar ── */
    [data-testid="stSidebar"] {
        background: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
        box-shadow: 4px 0 24px rgba(0,0,0,0.06) !important;
    }
    [data-testid="stSidebar"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #2563eb, #0ea5e9, #7c3aed, #2563eb);
        background-size: 200% 100%;
        animation: shimmer 4s linear infinite;
    }
    [data-testid="stSidebar"] * {
        color: #374151 !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #6b7280 !important;
        font-size: 0.86rem !important;
        padding: 7px 10px !important;
        border-radius: 8px !important;
        transition: all 0.18s ease !important;
        font-weight: 500 !important;
        cursor: pointer !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: #eff6ff !important;
        color: #2563eb !important;
    }
    [data-testid="stSidebar"] [aria-checked="true"] + label,
    [data-testid="stSidebar"] .stRadio [aria-checked="true"] ~ label {
        color: #2563eb !important;
        background: #dbeafe !important;
        font-weight: 600 !important;
    }

    /* ── Flipkart / Amazon Filter Styling ── */
    .fk-filter-title {
        font-size: 15px;
        font-weight: 800;
        color: #212121;
        letter-spacing: 0.3px;
        text-transform: uppercase;
        font-family: 'Inter', Roboto, sans-serif;
        padding-top: 4px;
    }
    .fk-section-header {
        font-size: 11.5px;
        font-weight: 700;
        text-transform: uppercase;
        color: #212121;
        letter-spacing: 0.5px;
        margin-top: 14px;
        margin-bottom: 6px;
        font-family: 'Inter', Roboto, sans-serif;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .fk-divider {
        height: 1px;
        background: #f0f0f0;
        margin: 12px 0 8px 0;
    }
    
    /* Checkbox Styling like Amazon & Flipkart */
    [data-testid="stSidebar"] [data-testid="stCheckbox"] {
        padding: 3px 4px !important;
        margin-bottom: 2px !important;
        border-radius: 4px !important;
        transition: background 0.12s ease !important;
    }
    [data-testid="stSidebar"] [data-testid="stCheckbox"]:hover {
        background: #f8fafc !important;
    }
    [data-testid="stSidebar"] [data-testid="stCheckbox"] label {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, Roboto, sans-serif !important;
        font-size: 0.83rem !important;
        color: #212121 !important;
        cursor: pointer !important;
    }
    [data-testid="stSidebar"] [data-testid="stCheckbox"] [data-baseweb="checkbox"] span {
        border-radius: 3px !important;
        border: 1.5px solid #c2c2c2 !important;
    }
    [data-testid="stSidebar"] [data-testid="stCheckbox"] [aria-checked="true"] {
        background-color: #2874f0 !important;
        border-color: #2874f0 !important;
    }
    [data-testid="stSidebar"] [data-testid="stCheckbox"] code {
        background: #f1f5f9 !important;
        color: #64748b !important;
        font-size: 0.72rem !important;
        border: 1px solid #e2e8f0 !important;
        padding: 1px 5px !important;
        font-weight: 500 !important;
        border-radius: 4px !important;
        margin-left: 4px !important;
    }
    
    /* CLEAR ALL Link styling (Flipkart Blue) */
    [data-testid="stSidebar"] [data-testid="stColumn"]:last-child button {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #2874f0 !important;
        font-weight: 800 !important;
        font-size: 0.72rem !important;
        text-transform: uppercase !important;
        padding: 0 !important;
        min-height: 28px !important;
        height: 28px !important;
        cursor: pointer !important;
        letter-spacing: 0.6px !important;
        float: right !important;
    }
    [data-testid="stSidebar"] [data-testid="stColumn"]:last-child button:hover {
        color: #1259c7 !important;
        text-decoration: underline !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    /* ── Reference UI Neumorphic & Glassmorphic Cards ── */
    .glass-card {
        background: rgba(255, 255, 255, 0.84) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.95) !important;
        border-radius: 22px !important;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.07), 0 2px 6px rgba(0, 0, 0, 0.02) !important;
        padding: 22px 24px;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 36px rgba(99, 102, 241, 0.12), 0 4px 10px rgba(0, 0, 0, 0.03) !important;
    }
    .ref-big-stat {
        font-size: 2.6rem;
        font-weight: 900;
        color: #1e1b4b;
        letter-spacing: -1.2px;
        line-height: 1.1;
        margin: 6px 0 14px 0;
    }
    .ref-seg-bar {
        height: 9px;
        border-radius: 6px;
        display: flex;
        overflow: hidden;
        gap: 3px;
        background: #e2e8f0;
        margin: 10px 0 14px 0;
    }
    .ref-seg-bar > div {
        height: 100%;
        border-radius: 4px;
        transition: width 0.4s ease;
    }
    .ref-legend-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 0;
        font-size: 0.82rem;
        color: #475569;
        font-weight: 500;
        border-bottom: 1px dashed rgba(226, 232, 240, 0.6);
    }
    .ref-legend-row:last-child {
        border-bottom: none;
    }
    .ref-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    .ref-pill-card {
        background: rgba(255, 255, 255, 0.86);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.95);
        border-radius: 18px;
        padding: 13px 18px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 14px;
        box-shadow: 0 4px 18px rgba(99, 102, 241, 0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .ref-pill-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 26px rgba(99, 102, 241, 0.12);
    }
    .ref-icon-box {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.25rem;
        flex-shrink: 0;
        color: #ffffff;
    }
    .ref-icon-purple {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
    }
    .ref-icon-cyan {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%);
        box-shadow: 0 4px 14px rgba(6, 182, 212, 0.35);
    }
    .ref-icon-amber {
        background: linear-gradient(135deg, #f59e0b 0%, #f43f5e 100%);
        box-shadow: 0 4px 14px rgba(245, 158, 11, 0.35);
    }

    /* ── Section Headers ── */
    .section-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: -0.3px;
        padding: 10px 16px;
        margin: 1.5rem 0 0.5rem 0;
        background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%);
        border-left: 3px solid #2563eb;
        border-radius: 0 10px 10px 0;
        position: relative;
    }
    .sub-header {
        font-size: 0.88rem;
        color: #94a3b8;
        margin-bottom: 1.2rem;
        margin-top: -0.2rem;
        font-weight: 400;
    }

    /* ── Premium Light Metric Cards ── */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 22px 18px 18px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.06);
        transition: transform 0.22s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.22s ease, border-color 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: #2563eb;
        border-radius: 16px 16px 0 0;
    }
    .metric-card:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 8px 30px rgba(37,99,235,0.12);
        border-color: #bfdbfe;
    }
    .metric-card .label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #94a3b8;
        margin-bottom: 10px;
        font-weight: 700;
    }
    .metric-card .value {
        font-size: 1.95rem;
        font-weight: 800;
        color: #1e40af;
        line-height: 1.1;
        letter-spacing: -1px;
    }
    .metric-card .delta {
        font-size: 0.76rem;
        color: #64748b;
        margin-top: 7px;
        font-weight: 500;
    }
    .metric-card.danger::before { background: #ef4444; }
    .metric-card.danger .value  { color: #dc2626; }
    .metric-card.warning::before{ background: #f59e0b; }
    .metric-card.warning .value { color: #d97706; }
    .metric-card.success::before{ background: #10b981; }
    .metric-card.success .value { color: #059669; }
    .metric-card.danger:hover   { box-shadow: 0 8px 30px rgba(239,68,68,0.12); border-color: #fecaca; }
    .metric-card.warning:hover  { box-shadow: 0 8px 30px rgba(245,158,11,0.12); border-color: #fde68a; }
    .metric-card.success:hover  { box-shadow: 0 8px 30px rgba(16,185,129,0.12); border-color: #a7f3d0; }

    /* ── Insight Boxes ── */
    .insight-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #2563eb;
        border-radius: 10px;
        padding: 13px 16px 13px 18px;
        margin-bottom: 10px;
        font-size: 0.89rem;
        color: #334155;
        line-height: 1.65;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        transition: box-shadow 0.2s ease, border-left-color 0.2s ease;
    }
    .insight-box:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.07); }
    .insight-box.warning {
        border-left-color: #f59e0b;
        background: #fffbeb;
        border-color: #fde68a;
    }
    .insight-box.danger {
        border-left-color: #ef4444;
        background: #fef2f2;
        border-color: #fecaca;
    }
    .insight-box.success {
        border-left-color: #10b981;
        background: #f0fdf4;
        border-color: #a7f3d0;
    }

    /* ── Alert Badges ── */
    .badge {
        display: inline-block;
        padding: 3px 11px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-critical { background: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
    .badge-high     { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }
    .badge-moderate { background: #fffbeb; color: #92400e; border: 1px solid #fde68a; }
    .badge-low      { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }

    /* ── Divider ── */
    hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.5rem 0; }

    /* ── Plotly Chart Containers ── */
    [data-testid="stPlotlyChart"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05), 0 4px 16px rgba(0,0,0,0.05);
        transition: box-shadow 0.25s ease, transform 0.25s ease;
    }
    [data-testid="stPlotlyChart"]:hover {
        box-shadow: 0 4px 20px rgba(37,99,235,0.1);
        transform: translateY(-2px);
    }

    /* ── Input Widgets ── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 10px !important;
        color: #374151 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important;
    }
    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.08) !important;
    }
    .stTextInput > div > div > input {
        background: #ffffff !important;
        border: 1px solid #d1d5db !important;
        border-radius: 10px !important;
        color: #374151 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #9ca3af !important; }

    /* ── Slider ── */
    [data-testid="stSlider"] [role="slider"] {
        background: #2563eb !important;
        border-color: #2563eb !important;
    }
    [data-testid="stSlider"] [data-testid="stSliderTrackFill"] {
        background: #2563eb !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #f1f5f9 !important;
        border-radius: 12px !important;
        padding: 4px !important;
        gap: 4px !important;
        border: 1px solid #e2e8f0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        color: #64748b !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.87rem !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: #ffffff !important;
        color: #2563eb !important;
        font-weight: 600 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }

    /* ── Download Button ── */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px !important;
        padding: 8px 18px !important;
        box-shadow: 0 2px 8px rgba(37,99,235,0.3) !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
        box-shadow: 0 6px 18px rgba(37,99,235,0.4) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Alerts ── */
    .stAlert {
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: #f8fafc !important;
        border-radius: 10px !important;
        border: 1px solid #e2e8f0 !important;
        color: #374151 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        transition: all 0.18s ease !important;
    }
    .streamlit-expanderHeader:hover {
        border-color: #bfdbfe !important;
        background: #eff6ff !important;
    }
    .streamlit-expanderContent {
        border: 1px solid #e2e8f0 !important;
        border-top: none !important;
        border-radius: 0 0 10px 10px !important;
        background: #ffffff !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

    /* ── Multiselect Tags ── */
    [data-baseweb="tag"] {
        background: #dbeafe !important;
        border: 1px solid #93c5fd !important;
        border-radius: 6px !important;
        color: #1e40af !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
    }

    /* ── Code ── */
    code {
        background: #f1f5f9 !important;
        color: #2563eb !important;
        border-radius: 5px !important;
        padding: 2px 7px !important;
        font-size: 0.84em !important;
        border: 1px solid #e2e8f0 !important;
    }

    /* ── Radio group labels in main content ── */
    .stRadio > label {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.88rem !important;
        color: #374151 !important;
        font-weight: 500 !important;
    }

    /* ── General headings ── */
    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        color: #0f172a !important;
    }
    p, span, li, td, th {
        font-family: 'Inter', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# DATA LOADING & CACHING
# ──────────────────────────────────────────────
@st.cache_data(show_spinner="Loading dataset…")
def load_data() -> pd.DataFrame:
    """Load and preprocess the smart meter dataset (parquet or CSV)."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "..", "data", "processed")

    # Try parquet first (smaller, faster), then CSV
    parquet_path = os.path.join(data_dir, "leakage_intelligence_dataset.parquet")
    csv_path = os.path.join(data_dir, "leakage_intelligence_dataset.csv")

    if os.path.exists(parquet_path):
        df = pd.read_parquet(parquet_path)
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        st.error("❌ Dataset not found! Please place 'leakage_intelligence_dataset.parquet' or '.csv' in data/processed/")
        st.stop()

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"]      = df["timestamp"].dt.date
    df["month"]     = df["timestamp"].dt.to_period("M").astype(str)
    df["day_of_week"] = df["timestamp"].dt.day_name()

    # Ordinal encodings for sorting
    sev_order  = {"Normal": 0, "Low Risk": 1, "Moderate Risk": 2, "High Risk": 3, "Critical Leak": 4}
    risk_order = {"Low Risk": 0, "Moderate Risk": 1, "High Risk": 2, "Critical": 3}
    df["sev_order"]  = df["leak_severity"].map(sev_order)
    df["risk_order"] = df["risk_level"].map(risk_order)
    return df


# ──────────────────────────────────────────────
# PLOTLY THEME DEFAULTS
# ──────────────────────────────────────────────
CHART_THEME = dict(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font_color="#334155",
    font_family="Inter, Segoe UI, sans-serif",
)
PALETTE = px.colors.sequential.Blues
COLOR_MAP_RISK = {
    "Low Risk":      "#10b981",
    "Moderate Risk": "#f59e0b",
    "High Risk":     "#ef4444",
    "Critical":      "#991b1b",
}
COLOR_MAP_SEV = {
    "Normal":        "#3b82f6",
    "Low Risk":      "#10b981",
    "Moderate Risk": "#f59e0b",
    "High Risk":     "#ef4444",
    "Critical Leak": "#991b1b",
}


def apply_theme(fig: go.Figure, title: str = "", height: int = 400) -> go.Figure:
    """Apply consistent premium white/light theme to every Plotly figure."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=14, color="#1e40af", family="Inter, sans-serif", weight=600),
            x=0.02, y=0.97,
        ),
        height=height,
        margin=dict(l=40, r=20, t=52, b=40),
        legend=dict(
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#e2e8f0",
            borderwidth=1,
            font=dict(color="#475569", size=11, family="Inter, sans-serif"),
        ),
        **CHART_THEME,
    )
    fig.update_xaxes(
        gridcolor="#f1f5f9",
        zerolinecolor="#e2e8f0",
        tickfont=dict(color="#94a3b8", size=10, family="Inter, sans-serif"),
        showline=False,
        linecolor="#e2e8f0",
    )
    fig.update_yaxes(
        gridcolor="#f1f5f9",
        zerolinecolor="#e2e8f0",
        tickfont=dict(color="#94a3b8", size=10, family="Inter, sans-serif"),
        showline=False,
        linecolor="#e2e8f0",
    )
    return fig



# ──────────────────────────────────────────────
# SIDEBAR — global filters
# ──────────────────────────────────────────────
def render_sidebar(df: pd.DataFrame):
    # ── Clean White Sidebar Branding with Reference UI Logo ──
    st.sidebar.markdown("""
    <div style="padding: 10px 4px 8px 4px;">
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:4px;">
            <div style="width:36px; height:36px; border-radius:50%; background:conic-gradient(from 180deg at 50% 50%, #7c3aed 0deg, #ec4899 180deg, #6366f1 360deg); padding:5px; box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35); flex-shrink:0;">
                <div style="width:100%; height:100%; background:#ffffff; border-radius:50%;"></div>
            </div>
            <div>
                <div style="font-family:'Inter',sans-serif; font-size:1.02rem; font-weight:800;
                            color:#1e1b4b; letter-spacing:-0.4px; line-height:1.2;">Water Monitor</div>
                <div style="font-family:'Inter',sans-serif; font-size:0.65rem; color:#8b5cf6; font-weight:700;
                            text-transform:uppercase; letter-spacing:1px; margin-top:1px;">Smart Infrastructure</div>
            </div>
        </div>
    </div>
    <div class="fk-divider"></div>
    """, unsafe_allow_html=True)

    # ── Wallpaper / Background Theme Selector ──
    st.sidebar.markdown('<div class="fk-section-header"><span>🖼️ Wallpaper Theme</span></div>', unsafe_allow_html=True)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bg_options = {
        "Option 1: Smart Water Grid Globe": os.path.join(base_dir, "assets", "bg_option1_globe.jpg"),
        "Option 2: Smart City Water Network": os.path.join(base_dir, "assets", "bg_option2_city_grid.jpg"),
        "Option 3: Crystalline Water Droplet Core": os.path.join(base_dir, "assets", "bg_option3_water_drop.jpg"),
        "Option 4: Clean Glass Gradient": "",
    }
    if "selected_bg" not in st.session_state:
        st.session_state["selected_bg"] = "Option 1: Smart Water Grid Globe"

    selected_bg = st.sidebar.selectbox(
        "Wallpaper Theme",
        list(bg_options.keys()),
        index=list(bg_options.keys()).index(st.session_state["selected_bg"]) if st.session_state["selected_bg"] in bg_options else 0,
        key="selected_bg",
        label_visibility="collapsed"
    )
    st.sidebar.markdown('<div class="fk-divider"></div>', unsafe_allow_html=True)

    # Dynamically inject background image style
    bg_path = bg_options.get(selected_bg, "")
    if bg_path and os.path.exists(bg_path):
        b64_bg = get_bg_base64(bg_path)
        st.markdown(f"""
        <style>
            [data-testid="stAppViewContainer"] {{
                background: url("data:image/jpeg;base64,{b64_bg}") no-repeat 56% center fixed !important;
                background-size: cover !important;
            }}
            [data-testid="stMain"], .main {{
                background: transparent !important;
            }}
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
                background: radial-gradient(circle at 60% 30%, #e0e7ff 0%, #f1f5f9 60%, #e2e8f0 100%) fixed !important;
            }
            [data-testid="stMain"], .main {
                background: transparent !important;
            }
        </style>
        """, unsafe_allow_html=True)

    # ── Flipkart / Amazon Filter Header with CLEAR ALL ──
    col_t, col_b = st.sidebar.columns([3, 2])
    with col_t:
        st.markdown('<div class="fk-filter-title">Filters</div>', unsafe_allow_html=True)
    with col_b:
        clear_clicked = st.button("CLEAR ALL", key="fk_clear_all", help="Reset all filters to default")

    # Options definition
    risk_options = ["Critical", "High Risk", "Moderate Risk", "Low Risk"]
    sev_options = ["Critical Leak", "High Risk", "Moderate Risk", "Low Risk", "Normal"]
    h_min, h_max = int(df["hour"].min()), int(df["hour"].max())
    hh_options = ["All Households (200)"] + sorted(df["household_id"].unique().tolist())

    # If CLEAR ALL clicked, reset state
    if clear_clicked:
        for opt in risk_options:
            st.session_state[f"fk_risk_{opt}"] = True
        for opt in sev_options:
            st.session_state[f"fk_sev_{opt}"] = True
        st.session_state["fk_hours"] = (h_min, h_max)
        st.session_state["fk_spike"] = 0.0
        st.session_state["fk_hh_select"] = "All Households (200)"
        st.rerun()

    # Pre-calculate category counts for display
    risk_counts = df["risk_level"].value_counts().to_dict()
    sev_counts = df["leak_severity"].value_counts().to_dict()

    # ── 1. RISK LEVEL CHECKBOXES (Flipkart/Amazon Facet) ──
    st.sidebar.markdown('<div class="fk-section-header"><span>Risk Level</span></div>', unsafe_allow_html=True)
    risk_icons = {
        "Critical": "🔴",
        "High Risk": "🟠",
        "Moderate Risk": "🟡",
        "Low Risk": "🟢",
    }
    sel_risk = []
    for opt in risk_options:
        key = f"fk_risk_{opt}"
        if key not in st.session_state:
            st.session_state[key] = True
        count = risk_counts.get(opt, 0)
        checked = st.sidebar.checkbox(
            f"{risk_icons.get(opt, '•')} {opt} &nbsp;`{count:,}`",
            value=st.session_state[key],
            key=key
        )
        if checked:
            sel_risk.append(opt)

    st.sidebar.markdown('<div class="fk-divider"></div>', unsafe_allow_html=True)

    # ── 2. LEAK SEVERITY CHECKBOXES (Flipkart/Amazon Facet) ──
    st.sidebar.markdown('<div class="fk-section-header"><span>Leak Severity</span></div>', unsafe_allow_html=True)
    sev_icons = {
        "Critical Leak": "🚨",
        "High Risk": "⚠️",
        "Moderate Risk": "⚡",
        "Low Risk": "💧",
        "Normal": "🔵",
    }
    sel_sev = []
    for opt in sev_options:
        key = f"fk_sev_{opt}"
        if key not in st.session_state:
            st.session_state[key] = True
        count = sev_counts.get(opt, 0)
        checked = st.sidebar.checkbox(
            f"{sev_icons.get(opt, '•')} {opt} &nbsp;`{count:,}`",
            value=st.session_state[key],
            key=key
        )
        if checked:
            sel_sev.append(opt)

    st.sidebar.markdown('<div class="fk-divider"></div>', unsafe_allow_html=True)

    # ── 3. TIME OF DAY (Flipkart/Amazon Range Slider) ──
    def fmt_hour(h):
        return f"{h:02d}:00 ({'AM' if h < 12 else 'PM'})"

    if "fk_hours" not in st.session_state:
        st.session_state["fk_hours"] = (h_min, h_max)

    sel_hours = st.sidebar.slider(
        "Time of Day",
        h_min, h_max,
        value=st.session_state["fk_hours"],
        key="fk_hours",
        label_visibility="collapsed",
        help="Filter by hour of day. 00:00–05:00 indicate persistent nocturnal leaks."
    )
    st.sidebar.markdown(f"""
    <div class="fk-section-header" style="margin-top:6px;">
        <span>Time of Day</span>
        <span style="font-size:10px; color:#878787; text-transform:none;">{fmt_hour(sel_hours[0])} – {fmt_hour(sel_hours[1])}</span>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div class="fk-divider"></div>', unsafe_allow_html=True)

    # ── 4. SPIKE RATIO / ANOMALY THRESHOLD ──
    if "fk_spike" not in st.session_state:
        st.session_state["fk_spike"] = 0.0

    spike_thresh = st.sidebar.slider(
        "Min Spike Ratio",
        0.0, float(df["spike_ratio"].max()),
        value=st.session_state["fk_spike"],
        step=0.1,
        key="fk_spike",
        label_visibility="collapsed",
        help="Filters records where water usage spiked X× above baseline."
    )
    spike_badge = "Severe Anomaly (≥3×)" if spike_thresh >= 3.0 else "Anomaly Zone (≥2×)" if spike_thresh >= 2.0 else "Mild Spike (≥1×)" if spike_thresh >= 1.0 else "All Records"
    spike_color = "#dc2626" if spike_thresh >= 3.0 else "#d97706" if spike_thresh >= 2.0 else "#059669" if spike_thresh >= 1.0 else "#878787"

    st.sidebar.markdown(f"""
    <div class="fk-section-header" style="margin-top:6px;">
        <span>Min Spike Ratio</span>
        <span style="font-size:10.5px; font-weight:600; color:{spike_color}; text-transform:none;">{spike_badge}</span>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown('<div class="fk-divider"></div>', unsafe_allow_html=True)

    # ── 5. HOUSEHOLD SEARCH (Clean Dropdown like Amazon/Flipkart) ──
    st.sidebar.markdown('<div class="fk-section-header"><span>Household Meter</span></div>', unsafe_allow_html=True)
    if "fk_hh_select" not in st.session_state:
        st.session_state["fk_hh_select"] = "All Households (200)"

    sel_hh = st.sidebar.selectbox(
        "Household Meter",
        hh_options,
        index=hh_options.index(st.session_state["fk_hh_select"]) if st.session_state["fk_hh_select"] in hh_options else 0,
        key="fk_hh_select",
        label_visibility="collapsed"
    )

    st.sidebar.markdown('<div class="fk-divider"></div>', unsafe_allow_html=True)

    # ── Apply filters to produce mask ──
    mask = (
        df["risk_level"].isin(sel_risk) &
        df["leak_severity"].isin(sel_sev) &
        df["hour"].between(*sel_hours) &
        (df["spike_ratio"] >= spike_thresh)
    )
    if sel_hh != "All Households (200)":
        mask &= (df["household_id"] == sel_hh)

    matched = mask.sum()
    pct = (matched / len(df) * 100) if len(df) > 0 else 0
    bar_color = "#10b981" if pct > 60 else "#f59e0b" if pct > 20 else "#ef4444"

    # ── Flipkart / Amazon "Results / Coverage" Card ──
    st.sidebar.markdown(f"""
    <div style="background:#ffffff; border:1px solid #e0e0e0; border-radius:8px; padding:12px 14px; margin-top:8px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
        <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:6px;">
            <div style="font-size:11px; text-transform:uppercase; font-weight:700; color:#878787; letter-spacing:0.5px;">Results</div>
            <div style="font-size:11px; font-weight:700; color:{bar_color};">{pct:.1f}% Match</div>
        </div>
        <div style="font-size:1.35rem; font-weight:800; color:#212121; font-family:'Inter',sans-serif; letter-spacing:-0.5px; line-height:1.1;">
            {matched:,}
        </div>
        <div style="font-size:11px; color:#878787; margin-bottom:8px;">of {len(df):,} total readings</div>
        <div style="background:#f0f0f0; border-radius:4px; height:4px; overflow:hidden;">
            <div style="width:{min(pct,100):.0f}%; background:{bar_color}; height:100%; border-radius:4px; transition:width 0.3s ease;"></div>
        </div>
    </div>
    <div style="font-size:11px; color:#878787; text-align:center; margin-top:8px; margin-bottom:6px;">
        📅 {df['timestamp'].min().strftime('%d %b %Y')} → {df['timestamp'].max().strftime('%d %b %Y')}
    </div>
    """, unsafe_allow_html=True)

    # ── User Profile & Notification Bell (Reference UI style) ──
    st.sidebar.markdown("""
    <div style="margin-top:14px; padding:10px 8px; border-top:1px solid #e2e8f0; display:flex; align-items:center; justify-content:space-between;">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:34px; height:34px; border-radius:50%; background:linear-gradient(135deg, #a855f7, #6366f1); display:flex; align-items:center; justify-content:center; color:#fff; font-weight:800; font-size:0.8rem; box-shadow:0 3px 10px rgba(99,102,241,0.35);">
                RA
            </div>
            <div>
                <div style="font-family:'Inter',sans-serif; font-size:0.78rem; font-weight:800; color:#1e1b4b;">Chief Engineer</div>
                <div style="font-family:'Inter',sans-serif; font-size:0.65rem; color:#10b981; font-weight:700;">● IoT Grid Online</div>
            </div>
        </div>
        <div style="position:relative; width:30px; height:30px; background:#f8fafc; border-radius:50%; border:1px solid #e2e8f0; display:flex; align-items:center; justify-content:center; font-size:0.85rem; cursor:pointer;" title="Notifications Active">
            🔔
            <span style="position:absolute; top:3px; right:3px; width:6px; height:6px; background:#ef4444; border-radius:50%; border:1px solid #fff;"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    return df[mask].copy()


# ──────────────────────────────────────────────
# PAGE 1 — SYSTEM OVERVIEW
# ──────────────────────────────────────────────
def page_overview(df: pd.DataFrame):
    total_records = len(df)
    total_households = df["household_id"].nunique() if total_records else 0
    total_leaks = int(df["leak_flag_detected"].sum()) if total_records else 0
    leak_pct = (total_leaks / total_records * 100) if total_records else 0

    risk_counts = df["risk_level"].value_counts()
    low_cnt = int(risk_counts.get("Low Risk", 0))
    mod_cnt = int(risk_counts.get("Moderate Risk", 0))
    high_cnt = int(risk_counts.get("High Risk", 0))
    crit_cnt = int(risk_counts.get("Critical", 0))

    low_pct = (low_cnt / total_records * 100) if total_records else 0
    mod_pct = (mod_cnt / total_records * 100) if total_records else 0
    high_pct = (high_cnt / total_records * 100) if total_records else 0
    crit_pct = (crit_cnt / total_records * 100) if total_records else 0

    avg_usage = df["water_usage_liters"].mean() if total_records else 0
    total_liters = int(df["water_usage_liters"].sum()) if total_records else 0
    avg_spike = df["spike_ratio"].mean() if total_records else 1.0

    # Diurnal / Time breakdown
    if total_records:
        night_leaks = len(df[(df["leak_flag_detected"] == 1) & (df["hour"].between(0, 5))])
        morning_leaks = len(df[(df["leak_flag_detected"] == 1) & (df["hour"].between(6, 12))])
        evening_leaks = max(0, total_leaks - night_leaks - morning_leaks)
    else:
        night_leaks = morning_leaks = evening_leaks = 0

    night_pct = (night_leaks / total_leaks * 100) if total_leaks else 0
    morning_pct = (morning_leaks / total_leaks * 100) if total_leaks else 0
    evening_pct = (evening_leaks / total_leaks * 100) if total_leaks else 0

    # Household / Network Coverage
    coverage_pct = min(100, int((total_households / 200.0) * 100)) if total_households else 0

    # Estimated Water Loss cost and peak flow
    leak_liters = df[df["leak_flag_detected"] == 1]["water_usage_liters"].sum() if total_records else 0
    est_loss_cost = leak_liters * 0.28  # financial telemetry estimate
    peak_flow = df["water_usage_liters"].max() if total_records else 0

    # Top households by leak incidents for the mini table
    top_hh_rows = []
    if total_records:
        top_hh = (
            df[df["leak_flag_detected"] == 1]
            .groupby("household_id")
            .agg(events=("leak_flag_detected", "count"), total_l=("water_usage_liters", "sum"))
            .sort_values(by="events", ascending=False)
            .head(3)
            .reset_index()
        )
        for _, r in top_hh.iterrows():
            top_hh_rows.append(
                f'<div style="display:flex; justify-content:space-between; align-items:center;">'
                f'<span style="font-weight:600; color:#334155;">{str(r["household_id"]).replace("_", " ")}</span>'
                f'<span style="color:#64748b;">{int(r["events"]):,} leaks</span>'
                f'<span style="font-weight:700; color:#1e1b4b;">{int(r["total_l"]):,} L</span>'
                f'<span style="color:#ef4444; font-weight:700;">▲</span>'
                f'</div>'
            )
    while len(top_hh_rows) < 3:
        idx = len(top_hh_rows) + 1
        top_hh_rows.append(
            f'<div style="display:flex; justify-content:space-between; align-items:center;">'
            f'<span style="font-weight:600; color:#334155;">Zone Meter {idx}</span>'
            f'<span style="color:#64748b;">0 leaks</span>'
            f'<span style="font-weight:700; color:#1e1b4b;">0 L</span>'
            f'<span style="color:#10b981; font-weight:700;">●</span>'
            f'</div>'
        )

    # Dynamic heights for the 16 Equalizer bars based on 16 sampled/hourly bins
    if total_records:
        hourly_means = df.groupby("hour")["water_usage_liters"].mean()
        max_h = hourly_means.max() if len(hourly_means) and hourly_means.max() > 0 else 1
        bar_heights = [
            max(16, min(62, int((hourly_means.get(int(h * 23 / 15), avg_usage) / max_h) * 60)))
            for h in range(16)
        ]
    else:
        bar_heights = [20] * 16

    # ══════════════════════════════════════════════════════════════
    # UPPER CANVAS: Floating Left (Stats) + Center (Globe) + Right (Engaged & Forecast)
    # ══════════════════════════════════════════════════════════════
    top_col_left, top_col_mid, top_col_right = st.columns([3.6, 4.4, 4.0])

    with top_col_left:
        html_top_left = (
            f'<div style="max-width:315px; padding-top:4px;">'
            f'<div style="font-size:1.75rem; font-weight:800; color:#1e1b4b; letter-spacing:-0.5px; margin-bottom:14px; font-family:\'Inter\',sans-serif;">General statistics</div>'
            f'<div style="display:flex; align-items:center; gap:8px;">'
            f'<span style="font-size:0.85rem; font-weight:700; color:#1e1b4b; font-family:\'Inter\',sans-serif;">Filtered telemetry</span>'
            f'<span style="font-size:0.68rem; color:#64748b; font-weight:700; background:rgba(255,255,255,0.85); border:1px solid #e2e8f0; padding:2px 6px; border-radius:6px; cursor:pointer;">DETAIL &rsaquo;</span>'
            f'</div>'
            f'<div style="font-size:3.2rem; font-weight:900; color:#1e1b4b; letter-spacing:-1.5px; line-height:1.05; margin:6px 0 16px 0; font-family:\'Inter\',sans-serif;">{total_records:,}</div>'
            f'<div style="font-size:0.92rem; font-weight:700; color:#1e1b4b; margin-bottom:8px; font-family:\'Inter\',sans-serif;">Current activity</div>'
            f'<div style="height:8px; border-radius:4px; display:flex; gap:3px; margin-bottom:20px; width:100%;">'
            f'<div style="width:{max(3, low_pct):.1f}%; background:#10b981; border-radius:4px;" title="Low Risk Normal: {low_pct:.1f}%"></div>'
            f'<div style="width:{max(3, mod_pct):.1f}%; background:#8b5cf6; border-radius:4px;" title="Moderate Elevated: {mod_pct:.1f}%"></div>'
            f'<div style="width:{max(3, high_pct):.1f}%; background:#f43f5e; border-radius:4px;" title="High Risk Anomaly: {high_pct:.1f}%"></div>'
            f'<div style="width:{max(3, crit_pct):.1f}%; background:#f59e0b; border-radius:4px;" title="Critical Hazard: {crit_pct:.1f}%"></div>'
            f'</div>'
            f'<div style="display:flex; flex-direction:column; gap:10px; width:100%;">'
            f'<div style="display:flex; justify-content:space-between; align-items:center; font-size:0.85rem; font-family:\'Inter\',sans-serif;">'
            f'<div><span style="display:inline-block; width:8px; height:8px; background:#10b981; border-radius:50%; margin-right:8px;"></span><span style="font-weight:600; color:#334155;">Low Risk (Normal)</span></div>'
            f'<div style="display:flex; gap:14px;"><span style="font-weight:700; color:#1e1b4b;">{low_cnt:,}</span><span style="font-weight:600; color:#64748b;">{low_pct:.1f}%</span></div>'
            f'</div>'
            f'<div style="display:flex; justify-content:space-between; align-items:center; font-size:0.85rem; font-family:\'Inter\',sans-serif;">'
            f'<div><span style="display:inline-block; width:8px; height:8px; background:#8b5cf6; border-radius:50%; margin-right:8px;"></span><span style="font-weight:600; color:#334155;">Moderate (Elevated)</span></div>'
            f'<div style="display:flex; gap:14px;"><span style="font-weight:700; color:#1e1b4b;">{mod_cnt:,}</span><span style="font-weight:600; color:#64748b;">{mod_pct:.1f}%</span></div>'
            f'</div>'
            f'<div style="display:flex; justify-content:space-between; align-items:center; font-size:0.85rem; font-family:\'Inter\',sans-serif;">'
            f'<div><span style="display:inline-block; width:8px; height:8px; background:#f43f5e; border-radius:50%; margin-right:8px;"></span><span style="font-weight:600; color:#334155;">High Risk (Anomaly)</span></div>'
            f'<div style="display:flex; gap:14px;"><span style="font-weight:700; color:#1e1b4b;">{high_cnt:,}</span><span style="font-weight:600; color:#64748b;">{high_pct:.1f}%</span></div>'
            f'</div>'
            f'<div style="display:flex; justify-content:space-between; align-items:center; font-size:0.85rem; font-family:\'Inter\',sans-serif;">'
            f'<div><span style="display:inline-block; width:8px; height:8px; background:#f59e0b; border-radius:50%; margin-right:8px;"></span><span style="font-weight:600; color:#334155;">Critical (Hazard)</span></div>'
            f'<div style="display:flex; gap:14px;"><span style="font-weight:700; color:#1e1b4b;">{crit_cnt:,}</span><span style="font-weight:600; color:#64748b;">{crit_pct:.1f}%</span></div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(html_top_left, unsafe_allow_html=True)

    with top_col_mid:
        st.markdown('<div style="min-height:280px;"></div>', unsafe_allow_html=True)

    with top_col_right:
        html_top_right = (
            f'<div style="padding-top:4px;">'
            f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">'
            f'<div style="font-size:0.95rem; font-weight:800; color:#1e1b4b; font-family:\'Inter\',sans-serif;">Most engaged</div>'
            f'<div style="color:#94a3b8; font-size:0.85rem; letter-spacing:1px; cursor:pointer;">&bull;&bull;&bull; &#10549;</div>'
            f'</div>'
            f'<div class="ref-pill-card" style="margin-bottom:10px;">'
            f'<div class="ref-icon-box ref-icon-purple" style="font-size:1.15rem;">👥</div>'
            f'<div style="flex-grow:1;">'
            f'<div style="font-size:0.75rem; color:#64748b; font-weight:600;">Monitored Smart Meters</div>'
            f'<div style="font-size:1.3rem; font-weight:800; color:#1e1b4b; line-height:1.1;">{total_households:,} <span style="font-size:0.72rem; color:#10b981; font-weight:700; margin-left:4px;">▲ {coverage_pct}%</span></div>'
            f'</div>'
            f'</div>'
            f'<div class="ref-pill-card" style="margin-bottom:18px;">'
            f'<div class="ref-icon-box ref-icon-cyan" style="font-size:1.15rem;">💧</div>'
            f'<div style="flex-grow:1;">'
            f'<div style="font-size:0.75rem; color:#64748b; font-weight:600;">Active Leak Anomalies</div>'
            f'<div style="font-size:1.3rem; font-weight:800; color:#1e1b4b; line-height:1.1;">{total_leaks:,} <span style="font-size:0.72rem; color:#ef4444; font-weight:700; margin-left:4px;">{leak_pct:.1f}% rate</span></div>'
            f'</div>'
            f'</div>'
            f'<div style="font-size:0.92rem; font-weight:800; color:#1e1b4b; margin-bottom:10px; font-family:\'Inter\',sans-serif;">Forecast</div>'
            f'<div style="margin-bottom:12px;">'
            f'<div style="font-size:0.75rem; color:#64748b; font-weight:600;">Estimated Water Loss</div>'
            f'<div style="font-size:1.45rem; font-weight:800; color:#1e1b4b;">${est_loss_cost:,.0f} <span style="font-size:0.75rem; color:#ef4444; font-weight:700; margin-left:4px;">▲ {leak_pct:.1f}%</span></div>'
            f'<div style="font-size:0.68rem; color:#94a3b8; font-weight:500;">Based on {leak_liters:,.0f} L excess leak flow</div>'
            f'</div>'
            f'<div>'
            f'<div style="font-size:0.75rem; color:#64748b; font-weight:600;">Peak Flow Observed</div>'
            f'<div style="font-size:1.45rem; font-weight:800; color:#1e1b4b;">{peak_flow:.1f} L <span style="font-size:0.75rem; color:#10b981; font-weight:700; margin-left:4px;">▲ {avg_spike:.2f}×</span></div>'
            f'<div style="font-size:0.68rem; color:#94a3b8; font-weight:500;">Max rate across active households</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(html_top_right, unsafe_allow_html=True)

    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # LOWER ROW: FLOATING CARDS (Bottom Left, Bottom Center, Bottom Right)
    # ══════════════════════════════════════════════════════════════
    b_left, b_mid, b_right = st.columns([3.8, 4.2, 4.0])

    with b_left:
        # Equalizer Bar Chart Card
        bars_html = "".join([
            f'<div style="width:4.5px; height:{bar_heights[i]}px; background:{"#818cf8" if i % 2 == 0 else "#f43f5e"}; border-radius:4px;"></div>'
            for i in range(16)
        ])
        rows_html = "".join(top_hh_rows)

        html_b_left = (
            f'<div class="glass-card" style="padding:20px 22px; min-height:290px;">'
            f'<div style="font-size:0.75rem; color:#64748b; font-weight:600;">Average Flow Volume</div>'
            f'<div style="font-size:1.55rem; font-weight:800; color:#1e1b4b; line-height:1.1; margin-top:2px;">{avg_usage:.1f} L <span style="font-size:0.75rem; color:#10b981; font-weight:700; margin-left:4px;">▲ {avg_spike:.2f}×</span></div>'
            f'<div style="font-size:0.68rem; color:#94a3b8; margin-bottom:14px;">Telemetry average liters per cycle</div>'
            f'<div style="display:flex; align-items:flex-end; justify-content:space-between; height:65px; padding:4px 0; margin-bottom:18px;">'
            f'{bars_html}'
            f'</div>'
            f'<div style="font-size:0.75rem; color:#475569; display:flex; flex-direction:column; gap:6px; border-top:1px dashed #e2e8f0; padding-top:10px;">'
            f'{rows_html}'
            f'</div>'
            f'</div>'
        )
        st.markdown(html_b_left, unsafe_allow_html=True)

    with b_mid:
        # Stacked Center Cards: Trend Card + Coverage Card
        html_trend_top = (
            f'<div class="glass-card" style="padding:14px 18px; margin-bottom:12px;">'
            f'<div style="display:flex; justify-content:space-between; align-items:baseline;">'
            f'<div style="font-size:0.75rem; color:#64748b; font-weight:600;">Leak Trend</div>'
            f'<div style="font-size:1.1rem; font-weight:800; color:#1e1b4b;">{total_leaks:,}</div>'
            f'</div>'
            f'<div style="font-size:0.65rem; color:#94a3b8; margin-bottom:2px;">Daily incident telemetry vs 7-day trend</div>'
        )
        st.markdown(html_trend_top, unsafe_allow_html=True)

        # Plotly Spline Chart dynamically populated from filtered df
        daily_leaks = df[df["leak_flag_detected"] == 1].groupby("date").size().reset_index(name="leaks")
        fig_spline = go.Figure()
        if len(daily_leaks) > 0:
            daily_leaks["rolling"] = daily_leaks["leaks"].rolling(7, min_periods=1).mean()
            fig_spline.add_trace(go.Scatter(
                x=daily_leaks["date"], y=daily_leaks["rolling"], mode="lines",
                line=dict(color="#6366f1", width=2.6, shape="spline"),
                showlegend=False
            ))
            fig_spline.add_trace(go.Scatter(
                x=daily_leaks["date"], y=daily_leaks["leaks"], mode="lines",
                line=dict(color="#f59e0b", width=2.4, shape="spline"),
                showlegend=False
            ))
        else:
            fig_spline.add_trace(go.Scatter(
                x=[0, 1, 2], y=[0, 0, 0], mode="lines",
                line=dict(color="#6366f1", width=2), showlegend=False
            ))

        fig_spline.update_layout(
            height=65,
            margin=dict(l=0, r=0, t=2, b=2),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )
        st.plotly_chart(fig_spline, use_container_width=True, config={"displayModeBar": False})

        html_trend_bot = "</div>"
        st.markdown(html_trend_bot, unsafe_allow_html=True)

        # Total Coverage Card with circular ring
        html_coverage = (
            f'<div class="glass-card" style="padding:14px 18px; display:flex; align-items:center; gap:16px;">'
            f'<div style="position:relative; width:54px; height:54px; flex-shrink:0;">'
            f'<svg width="54" height="54" viewBox="0 0 36 36">'
            f'<path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e0e7ff" stroke-width="3"/>'
            f'<path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#6366f1" stroke-width="3" stroke-dasharray="{coverage_pct}, 100"/>'
            f'<text x="18" y="21" font-size="8.5" font-weight="800" fill="#1e1b4b" text-anchor="middle" font-family="\'Inter\', sans-serif">{coverage_pct}%</text>'
            f'</svg>'
            f'</div>'
            f'<div>'
            f'<div style="font-size:0.75rem; color:#64748b; font-weight:600;">Total network volume</div>'
            f'<div style="font-size:1.2rem; font-weight:800; color:#1e1b4b; line-height:1.1;">{total_liters:,} L</div>'
            f'<div style="font-size:0.65rem; color:#94a3b8;">Across {total_households:,} monitored smart meters</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(html_coverage, unsafe_allow_html=True)

    with b_right:
        # Time Statistic Card
        html_b_right = (
            f'<div class="glass-card" style="padding:20px 22px; min-height:290px;">'
            f'<div style="font-size:0.75rem; color:#64748b; font-weight:600;">Time Statistic</div>'
            f'<div style="font-size:1.55rem; font-weight:800; color:#1e1b4b; line-height:1.1; margin-top:2px;">{total_leaks:,} <span style="font-size:0.75rem; color:#ef4444; font-weight:700; margin-left:4px;">▲ {night_pct:.1f}%</span></div>'
            f'<div style="font-size:0.68rem; color:#94a3b8; margin-bottom:18px;">Breakdown by operational window</div>'
            f'<div style="margin-bottom:14px;">'
            f'<div style="display:flex; justify-content:space-between; font-size:0.72rem; font-weight:600; margin-bottom:4px;">'
            f'<span style="color:#64748b;">Night (0–5 AM) — Hazard</span>'
            f'<span style="color:#1e1b4b; font-weight:700;">{night_leaks:,} ({night_pct:.1f}%)</span>'
            f'</div>'
            f'<div style="height:5px; background:#e0e7ff; border-radius:3px; overflow:hidden;">'
            f'<div style="width:{night_pct:.1f}%; background:#6366f1; height:100%; border-radius:3px;"></div>'
            f'</div>'
            f'</div>'
            f'<div style="margin-bottom:14px;">'
            f'<div style="display:flex; justify-content:space-between; font-size:0.72rem; font-weight:600; margin-bottom:4px;">'
            f'<span style="color:#64748b;">Morning (6 AM–12 PM)</span>'
            f'<span style="color:#1e1b4b; font-weight:700;">{morning_leaks:,} ({morning_pct:.1f}%)</span>'
            f'</div>'
            f'<div style="height:5px; background:#fee2e2; border-radius:3px; overflow:hidden;">'
            f'<div style="width:{morning_pct:.1f}%; background:#f43f5e; height:100%; border-radius:3px;"></div>'
            f'</div>'
            f'</div>'
            f'<div>'
            f'<div style="display:flex; justify-content:space-between; font-size:0.72rem; font-weight:600; margin-bottom:4px;">'
            f'<span style="color:#64748b;">Evening (12 PM–11 PM)</span>'
            f'<span style="color:#1e1b4b; font-weight:700;">{evening_leaks:,} ({evening_pct:.1f}%)</span>'
            f'</div>'
            f'<div style="height:5px; background:#fef3c7; border-radius:3px; overflow:hidden;">'
            f'<div style="width:{evening_pct:.1f}%; background:#f59e0b; height:100%; border-radius:3px;"></div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(html_b_right, unsafe_allow_html=True)




# ──────────────────────────────────────────────
# PAGE 2 — LEAKAGE SEVERITY ANALYSIS
# ──────────────────────────────────────────────
def page_severity(df: pd.DataFrame):
    st.markdown('<div class="section-header">🔴 Leakage Severity Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Breakdown of leak events by severity level and temporal trends</div>', unsafe_allow_html=True)

    sev_counts = df["leak_severity"].value_counts().sort_values(ascending=False)
    sev_order  = ["Normal", "Low Risk", "Moderate Risk", "High Risk", "Critical Leak"]
    sev_counts = sev_counts.reindex([s for s in sev_order if s in sev_counts.index]).dropna()

    c1, c2 = st.columns(2)

    with c1:
        fig = px.bar(
            x=sev_counts.index, y=sev_counts.values,
            color=sev_counts.index,
            color_discrete_map=COLOR_MAP_SEV,
            text=sev_counts.values,
            labels={"x": "Severity", "y": "Count"},
        )
        fig.update_traces(textposition="outside", textfont_color="#c8d8f0")
        apply_theme(fig, "Leak Severity Distribution (Bar)", 380)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.pie(
            names=sev_counts.index, values=sev_counts.values,
            color=sev_counts.index,
            color_discrete_map=COLOR_MAP_SEV,
            hole=0.45,
        )
        fig2.update_traces(textinfo="percent+label", textfont_color="#fff")
        apply_theme(fig2, "Severity Share (Donut)", 380)
        st.plotly_chart(fig2, use_container_width=True)

    # Trend over time by severity
    sev_time = (
        df[df["leak_severity"] != "Normal"]
        .groupby(["month", "leak_severity"])
        .size()
        .reset_index(name="count")
    )
    fig3 = px.line(
        sev_time, x="month", y="count",
        color="leak_severity",
        color_discrete_map=COLOR_MAP_SEV,
        markers=True,
        labels={"month": "Month", "count": "Events", "leak_severity": "Severity"},
    )
    apply_theme(fig3, "Leak Events Over Time by Severity", 360)
    st.plotly_chart(fig3, use_container_width=True)

    # Severity vs avg water usage
    sev_usage = df.groupby("leak_severity")["water_usage_liters"].mean().reindex(sev_order).dropna()
    fig4 = px.bar(
        x=sev_usage.index, y=sev_usage.values,
        color=sev_usage.index,
        color_discrete_map=COLOR_MAP_SEV,
        labels={"x": "Severity", "y": "Avg Usage (L)"},
        text=[f"{v:.1f} L" for v in sev_usage.values],
    )
    fig4.update_traces(textposition="outside", textfont_color="#c8d8f0")
    apply_theme(fig4, "Average Water Usage by Severity Level", 360)
    st.plotly_chart(fig4, use_container_width=True)


# ──────────────────────────────────────────────
# PAGE 3 — HOUSEHOLD RISK INTELLIGENCE
# ──────────────────────────────────────────────
def page_risk(df: pd.DataFrame):
    st.markdown('<div class="section-header">🏠 Household Risk Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Risk profiling and ranking of smart meter households</div>', unsafe_allow_html=True)

    # Risk distribution
    risk_order = ["Low Risk", "Moderate Risk", "High Risk", "Critical"]
    risk_counts = df["risk_level"].value_counts().reindex(risk_order).dropna()

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            x=risk_counts.index, y=risk_counts.values,
            color=risk_counts.index,
            color_discrete_map=COLOR_MAP_RISK,
            text=risk_counts.values,
            labels={"x": "Risk Level", "y": "Households"},
        )
        fig.update_traces(textposition="outside", textfont_color="#c8d8f0")
        apply_theme(fig, "Household Count by Risk Level", 360)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = px.pie(
            names=risk_counts.index, values=risk_counts.values,
            color=risk_counts.index,
            color_discrete_map=COLOR_MAP_RISK,
            hole=0.4,
        )
        fig2.update_traces(textinfo="percent+label", textfont_color="#fff")
        apply_theme(fig2, "Risk Level Proportions", 360)
        st.plotly_chart(fig2, use_container_width=True)

    # Top high-risk households
    st.markdown('<div class="section-header" style="font-size:1.1rem">🚨 Top High-Risk Households</div>', unsafe_allow_html=True)
    top_risk = (
        df[df["risk_level"].isin(["High Risk", "Critical"])]
        .groupby("household_id")
        .agg(
            risk_level=("risk_level", "first"),
            avg_leak_prob=("leak_probability", "mean"),
            avg_spike=("spike_ratio", "mean"),
            leak_events=("leak_flag_detected", "sum"),
            avg_usage=("water_usage_liters", "mean"),
        )
        .sort_values("avg_leak_prob", ascending=False)
        .reset_index()
        .head(20)
    )
    top_risk["avg_leak_prob"] = top_risk["avg_leak_prob"].map("{:.4f}".format)
    top_risk["avg_spike"]     = top_risk["avg_spike"].map("{:.2f}".format)
    top_risk["avg_usage"]     = top_risk["avg_usage"].map("{:.1f} L".format)

    st.dataframe(
        top_risk.rename(columns={
            "household_id": "Household",
            "risk_level": "Risk",
            "avg_leak_prob": "Leak Probability",
            "avg_spike": "Avg Spike Ratio",
            "leak_events": "Leak Events",
            "avg_usage": "Avg Usage",
        }),
        use_container_width=True,
        height=420,
    )

    # Interactive search
    st.markdown('<div class="section-header" style="font-size:1.1rem">🔎 Household Search</div>', unsafe_allow_html=True)
    search = st.text_input("Search household ID (partial match)", "")
    filtered = df[df["household_id"].str.contains(search, case=False)] if search else df
    summary = (
        filtered.groupby("household_id")
        .agg(
            risk_level=("risk_level", "first"),
            leak_severity=("leak_severity", lambda x: x.mode()[0]),
            avg_leak_prob=("leak_probability", "mean"),
            avg_spike=("spike_ratio", "mean"),
            leak_events=("leak_flag_detected", "sum"),
        )
        .sort_values("avg_leak_prob", ascending=False)
        .reset_index()
    )
    summary["avg_leak_prob"] = summary["avg_leak_prob"].map("{:.4f}".format)
    summary["avg_spike"]     = summary["avg_spike"].map("{:.2f}".format)
    st.dataframe(summary.head(100), use_container_width=True, height=380)


# ──────────────────────────────────────────────
# PAGE 4 — WATER CONSUMPTION BEHAVIOR
# ──────────────────────────────────────────────
def page_consumption(df: pd.DataFrame):
    st.markdown('<div class="section-header">💧 Water Consumption Behavior</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Temporal and distributional analysis of household water usage</div>', unsafe_allow_html=True)

    # Hourly average
    hourly = df.groupby("hour")["water_usage_liters"].mean().reset_index()
    fig = px.line(
        hourly, x="hour", y="water_usage_liters",
        markers=True,
        color_discrete_sequence=["#4fc3f7"],
        labels={"hour": "Hour of Day", "water_usage_liters": "Avg Usage (L)"},
    )
    fig.add_vline(x=hourly.loc[hourly["water_usage_liters"].idxmax(), "hour"],
                  line_dash="dash", line_color="#ffa726",
                  annotation_text="Peak hour", annotation_font_color="#ffa726")
    apply_theme(fig, "Hourly Average Water Consumption", 360)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig2 = px.histogram(
            df, x="water_usage_liters", nbins=60,
            color_discrete_sequence=["#4fc3f7"],
            labels={"water_usage_liters": "Usage (L)", "count": "Frequency"},
        )
        apply_theme(fig2, "Water Usage Distribution", 360)
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dow_usage = df.groupby("day_of_week")["water_usage_liters"].mean().reindex(dow_order).dropna()
        fig3 = px.bar(
            x=dow_usage.index, y=dow_usage.values,
            color=dow_usage.values,
            color_continuous_scale="Blues",
            labels={"x": "Day", "y": "Avg Usage (L)", "color": "Usage"},
        )
        apply_theme(fig3, "Average Consumption by Day of Week", 360)
        st.plotly_chart(fig3, use_container_width=True)

    # Box plot per risk level
    fig4 = px.box(
        df, x="risk_level", y="water_usage_liters",
        color="risk_level",
        color_discrete_map=COLOR_MAP_RISK,
        category_orders={"risk_level": ["Low Risk","Moderate Risk","High Risk","Critical"]},
        labels={"risk_level": "Risk Level", "water_usage_liters": "Usage (L)"},
    )
    apply_theme(fig4, "Water Usage Distribution by Risk Level", 400)
    st.plotly_chart(fig4, use_container_width=True)

    # Heatmap: hour × day
    heat_data = df.groupby(["day_of_week","hour"])["water_usage_liters"].mean().reset_index()
    heat_pivot = heat_data.pivot(index="day_of_week", columns="hour", values="water_usage_liters")
    heat_pivot = heat_pivot.reindex([d for d in dow_order if d in heat_pivot.index])
    fig5 = px.imshow(
        heat_pivot,
        color_continuous_scale="Blues",
        labels={"x": "Hour", "y": "Day", "color": "Avg L"},
        aspect="auto",
    )
    apply_theme(fig5, "Consumption Heatmap: Hour × Day", 380)
    st.plotly_chart(fig5, use_container_width=True)


# ──────────────────────────────────────────────
# PAGE 5 — ABNORMAL PATTERN DETECTION
# ──────────────────────────────────────────────
def page_anomalies(df: pd.DataFrame):
    st.markdown('<div class="section-header">⚠️ Abnormal Pattern Detection</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Spike ratio–based anomaly identification across the network</div>', unsafe_allow_html=True)

    # Summary badges
    n2 = (df["spike_ratio"] > 2).sum()
    n3 = (df["spike_ratio"] > 3).sum()
    pct2 = n2 / len(df) * 100 if len(df) else 0
    pct3 = n3 / len(df) * 100 if len(df) else 0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="metric-card warning">
            <div class="label">Spike Ratio &gt; 2</div>
            <div class="value">{n2:,}</div>
            <div class="delta">{pct2:.1f}% of records</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card danger">
            <div class="label">Spike Ratio &gt; 3</div>
            <div class="value">{n3:,}</div>
            <div class="delta">{pct3:.1f}% of records</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        max_spike = df["spike_ratio"].max()
        worst_hh  = df.loc[df["spike_ratio"].idxmax(), "household_id"]
        st.markdown(f"""<div class="metric-card danger">
            <div class="label">Max Spike Ratio</div>
            <div class="value">{max_spike:.2f}</div>
            <div class="delta">{worst_hh}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Scatter: spike_ratio vs water_usage, coloured by anomaly level
    df_plot = df.copy()
    df_plot["anomaly"] = "Normal"
    df_plot.loc[df_plot["spike_ratio"] > 2, "anomaly"] = "Spike > 2"
    df_plot.loc[df_plot["spike_ratio"] > 3, "anomaly"] = "Spike > 3"
    anom_colors = {"Normal": "#4fc3f7", "Spike > 2": "#ffa726", "Spike > 3": "#ef5350"}

    fig = px.scatter(
        df_plot.sample(min(3000, len(df_plot))),
        x="water_usage_liters", y="spike_ratio",
        color="anomaly", color_discrete_map=anom_colors,
        opacity=0.7, size_max=6,
        labels={"water_usage_liters": "Usage (L)", "spike_ratio": "Spike Ratio"},
        hover_data=["household_id", "risk_level"],
    )
    fig.add_hline(y=2, line_dash="dash", line_color="#ffa726",
                  annotation_text="Threshold 2", annotation_font_color="#ffa726")
    fig.add_hline(y=3, line_dash="dash", line_color="#ef5350",
                  annotation_text="Threshold 3", annotation_font_color="#ef5350")
    apply_theme(fig, "Spike Ratio vs Water Usage (Anomaly Scatter)", 440)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        # Spike > 2 over time
        spike2_time = df[df["spike_ratio"] > 2].groupby("date").size().reset_index(name="count")
        fig2 = px.bar(spike2_time, x="date", y="count",
                      color_discrete_sequence=["#ffa726"],
                      labels={"date": "Date", "count": "Anomaly Count"})
        apply_theme(fig2, "Daily Anomalies (Spike > 2)", 340)
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        spike3_time = df[df["spike_ratio"] > 3].groupby("date").size().reset_index(name="count")
        fig3 = px.bar(spike3_time, x="date", y="count",
                      color_discrete_sequence=["#ef5350"],
                      labels={"date": "Date", "count": "Critical Anomaly Count"})
        apply_theme(fig3, "Daily Critical Anomalies (Spike > 3)", 340)
        st.plotly_chart(fig3, use_container_width=True)

    # Anomaly table
    st.markdown('<div class="section-header" style="font-size:1.1rem">📋 Anomalous Records (Spike > 2)</div>', unsafe_allow_html=True)
    anomaly_df = df[df["spike_ratio"] > 2][
        ["household_id","timestamp","water_usage_liters","spike_ratio","leak_severity","risk_level","leak_probability"]
    ].sort_values("spike_ratio", ascending=False).head(200)
    st.dataframe(anomaly_df, use_container_width=True, height=400)


# ──────────────────────────────────────────────
# PAGE 6 — HOUSEHOLD EXPLORER
# ──────────────────────────────────────────────
def page_explorer(df: pd.DataFrame):
    st.markdown('<div class="section-header">🔬 Household Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Deep-dive into individual household water behavior and risk profile</div>', unsafe_allow_html=True)

    households = sorted(df["household_id"].unique())
    selected_hh = st.selectbox("Select Household ID", households)

    hh_df = df[df["household_id"] == selected_hh].sort_values("timestamp")

    if hh_df.empty:
        st.warning("No data found for this household with the current filters.")
        return

    # KPI row
    risk    = hh_df["risk_level"].iloc[-1]
    prob    = hh_df["leak_probability"].mean()
    leaks   = hh_df["leak_flag_detected"].sum()
    avg_u   = hh_df["water_usage_liters"].mean()
    max_sp  = hh_df["spike_ratio"].max()
    risk_color = {"Low Risk":"success","Moderate Risk":"","High Risk":"warning","Critical":"danger"}.get(risk,"")

    cols = st.columns(5)
    for col, (lbl, val, cls) in zip(cols, [
        ("Risk Level",       risk,            risk_color),
        ("Leak Probability", f"{prob:.4f}",   "danger" if prob > 0.1 else ""),
        ("Leak Events",      str(leaks),      "danger" if leaks > 0 else "success"),
        ("Avg Usage",        f"{avg_u:.1f} L", ""),
        ("Max Spike Ratio",  f"{max_sp:.2f}", "danger" if max_sp > 3 else "warning" if max_sp > 2 else ""),
    ]):
        with col:
            st.markdown(f"""<div class="metric-card {cls}">
                <div class="label">{lbl}</div>
                <div class="value">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Water usage over time
    fig = px.line(hh_df, x="timestamp", y="water_usage_liters",
                  color_discrete_sequence=["#4fc3f7"],
                  labels={"timestamp": "Time", "water_usage_liters": "Usage (L)"})
    # Overlay leak events
    leaks_df = hh_df[hh_df["leak_flag_detected"] == 1]
    if not leaks_df.empty:
        fig.add_scatter(x=leaks_df["timestamp"], y=leaks_df["water_usage_liters"],
                        mode="markers", marker=dict(color="#ef5350", size=8, symbol="x"),
                        name="Leak Detected")
    apply_theme(fig, f"Water Usage Over Time — {selected_hh}", 380)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig2 = px.line(hh_df, x="timestamp", y="spike_ratio",
                       color_discrete_sequence=["#ffa726"],
                       labels={"timestamp": "Time", "spike_ratio": "Spike Ratio"})
        fig2.add_hline(y=2, line_dash="dash", line_color="#ffa726",
                       annotation_text="Alert Threshold 2")
        fig2.add_hline(y=3, line_dash="dash", line_color="#ef5350",
                       annotation_text="Critical Threshold 3")
        apply_theme(fig2, "Spike Ratio Trend", 340)
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        sev_dist = hh_df["leak_severity"].value_counts()
        fig3 = px.pie(names=sev_dist.index, values=sev_dist.values,
                      color=sev_dist.index, color_discrete_map=COLOR_MAP_SEV, hole=0.4)
        fig3.update_traces(textinfo="percent+label", textfont_color="#fff")
        apply_theme(fig3, "Severity Distribution", 340)
        st.plotly_chart(fig3, use_container_width=True)

    # Leak events table
    if not leaks_df.empty:
        st.markdown('<div class="section-header" style="font-size:1.1rem">🚨 Detected Leak Events</div>', unsafe_allow_html=True)
        st.dataframe(
            leaks_df[["timestamp","water_usage_liters","spike_ratio","leak_severity","leak_probability","risk_level"]],
            use_container_width=True,
        )
    else:
        st.markdown('<div class="insight-box success">✅ No leak events detected for this household in the filtered window.</div>', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGE 6B — ML RISK PREDICTION (RF + XGBoost)
# ──────────────────────────────────────────────
def _load_model(name: str):
    """Load a model pipeline from the models directory. Returns pipeline or None."""
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", name)
    if not os.path.exists(model_path):
        return None
    try:
        pipeline = joblib.load(model_path)
        return pipeline
    except Exception:
        return None


def page_ml_prediction(df: pd.DataFrame):
    st.markdown('<div class="section-header">🤖 Machine Learning Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-driven predictive analytics using Random Forest &amp; XGBoost — side-by-side</div>', unsafe_allow_html=True)

    # Load both models
    rf_pipeline  = _load_model("household_risk_model.pkl")
    xgb_pipeline = _load_model("household_xgboost_model.pkl")

    if rf_pipeline is None and xgb_pipeline is None:
        st.warning("⚠️ No models found! Please run `train_xgboost_model.py` to train both Random Forest and XGBoost models.")
        return

    rf_model  = rf_pipeline['model']  if rf_pipeline  else None
    xgb_model = xgb_pipeline['model'] if xgb_pipeline else None
    req_features = (rf_pipeline or xgb_pipeline).get('features',
        ['avg_usage', 'max_usage', 'std_usage', 'night_avg_usage',
         'avg_spike_ratio', 'max_spike_ratio', 'std_spike_ratio'])

    households = sorted(df["household_id"].unique())
    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown('<div class="insight-box"><b>1. Select Household</b></div>', unsafe_allow_html=True)
        selected_hh = st.selectbox("Select Household ID ", households)

        hh_data = df[df["household_id"] == selected_hh]
        night_data = hh_data[hh_data['hour'].isin([0, 1, 2, 3, 4, 5])] if 'hour' in hh_data.columns else hh_data
        day_data   = hh_data[~hh_data['hour'].isin([0, 1, 2, 3, 4, 5])] if 'hour' in hh_data.columns else hh_data
        total_readings = len(hh_data) if len(hh_data) > 0 else 1

        real_features = {
            'avg_usage': hh_data['water_usage_liters'].mean(),
            'max_usage': hh_data['water_usage_liters'].max(),
            'std_usage': hh_data['water_usage_liters'].std() if len(hh_data) > 1 else 0.0,
            'night_avg_usage': night_data['water_usage_liters'].mean() if len(night_data) > 0 else 0.0,
            'avg_spike_ratio': hh_data['spike_ratio'].mean(),
            'max_spike_ratio': hh_data['spike_ratio'].max(),
            'std_spike_ratio': hh_data['spike_ratio'].std() if len(hh_data) > 1 else 0.0,
            'night_day_ratio': (night_data['water_usage_liters'].mean() / max(day_data['water_usage_liters'].mean(), 0.01)) if len(night_data) > 0 and len(day_data) > 0 else 0.0,
            'usage_range': hh_data['water_usage_liters'].max() - hh_data['water_usage_liters'].mean(),
            'cv_usage': (hh_data['water_usage_liters'].std() / max(hh_data['water_usage_liters'].mean(), 0.01)) if len(hh_data) > 1 else 0.0,
        }

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="insight-box warning"><b>2. What-If Analysis (Behavioral Simulation)</b></div>', unsafe_allow_html=True)

        with st.expander("🧪 Tweak Household Behaviors", expanded=True):
            val_avg_u = st.slider("Average Usage (L)", 0.0, float(max(100.0, real_features['avg_usage']*2)), float(real_features['avg_usage']))
            val_max_u = st.slider("Max Usage (L)", 0.0, float(max(200.0, real_features['max_usage']*2)), float(real_features['max_usage']))
            val_std_u = st.slider("Usage Volatility (Std Dev)", 0.0, float(max(50.0, real_features['std_usage']*2)), float(real_features['std_usage']))
            val_nigh = st.slider("Night Avg Usage", 0.0, float(max(50.0, real_features['night_avg_usage']*2)), float(real_features['night_avg_usage']))
            val_avg_s = st.slider("Avg Spike Ratio", 0.0, 8.0, float(real_features['avg_spike_ratio']))
            val_max_s = st.slider("Max Spike Ratio", 0.0, 20.0, float(real_features['max_spike_ratio']))
            val_std_s = st.slider("Spike Volatility", 0.0, float(max(5.0, real_features['std_spike_ratio']*2)), float(real_features['std_spike_ratio']))

        # Compute derived features from slider values
        day_avg_est = max(val_avg_u, 0.01)
        val_night_day_ratio = val_nigh / day_avg_est
        val_usage_range = val_max_u - val_avg_u
        val_cv_usage = val_std_u / day_avg_est

    with c2:
        # Build feature vector — only behavioral features (no target leakage)
        input_row = {
            'avg_usage': val_avg_u,
            'max_usage': val_max_u,
            'std_usage': val_std_u,
            'night_avg_usage': val_nigh,
            'avg_spike_ratio': val_avg_s,
            'max_spike_ratio': val_max_s,
            'std_spike_ratio': val_std_s,
            'night_day_ratio': val_night_day_ratio,
            'usage_range': val_usage_range,
            'cv_usage': val_cv_usage,
        }
        # Only use features the model expects
        input_data = pd.DataFrame([{f: input_row.get(f, 0.0) for f in req_features}])

        # ── Side-by-side gauge charts ──
        st.markdown('<div class="insight-box"><b>🎯 Model Predictions — Side by Side</b></div>', unsafe_allow_html=True)
        gauge_cols = st.columns(2)

        models_info = []
        if rf_model is not None:
            rf_prob = rf_model.predict_proba(input_data)[0][1] if len(rf_model.classes_) > 1 else (0.0 if rf_model.classes_[0] == 0 else 1.0)
            rf_pred = rf_model.predict(input_data)[0]
            models_info.append(("🌲 Random Forest", rf_prob, rf_pred, rf_model, "#4fc3f7"))
        if xgb_model is not None:
            xgb_prob = xgb_model.predict_proba(input_data)[0][1] if len(xgb_model.classes_) > 1 else (0.0 if xgb_model.classes_[0] == 0 else 1.0)
            xgb_pred = xgb_model.predict(input_data)[0]
            models_info.append(("⚡ XGBoost", xgb_prob, xgb_pred, xgb_model, "#ab47bc"))

        for idx, (name, prob, pred, model, accent) in enumerate(models_info):
            with gauge_cols[idx] if len(models_info) > 1 else gauge_cols[0]:
                prob_color = "#66bb6a" if prob < 0.3 else "#ffa726" if prob < 0.7 else "#ef5350"
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prob * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': f"{name}", 'font': {'size': 16, 'color': accent}},
                    gauge={
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#c8d8f0"},
                        'bar': {'color': prob_color},
                        'bgcolor': "rgba(0,0,0,0)",
                        'borderwidth': 2,
                        'bordercolor': "#e2e8f0",
                        'steps': [
                            {'range': [0, 30], 'color': 'rgba(102, 187, 106, 0.15)'},
                            {'range': [30, 70], 'color': 'rgba(255, 167, 38, 0.15)'},
                            {'range': [70, 100], 'color': 'rgba(239, 83, 80, 0.15)'}],
                    }
                ))
                fig.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", font_color="#334155",
                                  margin=dict(t=60, b=10, l=30, r=30), height=270)
                st.plotly_chart(fig, use_container_width=True)

                if pred == 1:
                    st.markdown(f'<div class="metric-card danger"><div class="value">🚨 HIGH RISK</div><div class="delta">{name}: Immediate inspection needed</div></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="metric-card success"><div class="value">✅ NORMAL</div><div class="delta">{name}: Operating properly</div></div>', unsafe_allow_html=True)

        # ── Ensemble Verdict ──
        if len(models_info) == 2:
            avg_prob = (models_info[0][1] + models_info[1][1]) / 2
            both_agree = models_info[0][2] == models_info[1][2]
            st.markdown("<br>", unsafe_allow_html=True)
            if both_agree:
                verdict_icon = "🚨" if models_info[0][2] == 1 else "✅"
                verdict_txt = "HIGH RISK" if models_info[0][2] == 1 else "NORMAL"
                st.markdown(f"""<div class="insight-box {'danger' if models_info[0][2] == 1 else 'success'}">
                    <b>🤝 Ensemble Verdict:</b> Both models agree — <b>{verdict_icon} {verdict_txt}</b> (Consensus probability: {avg_prob*100:.1f}%)
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="insight-box warning">
                    <b>⚖️ Ensemble Verdict:</b> Models disagree — RF says <b>{"HIGH RISK" if models_info[0][2] == 1 else "NORMAL"}</b>, 
                    XGBoost says <b>{"HIGH RISK" if models_info[1][2] == 1 else "NORMAL"}</b>. 
                    Average probability: {avg_prob*100:.1f}%. <i>Manual review recommended.</i>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Feature importance comparison ──
        if len(models_info) == 2:
            rf_imp = models_info[0][3].feature_importances_
            xgb_imp = models_info[1][3].feature_importances_
            imp_df = pd.DataFrame({
                'Feature': req_features,
                'Random Forest': rf_imp,
                'XGBoost': xgb_imp,
            })
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(name='🌲 Random Forest', x=imp_df['Feature'], y=imp_df['Random Forest'],
                                  marker_color='#4fc3f7', opacity=0.85))
            fig2.add_trace(go.Bar(name='⚡ XGBoost', x=imp_df['Feature'], y=imp_df['XGBoost'],
                                  marker_color='#ab47bc', opacity=0.85))
            fig2.update_layout(barmode='group',
                               paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", font_color="#334155",
                               title=dict(text="Feature Importance — RF vs XGBoost", font=dict(color="#4fc3f7", size=15)),
                               margin=dict(t=50, b=40, l=20, r=20), height=300,
                               legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor="#e2e8f0", borderwidth=1))
            fig2.update_xaxes(gridcolor="#f1f5f9", tickfont_color="#94a3b8")
            fig2.update_yaxes(gridcolor="#f1f5f9", tickfont_color="#94a3b8", title_text="Importance")
            st.plotly_chart(fig2, use_container_width=True)
        elif len(models_info) == 1:
            imp = models_info[0][3].feature_importances_
            imp_df = pd.DataFrame({'Feature': req_features, 'Importance': imp}).sort_values('Importance')
            fig2 = px.bar(imp_df, x='Importance', y='Feature', orientation='h',
                         color='Importance', color_continuous_scale='Blues_r',
                         labels={'Importance': 'Influence', 'Feature': 'Driver'})
            fig2.update_layout(paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", font_color="#334155",
                               title=dict(text="Key Risk Drivers (Feature Importance)", font=dict(color="#4fc3f7")),
                               margin=dict(t=50, b=0, l=20, r=20), height=250)
            fig2.update_xaxes(showgrid=False)
            st.plotly_chart(fig2, use_container_width=True)


# ──────────────────────────────────────────────
# PAGE — MODEL COMPARISON (RF vs XGBoost)
# ──────────────────────────────────────────────
def page_model_comparison(df: pd.DataFrame):
    st.markdown('<div class="section-header">📊 Model Comparison — Random Forest vs XGBoost</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Comprehensive evaluation and comparison of both machine learning models used in the system</div>', unsafe_allow_html=True)

    # Load comparison metrics
    metrics_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "model_comparison_metrics.pkl")

    if not os.path.exists(metrics_path):
        st.warning("⚠️ Model comparison metrics not found. Please run `train_xgboost_model.py` first to train both models and generate comparison data.")
        st.code("python train_xgboost_model.py", language="bash")
        return

    try:
        metrics = joblib.load(metrics_path)
    except Exception as e:
        st.error(f"Error loading comparison metrics: {e}")
        return

    rf_m  = metrics['random_forest']
    xgb_m = metrics['xgboost']
    features = metrics.get('features', [])

    # ════════════════════════════════════════════
    # Section 1: Algorithm Overview
    # ════════════════════════════════════════════
    st.markdown('<div class="section-header" style="font-size:1.15rem">🧬 Algorithm Overview</div>', unsafe_allow_html=True)

    algo_c1, algo_c2 = st.columns(2)
    with algo_c1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #0d2137 0%, #0f2a47 100%);
                    border: 1px solid #e2e8f0; border-radius: 14px; padding: 22px;
                    border-top: 3px solid #4fc3f7;">
            <h3 style="color:#4fc3f7; margin-top:0; font-size:1.15rem;">🌲 Random Forest</h3>
            <p style="color:#90a4c4; font-size:0.88rem; line-height:1.6;">
                An <b>ensemble</b> of multiple decision trees, each trained on a random subset of the data.
                Final prediction is made by <b>majority vote</b> (classification) across all trees.
            </p>
            <hr style="border-color:#e2e8f0;">
            <p style="color:#c8ddf2; font-size:0.83rem; margin-bottom:4px;"><b>✅ Strengths:</b></p>
            <ul style="color:#90a4c4; font-size:0.82rem; margin-top:0;">
                <li>Resistant to overfitting due to bagging</li>
                <li>Handles noisy data and outliers well</li>
                <li>Provides reliable feature importance</li>
                <li>Minimal hyperparameter tuning needed</li>
            </ul>
            <p style="color:#c8ddf2; font-size:0.83rem; margin-bottom:4px;"><b>⚠️ Limitations:</b></p>
            <ul style="color:#90a4c4; font-size:0.82rem; margin-top:0;">
                <li>Can be slower for very large datasets</li>
                <li>Less effective on highly imbalanced data</li>
                <li>Models can be large in size</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    with algo_c2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1a0d2e 0%, #231447 100%);
                    border: 1px solid #3a1e5f; border-radius: 14px; padding: 22px;
                    border-top: 3px solid #ab47bc;">
            <h3 style="color:#ab47bc; margin-top:0; font-size:1.15rem;">⚡ XGBoost</h3>
            <p style="color:#90a4c4; font-size:0.88rem; line-height:1.6;">
                <b>Extreme Gradient Boosting</b> — builds trees <i>sequentially</i>, where each new tree
                corrects the errors of the previous ones using <b>gradient descent optimization</b>.
            </p>
            <hr style="border-color:#3a1e5f;">
            <p style="color:#c8ddf2; font-size:0.83rem; margin-bottom:4px;"><b>✅ Strengths:</b></p>
            <ul style="color:#90a4c4; font-size:0.82rem; margin-top:0;">
                <li>Often achieves higher accuracy via boosting</li>
                <li>Built-in L1/L2 regularization prevents overfitting</li>
                <li>Handles imbalanced classes with scale_pos_weight</li>
                <li>Extremely fast with hardware optimizations</li>
            </ul>
            <p style="color:#c8ddf2; font-size:0.83rem; margin-bottom:4px;"><b>⚠️ Limitations:</b></p>
            <ul style="color:#90a4c4; font-size:0.82rem; margin-top:0;">
                <li>More sensitive to hyperparameter tuning</li>
                <li>Can overfit on small/noisy datasets</li>
                <li>Sequential nature makes training slower</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ════════════════════════════════════════════
    # Section 2: Head-to-Head Metrics
    # ════════════════════════════════════════════
    st.markdown('<div class="section-header" style="font-size:1.15rem">🏆 Performance Head-to-Head</div>', unsafe_allow_html=True)

    metric_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score', 'AUC-ROC']
    rf_vals  = [rf_m['accuracy'], rf_m['precision'], rf_m['recall'], rf_m['f1'], rf_m['auc_roc']]
    xgb_vals = [xgb_m['accuracy'], xgb_m['precision'], xgb_m['recall'], xgb_m['f1'], xgb_m['auc_roc']]

    metric_cols = st.columns(5)
    for i, (name, rv, xv) in enumerate(zip(metric_names, rf_vals, xgb_vals)):
        with metric_cols[i]:
            winner = "rf" if rv > xv else "xgb" if xv > rv else "tie"
            rf_color = "#4fc3f7" if winner == "rf" else "#90a4c4"
            xgb_color = "#ab47bc" if winner == "xgb" else "#90a4c4"
            crown = "👑" if winner != "tie" else "🤝"
            st.markdown(f"""
            <div class="metric-card" style="padding:16px 12px;">
                <div class="label" style="font-size:0.72rem;">{name} {crown}</div>
                <div style="display:flex; justify-content:center; gap:18px; margin-top:8px;">
                    <div>
                        <div style="font-size:0.65rem; color:#4fc3f7; text-transform:uppercase; letter-spacing:1px;">RF</div>
                        <div style="font-size:1.5rem; font-weight:800; color:{rf_color};">{rv:.3f}</div>
                    </div>
                    <div style="border-left:1px solid #e2e8f0;"></div>
                    <div>
                        <div style="font-size:0.65rem; color:#ab47bc; text-transform:uppercase; letter-spacing:1px;">XGB</div>
                        <div style="font-size:1.5rem; font-weight:800; color:{xgb_color};">{xv:.3f}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Winner summary
    rf_wins = sum(1 for rv, xv in zip(rf_vals, xgb_vals) if rv > xv)
    xgb_wins = sum(1 for rv, xv in zip(rf_vals, xgb_vals) if xv > rv)
    ties = 5 - rf_wins - xgb_wins

    if rf_wins > xgb_wins:
        st.markdown(f"""<div class="insight-box"><b>🌲 Random Forest wins {rf_wins}/5 metrics</b> | XGBoost wins {xgb_wins}/5 | Ties: {ties}
        <br><span style="color:#90a4c4; font-size:0.85rem;">Random Forest shows stronger overall performance on this dataset. 
        Its bagging approach and resistance to noise give it an edge for household risk classification.</span></div>""", unsafe_allow_html=True)
    elif xgb_wins > rf_wins:
        st.markdown(f"""<div class="insight-box"><b>⚡ XGBoost wins {xgb_wins}/5 metrics</b> | Random Forest wins {rf_wins}/5 | Ties: {ties}
        <br><span style="color:#90a4c4; font-size:0.85rem;">XGBoost's gradient boosting approach and regularization provide superior performance on this dataset, 
        particularly strong in precision and recall trade-offs.</span></div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="insight-box success"><b>🤝 It's a tie!</b> Both models perform equally across the evaluation metrics.
        <br><span style="color:#90a4c4; font-size:0.85rem;">Using both models simultaneously (ensemble) provides the most reliable predictions.</span></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ════════════════════════════════════════════
    # Section 3: ROC Curves + Confusion Matrices
    # ════════════════════════════════════════════
    roc_col, cm_col = st.columns(2)

    with roc_col:
        st.markdown('<div class="section-header" style="font-size:1.05rem">📈 ROC Curve Comparison</div>', unsafe_allow_html=True)
        fig_roc = go.Figure()
        fig_roc.add_trace(go.Scatter(x=rf_m['fpr'], y=rf_m['tpr'], mode='lines',
                                     name=f"RF (AUC={rf_m['auc_roc']:.3f})",
                                     line=dict(color='#4fc3f7', width=2.5)))
        fig_roc.add_trace(go.Scatter(x=xgb_m['fpr'], y=xgb_m['tpr'], mode='lines',
                                     name=f"XGB (AUC={xgb_m['auc_roc']:.3f})",
                                     line=dict(color='#ab47bc', width=2.5)))
        fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines',
                                     name="Random Baseline",
                                     line=dict(color='#3a5a80', width=1, dash='dash')))
        fig_roc.update_layout(
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate",
            height=380, margin=dict(l=40, r=20, t=40, b=40),
            legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor="#e2e8f0", borderwidth=1,
                       font=dict(color="#c8d8f0"), x=0.55, y=0.05),
            **CHART_THEME,
        )
        fig_roc.update_xaxes(gridcolor="#f1f5f9", tickfont_color="#94a3b8")
        fig_roc.update_yaxes(gridcolor="#f1f5f9", tickfont_color="#94a3b8")
        st.plotly_chart(fig_roc, use_container_width=True)

        st.markdown("""<div class="insight-box" style="font-size:0.82rem;">
            <b>📖 How to read the ROC curve:</b> The closer the curve follows the top-left corner, the better.
            AUC = 1.0 is perfect; AUC = 0.5 is random guessing (dashed line). A higher AUC means the model 
            is better at distinguishing high-risk from normal households.
        </div>""", unsafe_allow_html=True)

    with cm_col:
        st.markdown('<div class="section-header" style="font-size:1.05rem">🔢 Confusion Matrices</div>', unsafe_allow_html=True)

        cm_tabs = st.tabs(["🌲 Random Forest", "⚡ XGBoost"])
        for tab, (label, cm, accent) in zip(cm_tabs, [
            ("Random Forest", rf_m['confusion_matrix'], 'Blues'),
            ("XGBoost", xgb_m['confusion_matrix'], 'Purples'),
        ]):
            with tab:
                cm_arr = np.array(cm)
                fig_cm = px.imshow(
                    cm_arr,
                    labels=dict(x="Predicted", y="Actual", color="Count"),
                    x=["Normal", "High Risk"], y=["Normal", "High Risk"],
                    color_continuous_scale=accent,
                    text_auto=True,
                    aspect="equal",
                )
                fig_cm.update_layout(
                    height=310, margin=dict(l=20, r=20, t=30, b=20),
                    title=dict(text=f"{label} Confusion Matrix", font=dict(color="#4fc3f7", size=13)),
                    **CHART_THEME,
                )
                fig_cm.update_traces(textfont_size=18, textfont_color="#fff")
                st.plotly_chart(fig_cm, use_container_width=True)

        st.markdown("""<div class="insight-box" style="font-size:0.82rem;">
            <b>📖 Reading the matrix:</b> Top-left = correct normals (TN), bottom-right = correct high-risk (TP).
            Top-right = false alarms (FP), bottom-left = missed risks (FN). Fewer FN is critical for safety.
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ════════════════════════════════════════════
    # Section 4: Feature Importance Comparison
    # ════════════════════════════════════════════
    st.markdown('<div class="section-header" style="font-size:1.15rem">🔬 Feature Importance Analysis</div>', unsafe_allow_html=True)

    rf_imp  = rf_m.get('feature_importances', {})
    xgb_imp = xgb_m.get('feature_importances', {})

    imp_df = pd.DataFrame({
        'Feature': features,
        'Random Forest': [rf_imp.get(f, 0) for f in features],
        'XGBoost': [xgb_imp.get(f, 0) for f in features],
    })
    imp_df['Difference'] = imp_df['XGBoost'] - imp_df['Random Forest']
    imp_df = imp_df.sort_values('Random Forest', ascending=True)

    fig_imp = go.Figure()
    fig_imp.add_trace(go.Bar(name='🌲 Random Forest', y=imp_df['Feature'], x=imp_df['Random Forest'],
                             orientation='h', marker_color='#4fc3f7', opacity=0.85))
    fig_imp.add_trace(go.Bar(name='⚡ XGBoost', y=imp_df['Feature'], x=imp_df['XGBoost'],
                             orientation='h', marker_color='#ab47bc', opacity=0.85))
    fig_imp.update_layout(
        barmode='group', height=380,
        margin=dict(l=20, r=20, t=50, b=40),
        title=dict(text="Feature Influence — Which Behaviors Drive Risk?", font=dict(color="#4fc3f7", size=14)),
        xaxis_title="Importance Score",
        legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor="#e2e8f0", borderwidth=1),
        **CHART_THEME,
    )
    fig_imp.update_xaxes(gridcolor="#f1f5f9", tickfont_color="#94a3b8")
    fig_imp.update_yaxes(gridcolor="#f1f5f9", tickfont_color="#94a3b8")
    st.plotly_chart(fig_imp, use_container_width=True)

    # Feature descriptions
    feature_desc = {
        'avg_usage':       '📊 Average water consumption per reading',
        'max_usage':       '📈 Maximum single reading — detects burst events',
        'std_usage':       '📉 Volatility of consumption — erratic usage signals leaks',
        'night_avg_usage': '🌙 Average usage at night (12 AM – 5 AM) — key leak indicator',
        'avg_spike_ratio': '⚡ Average anomaly spike ratio over time',
        'max_spike_ratio': '🔺 Maximum spike ratio — detects the worst anomaly',
        'std_spike_ratio': '🎲 Spike ratio volatility — unstable patterns',
    }
    desc_items = "".join([f"<li><code>{f}</code> — {feature_desc.get(f, 'Behavioral metric')}</li>" for f in features])
    st.markdown(f"""<div class="insight-box" style="font-size:0.85rem;">
        <b>📖 Feature Descriptions:</b>
        <ul style="margin-top:6px; line-height:1.7;">{desc_items}</ul>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ════════════════════════════════════════════
    # Section 5: Training Configuration Details
    # ════════════════════════════════════════════
    st.markdown('<div class="section-header" style="font-size:1.15rem">⚙️ Model Configuration &amp; Training Details</div>', unsafe_allow_html=True)

    cfg_c1, cfg_c2 = st.columns(2)
    with cfg_c1:
        rf_params = rf_m.get('model_params', {})
        params_html = "".join([f"<tr><td style='color:#90a4c4; padding:6px 12px; border-bottom:1px solid #1a2f4a;'>{k}</td><td style='color:#4fc3f7; padding:6px 12px; border-bottom:1px solid #1a2f4a; font-weight:600;'>{v}</td></tr>" for k, v in rf_params.items()])
        st.markdown(f"""
        <div style="background:#0d1f3c; border:1px solid #1e3a5f; border-radius:12px; padding:18px; border-top:3px solid #4fc3f7;">
            <h4 style="color:#4fc3f7; margin-top:0;">🌲 Random Forest Configuration</h4>
            <table style="width:100%; border-collapse:collapse;">{params_html}</table>
            <p style="color:#7090b0; font-size:0.78rem; margin-top:12px;">Training samples: {rf_m.get('training_samples', 'N/A')} | Test samples: {rf_m.get('test_samples', 'N/A')}</p>
        </div>""", unsafe_allow_html=True)

    with cfg_c2:
        xgb_params = xgb_m.get('model_params', {})
        params_html = "".join([f"<tr><td style='color:#90a4c4; padding:6px 12px; border-bottom:1px solid #2a1a4a;'>{k}</td><td style='color:#ab47bc; padding:6px 12px; border-bottom:1px solid #2a1a4a; font-weight:600;'>{v}</td></tr>" for k, v in xgb_params.items()])
        st.markdown(f"""
        <div style="background:#1a0d2e; border:1px solid #3a1e5f; border-radius:12px; padding:18px; border-top:3px solid #ab47bc;">
            <h4 style="color:#ab47bc; margin-top:0;">⚡ XGBoost Configuration</h4>
            <table style="width:100%; border-collapse:collapse;">{params_html}</table>
            <p style="color:#7090b0; font-size:0.78rem; margin-top:12px;">Training samples: {xgb_m.get('training_samples', 'N/A')} | Test samples: {xgb_m.get('test_samples', 'N/A')}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ════════════════════════════════════════════
    # Section 6: Detailed Metrics Table
    # ════════════════════════════════════════════
    st.markdown('<div class="section-header" style="font-size:1.15rem">📋 Complete Metrics Summary</div>', unsafe_allow_html=True)

    summary_data = pd.DataFrame({
        'Metric': ['Accuracy', 'Precision', 'Recall (Sensitivity)', 'F1 Score', 'AUC-ROC',
                   'True Negatives', 'False Positives', 'False Negatives', 'True Positives'],
        'Random Forest': [
            f"{rf_m['accuracy']:.4f}", f"{rf_m['precision']:.4f}", f"{rf_m['recall']:.4f}",
            f"{rf_m['f1']:.4f}", f"{rf_m['auc_roc']:.4f}",
            str(rf_m['confusion_matrix'][0][0]), str(rf_m['confusion_matrix'][0][1]),
            str(rf_m['confusion_matrix'][1][0]), str(rf_m['confusion_matrix'][1][1]),
        ],
        'XGBoost': [
            f"{xgb_m['accuracy']:.4f}", f"{xgb_m['precision']:.4f}", f"{xgb_m['recall']:.4f}",
            f"{xgb_m['f1']:.4f}", f"{xgb_m['auc_roc']:.4f}",
            str(xgb_m['confusion_matrix'][0][0]), str(xgb_m['confusion_matrix'][0][1]),
            str(xgb_m['confusion_matrix'][1][0]), str(xgb_m['confusion_matrix'][1][1]),
        ],
    })

    # Best indicator
    best = []
    for i in range(5):
        rv = float(summary_data['Random Forest'].iloc[i])
        xv = float(summary_data['XGBoost'].iloc[i])
        best.append("🌲 RF" if rv > xv else "⚡ XGB" if xv > rv else "🤝 Tie")
    best += ["—", "—", "—", "—"]
    summary_data['Winner'] = best

    st.dataframe(summary_data, use_container_width=True, height=380)

    # ════════════════════════════════════════════
    # Section 7: Key Takeaways
    # ════════════════════════════════════════════
    st.markdown('<div class="section-header" style="font-size:1.15rem">💡 Key Takeaways</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background: linear-gradient(135deg, #0d2137 0%, #0f2a47 100%);
                border: 1px solid #1e3a5f; border-radius: 12px; padding: 22px; margin-bottom: 16px;">
        <h4 style="color:#4fc3f7; margin-top:0;">Why Use Two Models?</h4>
        <ul style="color:#c8ddf2; font-size:0.9rem; line-height:1.8;">
            <li><b>Ensemble Confidence:</b> When both models agree on a prediction, we have much higher 
                confidence in the result. Disagreements flag borderline cases for manual review.</li>
            <li><b>Different Perspectives:</b> Random Forest uses <i>bagging</i> (parallel trees, majority vote) 
                while XGBoost uses <i>boosting</i> (sequential error correction). They capture different patterns.</li>
            <li><b>Robustness:</b> If one model is affected by data drift or noise, the other provides a safety net.
                This is critical for infrastructure monitoring where missed leaks are costly.</li>
            <li><b>Interpretability vs Performance:</b> Random Forest feature importance is intuitive and stable; 
                XGBoost often squeezes out slightly better accuracy with gradient optimization.</li>
        </ul>
    </div>

    <div style="background: linear-gradient(135deg, #1e1e0d 0%, #2a2a14 100%);
                border: 1px solid #5f5f1e; border-radius: 12px; padding: 22px;">
        <h4 style="color:#ffa726; margin-top:0;">📊 Metric Explanations</h4>
        <ul style="color:#c8ddf2; font-size:0.88rem; line-height:1.8;">
            <li><b>Accuracy:</b> Overall correctness — what % of all predictions were right.</li>
            <li><b>Precision:</b> Of households flagged as high-risk, what % truly are. High precision = few false alarms.</li>
            <li><b>Recall (Sensitivity):</b> Of all actual high-risk households, what % did we catch. 
                <i>Critical for safety — missed leaks are expensive.</i></li>
            <li><b>F1 Score:</b> Harmonic mean of precision &amp; recall — balances both concerns.</li>
            <li><b>AUC-ROC:</b> Model's ability to rank high-risk above normal across all thresholds. 
                Higher = better discrimination ability.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGE 7 — SMART INSIGHTS PANEL
# ──────────────────────────────────────────────
def page_insights(df: pd.DataFrame):
    st.markdown('<div class="section-header">🧠 Smart Insights Panel</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automatically generated analytics intelligence from the dataset</div>', unsafe_allow_html=True)

    total = len(df)

    # ── Peak hours ──
    hourly_avg = df.groupby("hour")["water_usage_liters"].mean()
    peak_hour  = int(hourly_avg.idxmax())
    low_hour   = int(hourly_avg.idxmin())
    peak_val   = hourly_avg.max()

    # ── Spike stats ──
    pct_spike2 = (df["spike_ratio"] > 2).sum() / total * 100
    pct_spike3 = (df["spike_ratio"] > 3).sum() / total * 100
    avg_spike  = df["spike_ratio"].mean()

    # ── Leak stats ──
    leak_rate  = df["leak_flag_detected"].mean() * 100
    top5_leak  = df.groupby("household_id")["leak_flag_detected"].sum().nlargest(5)

    # ── Risk ──
    critical_pct = (df["risk_level"] == "Critical").sum() / total * 100
    high_pct     = (df["risk_level"] == "High Risk").sum() / total * 100

    insights = [
        ("info",    f"🕐 Peak consumption occurs at **{peak_hour:02d}:00** with avg {peak_val:.1f} L. "
                    f"Lowest demand is at **{low_hour:02d}:00**."),
        ("warning", f"⚠️ **{pct_spike2:.1f}%** of readings show abnormal spikes (ratio > 2). "
                    f"**{pct_spike3:.1f}%** are critically high (ratio > 3)."),
        ("info",    f"📊 Average spike ratio across the entire dataset is **{avg_spike:.3f}**. "
                    f"Values above 2.0 require immediate inspection."),
        ("danger",  f"🚨 Overall leak detection rate: **{leak_rate:.1f}%** of all records triggered a leak event."),
        ("warning", f"🔴 **{critical_pct:.1f}%** of records are in the Critical risk tier; "
                    f"**{high_pct:.1f}%** in High Risk."),
        ("success", f"✅ {(100 - pct_spike2):.1f}% of readings are within normal consumption bounds (spike ratio ≤ 2)."),
    ]

    col_cls = {"info": "", "warning": "warning", "danger": "danger", "success": "success"}
    for kind, text in insights:
        st.markdown(f'<div class="insight-box {col_cls[kind]}">{text}</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Top households by leak events
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🏆 Top 10 Households — Leak Events")
        top_leaks = df.groupby("household_id")["leak_flag_detected"].sum().nlargest(10).reset_index()
        fig = px.bar(top_leaks, x="household_id", y="leak_flag_detected",
                     color="leak_flag_detected", color_continuous_scale="Reds",
                     labels={"household_id": "Household", "leak_flag_detected": "Leak Events"})
        apply_theme(fig, "", 360)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### 📈 Top 10 Households — Avg Spike Ratio")
        top_spikes = df.groupby("household_id")["spike_ratio"].mean().nlargest(10).reset_index()
        fig2 = px.bar(top_spikes, x="household_id", y="spike_ratio",
                      color="spike_ratio", color_continuous_scale="Oranges",
                      labels={"household_id": "Household", "spike_ratio": "Avg Spike Ratio"})
        apply_theme(fig2, "", 360)
        st.plotly_chart(fig2, use_container_width=True)

    # Monthly trend
    monthly = df.groupby("month").agg(
        avg_usage=("water_usage_liters", "mean"),
        leak_events=("leak_flag_detected", "sum"),
        avg_spike=("spike_ratio", "mean"),
    ).reset_index()

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(go.Bar(x=monthly["month"], y=monthly["avg_usage"],
                          name="Avg Usage (L)", marker_color="#4fc3f7", opacity=0.7), secondary_y=False)
    fig3.add_trace(go.Scatter(x=monthly["month"], y=monthly["leak_events"],
                              name="Leak Events", mode="lines+markers",
                              line=dict(color="#ef5350", width=2)), secondary_y=True)
    fig3.update_layout(height=360, paper_bgcolor="#0d1526", plot_bgcolor="#0d1526",
                       font_color="#c8d8f0", title=dict(text="Monthly Usage vs Leak Events", font=dict(color="#4fc3f7")),
                       legend=dict(bgcolor="rgba(13,21,38,0.8)", bordercolor="#1e3a5f"))
    fig3.update_xaxes(gridcolor="#f1f5f9", tickfont_color="#94a3b8")
    fig3.update_yaxes(gridcolor="#f1f5f9", tickfont_color="#94a3b8")
    st.plotly_chart(fig3, use_container_width=True)


# ──────────────────────────────────────────────
# PAGE 8 — DATA FILTERS / RAW EXPLORER
# ──────────────────────────────────────────────
def page_data(df: pd.DataFrame):
    st.markdown('<div class="section-header">🗃️ Filtered Data Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Full interactive data table reflecting all active sidebar filters</div>', unsafe_allow_html=True)

    st.info(f"**{len(df):,}** records match the current filter criteria.")

    # Column selector
    all_cols = list(df.columns)
    visible  = st.multiselect(
        "Select columns to display",
        all_cols,
        default=["household_id","timestamp","hour","water_usage_liters","spike_ratio",
                 "leak_flag_detected","leak_severity","leak_probability","risk_level"],
    )

    # Sort
    sort_col = st.selectbox("Sort by", visible, index=0)
    sort_asc = st.radio("Order", ["Descending", "Ascending"], horizontal=True) == "Ascending"

    display_df = df[visible].sort_values(sort_col, ascending=sort_asc).reset_index(drop=True)
    st.dataframe(display_df, use_container_width=True, height=500)

    # Download
    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️  Download Filtered CSV",
        data=csv_bytes,
        file_name="filtered_water_data.csv",
        mime="text/csv",
    )

    # Quick stats
    st.markdown("#### 📊 Quick Statistics")
    numeric_cols = display_df.select_dtypes(include=np.number).columns.tolist()
    if numeric_cols:
        st.dataframe(display_df[numeric_cols].describe().T.style.background_gradient(cmap="Blues"),
                     use_container_width=True)


# ──────────────────────────────────────────────
# PAGE 8 — METHODOLOGY & DEFINITIONS
# ──────────────────────────────────────────────
def page_methodology(df: pd.DataFrame):
    st.markdown('<div class="section-header">📖 Methodology & Data Dictionary</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Technical transparency for formulas, thresholds, and risk profiling logic.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background-color: #1e2638; padding: 20px; border-radius: 8px; border-left: 5px solid #4fc3f7; margin-bottom: 20px;">
        <h4 style="color:#c8d8f0; margin-top:0;">1. Spike Ratio (Anomaly Detection)</h4>
        <p style="color:#90a4c4; font-size:14px; margin-bottom:5px;"><b>Formula:</b> <code>Spike Ratio = Current Hourly Usage / 7-Day Rolling Average</code></p>
        <ul style="color:#90a4c4; font-size:14px;">
            <li><b>< 1.0:</b> Below average usage (Normal).</li>
            <li><b>1.0 - 1.5:</b> Slightly elevated usage (Expected variance).</li>
            <li><b>1.5 - 3.0:</b> High Variance (Moderate Anomaly).</li>
            <li><b>> 3.0:</b> Severe Spike (Significant Anomaly/Potential Burst).</li>
        </ul>
    </div>
    
    <div style="background-color: #1e2638; padding: 20px; border-radius: 8px; border-left: 5px solid #ffa726; margin-bottom: 20px;">
        <h4 style="color:#c8d8f0; margin-top:0;">2. Leak Probability (Bayesian/Heuristic)</h4>
        <p style="color:#90a4c4; font-size:14px; margin-bottom:5px;">Calculated dynamically as a weighted score incorporating continuous prolonged usage (especially at night) and severe volume spikes.</p>
        <ul style="color:#90a4c4; font-size:14px;">
            <li><b>Threshold:</b> Probability > 0.8 automatically triggers a <code>leak_flag</code>.</li>
        </ul>
    </div>

    <div style="background-color: #1e2638; padding: 20px; border-radius: 8px; border-left: 5px solid #ef5350; margin-bottom: 20px;">
        <h4 style="color:#c8d8f0; margin-top:0;">3. Household Risk Tiers</h4>
        <p style="color:#90a4c4; font-size:14px; margin-bottom:5px;">Each record is ranked. A household's overarching priority is typically dictated by its highest historical risk tier.</p>
        <ul style="color:#90a4c4; font-size:14px;">
            <li><b>🟢 Normal:</b> No sustained anomalies.</li>
            <li><b>🟡 Low Risk:</b> Occasional minor spikes.</li>
            <li><b>🟠 Moderate Risk:</b> Frequent spikes or minor continuous flow (Prob: 0.4 - 0.7).</li>
            <li><b>🔴 High Risk:</b> High probability of hidden minor leak (Prob: 0.7 - 0.9).</li>
            <li><b>🚨 Critical:</b> Active burst pipe or massive continuous flow (Prob > 0.9).</li>
        </ul>
    </div>

    <div style="background-color: #1e2638; padding: 20px; border-radius: 8px; border-left: 5px solid #4fc3f7; margin-bottom: 20px;">
        <h4 style="color:#c8d8f0; margin-top:0;">4. Random Forest Classifier</h4>
        <p style="color:#90a4c4; font-size:14px; margin-bottom:5px;">An <b>ensemble learning</b> method that operates by constructing <b>100 decision trees</b> during training. Each tree is trained on a random subset of data (bagging) and features. Final prediction = majority vote.</p>
        <ul style="color:#90a4c4; font-size:14px;">
            <li><b>Inputs:</b> <i>Avg Usage, Max Usage, Night Usage (12 AM–5 AM), Std Dev of Usage, Spike Ratios (avg, max, std).</i></li>
            <li><b>Method:</b> Bagging (Bootstrap Aggregating) — parallel independent trees → majority vote.</li>
            <li><b>Target:</b> Predicts if a household is "High Risk" (1) or "Normal" (0) based on aggregated behavioral patterns.</li>
            <li><b>Advantage:</b> Robust to noise and outliers, requires minimal tuning, and provides interpretable feature importances.</li>
        </ul>
    </div>

    <div style="background-color: #1e2638; padding: 20px; border-radius: 8px; border-left: 5px solid #ab47bc; margin-bottom: 20px;">
        <h4 style="color:#c8d8f0; margin-top:0;">5. XGBoost Classifier (Extreme Gradient Boosting)</h4>
        <p style="color:#90a4c4; font-size:14px; margin-bottom:5px;">A <b>gradient boosting</b> algorithm that builds <b>150 trees sequentially</b>, where each tree corrects the residual errors of the previous ones using <b>gradient descent</b>.</p>
        <ul style="color:#90a4c4; font-size:14px;">
            <li><b>Inputs:</b> Same 7 behavioral features as Random Forest for fair comparison.</li>
            <li><b>Method:</b> Boosting — sequential dependent trees → additive error correction.</li>
            <li><b>Regularization:</b> Built-in L1/L2 regularization prevents overfitting; <code>scale_pos_weight</code> handles class imbalance.</li>
            <li><b>Key Params:</b> learning_rate=0.1, max_depth=6, subsample=0.8, colsample_bytree=0.8.</li>
            <li><b>Advantage:</b> Often achieves higher accuracy, hardware-optimized, handles imbalanced data well.</li>
        </ul>
    </div>

    <div style="background-color: #1e2638; padding: 20px; border-radius: 8px; border-left: 5px solid #66bb6a; margin-bottom: 20px;">
        <h4 style="color:#c8d8f0; margin-top:0;">6. Dual-Model Ensemble Strategy</h4>
        <p style="color:#90a4c4; font-size:14px; margin-bottom:5px;">This system uses <b>both models simultaneously</b> to provide higher-confidence predictions.</p>
        <ul style="color:#90a4c4; font-size:14px;">
            <li><b>Agreement (Both predict same class):</b> High confidence — proceed with automated action.</li>
            <li><b>Disagreement (Models conflict):</b> Flags the case for manual review — the household likely falls in a borderline risk zone.</li>
            <li><b>Bagging vs Boosting:</b> Different learning paradigms capture complementary patterns, reducing overall prediction error.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# MAIN APP
# ──────────────────────────────────────────────
def main():
    # ── Clean White Header Banner ──
    st.markdown("""
    <style>
    @keyframes headerShimmer {
        0%   { background-position: -200% 0; }
        100% { background-position:  200% 0; }
    }
    @keyframes statusPulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0.5); }
        70%       { box-shadow: 0 0 0 5px rgba(16,185,129,0); }
    }
    .header-banner {
        background: linear-gradient(135deg, #ffffff 0%, #f0f7ff 60%, #f8fafc 100%);
        padding: 26px 34px 22px;
        border-radius: 20px;
        margin-bottom: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 24px rgba(37,99,235,0.07), 0 1px 3px rgba(0,0,0,0.04);
        position: relative;
        overflow: hidden;
    }
    .header-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #2563eb, #0ea5e9, #7c3aed, #2563eb);
        background-size: 200% 100%;
        animation: headerShimmer 4s linear infinite;
    }
    .header-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.85rem;
        font-weight: 800;
        margin: 0 0 5px 0;
        background: linear-gradient(90deg, #1e40af, #2563eb, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
        line-height: 1.25;
    }
    .header-subtitle {
        font-family: 'Inter', sans-serif;
        color: #94a3b8;
        margin: 0;
        font-size: 0.87rem;
        font-weight: 400;
    }
    .status-dot {
        display: inline-block;
        width: 8px; height: 8px;
        background: #10b981;
        border-radius: 50%;
        margin-right: 6px;
        animation: statusPulse 2s ease-in-out infinite;
    }
    .status-text {
        font-size: 0.78rem;
        color: #059669;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    .header-tags { display: flex; gap: 8px; margin-top: 14px; flex-wrap: wrap; }
    .header-tag {
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.6px;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        color: #64748b;
        background: #f8fafc;
        transition: all 0.2s ease;
    }
    </style>
    """, unsafe_allow_html=True)

    # Load data
    df = load_data()

    # Sidebar filters → returns filtered dataframe
    filtered_df = render_sidebar(df)

    # ── Navigation ──
    pages = {
        "📊 System Overview":              page_overview,
        "🔴 Leakage Severity Analysis":    page_severity,
        "🏠 Household Risk Intelligence":  page_risk,
        "💧 Water Consumption Behavior":   page_consumption,
        "⚠️ Abnormal Pattern Detection":   page_anomalies,
        "🔬 Household Explorer":           page_explorer,
        "🤖 ML Risk Prediction":           page_ml_prediction,
        "📈 Model Comparison (RF vs XGB)": page_model_comparison,
        "🧠 Smart Insights Panel":         page_insights,
        "🗃️ Data Explorer":               page_data,
        "📖 Methodology & Formulas":       page_methodology,
    }

    st.sidebar.markdown("""
    <div style="height:1px; background:linear-gradient(90deg, #e2e8f0, transparent);
                margin: 8px 4px 14px 4px;"></div>
    <div style="font-size:0.68rem; text-transform:uppercase; letter-spacing:1.5px; color:#94a3b8;
                font-family:'Inter',sans-serif; font-weight:700; padding: 0 4px; margin-bottom:6px;">
        📑 Navigation
    </div>
    """, unsafe_allow_html=True)
    selected_page = st.sidebar.radio("Navigate to", list(pages.keys()), label_visibility="collapsed")

    # Warn if filters remove too much data
    if len(filtered_df) == 0:
        st.error("⚠️ No records match the current filters. Please adjust the sidebar filters.")
        return

    # Header banner only on sub-pages (System Overview uses clean reference layout)
    if selected_page != "📊 System Overview":
        st.markdown("""
        <div class="header-banner">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                <div>
                    <h1 class="header-title">💧 Smart Water Leakage Detection</h1>
                    <p class="header-subtitle">Big Data Analytics Platform &nbsp;·&nbsp; Smart City Infrastructure Monitoring</p>
                    <div class="header-tags">
                        <span class="header-tag">🔥 Apache Spark</span>
                        <span class="header-tag">🤖 ML Ensemble</span>
                        <span class="header-tag">📊 4.32M+ Records</span>
                        <span class="header-tag">🏠 1,000 Households</span>
                    </div>
                </div>
                <div style="text-align:right; padding-top:6px;">
                    <div><span class="status-dot"></span><span class="status-text">System Online</span></div>
                    <div style="font-size:0.7rem; color:#cbd5e1; margin-top:5px; font-family:'Inter',sans-serif;">
                        Real-Time Monitoring Active
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    pages[selected_page](filtered_df)

    # ── Clean White Footer ──
    st.markdown("""
    <div style="margin-top: 3rem; padding: 18px 24px;
                background: #ffffff;
                border-radius: 14px; border: 1px solid #e2e8f0;
                box-shadow: 0 1px 4px rgba(0,0,0,0.04);
                display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:1.1rem;">💧</span>
            <span style="font-family:'Inter',sans-serif; font-size:0.82rem; color:#475569; font-weight:600;">
                Smart Water Leakage Detection System
            </span>
            <span style="color:#e2e8f0; margin: 0 4px;">·</span>
            <span style="font-family:'Inter',sans-serif; font-size:0.8rem; color:#94a3b8;">
                Big Data Analytics Platform
            </span>
        </div>
        <div style="font-family:'Inter',sans-serif; font-size:0.72rem; color:#cbd5e1;">
            Apache Spark · Streamlit · Plotly · scikit-learn · XGBoost
        </div>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

