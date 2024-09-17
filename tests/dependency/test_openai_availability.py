import os
import pytest

from tests.helpers import is_openai_available

@pytest.mark.skipif(not "OPENAI_TEST_KEY" in os.environ, reason="OPENAI_TEST_KEY is not set")
def test_openai_availability():
    assert is_openai_available() == (True, None)
