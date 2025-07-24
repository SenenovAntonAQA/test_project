def test_api0(zero_level):
    assert zero_level == "fixture for all tests"

def test_api1(api_level):
    assert api_level == "Fixture only for API-tests"

def test_api2(api_load_level):
    assert api_load_level == "API -> load"