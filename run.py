from techies.agent import Agent
from techies.task import Task
from techies.crew import Crew

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
    agent_pool = Agent.eager_load_all()
    task_pool = Task.eager_load_all(agent_pool)
    crew = Crew('hierarchy_crew', agent_pool=agent_pool, task_pool=task_pool)

    return crew

game_specifications = """
NumSeq Scramble is a strategic board game where players aim to form the longest
sequences of the same digit on a 15x15 grid to score points. Each player starts
with 7 number tiles, drawing from a bag, and takes turns placing tiles to build
or extend sequences horizontally or vertically. Valid moves must connect to
existing sequences, and players draw new tiles to maintain 7 in hand. Points
are awarded based on sequence length, with bonuses for special tiles and
multiple sequences in one turn. The game includes wild tiles, combo bonuses,
and blocking strategies. It ends when no more valid moves are possible, and the
player with the highest score wins. Variations include timed turns, team play,
and advanced modes. The game promotes numerical recognition, strategic
thinking, and problem-solving skills, blending the familiar Scrabble format
with numerical challenges.
"""

inputs = { "game_specifications": " ".join(game_specifications.split()) }

get_openai_crew().kickoff(inputs=inputs)
