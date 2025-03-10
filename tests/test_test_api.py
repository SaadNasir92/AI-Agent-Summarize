# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_start_workflow(client, monkeypatch):
    # Create a dummy task class.
    class DummyTask:
        id = "dummy_task_id"

    def dummy_delay(source, destination, email):
        return DummyTask()

    # Override the run_workflow.delay call.
    monkeypatch.setattr("tasks.run_workflow.delay", dummy_delay)
    response = client.post(
        "/start_workflow/",
        json={"source": "local", "destination": "local", "email": "test@example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == "dummy_task_id"
    assert "Workflow started" in data["message"]
