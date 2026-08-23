import pytest

from api.jobs.handlers import _has_any_metric
from api.schemas import Daily

Day = tuple[str, float | None, float | None, float | None, float | None]


@pytest.mark.parametrize(
    ("metrics", "expected"),
    [
        ((25.0, 14.0, 0.0, 30.0), True),
        ((25.0, None, None, None), True),
        ((None, None, None, None), False),
    ],
    ids=["all metrics", "only one metric", "nothing at all"],
)
def test_has_any_metric(metrics: tuple[float | None, ...], expected: bool) -> None:
    temp_max, temp_min, precip, wind = metrics

    raw = Daily(
        time=["2026-08-20"],
        temperature_2m_max=[temp_max],
        temperature_2m_min=[temp_min],
        precipitation_sum=[precip],
        wind_gusts_10m_max=[wind],
    )

    assert _has_any_metric(raw, 0) is expected


@pytest.mark.parametrize(
    ("days", "expected"),
    [
        (
            (
                ("2026-08-20", 25.0, 14.0, 0.0, 30.0),
                ("2026-08-21", None, None, None, None),
            ),
            (True, False),
        ),
        (
            (
                ("2026-08-20", None, None, None, None),
                ("2026-08-21", 25.0, None, None, None),
            ),
            (False, True),
        ),
    ],
    ids=["metrics on the first day", "metrics on the second day"],
)
def test_has_any_metric_reads_the_right_day(
    days: tuple[Day, Day], expected: tuple[bool, bool]
) -> None:
    day_1, day_2 = days

    _, day_1_temp_max, day_1_temp_min, day_1_precip_sum, day_1_wind_gusts = day_1
    _, day_2_temp_max, day_2_temp_min, day_2_precip_sum, day_2_wind_gusts = day_2

    raw = Daily(
        time=[day_1[0], day_2[0]],
        temperature_2m_max=[day_1_temp_max, day_2_temp_max],
        temperature_2m_min=[day_1_temp_min, day_2_temp_min],
        precipitation_sum=[day_1_precip_sum, day_2_precip_sum],
        wind_gusts_10m_max=[day_1_wind_gusts, day_2_wind_gusts],
    )

    for day_index, has_metric in enumerate(expected):
        assert _has_any_metric(raw, day_index) is has_metric
