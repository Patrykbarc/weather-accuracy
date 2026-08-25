from datetime import date
from typing import TYPE_CHECKING

from sqlmodel import select

from api.constants import LocationSeed
from api.db.crud import create_observations, get_or_create_locations, set_new_forecasts
from api.schemas.schemas import Forecast, Location, Observation

if TYPE_CHECKING:
    from sqlmodel import Session

SEEDS = [
    LocationSeed("Rzeszów", "rzeszow", 50.04, 21.99),
    LocationSeed("Zakopane", "zakopane", 49.30, 19.95),
]


STORED_TEMP = 22.0
RESENT_TEMP = 99.0

DEFAULT_TEMP_MAX = 22.0


def test_get_or_create_locations_creates_missing_rows(session: Session) -> None:
    created = get_or_create_locations(session, SEEDS)

    assert [location.name for location in created] == ["Rzeszów", "Zakopane"]
    assert all(location.id is not None for location in created)
    assert len(session.exec(select(Location)).all()) == 2


def test_get_or_create_locations_is_idempotent(session: Session) -> None:
    first = get_or_create_locations(session, SEEDS)
    second = get_or_create_locations(session, SEEDS)

    assert [location.id for location in first] == [location.id for location in second]
    assert len(session.exec(select(Location)).all()) == 2


def test_get_or_create_locations_only_adds_the_new_seed(session: Session) -> None:
    get_or_create_locations(session, SEEDS[:1])

    returned = get_or_create_locations(session, SEEDS)

    assert [location.slug for location in returned] == ["rzeszow", "zakopane"]
    assert len(session.exec(select(Location)).all()) == 2


def test_get_or_create_locations_returns_seed_order(session: Session) -> None:
    get_or_create_locations(session, SEEDS)

    returned = get_or_create_locations(session, list(reversed(SEEDS)))

    assert [location.slug for location in returned] == ["zakopane", "rzeszow"]


def test_set_new_forecasts_stores_the_batch(
    session: Session, location: Location
) -> None:
    fetched_at = date(2026, 8, 18)
    forecasts = [
        _forecast(location.id, date(2026, 8, 19), fetched_at, temp_max=24.0),
        _forecast(location.id, date(2026, 8, 20), fetched_at, temp_max=25.0),
    ]

    set_new_forecasts(session, location.id, fetched_at, forecasts)

    stored = session.exec(select(Forecast)).all()
    assert len(stored) == 2
    assert {f.temp_max for f in stored} == {24.0, 25.0}


def test_set_new_forecasts_skips_a_repeated_fetch(
    session: Session, location: Location
) -> None:
    fetched_at = date(2026, 8, 18)
    set_new_forecasts(
        session,
        location.id,
        fetched_at,
        [_forecast(location.id, date(2026, 8, 19), fetched_at, temp_max=24.0)],
    )

    set_new_forecasts(
        session,
        location.id,
        fetched_at,
        [_forecast(location.id, date(2026, 8, 20), fetched_at, temp_max=25.0)],
    )

    stored = session.exec(select(Forecast)).all()
    assert len(stored) == 1
    assert stored[0].target_date == date(2026, 8, 19)


def test_set_new_forecasts_accepts_a_later_fetch(
    session: Session, location: Location
) -> None:
    set_new_forecasts(
        session,
        location.id,
        date(2026, 8, 18),
        [_forecast(location.id, date(2026, 8, 20), date(2026, 8, 18), temp_max=24.0)],
    )

    set_new_forecasts(
        session,
        location.id,
        date(2026, 8, 19),
        [_forecast(location.id, date(2026, 8, 20), date(2026, 8, 19), temp_max=25.0)],
    )

    stored = session.exec(select(Forecast)).all()
    assert len(stored) == 2
    assert {f.fetched_at for f in stored} == {date(2026, 8, 18), date(2026, 8, 19)}


def test_set_new_forecasts_keeps_locations_apart(session: Session) -> None:
    first, second = get_or_create_locations(session, SEEDS)
    fetched_at = date(2026, 8, 18)

    set_new_forecasts(
        session,
        first.id,
        fetched_at,
        [_forecast(first.id, date(2026, 8, 20), fetched_at, temp_max=24.0)],
    )
    set_new_forecasts(
        session,
        second.id,
        fetched_at,
        [_forecast(second.id, date(2026, 8, 20), fetched_at, temp_max=18.0)],
    )

    stored = session.exec(select(Forecast)).all()
    assert {f.location_id for f in stored} == {first.id, second.id}


def test_create_observations_stores_the_batch(
    session: Session, location: Location
) -> None:
    observations = [
        _observation(location.id, date(2026, 8, 19), temp_max=22.0),
        _observation(location.id, date(2026, 8, 20), temp_max=23.5),
    ]

    create_observations(session, location.id, observations)

    stored = session.exec(select(Observation)).all()
    assert len(stored) == 2
    assert {o.measured_at for o in stored} == {date(2026, 8, 19), date(2026, 8, 20)}


def test_create_observations_adds_only_the_unseen_days(
    session: Session, location: Location
) -> None:
    create_observations(
        session,
        location.id,
        [_observation(location.id, date(2026, 8, 19), temp_max=STORED_TEMP)],
    )

    create_observations(
        session,
        location.id,
        [
            _observation(location.id, date(2026, 8, 19), temp_max=RESENT_TEMP),
            _observation(location.id, date(2026, 8, 20), temp_max=23.5),
        ],
    )

    stored = session.exec(select(Observation)).all()
    assert len(stored) == 2
    by_date = {o.measured_at: o.temp_max for o in stored}
    assert by_date[date(2026, 8, 19)] == STORED_TEMP
    assert by_date[date(2026, 8, 20)] == 23.5


def test_create_observations_skips_a_fully_known_batch(
    session: Session, location: Location
) -> None:
    days = [
        _observation(location.id, date(2026, 8, 19)),
        _observation(location.id, date(2026, 8, 20)),
    ]
    create_observations(session, location.id, days)

    create_observations(
        session,
        location.id,
        [
            _observation(location.id, date(2026, 8, 19)),
            _observation(location.id, date(2026, 8, 20)),
        ],
    )

    assert len(session.exec(select(Observation)).all()) == 2


def test_create_observations_keeps_locations_apart(session: Session) -> None:
    first, second = get_or_create_locations(session, SEEDS)
    day = date(2026, 8, 20)

    create_observations(session, first.id, [_observation(first.id, day, temp_max=22.0)])
    create_observations(
        session, second.id, [_observation(second.id, day, temp_max=15.0)]
    )

    stored = session.exec(select(Observation)).all()
    assert len(stored) == 2
    assert {o.location_id for o in stored} == {first.id, second.id}


def test_create_observations_handles_an_empty_batch(
    session: Session, location: Location
) -> None:
    create_observations(session, location.id, [])

    assert session.exec(select(Observation)).all() == []


def _forecast(
    location_id: int | None,
    target_date: date,
    fetched_at: date,
    temp_max: float | None = 25.0,
) -> Forecast:
    return Forecast(
        location_id=location_id,
        target_date=target_date,
        fetched_at=fetched_at,
        temp_max=temp_max,
        temp_min=None,
        precipitation=None,
        wind_gusts=None,
    )


def _observation(
    location_id: int | None,
    measured_at: date,
    temp_max: float | None = DEFAULT_TEMP_MAX,
) -> Observation:
    return Observation(
        location_id=location_id,
        measured_at=measured_at,
        temp_max=temp_max,
        temp_min=None,
        precipitation=None,
        wind_gusts=None,
    )
