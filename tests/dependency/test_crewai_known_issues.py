import crewai
import pytest

from importlib.metadata import version
from crewai_tools import BaseTool, tool
from tests.helpers import expect_all_present, refute_any_present, MockLLM


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
    assert otherllm.called_times == 0

    assert str(result) == "my final answer"

class CountingTool(BaseTool):
    name: str = "COUNTINGTOOL"
    description: str = "COUNTINGTOOL_DESCRIPTION"
    number_of_calls: int = 0

    def _run(self) -> str:
        self.number_of_calls += 1
        return f"COUNTINGTOOL_OUTPUT_{self.number_of_calls}"

def setup_function():
    global function_tool_number_of_calls
    function_tool_number_of_calls = 0

@tool
def FUNCTIONTOOL():
    "FUNCTIONTOOL_DESCRIPTION"
    global function_tool_number_of_calls
    function_tool_number_of_calls += 1
    return f"FUNCTIONTOOL_OUTPUT_{function_tool_number_of_calls}"

function_tool_number_of_calls = 0

def get_tool_number_of_calls(tool):
    if tool.name == "COUNTINGTOOL":
        return tool.number_of_calls
    elif tool.name == "FUNCTIONTOOL":
        global function_tool_number_of_calls
        return function_tool_number_of_calls
    else:
        raise ValueError(f"Unknown tool type {tool}")

@pytest.mark.parametrize("tool", [CountingTool(), FUNCTIONTOOL])
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
    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, [tool.name, tool.description])

    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, f"Observation {tool.name}_OUTPUT_1".split())

    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, "Observation,I tried reusing the same input".split(","))

    assert get_tool_number_of_calls(tool) == 1
    assert str(result) == "my final answer"


@pytest.mark.parametrize("tool", [CountingTool(), FUNCTIONTOOL])
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

    assert get_tool_number_of_calls(tool) == 2

    assert str(result) == "my final answer"

