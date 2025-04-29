from techies.fixture_loader import load_fixture
from crewai import Crew as _Crew
import jsonschema
from techies.config_schema import CREW_SCHEMA
from functools import lru_cache
from techies.agent import Agent
from techies.task import Task
from techies.utils import is_topology_ordered


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

    @staticmethod
    @lru_cache(maxsize=128)
    def _validate_schema(name):
        """
        Validate crew configuration against the schema.
        
        Args:
            name: Name of the crew to validate
            
        Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
        """
        # Check if crew exists
        crew_configs = load_fixture('crews')
        if name not in crew_configs:
            return False, f"Crew '{name}' not found"
        
        # Validate schema
        try:
            jsonschema.validate(crew_configs[name], schema=CREW_SCHEMA)
            return True, None
        except jsonschema.exceptions.ValidationError as e:
            return False, f"Crew '{name}' schema validation failed: {e.message}"

    @staticmethod
    @lru_cache(maxsize=128)
    def _validate_agents(name):
        """
        Validate all agents in the crew.
        Assumes schema has already been validated.
        
        Args:
            name: Name of the crew to validate
            
        Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
        """
        # Get crew config
        crew_config = load_fixture('crews')[name]
        agent_names = crew_config.get('agents', [])
        
        # Validate each agent
        errors = []
        for agent_name in agent_names:
            ok, reason = Agent.validate(agent_name, recursive=True)
            if not ok:
                errors.append(f"Agent '{agent_name}': {reason}")
        
        if errors:
            return False, f"Crew '{name}' has invalid agents:\n" + "\n".join(errors)
        
        return True, None
    
    @staticmethod
    @lru_cache(maxsize=128)
    def _validate_tasks(name):
        """
        Validate all tasks in the crew, ensuring they are in topological order.
        Assumes schema has already been validated.
        
        Args:
            name: Name of the crew to validate
            
        Returns:
            Tuple[bool, Optional[str]]: (success, error_message)
        """
        # Get crew config
        crew_config = load_fixture('crews')[name]
        task_names = crew_config.get('tasks', [])
        
        # Get task dependency graph
        vertices, edges = Task.task_graph()
        
        # Check if tasks are in topological order
        if not is_topology_ordered(edges, reversed(task_names)):
            return False, f"Crew '{name}' tasks are not in valid topological order"
        
        # Validate each task
        errors = []
        for task_name in task_names:
            ok, reason = Task.validate(task_name, recursive=True)
            if not ok:
                errors.append(f"Task '{task_name}': {reason}")
        
        if errors:
            return False, f"Crew '{name}' has invalid tasks:\n" + "\n".join(errors)
        
        return True, None
    
    @staticmethod
    def validate(name, recursive=True):
        """
        Validate the crew with the given name.
        If recursive=True, also validates all agents and tasks in the crew.
        
        Returns (True, None) on success, (False, 'failure-reason') on failure.
        """
        # Always validate the schema first
        ok, reason = Crew._validate_schema(name)
        if not ok:
            return ok, reason
            
        # If not recursive, just return schema validation result
        if not recursive:
            return True, None
            
        # Validate agents
        ok, reason = Crew._validate_agents(name)
        if not ok:
            return ok, reason
            
        # Validate tasks
        ok, reason = Crew._validate_tasks(name)
        if not ok:
            return ok, reason
            
        return True, None
