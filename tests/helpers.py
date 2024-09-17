import os
import functools
import re

from openai import OpenAI, AuthenticationError, RateLimitError
from typing import List
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

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

class MockLLM(BaseChatModel):
    DEFAULT_RESPONSE = "Thought: I now can give a great answer\nFinal Answer: my final answer"
    called_times: int = 0
    last_messages: List[str] = []
    responses: List[str] = []

    def _generate(self, messages, **kwargs):
        self.called_times += 1
        self.last_messages.append(messages[-1].content)
        response = self.responses.pop(0) if self.responses else self.DEFAULT_RESPONSE
        return ChatResult(generations=[ChatGeneration(message=AIMessage(content=response))])

    @property
    def _llm_type(self):
        return "mocked"

