from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


def test_analytics_reports_error_at_lead_time(
    client: TestClient, forecast_pair: None
) -> None:
    response = client.get("/api/analytics", params={"metric": "temp_max"})

    assert response.status_code == 200
    assert response.json() == [{"lead_time": 2, "samples": 1, "bias": 1.5, "mae": 1.5}]
