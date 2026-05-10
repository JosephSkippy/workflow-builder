from sqlalchemy import func
from sqlalchemy.orm import Session

from app.tools.subway_db_query.models import Train


def get_delays_by_station(db: Session, station: str) -> list[Train]:
    return db.query(Train).filter(Train.station == station.upper()).all()


def get_average_delay_by_station(db: Session, station: str) -> float | None:
    result = (
        db.query(func.avg(Train.min_delay))
        .filter(Train.station == station.upper())
        .scalar()
    )
    return float(result) if result is not None else None
