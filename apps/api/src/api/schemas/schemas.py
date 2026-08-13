from datetime import date
from typing import Annotated

from sqlmodel import Field, SQLModel, UniqueConstraint

PrimaryKey = Annotated[int | None, Field(default=None, primary_key=True)]


class ForecastMetricsBase(SQLModel):
    temp_max: float | None
    temp_min: float | None
    precipitation: float | None
    wind_gusts: float | None


class Location(SQLModel, table=True):
    id: PrimaryKey = None
    name: str
    slug: str = Field(unique=True)
    latitude: float
    longitude: float
    __table_args__ = (UniqueConstraint("latitude", "longitude"),)


class Forecast(ForecastMetricsBase, table=True):
    id: PrimaryKey = None
    location_id: int | None = Field(default=None, foreign_key="location.id")
    target_date: date
    fetched_at: date
    __table_args__ = (UniqueConstraint("location_id", "target_date", "fetched_at"),)


class Observation(ForecastMetricsBase, table=True):
    id: PrimaryKey = None
    location_id: int | None = Field(default=None, foreign_key="location.id")
    measured_at: date
    __table_args__ = (UniqueConstraint("location_id", "measured_at"),)
