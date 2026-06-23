import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ============================================================
# Multi-Touch Marketing Attribution and ROI Dashboard
# Author: Chaitanya Pawar
# ============================================================

st.set_page_config(
    page_title="Multi-Touch Attribution ROI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------------------------------
# Basic Styling
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #0f172a;
        font-weight: 800;
    }
    h2, h3 {
        color: #1e293b;
    }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 16px;
        border-radius: 14px;
        box-shadow: 0px 4px 12px rgba(15, 23, 42, 0.06);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# File Paths
# ------------------------------------------------------------
DATA_DIR = Path("data")

SUMMARY_FILE = DATA_DIR / "attribution_channel_summary.csv"

# This app supports both possible cleaned file names.
CLEANED_FILE_OPTIONS = [
    DATA_DIR / "cleaned_multi_touch_attribution_dataset.csv",
    DATA_DIR / "cleaned_multi__touch_attribution_dataset.csv"
]


def find_cleaned_file():
    for file_path in CLEANED_FILE_OPTIONS:
        if file_path.exists():
            return file_path
    return None


# ------------------------------------------------------------
# Load Data
# ------------------------------------------------------------
@st.cache_data
def load_data():
    if not SUMMARY_FILE.exists():
        st.error("Missing file: data/attribution_channel_summary.csv")
        st.stop()

    cleaned_file = find_cleaned_file()

    if cleaned_file is None:
        st.error(
            "Missing cleaned dataset. Please add one of these files inside the data folder:\n\n"
            "1. cleaned_multi_touch_attribution_dataset.csv\n"
            "2. cleaned_multi__touch_attribution_dataset.csv"
        )
        st.stop()

    summary_df = pd.read_csv(SUMMARY_FILE)
    cleaned_df = pd.read_csv(cleaned_file)

    # Standardize column names just in case there are spaces
    summary_df.columns = summary_df.columns.str.strip()
    cleaned_df.columns = cleaned_df.columns.str.strip()

    # Convert timestamp if available
    if "event_timestamp_utc" in cleaned_df.columns:
        cleaned_df["event_timestamp_utc"] = pd.to_datetime(
            cleaned_df["event_timestamp_utc"],
            errors="coerce"
        )

    return summary_df, cleaned_df


summary_df, cleaned_df = load_data()

# ------------------------------------------------------------
# Required Column Check
# ------------------------------------------------------------
required_summary_columns = {
    "attribution_model",
    "channel",
    "attributed_conversions",
    "attributed_revenue",
    "total_spend",
    "roas",
    "cac"
}

missing_columns = required_summary_columns - set(summary_df.columns)

if missing_columns:
    st.error(f"Missing columns in attribution_channel_summary.csv: {missing_columns}")
    st.stop()

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.title("Multi-Touch Marketing Attribution and ROI Dashboard")

st.markdown(
    """
    This dashboard analyzes marketing channel performance using **First-Touch**, 
    **Last-Touch**, and **Linear Attribution** models. It helps identify which 
    channels contribute most to revenue, conversions, ROAS, and CAC.
    """
)

# ------------------------------------------------------------
# Sidebar Filters
# ------------------------------------------------------------
st.sidebar.title("Dashboard Filters")

models = sorted(summary_df["attribution_model"].dropna().unique())

default_model_index = 0
if "Linear" in models:
    default_model_index = models.index("Linear")

selected_model = st.sidebar.radio(
    "Select Attribution Model",
    models,
    index=default_model_index
)

channels = sorted(summary_df["channel"].dropna().unique())

selected_channels = st.sidebar.multiselect(
    "Select Channels",
    channels,
    default=channels
)

filtered_df = summary_df[
    (summary_df["attribution_model"] == selected_model)
    & (summary_df["channel"].isin(selected_channels))
].copy()

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ------------------------------------------------------------
# KPI Cards
# ------------------------------------------------------------
total_spend = filtered_df["total_spend"].sum()
total_revenue = filtered_df["attributed_revenue"].sum()
total_conversions = filtered_df["attributed_conversions"].sum()

overall_roas = total_revenue / total_spend if total_spend != 0 else 0
overall_cac = total_spend / total_conversions if total_conversions != 0 else 0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric("Total Spend", f"${total_spend:,.2f}")
kpi2.metric("Attributed Revenue", f"${total_revenue:,.2f}")
kpi3.metric("Attributed Conversions", f"{total_conversions:,.2f}")
kpi4.metric("ROAS", f"{overall_roas:,.2f}")
kpi5.metric("CAC", f"${overall_cac:,.2f}")

st.divider()

