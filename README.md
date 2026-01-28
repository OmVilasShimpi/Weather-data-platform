# 🌦️ Weather Data Platform

An end-to-end data engineering project that ingests **live weather data** from a public API and processes it using a **Bronze / Silver / Gold** data model with **Python, PostgreSQL, dbt, and Metabase**.

This project demonstrates **production-style data engineering practices**: raw data ingestion, layered transformations, automated data quality testing, data freshness monitoring, and analytics-ready dashboards.

---

## 🚀 Project Overview

### Goal
Build a production-style weather analytics platform that:

- Ingests **live weather data** from an external API
- Stores raw data safely without modification (**Bronze layer**)
- Transforms data into clean, structured tables (**Silver layer**)
- Aggregates data into analytics-ready summaries (**Gold layer**)
- Enforces data quality using automated **dbt tests**
- Displays **near-real-time dashboards** with freshness indicators

⏱️ **Live ingestion runs automatically every 10 minutes**, enabling near-real-time analytics.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|----------|--------|
| Python | API ingestion & orchestration |
| PostgreSQL | Analytical data warehouse |
| dbt | Data transformations, testing, modelling |
| Metabase | Analytics & dashboards |
| Docker | Local infrastructure |
| Git & GitHub | Version control |

---

## 🏗️ Architecture

```
Open-Meteo API
      ↓
Python Ingestion (scheduled every 10 min)
      ↓
PostgreSQL
      ↓
Bronze Layer (raw JSONB)
      ↓
dbt transformations
      ↓
Silver Layer (structured)
      ↓
Gold Layer (aggregated)
      ↓
Metabase Dashboards
```

---

## 🗂️ Data Layers

### 🥉 Bronze Layer
**Raw, immutable data**

- Weather data fetched from Open-Meteo API
- Stored as JSONB for schema flexibility
- Append-only architecture (no updates / deletes)

Example table:
```
bronze.weather_hourly_raw
```

---

### 🥈 Silver Layer
**Cleaned & structured data**

- Parsed and typed hourly weather observations
- One row per city per hour
- Optimized for analytical queries

Example table:
```
silver.weather_hourly
```

---

### 🥇 Gold Layer
**Analytics-ready aggregations**

- Daily weather summaries by city
- Pre-calculated metrics for dashboards

Example table:
```
gold.weather_daily_summary
```

Metrics include:
- Average / minimum / maximum temperature
- Total daily precipitation
- Average humidity
- Maximum wind speed
- Number of hourly observations per day

---

## 🧪 Data Quality (dbt Tests)

The project uses **dbt tests** to ensure data reliability:

- `not_null` tests on critical columns
- `unique` tests to enforce correct data grain
- Custom tests for data freshness and completeness

Run tests with:
```bash
dbt test
```

This ensures Silver and Gold layers remain trustworthy as data grows.

---

## ⏱️ Live Ingestion & Data Freshness

Weather data is ingested automatically every 10 minutes via a scheduled ingestion process.

To ensure transparency and trust:

- Each record includes an `ingested_at` timestamp (UTC)
- Dashboards display a "Last updated X minutes ago" indicator
- Users can immediately see whether the data is fresh or stale

This mirrors real production monitoring patterns.

---

## 📊 Analytics & Visualization

Metabase dashboards provide:

- 📈 Daily temperature trends
- 🌧️ Precipitation analysis
- 🏙️ City-level comparisons
- 💨 Wind speed patterns
- ⏱️ Live snapshot of current conditions per city

Example query:

```sql
SELECT
  city,
  date,
  avg_temperature_c,
  total_precipitation_mm
FROM gold.weather_daily_summary
WHERE date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY date DESC;
```

---

## 📋 Prerequisites

- Docker & Docker Compose
- Python 3.9+ (tested on Python 3.13)
- Git
- Basic SQL knowledge

---

## ▶️ How to Run the Project

### 1️⃣ Clone the repository
```bash
git clone https://github.com/OmVilasShimpi/Weather-data-platform.git
cd weather-data-platform
```

### 2️⃣ Start infrastructure
```bash
docker-compose up -d
```

This starts:
- PostgreSQL
- Metabase (http://localhost:3000)

### 3️⃣ Set up Python environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables
Create a `.env` file in the project root:

```env
PGHOST=localhost
PGPORT=5432
PGDATABASE=weather
PGUSER=postgres
PGPASSWORD=postgres
```

⚠️ `.env` is excluded via `.gitignore` and should never be committed.

### 5️⃣ Run ingestion manually (optional)
```bash
python ingestion/fetch_weather.py
```

In production-style usage, ingestion runs automatically via a scheduler.

### 6️⃣ Run dbt transformations
```bash
cd weather_dbt
dbt run
dbt test
```

### 7️⃣ View dashboards
Open:
```
http://localhost:3000
```

Connect Metabase to PostgreSQL and explore dashboards.

---

## 📂 Project Structure

```
weather-data-platform/
├── ingestion/              # Python ingestion scripts
│   └── fetch_weather.py
├── weather_dbt/            # dbt project
│   ├── models/
│   │   ├── bronze/
│   │   ├── silver/
│   │   └── gold/
│   ├── tests/
│   └── dbt_project.yml
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📌 Key Learnings

Through this project, you gain experience with:

- Designing layered data models (Bronze / Silver / Gold)
- Handling semi-structured JSON data in PostgreSQL
- Building reproducible pipelines with dbt
- Implementing automated data quality checks
- Monitoring data freshness
- End-to-end ownership of a data engineering system

---

## 🔮 Future Improvements

- Deploy PostgreSQL and Metabase on cloud infrastructure
- Add alerts when data becomes stale
- Introduce incremental loading strategies
- Implement true streaming ingestion (Kafka-style)
- Add CI/CD pipeline for automated dbt testing

---


---

⭐ **If you found this project helpful, please consider giving it a star!**
