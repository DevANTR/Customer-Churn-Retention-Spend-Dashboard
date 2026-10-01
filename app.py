"""
Customer Churn & Retention Spend Dashboard
Simple dark-theme Streamlit UI · SQL cohort analysis
Made by Sai Preethi
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_analysis import TENURE_BAND_ORDER, analyze_dataframe, build_analysis

st.set_page_config(
    page_title="Churn & Retention Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Simple dark theme only
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] * {
        color: #e6edf3;
    }
    h1, h2, h3, h4 {
        color: #f0f6fc !important;
    }
    .stMarkdown, p, label, span {
        color: #c9d1d9;
    }
    div[data-testid="stMetricValue"] {
        color: #f0f6fc !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #8b949e !important;
    }
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        color: #f0f6fc !important;
    }
    hr {
        border-color: #30363d;
    }
</style>
""",
    unsafe_allow_html=True,
)

DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#c9d1d9", size=12),
    margin=dict(l=40, r=20, t=50, b=40),
    xaxis=dict(gridcolor="#21262d", zerolinecolor="#21262d", color="#8b949e"),
    yaxis=dict(gridcolor="#21262d", zerolinecolor="#21262d", color="#8b949e"),
    title=dict(font=dict(color="#f0f6fc", size=14)),
)
COLORS = ["#58a6ff", "#3fb950", "#d2a8ff", "#e3b341", "#f85149", "#79c0ff"]


def style_fig(fig: go.Figure, height: int = 340) -> go.Figure:
    fig.update_layout(**DARK_LAYOUT, height=height, showlegend=False)
    return fig


def empty_fig(title: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        title=title,
        annotations=[dict(text="No data for current filters", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="#8b949e"))],
    )
    return style_fig(fig)


def bar_churn(df: pd.DataFrame, title: str) -> go.Figure:
    if df is None or len(df) == 0:
        return empty_fig(title)
    fig = px.bar(
        df,
        x="segment",
        y="churn_rate_pct",
        title=title,
        text="churn_rate_pct",
        color="segment",
        color_discrete_sequence=COLORS,
    )
    fig.update_traces(texttemplate="%{y:.1f}%", textposition="outside", cliponaxis=False, marker_line_width=0)
    fig.update_layout(yaxis_title="Churn %", xaxis_title="")
    return style_fig(fig)


def bar_revenue(df: pd.DataFrame, title: str) -> go.Figure:
    if df is None or len(df) == 0:
        return empty_fig(title)
    fig = px.bar(
        df,
        x="segment",
        y="revenue_at_risk",
        title=title,
        text="revenue_at_risk",
        color="segment",
        color_discrete_sequence=COLORS,
    )
    fig.update_traces(texttemplate="$%{y:,.0f}", textposition="outside", cliponaxis=False, marker_line_width=0)
    fig.update_layout(yaxis_title="Revenue at risk ($)", xaxis_title="")
    return style_fig(fig)


def pd_notna(v) -> bool:
    return bool(pd.notna(v))


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_base():
    return build_analysis()


base = load_base()
base_df = base["df"]
all_contracts = sorted(base_df["Contract"].dropna().unique().tolist())
all_internets = sorted(base_df["InternetService"].dropna().unique().tolist())
all_payments = sorted(base_df["payment_group"].dropna().unique().tolist())
all_tenures = [b for b in TENURE_BAND_ORDER if b in set(base_df["tenure_band"].unique())]

# Session defaults
for key, default in {
    "flt_contracts": all_contracts,
    "flt_internets": all_internets,
    "flt_payments": all_payments,
    "flt_tenures": all_tenures,
}.items():
    if key not in st.session_state:
        st.session_state[key] = list(default)

