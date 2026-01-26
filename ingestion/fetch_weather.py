import os
import json
import uuid
from datetime import datetime, timezone

import requests
import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv


def fetch_open_meteo(lat: float, lon: float):
    """
    Fetch hourly weather data from Open-Meteo.
    We keep the returned JSON 'raw' because this is the Bronze layer.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,relative_humidity_2m,wind_speed_10m",
        "timezone": "Europe/London",
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def get_conn():
    """Create a Postgres connection from environment variables."""
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=int(os.environ.get("PGPORT", "5432")),
        dbname=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
    )


def insert_bronze_weather_raw(conn, city: str, lat: float, lon: float, payload: dict):
    """
    Insert one row into bronze.weather_hourly_raw.
    Assumes columns:
      ingestion_id (uuid), ingested_at (timestamptz), city (text), lat (float), lon (float), payload (jsonb)
    """
    ingestion_id = str(uuid.uuid4())
    ingested_at = datetime.now(timezone.utc)

    sql = """
        INSERT INTO bronze.weather_hourly_raw
            (ingestion_id, ingested_at, city, lat, lon, payload)
        VALUES
            (%s, %s, %s, %s, %s, %s::jsonb);
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
                json.dumps(payload),  # keep raw JSON exactly as returned
            ),
        )
    conn.commit()
    return ingestion_id, ingested_at


def main():
    load_dotenv()  # loads .env into environment variables

    # ✅ One city for now (you can add more later)
    city = "Manchester"
    lat = 53.48
    lon = -2.24

    payload = fetch_open_meteo(lat, lon)

    with get_conn() as conn:
        ingestion_id, ingested_at = insert_bronze_weather_raw(conn, city, lat, lon, payload)

    print("✅ Inserted into bronze.weather_hourly_raw")
    print("ingestion_id:", ingestion_id)
    print("ingested_at (UTC):", ingested_at.isoformat())


if __name__ == "__main__":
    main()
