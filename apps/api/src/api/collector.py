from datetime import datetime
from pprint import pprint

import httpx

from schemas import Forecast, ForecastResp


def fetch_forecast(lat: float, long: float) -> ForecastResp:
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


def handle_forecasts() -> None:
    raw_forecasts = fetch_forecast(lat=50.04, long=21.99)

    daily = raw_forecasts.daily

    days = daily.time
    max_temps = daily.temperature_2m_max
    min_temps = daily.temperature_2m_min
    precipitation = daily.precipitation_sum
    wind_gusts = daily.wind_gusts_10m_max
    fetched_at = datetime.now()

    forecasts = []

    for i, day in enumerate(days):
        forecasts.append(
            Forecast(
                target_date=datetime.fromisoformat(day),
                temp_max=max_temps[i],
                temp_min=min_temps[i],
                precipitation=precipitation[i],
                wind_gusts=wind_gusts[i],
                fetched_at=fetched_at,
            )
        )

    pprint(forecasts, indent=2)


if __name__ == "__main__":
    handle_forecasts()
