CREATE SCHEMA IF NOT EXISTS bronze;

CREATE TABLE IF NOT EXISTS bronze.weather_hourly_raw (
    ingestion_id text PRIMARY KEY,
    ingested_at timestamptz NOT NULL,
    city text NOT NULL,
    lat double precision NOT NULL,
    lon double precision NOT NULL,
    payload jsonb NOT NULL
);
