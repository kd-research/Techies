from techies.fixture_loader import load_fixture
from crewai import Task as _Task


class Task(_Task):
    @staticmethod
    def eager_load_all(agent_pool):
        task_pool = {}
        for config_name in load_fixture('tasks').keys():
            if not config_name.startswith('_'):
                Task(config_name, agent_pool=agent_pool, task_pool=task_pool)
        return task_pool

    def __init__(self, config_name, *, agent_pool, task_pool, **kwargs):
        task_config = load_fixture('tasks')[config_name]

        agent = agent_pool.get(task_config['agent'])
        task_config['agent'] = agent

        context = []
        for context_name in task_config.pop('depends_on', []):
            context.append(task_pool.get(context_name))

        task_pool[config_name] = self
        super().__init__(**task_config, **kwargs)
