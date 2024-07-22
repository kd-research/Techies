from techies.agent import Agent
from techies.task import Task
from techies.crew import Crew
from techies.game_specs import game_specs
import agentops

agentops.init()

def get_groq_crew():
    from langchain_groq import ChatGroq

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
    from langchain_openai import ChatOpenAI

    agent_pool = Agent.eager_load_all(llm=ChatOpenAI(model="gpt-4o", temperature=0.2))
    task_pool = Task.eager_load_all(agent_pool)
    crew = Crew('hierarchy_crew', agent_pool=agent_pool, task_pool=task_pool)

    return crew


def main():
    inputs = { "game_specifications": game_specs("NumSeq_game_specifications") }
    get_openai_crew().kickoff(inputs=inputs)
