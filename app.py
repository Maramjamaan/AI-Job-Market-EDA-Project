import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Job Market Dashboard · Maram Alzahrani",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =======================================================================
# THEME — one clean light palette, indigo accent, Untitled-UI-style
# colorway. Color still encodes data lineage: indigo = real / observed
# data, amber = projected.
# =======================================================================
THEME = {
    "bg": "#0D0F17",
    "surface": "#161925",
    "surface_2": "#1E2233",
    "border": "#2B3044",
    "text": "#F2F4F8",
    "subtext": "#9AA1B5",
    "accent": "#818CF8",        # indigo — real / observed data
    "accent2": "#FDB022",       # amber — extrapolated / projected data
    "accent_soft": "rgba(129,140,248,0.15)",
    "plotly_template": "plotly_dark",
}
COLORWAY = ["#818CF8", "#38BDF8", "#FDB022", "#34D399", "#F472B6", "#9AA1B5"]
HEATMAP_SCALE = [[0, THEME["surface_2"]], [1, THEME["accent"]]]
T = THEME  # short alias used throughout


def inject_css(t):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {t['text']} !important;
    }}
    .stApp {{ background: {t['bg']}; }}
    #MainMenu, footer {{ visibility: hidden; }}
    header[data-testid="stHeader"] {{ background: transparent !important; }}
    [data-testid="stDecoration"] {{ display: none !important; }}
    div.block-container {{ padding-top: 1.6rem; max-width: 1220px; }}

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {{
        background: {t['surface']};
        border-right: 1px solid {t['border']};
    }}
    section[data-testid="stSidebar"] .block-container {{ padding-top: 1.4rem; }}

    /* Sidebar page nav */
    div[data-testid="stRadio"] > label {{ display: none; }}
    div[data-testid="stRadio"] > div {{ gap: 2px; }}
    div[data-testid="stRadio"] label {{
        padding: 8px 10px;
        border-radius: 8px;
        width: 100%;
    }}
    div[data-testid="stRadio"] label p {{
        font-size: 0.92rem !important;
        font-weight: 500 !important;
    }}
    div[data-testid="stRadio"] label:hover {{ background: {t['surface_2']}; }}

    /* ---------- Hero ---------- */
    .eyebrow {{
        color: {t['accent']};
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }}
    .hero-title {{
        font-weight: 700;
        font-size: 1.6rem;
        color: {t['text']};
        margin: 0 0 2px 0;
    }}
    .hero-sub {{
        color: {t['subtext']};
        font-size: 0.95rem;
        margin-bottom: 18px;
    }}
    .link-pill {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 7px 15px;
        border-radius: 999px;
        background: {t['surface']};
        border: 1px solid {t['border']};
        color: {t['text']};
        font-size: 0.82rem;
        font-weight: 600;
        text-decoration: none;
        margin-right: 8px;
        margin-bottom: 8px;
        transition: border-color 0.15s, color 0.15s, background 0.15s;
    }}
    .link-pill:hover {{ border-color: {t['accent']}; color: {t['accent']}; background: {t['accent_soft']}; }}

    /* ---------- Data-lineage badges (Real vs Projected) ---------- */
    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 11px;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin-right: 8px;
    }}
    .badge .dot {{ width: 6px; height: 6px; border-radius: 50%; }}
    .badge-real {{ background: rgba(79,70,229,0.10); color: {t['accent']}; border: 1px solid rgba(79,70,229,0.28); }}
    .badge-real .dot {{ background: {t['accent']}; }}
    .badge-proj {{ background: rgba(247,144,9,0.10); color: {t['accent2']}; border: 1px solid rgba(247,144,9,0.32); }}
    .badge-proj .dot {{ background: {t['accent2']}; }}

    /* ---------- Section headers above chart groups ---------- */
    .section-head {{ margin: 6px 0 14px 0; }}
    .section-head .eyebrow {{ margin-bottom: 2px; }}
    .section-head .section-title {{
        font-weight: 600;
        font-size: 1.05rem;
        color: {t['text']};
    }}
    .page-title {{
        font-weight: 700;
        font-size: 1.3rem;
        color: {t['text']};
        margin: 4px 0 2px 0;
    }}
    .page-sub {{ color: {t['subtext']}; font-size: 0.9rem; margin-bottom: 16px; }}

    /* ---------- Metric / KPI cards ---------- */
    div[data-testid="stMetric"] {{
        background: {t['surface']};
        border: 1px solid {t['border']};
        border-radius: 12px;
        padding: 14px 18px;
        box-shadow: 0 1px 2px rgba(16,24,40,0.04);
    }}
    div[data-testid="stMetricLabel"] {{
        color: {t['subtext']} !important;
        font-size: 0.82rem !important;
    }}
    div[data-testid="stMetricValue"] {{
        color: {t['text']} !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
        white-space: normal !important;
        overflow-wrap: break-word !important;
        line-height: 1.25 !important;
    }}

    /* ---------- Native bordered containers used as cards ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-radius: 14px !important;
        border-color: {t['border']} !important;
        background: {t['surface']};
    }}

    /* ---------- Insight callouts ---------- */
    .mini-insight {{
        color: {t['subtext']};
        font-size: 0.9rem;
        border-left: 2px solid {t['accent']};
        padding-left: 10px;
        margin: 10px 0 4px 0;
    }}

    /* ---------- Grouped insight bullet list ---------- */
    .insight-group-title {{
        font-weight: 600;
        font-size: 0.95rem;
        color: {t['text']};
        margin: 22px 0 10px 0;
    }}
    .insight-group-title:first-child {{ margin-top: 0; }}
    ul.insight-list {{
        list-style: none;
        padding-left: 0;
        margin: 0 0 4px 0;
    }}
    ul.insight-list li {{
        position: relative;
        padding-left: 22px;
        margin-bottom: 13px;
        line-height: 1.6;
        color: {t['text']};
    }}
    ul.insight-list li::before {{
        content: "";
        position: absolute;
        left: 2px;
        top: 8px;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: {t['accent']};
    }}
    ul.insight-list li strong {{ color: {t['text']}; }}
    ul.insight-list li span.detail {{ color: {t['subtext']}; }}

    /* ---------- Footer ---------- */
    .footer-name {{ font-weight: 700; color: {t['text']}; font-size: 0.98rem; }}
    .footer-role {{ color: {t['subtext']}; font-size: 0.85rem; margin-bottom: 10px; }}
    .stack-line {{ color: {t['subtext']}; font-size: 0.8rem; }}
    hr {{ border-color: {t['border']}; }}

    /* ---------- Keep native widgets on-brand regardless of host theme ---------- */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] strong,
    [data-testid="stWidgetLabel"] p,
    label p {{
        color: {t['text']} !important;
    }}
    [data-testid="stCaptionContainer"] p {{ color: {t['subtext']} !important; }}
    [data-testid="stDataFrame"] {{ background: {t['surface']} !important; }}

    [data-baseweb="select"] > div {{
        background: {t['surface']} !important;
        border-color: {t['border']} !important;
    }}
    [data-baseweb="tag"] {{
        background: {t['accent_soft']} !important;
        border: 1px solid rgba(79,70,229,0.35) !important;
    }}
    [data-baseweb="tag"] span {{ color: {t['text']} !important; }}
    [data-baseweb="tag"] svg {{ fill: {t['text']} !important; }}

    div[data-testid="stSlider"] div[role="slider"] {{
        background-color: {t['accent']} !important;
        border-color: {t['accent']} !important;
    }}
    div[data-testid="stSlider"] > div > div > div > div {{
        background-color: {t['accent']} !important;
    }}
    /* value bubble shown above each slider thumb — no filled box, just text */
    div[data-testid="stSlider"] [data-testid="stThumbValue"] {{
        background: transparent !important;
        color: {t['text']} !important;
        box-shadow: none !important;
        font-weight: 600 !important;
    }}
    /* min/max tick labels at the ends of the slider track */
    div[data-testid="stSlider"] [data-testid="stTickBarMin"],
    div[data-testid="stSlider"] [data-testid="stTickBarMax"] {{
        color: {t['subtext']} !important;
        background: transparent !important;
    }}
    </style>
    """, unsafe_allow_html=True)


def style_fig(fig, t, height=380):
    """Apply the shared theme + colorway to a Plotly figure."""
    fig.update_layout(
        template=t["plotly_template"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=t["text"], size=12),
        title_font=dict(size=14, color=t["text"]),
        colorway=COLORWAY,
        margin=dict(l=10, r=10, t=45, b=10),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=t["border"], zerolinecolor=t["border"])
    fig.update_yaxes(gridcolor=t["border"], zerolinecolor=t["border"])
    return fig


def mini_insight(text):
    st.markdown(f'<div class="mini-insight">{text}</div>', unsafe_allow_html=True)


def section_head(eyebrow_text, title_text):
    st.markdown(
        f'<div class="section-head"><div class="eyebrow">{eyebrow_text}</div>'
        f'<div class="section-title">{title_text}</div></div>',
        unsafe_allow_html=True,
    )


def page_head(title_text, sub_text):
    st.markdown(
        f'<div class="page-title">{title_text}</div><div class="page-sub">{sub_text}</div>',
        unsafe_allow_html=True,
    )


def lineage_legend():
    st.markdown(
        '<span class="badge badge-real"><span class="dot"></span>REAL DATA · 2020–2023</span>'
        '<span class="badge badge-proj"><span class="dot"></span>PROJECTED · 2024–2026</span>',
        unsafe_allow_html=True,
    )


def insight_group(title, items):
    """Render a titled group of bullet takeaways: each item is (headline, detail)."""
    st.markdown(f'<div class="insight-group-title">{title}</div>', unsafe_allow_html=True)
    rows = "".join(
        f'<li><strong>{headline}</strong> — <span class="detail">{detail}</span></li>'
        for headline, detail in items
    )
    st.markdown(f'<ul class="insight-list">{rows}</ul>', unsafe_allow_html=True)


inject_css(T)

# =======================================================================
# DATA
# =======================================================================
@st.cache_data
def load_data():
    df = pd.read_csv("ai_job_market_salary_global_2020_2026_clean.csv")
    df["posting_date"] = pd.to_datetime(df["posting_date"])
    return df


df = load_data()

# =======================================================================
# SIDEBAR — identity, page navigation, filters
# =======================================================================
with st.sidebar:
    st.markdown('<div class="eyebrow">Maram Alzahrani</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="font-weight:700; font-size:1.05rem; margin-bottom:16px; color:{T["text"]};">'
        'AI Job Market Dashboard</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="eyebrow">Navigate</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigate", ["Overview", "Deep Dive", "Insights"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("##### About this dataset")
    st.write(f"**{len(df):,}** AI/data job postings collected globally, 2020–2026.")
    lineage_legend()
    st.caption("Projected years follow the shape of the real trend rather than a random jump — see Deep Dive.")

    st.markdown("---")
    st.markdown("##### Filters")

    year_min, year_max = int(df["work_year"].min()), int(df["work_year"].max())
    year_range = st.sidebar.slider("Year range", year_min, year_max, (year_min, year_max))

    exp_levels = st.sidebar.multiselect(
        "Experience level", sorted(df["experience_level"].unique()),
        default=sorted(df["experience_level"].unique())
    )
    regions = st.sidebar.multiselect(
        "Region", sorted(df["region"].unique()),
        default=sorted(df["region"].unique())
    )
    remote_types = st.sidebar.multiselect(
        "Work type", sorted(df["remote_type"].unique()),
        default=sorted(df["remote_type"].unique())
    )
    data_note_options = st.sidebar.multiselect(
        "Data type", sorted(df["data_note"].unique()),
        default=sorted(df["data_note"].unique())
    )

    filtered_df = df[
        (df["work_year"].between(*year_range)) &
        (df["experience_level"].isin(exp_levels)) &
        (df["region"].isin(regions)) &
        (df["remote_type"].isin(remote_types)) &
        (df["data_note"].isin(data_note_options))
    ]

    st.markdown("---")
    st.caption(f"**{len(filtered_df):,}** of {len(df):,} postings match your filters")

    st.markdown("---")
    st.markdown(
        '<a class="link-pill" href="https://github.com/Maramjamaan/AI-Job-Market-EDA-Project" target="_blank">GitHub ↗</a>'
        '<a class="link-pill" href="https://www.linkedin.com/in/maram-alzahrani314/" target="_blank">LinkedIn ↗</a>',
        unsafe_allow_html=True,
    )

if filtered_df.empty:
    st.warning("No postings match the current filters — try widening your selection.")
    st.stop()

# =======================================================================
# HEADER
# =======================================================================
st.markdown(
    '<div class="eyebrow">Portfolio Project · Exploratory Data Analysis</div>'
    '<div class="hero-title">AI Job Market Salary Dashboard</div>'
    '<div class="hero-sub">A full picture of the global AI and data job market — who is posting, '
    'where, and in what roles — not just what they pay, blended with a transparent, '
    'trend-based projection for the years ahead.</div>',
    unsafe_allow_html=True,
)

# =======================================================================
# PAGE 1 — OVERVIEW: a broad snapshot across every dimension, not just salary
# =======================================================================
if page == "Overview":
    page_head("Overview", "The shape of the market: where the postings are, not only what they pay")

    with st.container(border=True):
        section_head("Snapshot", "Filtered market at a glance")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Postings shown", f"{len(filtered_df):,}")
        c2.metric("Average salary", f"${filtered_df['salary_usd'].mean():,.0f}")
        c3.metric("Regions covered", f"{filtered_df['region'].nunique()}")
        c4.metric("Top role category", filtered_df["ai_role_category"].mode().iloc[0])

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            region_counts = filtered_df["region"].value_counts().sort_values().reset_index()
            region_counts.columns = ["region", "count"]
            fig = px.bar(region_counts, x="count", y="region", orientation="h",
                         title="Postings by Region")
            st.plotly_chart(style_fig(fig, T), use_container_width=True)
    with col2:
        with st.container(border=True):
            exp_order = ["Entry Level", "Mid Level", "Senior", "Executive"]
            avail = [e for e in exp_order if e in filtered_df["experience_level"].unique()]
            exp_counts = filtered_df["experience_level"].value_counts().reindex(avail).reset_index()
            exp_counts.columns = ["experience_level", "count"]
            fig = px.bar(exp_counts, x="experience_level", y="count",
                         title="Postings by Experience Level")
            st.plotly_chart(style_fig(fig, T), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        with st.container(border=True):
            work_counts = filtered_df["remote_type"].value_counts().reset_index()
            work_counts.columns = ["remote_type", "count"]
            fig = px.bar(work_counts, x="remote_type", y="count", title="Postings by Work Type")
            st.plotly_chart(style_fig(fig, T), use_container_width=True)
    with col4:
        with st.container(border=True):
            role_counts = filtered_df["ai_role_category"].value_counts().sort_values().reset_index()
            role_counts.columns = ["ai_role_category", "count"]
            fig = px.bar(role_counts, x="count", y="ai_role_category", orientation="h",
                         title="Postings by AI Role Category")
            st.plotly_chart(style_fig(fig, T, height=420), use_container_width=True)

    col5, col6 = st.columns(2)
    with col5:
        with st.container(border=True):
            top_industries = filtered_df["industry"].value_counts().head(8).reset_index()
            top_industries.columns = ["industry", "count"]
            fig = px.bar(top_industries, x="industry", y="count", title="Top 8 Industries by Job Count")
            fig.update_xaxes(tickangle=-30)
            st.plotly_chart(style_fig(fig, T), use_container_width=True)
    with col6:
        with st.container(border=True):
            fig = px.histogram(filtered_df, x="salary_usd", nbins=30, marginal="box",
                                title="Salary Distribution")
            fig.update_xaxes(title="Salary (USD)")
            st.plotly_chart(style_fig(fig, T), use_container_width=True)

    mini_insight("Technology-sector, North-America-based, Senior-level postings dominate the "
                 "raw volume of listings — worth keeping in mind when reading averages elsewhere "
                 "in the dashboard, since smaller categories carry less statistical weight.")

# =======================================================================
# PAGE 2 — DEEP DIVE: every detailed / comparative chart, one page, sectioned
# =======================================================================
elif page == "Deep Dive":
    page_head("Deep Dive", "Compensation, trends, roles, and work style — all in one place")

    # ---------- Compensation ----------
    with st.container(border=True):
        section_head("Salary Breakdown", "What drives the salary spread")
        col1, col2 = st.columns(2)
        with col1:
            exp_order = ["Entry Level", "Mid Level", "Senior", "Executive"]
            avail = [e for e in exp_order if e in filtered_df["experience_level"].unique()]
            fig = px.bar(
                filtered_df.groupby("experience_level")["salary_usd"].mean().reindex(avail).reset_index(),
                x="experience_level", y="salary_usd", title="Average Salary by Experience Level",
                category_orders={"experience_level": avail},
            )
            st.plotly_chart(style_fig(fig, T), use_container_width=True)
        with col2:
            reg_avg = filtered_df.groupby("region")["salary_usd"].mean().sort_values().reset_index()
            fig = px.bar(reg_avg, x="salary_usd", y="region", orientation="h", title="Average Salary by Region")
            st.plotly_chart(style_fig(fig, T), use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            fig = px.box(filtered_df, x="remote_type", y="salary_usd", title="Salary by Work Type")
            st.plotly_chart(style_fig(fig, T), use_container_width=True)
        with col4:
            pivot = filtered_df.pivot_table(values="salary_usd", index="experience_level",
                                              columns="company_size", aggfunc="mean")
            fig = px.imshow(pivot, text_auto=".0f", color_continuous_scale=HEATMAP_SCALE,
                             title="Salary: Experience Level × Company Size")
            st.plotly_chart(style_fig(fig, T), use_container_width=True)

        mini_insight("Experience level drives salary far more than work type — the Entry-to-Executive "
                     "gap is the widest split in the whole dataset, and company size mainly matters "
                     "at the Entry, Senior, and Executive levels.")

    st.write("")
    # ---------- Trends & Projections ----------
    with st.container(border=True):
        section_head("Trends & projections", "Real data vs. trend-based projection")
        lineage_legend()
        st.write("")

        real = filtered_df[filtered_df["data_note"] == "real"].groupby("work_year")["salary_usd"].mean()
        extrap = filtered_df[filtered_df["data_note"] == "extrapolated"].groupby("work_year")["salary_usd"].mean()

        fig = go.Figure()
        if len(real) > 0:
            fig.add_trace(go.Scatter(x=real.index, y=real.values, mode="lines+markers",
                                      name="Real data", line=dict(color=T["accent"], width=3)))
        if len(extrap) > 0:
            fig.add_trace(go.Scatter(x=extrap.index, y=extrap.values, mode="lines+markers",
                                      name="Extrapolated", line=dict(color=T["accent2"], width=3, dash="dash")))
        fig.update_layout(title="Salary Trend: Real vs Extrapolated Data",
                           xaxis_title="Year", yaxis_title="Average Salary (USD)")
        st.plotly_chart(style_fig(fig, T), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            yearly = filtered_df.groupby("work_year")["salary_usd"].mean().reset_index()
            fig = px.line(yearly, x="work_year", y="salary_usd", markers=True,
                           title="Overall Average Salary Trend")
            st.plotly_chart(style_fig(fig, T), use_container_width=True)
        with col2:
            corr = filtered_df[["salary_usd", "yoy_demand_change", "work_year"]].corr()
            fig = px.imshow(corr, text_auto=".2f", color_continuous_scale=HEATMAP_SCALE, title="Correlation Heatmap")
            st.plotly_chart(style_fig(fig, T), use_container_width=True)

        mini_insight("The extrapolated years (2024–2026) follow a similar shape to the real historical "
                     "trend rather than jumping randomly, which makes the projection look reasonable "
                     "rather than arbitrary.")

    st.write("")
    # ---------- Roles & Skills ----------
    with st.container(border=True):
        section_head("Roles & skills", "Where the specialization premium shows up")
        col1, col2 = st.columns(2)
        with col1:
            role_avg = filtered_df.groupby("ai_role_category")["salary_usd"].mean().sort_values().reset_index()
            fig = px.bar(role_avg, x="salary_usd", y="ai_role_category", orientation="h",
                          title="Average Salary by AI Role Category")
            st.plotly_chart(style_fig(fig, T, height=420), use_container_width=True)
        with col2:
            tools = filtered_df["ai_tools_required"].str.split(",").explode().str.strip()
            top_tools = tools.value_counts().head(10).sort_values().reset_index()
            top_tools.columns = ["tool", "count"]
            fig = px.bar(top_tools, x="count", y="tool", orientation="h",
                          title="Top 10 Most Required AI Tools/Skills")
            st.plotly_chart(style_fig(fig, T, height=420), use_container_width=True)

        mini_insight("NLP/LLM roles pay roughly 3x more than Data Analytics roles, and Python, SQL, "
                     "and dbt are the most frequently required skills across postings.")

    st.write("")
    # ---------- Work Style & Risk ----------
    with st.container(border=True):
        section_head("Work style & risk", "Remote flexibility and automation exposure")
        col1, col2 = st.columns(2)
        with col1:
            fig = px.box(filtered_df, x="ai_disruption_risk", y="salary_usd",
                          category_orders={"ai_disruption_risk": ["Low", "Medium", "High"]},
                          title="Salary vs AI Disruption Risk")
            st.plotly_chart(style_fig(fig, T), use_container_width=True)
        with col2:
            pivot2 = filtered_df.pivot_table(values="salary_usd", index="experience_level",
                                               columns="remote_type", aggfunc="mean")
            fig = px.imshow(pivot2, text_auto=".0f", color_continuous_scale=HEATMAP_SCALE,
                             title="Salary: Experience Level × Work Type")
            st.plotly_chart(style_fig(fig, T), use_container_width=True)

        remote_counts = filtered_df["remote_type"].value_counts().reset_index()
        remote_counts.columns = ["remote_type", "count"]
        fig = px.pie(remote_counts, names="remote_type", values="count", hole=0.55,
                      title="Work Type Split")
        st.plotly_chart(style_fig(fig, T, height=360), use_container_width=True)

        mini_insight("AI disruption risk shows no strong link to salary — pay looks tied more to skill "
                     "and role than to how automatable a job is.")

# =======================================================================
# PAGE 3 — INSIGHTS & PREDICTOR
# =======================================================================
else:
    page_head("Insights", "Key takeaways from the analysis")

    with st.container(border=True):
        section_head("Insights", "Key takeaways")
        st.caption("Grouped by theme so the headline finding is easy to scan, with the supporting detail right after it.")
        st.write("")

        insight_group("What drives pay", [
            ("Experience beats everything else",
             "the Entry-to-Executive gap is the widest split in the dataset — wider than the gap "
             "between any two remote work types or AI-disruption-risk levels."),
            ("Specialization commands a premium",
             "NLP/LLM roles pay roughly 3x more than general Data Analytics roles."),
        ])

        insight_group("How reliable the projections are", [
            ("2024–2026 estimates track the real trend",
             "the projected years follow the same shape as the observed 2020–2023 data, rather "
             "than jumping in a random or arbitrary direction."),
        ])

        insight_group("Read with caution", [
            ("Automation risk isn't a pay signal",
             "AI disruption risk shows no strong relationship with salary — pay tracks skill and "
             "role, not how automatable a job looks."),
            ("The sample is concentrated",
             "~76% of postings are in Technology and North America dominates by region, so "
             "smaller categories should be read with wider error bars in mind."),
        ])

# =======================================================================
# FOOTER
# =======================================================================
st.write("")
with st.container(border=True):
    fcol1, fcol2 = st.columns([2, 1])
    with fcol1:
        st.markdown('<div class="footer-name">Maram Alzahrani</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="footer-role">Data Scientist · Tuwaiq Academy Data Science &amp; AI Bootcamp — Unit 3 Final Project</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<span class="stack-line">Python · Pandas · Plotly · Streamlit</span>',
            unsafe_allow_html=True,
        )
    with fcol2:
        st.markdown(
            '<div style="text-align:right; margin-top:6px;">'
            '<a class="link-pill" href="https://github.com/Maramjamaan/AI-Job-Market-EDA-Project" target="_blank">GitHub ↗</a>'
            '<a class="link-pill" href="https://www.linkedin.com/in/maram-alzahrani314/" target="_blank">LinkedIn ↗</a>'
            '</div>',
            unsafe_allow_html=True,
        )