# ------------------------------------------------------------
# Dashboard Charts
# ------------------------------------------------------------
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Channel Revenue")
    revenue_chart = px.bar(
        filtered_df.sort_values("attributed_revenue", ascending=True),
        x="attributed_revenue",
        y="channel",
        orientation="h",
        text="attributed_revenue",
        title=f"Attributed Revenue by Channel - {selected_model}"
    )
    revenue_chart.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    revenue_chart.update_layout(
        height=430,
        xaxis_title="Attributed Revenue",
        yaxis_title="Channel"
    )
    st.plotly_chart(revenue_chart, use_container_width=True)

with chart_col2:
    st.subheader("ROAS by Channel")
    roas_chart = px.bar(
        filtered_df.sort_values("roas", ascending=True),
        x="roas",
        y="channel",
        orientation="h",
        text="roas",
        title=f"ROAS by Channel - {selected_model}"
    )
    roas_chart.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    roas_chart.update_layout(
        height=430,
        xaxis_title="ROAS",
        yaxis_title="Channel"
    )
    st.plotly_chart(roas_chart, use_container_width=True)

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader("CAC by Channel")
    cac_chart = px.bar(
        filtered_df.sort_values("cac", ascending=True),
        x="cac",
        y="channel",
        orientation="h",
        text="cac",
        title=f"CAC by Channel - {selected_model}"
    )
    cac_chart.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    cac_chart.update_layout(
        height=430,
        xaxis_title="CAC",
        yaxis_title="Channel"
    )
    st.plotly_chart(cac_chart, use_container_width=True)

with chart_col4:
    st.subheader("Conversions by Channel")
    conversion_chart = px.bar(
        filtered_df.sort_values("attributed_conversions", ascending=True),
        x="attributed_conversions",
        y="channel",
        orientation="h",
        text="attributed_conversions",
        title=f"Attributed Conversions by Channel - {selected_model}"
    )
    conversion_chart.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    conversion_chart.update_layout(
        height=430,
        xaxis_title="Attributed Conversions",
        yaxis_title="Channel"
    )
    st.plotly_chart(conversion_chart, use_container_width=True)

st.divider()

# ------------------------------------------------------------
# Funnel Analysis
# ------------------------------------------------------------
st.subheader("Customer Funnel Analysis")

if "funnel_stage" in cleaned_df.columns and "event_id" in cleaned_df.columns:
    funnel_order = ["Awareness", "Consideration", "Decision", "Purchase"]

    funnel_df = (
        cleaned_df.groupby("funnel_stage")["event_id"]
        .count()
        .reset_index()
        .rename(columns={"event_id": "touchpoints"})
    )

    # Apply order only if these labels exist
    existing_order = [stage for stage in funnel_order if stage in funnel_df["funnel_stage"].values]

    if existing_order:
        funnel_df["funnel_stage"] = pd.Categorical(
            funnel_df["funnel_stage"],
            categories=existing_order,
            ordered=True
        )
        funnel_df = funnel_df.sort_values("funnel_stage")

    funnel_chart = px.funnel(
        funnel_df,
        x="touchpoints",
        y="funnel_stage",
        title="Funnel Stage Touchpoint Count"
    )
    funnel_chart.update_layout(height=420)
    st.plotly_chart(funnel_chart, use_container_width=True)
else:
    st.info("Funnel analysis requires funnel_stage and event_id columns in the cleaned dataset.")

st.divider()

# ------------------------------------------------------------
# Data Table
# ------------------------------------------------------------
st.subheader("Attribution Channel Summary Table")

display_df = filtered_df.copy()

round_columns = [
    "attributed_conversions",
    "attributed_revenue",
    "total_spend",
    "roas",
    "cac"
]

for column in round_columns:
    if column in display_df.columns:
        display_df[column] = display_df[column].round(2)

st.dataframe(display_df, use_container_width=True)

# ------------------------------------------------------------
# Business Insights
# ------------------------------------------------------------
st.subheader("Business Insights")

top_revenue_channel = filtered_df.sort_values(
    "attributed_revenue",
    ascending=False
)["channel"].iloc[0]

top_roas_channel = filtered_df.sort_values(
    "roas",
    ascending=False
)["channel"].iloc[0]

lowest_cac_channel = filtered_df.sort_values(
    "cac",
    ascending=True
)["channel"].iloc[0]

st.markdown(
    f"""
    Based on the selected **{selected_model}** model:

    - **Top revenue channel:** `{top_revenue_channel}`
    - **Best ROAS channel:** `{top_roas_channel}`
    - **Lowest CAC channel:** `{lowest_cac_channel}`

    These results help marketing managers compare channels, reduce wasted ad spend,
    and make better budget allocation decisions.
    """
)

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.divider()

st.caption(
    "Created by Chaitanya Pawar | Data Analytics Internship Project | Infotact Solutions & Co."
)
