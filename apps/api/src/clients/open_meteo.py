from datetime import datetime, timedelta
from enum import StrEnum

import httpx

from schemas import OpenMeteoResponse

type Params = dict[str, str | int | float]


class Endpoint(StrEnum):
    FORECAST = "https://api.open-meteo.com/v1/forecast"
    ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"
    HISTORICAL = "https://historical-forecast-api.open-meteo.com/v1/forecast"


_COMMON_PARAMS = {
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_gusts_10m_max",  # noqa: E501
    "timezone": "Europe/Warsaw",
}


def _get_date_delta(delta: int) -> str:
    return ((datetime.now().date()) - timedelta(days=delta)).isoformat()


def _fetch_open_meteo(
    endpoint: Endpoint,
    lat: float,
    long: float,
    **extra_params: str | int,
) -> OpenMeteoResponse:
    params: Params = {
        "latitude": lat,
        "longitude": long,
        **_COMMON_PARAMS,
        **extra_params,
    }

    resp = httpx.get(endpoint, params=params, timeout=30)
    resp.raise_for_status()
    return OpenMeteoResponse.model_validate(resp.json())


def fetch_forecast(lat: float, long: float, days: int = 16) -> OpenMeteoResponse:
    return _fetch_open_meteo(Endpoint.FORECAST, lat, long, forecast_days=days)


def fetch_observations(
    lat: float, long: float, days_back: int = 7
) -> OpenMeteoResponse:
    return _fetch_open_meteo(
        Endpoint.ARCHIVE,
        lat,
        long,
        start_date=_get_date_delta(days_back),
        end_date=_get_date_delta(1),
    )
