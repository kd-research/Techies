import re
import crewai
import pytest

from crewai_tools import BaseTool
from tests.helpers import expect_all_present, refute_any_present, MockLLM

# CrewAI agent should see all the information
def test_crewai_calls_llm():
    agentllm = MockLLM()
    otherllm = MockLLM()

    agent = crewai.Agent(role="AGENT_AGENT", goal="AGENT_GOAL", backstory="AGENT_BACKSTORY", llm=agentllm, allow_delegation=False)
    unused_agent = crewai.Agent(role="UNUSEDAGENT_AGENT", goal="UNUSEDAGENT_GOAL", backstory="UNUSEDAGENT_BACKSTORY", llm=otherllm)
    task = crewai.Task(description="TASK_DESCRIPTION", expected_output="TAST_EXPECTED_OUTPUT", agent=agent)
    crew = crewai.Crew(agents=[agent, unused_agent], tasks=[task])
    result = crew.kickoff()

    assert agentllm.called_times == 1
    assert expect_all_present(agentllm.last_messages[-1], "AGENT_AGENT AGENT_GOAL AGENT_BACKSTORY TASK_DESCRIPTION TAST_EXPECTED_OUTPUT".split())
    assert otherllm.called_times == 0

    assert str(result) == "my final answer"

# When the agent is not allowed to delegate, it should not see any other agent
def test_agent_should_sees_no_delegation():
    agentllm = MockLLM()
    otherllm = MockLLM()

    agent = crewai.Agent(role="AGENT_AGENT", goal="AGENT_GOAL", backstory="AGENT_BACKSTORY", llm=agentllm, allow_delegation=False)
    unused_agent = crewai.Agent(role="UNUSEDAGENT_AGENT", goal="UNUSEDAGENT_GOAL", backstory="UNUSEDAGENT_BACKSTORY", llm=otherllm)
    task = crewai.Task(description="TASK_DESCRIPTION", expected_output="TAST_EXPECTED_OUTPUT", agent=agent)
    crew = crewai.Crew(agents=[agent, unused_agent], tasks=[task])
    result = crew.kickoff()

    assert agentllm.called_times == 1
    refute_any_present(agentllm.last_messages[-1], "Delegate work to coworker,Ask question to coworker,UNUSEDAGENT_AGENT".split(","))
    assert otherllm.called_times == 0

    assert str(result) == "my final answer"

def test_crewai_seeing_delegation():
    agentllm = MockLLM()
    agentllm.responses.append("""\
Action: Delegate work to coworker
Action Input: {"task": "DELEGATE_GOAL", "context": "DELEGATE_BACKSTORY", coworker: "DELEGATE_AGENT"}
""")
    agentllm.responses.append("Thought: I now can give a great answer\nFinal Answer: my final answer")

    otherllm = MockLLM()
    otherllm.responses.append("Thought: I now can give a great answer\nFinal Answer: DELEGATE_AGENT's final answer")

    agent = crewai.Agent(role="AGENT_AGENT", goal="AGENT_GOAL", backstory="AGENT_BACKSTORY", llm=agentllm, allow_delegation=True)
    # Agent can not re-delegate even if it is allowed
    delegate_agent = crewai.Agent(role="DELEGATE_AGENT", goal="DELEGATE_GOAL", backstory="DELEGATE_BACKSTORY", llm=otherllm, allow_delegation=True)
    task = crewai.Task(description="TASK_DESCRIPTION", expected_output="TAST_EXPECTED_OUTPUT", agent=agent)
    crew = crewai.Crew(agents=[agent, delegate_agent], tasks=[task])
    result = crew.kickoff()

    assert agentllm.called_times == 2
    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, "Delegate work to coworker,DELEGATE_AGENT".split(","))

    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, "Observation,DELEGATE_AGENT's final answer".split(","))

    assert otherllm.called_times == 1
    message = otherllm.last_messages.pop(0)
    assert expect_all_present(message, "DELEGATE_GOAL DELEGATE_BACKSTORY".split())
    assert refute_any_present(message, "Delegate work to coworker,AGENT_AGENT".split(","))

    assert str(result) == "my final answer"


class TruthyTools(BaseTool):
    name: str = "TRUTHYTOOL"
    description: str = "TRUTHYTOOL_DESCRIPTION"
    being_called: bool = False

    def _run(self, argument: str) -> str:
        if argument != "TRUTHYTOOL_ARGUMENT":
            raise ValueError(f"Expected TRUTHYTOOL_ARGUMENT, got {argument}")
        self.being_called = True
        return "TRUTHYTOOL_OUTPUT"

def test_crewai_seeing_tools_through_agent():
    agentllm = MockLLM()
    agentllm.responses.append("""\
Action: TRUTHYTOOL
Action Input: {"argument": "TRUTHYTOOL_ARGUMENT"}
""")
    agentllm.responses.append("Thought: I now can give a great answer\nFinal Answer: AGENT_AGENT's final answer")
    otherllm = MockLLM()
    otherllm.responses.append("Thought: I now can give a great answer\nFinal Answer: OTHER_AGENT's final answer")

    tool = TruthyTools()

    agent = crewai.Agent(role="AGENT_AGENT", goal="AGENT_GOAL", backstory="AGENT_BACKSTORY", llm=agentllm, allow_delegation=False, tools=[tool])
    other_agent = crewai.Agent(role="OTHER_AGENT", goal="OTHER_GOAL", backstory="OTHER_BACKSTORY", llm=otherllm, allow_delegation=False)
    task = crewai.Task(description="TASK_DESCRIPTION", expected_output="TAST_EXPECTED_OUTPUT", agent=agent)
    other_task = crewai.Task(description="OTHER_TASK_DESCRIPTION", expected_output="OTHER_TAST_EXPECTED_OUTPUT", agent=other_agent)
    crew = crewai.Crew(agents=[other_agent, agent], tasks=[task, other_task])
    result = crew.kickoff()

    assert agentllm.called_times == 2
    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, "TRUTHYTOOL TRUTHYTOOL_DESCRIPTION".split())
    assert tool.being_called

    message = agentllm.last_messages.pop(0)
    assert expect_all_present(message, "Observation TRUTHYTOOL_OUTPUT".split())

    assert otherllm.called_times == 1
    message = otherllm.last_messages.pop(0)
    assert refute_any_present(message, "TRUTHYTOOL TRUTHYTOOL_DESCRIPTION".split())

    assert str(result) == "OTHER_AGENT's final answer"

