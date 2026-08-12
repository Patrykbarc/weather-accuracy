from pydantic import BaseModel


class DailyUnits(BaseModel):
    time: str
    temperature_2m_max: str
    temperature_2m_min: str
    precipitation_sum: str
    wind_gusts_10m_max: str


class Daily(BaseModel):
    time: list[str]
    temperature_2m_max: list[float | None]
    temperature_2m_min: list[float | None]
    precipitation_sum: list[float | None]
    wind_gusts_10m_max: list[float | None]


class Location(BaseModel):
    latitude: float
    longitude: float


class OpenMeteoResponse(Location):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    daily_units: DailyUnits
    daily: Daily


class OpenMeteoGeocodingResponse(Location):
    name: str
