import httpx
from pydantic import BaseModel

from schemas import ForecastResp

type Params = dict[str, str | int | float]

URL = {
    "forecast": "https://api.open-meteo.com/v1/forecast",
    "archive": "https://archive-api.open-meteo.com/v1/archive",
}


def get_open_meteo[T: BaseModel](url: str, params: Params, model: type[T]) -> T:
    resp = httpx.get(url, params=params)
    resp.raise_for_status()
    return model.model_validate(resp.json())


def fetch_forecast(lat: float, long: float) -> ForecastResp:
    params: Params = {
        "latitude": lat,
        "longitude": long,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_gusts_10m_max",  # noqa: E501
        "timezone": "Europe/Warsaw",
        "forecast_days": 16,
    }

    return get_open_meteo(URL["forecast"], params, model=ForecastResp)
