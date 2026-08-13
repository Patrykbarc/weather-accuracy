from typing import NamedTuple


class LocationSeed(NamedTuple):
    name: str
    latitude: float
    longitude: float


DEFAULT_LOCATIONS = [
    LocationSeed("Rzeszów", 50.04, 21.99),
    LocationSeed("Zakopane", 49.30, 19.95),
    LocationSeed("Sopot", 54.44, 18.56),
    LocationSeed("Suwałki", 54.10, 22.93),
]
