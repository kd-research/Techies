from techies.agent import Agent
from techies.task import Task
from techies.crew import Crew

def get_system_crew(crewname, manage_agentops=False, introduce_only=False):
    if manage_agentops:
        import agentops
        agentops.init()

    agent_pool = Agent.eager_load_all()
    task_pool = Task.eager_load_all(agent_pool)

    if isinstance(crewname, str):
        return Crew(
            crewname,
            agent_pool=agent_pool,
            task_pool=task_pool,
            introduce_only=introduce_only
        )
    elif isinstance(crewname, list):
        return [
            Crew(
                crew,
                agent_pool=agent_pool,
                task_pool=task_pool,
                introduce_only=introduce_only
            ) for crew in crewname
        ]
    else:
        raise ValueError("crewname must be a string or a list of strings")
