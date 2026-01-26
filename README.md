# Weather Data Platform

An end-to-end **data engineering platform** built using **Python**, **PostgreSQL**, and **dbt**, following a **Bronze / Silver / Gold** data architecture.

This project demonstrates real-world data engineering practices including API ingestion, raw data preservation, structured transformations, analytics-ready aggregates, and automated data quality testing.

---

## Architecture Overview

### 1. Ingestion (Python)

- Fetches hourly weather data from the **Open-Meteo API**
- Writes raw data directly into PostgreSQL
- Uses **append-only ingestion** (no updates or deletes)
- Stores raw payloads as **JSONB** (industry standard for raw data)

---

### 2. Data Warehouse (PostgreSQL)

#### Bronze Layer
- **Table:** `bronze.weather_hourly_raw`
- Stores raw API responses as JSONB
- No cleaning or transformation
- Acts as the immutable **source of truth**

#### Silver Layer
- **Table:** `silver.weather_hourly`
- Cleaned and structured hourly data
- One row per hour per city
- Flattened from Bronze JSON payloads

#### Gold Layer
- **Table:** `gold.weather_daily_summary`
- Aggregated daily metrics
- One row per city per day
- Designed for analytics and reporting

---

### 3. Transformations (dbt)

- Silver and Gold layers are implemented as **dbt models**
- Transformations are:
  - Version-controlled
  - Reproducible using `dbt run`
  - Validated using `dbt test`
- Business logic lives entirely in dbt (not ingestion scripts)

---

### 4. Analytics (Metabase)

- SQL-based exploration and querying
- Built on the Gold layer
- Ready for dashboards and visualizations

---

## Tech Stack

- **Python**
  - `requests`
  - `psycopg2`
  - `python-dotenv`
- **PostgreSQL**
- **dbt** (`dbt-postgres`)
- **Docker & Docker Compose**
- **Metabase**
---
## How to Run the Project

### Step 1: Start PostgreSQL and Metabase

Start all services using Docker Compose:
```bash
docker compose up -d
  - Metabase UI: http://localhost:3000
  - PostgreSQL: localhost:5432

**### Step 2: Ingest Weather Data (Bronze)**

Run the Python ingestion script:
 - python ingestion/fetch_weather.py
This will:
  - Call the Open-Meteo API
  - Insert raw hourly weather data into the Bronze table

**### Step 3: Run Transformations (Silver & Gold)**

Navigate to the dbt project and run:

**cd weather_dbt**
**dbt debug**
**dbt run**
**dbt test**
  - dbt debug → validates database connectivity
  - dbt run → builds Silver and Gold tables
  - dbt test → validates data quality
