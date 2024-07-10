from techies.agent import Agent
from techies.task import Task
from techies.crew import Crew

agent_pool = Agent.eager_load_all()
task_pool = Task.eager_load_all(agent_pool)
crew = Crew('hierarchy_crew', agent_pool=agent_pool, task_pool=task_pool)

crew.kickoff()

