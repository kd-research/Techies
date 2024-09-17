import os
import crewai
import pytest
import shutil

from tempfile import TemporaryDirectory
from importlib.metadata import version
from tests.helpers import expect_all_present, refute_any_present, MockLLM

from techies.tools import get_all_tools

@pytest.fixture
def temp_dir():
    temp_dir = TemporaryDirectory()
    old_dir = os.getcwd()

    os.chdir(temp_dir.name)
    yield temp_dir

    os.chdir(old_dir)
    temp_dir.cleanup()


# CrewAI agent should see all the information
@pytest.mark.focus
def test_crewai_can_list_file_twice(temp_dir):
    agentllm = MockLLM()
    agentllm.responses.append("""\
Action: List Existing Files
Action Input: {}
""")
    agentllm.responses.append("""\
Action: List Existing Files
Action Input: {}
""")

    tool = get_all_tools()['list_files']

    agent = crewai.Agent(role="AGENT_AGENT", goal="AGENT_GOAL", backstory="AGENT_BACKSTORY", llm=agentllm, allow_delegation=False, tools=[tool])
    task = crewai.Task(description="TASK_DESCRIPTION", expected_output="TAST_EXPECTED_OUTPUT", agent=agent)
    crew = crewai.Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()

    assert agentllm.called_times == 3
    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, ["List Existing Files"])

    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, "Observation,Theres nothing to be listed".split(","))

    message = agentllm.last_messages.pop(0)
    assert refute_any_present(message, "Observation,I tried reusing the same input".split(","))

    assert str(result) == "my final answer"
