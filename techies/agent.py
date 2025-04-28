from techies.fixture_loader import load_fixture
from techies.tools import get_all_tools
from crewai import Agent as _Agent



class Agent(_Agent):
    @staticmethod
    def eager_load_all(**extra_kwargs):

        agent_pool = {}
        all_tools = get_all_tools()
        for config_name in load_fixture('agents').keys():
            if not config_name.startswith('_'):
                agent = Agent(
                    config_name,
                    agent_pool=agent_pool,
                    tools_available=all_tools,
                    **extra_kwargs
                )

        return agent_pool

    def __init__(
        self, config_name, *, agent_pool=None, tools_available=None, **kwargs
    ):
        agent_config = load_fixture('agents')[config_name]
        agent_config['role'] = config_name
        agent_config['name'] = config_name.replace('_', ' ').title()

        agent_tools = []
        for tool_name in agent_config.get('tools', []):
            # intentionally raise if tool is not available
            agent_tools.append(tools_available[tool_name])

        agent_config['tools'] = agent_tools

        if agent_pool is not None:
            agent_pool[config_name] = self

        agent_config.update(kwargs)
        super().__init__(**agent_config)

