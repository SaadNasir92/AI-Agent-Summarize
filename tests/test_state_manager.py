# tests/test_state_manager.py
import pytest
from state_manager import set_workflow_state, get_workflow_state, delete_workflow_state


@pytest.fixture(autouse=True)
def use_fakeredis(monkeypatch):
    import fakeredis

    fake_redis = fakeredis.FakeStrictRedis(decode_responses=True)
    monkeypatch.setattr("state_manager.redis.Redis", lambda *args, **kwargs: fake_redis)


def test_workflow_state():
    workflow_id = "test123"
    set_workflow_state(workflow_id, "processing")
    state = get_workflow_state(workflow_id)
    assert state == "processing"
    delete_workflow_state(workflow_id)
    state = get_workflow_state(workflow_id)
    assert state is None
