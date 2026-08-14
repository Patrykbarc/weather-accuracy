from typing import TYPE_CHECKING

from sqlmodel import Session, col, select

from api.constants import DEFAULT_LOCATIONS, LocationSeed
from api.schemas import Forecast, Location
from api.schemas.schemas import Observation
from api.utils.logger import logger

if TYPE_CHECKING:
    from collections.abc import Sequence
    from datetime import date


def get_or_create_locations(
    session: Session, seeds: Sequence[LocationSeed] = DEFAULT_LOCATIONS
) -> list[Location]:
    stored = {
        (location.latitude, location.longitude): location
        for location in session.exec(select(Location)).all()
    }

    missing = [seed for seed in seeds if (seed.latitude, seed.longitude) not in stored]

    if missing:
        created = [
            Location(
                name=seed.name,
                slug=seed.slug,
                latitude=seed.latitude,
                longitude=seed.longitude,
            )
            for seed in missing
        ]
        session.add_all(created)
        session.commit()

        for location in created:
            session.refresh(location)
            stored[(location.latitude, location.longitude)] = location

        logger.info(f"Created locations: {[location.name for location in created]}")

    return [stored[(seed.latitude, seed.longitude)] for seed in seeds]


def set_new_forecasts(
    session: Session,
    location_id: int | None,
    fetched_at: date,
    forecasts: list[Forecast],
) -> None:
    statement = select(Forecast).where(
        Forecast.location_id == location_id, Forecast.fetched_at == fetched_at
    )
    result = session.exec(statement).first()

    if result is not None:
        logger.warning(
            f"Forecasts for location {location_id} at {fetched_at} already exist. "
            "Skipping."
        )
        return

    session.add_all(forecasts)
    session.commit()


def create_observations(
    session: Session, location_id: int | None, observations: list[Observation]
) -> None:
    dates = [o.measured_at for o in observations]

    statement = select(Observation).where(
        Observation.location_id == location_id,
        col(Observation.measured_at).in_(dates),
    )
    existing = {o.measured_at for o in session.exec(statement).all()}

    new = [o for o in observations if o.measured_at not in existing]

    if not new:
        logger.warning(
            f"All observations for location {location_id} already exist. Skipping."
        )
        return

    session.add_all(new)
    session.commit()
