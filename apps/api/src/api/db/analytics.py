from typing import Literal

from pydantic import BaseModel
from sqlalchemy import text
from sqlmodel import Session

from api.db.engine import engine

type Metric = Literal["temp_max", "temp_min", "precipitation", "wind_gusts"]

_ERROR_COLUMN_WHITELIST: dict[Metric, str] = {
    "temp_max": "temp_max_error",
    "temp_min": "temp_min_error",
    "precipitation": "precipitation_error",
    "wind_gusts": "wind_gusts_error",
}


class AccuracyByLeadTime(BaseModel):
    lead_time: int
    samples: int
    bias: float | None
    mae: float | None


def get_accuracy_by_lead_time(
    session: Session, metric: Metric
) -> list[AccuracyByLeadTime]:
    if metric not in _ERROR_COLUMN_WHITELIST:
        raise ValueError(
            f"Invalid metric '{metric}'. Allowed: {set(_ERROR_COLUMN_WHITELIST)}"
        )

    col = _ERROR_COLUMN_WHITELIST[metric]

    statement = f"""
        SELECT
            fe.lead_time,
            COUNT(fe.{col}) AS samples,
            ROUND(AVG(fe.{col}), 2) AS bias,
            ROUND(AVG(ABS(fe.{col})), 2) AS mae
        FROM forecast_error fe
        GROUP BY fe.lead_time
    """

    results = session.execute(text(statement)).mappings()
    return [AccuracyByLeadTime.model_validate(row) for row in results]


if __name__ == "__main__":
    with Session(engine) as session:
        resp = get_accuracy_by_lead_time(session, metric="temp_max")
        print(resp)
