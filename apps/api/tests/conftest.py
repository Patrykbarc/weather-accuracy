"""Test fixtures.

DATABASE_URL is set before anything from `api` is imported at runtime, because
`api.db.engine` builds its engine at import time from the settings. Runtime
imports of application code therefore happen inside fixtures. The TYPE_CHECKING
imports below never execute, so they are safe at module level.
"""

import os
import tempfile
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterator

    from fastapi.testclient import TestClient
    from sqlmodel import Session

    from api.schemas.schemas import Location

_TMP_DIR = tempfile.TemporaryDirectory()
_DB_PATH = os.path.join(_TMP_DIR.name, "test.db")

os.environ["DATABASE_URL"] = f"sqlite:///{_DB_PATH}"
os.environ["DB_ECHO"] = "false"


@pytest.fixture(scope="session", autouse=True)
def _migrated_database() -> Iterator[None]:
    """Build the schema the way production does, with Alembic.

    SQLModel.metadata.create_all() would be faster but would not create the
    forecast_error view, which only exists as a migration.
    """
    from pathlib import Path

    from alembic import command
    from alembic.config import Config

    command.upgrade(Config(str(Path(__file__).parent.parent / "alembic.ini")), "head")

    yield

    _TMP_DIR.cleanup()


@pytest.fixture
def session() -> Iterator[Session]:
    """A session whose writes are wiped afterwards, so test order never matters."""
    from sqlmodel import Session, SQLModel

    from api.db.engine import engine

    with Session(engine) as s:
        yield s

    with Session(engine) as cleanup:
        for table in reversed(SQLModel.metadata.sorted_tables):
            cleanup.execute(table.delete())
        cleanup.commit()


@pytest.fixture
def client() -> Iterator[TestClient]:
    """FastAPI test client, wired to the same temporary database."""
    from fastapi.testclient import TestClient

    from api.web.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def location(session: Session) -> Location:
    """One saved location, for tests that need something to hang rows off."""
    from api.schemas.schemas import Location

    loc = Location(name="Test", slug="test", latitude=50.0, longitude=21.0)
    session.add(loc)
    session.commit()
    session.refresh(loc)
    return loc


@pytest.fixture
def forecast_pair(session: Session, location: Location) -> None:
    """One forecast that met its measurement.

    Issued two days before the day it describes and 1.5 degrees too warm, so the
    view yields lead_time 2 with a temp_max_error of 1.5. Committed rather than
    left pending, because the API reads through a session of its own.
    """
    from datetime import date

    from api.schemas.schemas import Forecast, Observation

    target = date(2026, 8, 20)

    session.add(
        Forecast(
            location_id=location.id,
            target_date=target,
            fetched_at=date(2026, 8, 18),
            temp_max=25.0,
            temp_min=None,
            precipitation=None,
            wind_gusts=None,
        )
    )
    session.add(
        Observation(
            location_id=location.id,
            measured_at=target,
            temp_max=23.5,
            temp_min=None,
            precipitation=None,
            wind_gusts=None,
        )
    )
    session.commit()
