from tests.helpers import is_openai_available

def test_openai_availability():
    assert is_openai_available() == (True, None)
