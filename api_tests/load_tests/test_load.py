def test_load0(zero_level):
    assert zero_level == "fixture for all tests"

def test_load1(api_load_level):
    assert api_load_level == "redefinition 'API -> load'"

def test_load2(load_level):
    assert load_level == "Fixture only for load tests"