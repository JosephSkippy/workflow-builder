import json

from sqlalchemy.orm import Session

from app.tools.base import BaseTool
from app.tools.subway_db_query.queries import get_delays_by_station


class SubwayDbQueryTool(BaseTool):
    def run(self, inputs: dict[str, str], db: Session) -> str:
        station = inputs["station"]
        rows = get_delays_by_station(db, station)
        results = [
            {
                "date": r.date,
                "time": r.time,
                "day": r.day,
                "station": r.station,
                "code": r.code,
                "min_delay": r.min_delay,
                "min_gap": r.min_gap,
                "bound": r.bound,
                "line": r.line,
                "vehicle": r.vehicle,
            }
            for r in rows
        ]
        return json.dumps(
            {"station": station.upper(), "total_records": len(results), "delays": results}
        )
