import os
import shutil
import tempfile
from pathlib import Path

_TMP_DIR = tempfile.mkdtemp(prefix="weather-accuracy-tests-")
os.environ["DATABASE_URL"] = f"sqlite:///{_TMP_DIR}/test.db"

from datetime import date  # noqa: E402
from typing import TYPE_CHECKING  # noqa: E402

import pytest  # noqa: E402
from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlmodel import Session  # noqa: E402

from api.db import engine  # noqa: E402
from api.schemas.schemas import Forecast, Location, Observation  # noqa: E402
from api.web.main import app  # noqa: E402

if TYPE_CHECKING:
    from collections.abc import Iterator

API_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", autouse=True)
def migrated_db() -> Iterator[None]:
    """Build the schema the same way production does, view included."""
    config = Config(API_ROOT / "alembic.ini")
    config.set_main_option("script_location", str(API_ROOT / "migrations"))
    command.upgrade(config, "head")

    yield

    engine.dispose()
    shutil.rmtree(_TMP_DIR, ignore_errors=True)


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def session() -> Iterator[Session]:
    with Session(engine) as db_session:
        yield db_session


@pytest.fixture
def forecast_pair(session: Session) -> None:
    """One location with a forecast two days out and what actually happened.

    Forecast said 20.0, reality was 18.5, so the error is +1.5 at lead time 2.
    """
    location = Location(name="Rzeszów", slug="rzeszow", latitude=50.04, longitude=21.99)
    session.add(location)
    session.commit()
    session.refresh(location)

    session.add(
        Forecast(
            location_id=location.id,
            target_date=date(2026, 8, 3),
            fetched_at=date(2026, 8, 1),
            temp_max=20.0,
            temp_min=10.0,
            precipitation=0.0,
            wind_gusts=15.0,
        )
    )
    session.add(
        Observation(
            location_id=location.id,
            measured_at=date(2026, 8, 3),
            temp_max=18.5,
            temp_min=9.0,
            precipitation=0.0,
            wind_gusts=12.0,
        )
    )
    session.commit()
