# Weather dbt Project

This dbt project transforms raw weather API data from the Bronze layer into analytics-ready Silver and Gold models.

## Overview

The dbt part of this project is responsible for transforming raw weather API data stored in PostgreSQL into clean, structured, and aggregated tables that can be used for analysis and dashboarding.

The full pipeline follows a Bronze-Silver-Gold data engineering architecture:

```text
Open-Meteo API
      ↓
Python Ingestion
      ↓
PostgreSQL Bronze Layer
      ↓
dbt Silver Model
      ↓
dbt Gold Model
      ↓
Metabase Dashboard
```

## Data Layers

### Bronze Layer

The Bronze layer stores raw weather API responses in PostgreSQL as JSONB data.

This layer is created outside dbt using the SQL setup file in the main project folder:

```text
sql/create_bronze_tables.sql
```

The Python ingestion script writes raw Open-Meteo API responses into the Bronze table.

Bronze table:

```text
bronze.weather_hourly_raw
```

### Silver Layer

The Silver layer cleans and structures the raw Bronze data into hourly city-level weather observations.

Silver model:

```text
silver.weather_hourly
```

This model extracts useful fields such as:

- city
- observation time
- temperature
- humidity
- wind speed
- precipitation
- ingestion timestamp

### Gold Layer

The Gold layer creates daily city-level weather summaries for analytics and dashboarding.

Gold model:

```text
gold.weather_daily_summary
```

This model provides aggregated metrics such as:

- average daily temperature
- minimum daily temperature
- maximum daily temperature
- total precipitation
- average wind speed
- latest ingestion timestamp

## dbt Models

```text
weather_dbt/
├── models/
│   ├── silver/
│   │   └── weather_hourly.sql
│   └── gold/
│       └── weather_daily_summary.sql
├── dbt_project.yml
└── README.md
```

## Data Quality Tests

The project includes dbt tests to validate important fields and improve data reliability.

Tests include:

- non-null checks
- unique record checks
- accepted values
- basic data quality validation

These tests help ensure that the transformed data is suitable for dashboarding and analysis.

## Running the dbt Project

From inside the `weather_dbt` folder, run:

```bash
dbt run
```

To run data quality tests:

```bash
dbt test
```

## Requirements

This dbt project uses PostgreSQL as the data warehouse.

The required Python/dbt dependencies are listed in the main project-level `requirements.txt` file.

## Purpose

This dbt project demonstrates a practical Bronze-Silver-Gold data transformation workflow using PostgreSQL and dbt.

It is part of a larger weather data engineering project that includes:

- Python API ingestion
- PostgreSQL raw data storage
- dbt transformations
- data quality testing
- Metabase dashboarding
- Docker-based local infrastructure
- GitHub Actions CI checks