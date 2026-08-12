import sys
from typing import TYPE_CHECKING

from api.constants.default_locations import DEFAULT_LOCATIONS
from api.jobs.handlers import collect_observations
from api.utils.logger import logger

if TYPE_CHECKING:
    from collections.abc import Sequence

    from api.constants.default_locations import LocationSeed

BACKFILL_DAYS = 60


def run_backfill(seeds: Sequence[LocationSeed] = DEFAULT_LOCATIONS) -> list[str]:
    return collect_observations(seeds, days_back=BACKFILL_DAYS)


if __name__ == "__main__":
    failed = run_backfill()

    if failed:
        logger.error(f"Backfill finished with failures: {sorted(set(failed))}")
        sys.exit(1)
