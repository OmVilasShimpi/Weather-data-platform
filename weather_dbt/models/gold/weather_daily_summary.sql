{{ config(materialized='table') }}

SELECT
  city,
  (time AT TIME ZONE 'Europe/London')::date AS day,

  AVG(temperature_2m) AS avg_temperature_2m,
  MIN(temperature_2m) AS min_temperature_2m,
  MAX(temperature_2m) AS max_temperature_2m,

  SUM(precipitation) AS total_precipitation,
  AVG(relative_humidity_2m) AS avg_humidity,
  MAX(wind_speed_10m) AS max_wind_speed,

  COUNT(*) AS hours_count
FROM {{ ref('weather_hourly') }}
GROUP BY city, (time AT TIME ZONE 'Europe/London')::date
