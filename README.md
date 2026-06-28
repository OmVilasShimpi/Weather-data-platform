# 🌦️ Weather Data Platform

An end-to-end data engineering project that ingests **live weather data** from a public API and processes it using a **Bronze / Silver / Gold** data model with **Python, PostgreSQL, dbt, Docker, and Metabase**.

This project demonstrates **production-style data engineering practices**: raw data ingestion, layered transformations, automated data quality testing, data freshness monitoring, and analytics-ready dashboards.

---

## 🚀 Project Overview

### Goal

Build a production-style weather analytics platform that:

- Ingests **live weather data** from an external API
- Stores raw data safely without modification in a **Bronze layer**
- Transforms raw JSON data into clean, structured tables in a **Silver layer**
- Aggregates data into analytics-ready summaries in a **Gold layer**
- Enforces data quality using automated **dbt tests**
- Provides dashboard-ready data for weather trend analysis
- Tracks ingestion timestamps to support data freshness monitoring

⏱️ The ingestion script is designed to support scheduled runs, enabling near-real-time analytics when connected to a scheduler such as cron, Windows Task Scheduler, or GitHub Actions.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|----------|--------|
| Python | API ingestion and pipeline logic |
| PostgreSQL | Analytical data warehouse |
| JSONB | Raw semi-structured weather data storage |
| dbt | Data transformations, testing, and modelling |
| Metabase | Analytics and dashboards |
| Docker | Local infrastructure |
| GitHub Actions | CI checks for dbt |
| Git & GitHub | Version control and project hosting |

---

## 🏗️ Architecture

```text
Open-Meteo API
      ↓
Python Ingestion
      ↓
PostgreSQL
      ↓
Bronze Layer (raw JSONB)
      ↓
dbt transformations
      ↓
Silver Layer (structured hourly observations)
      ↓
Gold Layer (daily aggregated summaries)
      ↓
Metabase Dashboards
```

---

## 🗂️ Data Layers

### 🥉 Bronze Layer

**Raw, immutable data**

The Bronze layer stores raw weather API responses from Open-Meteo in PostgreSQL using JSONB.

- Weather data fetched from Open-Meteo API
- Stored as raw JSONB for schema flexibility
- Preserves original API response structure
- Includes ingestion timestamp for freshness tracking
- Designed as an append-style raw data layer

Bronze table:

```text
bronze.weather_hourly_raw
```

The Bronze table is created using:

```text
sql/create_bronze_tables.sql
```

---

### 🥈 Silver Layer

**Cleaned and structured data**

The Silver layer parses raw JSONB weather data into typed, structured hourly observations.

- Extracts useful fields from raw API payloads
- Creates one row per city per observation time
- Converts semi-structured JSON into queryable columns
- Prepares clean data for downstream analytics

Silver model:

```text
silver.weather_hourly
```

Example fields include:

- city
- observation time
- temperature
- humidity
- precipitation
- wind speed
- ingestion timestamp

---

### 🥇 Gold Layer

**Analytics-ready aggregations**

The Gold layer creates daily city-level weather summaries for dashboards and analysis.

Gold model:

```text
gold.weather_daily_summary
```

Metrics include:

- Average daily temperature
- Minimum daily temperature
- Maximum daily temperature
- Total daily precipitation
- Average humidity
- Maximum wind speed
- Number of hourly observations per day
- Latest ingestion timestamp

---

## 🧪 Data Quality

The project uses **dbt tests** to improve data reliability and validate transformed models.

Tests include:

- `not_null` tests on critical columns
- `unique` tests to enforce correct data grain
- accepted values checks
- basic completeness and quality validation

Run tests with:

```bash
dbt test
```

These checks help ensure that the Silver and Gold layers remain trustworthy as the dataset grows.

---

## ⏱️ Ingestion & Data Freshness

The Python ingestion script can be run manually or connected to a scheduler for regular updates.

To support freshness monitoring:

- Each raw record includes an `ingested_at` timestamp
- Transformed models preserve ingestion metadata
- Dashboards can display a "Last updated" indicator
- Stale data can be detected using the freshness check script

