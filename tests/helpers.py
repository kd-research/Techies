import os
import functools
import re

from openai import OpenAI, AuthenticationError, RateLimitError

@functools.lru_cache(maxsize=1)
def is_openai_available():
    if "OPENAI_TEST_KEY" not in os.environ:
        return False, "OPENAI_TEST_KEY is not set"

    del os.environ["OPENAI_API_KEY"]

    client = OpenAI(api_key=os.environ["OPENAI_TEST_KEY"])

    try:
        client.models.list()
    except AuthenticationError as e:
        print(e)
        return False, "API key is invalid"

    try:
        chat_completion = client.chat.completions.create(
            messages=[ { "role": "user", "content": "This is a test", } ],
            model="gpt-4o-mini",
        )
    except RateLimitError as e:
        print(e)
        return False, "API rate limit exceeded"

    return True, None

def expect_all_present(string, targets):
    return all((target in string) for target in targets)

def refute_any_present(string, targets):
    return not any((target in string) for target in targets)

