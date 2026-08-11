from typing import TYPE_CHECKING

from sqlmodel import Session, col, select

from schemas import Forecast, Location
from schemas.schemas import Observation
from utils.logger import logger

if TYPE_CHECKING:
    from datetime import date


def get_or_create_location(session: Session, lat: float, long: float) -> Location:
    statement = select(Location).where(
        Location.latitude == lat, Location.longitude == long
    )
    location = session.exec(statement).first()

    if location is None:
        new_location = Location(
            name="Rzeszów",
            longitude=long,
            latitude=lat,
        )
        session.add(new_location)
        session.commit()
        session.refresh(new_location)

        return new_location
    return location


def set_new_forecasts(
    session: Session, fetched_at: date, forecasts: list[Forecast]
) -> None:
    statement = select(Forecast).where(Forecast.fetched_at == fetched_at)
    result = session.exec(statement).first()

    if result is not None:
        logger.warning(f"Forecasts for {fetched_at} already exist. Skipping.")
        return

    session.add_all(forecasts)
    session.commit()


def create_observations(session: Session, observations: list[Observation]) -> None:
    dates = [o.measured_at for o in observations]

    statement = select(Observation).where(col(Observation.measured_at).in_(dates))
    existing = {o.measured_at for o in session.exec(statement).all()}

    new = [o for o in observations if o.measured_at not in existing]

    if not new:
        logger.warning("All observations already exist. Skipping.")
        return

    session.add_all(new)
    session.commit()
