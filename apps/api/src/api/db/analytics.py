from typing import Any, Literal, get_args

from pydantic import BaseModel
from sqlalchemy import text
from sqlmodel import Session

from api.constants import LOCATION_SLUGS
from api.db import engine

type Metric = Literal["temp_max", "temp_min", "precipitation", "wind_gusts"]

_ERROR_COLUMN_WHITELIST: dict[Metric, str] = {
    "temp_max": "temp_max_error",
    "temp_min": "temp_min_error",
    "precipitation": "precipitation_error",
    "wind_gusts": "wind_gusts_error",
}

ALLOWED_METRICS = set(_ERROR_COLUMN_WHITELIST.keys())
ALLOWED_SLUGS = set(get_args(LOCATION_SLUGS))


class AccuracyByLeadTime(BaseModel):
    lead_time: int
    samples: int
    bias: float | None
    mae: float | None


def get_accuracy_by_lead_time(
    session: Session, metric: Metric, slug: LOCATION_SLUGS | None = None
) -> list[AccuracyByLeadTime]:

    _validate_allowed(value=metric, collection=ALLOWED_METRICS)

    if slug is not None:
        _validate_allowed(value=slug, collection=ALLOWED_SLUGS)

    col = _ERROR_COLUMN_WHITELIST[metric]

    statement = f"""
        SELECT
            fe.lead_time,
            COUNT(fe.{col}) AS samples,
            ROUND(AVG(fe.{col}), 2) AS bias,
        ROUND(AVG(ABS(fe.{col})), 2) AS mae
        FROM forecast_error fe
        WHERE (:slug IS NULL OR fe.slug = :slug)
        GROUP BY fe.lead_time
    """

    results = session.execute(text(statement), {"slug": slug}).mappings()
    return [AccuracyByLeadTime.model_validate(row) for row in results]


def _validate_allowed(value: Any, collection: set[Any]) -> None:
    if value not in collection:
        raise ValueError(f"Invalid value '{value}'. Allowed: {collection}")


if __name__ == "__main__":
    with Session(engine) as session:
        resp = get_accuracy_by_lead_time(session, metric="temp_max", slug="rzeszow")
        print(resp)
