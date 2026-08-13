from pydantic import BaseModel
from sqlalchemy import text
from sqlmodel import Session

from api.db.engine import engine


class AccuracyByLeadTime(BaseModel):
    lead_time: int
    samples: int
    bias: float | None
    mae: float | None


def get_accuracy_by_lead_time(session: Session) -> list[AccuracyByLeadTime]:
    statement = """
        SELECT
            fe.lead_time,
            COUNT(fe.temp_max_error) AS samples,
            ROUND(AVG(fe.temp_max_error), 2) AS bias,
            ROUND(AVG(ABS(fe.temp_max_error)), 2) AS mae
        FROM forecast_error fe
        GROUP BY fe.lead_time;
    """

    results = session.execute(text(statement)).mappings()

    return [AccuracyByLeadTime.model_validate(row) for row in results]


if __name__ == "__main__":
    with Session(engine) as session:
        resp = get_accuracy_by_lead_time(session)
        print(resp)
