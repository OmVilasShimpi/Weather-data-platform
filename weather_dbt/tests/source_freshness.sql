with latest as (
    select max(ingested_at) as latest_ingested_at
    from bronze.weather_hourly_raw
)

select *
from latest
where latest_ingested_at is null
   or latest_ingested_at < now() - interval '15 minutes'
   