Freshness check script:

```text
ingestion/check_freshness.py
```

This mirrors real production monitoring patterns where users need to know whether dashboard data is current.

---

## 📊 Analytics & Visualization

Metabase dashboards can be connected to the Gold layer for weather analysis.

Dashboard use cases include:

- 📈 Daily temperature trends
- 🌧️ Precipitation analysis
- 🏙️ City-level comparisons
- 💨 Wind speed patterns
- ⏱️ Latest available weather snapshot per city
- 🔍 Freshness visibility using ingestion timestamps

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
- Python 3.9+
- Git
- PostgreSQL client tools such as `psql`
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
- Metabase

Metabase will be available at:

```text
http://localhost:3000
```

### 3️⃣ Set up Python environment

```bash
python -m venv venv
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure environment variables

Create a `.env` file in the project root:

```env
PGHOST=localhost
PGPORT=5432
PGDATABASE=weather
PGUSER=<your_db_user>
PGPASSWORD=<your_db_password>
```

⚠️ `.env` is excluded via `.gitignore` and should never be committed.

### 5️⃣ Create the Bronze table

Run the Bronze setup SQL file:

```bash
psql -h localhost -U postgres -d weather -f sql/create_bronze_tables.sql
```

This creates:

```text
bronze.weather_hourly_raw
```

The Python ingestion script writes raw Open-Meteo API responses into this table as JSONB.

### 6️⃣ Run ingestion manually

```bash
python ingestion/fetch_weather.py
```

This fetches weather data from the Open-Meteo API and stores the raw response in the Bronze table.

### 7️⃣ Run dbt transformations

Move into the dbt project folder:

```bash
cd weather_dbt
```

Run dbt models:

```bash
dbt run
```

Run dbt tests:

```bash
dbt test
```

### 8️⃣ View dashboards

Open Metabase:

```text
http://localhost:3000
```

Connect Metabase to PostgreSQL and build dashboards using the Gold layer tables.

---

## 📂 Project Structure

```text
weather-data-platform/
├── .github/
│   └── workflows/
│       └── dbt-ci.yml
├── ingestion/
│   ├── fetch_weather.py
│   └── check_freshness.py
├── sql/
│   └── create_bronze_tables.sql
├── weather_dbt/
│   ├── models/
│   │   ├── silver/
│   │   │   └── weather_hourly.sql
│   │   └── gold/
│   │       └── weather_daily_summary.sql
│   ├── tests/
│   ├── dbt_project.yml
│   └── README.md
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ✅ Current Features

- Live weather API ingestion using Python
- Raw JSONB storage in PostgreSQL
- Bronze / Silver / Gold data modelling approach
- dbt transformations for structured analytics tables
- dbt tests for data quality validation
- Data freshness tracking using ingestion timestamps
- Docker-based local infrastructure
- Metabase-ready analytics layer
- GitHub Actions workflow for dbt checks

---

## 📌 Key Learnings

Through this project, you gain experience with:

- Designing layered data models using Bronze / Silver / Gold architecture
- Handling semi-structured JSON data in PostgreSQL
- Building reproducible data pipelines with Python and dbt
- Writing analytics-ready SQL transformations
- Implementing automated data quality checks
- Monitoring data freshness
- Creating dashboard-ready datasets
- Managing an end-to-end data engineering project

---

## 🔮 Future Improvements

- Add a committed scheduler configuration for automated ingestion
- Deploy PostgreSQL and Metabase on cloud infrastructure
- Add alerts when data becomes stale
- Introduce incremental loading strategies in dbt
- Add more cities and weather metrics
- Implement true streaming ingestion using Kafka-style architecture
- Expand CI/CD pipeline for automated dbt testing and deployment
- Add dashboard screenshots to the README

---

## ⭐ Project Status

This project is portfolio-ready as a local end-to-end data engineering platform.

The next improvement would be to deploy it or add a scheduler configuration so ingestion runs automatically without manual execution.

---

⭐ **If you found this project helpful, please consider giving it a star!**