import re
import crewai
import pytest

from importlib.metadata import version
from crewai_tools import BaseTool, tool
from typing import List
from tests.helpers import expect_all_present, refute_any_present
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

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

class TruthyTools(BaseTool):
    name: str = "TRUTHYTOOL"
    description: str = "TRUTHYTOOL_DESCRIPTION"
    being_called: bool = False

    def _run(self, argument: str) -> str:
        if argument != "TRUTHYTOOL_ARGUMENT":
            raise ValueError(f"Expected TRUTHYTOOL_ARGUMENT, got {argument}")
        self.being_called = True
        return "TRUTHYTOOL_OUTPUT"


# CrewAI agent should see all the information
def test_crewai_should_see_delegation_with_tools():
    agentllm = MockLLM()
    otherllm = MockLLM()

    tool = TruthyTools()

    agent = crewai.Agent(role="AGENT_AGENT", goal="AGENT_GOAL", backstory="AGENT_BACKSTORY", llm=agentllm, allow_delegation=True, tools=[tool])
    # Agent can not re-delegate even if it is allowed
    delegate_agent = crewai.Agent(role="DELEGATE_AGENT", goal="DELEGATE_GOAL", backstory="DELEGATE_BACKSTORY", llm=otherllm, allow_delegation=True)
    task = crewai.Task(description="TASK_DESCRIPTION", expected_output="TAST_EXPECTED_OUTPUT", agent=agent)
    crew = crewai.Crew(agents=[agent, delegate_agent], tasks=[task])
    result = crew.kickoff()

    assert agentllm.called_times == 1
    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, "TRUTHYTOOL,TRUTHYTOOL_DESCRIPTION,Delegate work to coworker,DELEGATE_AGENT".split(",")), \
f"""
CrewAI{version("crewai")} failed to see the delegation when tools are present.
Provided message:
{message}
"""
    assert tool.being_called

    assert otherllm.called_times == 0

    assert result == "my final answer"

class CountingTools(BaseTool):
    name: str = "COUNTINGTOOL"
    description: str = "COUNTINGTOOL_DESCRIPTION"
    number_of_calls: int = 0

    def _run(self) -> str:
        self.number_of_calls += 1
        return f"COUNTINGTOOL_OUTPUT_{self.number_of_calls}"

function_tool_number_of_calls = 0
@tool
def FUNCTIONTOOL():
    "FUNCTIONTOOL_DESCRIPTION"
    global function_tool_number_of_calls
    function_tool_number_of_calls += 1
    return f"FUNCTIONTOOL_OUTPUT_{function_tool_number_of_calls}"

@pytest.mark.parametrize("tool", [CountingTools(), FUNCTIONTOOL])
def test_crewai_should_assume_deterministic_tools(tool):
    agentllm = MockLLM()
    agentllm.responses.append(f"""\
Action: {tool.name}
Action Input: {{}}
""")
    agentllm.responses.append(f"""\
Action: {tool.name}
Action Input: {{}}
""")

    agent = crewai.Agent(role="AGENT_AGENT", goal="AGENT_GOAL", backstory="AGENT_BACKSTORY", llm=agentllm, allow_delegation=False, tools=[tool])
    task = crewai.Task(description="TASK_DESCRIPTION", expected_output="TAST_EXPECTED_OUTPUT", agent=agent)
    crew = crewai.Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()

    assert agentllm.called_times == 3
    assert tool.number_of_calls == 1
    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, [tool.name, tool.description])

    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, f"Observation {tool.name}_OUTPUT_1".split())

    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, "Observation,I tried reusing the same input".split())

    assert result == "my final answer"


@pytest.mark.parametrize("tool", [CountingTools(), FUNCTIONTOOL])
def test_crewai_should_rerun_undeterministic_tools(tool):
    agentllm = MockLLM()
    agentllm.responses.append(f"""\
Action: {tool.name}
Action Input: {{}}
""")
    agentllm.responses.append(f"""\
Action: {tool.name}
Action Input: {{}}
""")

    def never_cache(*_):
        return False
    tool.cache_function = never_cache

    agent = crewai.Agent(role="AGENT_AGENT", goal="AGENT_GOAL", backstory="AGENT_BACKSTORY", llm=agentllm, allow_delegation=False, tools=[tool])
    task = crewai.Task(description="TASK_DESCRIPTION", expected_output="TAST_EXPECTED_OUTPUT", agent=agent)
    crew = crewai.Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()

    assert agentllm.called_times == 3
    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, [tool.name, tool.description])

    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, f"Observation {tool.name}_OUTPUT_1".split())

    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, f"Observation {tool.name}_OUTPUT_2".split()), \
f"""
CrewAI{version("crewai")} failed to rerun the undeterministic tool.
Provided message:
{message}
"""

    assert tool.number_of_calls == 2

    assert result == "my final answer"

