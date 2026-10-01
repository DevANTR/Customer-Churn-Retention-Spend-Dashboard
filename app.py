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

from data_analysis import TENURE_BAND_ORDER, analyze_dataframe, build_analysis

st.set_page_config(
    page_title="Churn & Retention Spend Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    :root {
        --bg: #0b0f19; --panel: #121826; --panel-2: #1a2234; --border: #2a3548;
        --text: #e8eef9; --muted: #9aa8c0; --accent: #5b8cff;
    }
    .stApp {
        background: radial-gradient(1200px 600px at 10% -10%, #15203a 0%, var(--bg) 45%),
                    radial-gradient(900px 500px at 100% 0%, #1a1430 0%, transparent 50%), var(--bg);
        color: var(--text); font-family: 'DM Sans', sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {
        background: rgba(11, 15, 25, 0.75) !important;
        backdrop-filter: blur(8px);
    }
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stBaseButton-headerNoPadding"],
    button[kind="header"], button[kind="headerNoPadding"] {
        visibility: visible !important; opacity: 1 !important;
        pointer-events: auto !important; z-index: 1000001 !important; color: #e8eef9 !important;
    }
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        display: flex !important; position: fixed !important;
        left: 0.6rem !important; top: 0.55rem !important;
        background: #1a2234 !important; border: 1px solid #5b8cff !important;
        border-radius: 10px !important; padding: 0.35rem 0.5rem !important;
        box-shadow: 0 8px 22px rgba(0,0,0,0.45) !important;
    }
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg {
        fill: #e8eef9 !important; color: #e8eef9 !important;
    }
    .block-container { padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1400px; }
    h1, h2, h3, h4 { color: var(--text) !important; font-family: 'DM Sans', sans-serif; }
    .hero {
        background: linear-gradient(135deg, rgba(91,140,255,0.18), rgba(167,139,250,0.12));
        border: 1px solid var(--border); border-radius: 18px; padding: 1.25rem 1.4rem;
        margin-bottom: 0.9rem; box-shadow: 0 10px 40px rgba(0,0,0,0.35);
    }
    .hero-title {
        font-size: 1.7rem; font-weight: 700; margin: 0 0 0.3rem 0;
        background: linear-gradient(90deg, #e8eef9, #9ec1ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero-sub { color: var(--muted); font-size: 0.95rem; margin: 0; line-height: 1.45; }
    .badge-row { margin-top: 0.75rem; display: flex; flex-wrap: wrap; gap: 0.4rem; }
    .badge {
        display: inline-block; padding: 0.25rem 0.65rem; border-radius: 999px;
        font-size: 0.74rem; font-weight: 600; border: 1px solid var(--border);
        background: rgba(255,255,255,0.04); color: var(--text);
    }
    .badge.accent { border-color: rgba(91,140,255,0.5); color: #9ec1ff; }
    .badge.good { border-color: rgba(34,211,166,0.45); color: #7dffd1; }
    .badge.warn { border-color: rgba(245,197,66,0.45); color: #ffe08a; }
    .badge.danger { border-color: rgba(255,107,138,0.45); color: #ffb0c0; }
    .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin: 0.35rem 0 0.9rem 0; }
    @media (max-width: 1100px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
    .kpi-card {
        background: linear-gradient(180deg, var(--panel-2), var(--panel));
        border: 1px solid var(--border); border-radius: 14px; padding: 0.95rem 1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25); min-height: 100px;
    }
    .kpi-label { color: var(--muted); font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem; }
    .kpi-value { font-size: 1.45rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; color: var(--text); line-height: 1.1; }
    .kpi-value.accent { color: #8fb4ff; } .kpi-value.warn { color: #ffd56a; } .kpi-value.danger { color: #ff8aa3; }
    .kpi-hint { margin-top: 0.35rem; color: var(--muted); font-size: 0.76rem; }
    .section-card { background: rgba(18,24,38,0.92); border: 1px solid var(--border); border-radius: 16px; padding: 0.95rem 1.1rem; margin-bottom: 0.85rem; }
    .section-title { font-size: 1.02rem; font-weight: 700; margin: 0 0 0.2rem 0; color: var(--text); }
    .section-sub { color: var(--muted); font-size: 0.85rem; margin: 0 0 0.55rem 0; }
    .insight-box {
        background: linear-gradient(90deg, rgba(91,140,255,0.12), rgba(34,211,166,0.08));
        border-left: 3px solid var(--accent); border-radius: 0 12px 12px 0;
        padding: 0.8rem 1rem; margin: 0.5rem 0; color: var(--text); font-size: 0.9rem; line-height: 1.5;
    }
    .story-card {
        background: var(--panel); border: 1px solid var(--border); border-radius: 12px;
        padding: 0.8rem 1rem; margin-bottom: 0.5rem; color: var(--text); font-size: 0.88rem; line-height: 1.45;
    }
    .story-card strong { color: #ffd56a; font-family: 'JetBrains Mono', monospace; font-weight: 500; }
    .decision-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.7rem; margin-top: 0.45rem; }
    @media (max-width: 900px) { .decision-grid { grid-template-columns: 1fr; } }
    .decision-card { background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 0.9rem 1rem; }
    .decision-card h4 { margin: 0 0 0.35rem 0; font-size: 0.92rem; color: #9ec1ff !important; }
    .decision-card p { margin: 0; color: var(--muted); font-size: 0.84rem; line-height: 1.45; }
    .filter-panel {
        background: rgba(18,24,38,0.96); border: 1px solid var(--border); border-radius: 16px;
        padding: 0.95rem 1rem 1rem 1rem; box-shadow: 0 8px 28px rgba(0,0,0,0.28); margin-bottom: 0.5rem;
    }
    .footer-bar {
        margin-top: 1.2rem; padding: 0.95rem 1.15rem; border-radius: 14px; border: 1px solid var(--border);
        background: linear-gradient(90deg, rgba(91,140,255,0.1), rgba(167,139,250,0.08));
        display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;
        color: var(--muted); font-size: 0.86rem;
    }
    .footer-bar .brand { color: var(--text); font-weight: 700; }
    section[data-testid="stSidebar"] { background: #0d1320 !important; border-right: 1px solid var(--border); }
    div[data-testid="stMetricValue"] { color: var(--text) !important; }
</style>
""",
    unsafe_allow_html=True,
)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#e8eef9", family="DM Sans"),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(gridcolor="rgba(42,53,72,0.55)", tickfont=dict(color="#9aa8c0")),
    yaxis=dict(gridcolor="rgba(42,53,72,0.55)", tickfont=dict(color="#9aa8c0")),
)
PALETTE = ["#5b8cff", "#22d3a6", "#a78bfa", "#f5c542", "#ff6b8a", "#38bdf8"]


def style_fig(fig: go.Figure, height: int = 360) -> go.Figure:
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    return fig


def empty_fig(title: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        title=title,
        annotations=[dict(text="No data for current filters", showarrow=False, font=dict(color="#9aa8c0"))],
    )
    return style_fig(fig)


def bar_churn(df: pd.DataFrame, title: str) -> go.Figure:
    if df is None or len(df) == 0:
        return empty_fig(title)
    fig = px.bar(
        df, x="segment", y="churn_rate_pct", title=title, text="churn_rate_pct",
        color="segment", color_discrete_sequence=PALETTE,
    )
    fig.update_traces(
        texttemplate="%{y:.1f}%", textposition="outside",
        textfont=dict(color="#e8eef9", size=12), cliponaxis=False, marker_line_width=0,
    )
    fig.update_layout(showlegend=False, yaxis_title="Churn rate (%)", xaxis_title="")
    return style_fig(fig)


def bar_revenue(df: pd.DataFrame, title: str) -> go.Figure:
    if df is None or len(df) == 0:
        return empty_fig(title)
    fig = px.bar(
        df, x="segment", y="revenue_at_risk", title=title, text="revenue_at_risk",
        color="segment", color_discrete_sequence=PALETTE,
    )
    fig.update_traces(
        texttemplate="$%{y:,.0f}", textposition="outside",
        textfont=dict(color="#e8eef9", size=11), cliponaxis=False, marker_line_width=0,
    )
    fig.update_layout(showlegend=False, yaxis_title="Monthly revenue at risk ($)", xaxis_title="")
    return style_fig(fig)


def pd_notna(v) -> bool:
    return bool(pd.notna(v))


@st.cache_data(show_spinner=False)
def get_base_data():
    return build_analysis()


with st.spinner("Loading dataset…"):
    base = get_base_data()

base_df = base["df"]
all_contracts = sorted(base_df["Contract"].dropna().unique().tolist())
all_internets = sorted(base_df["InternetService"].dropna().unique().tolist())
all_payments = sorted(base_df["payment_group"].dropna().unique().tolist())
all_tenures = [b for b in TENURE_BAND_ORDER if b in set(base_df["tenure_band"].unique())]

if "filters_open" not in st.session_state:
    st.session_state["filters_open"] = True
if "flt_contracts" not in st.session_state:
    st.session_state["flt_contracts"] = list(all_contracts)
if "flt_internets" not in st.session_state:
    st.session_state["flt_internets"] = list(all_internets)
if "flt_payments" not in st.session_state:
    st.session_state["flt_payments"] = list(all_payments)
if "flt_tenures" not in st.session_state:
    st.session_state["flt_tenures"] = list(all_tenures)


def render_filters():
    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    st.markdown("### 🎛️ Filters")
    st.caption("Changes update KPIs, charts, cohorts, heatmap, stories, and the table.")

    if st.button("↺ Reset filters", use_container_width=True, key="btn_reset"):
        st.session_state["flt_contracts"] = list(all_contracts)
        st.session_state["flt_internets"] = list(all_internets)
        st.session_state["flt_payments"] = list(all_payments)
        st.session_state["flt_tenures"] = list(all_tenures)
        st.rerun()

    contracts = st.multiselect("Contract type", options=all_contracts, key="flt_contracts")
    internets = st.multiselect("Internet service", options=all_internets, key="flt_internets")
    payments = st.multiselect("Payment group", options=all_payments, key="flt_payments")
    tenure_bands = st.multiselect("Tenure band", options=all_tenures, key="flt_tenures")

    st.markdown("**Formulas**")
    st.code(
        "Churn Rate = Churned ÷ Total × 100\nRevenue at Risk = Σ MonthlyCharges (churned)",
        language="text",
    )
    st.markdown("**Made by Sai Preethi**")
    st.markdown("</div>", unsafe_allow_html=True)
    return contracts, internets, payments, tenure_bands


# Left Streamlit chrome: help + backup open/close
with st.sidebar:
    st.markdown("### 📡 Churn Dashboard")
    st.caption("Made by Sai Preethi")
    st.markdown(
        """
**How to open / close filters**

1. Use the blue **Show filters / Hide filters** button on the main page (always works).
2. Or use the buttons below.
3. If this left chrome is collapsed, click the **>** control at the top-left edge of the screen to reopen it.
"""
    )
    if st.button("☰ Show filters panel", use_container_width=True, key="sb_show"):
        st.session_state["filters_open"] = True
        st.rerun()
    if st.button("« Hide filters panel", use_container_width=True, key="sb_hide"):
        st.session_state["filters_open"] = False
        st.rerun()

# ALWAYS-VISIBLE main toggle
t1, t2 = st.columns([1.3, 4.7])
with t1:
    label = "« Hide filters" if st.session_state["filters_open"] else "☰ Show filters"
    if st.button(label, use_container_width=True, type="primary", key="main_toggle"):
        st.session_state["filters_open"] = not st.session_state["filters_open"]
        st.rerun()
with t2:
    st.caption("This button always opens or closes the filters panel — independent of the left Streamlit sidebar.")

if st.session_state["filters_open"]:
    filter_col, dash_col = st.columns([1.15, 3.35], gap="large")
    with filter_col:
        contracts, internets, payments, tenure_bands = render_filters()
else:
    dash_col = st.container()
    contracts = list(st.session_state.get("flt_contracts", all_contracts))
    internets = list(st.session_state.get("flt_internets", all_internets))
    payments = list(st.session_state.get("flt_payments", all_payments))
    tenure_bands = list(st.session_state.get("flt_tenures", all_tenures))
    st.info("Filters panel is hidden. Click **☰ Show filters** above to open it again.")

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

filter_active = len(filtered_df) != len(base_df)
filter_note = (
    f"Showing **{len(filtered_df):,}** of **{len(base_df):,}** customers"
    + (" · filters active" if filter_active else " · full dataset")
)

with dash_col:
    st.markdown(
        f"""
<div class="hero">
  <div class="hero-title">📡 Customer Churn & Retention Spend Dashboard</div>
  <p class="hero-sub">
    Telecom retention intelligence powered by SQL cohort analysis.
    Quantify where limited retention budget stops the most revenue leakage.
  </p>
  <div class="badge-row">
    <span class="badge accent">SQL cohorts</span>
    <span class="badge danger">Churn {kpis['churn_rate_pct']}%</span>
    <span class="badge warn">Revenue at risk ${kpis['revenue_at_risk']:,.0f}/mo</span>
    <span class="badge good">Made by Sai Preethi</span>
    <span class="badge {'warn' if filter_active else 'accent'}">{'Filtered view' if filter_active else 'Full base'}</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.caption(filter_note)
    if len(filtered_df) == 0:
        st.warning("No customers match the current filters. Open filters and reset or widen selections.")

    st.markdown(
        f"""
<div class="kpi-grid">
  <div class="kpi-card"><div class="kpi-label">Total customers</div>
    <div class="kpi-value accent">{kpis['total_customers']:,}</div>
    <div class="kpi-hint">{kpis['retained_customers']:,} retained · {kpis['churned_customers']:,} churned</div></div>
  <div class="kpi-card"><div class="kpi-label">Overall churn rate</div>
    <div class="kpi-value danger">{kpis['churn_rate_pct']}%</div>
    <div class="kpi-hint">Baseline for all retention targets</div></div>
  <div class="kpi-card"><div class="kpi-label">Monthly revenue at risk</div>
    <div class="kpi-value warn">${kpis['revenue_at_risk']:,.0f}</div>
    <div class="kpi-hint">Σ monthly charges of churned customers</div></div>
  <div class="kpi-card"><div class="kpi-label">Annual revenue at risk</div>
    <div class="kpi-value danger">${kpis['annual_revenue_at_risk']:,.0f}</div>
    <div class="kpi-hint">Avg churn bill ${kpis['avg_churn_monthly_charge']:.0f}/mo</div></div>
</div>
""",
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Month-to-month churn", f"{kpis['m2m_churn_pct']}%")
    m2.metric("3–6 mo danger zone churn", f"{kpis['danger_zone_churn_pct']}%")
    m3.metric("Electronic check churn", f"{kpis['echeck_churn_pct']}%")
    m4.metric("Autopay churn", f"{kpis['autopay_churn_pct']}%")

    tab_overview, tab_cohorts, tab_heatmap, tab_story, tab_data = st.tabs(
        ["📊 Overview", "🧮 SQL Cohorts", "🔥 Cohort Heatmap", "📖 Storytelling & Decisions", "📁 Customer table"]
    )

    with tab_overview:
        st.markdown(
            """<div class="section-card"><div class="section-title">Where does retention budget buy the most lift?</div>
            <p class="section-sub">Churn rate and revenue at risk by contract, tenure, internet, and payment.</p></div>""",
            unsafe_allow_html=True,
        )
        c_a, c_b = st.columns(2)
        with c_a:
            st.plotly_chart(bar_churn(by_contract, "Churn rate by contract type"), use_container_width=True)
            st.plotly_chart(bar_revenue(by_contract, "Revenue at risk by contract"), use_container_width=True)
        with c_b:
            st.plotly_chart(bar_churn(by_tenure, "Churn rate by tenure band"), use_container_width=True)
            st.plotly_chart(bar_revenue(by_tenure, "Revenue at risk by tenure band"), use_container_width=True)
        c_c, c_d = st.columns(2)
        with c_c:
            st.plotly_chart(bar_churn(by_internet, "Churn rate by internet service"), use_container_width=True)
        with c_d:
            st.plotly_chart(bar_churn(by_payment, "Churn rate by payment method"), use_container_width=True)
        st.markdown(
            f"""<div class="insight-box"><strong>Executive takeaway:</strong> Month-to-month churn
            <strong>{kpis['m2m_churn_pct']}%</strong>, 3–6 month danger zone
            <strong>{kpis['danger_zone_churn_pct']}%</strong>, e-check
            <strong>{kpis['echeck_churn_pct']}%</strong> vs autopay
            <strong>{kpis['autopay_churn_pct']}%</strong>. Monthly revenue at risk
            <strong>${kpis['revenue_at_risk']:,.0f}</strong>
            (~${kpis['annual_revenue_at_risk']:,.0f}/year).</div>""",
            unsafe_allow_html=True,
        )

    with tab_cohorts:
        st.subheader("Contract type")
        st.dataframe(by_contract, use_container_width=True, hide_index=True)
        st.subheader("Tenure band")
        st.dataframe(by_tenure, use_container_width=True, hide_index=True)
        st.subheader("Internet service")
        st.dataframe(by_internet, use_container_width=True, hide_index=True)
        st.subheader("Payment method — grouped")
        st.dataframe(by_payment, use_container_width=True, hide_index=True)
        st.subheader("Payment method — detailed")
        st.dataframe(by_payment_detail, use_container_width=True, hide_index=True)
        st.plotly_chart(bar_revenue(by_payment_detail, "Revenue at risk by payment method"), use_container_width=True)

    with tab_heatmap:
        hm = heatmap.copy() if heatmap is not None else pd.DataFrame()
        if hm.empty:
            st.info("Heatmap unavailable for the current filter selection.")
        else:
            fig = go.Figure(
                data=go.Heatmap(
                    z=hm.values, x=list(hm.columns), y=list(hm.index),
                    colorscale=[[0, "#0f1b2e"], [0.25, "#1e3a5f"], [0.5, "#5b8cff"], [0.75, "#f5c542"], [1, "#ff6b8a"]],
                    text=[[f"{v:.1f}%" if pd_notna(v) else "" for v in row] for row in hm.values],
                    texttemplate="%{text}", textfont=dict(color="#e8eef9", size=12),
                    colorbar=dict(title="Churn %", ticksuffix="%"),
                    hovertemplate="Contract: %{y}<br>Tenure: %{x}<br>Churn: %{z:.1f}%<extra></extra>",
                )
            )
            fig.update_layout(xaxis_title="Tenure band", yaxis_title="Contract")
            st.plotly_chart(style_fig(fig, height=420), use_container_width=True)

    with tab_story:
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown(
                f"""<div class="decision-card"><h4>1. Month-to-month</h4>
                <p>Churn <strong style="color:#ff8aa3">{kpis['m2m_churn_pct']}%</strong>.</p></div>""",
                unsafe_allow_html=True,
            )
        with f2:
            st.markdown(
                f"""<div class="decision-card"><h4>2. 3–6 month danger zone</h4>
                <p>Churn <strong style="color:#ffd56a">{kpis['danger_zone_churn_pct']}%</strong>.</p></div>""",
                unsafe_allow_html=True,
            )
        with f3:
            st.markdown(
                f"""<div class="decision-card"><h4>3. E-check vs autopay</h4>
                <p>E-check <strong style="color:#ff8aa3">{kpis['echeck_churn_pct']}%</strong> vs
                autopay <strong style="color:#5dffc4">{kpis['autopay_churn_pct']}%</strong>.</p></div>""",
                unsafe_allow_html=True,
            )
        st.markdown("#### Real customer stories")
        if stories is None or len(stories) == 0:
            st.info("No churned-customer stories for the current filters.")
        else:
            for _, row in stories.iterrows():
                st.markdown(
                    f"""<div class="story-card">{row['story']}<br/>
                    <span style="color:#9aa8c0;font-size:0.82rem;">Internet: {row['InternetService']} · Payment: {row['PaymentMethod']}</span></div>""",
                    unsafe_allow_html=True,
                )
        st.markdown(
            """<div class="insight-box"><strong>Example:</strong> Customer A churned in month 4 at
            <strong>$70</strong>/mo → <strong>$840</strong> annual risk. A $90 save offer ≈ <strong>9.3×</strong> ROI.</div>""",
            unsafe_allow_html=True,
        )
        st.markdown(
            """<div class="decision-grid">
              <div class="decision-card"><h4>🎯 Contract upgrades</h4><p>Move month-to-month to 1/2-year terms.</p></div>
              <div class="decision-card"><h4>⏱️ Early-tenure saves</h4><p>Focus spend on months 3–6.</p></div>
              <div class="decision-card"><h4>💳 Autopay adoption</h4><p>Migrate e-check users to autopay.</p></div>
            </div>""",
            unsafe_allow_html=True,
        )

    with tab_data:
        cols = [c for c in [
            "customerID", "gender", "tenure", "tenure_band", "Contract", "InternetService",
            "PaymentMethod", "payment_group", "MonthlyCharges", "TotalCharges", "Churn", "AnnualRisk",
        ] if c in df.columns]
        view = df.loc[:, cols] if len(df) and cols else pd.DataFrame(columns=cols)
        st.caption(f"Showing {len(view):,} of {len(base_df):,} customers (after filters)")
        st.dataframe(view, use_container_width=True, hide_index=True, height=420)
        st.download_button(
            "⬇️ Download filtered CSV",
            data=view.to_csv(index=False).encode("utf-8"),
            file_name="filtered_customers.csv",
            mime="text/csv",
            disabled=len(view) == 0,
        )

st.markdown(
    """
<div class="footer-bar">
  <div><span class="brand">Made by Sai Preethi</span> · Customer Churn &amp; Retention Spend Dashboard</div>
  <div>SQL cohorts · Plotly · Streamlit · Telco Customer Churn dataset</div>
</div>
""",
    unsafe_allow_html=True,
)
