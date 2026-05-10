from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DB_DIR = Path("/app/localdb") if Path("/app/localdb").exists() else DATA_DIR
DB_DIR.mkdir(exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_DIR / 'workflow.db'}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def create_tables() -> None:
    """Create all tables if they don't exist. No-op if already created."""
    # Import all models so Base.metadata knows about them
    import app.executions.models  # noqa: F401
    import app.workflows.models  # noqa: F401
    import app.tools.subway_db_query.models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def seed_train_data() -> None:
    """Load toronto.csv into the train table if it's empty."""
    import csv

    from app.tools.subway_db_query.models import Train

    db = SessionLocal()
    try:
        if db.query(Train).first() is not None:
            return  # already seeded

        csv_path = DATA_DIR / "toronto.csv"
        if not csv_path.exists():
            return

        with open(csv_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            rows = []
            for row in reader:
                rows.append(
                    Train(
                        date=row.get("Date", "").strip(),
                        time=row.get("Time", "").strip(),
                        day=row.get("Day", "").strip(),
                        station=row.get("Station", "").strip(),
                        code=row.get("Code", "").strip(),
                        min_delay=int(row.get("Min Delay", 0) or 0),
                        min_gap=int(row.get("Min Gap", 0) or 0),
                        bound=row.get("Bound", "").strip(),
                        line=row.get("Line", "").strip(),
                        vehicle=row.get("Vehicle", "").strip(),
                    )
                )
            db.add_all(rows)
            db.commit()
    finally:
        db.close()


def get_db():
    """FastAPI dependency — yields a DB session, closes after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_workflows() -> None:
    """Insert demo workflow if the workflows table is empty."""
    import json

    from app.workflows.models import Workflow

    db = SessionLocal()
    try:
        if db.query(Workflow).first() is not None:
            return  # already seeded

        demo_nodes = [
            {
                "id": "input-001",
                "type": "input",
                "order": 1,
                "config": {
                    "variables": [{"name": "station_name", "value": "VICTORIA PARK STATION"}]
                },
            },
            {
                "id": "tool-001",
                "type": "tool",
                "order": 2,
                "config": {
                    "tool_name": "query_subway_db",
                    "inputs": {"station": "{{station_name}}"},
                    "output_variable": "query_subway_db_result",
                },
            },
            {
                "id": "prompt-001",
                "type": "prompt",
                "order": 3,
                "config": {
                    "template": "What are the days that {{station_name}} faced delay?\n\n{{query_subway_db_result}}"
                },
            },
        ]

        workflow = Workflow(
            id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            name="Subway Delay Analysis",
            nodes_json=json.dumps(demo_nodes),
        )
        db.add(workflow)
        db.commit()
    finally:
        db.close()
