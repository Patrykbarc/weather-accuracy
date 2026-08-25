from typing import TYPE_CHECKING

import pytest

from api.db.analytics import get_accuracy_by_lead_time

if TYPE_CHECKING:
    from fastapi.testclient import TestClient
    from sqlmodel import Session


def test_analytics_reports_error_at_lead_time(
    client: TestClient, forecast_pair: None
) -> None:
    response = client.get("/api/analytics", params={"metric": "temp_max"})

    assert response.status_code == 200
    assert response.json() == [{"lead_time": 2, "samples": 1, "bias": 1.5, "mae": 1.5}]


@pytest.mark.parametrize(
    ("kwargs", "rejected"),
    [
        ({"metric": "pressure"}, "pressure"),
        ({"metric": "temp_max; DROP TABLE forecast"}, "DROP TABLE"),
        ({"metric": "temp_max", "slug": "krakow"}, "krakow"),
    ],
    ids=["unknown metric", "sql in the metric", "unknown slug"],
)
def test_rejects_values_outside_the_whitelist(
    session: Session, kwargs: dict[str, str], rejected: str
) -> None:
    """The metric picks a column name, so it never reaches SQL unchecked."""
    with pytest.raises(ValueError, match=rejected):
        get_accuracy_by_lead_time(session, **kwargs)  # type: ignore[arg-type]


def test_accepts_a_known_slug(session: Session, forecast_pair: None) -> None:
    rows = get_accuracy_by_lead_time(session, metric="temp_max", slug="rzeszow")

    assert [row.lead_time for row in rows] == [2]


def test_filters_out_other_locations(session: Session, forecast_pair: None) -> None:
    rows = get_accuracy_by_lead_time(session, metric="temp_max", slug="zakopane")

    assert rows == []
