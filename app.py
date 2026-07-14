import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="AI Job Market Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =======================================================================
# THEME — single light "lilac" palette
# =======================================================================
T = {
    "bg": "#F9F6F9",         # 50
    "surface": "#FFFFFF",
    "surface_2": "#F4EFF4",  # 100
    "card_border": "#EBDFEA",  # 200
    "grid": "#DBC6DA",       # 300
    "subtext": "#805678",    # 700
    "text": "#352231",       # 950
    "accent": "#986A90",     # 600 — primary line/highlight
    "accent_warm": "#5B4055",  # 900 — secondary line/highlight
    "plotly_template": "plotly_white",
}
COLORWAY_EXTRA = ["#C19FBE", "#AF85AA", "#6B4964", "#DBC6DA"]


def inject_css(t):
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        color: {t['text']};
    }}
    h1, h2, h3, h4 {{
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.01em;
    }}
    .stApp {{ background: {t['bg']}; }}
    section[data-testid="stSidebar"] {{
        background: {t['surface']};
        border-right: 1px solid {t['card_border']};
    }}
    div[data-testid="stMetric"] {{
        background: {t['surface']};
        border: 1px solid {t['card_border']};
        border-radius: 10px;
        padding: 14px 16px;
    }}
    div[data-testid="stMetricLabel"] {{ color: {t['subtext']} !important; }}
    div[data-testid="stMetricValue"] {{
        color: {t['accent']} !important;
        font-family: 'Space Grotesk', sans-serif;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        border-bottom: 1px solid {t['card_border']};
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        color: {t['subtext']};
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
    }}
    .stTabs [aria-selected="true"] {{
        background: {t['surface_2']} !important;
        color: {t['accent_warm']} !important;
    }}
    .eyebrow {{
        color: {t['accent']};
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: -6px;
    }}
    .insight-card {{
        background: {t['surface']};
        border: 1px solid {t['card_border']};
        border-left: 3px solid {t['accent']};
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 10px;
        color: {t['text']};
    }}
    .mini-insight {{
        color: {t['subtext']};
        font-size: 0.9rem;
        border-left: 2px solid {t['accent']};
        padding-left: 10px;
        margin: 4px 0 18px 0;
    }}
    hr {{ border-color: {t['card_border']}; }}
    </style>
    """, unsafe_allow_html=True)


def style_fig(fig, t, height=400):
    """Apply the lilac theme + colorway to a Plotly figure."""
    fig.update_layout(
        template=t["plotly_template"],
        paper_bgcolor=t["surface"],
        plot_bgcolor=t["surface"],
        font=dict(family="Inter, sans-serif", color=t["text"], size=13),
        title_font=dict(family="Space Grotesk, sans-serif", size=16, color=t["text"]),
        colorway=[t["accent"], t["accent_warm"]] + COLORWAY_EXTRA,
        margin=dict(l=10, r=10, t=50, b=10),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor=t["grid"], zerolinecolor=t["grid"])
    fig.update_yaxes(gridcolor=t["grid"], zerolinecolor=t["grid"])
    return fig


def mini_insight(text):
    """Short one-line insight caption placed under a chart section."""
    st.markdown(f'<div class="mini-insight">💡 {text}</div>', unsafe_allow_html=True)


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
# SIDEBAR — description + filters
# =======================================================================
st.sidebar.markdown("### About this dataset")
st.sidebar.write(
    "6,823 AI/data job postings collected globally, 2020–2026. "
    "**2020–2023** reflects real postings and salary surveys. "
    "**2024–2026** is trend-based projection, explicitly flagged below."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")

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

st.sidebar.markdown("---")
st.sidebar.caption(f"**{len(filtered_df):,}** of {len(df):,} postings match your filters")

if filtered_df.empty:
    st.warning("No postings match the current filters — try widening your selection.")
    st.stop()

# =======================================================================
# HEADER
# =======================================================================
st.markdown('<div class="eyebrow">Global AI &amp; Data Careers · 2020–2026</div>', unsafe_allow_html=True)
st.title("AI Job Market Salary Dashboard")
st.markdown(
    f'<span style="color:{T["subtext"]}">Exploring how pay, demand, and role types have shifted '
    "across the AI and data job market, blending real postings with forward-looking projections.</span>",
    unsafe_allow_html=True,
)
st.write("")

# =======================================================================
# TABS
# =======================================================================
tab_overview, tab_pay, tab_trends, tab_roles, tab_worklife, tab_insights = st.tabs(
    ["Overview", "Compensation", "Trends & Projections", "Roles & Skills", "Work Style & Risk", "Insights"]
)

# ---------- OVERVIEW ----------
with tab_overview:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Average salary", f"${filtered_df['salary_usd'].mean():,.0f}")
    c2.metric("Median salary", f"${filtered_df['salary_usd'].median():,.0f}")
    c3.metric("Highest salary", f"${filtered_df['salary_usd'].max():,.0f}")
    c4.metric("Postings shown", f"{len(filtered_df):,}")
    st.write("")

    col1, col2 = st.columns([1.3, 1])
    with col1:
        fig = px.histogram(filtered_df, x="salary_usd", nbins=30, marginal="box",
                            title="Salary Distribution")
        fig.update_xaxes(title="Salary (USD)")
        st.plotly_chart(style_fig(fig, T), use_container_width=True)
    with col2:
        counts = filtered_df["experience_level"].value_counts().reset_index()
        counts.columns = ["experience_level", "count"]
        fig = px.bar(counts, x="experience_level", y="count", title="Postings by Experience Level")
        st.plotly_chart(style_fig(fig, T), use_container_width=True)

    mini_insight("Most salaries cluster between $100K–$200K with a right-skewed tail, "
                 "and Senior-level postings make up the largest share of the market.")

    st.markdown("##### Data preview")
    st.dataframe(filtered_df.head(20), use_container_width=True)

# ---------- COMPENSATION ----------
with tab_pay:
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
        fig = px.imshow(pivot, text_auto=".0f", color_continuous_scale="Purp",
                         title="Salary: Experience Level × Company Size")
        st.plotly_chart(style_fig(fig, T), use_container_width=True)

    mini_insight("Experience level drives salary far more than work type — the Entry-to-Executive "
                 "gap is the widest split in the whole dataset, and company size mainly matters "
                 "at the Entry, Senior, and Executive levels.")

# ---------- TRENDS & PROJECTIONS ----------
with tab_trends:
    real = filtered_df[filtered_df["data_note"] == "real"].groupby("work_year")["salary_usd"].mean()
    extrap = filtered_df[filtered_df["data_note"] == "extrapolated"].groupby("work_year")["salary_usd"].mean()

    fig = go.Figure()
    if len(real) > 0:
        fig.add_trace(go.Scatter(x=real.index, y=real.values, mode="lines+markers",
                                  name="Real data", line=dict(color=T["accent"], width=3)))
    if len(extrap) > 0:
        fig.add_trace(go.Scatter(x=extrap.index, y=extrap.values, mode="lines+markers",
                                  name="Extrapolated", line=dict(color=T["accent_warm"], width=3, dash="dash")))
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
        fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="Purp", title="Correlation Heatmap")
        st.plotly_chart(style_fig(fig, T), use_container_width=True)

    mini_insight("The extrapolated years (2024–2026) follow a similar shape to the real historical "
                 "trend rather than jumping randomly, which makes the projection look reasonable "
                 "rather than arbitrary.")

# ---------- ROLES & SKILLS ----------
with tab_roles:
    col1, col2 = st.columns(2)
    with col1:
        role_avg = filtered_df.groupby("ai_role_category")["salary_usd"].mean().sort_values().reset_index()
        fig = px.bar(role_avg, x="salary_usd", y="ai_role_category", orientation="h",
                      title="Average Salary by AI Role Category")
        st.plotly_chart(style_fig(fig, T, height=460), use_container_width=True)
    with col2:
        tools = filtered_df["ai_tools_required"].str.split(",").explode().str.strip()
        top_tools = tools.value_counts().head(10).sort_values().reset_index()
        top_tools.columns = ["tool", "count"]
        fig = px.bar(top_tools, x="count", y="tool", orientation="h",
                      title="Top 10 Most Required AI Tools/Skills")
        st.plotly_chart(style_fig(fig, T, height=460), use_container_width=True)

    top_industries = filtered_df["industry"].value_counts().head(8).reset_index()
    top_industries.columns = ["industry", "count"]
    fig = px.bar(top_industries, x="industry", y="count", title="Top 8 Industries by Job Count")
    st.plotly_chart(style_fig(fig, T), use_container_width=True)

    mini_insight("NLP/LLM roles pay roughly 3x more than Data Analytics roles, and Python, SQL, "
                 "and dbt are the most frequently required skills across postings.")

# ---------- WORK STYLE & RISK ----------
with tab_worklife:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.box(filtered_df, x="ai_disruption_risk", y="salary_usd",
                      category_orders={"ai_disruption_risk": ["Low", "Medium", "High"]},
                      title="Salary vs AI Disruption Risk")
        st.plotly_chart(style_fig(fig, T), use_container_width=True)
    with col2:
        pivot2 = filtered_df.pivot_table(values="salary_usd", index="experience_level",
                                           columns="remote_type", aggfunc="mean")
        fig = px.imshow(pivot2, text_auto=".0f", color_continuous_scale="Purp",
                         title="Salary: Experience Level × Work Type")
        st.plotly_chart(style_fig(fig, T), use_container_width=True)

    remote_counts = filtered_df["remote_type"].value_counts().reset_index()
    remote_counts.columns = ["remote_type", "count"]
    fig = px.pie(remote_counts, names="remote_type", values="count", hole=0.55,
                  title="Work Type Split", color_discrete_sequence=[T["accent"], T["accent_warm"]] + COLORWAY_EXTRA)
    st.plotly_chart(style_fig(fig, T, height=360), use_container_width=True)

    mini_insight("AI disruption risk shows no strong link to salary — pay looks tied more to skill "
                 "and role than to how automatable a job is.")

# ---------- INSIGHTS ----------
with tab_insights:
    st.markdown("##### Key takeaways")
    insights = [
        "Experience level is the strongest driver of salary in this dataset — more than remote "
        "work type or AI disruption risk.",
        "Specialized roles like NLP/LLM pay noticeably more than general data roles, reflecting "
        "the market's premium on specialized AI skills.",
        "The projected data (2024–2026) follows a similar pattern to the real data (2020–2023), "
        "suggesting the projections are reasonable rather than random.",
        "AI disruption risk doesn't show a strong relationship with salary — pay looks tied more "
        "to skill and role than to automation exposure.",
        "Technology dominates the industry breakdown (~76% of postings) and North America "
        "dominates by region — smaller categories should be read with caution given limited "
        "sample sizes.",
    ]
    for text in insights:
        st.markdown(f'<div class="insight-card">{text}</div>', unsafe_allow_html=True)

st.write("")
st.caption("Built by Maram Alzahrani — Tuwaiq Academy Data Science & AI Bootcamp, Unit 3 Final Project")