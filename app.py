import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Touch Attribution ROI Dashboard",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------------------------------
# Custom CSS
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
    .metric-card {
        background-color: white;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        border-left: 5px solid #2563eb;
    }
    h1, h2, h3 {
        color: #0f172a;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# Load Data
# ------------------------------------------------------------
@st.cache_data
def load_data():
    summary_path = Path("data/attribution_channel_summary.csv")
    cleaned_path = Path("data/cleaned_multi_touch_attribution_dataset.csv")

    if not summary_path.exists():
        st.error("Missing file: data/attribution_channel_summary.csv")
        st.stop()

    if not cleaned_path.exists():
        st.error("Missing file: data/cleaned_multi_touch_attribution_dataset.csv")
        st.stop()

    summary_df = pd.read_csv(summary_path)
    cleaned_df = pd.read_csv(cleaned_path)

    if "event_timestamp_utc" in cleaned_df.columns:
        cleaned_df["event_timestamp_utc"] = pd.to_datetime(
            cleaned_df["event_timestamp_utc"], errors="coerce"
        )

    return summary_df, cleaned_df


summary_df, cleaned_df = load_data()

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.title("📊 Multi-Touch Marketing Attribution & ROI Dashboard")
st.markdown(
    """
    This Streamlit dashboard analyzes how marketing channels contribute to conversions and revenue using
    **First-Touch**, **Last-Touch**, and **Linear Attribution** models.
    """
)

# ------------------------------------------------------------
# Sidebar Filters
# ------------------------------------------------------------
st.sidebar.header("Dashboard Filters")

available_models = sorted(summary_df["attribution_model"].dropna().unique())
selected_model = st.sidebar.radio(
    "Select Attribution Model",
    available_models,
    index=available_models.index("Linear") if "Linear" in available_models else 0
)

available_channels = sorted(summary_df["channel"].dropna().unique())
selected_channels = st.sidebar.multiselect(
    "Select Channels",
    available_channels,
    default=available_channels
)

filtered_df = summary_df[
    (summary_df["attribution_model"] == selected_model)
    & (summary_df["channel"].isin(selected_channels))
].copy()

# ------------------------------------------------------------
# KPI Cards
# ------------------------------------------------------------
total_spend = filtered_df["total_spend"].sum()
total_revenue = filtered_df["attributed_revenue"].sum()
total_conversions = filtered_df["attributed_conversions"].sum()

overall_roas = total_revenue / total_spend if total_spend else 0
overall_cac = total_spend / total_conversions if total_conversions else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Spend", f"${total_spend:,.2f}")
col2.metric("Attributed Revenue", f"${total_revenue:,.2f}")
col3.metric("Attributed Conversions", f"{total_conversions:,.2f}")
col4.metric("ROAS", f"{overall_roas:,.2f}")
col5.metric("CAC", f"${overall_cac:,.2f}")

st.divider()

# ------------------------------------------------------------
# Main Charts
# ------------------------------------------------------------
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Channel Revenue")
    fig_revenue = px.bar(
        filtered_df.sort_values("attributed_revenue", ascending=True),
        x="attributed_revenue",
        y="channel",
        orientation="h",
        text="attributed_revenue",
        title=f"Attributed Revenue by Channel ({selected_model})"
    )
    fig_revenue.update_traces(texttemplate="%{text:.2s}", textposition="outside")
    fig_revenue.update_layout(height=420, xaxis_title="Attributed Revenue", yaxis_title="Channel")
    st.plotly_chart(fig_revenue, use_container_width=True)

with right_col:
    st.subheader("ROAS by Channel")
    fig_roas = px.bar(
        filtered_df.sort_values("roas", ascending=True),
        x="roas",
        y="channel",
        orientation="h",
        text="roas",
        title=f"Return on Ad Spend by Channel ({selected_model})"
    )
    fig_roas.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_roas.update_layout(height=420, xaxis_title="ROAS", yaxis_title="Channel")
    st.plotly_chart(fig_roas, use_container_width=True)

left_col2, right_col2 = st.columns(2)

with left_col2:
    st.subheader("CAC by Channel")
    fig_cac = px.bar(
        filtered_df.sort_values("cac", ascending=True),
        x="cac",
        y="channel",
        orientation="h",
        text="cac",
        title=f"Customer Acquisition Cost by Channel ({selected_model})"
    )
    fig_cac.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_cac.update_layout(height=420, xaxis_title="CAC", yaxis_title="Channel")
    st.plotly_chart(fig_cac, use_container_width=True)

with right_col2:
    st.subheader("Conversions by Channel")
    fig_conversions = px.bar(
        filtered_df.sort_values("attributed_conversions", ascending=True),
        x="attributed_conversions",
        y="channel",
        orientation="h",
        text="attributed_conversions",
        title=f"Attributed Conversions by Channel ({selected_model})"
    )
    fig_conversions.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig_conversions.update_layout(height=420, xaxis_title="Attributed Conversions", yaxis_title="Channel")
    st.plotly_chart(fig_conversions, use_container_width=True)

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
        .reindex(funnel_order)
        .dropna()
        .reset_index()
    )
    funnel_df.columns = ["funnel_stage", "touchpoints"]

    fig_funnel = px.funnel(
        funnel_df,
        x="touchpoints",
        y="funnel_stage",
        title="Funnel Stage Touchpoint Count"
    )
    st.plotly_chart(fig_funnel, use_container_width=True)
else:
    st.warning("Funnel columns not found in cleaned dataset.")

# ------------------------------------------------------------
# Data Table
# ------------------------------------------------------------
st.subheader("Attribution Channel Summary Table")

display_df = filtered_df.copy()
numeric_cols = ["attributed_conversions", "attributed_revenue", "total_spend", "roas", "cac"]
for col in numeric_cols:
    if col in display_df.columns:
        display_df[col] = display_df[col].round(2)

st.dataframe(display_df, use_container_width=True)

# ------------------------------------------------------------
# Business Insights
# ------------------------------------------------------------
st.subheader("Business Interpretation")

top_revenue_channel = (
    filtered_df.sort_values("attributed_revenue", ascending=False)["channel"].iloc[0]
    if not filtered_df.empty else "N/A"
)
top_roas_channel = (
    filtered_df.sort_values("roas", ascending=False)["channel"].iloc[0]
    if not filtered_df.empty else "N/A"
)
lowest_cac_channel = (
    filtered_df.sort_values("cac", ascending=True)["channel"].iloc[0]
    if not filtered_df.empty else "N/A"
)

st.markdown(
    f"""
    - **Top revenue channel:** `{top_revenue_channel}`
    - **Best ROAS channel:** `{top_roas_channel}`
    - **Lowest CAC channel:** `{lowest_cac_channel}`

    These insights help marketing managers identify which channels deserve more budget and which channels need optimization.
    """
)

st.info(
    "Tip: Change the attribution model in the sidebar to see how channel performance changes under First-Touch, Last-Touch, and Linear Attribution."
)
