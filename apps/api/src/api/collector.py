from datetime import date, datetime

import httpx
from sqlmodel import Session, select

from api.db import engine
from schemas import Forecast, ForecastResp, Location
from utils.logger import logger


def handle_forecasts(lat: float = 50.04, long: float = 21.99) -> None:
    raw_forecasts = _fetch_forecast(lat, long)

    daily = raw_forecasts.daily

    days = daily.time
    max_temps = daily.temperature_2m_max
    min_temps = daily.temperature_2m_min
    precipitation = daily.precipitation_sum
    wind_gusts = daily.wind_gusts_10m_max
    fetched_at = datetime.now().date()

    with Session(engine) as session:
        location = _get_or_create_location(session, lat, long)

        forecasts = [
            Forecast(
                location_id=location.id,
                target_date=datetime.fromisoformat(day),
                temp_max=max_temps[i],
                temp_min=min_temps[i],
                precipitation=precipitation[i],
                wind_gusts=wind_gusts[i],
                fetched_at=fetched_at,
            )
            for i, day in enumerate(days)
        ]

        _set_new_forecasts(session, fetched_at, forecasts)


def _fetch_forecast(lat: float, long: float) -> ForecastResp:
    url = "https://api.open-meteo.com/v1/forecast"

    params: dict[str, str | int | float] = {
        "latitude": lat,
        "longitude": long,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_gusts_10m_max",  # noqa: E501
        "timezone": "Europe/Warsaw",
        "forecast_days": 16,
    }

    resp = httpx.get(url, params=params)
    resp.raise_for_status()

    return ForecastResp.model_validate(resp.json())


def _get_or_create_location(session: Session, lat: float, long: float) -> Location:
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


def _set_new_forecasts(
    session: Session, fetched_at: date, forecasts: list[Forecast]
) -> None:
    statement = select(Forecast).where(Forecast.fetched_at == fetched_at)
    result = session.exec(statement).first()

    if result is not None:
        logger.warning(f"Forecasts for {fetched_at} already exist. Skipping.")
        return

    session.add_all(forecasts)
    session.commit()


if __name__ == "__main__":
    handle_forecasts()
