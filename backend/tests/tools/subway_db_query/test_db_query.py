"""
Test: verify DB connection, seeding, and query matches production structure.
Run from backend/ dir: python -m tests.test_db_query
"""

import sys
from pathlib import Path

# Add backend to path so we can import app modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import SessionLocal, create_tables, seed_train_data
from app.tools.subway_db_query.models import Train
from app.tools.subway_db_query.queries import get_delays_by_station


def test_tables_exist():
    """Verify create_tables runs without error."""
    create_tables()
    print("[PASS] Tables created")


def test_seed_data():
    """Verify CSV is seeded into train table."""
    seed_train_data()
    db = SessionLocal()
    count = db.query(Train).count()
    db.close()
    print(f"[INFO] Train table has {count} rows")
    assert count > 0, "Train table is empty — seed failed"
    print("[PASS] Seed data loaded")


def test_query_by_station():
    """Verify querying by station name returns results."""
    db = SessionLocal()

    # Check what stations exist
    stations = db.query(Train.station).distinct().limit(5).all()
    print(f"[INFO] Sample stations: {[s[0] for s in stations]}")

    # Pick first station and query
    if stations:
        station_name = stations[0][0]
        results = get_delays_by_station(db, station_name)
        print(f"[INFO] Query '{station_name}' returned {len(results)} rows")
        assert len(results) > 0, f"No results for station '{station_name}'"
        print(f"[PASS] Query works — first row: delay={results[0].min_delay}, gap={results[0].min_gap}")

    db.close()


def test_query_victoria_park():
    """Verify VICTORIA PARK STATION specifically — mimics execution flow."""
    db = SessionLocal()

    # Exact same flow as executor: resolve variable → call tool
    from app.tools.subway_db_query.tool import SubwayDbQueryTool

    tool = SubwayDbQueryTool()
    result = tool.run({"station": "VICTORIA PARK STATION"}, db)
    print(f"[INFO] Tool output: {result[:200]}")

    import json
    parsed = json.loads(result)
    print(f"[INFO] total_records: {parsed['total_records']}")
    assert parsed["total_records"] > 0, "Tool returned 0 records for VICTORIA PARK STATION"
    print(f"[PASS] Tool returned {parsed['total_records']} records")

    db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("DB Connection & Query Tests")
    print("=" * 50)
    test_tables_exist()
    test_seed_data()
    test_query_by_station()
    test_query_victoria_park()
    print("=" * 50)
    print("All tests complete")
