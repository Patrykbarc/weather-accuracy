from api.handlers import collect_forecasts, collect_observations
from constants.default_location import DEFAULT_LOCATION


def run_collector(
    lat: float = DEFAULT_LOCATION["lat"], long: float = DEFAULT_LOCATION["long"]
) -> None:
    collect_forecasts(lat, long)
    collect_observations(lat, long)


if __name__ == "__main__":
    run_collector()
