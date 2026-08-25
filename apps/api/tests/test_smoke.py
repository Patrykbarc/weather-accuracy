"""One worked example per fixture, so the harness itself is proven.

Delete these once the real test files cover the same ground.
"""

from typing import TYPE_CHECKING

from sqlalchemy import text

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from sqlmodel import Session

    from api.schemas.schemas import Location


def test_migrations_created_the_view(session: Session) -> None:
    views = session.execute(
        text("SELECT name FROM sqlite_master WHERE type = 'view'")
    ).scalars()
    assert "forecast_error" in list(views)


def test_location_fixture_is_saved(location: Location) -> None:
    assert location.id is not None
    assert location.slug == "rzeszow"


def test_view_computes_lead_time_and_error(
    session: Session, forecast_pair: None
) -> None:
    lead_time, error = session.execute(
        text("SELECT lead_time, temp_max_error FROM forecast_error")
    ).one()

    assert lead_time == 2
    assert error == 1.5


def test_endpoint_rejects_an_unknown_metric(client: TestClient) -> None:
    response = client.get("/api/analytics", params={"metric": "pressure"})
    assert response.status_code == 422
