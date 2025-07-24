import pytest


@pytest.fixture
def api_level():
    return "Fixture only for API-tests"


@pytest.fixture
def api_load_level():
    return "API -> load"
