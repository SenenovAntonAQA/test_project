import pytest


@pytest.fixture
def load_level():
    return "Fixture only for load tests"


@pytest.fixture
def api_load_level(api_load_level):
    return f"redefinition '{api_load_level}'"
