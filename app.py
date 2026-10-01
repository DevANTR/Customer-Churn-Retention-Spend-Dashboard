"""
Customer Churn & Retention Spend Dashboard
Dark-mode Streamlit UI · SQL cohort analysis · Revenue at Risk
Made by Sai Preethi
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_analysis import build_analysis


def pd_notna(v):
    return pd.notna(v)

# ---------------------------------------------------------------------------
# Page config & global theme
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Churn & Retention Spend Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom dark CSS — high contrast, portfolio-polished
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg: #0b0f19;
        --panel: #121826;
        --panel-2: #1a2234;
        --border: #2a3548;
        --text: #e8eef9;
        --muted: #9aa8c0;
        --accent: #5b8cff;
        --accent-2: #22d3a6;
        --danger: #ff6b8a;
        --warn: #f5c542;
        --purple: #a78bfa;
    }

    .stApp {
        background: radial-gradient(1200px 600px at 10% -10%, #15203a 0%, var(--bg) 45%),
                    radial-gradient(900px 500px at 100% 0%, #1a1430 0%, transparent 50%),
                    var(--bg);
        color: var(--text);
        font-family: 'DM Sans', sans-serif;
    }

    /* Hide default Streamlit chrome noise */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1280px;
    }

    h1, h2, h3, h4 {
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif;
        letter-spacing: -0.02em;
    }

    p, li, label, span {
        color: var(--text);
    }

    .hero {
        background: linear-gradient(135deg, rgba(91,140,255,0.18), rgba(167,139,250,0.12));
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1.4rem 1.6rem 1.2rem 1.6rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.35);
    }

    .hero-title {
        font-size: 1.85rem;
        font-weight: 700;
        margin: 0 0 0.35rem 0;
        background: linear-gradient(90deg, #e8eef9, #9ec1ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-sub {
        color: var(--muted);
        font-size: 0.98rem;
        margin: 0;
        line-height: 1.45;
    }

    .badge-row {
        margin-top: 0.85rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
    }

    .badge {
        display: inline-block;
        padding: 0.28rem 0.7rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid var(--border);
        background: rgba(255,255,255,0.04);
        color: var(--text);
    }

    .badge.accent { border-color: rgba(91,140,255,0.5); color: #9ec1ff; }
    .badge.good { border-color: rgba(34,211,166,0.45); color: #7dffd1; }
    .badge.warn { border-color: rgba(245,197,66,0.45); color: #ffe08a; }
    .badge.danger { border-color: rgba(255,107,138,0.45); color: #ffb0c0; }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.85rem;
        margin: 0.4rem 0 1.1rem 0;
    }

    @media (max-width: 1100px) {
        .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    }

    .kpi-card {
        background: linear-gradient(180deg, var(--panel-2), var(--panel));
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1rem 1.05rem 0.95rem 1.05rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        min-height: 110px;
    }

    .kpi-label {
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.45rem;
    }

    .kpi-value {
        font-size: 1.55rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: var(--text);
        line-height: 1.1;
    }

    .kpi-value.accent { color: #8fb4ff; }
    .kpi-value.good { color: #5dffc4; }
    .kpi-value.warn { color: #ffd56a; }
    .kpi-value.danger { color: #ff8aa3; }

    .kpi-hint {
        margin-top: 0.4rem;
        color: var(--muted);
        font-size: 0.78rem;
    }

    .section-card {
        background: rgba(18, 24, 38, 0.92);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1rem 1.15rem 0.85rem 1.15rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 28px rgba(0,0,0,0.28);
    }

    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin: 0 0 0.25rem 0;
        color: var(--text);
    }

    .section-sub {
        color: var(--muted);
        font-size: 0.86rem;
        margin: 0 0 0.75rem 0;
    }

    .insight-box {
        background: linear-gradient(90deg, rgba(91,140,255,0.12), rgba(34,211,166,0.08));
        border-left: 3px solid var(--accent);
        border-radius: 0 12px 12px 0;
        padding: 0.85rem 1rem;
        margin: 0.6rem 0 0.2rem 0;
        color: var(--text);
        font-size: 0.92rem;
        line-height: 1.5;
    }

    .story-card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.55rem;
        color: var(--text);
        font-size: 0.9rem;
        line-height: 1.45;
    }

    .story-card strong {
        color: #ffd56a;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
    }

    .decision-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin-top: 0.5rem;
    }

    @media (max-width: 900px) {
        .decision-grid { grid-template-columns: 1fr; }
    }

    .decision-card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 0.95rem 1rem;
    }

    .decision-card h4 {
        margin: 0 0 0.4rem 0;
        font-size: 0.95rem;
        color: #9ec1ff !important;
    }

    .decision-card p {
        margin: 0;
        color: var(--muted);
        font-size: 0.86rem;
        line-height: 1.45;
    }

    .footer-bar {
        margin-top: 1.4rem;
        padding: 1rem 1.2rem;
        border-radius: 14px;
        border: 1px solid var(--border);
        background: linear-gradient(90deg, rgba(91,140,255,0.1), rgba(167,139,250,0.08));
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        color: var(--muted);
        font-size: 0.88rem;
    }

    .footer-bar .brand {
        color: var(--text);
        font-weight: 700;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #0d1320 !important;
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] * {
        color: var(--text) !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p {
        color: var(--muted) !important;
    }

    /* Dataframes */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stMetricValue"] {
        color: var(--text) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Plotly shared theme
# ---------------------------------------------------------------------------
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e8eef9", family="DM Sans"),
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#c9d4e8")),
    xaxis=dict(
        gridcolor="rgba(42,53,72,0.55)",
        zerolinecolor="rgba(42,53,72,0.55)",
        tickfont=dict(color="#9aa8c0"),
        title_font=dict(color="#c9d4e8"),
    ),
    yaxis=dict(
        gridcolor="rgba(42,53,72,0.55)",
        zerolinecolor="rgba(42,53,72,0.55)",
        tickfont=dict(color="#9aa8c0"),
        title_font=dict(color="#c9d4e8"),
    ),
)

PALETTE = ["#5b8cff", "#22d3a6", "#a78bfa", "#f5c542", "#ff6b8a", "#38bdf8"]


def style_fig(fig: go.Figure, height: int = 360) -> go.Figure:
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    return fig


def bar_churn(df, x, y, title, color_seq=None, texttemplate="%{y:.1f}%"):
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        text=y,
        color=x,
        color_discrete_sequence=color_seq or PALETTE,
    )
    fig.update_traces(
        texttemplate=texttemplate,
        textposition="outside",
        textfont=dict(color="#e8eef9", size=12),
        cliponaxis=False,
        marker_line_width=0,
    )
    fig.update_layout(showlegend=False, yaxis_title="Churn rate (%)", xaxis_title="")
    return style_fig(fig)


def bar_revenue(df, x, y, title):
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        text=y,
        color=x,
        color_discrete_sequence=PALETTE,
    )
    fig.update_traces(
        texttemplate="$%{y:,.0f}",
        textposition="outside",
        textfont=dict(color="#e8eef9", size=11),
        cliponaxis=False,
        marker_line_width=0,
    )
    fig.update_layout(showlegend=False, yaxis_title="Monthly revenue at risk ($)", xaxis_title="")
    return style_fig(fig)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_analysis():
    return build_analysis()


with st.spinner("Running SQL cohort analysis…"):
    analysis = get_analysis()

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
# Sidebar filters (optional exploration)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🎛️ Explore filters")
    st.caption("Filters refine the customer table below. KPI cards & SQL cohorts stay full-base for decision context.")
    contracts = st.multiselect(
        "Contract type",
        options=sorted(df["Contract"].unique()),
        default=sorted(df["Contract"].unique()),
    )
    internets = st.multiselect(
        "Internet service",
        options=sorted(df["InternetService"].unique()),
        default=sorted(df["InternetService"].unique()),
    )
    payments = st.multiselect(
        "Payment group",
        options=sorted(df["payment_group"].unique()),
        default=sorted(df["payment_group"].unique()),
    )
    tenure_bands = st.multiselect(
        "Tenure band",
        options=list(by_tenure["segment"].astype(str)),
        default=list(by_tenure["segment"].astype(str)),
    )
    st.markdown("---")
    st.markdown("**Formulas**")
    st.code(
        "Churn Rate = Churned ÷ Total × 100\n"
        "Revenue at Risk = Σ MonthlyCharges (churned)",
        language="text",
    )
    st.markdown("---")
    st.markdown("**Made by Sai Preethi**")
    st.caption("Data-driven retention spend decisions")

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    f"""
<div class="hero">
  <div class="hero-title">📡 Customer Churn & Retention Spend Dashboard</div>
  <p class="hero-sub">
    Telecom retention intelligence powered by SQL cohort analysis.
    Quantify where limited retention budget stops the most revenue leakage —
    contract type, early tenure danger zone, internet service, and payment method.
  </p>
  <div class="badge-row">
    <span class="badge accent">SQL cohorts</span>
    <span class="badge danger">Churn {kpis['churn_rate_pct']}%</span>
    <span class="badge warn">Revenue at risk ${kpis['revenue_at_risk']:,.0f}/mo</span>
    <span class="badge good">Made by Sai Preethi</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# KPI cards
