from datetime import date, datetime
from typing import TYPE_CHECKING

import httpx
from sqlmodel import Session

from api.clients.open_meteo import fetch_forecast, fetch_observations
from api.constants import DEFAULT_LOCATIONS, LocationSeed
from api.db import engine
from api.db.crud import create_observations, get_or_create_locations, set_new_forecasts
from api.schemas import Forecast
from api.schemas.schemas import Observation
from api.utils.logger import logger

if TYPE_CHECKING:
    from collections.abc import Sequence

    from api.schemas import Daily


def _has_any_metric(raw: Daily, i: int) -> bool:
    return any(
        metric is not None
        for metric in (
            raw.temperature_2m_max[i],
            raw.temperature_2m_min[i],
            raw.precipitation_sum[i],
            raw.wind_gusts_10m_max[i],
        )
    )


def collect_forecasts(
    seeds: Sequence[LocationSeed] = DEFAULT_LOCATIONS,
) -> list[str]:
    fetched_at = datetime.now().date()
    failed: list[str] = []

    with Session(engine) as session:
        for location in get_or_create_locations(session, seeds):
            try:
                raw = fetch_forecast(location.latitude, location.longitude).daily

                forecasts = [
                    Forecast(
                        location_id=location.id,
                        target_date=date.fromisoformat(day),
                        temp_max=raw.temperature_2m_max[i],
                        temp_min=raw.temperature_2m_min[i],
                        precipitation=raw.precipitation_sum[i],
                        wind_gusts=raw.wind_gusts_10m_max[i],
                        fetched_at=fetched_at,
                    )
                    for i, day in enumerate(raw.time)
                    if _has_any_metric(raw, i)
                ]

                set_new_forecasts(session, location.id, fetched_at, forecasts)
            except httpx.HTTPError:
                logger.exception(f"Failed to collect forecasts for {location.name}")
                session.rollback()
                failed.append(location.name)

    return failed


def collect_observations(
    seeds: Sequence[LocationSeed] = DEFAULT_LOCATIONS, days_back: int = 7
) -> list[str]:
    failed: list[str] = []

    with Session(engine) as session:
        for location in get_or_create_locations(session, seeds):
            try:
                raw = fetch_observations(
                    location.latitude, location.longitude, days_back
                ).daily

                observations = [
                    Observation(
                        location_id=location.id,
                        measured_at=date.fromisoformat(day),
                        temp_max=raw.temperature_2m_max[i],
                        temp_min=raw.temperature_2m_min[i],
                        precipitation=raw.precipitation_sum[i],
                        wind_gusts=raw.wind_gusts_10m_max[i],
                    )
                    for i, day in enumerate(raw.time)
                    if _has_any_metric(raw, i)
                ]

                create_observations(session, location.id, observations)
            except httpx.HTTPError:
                logger.exception(f"Failed to collect observations for {location.name}")
                session.rollback()
                failed.append(location.name)

    return failed
