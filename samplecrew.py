from functools import lru_cache
from crewai import Agent, Task, Crew, Process

from langchain.agents import load_tools
from langchain_community.llms.ollama import Ollama
from langchain_groq import ChatGroq


@lru_cache
def ollama_model():
    return Ollama(
        base_url="http://localhost:11434",
        model="llama3:8b",
    )


@lru_cache
def groq_model():
    return ChatGroq(model="llama3-70b-8192", )

@lru_cache
def huggingface_embedder():
    return {
        "provider": "huggingface",
        "config":
            {
                "model":
                    "sentence-transformers/all-mpnet-base-v2",
            }
    }

@lru_cache
def gpt4all_embedder():
    return {
        "provider": "gpt4all",
    }


llm = groq_model()

llm_config = dict(
    memory=True,
    embedder=huggingface_embedder(),
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
    output_file="tldr_summary.txt",
    agent=agent2,
    context=[task1],
)

my_crew = Crew(
    agents=[agent1, agent2],
    tasks=[task1, task2],
    verbose=True,
    process=Process.sequential,
    **llm_config,
    max_rpm=1,
    max_iter=1,
)

crew = my_crew.kickoff(inputs={"input": "Chris Lee (singer)"})
