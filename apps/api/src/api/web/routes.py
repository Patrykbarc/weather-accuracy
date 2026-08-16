from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.constants import LOCATION_SLUGS  # noqa: TC001
from api.db.analytics import (
    AccuracyByLeadTime,
    LastUpdatedAt,
    Metric,
    get_accuracy_by_lead_time,
    get_last_updated,
)

from .deps import get_session

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/analytics")
def read_accuracy(
    session: SessionDep,
    metric: Metric,
    slug: LOCATION_SLUGS | None = None,
) -> list[AccuracyByLeadTime]:
    return get_accuracy_by_lead_time(session, metric, slug)


@router.get("/last-updated")
def read_last_updated(session: SessionDep) -> LastUpdatedAt:
    return get_last_updated(session)
