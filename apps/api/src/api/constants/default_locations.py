from typing import Literal, NamedTuple


class LocationSeed(NamedTuple):
    name: LOCATION_NAMES
    slug: LOCATION_SLUGS
    latitude: float
    longitude: float


LOCATION_NAMES = Literal["Rzeszów", "Zakopane", "Sopot", "Suwałki"]
LOCATION_SLUGS = Literal["rzeszow", "zakopane", "sopot", "suwalki"]


DEFAULT_LOCATIONS = [
    LocationSeed("Rzeszów", "rzeszow", 50.04, 21.99),
    LocationSeed("Zakopane", "zakopane", 49.30, 19.95),
    LocationSeed("Sopot", "sopot", 54.44, 18.56),
    LocationSeed("Suwałki", "suwalki", 54.10, 22.93),
]
