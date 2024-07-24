from techies.fixture_loader import load_fixture
from crewai import Crew as _Crew


class Crew(_Crew):
    def __init__(self, config_name, *, agent_pool, task_pool, **kwargs):
        crew_config = load_fixture('crews')[config_name]

        agents = []
        for agent_name in crew_config.get('agents'):
            agents.append(agent_pool.get(agent_name))
        crew_config['agents'] = agents

        tasks = []
        for task_name in crew_config.get('tasks'):
            tasks.append(task_pool.get(task_name))
        crew_config['tasks'] = tasks

        crew_config.update(kwargs)
        super().__init__(**crew_config)

    @staticmethod
    def list_crews():
        return load_fixture('crews', result="locations")
