import pytest
from falcon import testing

from api.app import app


@pytest.fixture
def api_client() -> testing.TestClient:
    return testing.TestClient(app)
