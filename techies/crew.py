from techies.fixture_loader import load_fixture
from crewai import Crew as _Crew


class Crew(_Crew):
    input_args: list[str] = []
    def __init__(self, config_name, *, agent_pool, task_pool, **kwargs):
        introduction_task_override = kwargs.get('introduce_only', False)
        del kwargs['introduce_only']

        crew_config = load_fixture('crews')[config_name]

        agents = []
        for agent_name in crew_config.get('agents'):
            agents.append(agent_pool.get(agent_name))

        tasks = []
        for task_name in crew_config.get('tasks'):
            tasks.append(task_pool.get(task_name))

        if introduction_task_override:
            agents.append(agent_pool.get('introduction_host'))
            tasks = [task_pool.get('introduce_crew_members')]

        crew_config['agents'] = agents
        crew_config['tasks'] = tasks

        # Extract input_args from crew_config but don't set it yet
        input_args = crew_config.pop('input_args', [])

        crew_config.update(kwargs)
        super().__init__(**crew_config)
        
        # Set input_args after parent initialization to avoid Pydantic issues
        self.input_args = input_args

    @staticmethod
    def list_crews():
        return load_fixture('crews', result="locations")
