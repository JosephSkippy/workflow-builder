import json

from sqlalchemy.orm import Session

from app.tools.base import BaseTool
from app.tools.subway_db_query.queries import get_average_delay_by_station


class AverageDelayTool(BaseTool):
    def run(self, inputs: dict[str, str], db: Session) -> str:
        station = inputs["station"]
        avg = get_average_delay_by_station(db, station)
        if avg is None:
            return json.dumps({"station": station.upper(), "average_delay_minutes": None, "message": "No records found"})
        return json.dumps({"station": station.upper(), "average_delay_minutes": round(avg, 2)})