# ---------------------------------------------------------------------------
# Sidebar filters (simple)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.title("Filters")
    st.caption("Made by Sai Preethi")

    if st.button("Reset filters", use_container_width=True):
        st.session_state["flt_contracts"] = list(all_contracts)
        st.session_state["flt_internets"] = list(all_internets)
        st.session_state["flt_payments"] = list(all_payments)
        st.session_state["flt_tenures"] = list(all_tenures)
        st.rerun()

    contracts = st.multiselect("Contract", options=all_contracts, key="flt_contracts")
    internets = st.multiselect("Internet service", options=all_internets, key="flt_internets")
    payments = st.multiselect("Payment group", options=all_payments, key="flt_payments")
    tenure_bands = st.multiselect("Tenure band", options=all_tenures, key="flt_tenures")

    st.divider()
    st.markdown("**Formulas**")
    st.code("Churn % = Churned / Total × 100\nRisk $ = Σ MonthlyCharges (churned)")
    st.caption("Close/open this sidebar with the arrow at the top-left.")

# Apply filters
mask = (
    base_df["Contract"].isin(contracts or [])
    & base_df["InternetService"].isin(internets or [])
    & base_df["payment_group"].isin(payments or [])
    & base_df["tenure_band"].isin(tenure_bands or [])
)
filtered_df = base_df.loc[mask].copy()
analysis = analyze_dataframe(filtered_df)

kpis = analysis["kpis"]
by_contract = analysis["by_contract"]
by_tenure = analysis["by_tenure"]
by_internet = analysis["by_internet"]
by_payment = analysis["by_payment"]
by_payment_detail = analysis["by_payment_detail"]
heatmap = analysis["heatmap"]
stories = analysis["stories"]
df = analysis["df"]

# ---------------------------------------------------------------------------
# Main page
# ---------------------------------------------------------------------------
st.title("Customer Churn & Retention Spend")
st.caption(
    f"Made by Sai Preethi  ·  Showing {len(filtered_df):,} of {len(base_df):,} customers"
    + ("  ·  filters active" if len(filtered_df) != len(base_df) else "")
)

if len(filtered_df) == 0:
    st.warning("No customers match the current filters. Reset or widen selections in the sidebar.")

# KPI row
k1, k2, k3, k4 = st.columns(4)
k1.metric("Customers", f"{kpis['total_customers']:,}", f"{kpis['churned_customers']:,} churned")
k2.metric("Churn rate", f"{kpis['churn_rate_pct']}%")
k3.metric("Revenue at risk / mo", f"${kpis['revenue_at_risk']:,.0f}")
k4.metric("Revenue at risk / yr", f"${kpis['annual_revenue_at_risk']:,.0f}")