# ---------------------------------------------------------------------------
st.markdown(
    f"""
<div class="kpi-grid">
  <div class="kpi-card">
    <div class="kpi-label">Total customers</div>
    <div class="kpi-value accent">{kpis['total_customers']:,}</div>
    <div class="kpi-hint">{kpis['retained_customers']:,} retained · {kpis['churned_customers']:,} churned</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Overall churn rate</div>
    <div class="kpi-value danger">{kpis['churn_rate_pct']}%</div>
    <div class="kpi-hint">Baseline for all retention targets</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Monthly revenue at risk</div>
    <div class="kpi-value warn">${kpis['revenue_at_risk']:,.0f}</div>
    <div class="kpi-hint">Σ monthly charges of churned customers</div>
  </div>
  <div class="kpi-card">
    <div class="kpi-label">Annual revenue at risk</div>
    <div class="kpi-value danger">${kpis['annual_revenue_at_risk']:,.0f}</div>
    <div class="kpi-hint">Avg churn bill ${kpis['avg_churn_monthly_charge']:.0f}/mo</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# Secondary KPI strip
c1, c2, c3, c4 = st.columns(4)
c1.metric("Month-to-month churn", f"{kpis['m2m_churn_pct']}%")
c2.metric("3–6 mo danger zone churn", f"{kpis['danger_zone_churn_pct']}%")
c3.metric("Electronic check churn", f"{kpis['echeck_churn_pct']}%")
c4.metric("Autopay churn", f"{kpis['autopay_churn_pct']}%")

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_overview, tab_cohorts, tab_heatmap, tab_story, tab_data = st.tabs(
    [
        "📊 Overview",
        "🧮 SQL Cohorts",
        "🔥 Cohort Heatmap",
        "📖 Storytelling & Decisions",
        "📁 Customer table",
    ]
)

with tab_overview:
    st.markdown(
        """
        <div class="section-card">
          <div class="section-title">Where does retention budget buy the most lift?</div>
          <p class="section-sub">Churn rate and revenue at risk by the four decision dimensions leadership cares about.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        fig = bar_churn(by_contract, "segment", "churn_rate_pct", "Churn rate by contract type")
        st.plotly_chart(fig, use_container_width=True)
        fig2 = bar_revenue(by_contract, "segment", "revenue_at_risk", "Revenue at risk by contract")
        st.plotly_chart(fig2, use_container_width=True)
    with col_b:
        fig = bar_churn(by_tenure, "segment", "churn_rate_pct", "Churn rate by tenure band")
        st.plotly_chart(fig, use_container_width=True)
        fig2 = bar_revenue(by_tenure, "segment", "revenue_at_risk", "Revenue at risk by tenure band")
        st.plotly_chart(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        fig = bar_churn(by_internet, "segment", "churn_rate_pct", "Churn rate by internet service")
        st.plotly_chart(fig, use_container_width=True)
    with col_d:
        fig = bar_churn(
            by_payment,
            "segment",
            "churn_rate_pct",
            "Churn rate by payment method (e-check vs autopay)",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f"""
        <div class="insight-box">
          <strong>Executive takeaway:</strong> Month-to-month contracts churn at
          <strong>{kpis['m2m_churn_pct']}%</strong>, the 3–6 month tenure band sits in a
          <strong>{kpis['danger_zone_churn_pct']}%</strong> danger zone, and electronic-check payers
          churn at <strong>{kpis['echeck_churn_pct']}%</strong> vs autopay at
          <strong>{kpis['autopay_churn_pct']}%</strong>. Combined monthly revenue at risk is
          <strong>${kpis['revenue_at_risk']:,.0f}</strong>
          (~${kpis['annual_revenue_at_risk']:,.0f}/year).
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_cohorts:
    st.markdown(
        """
        <div class="section-card">
          <div class="section-title">SQL cohort tables</div>
          <p class="section-sub">
            Metrics computed in SQLite:
            <code>Churn Rate = (Churned ÷ Total) × 100</code> ·
            <code>Revenue at Risk = Σ MonthlyCharges of churned</code>
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Contract type")
    st.dataframe(by_contract, use_container_width=True, hide_index=True)

    st.subheader("Tenure band (watch the 3–6 month danger zone)")
    st.dataframe(by_tenure, use_container_width=True, hide_index=True)

    st.subheader("Internet service")
    st.dataframe(by_internet, use_container_width=True, hide_index=True)

    st.subheader("Payment method — grouped (electronic check vs autopay)")
    st.dataframe(by_payment, use_container_width=True, hide_index=True)

    st.subheader("Payment method — detailed")
    st.dataframe(by_payment_detail, use_container_width=True, hide_index=True)

    # Side-by-side revenue charts for payment detail
    fig = bar_revenue(
        by_payment_detail,
        "segment",
        "revenue_at_risk",
        "Revenue at risk by detailed payment method",
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_heatmap:
    st.markdown(
        """
        <div class="section-card">
          <div class="section-title">Contract × tenure cohort heatmap</div>
          <p class="section-sub">Cross-segment churn rate (%) — darker / hotter cells = higher churn pressure.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    hm = heatmap.copy()
    fig = go.Figure(
        data=go.Heatmap(
            z=hm.values,
            x=list(hm.columns),
            y=list(hm.index),
            colorscale=[
                [0.0, "#0f1b2e"],
                [0.25, "#1e3a5f"],
                [0.5, "#5b8cff"],
                [0.75, "#f5c542"],
                [1.0, "#ff6b8a"],
            ],
            text=[[f"{v:.1f}%" if pd_notna(v) else "" for v in row] for row in hm.values],
            texttemplate="%{text}",
            textfont=dict(color="#e8eef9", size=12),
            colorbar=dict(title="Churn %", ticksuffix="%"),
            hovertemplate="Contract: %{y}<br>Tenure: %{x}<br>Churn: %{z:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(xaxis_title="Tenure band", yaxis_title="Contract")
    st.plotly_chart(style_fig(fig, height=420), use_container_width=True)

    st.markdown(
        """
        <div class="insight-box">
          <strong>Cohort reading:</strong> The hottest cells concentrate in
          <em>Month-to-month × early tenure</em>. Retention offers timed in months 3–6
          for month-to-month customers deliver the highest expected ROI on limited budget.
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_story:
    st.markdown(
        """
        <div class="section-card">
          <div class="section-title">Business context</div>
          <p class="section-sub">
            A telecom operator has a finite retention budget. Every dollar must target
            segments where churn probability and revenue exposure are both high.
            This dashboard turns SQL cohorts into spend decisions.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Analysis findings")
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(
            f"""
            <div class="decision-card">
              <h4>1. Month-to-month contracts</h4>
              <p>Highest churn at <strong style="color:#ff8aa3">{kpis['m2m_churn_pct']}%</strong>.
              Flexible plans convert free-look behavior into permanent loss unless upgraded.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            f"""
            <div class="decision-card">
              <h4>2. 3–6 month danger zone</h4>
              <p>Early tenure band churns at <strong style="color:#ffd56a">{kpis['danger_zone_churn_pct']}%</strong>.
              Onboarding friction + first-bill shock make this the highest-ROI save window.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            f"""
            <div class="decision-card">
              <h4>3. Electronic check vs autopay</h4>
              <p>E-check churn <strong style="color:#ff8aa3">{kpis['echeck_churn_pct']}%</strong> vs
              autopay <strong style="color:#5dffc4">{kpis['autopay_churn_pct']}%</strong>.
              Friction in payment predicts voluntary exit.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("#### Real customer stories (revenue at risk)")
    for _, row in stories.iterrows():
        st.markdown(
            f"""
            <div class="story-card">
              {row['story']}<br/>
              <span style="color:#9aa8c0;font-size:0.82rem;">
                Internet: {row['InternetService']} · Payment: {row['PaymentMethod']}
              </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Classic narrative example baked in (as required)
    example_charge = 70.0
    st.markdown(
        f"""
        <div class="insight-box">
          <strong>Storytelling example:</strong>
          Customer A churned in month 4 on a month-to-month plan with a
          <strong>${example_charge:.0f}</strong> monthly charge →
          <strong>${example_charge * 12:.0f}</strong> annual revenue at risk.
          If a $15/month contract-upgrade incentive for 6 months ($90 total)
          retains that customer, ROI is roughly <strong>{(example_charge * 12 / 90):.1f}×</strong>
          on that single save — before lifetime value.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("#### Business decisions enabled")
    st.markdown(
        """
        <div class="decision-grid">
          <div class="decision-card">
            <h4>🎯 Contract upgrade incentives</h4>
            <p>Offer month-to-month customers a discount or device credit to lock 1-year / 2-year terms —
            attack the highest-churn contract cohort directly.</p>
          </div>
          <div class="decision-card">
            <h4>⏱️ Early-tenure save plays</h4>
            <p>Concentrate outreach, tech-support white-glove, and loyalty credits on months 3–6 —
            where retention spend is most valuable per dollar.</p>
          </div>
          <div class="decision-card">
            <h4>💳 Promote autopay adoption</h4>
            <p>Incentivize electronic-check users to switch to bank/card autopay —
            lower payment friction correlates with materially lower churn.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_data:
    st.markdown(
        """
        <div class="section-card">
          <div class="section-title">Filtered customer explorer</div>
          <p class="section-sub">Use the sidebar filters to inspect individual records. Export-ready table.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    mask = (
        df["Contract"].isin(contracts)
        & df["InternetService"].isin(internets)
        & df["payment_group"].isin(payments)
        & df["tenure_band"].isin(tenure_bands)
    )
    view = df.loc[
        mask,
        [
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
        ],
    ]
    st.caption(f"Showing {len(view):,} of {len(df):,} customers")
    st.dataframe(view, use_container_width=True, hide_index=True, height=420)

    csv_bytes = view.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered CSV",
        data=csv_bytes,
        file_name="filtered_customers.csv",
        mime="text/csv",
    )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown(
    """
<div class="footer-bar">
  <div>
    <span class="brand">Made by Sai Preethi</span>
    &nbsp;·&nbsp; Customer Churn &amp; Retention Spend Dashboard
  </div>
  <div>SQL cohorts · Plotly · Streamlit · Telco Customer Churn dataset</div>
</div>
""",
    unsafe_allow_html=True,
)
