from crewai import Agent, Task, Crew

from langchain.agents import load_tools
from langchain_community.llms.ollama import Ollama

llm = Ollama(
    base_url="http://localhost:11434",
    model="llama3:70b",
)
llm_config = dict(
    memory=True,
    embedder={
        "provider": "huggingface",
        "config":
            {
                "model":
                    "mixedbread-ai/mxbai-embed-large-v1",  # https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1
            }
    }
)

langchain_tools = load_tools(["google-serper"], llm=llm)

agent1 = Agent(
    role="backstory agent",
    goal="Gives an update-to-date result of who is {input}?",
    backstory="agent backstory",
    tools=langchain_tools,
    verbose=True,
    llm=llm,
)

task1 = Task(
    expected_output="a short biography of {input}",
    description="a short biography of {input}",
    agent=agent1,
)

agent2 = Agent(
    role="bio agent",
    goal="summarize the short bio for {input} and if needed do more research",
    backstory="agent backstory",
    llm=llm,
)

task2 = Task(
    description="a tldr summary of the short biography",
    expected_output="5 bullet point summary of the biography",
    agent=agent2,
    context=[task1],
)

my_crew = Crew(
    agents=[agent1, agent2], tasks=[task1, task2], verbose=True, **llm_config

)

crew = my_crew.kickoff(inputs={"input": "Chris Lee (singer)"})
