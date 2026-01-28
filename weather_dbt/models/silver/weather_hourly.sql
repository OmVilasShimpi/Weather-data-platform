{{ config(materialized='table') }}

WITH base AS (
  SELECT
    ingestion_id,
    ingested_at,
    city,
    lat,
    lon,
    payload
  FROM bronze.weather_hourly_raw
),

times AS (
  SELECT
    b.ingestion_id,
    b.ingested_at,
    b.city,
    b.lat,
    b.lon,
    t.time_str,
    t.idx
  FROM base b
  CROSS JOIN LATERAL jsonb_array_elements_text(b.payload->'hourly'->'time')
    WITH ORDINALITY AS t(time_str, idx)
),

temps AS (
  SELECT
    b.ingestion_id,
    a.idx,
    a.val::double precision AS temperature_2m
  FROM base b
  CROSS JOIN LATERAL jsonb_array_elements_text(b.payload->'hourly'->'temperature_2m')
    WITH ORDINALITY AS a(val, idx)
),

precip AS (
  SELECT
    b.ingestion_id,
    a.idx,
    a.val::double precision AS precipitation
  FROM base b
  CROSS JOIN LATERAL jsonb_array_elements_text(b.payload->'hourly'->'precipitation')
    WITH ORDINALITY AS a(val, idx)
),

humid AS (
  SELECT
    b.ingestion_id,
    a.idx,
    a.val::double precision AS relative_humidity_2m
  FROM base b
  CROSS JOIN LATERAL jsonb_array_elements_text(b.payload->'hourly'->'relative_humidity_2m')
    WITH ORDINALITY AS a(val, idx)
),

wind AS (
  SELECT
    b.ingestion_id,
    a.idx,
    a.val::double precision AS wind_speed_10m
  FROM base b
  CROSS JOIN LATERAL jsonb_array_elements_text(b.payload->'hourly'->'wind_speed_10m')
    WITH ORDINALITY AS a(val, idx)
)

SELECT
  t.city,
  t.lat,
  t.lon,
  (t.time_str::timestamp AT TIME ZONE 'Europe/London') AS time,
  te.temperature_2m,
  p.precipitation,
  h.relative_humidity_2m,
  w.wind_speed_10m,
  t.ingestion_id::uuid AS ingestion_id,
  t.ingested_at
FROM times t
LEFT JOIN temps  te ON te.ingestion_id = t.ingestion_id AND te.idx = t.idx
LEFT JOIN precip p  ON p.ingestion_id  = t.ingestion_id AND p.idx  = t.idx
LEFT JOIN humid  h  ON h.ingestion_id  = t.ingestion_id AND h.idx  = t.idx
LEFT JOIN wind   w  ON w.ingestion_id  = t.ingestion_id AND w.idx  = t.idx
