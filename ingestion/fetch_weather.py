import os
import json
import uuid
from datetime import datetime, timezone

import requests
import psycopg2
from dotenv import load_dotenv


def fetch_open_meteo(lat: float, lon: float) -> dict:
    """
    Fetch weather data from Open-Meteo and return raw JSON.

    Includes:
    - hourly forecast fields
    - current_weather (live snapshot)

    Bronze rule: store raw JSON as-is.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,

        # ✅ MUST be string "true" so Open-Meteo returns current_weather in payload
        "current_weather": "true",

        # Keep hourly forecast data as well
        "hourly": "temperature_2m,precipitation,relative_humidity_2m,wind_speed_10m",

        "timezone": "Europe/London",
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def get_conn():
    """
    Create a PostgreSQL connection using environment variables.
    Required: PGHOST, PGDATABASE, PGUSER, PGPASSWORD
    Optional: PGPORT (defaults to 5432)
    """
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=int(os.environ.get("PGPORT", "5432")),
        dbname=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
    )


def insert_bronze_weather_raw(conn, city: str, lat: float, lon: float, payload: dict):
    """
    Insert one raw weather payload into the Bronze table.
    """
    ingestion_id = str(uuid.uuid4())
    ingested_at = datetime.now(timezone.utc)

    sql = """
        INSERT INTO bronze.weather_hourly_raw (
            ingestion_id,
            ingested_at,
            city,
            lat,
            lon,
            payload
        )
        VALUES (%s, %s, %s, %s, %s, %s::jsonb);
    """

    with conn.cursor() as cur:
        cur.execute(
            sql,
            (
                ingestion_id,
                ingested_at,
                city,
                lat,
                lon,
                json.dumps(payload),
            ),
        )

    conn.commit()
    return ingestion_id, ingested_at


def main():
    load_dotenv()

    CITIES = [
        ("Manchester", 53.4808, -2.2426),
        ("London", 51.5074, -0.1278),
        ("Birmingham", 52.4862, -1.8904),
        ("Leeds", 53.8008, -1.5491),
        ("Liverpool", 53.4084, -2.9916),
        ("Sheffield", 53.3811, -1.4701),
        ("Bristol", 51.4545, -2.5879),
        ("Newcastle", 54.9783, -1.6178),
        ("Nottingham", 52.9548, -1.1581),
        ("Cambridge", 52.2053, 0.1218),
    ]

    with get_conn() as conn:
        for city, lat, lon in CITIES:
            payload = fetch_open_meteo(lat, lon)

            # ✅ Quick sanity print to confirm current_weather is present
            cw = payload.get("current_weather")
            if cw:
                print(f"🌤️  Live {city}: {cw.get('temperature')}°C at {cw.get('time')}")
            else:
                print(f"⚠️  current_weather missing for {city} (check API params)")

            ingestion_id, ingested_at = insert_bronze_weather_raw(conn, city, lat, lon, payload)

            print(f"✅ Inserted {city}")
            print(f"   ingestion_id: {ingestion_id}")
            print(f"   ingested_at (UTC): {ingested_at.isoformat()}")
            print("-" * 50)


if __name__ == "__main__":
    main()