s1, s2, s3, s4 = st.columns(4)
s1.metric("Month-to-month churn", f"{kpis['m2m_churn_pct']}%")
s2.metric("3–6 mo danger zone", f"{kpis['danger_zone_churn_pct']}%")
s3.metric("Electronic check churn", f"{kpis['echeck_churn_pct']}%")
s4.metric("Autopay churn", f"{kpis['autopay_churn_pct']}%")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "SQL Cohorts", "Heatmap", "Story & Decisions", "Customers"]
)

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(bar_churn(by_contract, "Churn rate by contract"), use_container_width=True)
        st.plotly_chart(bar_revenue(by_contract, "Revenue at risk by contract"), use_container_width=True)
    with c2:
        st.plotly_chart(bar_churn(by_tenure, "Churn rate by tenure band"), use_container_width=True)
        st.plotly_chart(bar_revenue(by_tenure, "Revenue at risk by tenure band"), use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(bar_churn(by_internet, "Churn rate by internet service"), use_container_width=True)
    with c4:
        st.plotly_chart(bar_churn(by_payment, "Churn rate by payment group"), use_container_width=True)

    st.info(
        f"**Takeaway:** Month-to-month churn is **{kpis['m2m_churn_pct']}%**, "
        f"3–6 month danger zone is **{kpis['danger_zone_churn_pct']}%**, "
        f"electronic check is **{kpis['echeck_churn_pct']}%** vs autopay **{kpis['autopay_churn_pct']}%**. "
        f"Monthly revenue at risk: **${kpis['revenue_at_risk']:,.0f}** "
        f"(~${kpis['annual_revenue_at_risk']:,.0f}/year)."
    )

with tab2:
    st.markdown("SQL cohort metrics: `Churn % = Churned ÷ Total × 100` · `Revenue at Risk = Σ MonthlyCharges of churned`")
    st.subheader("Contract")
    st.dataframe(by_contract, use_container_width=True, hide_index=True)
    st.subheader("Tenure band")
    st.dataframe(by_tenure, use_container_width=True, hide_index=True)
    st.subheader("Internet service")
    st.dataframe(by_internet, use_container_width=True, hide_index=True)
    st.subheader("Payment group")
    st.dataframe(by_payment, use_container_width=True, hide_index=True)
    st.subheader("Payment method (detail)")
    st.dataframe(by_payment_detail, use_container_width=True, hide_index=True)
    st.plotly_chart(bar_revenue(by_payment_detail, "Revenue at risk by payment method"), use_container_width=True)

with tab3:
    st.subheader("Contract × tenure churn heatmap")
    hm = heatmap.copy() if heatmap is not None else pd.DataFrame()
    if hm.empty:
        st.info("No heatmap data for current filters.")
    else:
        fig = go.Figure(
            data=go.Heatmap(
                z=hm.values,
                x=list(hm.columns),
                y=list(hm.index),
                colorscale="Blues",
                text=[[f"{v:.1f}%" if pd_notna(v) else "" for v in row] for row in hm.values],
                texttemplate="%{text}",
                textfont=dict(color="#f0f6fc", size=12),
                colorbar=dict(title="Churn %"),
                hovertemplate="Contract: %{y}<br>Tenure: %{x}<br>Churn: %{z:.1f}%<extra></extra>",
            )
        )
        fig.update_layout(xaxis_title="Tenure band", yaxis_title="Contract")
        st.plotly_chart(style_fig(fig, height=400), use_container_width=True)
        st.caption("Hotter cells = higher churn. Focus retention on month-to-month × early tenure.")

with tab4:
    st.subheader("Findings")
    col_a, col_b, col_c = st.columns(3)
    col_a.write(f"**Month-to-month** contracts churn highest at **{kpis['m2m_churn_pct']}%**.")
    col_b.write(f"**3–6 month** tenure is a danger zone at **{kpis['danger_zone_churn_pct']}%**.")
    col_c.write(f"**Electronic check** churns at **{kpis['echeck_churn_pct']}%** vs autopay **{kpis['autopay_churn_pct']}%**.")

    st.subheader("Customer examples")
    if stories is None or len(stories) == 0:
        st.info("No churned-customer examples for current filters.")
    else:
        for _, row in stories.iterrows():
            st.write(f"- {row['story']}")

    st.subheader("Story example")
    st.write(
        "Customer A churned in month 4 with a **$70** monthly charge → **$840** annual revenue at risk. "
        "A $90 contract-upgrade incentive that saves them is roughly **9×** ROI on that account."
    )

    st.subheader("Decisions enabled")
    st.markdown(
        """
1. **Contract upgrade incentives** for month-to-month customers  
2. **Focus retention spend** on early tenure (especially 3–6 months)  
3. **Promote autopay** among electronic-check users  
"""
    )

with tab5:
    cols = [
        c
        for c in [
            "customerID",
            "gender",
            "tenure",
            "tenure_band",
            "Contract",
            "InternetService",
            "PaymentMethod",
            "payment_group",
            "MonthlyCharges",
            "TotalCharges",
            "Churn",
            "AnnualRisk",
        ]
        if c in df.columns
    ]
    view = df.loc[:, cols] if len(df) and cols else pd.DataFrame(columns=cols)
    st.caption(f"{len(view):,} rows")
    st.dataframe(view, use_container_width=True, hide_index=True, height=420)
    st.download_button(
        "Download filtered CSV",
        data=view.to_csv(index=False).encode("utf-8"),
        file_name="filtered_customers.csv",
        mime="text/csv",
        disabled=len(view) == 0,
    )

st.divider()
st.caption("Made by Sai Preethi · SQL cohorts · Pandas · Plotly · Streamlit")
