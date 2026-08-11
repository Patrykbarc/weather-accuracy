from api.handlers import collect_observations
from constants.default_location import DEFAULT_LOCATION

BACKFILL_DAYS = 60


def run_backfill(
    lat: float = DEFAULT_LOCATION["lat"], long: float = DEFAULT_LOCATION["long"]
) -> None:
    collect_observations(lat, long, days_back=BACKFILL_DAYS)


if __name__ == "__main__":
    run_backfill()
