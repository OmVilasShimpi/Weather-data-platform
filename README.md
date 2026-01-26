# 🌦️ Weather Data Platform

An end-to-end **data engineering project** that ingests real weather data from a public API and processes it using a **Bronze / Silver / Gold** data model with **Python, PostgreSQL, and dbt**.

This project demonstrates production-ready data engineering practices: raw data ingestion, structured transformations, automated data quality testing, and analytics-ready outputs.

---

## 🚀 Project Overview

**Goal:**  
Build a production-style data platform that:
- Ingests real weather data from an external API  
- Stores raw data safely without modification (Bronze layer)  
- Transforms data into clean, structured tables (Silver layer)  
- Aggregates data into analytics-ready summaries (Gold layer)  
- Enforces data quality using automated dbt tests  

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python** | API ingestion scripts |
| **PostgreSQL** | Analytical data warehouse |
| **dbt** | Data transformations, testing, and modelling |
| **Metabase** | Querying and visualization |
| **Docker** | Local infrastructure setup |
| **Git & GitHub** | Version control |

---

## 🏗️ Architecture

```
Open-Meteo API → Python Ingestion → PostgreSQL
                                          ↓
                                    Bronze Layer (Raw JSONB)
                                          ↓
                                    dbt Transformations
                                          ↓
                                    Silver Layer (Structured)
                                          ↓
                                    Gold Layer (Aggregated)
                                          ↓
                                    Metabase Dashboards
```

---

## 🗂️ Data Layers

### 🥉 Bronze Layer
**Raw, immutable data**
- Weather data fetched from the Open-Meteo API  
- Stored as **JSONB** for flexibility  
- Append-only architecture (no updates or deletes)  

**Example table:** `bronze.weather_hourly_raw`

### 🥈 Silver Layer
**Cleaned and structured data**
- Parsed and typed hourly weather observations  
- One row per city per hour  
- Optimized for analytical queries  

**Example table:** `silver.weather_hourly`

### 🥇 Gold Layer
**Analytics-ready aggregations**
- Daily weather summaries by city  
- Pre-calculated metrics for dashboards  

**Example table:** `gold.weather_daily_summary`

**Metrics include:**
- Average / Minimum / Maximum temperature  
- Total daily precipitation  
- Average humidity  
- Maximum wind speed  
- Number of hourly records per day  

---

## 🧪 Data Quality (dbt Tests)

The project uses **dbt tests** to ensure data reliability:

- `not_null` tests on critical columns  
- `unique` tests to enforce correct data grain  
- Custom tests for data freshness and completeness  

Run all tests with:
```bash
dbt test
```

This ensures Silver and Gold tables remain trustworthy as data grows.

---

## 📋 Prerequisites

Before running this project, ensure you have:

- **Docker** and **Docker Compose** installed
- **Python 3.8+** installed
- **Git** for version control
- Basic familiarity with SQL and command line

---

## ▶️ How to Run the Project

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/weather-data-platform.git
cd weather-data-platform
```

### 2️⃣ Start infrastructure
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Metabase (accessible at `http://localhost:3000`)

### 3️⃣ Set up Python environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4️⃣ Run data ingestion
```bash
python ingestion/fetch_weather.py
```

This fetches the latest weather data and loads it into the Bronze layer.

### 5️⃣ Run dbt transformations and tests
```bash
cd weather_dbt
dbt run
dbt test
```

This will:
- Transform Bronze → Silver → Gold
- Run all data quality tests

### 6️⃣ View results in Metabase
1. Navigate to `http://localhost:3000`
2. Connect to PostgreSQL database
3. Query the Gold layer tables or build dashboards

---

## 📊 Analytics & Visualization

The final Gold tables can be used to build:

- 📈 Daily temperature trends
- 🌧️ Precipitation analysis  
- 🏙️ City-level weather comparisons
- 💨 Wind speed patterns

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

## 📂 Project Structure

```
weather-data-platform/
├── ingestion/              # Python scripts for API data fetching
│   └── fetch_weather.py
├── weather_dbt/            # dbt project
│   ├── models/
│   │   ├── bronze/        # Raw data models
│   │   ├── silver/        # Cleaned data models
│   │   └── gold/          # Aggregated models
│   ├── tests/             # Data quality tests
│   └── dbt_project.yml
├── docker-compose.yml      # Infrastructure setup
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 📌 Key Learnings

Through this project, you'll gain hands-on experience with:

✅ Designing layered data models (Bronze / Silver / Gold)  
✅ Handling semi-structured JSON data in PostgreSQL  
✅ Building reproducible data pipelines with dbt  
✅ Implementing automated data quality checks  
✅ End-to-end ownership of a data engineering project  

---

## 🔮 Future Improvements

- [ ] Add multiple cities dynamically from configuration
- [ ] Schedule ingestion using **Airflow** or **Prefect**
- [ ] Implement data freshness tests
- [ ] Add incremental loading strategies
- [ ] Extend dashboards with advanced analytics
- [ ] Add CI/CD pipeline for automated testing

---


Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - your.email@example.com

Project Link: [https://github.com/yourusername/weather-data-platform](https://github.com/yourusername/weather-data-platform)
