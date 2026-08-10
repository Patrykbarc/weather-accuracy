from datetime import datetime

from sqlmodel import Session

from api.crud import get_or_create_location, set_new_forecasts
from api.db import engine
from clients.get_open_meteo import fetch_forecast
from schemas import Forecast


def handle_forecasts(lat: float = 50.04, long: float = 21.99) -> None:
    raw_forecasts = fetch_forecast(lat, long)

    daily = raw_forecasts.daily
    fetched_at = datetime.now().date()

    with Session(engine) as session:
        location = get_or_create_location(session, lat, long)

        forecasts = [
            Forecast(
                location_id=location.id,
                target_date=datetime.fromisoformat(day),
                temp_max=daily.temperature_2m_max[i],
                temp_min=daily.temperature_2m_min[i],
                precipitation=daily.precipitation_sum[i],
                wind_gusts=daily.wind_gusts_10m_max[i],
                fetched_at=fetched_at,
            )
            for i, day in enumerate(daily.time)
        ]

        set_new_forecasts(session, fetched_at, forecasts)


if __name__ == "__main__":
    handle_forecasts()
