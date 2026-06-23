import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# ============================================================
# Multi-Touch Marketing Attribution and ROI Dashboard
# Author: Chaitanya Pawar
# Upgraded Streamlit Version:
# 1. Attribution model toggle
# 2. ROI scatter plot
# 3. Funnel drop-off table
# 4. Campaign-level drilldown
# ============================================================

st.set_page_config(
    page_title="Multi-Touch Attribution ROI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------------------------------
# Styling
# ------------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        font-weight: 800;
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
# File paths
# ------------------------------------------------------------
DATA_DIR = Path("data")

SUMMARY_FILE = DATA_DIR / "attribution_channel_summary.csv"
ATTRIBUTION_FILE = DATA_DIR / "attribution_model_output.csv"

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
# Load data
# ------------------------------------------------------------
@st.cache_data
def load_data():
    if not SUMMARY_FILE.exists():
        st.error("Missing file: data/attribution_channel_summary.csv")
        st.stop()

    cleaned_file = find_cleaned_file()
    if cleaned_file is None:
        st.error(
            "Missing cleaned dataset. Please add cleaned_multi_touch_attribution_dataset.csv "
            "inside the data folder."
        )
        st.stop()

    summary_df = pd.read_csv(SUMMARY_FILE)
    cleaned_df = pd.read_csv(cleaned_file)

    attribution_df = None
    if ATTRIBUTION_FILE.exists():
        attribution_df = pd.read_csv(ATTRIBUTION_FILE)

    # Clean column names
    summary_df.columns = summary_df.columns.str.strip()
    cleaned_df.columns = cleaned_df.columns.str.strip()

    if attribution_df is not None:
        attribution_df.columns = attribution_df.columns.str.strip()

    # Convert timestamp
    if "event_timestamp_utc" in cleaned_df.columns:
        cleaned_df["event_timestamp_utc"] = pd.to_datetime(
            cleaned_df["event_timestamp_utc"],
            errors="coerce"
        )

    return summary_df, cleaned_df, attribution_df


summary_df, cleaned_df, attribution_df = load_data()

# ------------------------------------------------------------
# Required columns check
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

missing_summary_cols = required_summary_columns - set(summary_df.columns)

if missing_summary_cols:
    st.error(f"Missing columns in attribution_channel_summary.csv: {missing_summary_cols}")
    st.stop()

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.title("📊 Multi-Touch Marketing Attribution and ROI Dashboard")

st.markdown(
    """
    This dashboard analyzes marketing channel performance using **First-Touch**, 
    **Last-Touch**, and **Linear Attribution** models. It helps marketing managers 
    understand revenue contribution, conversions, ROAS, CAC, funnel drop-off, and campaign performance.
    """
)

# ------------------------------------------------------------
# Sidebar filters
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
# KPI cards
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
# Channel-level charts
# ------------------------------------------------------------
st.header("1. Channel Performance Overview")

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
# ROI Scatter Plot
# ------------------------------------------------------------
st.header("2. ROI Scatter Plot")

scatter_df = filtered_df.copy()

# Avoid zero-size bubbles
scatter_df["bubble_size"] = scatter_df["attributed_conversions"].clip(lower=1)

roi_scatter = px.scatter(
    scatter_df,
    x="total_spend",
    y="attributed_revenue",
    size="bubble_size",
    color="channel",
    hover_name="channel",
    hover_data={
        "total_spend": ":.2f",
        "attributed_revenue": ":.2f",
        "attributed_conversions": ":.2f",
        "roas": ":.2f",
        "cac": ":.2f",
        "bubble_size": False
    },
    title=f"ROI Scatter Plot - Spend vs Revenue ({selected_model})"
)

roi_scatter.update_layout(
    height=500,
    xaxis_title="Total Spend",
    yaxis_title="Attributed Revenue"
)

st.plotly_chart(roi_scatter, use_container_width=True)

st.caption(
    "Interpretation: Channels in the upper-left area are more efficient because they generate higher revenue with lower spend."
)

st.divider()

# ------------------------------------------------------------
# Funnel Analysis with Drop-off
# ------------------------------------------------------------
st.header("3. Funnel Analysis and Drop-off Rate")

if "funnel_stage" in cleaned_df.columns and "event_id" in cleaned_df.columns:
    funnel_order = ["Awareness", "Consideration", "Decision", "Purchase"]

    funnel_df = (
        cleaned_df.groupby("funnel_stage")["event_id"]
        .count()
        .reset_index()
        .rename(columns={"event_id": "touchpoints"})
    )

    existing_order = [stage for stage in funnel_order if stage in funnel_df["funnel_stage"].values]

    if existing_order:
        funnel_df["funnel_stage"] = pd.Categorical(
            funnel_df["funnel_stage"],
            categories=existing_order,
            ordered=True
        )
        funnel_df = funnel_df.sort_values("funnel_stage")

    funnel_df["previous_stage_touchpoints"] = funnel_df["touchpoints"].shift(1)
    funnel_df["dropoff_count"] = funnel_df["previous_stage_touchpoints"] - funnel_df["touchpoints"]
    funnel_df["dropoff_rate_percent"] = (
        funnel_df["dropoff_count"] / funnel_df["previous_stage_touchpoints"] * 100
    )

    funnel_df["dropoff_count"] = funnel_df["dropoff_count"].fillna(0)
    funnel_df["dropoff_rate_percent"] = funnel_df["dropoff_rate_percent"].fillna(0)

    funnel_chart = px.funnel(
        funnel_df,
        x="touchpoints",
        y="funnel_stage",
        title="Conversion Funnel"
    )

    funnel_chart.update_layout(height=420)
    st.plotly_chart(funnel_chart, use_container_width=True)

    display_funnel = funnel_df.copy()
    display_funnel["dropoff_rate_percent"] = display_funnel["dropoff_rate_percent"].round(2)

    st.subheader("Funnel Drop-off Table")
    st.dataframe(
        display_funnel[
            ["funnel_stage", "touchpoints", "dropoff_count", "dropoff_rate_percent"]
        ],
        use_container_width=True
    )

else:
    st.info("Funnel analysis requires funnel_stage and event_id columns in the cleaned dataset.")

st.divider()

# ------------------------------------------------------------
# Campaign-level Drilldown
# ------------------------------------------------------------
st.header("4. Campaign-Level Drilldown")

if attribution_df is not None and {"attribution_model", "channel", "campaign", "attributed_conversions", "attributed_revenue"}.issubset(attribution_df.columns):

    campaign_attr = attribution_df[
        (attribution_df["attribution_model"] == selected_model)
        & (attribution_df["channel"].isin(selected_channels))
    ].copy()

    campaign_summary = (
        campaign_attr.groupby(["channel", "campaign"])
        .agg(
            attributed_conversions=("attributed_conversions", "sum"),
            attributed_revenue=("attributed_revenue", "sum")
        )
        .reset_index()
    )

    if {"channel", "campaign", "ad_spend"}.issubset(cleaned_df.columns):
        campaign_spend = (
            cleaned_df.groupby(["channel", "campaign"])
            .agg(total_spend=("ad_spend", "sum"))
            .reset_index()
        )

        campaign_summary = campaign_summary.merge(
            campaign_spend,
            on=["channel", "campaign"],
            how="left"
        )
    else:
        campaign_summary["total_spend"] = 0

    campaign_summary["total_spend"] = campaign_summary["total_spend"].fillna(0)

    campaign_summary["roas"] = np.where(
        campaign_summary["total_spend"] == 0,
        0,
        campaign_summary["attributed_revenue"] / campaign_summary["total_spend"]
    )

    campaign_summary["cac"] = np.where(
        campaign_summary["attributed_conversions"] == 0,
        0,
        campaign_summary["total_spend"] / campaign_summary["attributed_conversions"]
    )

    selected_campaign_channels = st.multiselect(
        "Filter campaign table by channel",
        sorted(campaign_summary["channel"].dropna().unique()),
        default=sorted(campaign_summary["channel"].dropna().unique())
    )

    campaign_summary_filtered = campaign_summary[
        campaign_summary["channel"].isin(selected_campaign_channels)
    ].copy()

    top_campaigns = campaign_summary_filtered.sort_values(
        "attributed_revenue",
        ascending=False
    ).head(15)

    campaign_chart = px.bar(
        top_campaigns.sort_values("attributed_revenue", ascending=True),
        x="attributed_revenue",
        y="campaign",
        color="channel",
        orientation="h",
        title=f"Top Campaigns by Attributed Revenue - {selected_model}"
    )

    campaign_chart.update_layout(
        height=550,
        xaxis_title="Attributed Revenue",
        yaxis_title="Campaign"
    )

    st.plotly_chart(campaign_chart, use_container_width=True)

    st.subheader("Campaign Performance Table")

    table_cols = [
        "channel",
        "campaign",
        "attributed_conversions",
        "attributed_revenue",
        "total_spend",
        "roas",
        "cac"
    ]

    campaign_table = campaign_summary_filtered[table_cols].copy()

    for col in ["attributed_conversions", "attributed_revenue", "total_spend", "roas", "cac"]:
        campaign_table[col] = campaign_table[col].round(2)

    st.dataframe(
        campaign_table.sort_values("attributed_revenue", ascending=False),
        use_container_width=True
    )

else:
    st.info(
        "Campaign-level drilldown requires data/attribution_model_output.csv. "
        "Please upload that file to the data folder."
    )

st.divider()

# ------------------------------------------------------------
# Channel summary table
# ------------------------------------------------------------
st.header("5. Attribution Channel Summary Table")

summary_table = filtered_df.copy()

for column in ["attributed_conversions", "attributed_revenue", "total_spend", "roas", "cac"]:
    if column in summary_table.columns:
        summary_table[column] = summary_table[column].round(2)

st.dataframe(summary_table, use_container_width=True)

# ------------------------------------------------------------
# Business Insights
# ------------------------------------------------------------
st.header("6. Executive Business Insights")

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

    These insights help marketing managers compare channels, reduce wasted ad spend,
    and make better budget allocation decisions.
    """
)

st.success(
    "Dashboard upgraded successfully with ROI scatter plot, funnel drop-off analysis, and campaign-level drilldown."
)

st.caption(
    "Created by Chaitanya Pawar | Data Analytics Internship Project | Infotact Solutions & Co."
)
