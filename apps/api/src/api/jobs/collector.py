import sys
from typing import TYPE_CHECKING

from api.constants.default_locations import DEFAULT_LOCATIONS
from api.jobs.handlers import collect_forecasts, collect_observations
from api.utils.logger import logger

if TYPE_CHECKING:
    from collections.abc import Sequence

    from api.constants.default_locations import LocationSeed


def run_collector(seeds: Sequence[LocationSeed] = DEFAULT_LOCATIONS) -> list[str]:
    return collect_forecasts(seeds) + collect_observations(seeds)


if __name__ == "__main__":
    failed = run_collector()

    if failed:
        logger.error(f"Collector finished with failures: {sorted(set(failed))}")
        sys.exit(1)
