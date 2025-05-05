from techies.fixture_loader import load_fixture
from techies.tools import get_all_tools, validate_tool
from crewai import Agent as _Agent
import jsonschema
from techies.config_schema import AGENT_SCHEMA



class Agent(_Agent):
    @staticmethod
    def eager_load_all(tools=None, **extra_kwargs):

        agent_pool = {}
        all_tools = get_all_tools() if tools is None else tools
        for config_name in load_fixture('agents').keys():
            if not config_name.startswith('_'):
                agent = Agent(
                    config_name,
                    agent_pool=agent_pool,
                    tools_available=all_tools,
                    **extra_kwargs
                )

        return agent_pool

    @staticmethod
    def list_agents():
        """List available agents with their locations."""
        return load_fixture('agents', result="locations")
        
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

    @staticmethod
    def validate(name, recursive=True):
        """
        Validate the agent with the given name.
        Returns (True, None) on success, (False, 'failure-reason') on failure.
        """
        # Check if agent exists
        agent_configs = load_fixture('agents')
        if name not in agent_configs:
            return False, f"Agent '{name}' not found"
        
        # Validate schema
        agent_config = agent_configs[name]
        try:
            jsonschema.validate(agent_config, schema=AGENT_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            return False, f"Agent '{name}' schema validation failed: {e.message}"
        
        # If recursive, validate tools
        if recursive and 'tools' in agent_config:
            errors = []
            for tool_name in agent_config['tools']:
                ok, reason = validate_tool(tool_name, recursive=False)
                if not ok:
                    errors.append(f"Tool '{tool_name}': {reason}")
            
            if errors:
                return False, f"Agent '{name}' uses invalid tools:\n" + "\n".join(errors)
        
        return True, None

