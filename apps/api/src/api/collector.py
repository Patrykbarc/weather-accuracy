from datetime import datetime

from sqlmodel import Session

from api.crud import get_or_create_location, set_new_forecasts, set_new_observation
from api.db import engine
from clients.open_meteo import fetch_forecast, fetch_observations
from schemas import Forecast
from schemas.schemas import Observation


def handle_forecasts(lat: float = 50.04, long: float = 21.99) -> None:
    raw_forecasts = fetch_forecast(lat, long).daily
    raw_observation = fetch_observations(lat, long).daily

    fetched_at = datetime.now().date()

    with Session(engine) as session:
        location = get_or_create_location(session, lat, long)

        forecasts = [
            Forecast(
                location_id=location.id,
                target_date=datetime.fromisoformat(day),
                temp_max=raw_forecasts.temperature_2m_max[i],
                temp_min=raw_forecasts.temperature_2m_min[i],
                precipitation=raw_forecasts.precipitation_sum[i],
                wind_gusts=raw_forecasts.wind_gusts_10m_max[i],
                fetched_at=fetched_at,
            )
            for i, day in enumerate(raw_forecasts.time)
        ]

        observation = Observation(
            location_id=location.id,
            measured_at=datetime.fromisoformat(raw_observation.time[0]),
            temp_max=raw_observation.temperature_2m_max[0],
            temp_min=raw_observation.temperature_2m_min[0],
            precipitation=raw_observation.precipitation_sum[0],
            wind_gusts=raw_observation.wind_gusts_10m_max[0],
        )

        set_new_forecasts(session, fetched_at, forecasts)
        set_new_observation(session, fetched_at, observation)


if __name__ == "__main__":
    handle_forecasts()
