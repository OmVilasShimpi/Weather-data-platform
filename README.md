Weather Data Platform

An end-to-end weather data engineering platform built using Python, PostgreSQL, and dbt, following a Bronze / Silver / Gold data architecture.

This project demonstrates real-world data engineering practices, including API ingestion, raw data preservation, structured transformations, analytics-ready aggregates, and data quality testing.

Architecture Overview
1. Ingestion (Python)

Fetches hourly weather data from the Open-Meteo API

Writes raw data directly into PostgreSQL

Uses append-only ingestion (no updates or deletes)

Stores raw payloads as JSONB (industry standard)

2. Data Warehouse (PostgreSQL)
Bronze Layer

Table: bronze.weather_hourly_raw

Stores raw API responses as JSONB

No cleaning or transformation

Acts as the source of truth

Silver Layer

Table: silver.weather_hourly

Cleaned and structured hourly data

One row per hour per city

Flattened from Bronze JSON

Gold Layer

Table: gold.weather_daily_summary

Aggregated daily metrics

One row per city per day

Designed for analytics and dashboards

3. Transformations (dbt)

Silver and Gold tables built using dbt models

Transformations are version-controlled

Reproducible using dbt run

Data quality enforced using dbt test

4. Analytics (Metabase)

SQL-based exploration

Ready for dashboards and charts

Built on the Gold layer

Tech Stack

Python

requests

psycopg2

python-dotenv

PostgreSQL

dbt (dbt-postgres)

Docker & Docker Compose

Metabase

Project Structure
weather-data-platform/
│
├── ingestion/
│   └── fetch_weather.py
│
├── weather_dbt/
│   ├── models/
│   │   ├── silver/
│   │   │   └── weather_hourly.sql
│   │   ├── gold/
│   │   │   └── weather_daily_summary.sql
│   │   └── schema.yml
│   ├── macros/
│   └── dbt_project.yml
│
├── docker-compose.yml
├── .gitignore
└── README.md

How to Run the Project
Step 1: Start PostgreSQL and Metabase

Start all services using Docker Compose:

docker compose up -d


Metabase: http://localhost:3000

PostgreSQL: localhost:5432

Step 2: Ingest Weather Data (Bronze)

Run the Python ingestion script:

python ingestion/fetch_weather.py


This will:

Call the Open-Meteo API

Insert raw hourly weather data into the Bronze table

Step 3: Run Transformations (Silver & Gold)

Navigate to the dbt project and run:

cd weather_dbt
dbt debug
dbt run
dbt test


dbt debug validates the connection

dbt run builds Silver and Gold tables

dbt test validates data quality

Output Tables
Silver Layer

Table: silver.weather_hourly

One row per hour per city

Gold Layer

Table: gold.weather_daily_summary

Daily metrics per city:

Average temperature

Minimum temperature

Maximum temperature

Total precipitation

Average humidity

Maximum wind speed

Hour count per day

Data Quality Guarantees

Implemented using dbt tests:

Not-null checks on key columns

Uniqueness checks to prevent duplicate records

Ensures analytics outputs are reliable and trustworthy

Design Principles

Bronze data is immutable

Transformations are idempotent

Business logic lives in dbt, not in ingestion scripts

Easy to scale to multiple cities

Follows production-style data engineering practices

Future Improvements

Add additional cities

Schedule ingestion using Airflow or Prefect

Build interactive Metabase dashboards

Add data freshness tests

Add CI/CD pipeline for dbt runs and tests

Why This Project

This project was built to demonstrate real data engineering workflows, not toy examples.

It reflects how modern analytics platforms are designed, tested, and maintained in production environments.

Next Steps

Add more cities to ingestion

Build a Metabase dashboard

Automate ingestion and transformations
