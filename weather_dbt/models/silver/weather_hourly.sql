{{ config(materialized='table') }}

SELECT
    city,
    lat,
    lon,
    time,
    temperature_2m,
    precipitation,
    relative_humidity_2m,
    wind_speed_10m,
    ingestion_id,
    ingested_at
FROM silver.weather_hourly
