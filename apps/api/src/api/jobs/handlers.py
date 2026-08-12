from datetime import date, datetime

from sqlmodel import Session

from api.clients.open_meteo import fetch_forecast, fetch_observations
from api.db.crud import create_observations, get_or_create_location, set_new_forecasts
from api.db.engine import engine
from api.schemas import Forecast
from api.schemas.schemas import Observation


def collect_forecasts(lat: float, long: float) -> None:
    raw = fetch_forecast(lat, long).daily
    fetched_at = datetime.now().date()

    with Session(engine) as session:
        location = get_or_create_location(session, lat, long)

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
            if None
            not in (
                raw.temperature_2m_max[i],
                raw.temperature_2m_min[i],
                raw.precipitation_sum[i],
                raw.wind_gusts_10m_max[i],
            )
        ]

        set_new_forecasts(session, fetched_at, forecasts)


def collect_observations(lat: float, long: float, days_back: int = 7) -> None:
    raw = fetch_observations(lat, long, days_back).daily

    with Session(engine) as session:
        location = get_or_create_location(session, lat, long)

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
        ]

        create_observations(session, observations)
