from techies.agent import Agent
from techies.task import Task
from techies.crew import Crew

from langchain_groq import ChatGroq

def get_groq_crew():
    agent_pool = Agent.eager_load_all(llm=ChatGroq(model="llama3-8b-8192"))
    task_pool = Task.eager_load_all(agent_pool)
    crew = Crew(
        'hierarchy_crew',
        agent_pool=agent_pool,
        task_pool=task_pool,
        embedder={
            "provider": "huggingface",
            "config": {
                "model": "sentence-transformers/all-mpnet-base-v2"
            }
        },
        max_rpm=2
    )

    return crew

def get_openai_crew():
    agent_pool = Agent.eager_load_all()
    task_pool = Task.eager_load_all(agent_pool)
    crew = Crew('hierarchy_crew', agent_pool=agent_pool, task_pool=task_pool)

    return crew

get_openai_crew().kickoff()
