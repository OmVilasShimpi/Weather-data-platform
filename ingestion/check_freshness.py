import os
import sys
from datetime import datetime, timezone, timedelta

import psycopg2
from dotenv import load_dotenv


THRESHOLD_MINUTES = 15


def get_conn():
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=int(os.environ.get("PGPORT", "5432")),
        dbname=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
    )


def main():
    load_dotenv()

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                select max(ingested_at) as latest_ingested_at
                from bronze.weather_hourly_raw
            """)
            row = cur.fetchone()

    latest_ingested_at = row[0]

    if latest_ingested_at is None:
        print("ALERT: No ingestion data found in bronze.weather_hourly_raw")
        sys.exit(1)

    now_utc = datetime.now(timezone.utc)
    age = now_utc - latest_ingested_at
    threshold = timedelta(minutes=THRESHOLD_MINUTES)

    if age > threshold:
        print(
            f"ALERT: Data is stale. Latest ingestion was at {latest_ingested_at.isoformat()} "
            f"({age.total_seconds() / 60:.1f} minutes ago)."
        )
        sys.exit(1)

    print(
        f"OK: Data is fresh. Latest ingestion was at {latest_ingested_at.isoformat()} "
        f"({age.total_seconds() / 60:.1f} minutes ago)."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()