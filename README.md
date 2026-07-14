# AI Job Market Salary Dashboard

An interactive Streamlit dashboard exploring how pay, demand, and role types have shifted across the global AI and data job market from 2020 to 2026 — blending real job postings with a transparent, trend-based projection for the years ahead.

**Live demo:** https://share.streamlit.io/-/auth/app?redirect_uri=https%3A%2F%2Fai-job-market-eda.streamlit.app%2F---

## Overview

This project analyzes **6,823 AI and data job postings** collected globally between 2020 and 2026. Postings from 2020–2023 reflect real job listings and salary survey data; postings from 2024–2026 are a trend-based projection, clearly flagged throughout the dashboard so the two are never confused.

The dashboard lets a user filter the dataset by year, experience level, region, work type, and data type, and explore the results across six focused views.

## Features

- **Snapshot KPIs** — average, median, and highest salary for the currently filtered postings
- **Compensation breakdown** — salary by experience level, region, work type, and company size
- **Trends & projections** — real vs. projected salary trend line, year-over-year averages, and a correlation heatmap
- **Roles & skills** — salary by AI role category, most in-demand tools/skills, and top industries by posting volume
- **Work style & risk** — salary vs. AI disruption risk, and the remote/hybrid/on-site split
- **Insights** — key takeaways written up as scannable, grouped bullet points
- Fully interactive sidebar filters (year range, experience level, region, work type, data type) that drive every chart and metric on the page

## Dataset

| | |
|---|---|
| Rows | 6,823 postings |
| Time range | 2020–2026 |
| Regions | 7 (North America, Europe, Asia Pacific, Latin America, Middle East, Africa, Other) |
| Data lineage | 2020–2023 real, 2024–2026 trend-based projection |
| File | `ai_job_market_salary_global_2020_2026_clean.csv` |

Key columns include `posting_date`, `work_year`, `job_title`, `ai_role_category`, `experience_level`, `salary_usd`, `region`, `remote_type`, `company_size`, `industry`, `ai_tools_required`, `ai_disruption_risk`, and `data_note`.

## Key Insights

**What drives pay**
- Experience level is the strongest driver of salary in this dataset — the Entry-to-Executive gap is wider than the gap between any two remote work types or AI-disruption-risk levels.
- Specialization commands a premium: NLP/LLM roles pay roughly 3x more than general Data Analytics roles.

**How reliable the projections are**
- The 2024–2026 estimates follow the same shape as the observed 2020–2023 data, rather than jumping in a random or arbitrary direction.

**Read with caution**
- AI disruption risk shows no strong relationship with salary — pay tracks skill and role, not how automatable a job looks.
- ~76% of postings are in the Technology industry and North America dominates by region, so smaller categories should be read with wider error bars in mind.

## Tech Stack

- **Python**
- **Pandas** — data loading and aggregation
- **Plotly** — interactive charts
- **Streamlit** — dashboard framework and UI

## Getting Started

### Prerequisites
- Python 3.9+

### Installation

```bash
# Clone the repository
git clone https://github.com/Maramjamaan/AI-Job-Market-EDA-Project.git
cd AI-Job-Market-EDA-Project

# (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the dashboard

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## Project Structure

```
AI-Job-Market-EDA-Project/
├── app.py                                          # Streamlit dashboard
├── ai_job_market_salary_global_2020_2026_clean.csv # Dataset
├── requirements.txt                                # Python dependencies
└── README.md                                       # Project documentation
```

## Author

**Maram Alzahrani**
Data Scientist · Tuwaiq Academy Data Science & AI Bootcamp — Unit 3 Final Project

- GitHub: [github.com/Maramjamaan](https://github.com/Maramjamaan)
- LinkedIn: [linkedin.com/in/maram-alzahrani314](https://www.linkedin.com/in/maram-alzahrani314/)

## License

This project was built for educational and portfolio purposes.